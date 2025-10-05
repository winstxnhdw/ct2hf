from __future__ import annotations

from functools import partial
from json import load
from logging import INFO, basicConfig, getLogger
from pathlib import Path
from shutil import rmtree
from typing import TYPE_CHECKING, Any, Callable
from weakref import finalize

from ctranslate2.converters import TransformersConverter
from huggingface_hub import HfApi
from huggingface_hub.constants import DEFAULT_REVISION, HF_HUB_CACHE
from huggingface_hub.file_download import repo_folder_name

if TYPE_CHECKING:
    from ct2hf.parse_args import Arguments


def clean_up(*, storage_path: str | Path, output_directory: str | Path) -> None:
    rmtree(storage_path, ignore_errors=True)
    rmtree(output_directory, ignore_errors=True)


def upload_to_huggingface(repository_directory: Path) -> str:
    hf_api = HfApi()
    repository_id = f"{hf_api.whoami()['name']}/{repository_directory}"

    repo_url = hf_api.create_repo(repository_id, exist_ok=True)
    hf_api.upload_folder(
        repo_id=repository_id,
        folder_path=repository_directory,
        commit_message=f"feat: add {repository_directory} model",
    )

    return repo_url


def generate_gitattributes(repository_directory: Path, min_lfs_size: int = 10485760) -> Path:
    with (repository_directory / ".gitattributes").open("w", encoding="utf-8") as file:
        file.writelines(
            f"{path.relative_to(repository_directory).as_posix()} filter=lfs diff=lfs merge=lfs -text\n"
            for path in repository_directory.rglob("*")
            if path.is_file() and path.stat().st_size > min_lfs_size
        )

    return repository_directory


def load_model_patch(load_model: Callable[..., Any], model_refs_path: Path, *_, **kwargs: Any) -> Any:  # noqa: ANN401
    with (
        model_refs_path.open("r") as commit_hash,
        (model_refs_path.parent.parent / "snapshots" / commit_hash.read().strip() / "config.json").open("r") as json,
    ):
        config = load(json)

    kwargs.pop("torch_dtype")
    kwargs["dtype"] = config.get("dtype") or config.get("torch_dtype") or "bfloat16"

    return load_model(*_, **kwargs)


def convert(args: Arguments) -> None:
    basicConfig(level=INFO, format="%(message)s")
    logger = getLogger(__name__)
    storage_path = Path(HF_HUB_CACHE) / repo_folder_name(repo_id=args.model_id, repo_type="model")
    refs_path = storage_path / "refs" / (args.revision or DEFAULT_REVISION)
    model_name = args.model_id.split("/", 1)[1]
    quantisation = args.quantisation
    output_directory = args.output_name or f"{model_name}-ct2-{quantisation}" if quantisation else f"{model_name}-ct2"

    if not args.preserve_models:
        finalize(
            args,
            clean_up,
            storage_path=storage_path,
            output_directory=output_directory,
        )

    converter = TransformersConverter(
        args.model_id,
        copy_files=args.files_to_copy,
        load_as_float16=True,
        revision=args.revision,
        low_cpu_mem_usage=not args.compatibility,
        trust_remote_code=True,
    )

    converter.load_model = partial(load_model_patch, converter.load_model, refs_path)
    converted_model_path = Path(converter.convert(output_directory, quantization=quantisation))
    repository_path = generate_gitattributes(converted_model_path)
    repository_url = upload_to_huggingface(repository_path)

    logger.info("Successfully converted and uploaded the model to %s", repository_url)
