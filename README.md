# Critics-Spot
![alt text](image.png)
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
├── critics_spot/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
└── requirements.txt
```


### User Routes

- **`/api/users/`**: User-related operations.
  - **`POST /api/users/`**: Create a new user.
  - **`GET /api/users/`**: List all users.
  - **`GET /api/users/{id}/`**: Retrieve a specific user.
  - **`PUT /api/users/{id}/`**: Update a specific user.
  - **`DELETE /api/users/{id}/`**: Delete a specific user.

- **`/auth/users/activation/{uid}/{token}/`**: Activate a user account.
- **`/auth/users/reset_password_confirm/{uid}/{token}/`**: Confirm password reset.

### Book Routes

- **`/api/books/`**: Book-related operations.
  - **`POST /api/books/`**: Create a new book.
  - **`GET /api/books/`**: List all books.
  - **`GET /api/books/{id}/`**: Retrieve a specific book.
  - **`PUT /api/books/{id}/`**: Update a specific book.
  - **`DELETE /api/books/{id}/`**: Delete a specific book.

### Shelf Routes

- **`/api/shelves/`**: Shelf-related operations.
  - **`POST /api/shelves/`**: Create a new shelf.
  - **`GET /api/shelves/`**: List all shelves.
  - **`GET /api/shelves/{id}/`**: Retrieve a specific shelf.
  - **`PUT /api/shelves/{id}/`**: Update a specific shelf.
  - **`DELETE /api/shelves/{id}/`**: Delete a specific shelf.

### Community Routes

- **`/api/communities/`**: Community-related operations.
  - **`POST /api/communities/`**: Create a new community.
  - **`GET /api/communities/`**: List all communities.
  - **`GET /api/communities/{id}/`**: Retrieve a specific community.
  - **`PUT /api/communities/{id}/`**: Update a specific community.
  - **`DELETE /api/communities/{id}/`**: Delete a specific community.

- **`/api/communities/{community_id}/posts/`**: Community post-related operations.
  - **`POST /api/communities/{community_id}/posts/`**: Create a new post in a community.
  - **`GET /api/communities/{community_id}/posts/`**: List all posts in a community.
  - **`GET /api/communities/{community_id}/posts/{id}/`**: Retrieve a specific post in a community.
  - **`PUT /api/communities/{community_id}/posts/{id}/`**: Update a specific post in a community.
  - **`DELETE /api/communities/{community_id}/posts/{id}/`**: Delete a specific post in a community.

- **`/api/communities/{community_id}/posts/{post_id}/comments/`**: Post comment-related operations.
  - **`POST /api/communities/{community_id}/posts/{post_id}/comments/`**: Create a new comment on a post.
  - **`GET /api/communities/{community_id}/posts/{post_id}/comments/`**: List all comments on a post.
  - **`GET /api/communities/{community_id}/posts/{post_id}/comments/{id}/`**: Retrieve a specific comment on a post.
  - **`PUT /api/communities/{community_id}/posts/{post_id}/comments/{id}/`**: Update a specific comment on a post.
  - **`DELETE /api/communities/{community_id}/posts/{post_id}/comments/{id}/`**: Delete a specific comment on a post.

### Swagger Documentation

- **`/api/docs/`**: Swagger UI for API documentation.
- **`/api/redoc/`**: ReDoc UI for API documentation.

### Debug Toolbar

- **`/__debug__/`**: Django Debug Toolbar.

### Static and Media Files

- **`/static/`**: Static files.
- **`/media/`**: Media files.


for more details on all the routes and methods see the documentation at 
the route `api/docs`


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

## Challenges and Solutions

### Issue with Applying Email Verification and Password Reset Features
**Challenge**: During the implementation of email verification and password reset, integrating with an email-sending service proved tricky. Setting up the email backend and ensuring emails were properly delivered to users' inboxes (not spam) required adjustments to configurations.

**Solution**: We used Django's and djoser’s built-in email utilities. Configurations for email templates and backend were fine-tuned. Testing with multiple email accounts helped ensure consistent delivery.

### Dependencies and Environment Conflicts
**Challenge**: The backend developers were using different operating systems—one on Linux and the other on Windows with WSL. This caused compatibility issues with dependencies (e.g., some Python packages behaving differently across platforms).

**Solution**: We created two separate virtual environments for each OS, ensuring all required dependencies were correctly installed and configured. This avoided cross-platform conflicts without resorting to Docker.

**Challenge**: Having a hard time making hyperlinks for nested routes for the api in some apps due to bugs in django rest-framework.

**Solution**: Avoiding nested routes as much as possible and using other field options like dictionaries and strings.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments
- Django and Django Rest Framework for the powerful backend
- React for the frontend (if applicable)
- Goodreads for the inspiration

## Contributors
- Mohamed Ali ([7amzawey](https://github.com/7amzawey))
- Eyad AbdelFattah ([eyadfattah23](https://github.com/eyadfattah23))