from importlib import import_module

from ct2hf.parse_args import parse_args


def main() -> None:
    args = parse_args()

    import_module("ct2hf.convert").convert(
        args.model_id,
        output_name=args.output_name,
        revision=args.revision,
        files_to_copy=args.files_to_copy,
        preserve_models=args.preserve_models,
        compatibility=args.compatibility,
        quantisation=args.quantisation,
    )


if __name__ == "__main__":
    main()
