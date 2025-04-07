from __future__ import annotations

from argparse import ArgumentParser
from pathlib import Path
from shutil import rmtree
from typing import Literal, NamedTuple
from weakref import finalize

from ctranslate2.converters import TransformersConverter
from huggingface_hub import HfApi
from huggingface_hub.constants import HF_HUB_CACHE
from huggingface_hub.file_download import repo_folder_name


class Arguments(NamedTuple):
    model_id: str
    output_name: str | None
    revision: str | None
    files_to_copy: list[str]
    preserve_models: bool
    compatibility: bool
    quantisation: Literal[
        None,
        "int8",
        "int8_float32",
        "int8_float16",
        "int8_bfloat16",
        "int16",
        "float16",
        "bfloat16",
        "float32",
    ]


def parse_args() -> Arguments:
    parser = ArgumentParser(description="convert and upload a transformer model to huggingface")
    parser.add_argument("model_id", type=str, help="transformer model to convert")
    parser.add_argument("--output-name", type=str, help="name of the output model")
    parser.add_argument("--revision", type=str, help="revision of the model to convert")
    parser.add_argument("--files-to-copy", type=str, nargs="+", help="files to copy to the output model", default=[])
    parser.add_argument("--preserve-models", action="store_true", help="do not delete the downloaded models")
    parser.add_argument("--compatibility", action="store_true", help="better compatibility but higher memory usage")
    parser.add_argument(
        "--quantisation",
        type=lambda choice: None if (quantisation := choice.lower()) == "none" else quantisation,
        help="quantisation type",
        default="int8",
        choices=[
            None,
            "int8",
            "int8_float32",
            "int8_float16",
            "int8_bfloat16",
            "int16",
            "float16",
            "bfloat16",
            "float32",
        ],
    )

    return parser.parse_known_args()[0]  # pyright: ignore [reportReturnType]


def clean_up(*, storage_path: str | Path, output_directory: str | Path, preserve_models: bool) -> None:
    if preserve_models:
        return

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
            f"{path.relative_to(repository_directory)} filter=lfs diff=lfs merge=lfs -text\n"
            for path in repository_directory.rglob("*")
            if path.is_file() and path.stat().st_size > min_lfs_size
        )

    return repository_directory


def main() -> None:
    args = parse_args()
    storage_path = Path(HF_HUB_CACHE) / repo_folder_name(repo_id=args.model_id, repo_type="model")
    model_name = args.model_id.split("/", 1)[1]
    quantisation = args.quantisation
    output_directory = args.output_name or f"{model_name}-ct2-{quantisation}" if quantisation else f"{model_name}-ct2"

    finalize(
        args,
        clean_up,
        storage_path=storage_path,
        output_directory=output_directory,
        preserve_models=args.preserve_models,
    )

    converter = TransformersConverter(
        args.model_id,
        copy_files=args.files_to_copy,
        load_as_float16=True,
        revision=args.revision,
        low_cpu_mem_usage=not args.compatibility,
        trust_remote_code=True,
    )

    converted_model_path = Path(converter.convert(output_directory, quantization=quantisation))
    repository_path = generate_gitattributes(converted_model_path)
    repository_url = upload_to_huggingface(repository_path)

    print(f"Successfully converted and uploaded the model to {repository_url}")  # noqa: T201


if __name__ == "__main__":
    main()
