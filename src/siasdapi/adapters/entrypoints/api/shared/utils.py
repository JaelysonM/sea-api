from fastapi import UploadFile
from src.siasdapi.domain.shared.file import (
    bytes_to_named_temporary_file,
)
from src.siasdapi.domain.ports.shared.exceptions import (
    FileBadFormatException,
)
from src.siasdapi.domain.dtos.mics import UploadedFile


def convert_upload_file_to_domain(
    upload_file: UploadFile,
) -> UploadedFile:
    try:
        content = upload_file.file.read()
        filename = upload_file.filename
        relative_path = bytes_to_named_temporary_file(
            content, filename
        )

        return UploadedFile(
            content=content,
            filename=filename,
            relative_path=relative_path,
        )
    except Exception as e:  # pragma: no cover
        print(e)
        raise FileBadFormatException()
