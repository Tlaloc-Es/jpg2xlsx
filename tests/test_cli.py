from pathlib import Path
from unittest.mock import patch

import pytest
from PIL import Image

from jpg2xlsx.cli import main


def make_image(path: Path) -> None:
    image = Image.new("RGB", (1, 1), (10, 20, 30))
    image.save(path)


def test_cli_uses_default_output_name(tmp_path: Path) -> None:
    input_path = tmp_path / "pixel.png"
    make_image(input_path)

    exit_code = main([str(input_path)])

    assert exit_code == 0
    assert (tmp_path / "pixel.xlsx").exists()


def test_cli_refuses_to_overwrite_without_flag(tmp_path: Path) -> None:
    input_path = tmp_path / "pixel.png"
    output_path = tmp_path / "pixel.xlsx"
    make_image(input_path)
    output_path.write_text("existing")

    with pytest.raises(SystemExit):
        main([str(input_path), str(output_path)])


def test_cli_passes_compact_options(tmp_path: Path) -> None:
    input_path = tmp_path / "pixel.png"
    output_path = tmp_path / "pixel.xlsx"
    make_image(input_path)

    with patch("jpg2xlsx.cli.convert") as mocked_convert:
        exit_code = main(
            [
                str(input_path),
                str(output_path),
                "--max-dimension",
                "256",
                "--colors",
                "64",
                "--overwrite",
            ]
        )

    assert exit_code == 0
    mocked_convert.assert_called_once_with(
        input_path=input_path,
        output_path=output_path,
        cell_width=0.15,
        cell_height=1.4,
        max_dimension=256,
        colors=64,
    )
