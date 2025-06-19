from src.siasdapi.domain.ports.services.storage import (
    StorageServiceInterface,
)


class FakeStorageService(StorageServiceInterface):
    def upload(
        self,
        path: str,
        content: bytes,
        temp_file_path: str = None,
    ):
        print("Uploading file " + path)

    def get(self, path: str, expires: int = None):
        return path

    def delete(self, path: str):
        print("Deleting file " + path)
