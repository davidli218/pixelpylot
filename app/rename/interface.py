from pathlib import Path

from .sony_v_pipeline import generate_tasks_from_dir
from .sony_v_pipeline import generate_tasks_from_file
from .sony_v_pipeline import process_tasks


def handle_args(mode, work_dest, dry_run, strict):
    work_dest = Path(work_dest)

    if mode == 'sony-v':
        if work_dest.is_dir():
            tasks = generate_tasks_from_dir(work_dest, strict=strict)
        elif work_dest.is_file():
            tasks = generate_tasks_from_file(work_dest, strict=strict)
        else:
            raise FileNotFoundError(f"File Not Found: {work_dest}")

        process_tasks(tasks, dry_run=dry_run)
    else:
        raise ValueError(f"Invalid mode: {mode}")
