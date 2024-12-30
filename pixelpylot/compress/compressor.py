from PIL import Image
from photoshop import Session


def worker_pil(image_path, output_path, long_edge=1706, ppi=72, quality=10):
    with Image.open(image_path) as img:
        width, height = img.size

        if width > height:
            new_width = long_edge
            new_height = round((long_edge / width) * height)
        else:
            new_height = long_edge
            new_width = round((long_edge / height) * width)

        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        img.info['dpi'] = (ppi, ppi)

        img.save(output_path, quality=quality, dpi=(ppi, ppi), optimize=True)


def worker_ps(image_path, output_path, long_edge=1706, ppi=72, quality=10):
    with Session() as ps:
        doc = ps.app.open(image_path)
        width, height = doc.width, doc.height

        if width > height:
            new_width = long_edge
            new_height = round((long_edge / width) * height)
        else:
            new_height = long_edge
            new_width = round((long_edge / height) * width)

        doc.resizeImage(new_width, new_height, ppi, ps.ResampleMethod.Automatic)

        options = ps.JPEGSaveOptions()
        options.quality = quality
        options.embedColorProfile = True

        doc.saveAs(output_path, options)
        doc.close()
