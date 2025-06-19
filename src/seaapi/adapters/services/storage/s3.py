import boto3
import os
from src.seaapi.domain.ports.services.storage import (
    StorageServiceInterface,
)
from src.seaapi.config.settings import settings
from src.seaapi.domain.shared.file import (
    bytes_to_named_temporary_file,
)


class S3StorageService(
    StorageServiceInterface
):  # pragma: no cover
    def __init__(self):
        self.client = boto3.client(
            "s3",
            aws_access_key_id=settings.STORAGE_ACCESS_KEY,
            aws_secret_access_key=settings.STORAGE_SECRET_KEY,
        )

    def upload(
        self,
        path: str,
        content: bytes = None,
        temp_file_path: str = None,
    ):  # pragma: no cover
        if temp_file_path is None:
            temp_file_path = bytes_to_named_temporary_file(
                content, path
            )
        if temp_file_path is None and content is None:
            raise Exception(
                "Cannot upload empty file or content"
            )

        self.client.upload_file(
            temp_file_path,
            settings.STORAGE_BUCKET,
            path,
        )
        os.remove(temp_file_path)

    def get(
        self, path: str, expires: int = None
    ):  # pragma: no cover
        return f"https://{settings.STORAGE_BUCKET}.s3.amazonaws.com/{path}"

    def delete(self, path: str):  # pragma: no cover
        self.client.delete_object(
            Bucket=settings.STORAGE_BUCKET,
            Key=path,
        )
