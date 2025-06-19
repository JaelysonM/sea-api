from abc import ABC, abstractmethod


class StorageServiceInterface(ABC):
    @abstractmethod
    def upload(
        self,
        path: str,
        content: bytes = None,
        temp_file_path: str = None,
    ):
        raise NotImplementedError

    @abstractmethod
    def get(self, path: str, expires: int = None) -> str:
        raise NotImplementedError

    def delete(self, path: str):
        raise NotImplementedError
