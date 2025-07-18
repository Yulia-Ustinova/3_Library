from lib_core import ABCItemLibrary, ABCAuthorGenre, ABCBook
import pandas as pd
from pathlib import Path


class _BaseInfra:
    """Межклассовые методы"""

    def __init__(self, file_name: str) -> None:
        self.file_name = file_name

    def create_new_id(self) -> int:
        """Метод создания нового id для автора, жанра или книги"""

        df = pd.read_csv(self.file_name)
        max_id = df["ID"].max()
        new_id = max_id + 1
        return new_id

    def find_id(self, column: str, name: str) -> int:
        """Метод нахождения существующего id в одной из таблиц"""

        df = pd.read_csv(self.file_name)
        series_item_id = df.loc[df[column] == name, "ID"]
        item_id = series_item_id.values[0]
        return item_id

    def get_df(self) -> pd.DataFrame:
        """Метод для получения датафрейма из файла"""

        df = pd.read_csv(self.file_name)
        return df


class AuthorInfra(ABCItemLibrary, ABCAuthorGenre, _BaseInfra):
    """Класс для работы с авторами"""

    def __init__(self, authors_file: str) -> None:
        super().__init__(authors_file)   # authors_file заполняет атрибут родителя file_name
        if not Path(self.file_name).exists():
            self.first_launch()

    def first_launch(self) -> None:
        """метод для первого входа: создает csv-файлы с авторами, жанрами и книгами с тестовыми данными"""
        author = [
            {"ID": 1, "Имя": "Майн Рид"}
        ]

        df_author = pd.DataFrame(author)
        df_author.to_csv(self.file_name, index=False, encoding="utf-8")

    def get_list(self) -> list:
        """Метод, получающий список авторов"""
        df_authors = pd.read_csv(self.file_name)
        author_list = df_authors["Имя"].tolist()
        return author_list

    def add_item(self, author: str) -> None:
        """Метод, добавляющий нового автора"""

        if_author_exists = self._check_exists(author)
        if if_author_exists == 0:
            new_author_id = self.create_new_id()
            new_author = pd.DataFrame({
                "ID": [new_author_id],
                "Имя": [author]
            })
            new_author.to_csv(self.file_name, mode="a", header=False, index=False)
        else:
            pass

    def _check_exists(self, new_author: str) -> int:
        """Метод, проверяющий, существует ли автор в базе ('0' - не существует, '1' - существует)"""
        authors = pd.read_csv(self.file_name)
        names = authors["Имя"]
        try:
            index_name = names[names == new_author].index[0]
        except IndexError:
            index_name = -1

        if index_name == -1:
            return 0
        else:
            return 1


class GenreInfra(ABCItemLibrary, ABCAuthorGenre, _BaseInfra):
    """Класс для работы с жанрами"""

    def __init__(self, genres_file: str) -> None:
        super().__init__(genres_file)    # genres_file заполняет атрибут родителя file_name
        if not Path(self.file_name).exists():
            self.first_launch()

    def first_launch(self) -> None:
        """метод для первого входа: создает csv-файлы с авторами, жанрами и книгами с тестовыми данными"""
        genre = [
            {"ID": 1, "Название": "Роман"}
        ]
        df_genre = pd.DataFrame(genre)
        df_genre.to_csv(self.file_name, index=False, encoding="utf-8")

    def get_list(self) -> list:
        """Метод, получающий список авторов"""
        df_genres = pd.read_csv(self.file_name)
        genre_list = df_genres["Название"].tolist()
        return genre_list

    def add_item(self, genre: str) -> None:
        """Метод, добавляющий новый жанр"""

        if_genre_exists = self._check_exists(genre)
        if if_genre_exists == 0:
            new_genre_id = self.create_new_id()
            new_genre = pd.DataFrame({
                "ID": [new_genre_id],
                "Название": [genre]
            })
            new_genre.to_csv(self.file_name, mode="a", header=False, index=False)
        else:
            pass

    def _check_exists(self, new_genre: str) -> int:
        """Метод, проверяющий, существует ли жанр в базе ('0' - не существует, '1' - существует)"""
        genres = pd.read_csv(self.file_name)
        names = genres["Название"]
        try:
            index_name = names[names == new_genre].index[0]
        except IndexError:
            index_name = -1

        if index_name == -1:
            return 0
        else:
            return 1


