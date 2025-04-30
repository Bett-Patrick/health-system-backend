# 🏥 Health Information System – CEMA Internship Task

## Deployed Link
  #### [https://health-system-backend-yqbu.onrender.com](#https://health-system-backend-yqbu.onrender.com)

## 📋 Overview

This is a basic Health Information System built using **Flask**, designed to help doctors manage health programs and client data efficiently.  
It enables a doctor to:

- Create and manage health programs
- Register clients (patients)
- Enroll clients in specific programs
- Search and view client profiles
- Expose client profiles via an API

---

## ⚙️ Technologies Used

- **Python 3.11**
- **Flask** – Web framework
- **Flask-SQLAlchemy** – ORM for database models
- **Flask-Migrate** – For database migrations
- **Flask-RESTful** – For building REST APIs
- **Flask-Bcrypt** – Password hashing
- **Postgresql** – Deployment database
- **SQLite** – Lightweight development database 
- **JWT (JSON Web Tokens)** – For authentication
- **python-dotenv** – For managing environment variables

---

## 🗂️ Project Structure

```
health-system-backend/
├── app.py               # Main application logic
├── models.py            # Database models
├── migrations/          # Auto-generated DB migrations
├── requirements.txt     # Python dependencies
├── README.md
```

---

## 🚀 GETting Started

### 1. Clone the Repository

```bash
git clone git@github.com:Bett-Patrick/health-system-backend.git
cd health-system-backend
```

### 2. Create Virtual Environment and Activate It

```bash
pipenv install
pipenv shell
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Database Migrations

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 5. Start the Server

```bash
python3 app.py or 
flask run or
gunicorn app:app
```

---

## 📖 API Endpoints

### Authentication
This API uses **JWT (JSON Web Tokens)** for authentication. To access protected routes, you must include a valid token in the `Authorization` header of your requests.

#### How to Obtain a Token
1. Use the `/login` endpoint to log in with valid credentials.
2. The response will include a `token` that you can use for subsequent requests.

#### Using the Token
Include the token in the `Authorization` header of your requests:
```
Authorization: Bearer <JWT_TOKEN>
```

---

### Endpoints

| Method | Endpoint              | Description                             |
|--------|-----------------------|-----------------------------------------|
| POST   | `/register-admin`     | Register the first user as admin        |
| POST   | `/login`              | Login (Admin/Doctor) and GET a token    |
| POST   | `/register-doctor`    | Admin registers a doctor (protected)    |
| POST   | `/clients`            | Doctor registers a new client           |
| POST   | `/programs`           | Create a new health program             |
| POST   | `/enroll-client`        | Enroll a client in a program            |
| GET    | `/clients`            | Search clients                          |
| GET    | `/clients/<id>`       | View full client profile + enrollments  |

---

### Example Requests

## Base URL

```
https://health-system-backend-yqbu.onrender.com/
```

---

### 1. Register Admin

- **URL**: `/register-admin`
- **Method**: `POST`
- **Body**:
  ```json
  {
    "username": "admin",
    "email": "admin@example.com",
    "password": "adminpassword"
  }
  ```
- **Success Response**:
  ```json
  {
    "message": "Admin registered successfully"
  }
  ```
- **Error Response**:
  ```json
  {
    "error": "Admin already exists"
  }
  ```

---

### 2. Login (Admin)

- **URL**: `/login`
- **Method**: `POST`
- **Body**:
  ```json
  {
    "email": "admin@example.com",
    "password": "adminpassword"
  }
  ```
- **Success Response**:
  ```json
  {
    "message": "Login successful",
    "token": "<JWT_TOKEN>",
    "user": {
      "id": 1,
      "username": "admin",
      "email": "admin@example.com",
      "role": "ADMIN"
    }
  }
  ```
- **Error Response**:
  ```json
  {
    "error": "Invalid credentials"
  }
  ```

---


### 3. Register Doctor (Admin Only)

- **URL**: `/register-doctor`
- **Method**: `POST`
- **Headers**:
  - `Authorization: Bearer <JWT_TOKEN>`
- **Body**:
  ```json
  {
    "username": "doctor2",
    "email": "doctor2@example.com",
    "password": "password123"
  }
  ```
- **Success Response**:
  ```json
  {
    "message": "Doctor registered successfully",
    "doctor": {
      "id": 2,
      "username": "doctor2",
      "email": "doctor2@example.com",
      "role": "DOCTOR"
    }
  }
  ```
- **Error Responses**:
  ```json
  {
    "error": "Only admin can register doctors"
  }
  ```
  ```json
  {
    "error": "Email already exists"
  }
  ```
---

### 4. Login (Doctor)

- **URL**: `/login`
- **Method**: `POST`
- **Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "password123"
  }
  ```
