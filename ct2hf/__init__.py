from importlib import import_module

from ct2hf.parse_args import parse_args


def main() -> None:
    args = parse_args()
    import_module("ct2hf.convert").convert(args)


if __name__ == "__main__":
    main()
