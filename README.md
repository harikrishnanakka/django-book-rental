#  Django Book Rental System

A web application for managing student book rentals using **Django** and **Django REST Framework**.

Students can rent books for **1 month free**.  
After that, they pay a fee based on the book’s page count:  
 **Charge = (pages / 100) × number of months extended**

---

##  Features

- Admin can start a rental for students.
- Automatically fetches book details from **OpenLibrary API**.
- Students can extend rentals for additional months.
- Calculates total charges dynamically.
- Authenticated users can view available books.
- Admins can view all rentals.

---

## Project Setup

### 1. Clone the repository
```bash
git clone https://github.com/harikrishnanakka/django-book-rental.git
cd django-book-rental

## 2. Create & activate virtual environment

python -m venv venv
venv\Scripts\activate   # On Windows
# source venv/bin/activate  # On Mac/Linux



## 3.Install dependencies

pip install -r requirements.txt

## 4. Run migrations

python manage.py makemigrations
python manage.py migrate

## 5.Create superuser
python manage.py createsuperuser

## 6.Run server

python manage.py runserver

| Endpoint                    | Method   | Description                         |
| --------------------------- | -------- | ----------------------------------- |
| `/api/start-rental/`        | **POST** | Admin starts a rental for a student |
| `/api/rentals/`             | **GET**  | List all rentals (Admin only)       |
| `/api/books/`               | **GET**  | List all available books            |
| `/api/rentals/<id>/extend/` | **POST** | Extend an existing rental           |

Authentication

Some endpoints are protected with Basic Authentication.

In Postman:

Go to Authorization tab.

Select Basic Auth.

Enter your Django superuser username and password.

1.Start a rental (Admin only)

POST: /api/start-rental/

{
    "title": "The Hobbit",
    "user_id": 1
}

2.Extend a rental (Authenticated user)

POST: /api/rentals/1/extend/

{
    "months": 2
}

Technologies Used

Python 3.10+

Django 4.2+

Django REST Framework

SQLite3

Requests library (for OpenLibrary API)



