from tabulate import tabulate
from lib_infrastructure import BookInfra


class UI:
    """интерфейс"""

    def get_main_menu(self) -> int:
        """Метод, выводящий меню"""
        print("Что вы хотите сделать?")
        print("1. Показать меню книг")
        print("2. Показать меню авторов")
        print("3. Показать меню жанров")
        print("4. Показать рекомендации по следующим книгам")
        print("5. Выйти из программы")
        return int(input("Напишите номер пункта: "))

    def get_book_menu(self) -> int:
        """Метод, выводящий меню по книгам"""
        print("Что вы хотите сделать?")
        print("1. Просмотреть список всех книг")
        print("2. Добавить новую книгу")
        print("3. Найти книгу")
        print("4. Отметить книгу прочитанной")
        print("5. Отметить книгу непрочитанной")
        print("6. Выйти в главное меню")
        return int(input("Напишите номер пункта: "))

    def get_author_menu(self) -> int:
        """Метод, выводящий меню по авторам"""
        print("Что вы хотите сделать?")
        print("1. Просмотреть список авторов")
        print("2. Добавить нового автора")
        print("3. Выйти в общее меню")
        return int(input("Напишите номер пункта: "))

    def get_genre_menu(self) -> int:
        """Метод, выводящий меню по жанрам"""
        print("Что вы хотите сделать?")
        print("1. Просмотреть список жанров")
        print("2. Добавить новый жанр")
        print("3. Выйти в общее меню")
        return int(input("Напишите номер пункта: "))

    def wrong_menu_responce(self) -> None:
        """Метод, отвечающий пользователю, что введенная цифра меню некорректна"""
        print("\nВведите корректную цифру меню.\n")

    def show_book_list(self, book_dict: dict) -> None:
        """Метод, выводящий пользователю список книг с именами авторов и названиями жанров"""
        tbl_book = tabulate(book_dict, headers="keys", showindex=False, tablefmt="simple_outline")
        print(tbl_book)

    def show_author_list(self, author_list: list) -> None:
        """Метод, выводящий список авторов"""
        print("\n")
        for au in author_list:
            print(au)
        print("\n")

    def show_genre_list(self, genre_list: list) -> None:
        """Метод, выводящий список жанров"""
        print("\n")
        for g in genre_list:
            print(g)
        print("\n")

    def ask_for_new_book(self) -> tuple:
        """Метод, запрашивающий у пользователя информацию о новой книге, авторе и жанре"""
        book = input("Введите название книги: ")
        author = input("Введите имя автора: ")
        genre = input("Введите жанр: ")
        is_read = int(input("Введите '1', если книга прочитана или '0', если книга еще не прочитана: "))

        counter = 1
        while counter <= 5 and (is_read != 0 and is_read != 1):
            is_read = int(input("Некорректное значение! "
                                "Введите '1', если книга прочитана или '0', если книга еще не прочитана: "))
            counter += 1
        if counter == 6:
            print("\nВы исчерпали терпение программы. Начните заново.\n")
            raise ValueError()

        return book, author, genre, is_read

    def ask_new_author(self) -> str:
        """Метод, запрашивающий у пользователя имя нового автора"""
        author = input("Введите имя автора: ")
        return author

    def ask_new_genre(self) -> str:
        """Метод, запрашивающий у пользователя название нового жанра"""
        genre = input("Введите название жанра: ")
        return genre

    def success_adding(self) -> None:
        """Метод, выдающий уведомление, что книга, автор или жанр были успешно добавлены в список"""
        print("\nНовая запись была успешно добавлена.\n")

    def ask_for_looked_book(self) -> tuple:
        """Метод, запрашивающий у пользователя данные для поиска книги"""
        print("Заполните те поля, по которым хотите осуществить поиск."
              " Остальные поля оставьте пустыми (нажмите 'Enter')")

        book = input("Введите название книги: ")
        author = input("Введите имя автора: ")
        genre = input("Введите название жанра: ")

        if (not book) and (not author) and (not genre):
            print("\nНе заданы критерии поиска\n")
            raise ValueError()
        else:
            return book, author, genre

    def respond_to_looked_book(self, find_books: dict) -> None:
        """Метод, выдающий пользователю результат поиска книги"""

        if all(not book for book in find_books.values()):
            print("\nКниги не найдены\n")
        else:
            tbl_book = tabulate(find_books, headers="keys", showindex=False, tablefmt="simple_outline")
            print(tbl_book)

    def ask_for_read_book(self, mark: int) -> str:
        """Метод, запрашивающий название книги, которую нужно отметить прочитанной или нет"""

        if mark == 1:
            status = "прочитанной"
        else:
            status = "непрочитанной"

        book = input(f"Введите название книги, которую хотите отметить {status}: ")
        return book

    def respond_to_mark_read(self, mark: str) -> None:
        """Метод, сообщающий пользователю об успешном изменении статуса книги"""
        print(f"\nСтатус книги был успешно изменен на {mark}\n")

    def show_recommendation(self, recommendation: dict) -> None:
        """Метод, показывающий пользователю рекомендации по книгам"""
        tbl_book = tabulate(recommendation, headers="keys", showindex=False, tablefmt="simple_outline")
        print(tbl_book)


