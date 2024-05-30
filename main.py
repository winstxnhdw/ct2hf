from pathlib import Path
from shutil import rmtree

from ctranslate2.converters import TransformersConverter
from huggingface_hub import HfApi, snapshot_download


def clean_up(converted_model: str, snapshot_path: str):
    rmtree(Path(snapshot_path).parent.parent)
    rmtree(converted_model)


def upload_to_huggingface(converted_model: str):
    repository_id = f'winstxnhdw/{converted_model}'
    hf_api = HfApi()
    hf_api.create_repo(repository_id, exist_ok=True)
    hf_api.delete_file('.gitattributes', repository_id)
    hf_api.upload_folder(
        repo_id=repository_id,
        folder_path=converted_model,
        commit_message=f'feat: add {converted_model} model',
    )


def generate_gitattributes(converted_model: str):
    converted_model_path = Path(converted_model)

    with open(converted_model_path / '.gitattributes', 'w', encoding='utf-8') as file:
        file.writelines(
            f'{path.relative_to(converted_model_path)} filter=lfs diff=lfs merge=lfs -text'
            for path in converted_model_path.rglob('*') if path.is_file() and path.stat().st_size > 10485760
        )


def main():
    model_owner = 'openchat'
    model_name = 'openchat-3.6-8b-20240522'
    output_model_name = 'openchat-3.6'

    files_to_copy = [
        'tokenizer.json',
        'tokenizer_config.json',
    ]

    model = f'{model_owner}/{model_name}'
    snapshot_path = snapshot_download(model)

    converter = TransformersConverter(
        model,
        copy_files=files_to_copy,
        load_as_float16=True,
        low_cpu_mem_usage=True,
        trust_remote_code=True,
    )

    converted_model = converter.convert(
        f'{output_model_name or model_name}-ct2-int8',
        quantization='int8',
        force=True,
    )

    generate_gitattributes(converted_model)
    upload_to_huggingface(converted_model)
    clean_up(converted_model, snapshot_path)


if __name__ == '__main__':
    main()
