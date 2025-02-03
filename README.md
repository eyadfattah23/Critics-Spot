# Critics-Spot
![alt text](image.png)
## Overview
Critics-Spot is a web application that allows users to create and manage bookshelves, add books to their shelves, know where to buy these books from, and interact with other users. The app provides functionalities for user registration, authentication, and managing user profiles. Users can also add comments and likes to posts within communities.

## Features
- **User Registration and Authentication**: Users can register, log in, and obtain authentication tokens.
- **User Profiles**: Users can update their profiles and view their favorite books.
- **Bookshelves**: Users can create, update, and delete bookshelves. They can also add, update, and remove books from their shelves.
- **Books**: Users can add new books, update book details, and delete books.
- **Communities**: Users can create posts, add comments, and like posts within communities.

### [short features video](https://drive.google.com/file/d/12IZEr3W_MHP3Qr5o1VH4XI8ILHxA51M1/view?usp=drivesdk)
### [presentation](https://docs.google.com/presentation/d/14l8wjkGlodnNFtiX65iqRRUrZHDswzsH_qDQ2Si-vu4/edit?usp=drive_link)
## Installation
* ### 1. **Clone the repository**:
   ```bash
   git clone https://github.com/eyadfattah23/critics-spot.git
   cd critics-spot
   ```

* ### 2. **install python3 and pip3 if not already installed**:
    ```bash
    sudo apt install -y software-properties-common
    sudo add-apt-repository -y ppa:deadsnakes/ppa
    sudo apt update
    sudo apt install -y python3.10 python3.10-venv python3.10-dev

    python3 --version
    ```
* ### 3. **install and setup postgresql-14 if not already installed**:
    ```bash
    sudo apt update
    wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
    echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -cs)-pgdg main" | sudo tee /etc/apt/sources.list.d/postgresql-pgdg.list > /dev/null
    sudo apt update
    sudo apt install postgresql-14
    sudo apt install postgresql postgresql-contrib
    sudo service postgresql start
    ```
