# pylint: disable=import-error
from typing import Protocol
from allocation.domain.model import Product
from abc import abstractmethod


class AbstractRepository(Protocol):
    @abstractmethod
    def add(self, product: Product) -> None:
        pass

    @abstractmethod
    def get(self, sku: str) -> Product:
        pass


class SQLAlchemyRepository:
    def __init__(self, session) -> None:
        self.session = session

    def add(self, product: Product) -> None:
        self.session.add(product)

    def get(self, sku: str) -> Product:
        return self.session.query(Product).filter_by(sku=sku).first()

