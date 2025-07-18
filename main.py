from lib_UI import UI, Menu
from lib_infrastructure import AuthorInfra, GenreInfra, BookInfra


authors_file = "authors.csv"
genres_file = "genres.csv"
books_file = "books.csv"


if __name__ == "__main__":

    author = AuthorInfra(authors_file)
    genre = GenreInfra(genres_file)
    book = BookInfra(books_file, author, genre)
    ui = UI()
    menu = Menu(book, ui)

    menu.run()

