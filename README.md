
# Speer Backend Project

A secure and scalable RESTful API that allows users to create, read, update, and delete notes. The application also allow users to share their notes with other users and search for notes based on keywords.


## Framework Detais

#### Django Rest Framework

I chose Django REST framework to build a secure and scalable RESTful API for note-taking due to its seamless integration with Django, facilitating rapid development. The framework's robust features, including serialization, authentication, and viewsets, streamlined the implementation of CRUD operations, note sharing, and keyword-based search. This ensured efficient development and a reliable foundation for building a feature-rich and user-friendly application. 

#### PostgreSQL

PostgreSQL was the natural choice for the database in building my note-taking RESTful API. Renowned for its reliability and extensibility, PostgreSQL excels in managing complex data relationships and transactions. Its strong community support and compatibility with Django made it an ideal fit, ensuring data integrity, scalability, and optimal performance for a seamless user experience.

#### django-filters (Library)

For robust and secure authentication in my note-taking RESTful API, I integrated djangorestframework-simplejwt with Django REST framework. This token-based authentication solution enhances user data protection, offering JSON Web Token (JWT) support. The simplicity and flexibility of this package seamlessly complemented Django REST framework, providing a reliable authentication layer for user interactions and data access.


#### djangorestframework-simplejwt (Library)

To empower users with efficient keyword-based search functionality in my note-taking RESTful API, I integrated django-filter. This Django app simplifies the implementation of dynamic query parameters, enhancing the API's search capabilities. Leveraging django-filter ensures a user-friendly and responsive experience, allowing users to effortlessly find relevant notes based on their keywords.

## Run Locally

### Requirements
- docker
- docker-compose

NOTE: I have already shared .env file in this repository for easy setup 😉

### Running the project

Clone the project

```bash
  git clone https://github.com/prathameshramane/speer-app.git
```

Go to the project directory

```bash
  cd speer-app
```

Run docker-compose command

```bash
  docker-compose up -d --build
```

Start will start at port 8000

```bash
  http://localhost:8000
```

### Running test cases

Run the following command to execute test cases

```bash
  docker-compose exec app python manage.py test
```

## API Reference

### Auth endpoints

#### Register user

```http
  POST /api/auth/signup
```

| Request Body | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `username` | `string` | **Required**. Unique username for the user.|
| `email` | `string` | **Required**. Email of the user.|
| `password` | `string` | **Required**. Strong password for the user.|
| `first_name` | `string` | **Required**. First name of the user.|
| `last_name` | `string` | **Required**. Last name of the user.|



#### Login User

```http
  POST /api/auth/login
```

| Request Body | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `username`      | `string` | **Required**. Registered username of the user.|
| `password`      | `string` | **Required**. Correct password for the user|



#### Refresh Token

```http
  POST /api/auth/refresh
```

| Request Body | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `refresh`      | `string` | **Required**. Refresh token recevied as response of login api.|


### Notes Endpoint

#### Get all notes for user

```http
  GET /api/notes/
```

#### Note details

```http
  GET /api/notes/${id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `number` | **Required**. Id of the note|

#### Search note based on keyword

```http
  GET /api/search/?q=:query
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `search`      | `string` | **Required**. Keyword to search for.|
| `description`      | `string` | **Required**. Search based on description.|

NOTE: Currently both give same result.

#### Create a new note

```http
  POST /api/notes/
```

| Request Body | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `description`      | `string` | **Required**. Note description.|

#### Update note

```http
  PUT /api/notes/
```

| Request Body | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `description`      | `string` | **Required**. Note description.|

#### Delete note

```http
  DELETE /api/notes/${id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `description`      | `string` | **Required**. Note description.|
