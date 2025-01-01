# goodreads-clone
A back-end clone to goodreads.com platform,which is a huge platform for book readers, authors and reviews,


## commands used:
1. `psql -U goodreads_clone_dev -d goodreads_clone_dev_db -h localhost -W` ==> access the database using psql terminal.

2. `pip3 install psycopg2-binary` ==> the PostgreSQL Driver to allow Django to work with PostgreSQL

3. `pip3 freeze > requirements.txt ` ==> get all required packages

4. `sudo -u postgres psql` ==> open the psql as the superuser postgres

5. `python3 -m venv goodreads_clone_venv` to create a virtual environment
6. `source goodreads_clone_venv/bin/activate` to run this venv
7. `sudo service postgresql restart`


## architecture:
```bash
myproject/
│
├── manage.py
├── myproject/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│
├── users/ #done
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── serializers.py
│
├── books/ # done
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── serializers.py
│
├── reviews/ #done
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── serializers.py
│
├── groups/ #done
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── serializers.py
│
├── shelves/ # done 
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── serializers.py
│
├── favorites/ #done
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── serializers.py
│
```


### Using add() After Creating the Book
```python
# Create the genres
genre1 = Genre.objects.get_or_create(name="Fiction")[0]
genre2 = Genre.objects.get_or_create(name="Adventure")[0]

# Create the book
book = Book.objects.create(
    title="The Adventures of Sherlock Holmes",
    publication_date="1892-10-14",
    pages=307,
    description="A collection of Sherlock Holmes stories.",
)

# Add the genres to the book
book.genres.add(genre1, genre2)
```
* `get_or_create()` ensures you don't create duplicate genres.
* The `add()` method associates the `Genre` instances with the `Book`.


### 2. Backend Search Logic
Basic Search Functionality

Start with a simple search by querying the Book table using Django's ORM.

In your `views.py`:

```python
from django.db.models import Q
from django.shortcuts import render
from .models import Book

def book_search(request):
    query = request.GET.get('q', '')  # Get the search query from URL parameters
    books = Book.objects.filter(
        Q(title__icontains=query) |  # Search in the title
        Q(description__icontains=query) |  # Search in the description
        Q(author__name__icontains=query)  # Search in the author's name
    )
    return render(request, 'book_search.html', {'books': books, 'query': query})

```
**Explanation of `Q`**:

* `icontains`: Case-insensitive search for matching substrings.
* `Q`: Allows you to combine multiple conditions (title, description, author) with an OR operator.
---
to solve this problem:
I get the following error:

ERROR:  database "pilot" is being accessed by other users
DETAIL:  There is 1 other session using the database.

run : `sudo service postgresql restart`
---

### How to Get All Books in a Specific Genre?

If you're using the BookGenre junction table:
```python
# Query for all books in a specific genre
genre_name = "Fiction"
books_in_genre = Book.objects.filter(bookgenre__genre__name=genre_name)
```

If using ManyToManyField:
```python
books_in_genre = Book.objects.filter(genres__name="Fiction")
```
### How to Get All Genres of a Book?

If using BookGenre:

book_id = 1
genres_of_book = Genre.objects.filter(bookgenre__book_id=book_id)

If using ManyToManyField:
```python
book = Book.objects.get(id=1)
genres_of_book = book.genres.all()
```

**Note**: use this `results?search_query=postgresql+tutorial` url example to implement search functionality
---


## Superuser/Admin:
Username: admin
Email: admin@grclone.com
Password: grclone_admin_pwd


{
        "title": "Tom and Jerry",
        "description": "test post request novel",
        "author": "http://127.0.0.1:8000/api/authors/1",
        "genres": [
            "http://127.0.0.1:8000/api/genres/3",
            "http://127.0.0.1:8000/api/genres/2",
            "http://127.0.0.1:8000/api/genres/1"
        ]
    }

## steps for changing the auth method for you psql user
first step 
you look up the file on your local machine
using this command
    psql -u postgres -c "SHOW hba_file.conf"

reload postgres server using

sudo service postgresql reload 

then you look up your user and change its auth method from peer (the default) to md5

but if it's not there at all you can add the user along with the auth method md5 in our case


## in case of getting this error:
duplicate key value violates unique constraint "users_customuser_pkey" DETAIL: Key (id)=(10) already exists.

1. First, you need to check the max(id) in your table.
    SELECT MAX(id) FROM users_customuser;

2. Then update the id sequence to start from the 
max(id) + 1
    ALTER SEQUENCE users_customuser_id_seq RESTART
    WITH max(id) + 1;
---

### to reverse a link to to another page
reverse('admin:app_model_page')
