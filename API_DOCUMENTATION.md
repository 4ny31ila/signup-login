# API Documentation

This document provides a comprehensive guide to the API endpoints available in this project.

## Authentication

Endpoints that require authentication expect a JSON Web Token (JWT) to be included in the `Authorization` header of the request, using the `Bearer` scheme.

**Example Header:**
```
Authorization: Bearer <your_jwt_token>
```

---

## Endpoints

### 1. User Registration

- **Method:** `POST`
- **Path:** `/register`
- **Description:** Creates a new user account.

**Request Body:**
```json
{
  "username": "your_username",
  "email": "your_email@example.com",
  "password": "your_password"
}
```

**Success Response (201 Created):**
```json
{
  "id": 1,
  "username": "your_username",
  "email": "your_email@example.com"
}
```

**Error Response (400 Bad Request):**
```json
{
  "error": "User with this email already exists."
}
```
```json
{
  "error": "Invalid JSON or missing fields"
}
```

---

### 2. User Login

- **Method:** `POST`
- **Path:** `/login`
- **Description:** Authenticates a user and returns a JWT.

**Request Body:**
```json
{
  "email": "your_email@example.com",
  "password": "your_password"
}
```

**Success Response (200 OK):**
```json
{
  "token": "your_jwt_token"
}
```

**Error Response (401 Unauthorized):**
```json
{
  "error": "Invalid email or password"
}
```
```json
{
  "error": "Invalid JSON or missing fields"
}
```

---

### 3. Get User Profile

- **Method:** `GET`
- **Path:** `/profile`
- **Description:** Retrieves the profile of the authenticated user.
- **Authentication:** Required.

**Success Response (200 OK):**
```json
{
  "id": 1,
  "username": "your_username",
  "email": "your_email@example.com"
}
```

**Error Response (404 Not Found):**
```json
{
  "error": "User not found"
}
```

---

### 4. Update Password

- **Method:** `PUT`
- **Path:** `/profile/password`
- **Description:** Updates the password of the authenticated user.
- **Authentication:** Required.

**Request Body:**
```json
{
  "new_password": "your_new_secure_password"
}
```

**Success Response (200 OK):**
```json
{
  "message": "Password updated successfully"
}
```

**Error Response (400 Bad Request):**
```json
{
  "error": "Invalid JSON or missing 'new_password' field"
}
```

**Error Response (404 Not Found):**
```json
{
  "error": "User not found"
}
```

---

### 5. Delete User Profile

- **Method:** `DELETE`
- **Path:** `/profile`
- **Description:** Deletes the profile of the authenticated user.
- **Authentication:** Required.

**Success Response (204 No Content):**
- The response will have an empty body.

**Error Response (404 Not Found):**
```json
{
  "error": "User not found"
}
```
