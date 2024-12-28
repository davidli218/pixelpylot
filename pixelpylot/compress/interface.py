from pathlib import Path

from .compressor import worker_ps


def handle_args(input_dir):
    input_dir = Path(input_dir)
    output_dir = input_dir / 'output'

    output_dir.mkdir(parents=True, exist_ok=True)

    image_paths = list(input_dir.glob('*.jpg')) + list(input_dir.glob('*.JPG'))

    print(f"Found {len(image_paths)} images to process.")
    for image_path in image_paths:
        print(f"Processing: {image_path}")

        output_path = output_dir / f"{image_path.stem}_x1706p{image_path.suffix}"
        worker_ps(image_path, output_path)

        print(f"Saved to: {output_path}")
