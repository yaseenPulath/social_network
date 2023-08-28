# Social Networking Application API

This project implements a social networking application API using Django Rest Framework. The API offers a range of functionalities for user management and friend requests. Below are the details of the implemented functionalities and the overall structure of the project.

`Except for the registration and login endpoints, you'll need to include the JWTAuth token in your requests. This token ensures proper authentication and access to secured functionalities. 
For the Authorization Type, select Bearer Token.
In the Token field, use the JWTAuth token`
## Easy Evaluation with Postman Collection

have included a Postman collection in this repo for testing our API endpoints. It's designed for quick and efficient evaluation.


## Seamless Authentication

Our collection includes an automation script that sets ``JWTToken-<userid>`` variables in tests. No need to copy-paste tokens. Just remember the user IDs for smooth authorization. To utilize this, choose the Bearer Token as the authentication type and use ``{{JWTToken-<userid>}}`` in the token field.

## Getting Started

To set up the project locally, follow these steps:

1. Clone the repository: 
    ```shell
    git clone <repository-url>
    ```
2. Navigate to the project directory: 
    ```bash
    cd social_network
    ```
3. install docker

    `https://docs.docker.com/engine/install/`

4. to start the development process run the below command

    ```bash
    docker compose -f docker.compose.development.yml up --build backend
    ```

## Functionality Implemented

### User Signup and Login

- **Quick Signup:** Users can sign up with their email, and a random password is generated for their account at the backend.
- **Token Access:** After successful signup, users receive a 24-hour valid authentication token for application access.
- **Token Expiry:** If the token expires, users can still use the signup API to get a new token for the next 24 hours.
- **User-Friendly:** This prevents frustration if users return after a while and find their token expired.
- **Security Boost:** To complete registration, users are prompted to change their password using the "change_password" endpoint as a response to the registration api.
- **Registration Completed:** After password change, users cannot re-register with the same email; they can use the login API for a valid token.
- **Security & Satisfaction:** This strategy ensures robust security and maintains a seamless user experience.
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

**API Endpoint**: 

```bash
POST http://localhost:8000/api/user/register
```

**Description**: This endpoint allows users to register using their email. A random password is generated and associated with the user's account at the backend. An authentication token is returned upon successful signup, which is valid for 24 hours.

**Sample Request Body**:

```json
{
    "email": "user@example.com"
}
```
**Sample Success Response (Status Code: 201 Created)**:
```json
{
    "status": "Success",
    "message": "User registered successfully. Please update password to avoid security risks.",
    "detail": {
        "id": 123,
        "email": "user@example.com",
        "token": "sample_token_here"
    }
}

```
**Sample Failure Response (Status Code: 400 Bad Request)**:

```json
{
    "status": "Failure",
    "message": "Email is already taken."
}
```
### Change User Password

**API Endpoint**:
 ```bash
 PATCH http://localhost:8000/api/user/profile/change-password
 ```

**Description**: This endpoint allows users to change their account password using the JWT token received during signup or login. This new password will allow users to log in to the system after the authentication token has expired.

**Sample Request Body**:

```json
{
    "password": "newPassword"
}
```
**Sample Success Response (Status Code: 200 OK)**:
```json
{
    "status": "Success",
    "message": "Password changed successfully."
}
```
**Sample Failure Response (Status Code: 400 Bad Request)**:

```json
{
    "status": "Failure",
    "message": "password can't me empty"
}
```
### User Login

**API Endpoint**: 
```bash
POST http://localhost:8000/api/user/login
```

**Description**: This endpoint enables users to log in using their email and the password. Upon successful login, a JWT token is provided, which is valid for 24 hours.

**Sample Request Body**:

```json
{
    "email": "user@example.com",
    "password": "password"
}
```
**Sample Success Response (Status Code: 200 OK)**:
```json
{
    "status": "Success",
    "message": "User logged in successfully.",
    "detail": {
        "token": "sample_token_here",
        "id": 1,
        "email": "user@example.com"
    }
}
```
**Sample Failure Response (Status Code: 400 Bad Request)**:

```json
{
    "status": "Failure",
    "message": "Invalid credentials. Please try again."
}
```

### Update Profile

**API Endpoint**: 
```bash
PATCH http://localhost:8000/api/user/profile/update-profile
```

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
**Sample Success Response (Status Code: 200 OK)**:
```json
{
    "status": "Success",
    "message": "Profile updated successfully.",
    "detail": {
        "user_id": 1,
        "username": "yaseen",
        "email": "yaseen@gmail.com",
        "date_of_birth": "1996-04-17",
        "gender": "Male",
        "interests": "coding",
        "about": "Developer"
    }
}
```
**Sample Failure Response (Status Code: 400 Bad Request)**:

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

