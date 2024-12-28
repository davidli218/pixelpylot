import argparse
from pathlib import Path

from app.rename_sony_clip.task_pipeline import generate_tasks_from_dir
from app.rename_sony_clip.task_pipeline import generate_tasks_from_file
from app.rename_sony_clip.task_pipeline import process_tasks


def main():
    parser = argparse.ArgumentParser(description='PixelPylot – Photography workflow automation CLI')

    subparsers = parser.add_subparsers(dest='command', help='sub-command help')

    sony_clip_rename_parser = subparsers.add_parser('rename-sony-clip', help='Batch rename Sony clips')
    sony_clip_rename_parser.add_argument('work_dest', nargs='?', default='.', help='Directory or file to process.')
    sony_clip_rename_parser.add_argument('-d', '--dry', action='store_true', help='Dry run.')
    sony_clip_rename_parser.add_argument('-s', '--strict', action='store_true', help='Strict mode.')

    args = parser.parse_args()

    if args.command == 'rename-sony-clip':
        work_dest = Path(args.work_dest)

        if work_dest.is_dir():
            tasks = generate_tasks_from_dir(work_dest, strict=args.strict)
        elif work_dest.is_file():
            tasks = generate_tasks_from_file(work_dest, strict=args.strict)
        else:
            raise FileNotFoundError(f"File Not Found: {work_dest}")

        process_tasks(tasks, dry_run=args.dry)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