class BookInfra(ABCItemLibrary, ABCBook, _BaseInfra):
    """Класс для работы с книгой"""

    def __init__(self, books_file: str, authors: AuthorInfra, genres: GenreInfra) -> None:
        self.authors = authors
        self.genres = genres
        super().__init__(books_file)
        if not Path(self.file_name).exists():
            self.first_launch()

    def first_launch(self) -> None:
        """метод для первого входа: создает csv-файлы с авторами, жанрами и книгами с тестовыми данными"""

        book = [
            {"ID": 1, "Название": "Всадник без головы", "Автор": 1, "Жанр": 1, "Прочитано": True}
        ]
        df_book = pd.DataFrame(book)
        df_book.to_csv(self.file_name, index=False, encoding="utf-8")

    def get_list(self) -> dict:
        """Метод, получающий датафрейм книг с авторами и жанром"""
        books = self.get_df()
        authors = self.authors.get_df()
        genres = self.genres.get_df()

        books = pd.merge(books, authors, how="left", left_on="Автор", right_on="ID", suffixes=("_b", "_a"))
        books = books[["ID_b", "Название", "Имя", "Жанр", "Прочитано"]]
        books = books.rename(columns={"Имя": "Автор"})

        books = pd.merge(books, genres, how="left", left_on="Жанр", right_on="ID", suffixes=("_b", "_g"))
        books = books[["ID_b", "Название_b", "Автор", "Название_g", "Прочитано"]]
        books = books.rename(columns={"ID_b": "ID", "Название_b": "Книга", "Название_g": "Жанр"})
        books["Прочитано"] = books["Прочитано"].replace({True: "Да", False: "Нет"})

        books_dict = books.to_dict("list")

        return books_dict

    def add_item(self, book: str, author: str, genre: str, is_read: int) -> None:
        """Метод, добавляющий новую книгу в список"""

        self.authors.add_item(author)
        self.genres.add_item(genre)

        new_book_id = self.create_new_id()
        author_id = self.authors.find_id("Имя", author)
        genre_id = self.genres.find_id("Название", genre)

        if is_read == 1:
            is_read_value = True
        else:
            is_read_value = False

        new_book = pd.DataFrame({
            "ID": [new_book_id],
            "Название": [book],
            "Автор": [author_id],
            "Жанр": [genre_id],
            "Прочитано": [is_read_value]
        })
        new_book.to_csv(self.file_name, mode="a", header=False, index=False)

    def find_book(self, book: str, author: str, genre: str) -> dict:
        """Метод, который ищет книгу по заданным параметрам"""

        df_books_lower = pd.DataFrame(self.get_list())
        str_col = df_books_lower.select_dtypes(include="object").columns
        df_books_lower[str_col] = df_books_lower[str_col].apply(lambda col: col.str.lower())

        book_condition = df_books_lower["Книга"] == book.lower()
        author_condition = df_books_lower["Автор"] == author.lower()
        genre_condition = df_books_lower["Жанр"] == genre.lower()

        # проверка на заполнение входящих параметров (названия книги, автора и жанра)
        if (book) and (not author) and (not genre):
            conditions = book_condition
        elif (not book) and (author) and (not genre):
            conditions = author_condition
        elif (not book) and (not author) and (genre):
            conditions = genre_condition
        elif (book) and (author) and (not genre):
            conditions = (book_condition) & (author_condition)
        elif (not book) and (author) and (genre):
            conditions = (author_condition) & (genre_condition)
        elif (book) and (not author) and (genre):
            conditions = (book_condition) & (genre_condition)
        else:
            conditions = (book_condition) & (author_condition) & (genre_condition)

        series_lower_item_id: pd.Series = df_books_lower.loc[conditions, "ID"]
        list_id = series_lower_item_id.values

        df_books = pd.DataFrame(self.get_list())
        df_books = df_books[df_books["ID"].isin(list_id)]
        books_dict = df_books.to_dict("list")

        return books_dict

    def mark_read(self, book: str, mark_read: bool) -> None:
        """Метод, изменяющий статус 'Прочитано' у книги"""

        df_books = self.get_df()
        df_books.loc[df_books["Название"] == book, "Прочитано"] = mark_read
        df_books.to_csv(self.file_name, index=False, encoding="utf-8")

    def recommendations(self) -> dict:
        """Метод, создающий рекомендации новых книг для пользователя"""

        df_books = pd.DataFrame(self.get_list())
        df_books_read = df_books[df_books["Прочитано"] == "Да"]
        df_books_not_read = df_books[df_books["Прочитано"] == "Нет"]

        # Считаем, сколько раз встречается каждое значение в столбце "Жанр".
        # Получаем Series, где подсчитываемый элемент (жанр) - это индекс, а кол-во его повторений - значение
        genre_counts_series = df_books_read["Жанр"].value_counts()
        # находим максимальное значение
        max_v_genre = genre_counts_series.max()
        # получаем список индексов (жанров) с максимальным значением
        max_genres = genre_counts_series[genre_counts_series == max_v_genre].index.tolist()
        genre_recommendation = df_books_not_read[df_books_not_read["Жанр"].isin(max_genres)]

        # Считаем, сколько раз встречается каждое значение в столбце "Автор".
        # Получаем Series, где подсчитываемый элемент (автор) - это индекс, а кол-во его повторений - значение
        author_counts_series = df_books_read["Автор"].value_counts()
        # находим максимальное значение
        max_v_author = author_counts_series.max()
        # получаем список индексов (авторов) с максимальным значением
        max_authors = author_counts_series[author_counts_series == max_v_author].index.tolist()
        author_recommendation = df_books_not_read[df_books_not_read["Автор"].isin(max_authors)]

        recommendation = pd.concat([genre_recommendation, author_recommendation], axis=0)
        recom_dict = recommendation.to_dict("list")

        return recom_dict




