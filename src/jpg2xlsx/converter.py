from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

import xlsxwriter
from PIL import Image


def _prepare_image(
    image: Image.Image,
    *,
    max_dimension: int | None,
    colors: int | None,
) -> Image.Image:
    prepared = image.convert("RGB")

    if max_dimension is not None:
        if max_dimension < 1:
            raise ValueError("max_dimension must be greater than 0")

        width, height = prepared.size
        largest_side = max(width, height)
        if largest_side > max_dimension:
            scale = max_dimension / largest_side
            resized_size = (
                max(1, round(width * scale)),
                max(1, round(height * scale)),
            )
            prepared = prepared.resize(resized_size, Image.Resampling.LANCZOS)

    if colors is not None:
        if not 1 <= colors <= 256:
            raise ValueError("colors must be between 1 and 256")
        prepared = prepared.quantize(colors=colors).convert("RGB")

    return prepared


def convert(
    input_path: Path | str,
    output_path: Path | str,
    *,
    cell_width: float = 0.15,
    cell_height: float = 1.4,
    max_dimension: int | None = None,
    colors: int | None = None,
    on_row: Callable[[int], None] | None = None,
) -> None:
    """Convert an image file to an XLSX where each cell represents a pixel.

    Args:
        input_path: Path to the source image (JPEG, PNG, GIF, BMP, …).
        output_path: Destination XLSX path. ``.xlsx`` is appended when no
            suffix is provided.
        cell_width: Excel column width applied to every pixel column.
        cell_height: Excel row height (pt) applied to every pixel row.
        max_dimension: Optional max size for the largest image dimension.
            When provided, the image is downscaled before writing the sheet.
        colors: Optional number of colors to quantize the image to.
        on_row: Optional callback called after each row is written, receiving
            the zero-based row index. Useful for progress tracking.
    """
    input_path = Path(input_path)
    output_path = Path(output_path)

    if not input_path.exists():
        raise FileNotFoundError(f"Input image does not exist: {input_path}")

    if not output_path.suffix:
        output_path = output_path.with_suffix(".xlsx")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with Image.open(input_path) as image:
        rgb_image = _prepare_image(
            image,
            max_dimension=max_dimension,
            colors=colors,
        )

    width, height = rgb_image.size
    pix = rgb_image.load()

    workbook = xlsxwriter.Workbook(str(output_path), {"constant_memory": True})
    worksheet = workbook.add_worksheet()

    worksheet.set_column(0, width - 1, cell_width)
    worksheet.set_default_row(cell_height)

    fmt_cache: dict[tuple[int, int, int], xlsxwriter.format.Format] = {}

    for y in range(height):
        for x in range(width):
            rgb: tuple[int, int, int] = pix[x, y]
            if rgb not in fmt_cache:
                r, g, b = rgb
                fmt_cache[rgb] = workbook.add_format(
                    {"bg_color": f"#{r:02x}{g:02x}{b:02x}", "pattern": 1}
                )
            worksheet.write_blank(y, x, None, fmt_cache[rgb])

        if on_row is not None:
            on_row(y)

    workbook.close()
