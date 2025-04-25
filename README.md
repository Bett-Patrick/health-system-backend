# 🏥 Health Information System – CEMA Internship Task

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
- **SQLite** – Lightweight development database

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

## 🚀 Getting Started

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
flask run
```

---

## 📖 API Endpoints

| Method | Endpoint              | Description                             |
|------------|-----------------------|-----------------------------------------|
| POST   | `/register-admin`     | Register the first user as admin        |
| POST   | `/login`              | Login (Admin/Doctor)                    |
| POST   | `/register-doctor`    | Admin registers a doctor                |
| POST   | `/clients`            | Doctor registers a new client           |
| POST   | `/programs`           | Create a new health program             |
| POST   | `/enrollments`        | Enroll a client in a program            |
| GET    | `/clients`            | Search clients                          |
| GET    | `/clients/<id>`       | View full client profile + enrollments  |

---

## 🔒 Security Considerations

- Passwords are hashed using bcrypt
- Only doctors can access system features
- Admin manually approves doctor accounts

---

## 👨‍💻 Author

- **Bett Patrick** – [GitHub Repository](https://github.com/Bett-Patrick/health-system-backend)

