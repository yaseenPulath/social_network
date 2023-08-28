# Social Networking Application API

Welcome to the Social Networking Application API documentation. This repository contains the implementation of a social networking application's API using Django Rest Framework. The API offers a range of functionalities for user management and friend requests. Below are the details of the implemented functionalities and the overall structure of the project.

## Getting Started

To set up the project locally, follow these steps:

1. Clone the repository: `git clone <repository-url>`
2. Navigate to the project directory: `cd social_network`
3. Create a Virtual Environment

    It's recommended to use a virtual environment to isolate project dependencies. You can create a virtual environment using the following command:

   ```shell
   python -m venv env
   ```

    Activate the virtual environment:

    On Windows:
    ```shell
    env\Scripts\activate
    ```
    On macOS and Linux:
    ```shell
    source env/bin/activate
    ```
3. Install the required dependencies: `pip install -r requirements.txt`
4. Apply database migrations: `python manage.py migrate`
5. Run the development server: `python manage.py runserver`

## Functionality Implemented

### User Signup and Login

- Users can sign up with their email. A random password is generated and associated with the user's account at the backend. An authentication token is returned upon successful signup, which is valid for 24 hours.
- With the help of the authentication token, users can change their password to a known password.

### Changing Password

- Users can change their account password using the JWT token received during signup or login.
- This password will allow users to log in to the system even after the authentication token expired.

### User Profile

- User profiles are associated with the main user model, containing additional information to make the profile more appealing.

### User Search

- Users can search for other users using either their email or name as a search keyword.
- If the search keyword matches an exact email, the user associated with that email is returned.
- If the search keyword contains any part of a user's name, a list of matching users is returned.

### Friend Requests

- Users can send friend requests to other users.
- Users can accept or reject received friend requests.
- Users cannot send more than 3 friend requests within a minute.

### Friends List

- Users can list their accepted friends, showing the users who have accepted their friend requests.

### Pending Friend Requests

- Users can list friend requests that they have received and are pending acceptance.

### Additional APIs

- **Update Profile**: Users can update their profile information.

## Project Structure

The project is structured into several components:

- **api**: Contains the main views and URLs for the API endpoints.
- **friends**: Manages friend requests and friendships using models and signals.
- **user**: Defines the user model and user profile for additional information.

## API Documentation

### User Registration

**URL Endpoint**: `http://localhost:8000/api/user/register`

**Description**: This endpoint allows users to register using their email. A random password is generated and associated with the user's account at the backend. An authentication token is returned upon successful signup, which is valid for 24 hours.

**Sample Request Body**:

```json
{
    "email": "example@example.com"
}
```
**Sample Success Response**:
```json
{
    "status": "Success",
    "message": "User registered successfully. Please update your password within 24 hours.",
    "id": 4,
    "email": "example@example.com",
    "token": "..."
}
```
**Sample Failure Response**:

```json
{
    "status": "Failure",
    "message": "User Already exists."
}
```
### Change User Password

**URL Endpoint**: `http://localhost:8000/api/user/change-password`

**Description**: This endpoint allows users to change their account password using the JWT token received during signup or login. This new password will allow users to log in to the system after the authentication token has expired.

**Sample Request Body**:

```json
{
    "password": "testPassword"
}
```
**Sample Success Response**:
```json
{
    "status": "Success",
    "message": "Password changed successfully."
}
```
**Sample Failure Response**:

```json
{
    "status": "Failure",
    "message": "password can't me empty"
}
```
### User Login

**URL Endpoint**: `http://localhost:8000/api/user/login`

**Description**: This endpoint enables users to log in using their email and the password. Upon successful login, a JWT token is provided, which is valid for 24 hours.

**Sample Request Body**:

```json
{
    "email": "yaseen@gmail.com",
    "password": "newpassword"
}
```
**Sample Success Response**:
```json
{
    "status": "Success",
    "message": "User logged in successfully.",
    "token": "...",
    "id": 1,
    "email": "yaseen@gmail.com"
}
```
**Sample Failure Response**:

```json
{
    "status": "Failure",
    "message": "Invalid credentials. Please try again."
}
```

### Update Profile

**URL Endpoint**: `http://localhost:8000/api/user/update-profile`

