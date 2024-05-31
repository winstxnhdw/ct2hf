from pathlib import Path
from shutil import rmtree

from ctranslate2.converters import TransformersConverter
from huggingface_hub import HfApi, snapshot_download
from argparse import ArgumentParser


def clean_up(snapshot_path: Path, converted_model: str):
    rmtree(snapshot_path)
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

    with open(converted_model_path/'.gitattributes', 'w', encoding='utf-8') as file:
        file.writelines(
            f'{path.relative_to(converted_model_path)} filter=lfs diff=lfs merge=lfs -text'
            for path in converted_model_path.rglob('*') if path.is_file() and path.stat().st_size > 10485760
        )


def convert_model(model_id: str, output_name: str, files_to_copy: list[str], snapshot_path: Path) -> str:
    converter = TransformersConverter(
        model_id,
        copy_files=files_to_copy,
        load_as_float16=True,
        low_cpu_mem_usage=True,
        trust_remote_code=True,
    )

    converted_model_path = converter.convert(
        output_name or f"{model_id.split('/')[1]}-ct2-int8",
        quantization='int8',
        force=True,
    )

    rmtree(snapshot_path)

    return converted_model_path


class ModelConverter:
    def __init__(self):
        pass


    def __enter__(self):
        return self


    def __exit__(self, *_):
        pass


def parse_args():
    parser = ArgumentParser(description='convert and upload a transformer model to huggingface')
    parser.add_argument('model_id', type=str, help='transformer model to convert')
    parser.add_argument('--output_name', type=str, help='name of the output model')
    parser.add_argument('--files_to_copy', type=str, nargs='+', help='files to copy to the output model', default=[])

    return parser.parse_known_args()[0]


def main():
    args = parse_args()

    files_to_copy = [
        'tokenizer.json',
        'tokenizer_config.json',
        *args.files_to_copy
    ]


    try:
        snapshot_path = Path(snapshot_download(args.model_id)).parent.parent
        converted_model = convert_model(args.model_id, args.output_name, files_to_copy, snapshot_path)
        generate_gitattributes(converted_model)
        upload_to_huggingface(converted_model)

    finally:
        clean_up(snapshot_path, converted_model)


if __name__ == '__main__':
    main()
