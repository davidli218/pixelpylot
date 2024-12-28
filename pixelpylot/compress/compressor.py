from pathlib import Path

from photoshop import Session


def worker_ps(image_path, output_path, long_edge=1706, ppi=72, quality=10):
    with Session() as ps:
        doc = ps.app.open(image_path)
        width = doc.width
        height = doc.height

        # 判断长边并计算比例
        if width > height:
            new_width = long_edge
            new_height = round((long_edge / width) * height)
        else:
            new_height = long_edge
            new_width = round((long_edge / height) * width)

        # 修改 PPI (分辨率)
        doc.resizeImage(new_width, new_height, ppi, ps.ResampleMethod.Automatic)

        # 设置保存选项 (JPEG)
        options = ps.JPEGSaveOptions()
        options.quality = quality  # 最高质量
        options.embedColorProfile = True  # 嵌入颜色配置文件

        # 保存并关闭
        doc.saveAs(output_path, options)
        doc.close()