**API Endpoint**:

```bash
GET http://localhost:8000/api/user/profile/search?email=gmail
```

**Description**: This endpoint allows users to search for other user profiles using their email or name as a search keyword. Matching profiles are returned in the response. Pagination is implemented with a page size of 10, so the API response will include up to 10 records per page.

**Sample Response (Status Code: 200 OK)**:
```json
{
    "count": 15,
    "next": "sample_next_url",
    "previous": null,
    "results": [
        {
            "user_id": 3,
            "username": "sample_username",
            "interests": "sample_interests",
            "about": "sample_about"
        }
        ...
    ],
    "is_exact_match": false
}
```

### Send Friend Request

**API Endpoint**: 
```bash
POST http://localhost:8000/api/friend-request
```

**Description**: This endpoint lets users send friend requests to other users.

**Sample Request Body**:

```json
{
    "user_id" : 6
}
```
**Sample Success Response (Status Code: 201 Created)**:
```json
{
    "status": "Success",
    "message": "Friend request sent successfully.",
    "detail": {
        "request_id": 1
    }
}
```
**Sample Failure Response (Status Code: 400 Bad Request)**:

```json
{
    "status": "Failure",
    "message": "There is already an open friend request between you and this user."
}
```
**Sample Failure Response (Status Code: 429 Many Requests)**:

```json
{
    "detail": "Request was throttled. Expected available in 48 seconds."
}
```
### Accept Friend Request

**API Endpoint**: 
```bash
PATCH http://localhost:8000/api/friend-request/<request_id>
```

**Description**: This endpoint allows users to accept friend requests received from other users.

**Sample Request Body**:

```json
{
    "action": "accept-request"
}
```
**Sample Success Response (Status Code: 200 OK)**:
```json
{
    "status": "Success",
    "message": "Friend request accepted successfully.",
    "detail": {
        "user_id": 1,
        "username": "yaseen",
        "email": "yaseen3@gmail.com",
        "date_of_birth": "1996-04-17",
        "gender": "Male",
        "interests": "coding",
        "about": "Developer"
    }
}
```
**Sample Failure Response (Status Code: 400 Bad Request)**:

```json
{
    "status": "Failure",
    "message": "Friend Request Not Found"
}
```
**Sample Failure Response (Status Code: 401 Unauthorized)**:

```json
{
    "status": "Failure",
    "message": "You are not authorized to perform this action."
}
```
### Reject Friend Request

**API Endpoint**: 
```bash
PATCH http://localhost:8000/api/friend-request/<request_id>
```

**Description**: This endpoint allows users to reject friend requests received from other users.

**Sample Request Body**:

```json
{
    "action": "reject-request"
}
```

**Sample Success Response (Status Code: 200 OK)**:
```json
{
    "status": "Success",
    "message": "Friend request rejected successfully."
}
```
**Sample Failure Response (Status Code: 400 Bad Request)**:

```json
{
    "status": "Failure",
    "message": "Friend Request Not Found"
}
```
**Sample Failure Response (Status Code: 401 Unauthorized)**:

```json
{
    "status": "Failure",
    "message": "You are not authorized to perform this action."
}
```
### Accepted Friend Requests List

**API Endpoint**: 
```bash
GET http://localhost:8000/api/friend-request/sent-accepted
```

**Description**: This endpoint lists users who have accepted their friend requests. Pagination is implemented with a page size of 10, so the API response will include up to 10 records per page.

**Sample Success Response (Status Code: 200 OK)**:
```json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "request_id": 1,
            "request_created_at": "2023-08-28 15:38:20",
            "request_accepted_at": "2023-08-28 15:53:56",
            "to_user": {
                "user_id": 2,
                "username": null,
                "email": "Ladarius_Rempel31@hotmail.com"
            }
        }
    ]
}
```
### Pending Friend Requests

**API Endpoint**: 
```bash
GET http://localhost:8000/api/friend-request/received-pending
```

**Description**: This endpoint lists friend requests that users have received and are pending acceptance. Pagination is implemented with a page size of 10, so the API response will include up to 10 records per page.

**Sample Success Response (Status Code: 200 OK)**:
```json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "request_id": 11,
            "request_created_at": "2023-08-28 04:35:51",
            "from_user": {
                "user_id": 1,
                "username": "yaseen"
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

