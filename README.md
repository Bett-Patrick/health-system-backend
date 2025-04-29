# 🏥 Health Information System – CEMA Internship Task

## Deployed Link
  #### [click here to visit health system backend link](#health-system-backend-production.up.railway.app)

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

#### 1. Register Admin
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

#### 2. Login (Admin & Doctors Only)
- **URL**: `/login`
- **Method**: `POST`
- **Body**:
  ```json
  {
    "email": "tadams@example.com",
    "password": "password123"
  }
  ```
- **Response**:
  ```json
  {
    "message": "Login successful",
    "token": "<JWT_TOKEN>",
    "user": {
      "id": 1,
      "username": "whiteadam",
      "email": "tadams@example.com",
      "role": "ADMIN"
    }
  }
  ```

#### 3. Register Doctor (Admin Only)
- **URL**: `/register-doctor`
- **Method**: `POST`
- **Headers**:
  ```
  Authorization: Bearer <JWT_TOKEN>
  ```
- **Body**:
  ```json
  {
    "username": "doctor1",
    "email": "doctor1@example.com",
    "password": "doctorpassword"
  }
  ```

#### 4. Doctor Login (Doctors Only)
- **URL**: `/login`
- **Method**: `POST`
- **Headers**:
  ```
  Authorization: Bearer <JWT_TOKEN>
  ```
- **Body**:
  ```json
  {
    "email": "doctor1@example.com",
    "password": "doctorpassword"
  }
  ```

#### 5. Create Health Programs (Doctors Only)
- **URL**: `/programs`
- **Method**: `POST`
- **Headers**:
  ```
  Authorization: Bearer <JWT_TOKEN>
  ```
- **Body**:
  ```json
  {
    "name": "Diabetes Management"
  }
  ```

#### 6. Client Enrollment into Health Programs (Doctors Only)
- **URL**: `/enroll-client`
- **Method**: `POST`
- **Headers**:
  ```
  Authorization: Bearer <JWT_TOKEN>
  ```
- **Body**:
  ```json
  {
    "client_id": 1,
    "program_ids": [1, 2]
  }
  ```


#### 7. List All Clients (Doctors Only)
- **URL**: `/clients`
- **Method**: `GET`
- **Headers**:
  ```
  Authorization: Bearer <JWT_TOKEN>
  ```

#### 8. GET Client Details by ID/Client profile(Doctors Only)
- **URL**: `/clients/<id>`
- **Method**: `GET`
- **Headers**:
  ```
  Authorization: Bearer <JWT_TOKEN>
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

