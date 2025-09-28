from typing import Literal, NamedTuple

class Arguments(NamedTuple):
    model_id: str
    output_name: str | None
    revision: str | None
    files_to_copy: list[str]
    preserve_models: bool
    compatibility: bool
    quantisation: (
        None
        | Literal[
            "int8",
            "int8_float32",
            "int8_float16",
            "int8_bfloat16",
            "int16",
            "float16",
            "bfloat16",
            "float32",
        ]
    )

def parse_args() -> Arguments: ...
