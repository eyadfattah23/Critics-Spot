import random
from datetime import datetime, timedelta
from decimal import Decimal
from books.models import Author, Genre, Book

# Helper functions


def random_date(start, end):
    """Generate a random date between start and end."""
    return start + timedelta(days=random.randint(0, (end - start).days))


def create_authors():
    """Create sample authors."""
    authors = [
        {"name": "Jane Austen", "birth_date": datetime(1775, 12, 16).date(
        ), "bio": "English novelist known for her romantic fiction."},
        {"name": "Mark Twain", "birth_date": datetime(1835, 11, 30).date(
        ), "bio": "American writer and humorist, famous for 'Adventures of Huckleberry Finn'."},
        {"name": "Virginia Woolf", "birth_date": datetime(1882, 1, 25).date(
        ), "bio": "English writer and pioneer of modernist literature."},
        {"name": "J.K. Rowling", "birth_date": datetime(1965, 7, 31).date(
        ), "bio": "British author of the 'Harry Potter' series."},
        {"name": "George Orwell", "birth_date": datetime(
            1903, 6, 25).date(), "bio": "English novelist, essayist, and critic."},
        {"name": "F. Scott Fitzgerald", "birth_date": datetime(1896, 9, 24).date(
        ), "bio": "American novelist, known for 'The Great Gatsby'."},
    ]
    author_objs = []
    for author in authors:
        author_obj, _ = Author.objects.get_or_create(
            name=author["name"],
            birth_date=author["birth_date"],
            bio=author["bio"],
        )
        author_objs.append(author_obj)
    return author_objs


def create_genres():
    """Create sample genres."""
    genres = [
        "Fiction", "Non-Fiction", "Fantasy", "Science Fiction",
        "Mystery", "Thriller", "Romance", "Historical Fiction",
        "Biography", "Self-Help", "Philosophy", "Poetry",
    ]
    genre_objs = []
    for genre in genres:
        genre_obj, _ = Genre.objects.get_or_create(
            name=genre,
            description=f"A genre that focuses on {genre.lower()} stories."
        )
        genre_objs.append(genre_obj)
    return genre_objs


def create_books(authors, genres):
    """Create sample books."""
    books = [
        {"title": "Pride and Prejudice", "description": "A story of love and misunderstandings.",
         "pages": 432, "author": authors[0]},
        {"title": "Adventures of Huckleberry Finn",
         "description": "A tale of adventure and morality.", "pages": 366, "author": authors[1]},
        {"title": "1984", "description": "A dystopian novel on surveillance and totalitarianism.",
         "pages": 328, "author": authors[4]},
        {"title": "Harry Potter and the Philosopher's Stone",
         "description": "A young wizard discovers his magical heritage.", "pages": 309, "author": authors[3]},
        {"title": "Mrs. Dalloway", "description": "A single day in the life of Clarissa Dalloway.",
         "pages": 194, "author": authors[2]},
        {"title": "The Great Gatsby", "description": "The story of Jay Gatsby's quest for Daisy Buchanan.",
         "pages": 180, "author": authors[5]},
    ]

    for _ in range(15):  # Add more randomized books
        book = {
            "title": f"Random Book {random.randint(1, 1000)}",
            "description": "A captivating tale filled with intrigue and drama.",
            "pages": random.randint(150, 600),
            "author": random.choice(authors),
            "publication_date": random_date(datetime(1900, 1, 1), datetime(2020, 12, 31)).date(),
        }
        books.append(book)

    for book in books:
        book_obj, _ = Book.objects.get_or_create(
            title=book["title"],
            description=book["description"],
            pages=book["pages"],
            author=book["author"],
            publication_date=random_date(
                datetime(1900, 1, 1), datetime(2023, 12, 31)).date(),
        )
        genres_subset = random.sample(genres, random.randint(1, 3))
        book_obj.genres.set(genres_subset)


# Run the script
if __name__ == "__main__":
    print("Creating authors...")
    authors = create_authors()

    print("Creating genres...")
    genres = create_genres()

    print("Creating books...")
    create_books(authors, genres)

    print("Data population complete!")
