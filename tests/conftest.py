from pathlib import Path
from typing import NamedTuple

from pytest import fixture


class RepositoryFiles(NamedTuple):
    repository_directory: Path
    small_file: Path
    large_file: Path
    small_file_in_subdir: Path
    large_file_in_subdir: Path


@fixture
def mock_repository(tmp_path: Path) -> RepositoryFiles:
    repository_directory = tmp_path / "repo"
    repository_directory.mkdir()

    small_file = repository_directory / "small_file.txt"
    large_file = repository_directory / "large_file.txt"

    subdirectory = repository_directory / "subdir"
    subdirectory.mkdir()

    small_file_in_subdir = subdirectory / "small_file_in_subdir.txt"
    large_file_in_subdir = subdirectory / "large_file_in_subdir.txt"

    small_file.write_text("small file content")
    large_file.write_text("large file content" * 100)
    small_file_in_subdir.write_text("small file content in subdir")
    large_file_in_subdir.write_text("large file content in subdir" * 100)

    return RepositoryFiles(
        repository_directory=repository_directory,
        small_file=small_file,
        large_file=large_file,
        small_file_in_subdir=small_file_in_subdir,
        large_file_in_subdir=large_file_in_subdir,
    )
