from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass
class Author:
    id: int
    name: str


@dataclass
class Genre:
    id: int
    name: str


@dataclass
class Book:
    id: int
    name: str
    author_id: int
    genre_id: int
    is_read: bool


class ABCItemLibrary(ABC):
    """Бизнес-логика библиотеки"""

    @abstractmethod
    def first_launch(self) -> None:
        pass

    @abstractmethod
    def get_list(self) -> list | dict:
        pass

    @abstractmethod
    def add_item(self, *args) -> None:
        pass


class ABCAuthorGenre(ABC):
    """Класс управления авторами и жанрами"""

    @abstractmethod
    def _check_exists(self, name: str) -> int:
        pass


class ABCBook(ABC):
    """Класс управления книгами"""

    @abstractmethod
    def find_book(self, book: str, author: str, genre: str) -> dict:
        pass

    @abstractmethod
    def mark_read(self, book: str, mark_read: bool) -> None:
        pass

    @abstractmethod
    def recommendations(self) -> dict:
        pass








