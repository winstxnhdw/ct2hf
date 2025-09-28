# ruff: noqa: S101

from pathlib import Path

from conftest import RepositoryFiles

from ct2hf.convert import generate_gitattributes


def gitattribute_line(path: Path) -> str:
    return f"{path.as_posix()} filter=lfs diff=lfs merge=lfs -text\n"


def get_lines_from_generated_gitattributes(repository_directory: Path, *, min_lfs_size: int) -> list[str]:
    generate_gitattributes(repository_directory, min_lfs_size=min_lfs_size)

    with (repository_directory / ".gitattributes").open("r") as file:
        return file.readlines()


def test_all_files_in_gitattributes(mock_repository: RepositoryFiles) -> None:
    lines = get_lines_from_generated_gitattributes(mock_repository.repository_directory, min_lfs_size=10)
    expected_lines = {
        gitattribute_line(mock_repository.small_file),
        gitattribute_line(mock_repository.large_file),
        gitattribute_line(mock_repository.small_file_in_subdir),
        gitattribute_line(mock_repository.large_file_in_subdir),
    }

    assert len(lines) == len(expected_lines)
    assert set(lines) == expected_lines


def test_large_files_in_gitattributes(mock_repository: RepositoryFiles) -> None:
    lines = get_lines_from_generated_gitattributes(mock_repository.repository_directory, min_lfs_size=100)
    expected_lines = {
        gitattribute_line(mock_repository.large_file),
        gitattribute_line(mock_repository.large_file_in_subdir),
    }

    assert len(lines) == len(expected_lines)
    assert set(lines) == expected_lines


def test_no_files_in_gitattributes(mock_repository: RepositoryFiles) -> None:
    assert not get_lines_from_generated_gitattributes(mock_repository.repository_directory, min_lfs_size=100000)
