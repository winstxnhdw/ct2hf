from argparse import ArgumentParser, Namespace

from ct2hf.model_converter import ModelConverter


def parse_args() -> Namespace:
    parser = ArgumentParser(description="convert and upload a transformer model to huggingface")
    parser.add_argument("model_id", type=str, help="transformer model to convert")
    parser.add_argument("--output-name", type=str, help="name of the output model")
    parser.add_argument("--files-to-copy", type=str, nargs="+", help="files to copy to the output model", default=[])
    parser.add_argument("--preserve-models", action="store_true", help="do not delete the downloaded models")
    parser.add_argument(
        "--quantisation",
        type=str,
        help="quantisation type",
        default="int8",
        choices=[
            "none",
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

    return parser.parse_known_args()[0]


def main() -> None:
    args = parse_args()

    with ModelConverter(
        args.model_id,
        args.output_name,
        files_to_copy=args.files_to_copy,
        preserve_models=args.preserve_models,
        quantisation=args.quantisation,
    ) as converter:
        converter.generate_gitattributes()
        converter.upload_to_huggingface()


if __name__ == "__main__":
    main()