**Description**: This endpoint enables users to update their profile information. 

**Sample Request Body**:

```json
{
    "username": "yaseen",
    "password": "newpassword",
    "date_of_birth": "1996-04-17",
    "gender": "Male",
    "interests": "coding",
    "about": "Developer"
}
```
**Sample Success Response**:
```json
{
    "status": "Success",
    "message": "Profile updated successfully.",
    "user_id": 1,
    "username": "yaseen",
    "email": "yaseen3@gmail.com",
    "date_of_birth": "1996-04-17",
    "gender": "Male",
    "interests": "coding",
    "about": "Developer"
}
```
**Sample Failure Response**:

```json
{
    "status": "Failure",
    "Errors": {
        "date_of_birth": [
            "You must be at least 13 years old."
        ]
    },
    "message": "Please provide a valid data"
}
```

### Search for Other Profiles

**URL Endpoint**: `http://localhost:8000/api/user/search-users?email=gmail`

**Description**: This endpoint allows users to search for other user profiles using their email or name as a search keyword. Matching profiles are returned in the response. Pagination is implemented with a page size of 10, so the API response will include up to 10 records per page.

**Sample Response**:
```json
{
    "count": 15,
    "next": "http://localhost:8000/api/user/search-users?email=gmail&page=2",
    "previous": null,
    "results": [
        {
            "user_id": 3,
            "username": "Bertram",
            "email": "Bertram.Deckow37@gmail.com",
            "date_of_birth": null,
            "gender": null,
            "interests": null,
            "about": null
        },
        ...
    ]
}
```

### Send Friend Request

**URL Endpoint**: `http://localhost:8000/api/friend-request/1/send-request`

**Description**: This endpoint lets users send friend requests to other users.

**Sample Success Response**:
```json
{
    "status": "Success",
    "message": "Friend request sent successfully."
}
```
**Sample Failure Response**:

```json
{
    "status": "Failure",
    "message": "There is already an open friend request between you and this user."
}
```
### Accept Friend Request

**URL Endpoint**: `http://localhost:8000/api/friend-request/1/accept-request`

**Description**: This endpoint allows users to accept friend requests received from other users.

**Sample Success Response**:
```json
{
    "status": "Success",
    "message": "Friend request accepted successfully.."
}
```
**Sample Failure Response**:

```json
{
    "status": "Failure",
    "message": "Friend Request Not Found"
}
```
### Reject Friend Request

**URL Endpoint**: `http://localhost:8000/api/friend-request/1/reject-request`

**Description**: This endpoint allows users to reject friend requests received from other users.

**Sample Success Response**:
```json
{
    "status": "Success",
    "message": "Friend request rejected successfully."
}
```
**Sample Failure Response**:

```json
{
    "status": "Failure",
    "message": "Friend Request Not Found"
}
```

### Accepted Friend Requests List

**URL Endpoint**: `http://localhost:8000/api/friend-request/sent-accepted`

**Description**: This endpoint lists users who have accepted their friend requests. Pagination is implemented with a page size of 10, so the API response will include up to 10 records per page.

**Sample Success Response**:
```json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "request_created_at": "2023-08-27T15:42:48.411400Z",
            "request_accepted_at": "2023-08-27T15:44:55.407670Z",
            "to_user": {
                "user_id": 1,
                "username": "yaseen",
                "email": "yaseen3@gmail.com"
            }
        }
    ]
}
```
### Pending Friend Requests

**URL Endpoint**: `http://localhost:8000/api/friend-request/received-pending`

**Description**: This endpoint lists friend requests that users have received and are pending acceptance. Pagination is implemented with a page size of 10, so the API response will include up to 10 records per page.

**Sample Success Response**:
```json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "request_created_at": "2023-08-27T16:17:00.111852Z",
            "from_user": {
                "user_id": 2,
                "username": null,
                "email": "Christiana_Nicolas@yahoo.com"
            },
            "status": "sent",
            "days_since_updated": 0
        }
    ]
}
```


## Contributing

If you would like to contribute to this project, feel free to fork the repository and create a pull request with your changes.

## Credits

This project was developed by Mohammed Yaseen P. You can contact me at pulath.m.yaseen@gmail.com for any questions or inquiries.

