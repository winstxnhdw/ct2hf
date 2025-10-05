from argparse import ArgumentParser, Namespace


def parse_args() -> Namespace:
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

    return parser.parse_known_args()[0]
