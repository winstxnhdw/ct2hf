from pathlib import Path
from shutil import rmtree

from ctranslate2.converters import TransformersConverter
from huggingface_hub import HfApi
from huggingface_hub.constants import HF_HUB_CACHE
from huggingface_hub.file_download import repo_folder_name
from typing_extensions import Self


class ModelConverter:
    __slots__ = ('preserve_models', 'storage_path', 'output_directory', 'converted_model_path')

    def __init__(
        self,
        model_id: str,
        output_name: str,
        preserve_models: bool,
        files_to_copy: list[str],
    ):
        converter = TransformersConverter(
            model_id,
            copy_files=files_to_copy,
            load_as_float16=True,
            low_cpu_mem_usage=True,
            trust_remote_code=True,
        )

        self.preserve_models = preserve_models
        self.storage_path = Path(HF_HUB_CACHE) / repo_folder_name(repo_id=model_id, repo_type='model')
        self.output_directory = output_name or f"{model_id.split('/')[1]}-ct2-int8"
        self.converted_model_path = Path(converter.convert(self.output_directory, quantization='int8'))

    def __enter__(self) -> Self:
        if not self.preserve_models:
            rmtree(self.storage_path, ignore_errors=True)

        return self

    def __exit__(self, *_):
        if self.preserve_models:
            return

        rmtree(self.storage_path, ignore_errors=True)
        rmtree(self.converted_model_path, ignore_errors=True)

    def generate_gitattributes(self):
        with open(self.converted_model_path / '.gitattributes', 'w', encoding='utf-8') as file:
            file.writelines(
                f'{path.relative_to(self.converted_model_path)} filter=lfs diff=lfs merge=lfs -text'
                for path in self.converted_model_path.rglob('*')
                if path.is_file() and path.stat().st_size > 10485760
            )

    def upload_to_huggingface(self):
        hf_api = HfApi()
        repository_id = f"{hf_api.whoami()['name']}/{self.output_directory}"

        hf_api.create_repo(repository_id, exist_ok=True)
        hf_api.upload_folder(
            repo_id=repository_id,
            folder_path=self.output_directory,
            commit_message=f'feat: add {self.output_directory} model',
        )
