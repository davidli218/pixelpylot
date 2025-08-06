from enum import Enum
from pathlib import Path

import typer
from rich.console import Console
from rich.progress import track
from rich.table import Table
from rich.theme import Theme
from typing_extensions import Annotated

from pixelpylot import __version__
from pixelpylot.core.utils import find_photos
from pixelpylot.core.utils import prepare_output_paths
from pixelpylot.service.compressor import ImageCompressor
from pixelpylot.service.compressor import ImageCompressorPreset
from pixelpylot.service.compressor import PhotoshopImageCompressor
from pixelpylot.service.compressor import PillowImageCompressor

app = typer.Typer(help="PixelPylot - 化繁为简，一览全局。", )
console = Console(theme=Theme({
    "path": "cyan",
    "task": "bright_white",
    "success": "bold aquamarine1",
    "warning": "bold light_goldenrod1",
    "danger": "bold light_salmon1",
    "error": "light_salmon1",
    "table_header": "bold cyan",
    "filename": "sky_blue2",
}))


class SocialPlatform(str, Enum):
    XHS = "xhs"

    @property
    def display_name(self) -> str:
        return {
            "xhs": "小红书",
        }.get(self.value, self.value)

    @property
    def compressor_preset(self) -> ImageCompressorPreset:
        return {
            "xhs": ImageCompressorPreset.XHS,
        }[self.value]

    @property
    def filename_suffix(self) -> str:
        return {
            "xhs": "_XHS",
        }[self.value]


class CompressorChoice(str, Enum):
    PHOTOSHOP = "ps"
    PIL = "pil"

    @property
    def display_name(self) -> str:
        return {
            "ps": "Photoshop",
            "pil": "Pillow",
        }.get(self.value, self.value)

    @property
    def instance(self) -> ImageCompressor:
        return {
            "ps": PhotoshopImageCompressor(),
            "pil": PillowImageCompressor(),
        }[self.value]


@app.command(name="version", help="显示 PixelPylot 的版本信息。")
def version_command():
    console.print(f"PixelPylot Version:{__version__}\n")


@app.command(name="compress", help="压缩图片到适合社交媒体的大小。")
def compress_command(
        path: Annotated[Path, typer.Argument(
            help="要处理的图片文件或文件夹路径。",
            exists=True,
            file_okay=True,
            dir_okay=True,
            readable=True,
            resolve_path=True
        )] = Path.cwd(),

        platform: Annotated[SocialPlatform, typer.Option(
            "--platform", "-p",
            help="选择目标社交媒体平台。",
            case_sensitive=False
        )] = SocialPlatform.XHS,

        compressor: Annotated[CompressorChoice, typer.Option(
            "--backend", "-b",
            help="选择要使用的图像压缩器后端。",
            case_sensitive=False
        )] = CompressorChoice.PHOTOSHOP
):
    # --- 阶段 1: 启动信息 ---
    console.print(f"💾 路径: {path}", style="path")
    console.print(f"⚙️ 任务: 使用 {compressor.display_name} 压缩至 {platform.display_name} 标准", style="task")
    console.print()

    # --- 阶段 2: 文件发现 & 任务准备 ---
    files_to_process = find_photos(path) if path.is_dir() else [path]
    if not files_to_process:
        console.print("❌ 错误: 未找到任何可处理的图片文件。", style="danger")
        raise typer.Exit()
    tasks = prepare_output_paths(files_to_process, path / "compressed", platform.filename_suffix)

    # --- 阶段 3: 文件处理 ---
    worker = compressor.instance
    compress_cfg = platform.compressor_preset

    worker_err: list[tuple[Path, str]] = []

    for input_path, output_path in track(tasks, description="🚀 压缩中...[/]"):
        try:
            worker.process(input_path, output_path, compress_cfg.size, compress_cfg.ppi)
        except Exception as e:
            worker_err.append((input_path, str(e)))
    console.print()

    # --- 阶段 4: 结果输出 ---
    total_count = len(tasks)
    error_count = len(worker_err)
    success_count = total_count - error_count

    if worker_err:
        console.print(f"⚠️ 处理完成! 成功: {success_count}, 失败: {error_count}", style="warning")
        table = Table()
        table.add_column("文件路径", style="filename", overflow="fold", header_style="table_header")
        table.add_column("错误原因", style="error", overflow="fold", header_style="table_header")
        for file_path, error in worker_err:
            table.add_row(str(file_path.name), error)
        console.print(table)
    else:
        console.print(f"✅ 所有文件处理成功! 总计: {total_count} 文件。", style="success")
