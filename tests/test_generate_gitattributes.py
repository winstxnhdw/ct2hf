# ruff: noqa: S101

from pathlib import Path

from conftest import RepositoryFiles

from ct2hf import generate_gitattributes


def gitattribute_line(path: str) -> str:
    return f"{path} filter=lfs diff=lfs merge=lfs -text\n"


def get_lines_from_generated_gitattributes(repository_directory: Path, *, min_lfs_size: int) -> list[str]:
    generate_gitattributes(repository_directory, min_lfs_size=min_lfs_size)

    with (repository_directory / ".gitattributes").open("r") as file:
        return file.readlines()


def test_all_files_in_gitattributes(mock_repository: RepositoryFiles) -> None:
    lines = get_lines_from_generated_gitattributes(mock_repository.repository_directory, min_lfs_size=10)

    assert lines[0] == gitattribute_line("large_file.txt")
    assert lines[1] == gitattribute_line("small_file.txt")
    assert lines[2] == gitattribute_line("subdir/large_file_in_subdir.txt")
    assert lines[3] == gitattribute_line("subdir/small_file_in_subdir.txt")


def test_large_files_in_gitattributes(mock_repository: RepositoryFiles) -> None:
    lines = get_lines_from_generated_gitattributes(mock_repository.repository_directory, min_lfs_size=100)

    assert lines[0] == gitattribute_line("large_file.txt")
    assert lines[1] == gitattribute_line("subdir/large_file_in_subdir.txt")


def test_no_files_in_gitattributes(mock_repository: RepositoryFiles) -> None:
    assert not get_lines_from_generated_gitattributes(mock_repository.repository_directory, min_lfs_size=100000)