- **Success Response**:
  ```json
  {
    "message": "Login successful",
    "token": "<JWT_TOKEN>",
    "user": {
      "id": 1,
      "username": "doctor1",
      "email": "user@example.com",
      "role": "DOCTOR"
    }
  }
  ```
- **Error Response**:
  ```json
  {
    "error": "Invalid credentials"
  }
  ```
---

### 5. Create Health Program (Doctor Only)

- **URL**: `/programs`
- **Method**: `POST`
- **Headers**:
  - `Authorization: Bearer <JWT_TOKEN>`
- **Body**:
  ```json
  {
    "name": "Maternal Health"
  }
  ```
- **Success Response**:
  ```json
  {
    "message": "Health program created successfully",
    "program": {
      "id": 1,
      "name": "Maternal Health",
      "created_by": 2
    }
  }
  ```
- **Error Response**:
  ```json
  {
    "error": "Program name already exists"
  }
  ```

---

### 6. Get All Health Programs (Doctor Only)

- **URL**: `/programs`
- **Method**: `GET`
- **Headers**:
  - `Authorization: Bearer <JWT_TOKEN>`
- **Success Response**:
  ```json
  [
    {
      "id": 1,
      "name": "Maternal Health",
      "created_by": 2
    }
  ]
  ```
- **Error Response**:
  ```json
  {
    "error": "No health programs availlable yet"
  }
  ```

---

### 7. Create Client (Doctor Only)

- **URL**: `/clients`
- **Method**: `POST`
- **Headers**:
  - `Authorization: Bearer <JWT_TOKEN>`
- **Body**:
  ```json
  {
    "full_name": "Jane Doe",
    "gender": "Female",
    "phone": "0712345678",
    "address": "123 Nairobi St.",
    "date_of_birth": "1990-05-15"
  }
  ```
- **Success Response**:
  ```json
  {
    "message": "Patient created successfully",
    "client": {
      "id": 1,
      "full_name": "Jane Doe",
      "gender": "Female",
      "phone": "0712345678",
      "address": "123 Nairobi St.",
      "date_of_birth": "1990-05-15"
    }
  }
  ```

---

### 8. Get All Clients (Doctor Only)

- **URL**: `/clients`
- **Method**: `GET`
- **Headers**:
  - `Authorization: Bearer <JWT_TOKEN>`
- **Success Response**:
  ```json
  [
    {
      "id": 1,
      "full_name": "Jane Doe",
      "gender": "Female",
      "phone": "0712345678",
      "address": "123 Nairobi St.",
      "date_of_birth": "1990-05-15",
      "enrollments": [
        {
          "program_id": 1,
          "client_id": 1,
          "date_enrolled": "2024-01-01"
        }
      ]
    }
  ]
  ```

---

### 9. Get Client by ID

- **URL**: `/clients/<id>`
- **Method**: `GET`
- **Success Response**:
  ```json
  {
    "id": 1,
    "full_name": "Jane Doe",
    "gender": "Female",
    "phone": "0712345678",
    "address": "123 Nairobi St.",
    "date_of_birth": "1990-05-15",
    "enrollments": [...]
  }
  ```
- **Error Response**:
  ```json
  {
    "error": "Client with ID 5 not registered"
  }
  ```

---

### 10. Enroll Client in Programs (Doctor Only)

- **URL**: `/enroll-client`
- **Method**: `POST`
- **Headers**:
  - `Authorization: Bearer <JWT_TOKEN>`
- **Body**:
  ```json
  {
    "client_id": 1,
    "program_ids": [1, 2]
  }
  ```
- **Success Response**:
  ```json
  {
    "message": "Client enrolled in programs successfully"
  }
  ```
- **Error Response**:
  ```json
  {
    "error": "Program with ID 2 not found"
  }
  ```

---

### 11. Home Route

- **URL**: `/`
- **Method**: `GET`
- **Response**:
  ```
  Welcome to Health Information System(HIS) API
  ```

---

## 🔒 Security Considerations

- Passwords are hashed using bcrypt.
- JWT tokens are used for authentication.
- Only admins can register doctors.
- Tokens expire after 1 hour for security.

---

## 👨‍💻 Author

- **Bett Patrick** – [GitHub Repository](https://github.com/Bett-Patrick/health-system-backend)

