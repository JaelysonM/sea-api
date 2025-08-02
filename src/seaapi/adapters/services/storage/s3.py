import boto3
import os
from src.fansapi.domain.ports.services.storage import (
    StorageServiceInterface,
)
from src.fansapi.config.settings import settings
from src.fansapi.domain.shared.file import (
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
            region_name=settings.STORAGE_REGION,
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
        if expires is None:
            return f"https://{settings.STORAGE_BUCKET}.s3.amazonaws.com/{path}"
        response = self.client.generate_presigned_url(
            "get_object",
            Params={
                "Bucket": settings.STORAGE_BUCKET,
                "Key": path,
            },
            ExpiresIn=expires,
        )
        return response

    def delete(self, path: str):  # pragma: no cover
        self.client.delete_object(
            Bucket=settings.STORAGE_BUCKET,
            Key=path,
        )
