from pathlib import Path
from typing import Sequence


def find_files_by_extensions(
        folder: str | Path,
        extensions: Sequence[str],
        recursive: bool
) -> list[Path]:
    """Find files with given extensions in a directory."""
    source_folder = Path(folder)
    extensions = {ext.lower() for ext in extensions}

    glob_iterator = source_folder.rglob("*") if recursive else source_folder.glob("*")

    return [
        p for p in glob_iterator
        if p.is_file() and p.suffix.lower() in extensions
    ]


def find_photos(folder: str | Path, recursive: bool = False) -> list[Path]:
    """Find images with given extensions in a directory."""
    return find_files_by_extensions(folder=folder, extensions=(".jpg", ".jpeg", ".png"), recursive=recursive)


def find_clips(folder: str | Path, recursive: bool = False) -> list[Path]:
    """Find video files in a directory."""
    return find_files_by_extensions(folder=folder, extensions=(".mp4", ".mov", ".avi"), recursive=recursive)


def prepare_output_paths(
        input_paths: list[Path],
        output_folder: str | Path,
        filename_suffix: str = "",
) -> list[tuple[Path, Path]]:
    """Generate pairs of input paths and their corresponding output paths."""
    output_folder = Path(output_folder)
    output_folder.mkdir(parents=True, exist_ok=True)

    ret = []
    for input_path in input_paths:
        output_filename = f"{input_path.stem}{filename_suffix}{input_path.suffix}"
        output_path = output_folder / output_filename
        ret.append((input_path, output_path))

    return ret
