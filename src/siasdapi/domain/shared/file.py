import os
import ffmpeg
from tempfile import NamedTemporaryFile


def parse_input_size(input_size):
    input_size = input_size.strip().lower()
    units = {
        "kb": 1024,
        "mb": 1024**2,
        "gb": 1024**3,
        "tb": 1024**4,
        "b": 1,
    }
    for unit, multiplier in units.items():
        if input_size.endswith(unit):
            return (
                int(input_size[: -len(unit)]) * multiplier
            )
    raise ValueError(
        "Tamanho inválido. Use o formato 'X', 'XKB', 'XMB', 'XGB' ou 'XTB'."
    )  # pragma: no cover


def check_content_size(
    content: bytes, max_size: str = "50M"
):
    try:
        max_size_bytes = parse_input_size(max_size)
        content_bytes = len(content)

        if content_bytes <= max_size_bytes:
            return True
        else:
            return False
    except ValueError as e:  # pragma: no cover
        print(e)
        return False


def bytes_to_named_temporary_file(content, filename) -> str:
    extension = filename.split(".")[-1]
    tmp_file = NamedTemporaryFile(
        delete=False,
        suffix=f".{extension}",
    )
    tmp_file.write(content)
    tmp_file.seek(0)
    return tmp_file.name


def convert_to_mp4(input_path: str) -> bytes:
    with NamedTemporaryFile(
        delete=False, suffix=".mp4"
    ) as output_temp:
        output_temp_path = output_temp.name

    ffmpeg.input(input_path).output(
        output_temp_path, vcodec="libx264", acodec="aac"
    ).global_args("-loglevel", "quiet").run(
        overwrite_output=True
    )

    with open(output_temp_path, "rb") as f:
        output_bytes = f.read()

    os.remove(output_temp_path)

    return output_bytes
