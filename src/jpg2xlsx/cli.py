from __future__ import annotations

import argparse
from pathlib import Path

from . import __version__
from .converter import convert


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="jpg2xlsx",
        description=(
            "Convert an image into an Excel workbook where each cell matches a pixel."
        ),
    )
    parser.add_argument("input", type=Path, help="Path to the source image.")
    parser.add_argument(
        "output",
        nargs="?",
        type=Path,
        help="Output XLSX path. Defaults to the input path with an .xlsx suffix.",
    )
    parser.add_argument(
        "--cell-width",
        type=float,
        default=0.15,
        help="Excel column width to use for each pixel column.",
    )
    parser.add_argument(
        "--cell-height",
        type=float,
        default=1.4,
        help="Excel row height in points to use for each pixel row.",
    )
    parser.add_argument(
        "--max-dimension",
        type=int,
        help=(
            "Downscale the image so its largest side matches this value before "
            "creating the workbook."
        ),
    )
    parser.add_argument(
        "--colors",
        type=int,
        help=(
            "Quantize the image to this many colors before writing the workbook "
            "to reduce size."
        ),
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Allow overwriting an existing output file.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    input_path = args.input
    if args.output is None:
        output_path = input_path.with_suffix(".xlsx")
    else:
        output_path = args.output

    if not input_path.exists():
        parser.error(f"input file does not exist: {input_path}")

    if output_path.exists() and not args.overwrite:
        parser.error(
            f"output file already exists; pass --overwrite to replace it: {output_path}"
        )

    convert(
        input_path=input_path,
        output_path=output_path,
        cell_width=args.cell_width,
        cell_height=args.cell_height,
        max_dimension=args.max_dimension,
        colors=args.colors,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
