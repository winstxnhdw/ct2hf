from ct2hf.compute_type import ComputeType as ComputeTypeAlias

class ComputeType(str):
    __args__: tuple[ComputeTypeAlias, ...]
