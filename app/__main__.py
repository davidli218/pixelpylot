import argparse

from app import compress
from app import rename


def main():
    parser = argparse.ArgumentParser(description='PixelPylot – Photography workflow automation CLI')

    subparsers = parser.add_subparsers(dest='command', help='sub-command help')

    sony_clip_rename_parser = subparsers.add_parser('rename', help='Batch rename Sony clips')
    sony_clip_rename_parser.add_argument('mode', choices=['sony-v'], help='Mode to run.')
    sony_clip_rename_parser.add_argument('work_dest', nargs='?', default='.', help='Directory or file to process.')
    sony_clip_rename_parser.add_argument('-d', '--dry', action='store_true', help='Dry run.')
    sony_clip_rename_parser.add_argument('-s', '--strict', action='store_true', help='Strict mode.')

    compress_parser = subparsers.add_parser('compress', help='Compress images')
    compress_parser.add_argument('work_dest', nargs='?', default='.', help='Directory to process.')

    args = parser.parse_args()

    if args.command == 'rename':
        rename.handle_args(args.mode, args.work_dest, dry_run=args.dry, strict=args.strict)
    elif args.command == 'compress':
        compress.handle_args(args.work_dest)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