class Menu:
    """Связующий код между всеми модулями"""

    def __init__(self, book_infra: BookInfra, ui: UI) -> None:
        self.book_infra = book_infra
        self.ui = ui

    def run(self) -> None:
        while True:
            menu_item = self.ui.get_main_menu()

            # МЕНЮ КНИГ
            if menu_item == 1:
                menu_book = self.ui.get_book_menu()

                if menu_book == 1:     # показать все книги
                    book_dict = self.book_infra.get_list()
                    self.ui.show_book_list(book_dict)

                elif menu_book == 2:   # добавить новую книгу
                    try:
                        book, author, genre, is_read = self.ui.ask_for_new_book()
                        self.book_infra.add_item(book, author, genre, is_read)
                        self.ui.success_adding()
                    except ValueError as err:
                        print(err)
                        pass

                elif menu_book == 3:    # найти книгу по автору, жанру и  названию
                    try:
                        book, author, genre = self.ui.ask_for_looked_book()
                        find_book = self.book_infra.find_book(book, author, genre)
                        self.ui.respond_to_looked_book(find_book)
                    except ValueError as err:
                        print(err)
                        pass

                elif menu_book == 4:    # отметить книгу прочитанной
                    book = self.ui.ask_for_read_book(1)
                    self.book_infra.mark_read(book, True)
                    self.ui.respond_to_mark_read("'Прочитано'")

                elif menu_book == 5:    # отметить книгу непрочитанной
                    book = self.ui.ask_for_read_book(0)
                    self.book_infra.mark_read(book, False)
                    self.ui.respond_to_mark_read("'Непрочитано'")

                elif menu_book == 6:
                    pass

                else:
                    self.ui.wrong_menu_responce()

            # МЕНЮ АВТОРОВ
            elif menu_item == 2:
                menu_author = self.ui.get_author_menu()

                if menu_author == 1:
                    author_list = self.book_infra.authors.get_list()
                    self.ui.show_author_list(author_list)

                elif menu_author == 2:
                    author = self.ui.ask_new_author()
                    self.book_infra.authors.add_item(author)
                    self.ui.success_adding()

                elif menu_author == 3:
                    pass

                else:
                    self.ui.wrong_menu_responce()

            # МЕНЮ ЖАНРОВ
            elif menu_item == 3:
                menu_genre = self.ui.get_genre_menu()

                if menu_genre == 1:
                    genre_list = self.book_infra.genres.get_list()
                    self.ui.show_genre_list(genre_list)

                elif menu_genre == 2:
                    genre = self.ui.ask_new_genre()
                    self.book_infra.genres.add_item(genre)
                    self.ui.success_adding()

                elif menu_genre == 3:
                    pass

                else:
                    self.ui.wrong_menu_responce()

            elif menu_item == 4:
                recommendation = self.book_infra.recommendations()
                self.ui.show_recommendation(recommendation)

            elif menu_item == 5:
                break

            else:
                self.ui.wrong_menu_responce()




