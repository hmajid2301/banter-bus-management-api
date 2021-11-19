import abc
from typing import Generic, TypeVar

from motor import motor_asyncio

T = TypeVar("T")


class AbstractRepository(abc.ABC, Generic[T]):
    def __init__(
        self,
        username: str,
        password: str,
        host: str,
        port: int,
        db_name: str,
        auth_db_name: str,
        collection_name: str,
    ) -> None:
        uri = f"mongodb://${username}:${password}@${host}:${port}/${db_name}"
        if auth_db_name:
            uri += f"?authSource=${auth_db_name}"

        self.client = motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    @abc.abstractmethod
    def add(self, doc: T) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, id_: str) -> T:
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, id_: str, doc: T) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def remove(self, id_: str) -> bool:
        raise NotImplementedError
