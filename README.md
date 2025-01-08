# Critics-Spot

## Overview
Critics-Spot is a web application that allows users to create and manage bookshelves, add books to their shelves, and interact with other users. The app provides functionalities for user registration, authentication, and managing user profiles. Users can also add comments and likes to posts within communities.

## Features
- **User Registration and Authentication**: Users can register, log in, and obtain authentication tokens.
- **User Profiles**: Users can update their profiles and view their favorite books.
- **Bookshelves**: Users can create, update, and delete bookshelves. They can also add, update, and remove books from their shelves.
- **Books**: Users can add new books, update book details, and delete books.
- **Communities**: Users can create posts, add comments, and like posts within communities.

## Installation
1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/critics-spot.git
   cd critics-spot
   ```

2. **Set up a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a superuser**:
   ```bash
   python manage.py createsuperuser
   ```

## Running the Application
1. **Start the development server**:
   ```bash
   python manage.py runserver
   ```

2. **Access the application**:
   Open your web browser and navigate to [http://localhost:8000/api/](http://localhost:8000/api/)

## Project Architecture
The project follows a standard Django architecture with the following structure:

```
critics-spot/
├── books/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── permissions.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── communities/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── permissions.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── shelves/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── permissions.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── users/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── goodreads_clone/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
└── requirements.txt
```
## API Endpoints
- `/api/users/`: User registration and management
- `/auth/jwt/`: Obtain JWT tokens
- `/api/bookshelves/`: Bookshelf management
- `/api/books/`: Book management
- `/api/communities/`: Community and post management

For detailed API documentation, refer to the API docs at `/api/docs/` when the server is running.

## Testing
Run the test suite using:
```bash
python manage.py test # for testing the models.
pytest # for testing the api routes.
```

## Contributing
1. **Fork the repository**
2. **Create your feature branch**:
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. **Commit your changes**:
   ```bash
   git commit -m 'Add some AmazingFeature'
   ```
4. **Push to the branch**:
   ```bash
   git push origin feature/AmazingFeature
   ```
5. **Open a Pull Request**

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments
- Django and Django Rest Framework for the powerful backend
- React for the frontend (if applicable)
- Goodreads for the inspiration

## Contributors
- Mohamed Ali ([7amzawey](https://github.com/7amzawey))
- Eyad AbdelFattah ([eyadfattah23](https://github.com/eyadfattah23))
