# Project Management Application (PMA)

A Django-based web application for managing projects and team collaboration, built as part of CS 3240.

## 🌟 Features

### User Authentication & Roles
- Google account integration for login
- Multiple user types:
  - Anonymous Users: Limited access to view project listings
  - Common Users: Can create/join projects and participate
  - PMA Administrators: Full moderation capabilities
  - Django Administrators: Access to Django admin interface

### Course Work Management
- Create and manage assignments with:
  - Title and description
  - Owner and member management
  - File uploads with metadata
  - Message board system
- File management with metadata tracking:
  - File title
  - Timestamp
  - Description
  - Keywords for searching

### Storage & Files
- Cloud storage integration with Amazon S3
- Supported file types:
  - PDF documents
  - Text files (.txt)
  - JPEG images
- File metadata and search capabilities

## 🔧 Technical Requirements

- Python 3.8+
- Django 5.0
- PostgreSQL database
- Additional dependencies in requirements.txt

## 🚀 Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd project-management-app
```

2. Set up virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install requirements:
```bash
pip install -r requirements.txt
```

4. Initialize database:
```bash
python manage.py migrate
```

5. Create superuser:
```bash
python manage.py createsuperuser
```

## 💻 Configuration Required

1. Google OAuth credentials for authentication
2. Amazon S3 bucket configuration:
   - Access key
   - Secret key
   - Bucket name
3. PostgreSQL database connection
4. Django secret key
5. Heroku deployment settings

## 🚀 Running the Application

Development server:
```bash
python manage.py runserver
```
Access at `http://localhost:8000`


## 🧪 Testing

- Run tests:
```bash
python manage.py test
```

## 📝 Documentation

All code follows PEP 257 guidelines for docstrings:

```python
def create_project(request):
    """
    Create a new project in the system.

    Args:
        request: HTTP request containing project data

    Returns:
        HttpResponse: Redirect to new project or error page
    """
    # Implementation
```

## ⚠️ Important Notes

- This is a class project for CS 3240
- Not intended for production use
- No sensitive information should be submitted
- System is not actively monitored

## 📄 License

This project is part of CS 3240 coursework and is subject to University of Virginia academic policies.

Authors: Isaac Coles,  Samuel Honigblum, Jessica Choi, and Huyen Huynh