import abc
from typing import T


class BaseRepositoryInterface(abc.ABC):
    entity = None

    def find_by_id(self, id: int) -> T:
        model = self._find_by_id(id)
        return model

    def count_all(self, *args, **kwargs) -> int:
        count = self._count_all(*args, **kwargs)
        return count

    @abc.abstractmethod
    def _find_by_id(self, *args, **kwargs) -> T:
        raise NotImplementedError

    @abc.abstractmethod
    def _find_all(self, *args, **kwargs) -> T:
        raise NotImplementedError

    @abc.abstractmethod
    def _count_all(self) -> int:
        raise NotImplementedError


class BaseWriteableRepositoryInterface(
    BaseRepositoryInterface
):
    def create(self, model: T):
        self._create(model)

    def delete(self, model: T):
        self._delete(model)

    @abc.abstractmethod
    def _create(self, model: T):
        raise NotImplementedError

    @abc.abstractmethod
    def _delete(self, model: T):
        raise NotImplementedError
