# Social Media API Documentation

## Authentication

### Register a New User

- **URL**: `/api/accounts/register/`
- **Method**: POST
- **Data**:
  ```json
  {
    "username": "string",
    "password": "string",
    "password2": "string",
    "email": "string",
    "first_name": "string",
    "last_name": "string",
    "bio": "string",
    "profile_picture": "file"
  }
  ```
- **Success Response**: 201 Created
  ```json
  {
    "token": "string",
    "user_id": "integer",
    "username": "string"
  }
  ```

### Login

- **URL**: `/api/accounts/login/`
- **Method**: POST
- **Data**:
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```
- **Success Response**: 200 OK
  ```json
  {
    "token": "string",
    "user_id": "integer",
    "username": "string"
  }
  ```

## User Profile Management

### View/Update Profile

- **URL**: `/api/accounts/profile/`
- **Methods**: GET, PATCH
- **Authentication**: Required
- **PATCH Data**:
  ```json
  {
    "first_name": "string",
    "last_name": "string",
    "bio": "string",
    "profile_picture": "file"
  }
  ```

## Follow System

### Follow a User

- **URL**: `/api/accounts/follow/<user_id>/`
- **Method**: POST
- **Authentication**: Required
- **Success Response**: 200 OK
  ```json
  {
    "message": "You are now following username"
  }
  ```
- **Error Response**: 400 Bad Request
  ```json
  {
    "error": "You cannot follow yourself"
  }
  ```

### Unfollow a User

- **URL**: `/api/accounts/unfollow/<user_id>/`
- **Method**: POST
- **Authentication**: Required
- **Success Response**: 200 OK
  ```json
  {
    "message": "You have unfollowed username"
  }
  ```
- **Error Response**: 400 Bad Request
  ```json
  {
    "error": "You cannot unfollow yourself"
  }
  ```

## Posts

### Create a Post

- **URL**: `/api/posts/posts/`
- **Method**: POST
- **Authentication**: Required
- **Data**:
  ```json
  {
    "title": "string",
    "content": "string"
  }
  ```

### List All Posts

- **URL**: `/api/posts/posts/`
- **Method**: GET
- **Query Parameters**:
  - `page`: Page number for pagination
  - `search`: Search in title and content
  - `author`: Filter by author ID
  - `ordering`: Order by created_at or updated_at

### User Feed

- **URL**: `/api/posts/feed/`
- **Method**: GET
- **Authentication**: Required
- **Description**: Returns posts from users that the authenticated user follows
- **Query Parameters**:
  - `page`: Page number for pagination
  - `page_size`: Number of posts per page (default: 10, max: 100)

## Comments

### Create a Comment

- **URL**: `/api/posts/comments/`
- **Method**: POST
- **Authentication**: Required
- **Data**:
  ```json
  {
    "post": "integer",
    "content": "string"
  }
  ```

### List Comments

- **URL**: `/api/posts/comments/`
- **Method**: GET
- **Query Parameters**:
  - `post`: Filter by post ID
  - `author`: Filter by author ID
  - `ordering`: Order by created_at
