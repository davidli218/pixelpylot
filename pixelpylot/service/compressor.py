import abc
from enum import Enum
from pathlib import Path
from typing import final

from PIL import Image
from photoshop import Session

__all__ = [
    "ImageCompressor",
    "ImageCompressorPreset",
    "PillowImageCompressor",
    "PhotoshopImageCompressor"
]


class ImageCompressorPreset(Enum):
    XHS = ((1280, 1706), 72)

    @property
    def size(self) -> tuple[int, int]:
        return self.value[0]

    @property
    def ppi(self) -> int:
        return self.value[1]


class ImageCompressor(abc.ABC):

    @staticmethod
    def _calc_rect_fit_size(w: int, h: int, container_size: tuple[int, int]) -> tuple[int, int]:
        a, b = container_size

        # S1. 计算两种朝向对应的缩放因子
        s1 = min(a / w, b / h)
        s2 = min(b / w, a / h)

        # S2. 取1.0以内较大的缩放因子，矩形应最大化得利用容器
        scale = min(max(s1, s2), 1.0)
        a_is_w = s1 >= s2

        # S3. 计算新的宽高，并确保不超过最大边界
        new_width = min(round(w * scale), a if a_is_w else b)
        new_height = min(round(h * scale), b if a_is_w else a)

        return new_width, new_height

    @staticmethod
    def _std_aspect_ratio_compensator(size: tuple[int, int]) -> tuple[int, int]:
        compensate_table = {
            (1705, 1280): (1706, 1280),
            (1280, 1705): (1280, 1706),
        }

        return compensate_table.get(size, size)

    @abc.abstractmethod
    def process(self, path_in: Path | str, path_out: Path | str, max_size: tuple[int, int], ppi: int) -> None:
        raise NotImplementedError


@final
class PillowImageCompressor(ImageCompressor):

    def process(self, path_in, path_out, max_size, ppi):
        with Image.open(path_in) as img:
            w, h = img.size

            new_size = self._calc_rect_fit_size(w, h, max_size)
            new_size = self._std_aspect_ratio_compensator(new_size)

            img = img.resize(new_size, Image.Resampling.LANCZOS)

            img.save(path_out, quality=95, dpi=(ppi, ppi), optimize=True)


@final
class PhotoshopImageCompressor(ImageCompressor):

    def process(self, path_in, path_out, max_size, ppi):
        with Session() as ps:
            doc = ps.app.open(str(path_in))

            w, h = doc.width, doc.height
            new_size = self._calc_rect_fit_size(w, h, max_size)
            new_width, new_height = self._std_aspect_ratio_compensator(new_size)

            doc.resizeImage(new_width, new_height, ppi, ps.ResampleMethod.Automatic)

            doc.saveAs(str(path_out), ps.JPEGSaveOptions(quality=10, embedColorProfile=True))
            doc.close()