* ### 4. **prepare the databases**:
    ```bash
    ./database_creation.sh
    ```
    **if `FATAL: Peer authentication failed for user "postgres"` arises refer to this [link](https://stackoverflow.com/questions/18664074/getting-error-peer-authentication-failed-for-user-postgres-when-trying-to-ge) and [this one](https://stackoverflow.com/questions/18664074/getting-error-peer-authentication-failed-for-user-postgres-when-trying-to-ge)**

* ### 5. **Set up a virtual environment**:
   ```bash
   apt install python3-venv
   python3.10 -m venv venv
   source venv/bin/activate
   ```

* ### 6. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```


* ### 7. **create`.env` file**:
    create an app password using this [link](https://myaccount.google.com/apppasswords?pli=1&rapt=AEjHL4OOoBqDwmuaqYhjHZjIZ0LdXCFVqzXUcphwXe7ybYLEjhsgpT3swJEYpopNtN1pCtv7MiXSY9cxFSM1B2AJUujbVnp4vqXbyGa8qYDPEU_rpg13hmc) if you're using gmail.
    ```bash
    $# cat .env
    EMAIL_HOST_USER="your_email_host"
    EMAIL_HOST_PASSWORD="application_password_created_above"
    DEFAULT_FROM_EMAIL="default_email" # usually same as host
    ```

* ### 8. **migrate the tables**:
   ```bash
   python3.10 manage.py makemigrations
   python3.10 manage.py migrate
   ```
   if any error is encountered delete all migrations using the following command:
   `find . -path "*/migrations/*.py" ! -path "./.env/*" ! -name "__init__.py" -delete`.

   [then migrate the tables again.](#8-migrate-the-tables)


* ### 9. **Create a superuser**:
   ```bash
   python manage.py createsuperuser
   ```
    and enter your credentials for this superuser/admin account.

* ### 10. **activate this new superuser**:
    a. open the psql shell:
    ```bash
    sudo psql -U postgres
    ```
    b. connect to the development database:
    ```psql
    postgres=# \c goodreads_clone_dev_db;
    ```
    c. change the `is_active` parameter in the table `users_customeuser`:
    ```psql
    goodreads_clone_dev_db=# update users_customuser set is_active = TRUE  where email='{EMAIL_USED_WHEN_CREATING_THE_SUPERUSER}';
    ```
    **NOTE: you can use any piece of credentials you want instead of email (e.g. id = 1, username = 'admin', ...etc.) run: `goodreads_clone_dev_db=# select * from users_customuser;`** to see the suitable piece of data for you


* ### 11. [Run the application](#running-the-application)


* ### 12. Open your web browser and navigate to [http://localhost:8000/admin/](http://localhost:8000/admin/) then login using the credentials you used with the command `python3.10 manage.py createsuperuser`

    ### ***AND NOW YOU HAVE ACCESS TO THE ADMIN PANEL!!!***

## Running the Application
### 1. **Start the development server**:
   ```bash
   python3.10 manage.py runserver;
   ```

### 2. **Access the application**:

#### a. use your preferred rest api access tool like postman or curl in terminal.
> **we recommend that you use the django rest-framework webpage (`http://localhost:8000/api/{ROUTE}/` or `http://localhost:8000/auth/{ROUTE}/`) in your browser or postman instead of the curl command in the terminal for ease of use.**

#### b. if you want to login immediately with the superuser account created earlier jump to step 4.
    
#### c. send a POST request to **`POST http://localhost:8000/auth/users/`**.
example:

```bash
    curl -H "Content-Type: application/json" -X POST -d '{"username": "tester_user", "email": "tester@gmail.com", "password": "Pass#test123", "password_confirm": "Pass#test123", "first_name": "Test", "last_name": "User"}' http://localhost:8000/auth/users/
```

now this user (`tester_user`) will  receive an activation email on `tester@gmail.com` which will have an activation link like this:
    `http://127.0.0.1:8000/auth/users/activation/MTA/cjb2x8-7ab038931019f4316ec8a816af90646a/`

### 3. from here we have 2 scenarios (since the application is not deployed yet):**

* email inbox is on the same device as the application --> just click on the activation link

* email inbox is not on the same device as the application. --> either activate by going to the admin panel, clicking on the new_user's id and editing `Active` parameter for this user, OR using the [psql command used in installation to create a super user](#10-activate-this-new-superuser)


### 4. Login and save the access token:

now send a POST request to `http://localhost:8000/auth/jwt/create` with the email and password.
example:
```bash
curl -H "Content-Type: application/json" -X POST -d { "email": "tester@gmail.com", "password": "Pass#test123"} http://localhost:8000/auth/jwt/create/
```
which will result in a response like this:
```bash
{
"refresh":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczNzk4NzQ2NywiaWF0IjoxNzM3OTAxMDY3LCJqdGkiOiIxMTM3Yjg4MWRjYWM0MzhjOTI5YmQzOTNkM2E1YjBhYSIsInVzZXJfaWQiOjExfQ.2jy_R9-CNJAtx2SU8N4CFdHxjz-5C4hI3_T-CNzmiYI",

"access":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM3OTg3NDY3LCJpYXQiOjE3Mzc5MDEwNjcsImp0aSI6IjhkNTkxYzNiN2YxMTQyYWNiOWM2M2Y4YzNkYmU3MjZiIiwidXNlcl9pZCI6MTF9.DOqizcVDmlYcWb2efSZJUmOHazoaV9GTVeNMq1wtad0"
}
```
this access token will be used to access all the routes of the application.

### 5. adding the access token to all your requests.
any request from here on out must have the header:
```json
"Authorization": "JWT {ACCESS_TOKEN}"
```
- If in browser, download an extension that passes headers like [**Mod Header**](https://chromewebstore.google.com/detail/modheader-modify-http-hea/idgpnmonknjnojddfkpgkljpfnnfcklj?hl=en) and [**Header Editor**](https://chromewebstore.google.com/detail/header-editor/eningockdidmgiojffjmkdblpjocbhgh?hl=en).

- If in postman, navigate to the `headers` tab and add a new header with the key `Authorization` and the value `"JWT {ACCESS_TOKEN}"`

- If using curl command:
    ```bash
    curl -H curl -H "Content-Type: application/json" -X GET -H "Authorization: JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM3OTg3NDY3LCJpYXQiOjE3Mzc5MDEwNjcsImp0aSI6IjhkNTkxYzNiN2YxMTQyYWNiOWM2M2Y4YzNkYmU3MjZiIiwidXNlcl9pZCI6MTF9.DOqizcVDmlYcWb2efSZJUmOHazoaV9GTVeNMq1wtad0" http://localhost:8000/auth/users/me/
    ``` 
    and response should be like this:
    ```json
    
    {
        "id": 11,
        "username": "tester_user",
        "email": "tester@gmail.com",
        "first_name": "Test",
        "last_name": "User",
        "date_joined": "2025-01-26T13:01:53Z",
        "image": "http://localhost:8000/media/profile_pictures/tester_user/profile.png",
        "shelves": [
            {
                "id": 41,
                "name": "Read",
                "url": "http://localhost:8000/api/shelves/41/",
                "image": null
            },
            {
                "id": 42,
                "name": "Currently Reading",
                "url": "http://localhost:8000/api/shelves/42/",
                "image": null
            },
            {
                "id": 43,
                "name": "Want To Read",
                "url": "http://localhost:8000/api/shelves/43/",
                "image": null
            },
            {
                "id": 44,
                "name": "Favorites",
                "url": "http://localhost:8000/api/shelves/44/",
                "image": null
            }
        ],
        "is_staff": false
    }
    ```
    well I know it's not this clean but it's the same. 😅

### **IMPORTANT NOTE**: most of the app won't work and you will get `401 Unauthorized` error  without using it


Again!! we recommend using the django rest-framework webpage (http://localhost:8000/api/{ROUTE}/ or http://localhost:8000/auth/{ROUTE}/) in your browser with a header extension as mentioned above or postman instead of the curl command in the terminal for ease of use.

don't forget to pass the header `"Authorization": "JWT {ACCESS_TOKEN}"`
---
### User Routes

- `/auth/users`**: User and authorization related operations.
  - **`POST /auth/users/`**: Create a new user. (registration route)
    * body:
        ```json
        {
            "username": "tester_user",
            "email": "tester@gmail.com",
            "password": "Pass#test123",
            "password_confirm": "Pass#test123",
            "first_name": "Test",
            "last_name": "User"
        }
        ```
  - **`POST /auth/jwt/create`**: Create a new jwt token by logging in.
    * body:
        ```json
        {
            "email": "tester@gmail.com",
            "password": "Pass#test123"
        }
        ```
  - **`GET /auth/users/`**: List all users. (only a super user can see all users)
  - **`GET /auth/users/{id}/`**: Retrieve a specific user. (you can only retrieve the Currently logged in user)
  - **`GET /auth/users/me/`**: Retrieve the Currently logged in user.
  - **`PUT/PATCH /api/users/{id}/`**: Update a specific user.
  - **`PUT/PATCH /auth/users/me/`**: Update the Currently logged in user.

- **`/auth/users/activation/{uid}/{token}/`**: Activate a user account.
- **`/auth/users/reset_password_confirm/{uid}/{token}/`**: Confirm password reset.

### Book Routes (and their reviews)

note: to get the best out of the books route you should:

1. **Populate the books table using the script named `populate_books_data.py` by running `python3 manage.py shell` and pasting the content of the file.**
2. **Add admin or librarian privileges to the current logged in user**(if logged in as an admin/superuser ignore this), **by using the script named `populate_group_permissions.sql` to populate permissions tables and then going to the admin panel to add the new privileges to the logged in user**(you can simply do all this in the admin panel by creating a new group in the groups table with the desired permissions then add this new group to the user in the custom users table)  

now for the **`/api/books/`** routes: Book-related operations.
  - **`POST /api/books/`**: Create a new book.

    * body:
        ```json
        {
            "title": "new book",
            "cover": "valid_file_url_or_remove_parameter_completely",
            "description": "description",
            "author": 2,
            "genres": [1, 2],
            "publication_date": "1925-04-10",
            "buy_link": "a_valid_full_url",
            "pages": 123
        }
        ```
  - **`GET /api/books/`**: List all books.
  - **`GET /api/books/{id}/`**: Retrieve a specific book.
  - **`PUT/PATCH /api/books/{id}/`**: Update a specific book. (Librarian or admin only)
    * body:
        ```json
        {
            "title": "new book",
            "description": "description",
            "author": 2,
            "genres": [
                1,
                2
            ],
            "publication_date": "1925-04-10",
            "buy_link": "https://mail.google.com/",
            "pages": 123
        }
        ```
  - **`DELETE /api/books/{id}/`**: Delete a specific book. (Librarian or admin only)

  - **`GET /api/books/{id}/reviews/`**: Get all reviews of a specific book. 
  - **`POST /api/books/{id}/reviews/`**: Create a new book review.
  - **`GET /api/reviews/{id}`**: Get a specific book review.
  - **`PUT/PATCH /api/reviews/{id}`**: Update a specific book review.
  - **`DELETE /api/reviews/{id}`**: Delete a specific book review.

### Authors routes
- **`/api/authors/`**: Authors-related operations.
  - **`POST /api/authors/`**: Create a new book.
  - **`GET /api/authors/`**: List all books.
  - **`GET /api/authors/{id}/`**: Retrieve a specific book.
  - **`PUT /api/auhtors/{id}/`**: Update a specific book.
### Genres routes
- **`/api/genres/`**: Genres-related operations.
  - **`POST /api/genres/`**: Create a new book.
  - **`GET /api/genres/`**: List all books.
  - **`GET /api/genres/{id}/`**: Retrieve a specific book.
  - **`PUT /api/genres/{id}/`**: Update a specific book.


### Shelf Routes

- **`/api/shelves/`**: Shelf-related operations.
  - **`GET /api/users/{user_id}/shelves/`**: List all shelves of a specific user.
  - **`GET /api/users/{user_id}/favorites/`**: Retrieve the favorites shelf of a specific user.
  - **`GET /api/users/{id}/shelves/`**: List all shelves owned by a specific user.
  - **`POST /api/users/{id}/shelves/`**: Add a new shelf for a specific user.

    * body:
        ```json
        {
            "name": "new shelf"
            //, "image" : "valid_image_file_or_remove_parameter_or_keep_this_parameter_commented"
        }
        ```
  - **`POST /api/shelves/`**: Create a new shelf.
  - **`GET /api/shelves/`**: List all shelves.
  - **`GET /api/shelves/{id}/`**: Retrieve a specific shelf.
  - **`PUT /api/shelves/{id}/`**: Update a specific shelf.
  - **`DELETE /api/shelves/{id}/`**: Delete a specific shelf.

  - **

### Community Routes

- **`/api/communities/`**: Community-related operations.
  - **`POST /api/communities/`**: Create a new community.
  - **`GET /api/communities/`**: List all communities.
  - **`GET /api/communities/{id}/`**: Retrieve a specific community.
  - **`PUT /api/communities/{id}/`**: Update a specific community.
  - **`DELETE /api/communities/{id}/`**: Delete a specific community.

  - **`POST /api/communities/{id}/join/`**: Join a community. (No body required).
  - **`POST /api/communities/{id}/leave/`**: leave a community. (No body required).
  - **`GET /api/communities/{id}/members/`**: List all members of a community.
    

- **`/api/communities/{community_id}/posts/`**: Community post-related operations.
  - **`POST /api/communities/{community_id}/posts/`**: Create a new post in a community.
    * body:
        ```json
            {  
                "content": "Just finished Dune – what an amazing book!"  
            }
        ```  
        
  - **`GET /api/communities/{community_id}/posts/`**: List all posts in a community.
  - **`GET /api/communities/{community_id}/posts/{id}/`**: Retrieve a specific post in a community.
  - **`PUT /api/communities/{community_id}/posts/{id}/`**: Update a specific post in a community.
  - **`DELETE /api/communities/{community_id}/posts/{id}/`**: Delete a specific post in a community.

  - **`POST /api/communities/{community_id}/posts/{post_id}/like/`**: Like a post. (No body required).
  - **`POST /api/communities/{community_id}/posts/{post_id}/unlike/`**: Like a post. (No body required).

- **`/api/communities/{community_id}/posts/{post_id}/comments/`**: Post comment-related operations.
    * body:
        ```json
            {  
                "content": "content": "Agreed! The world-building is incredible."  
            }
        ```  
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
