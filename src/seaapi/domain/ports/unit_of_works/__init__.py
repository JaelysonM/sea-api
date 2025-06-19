import abc


class DefaultUnitOfWorkInterface(abc.ABC):
    def __exit__(self, exc_type, exc_value, traceback):
        self.expunge()
        if exc_value is not None:
            self.rollback()

    def commit(self):
        self._commit()

    @abc.abstractmethod
    def _commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError

    @abc.abstractmethod
    def expunge(self):
        raise NotImplementedError
