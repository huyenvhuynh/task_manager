
# task_manager
Clone of task managing project

# Task Management System (TMS)

A Django-based web application for managing academic assignments, discussions, and course collaborations, developed for CS 3240.

## 🌟 Features

### User Authentication
- Google OAuth integration for secure login
- User profile management with course enrollment
- Role-based access control

### Course Management
- Course enrollment system
- Course listings with detailed information
- Course-specific content organization

### Assignment Management
- Create and track assignments with:
  - Title and description
  - Due dates
  - Course association
  - File attachments
  - Metadata tracking
- File management with metadata:
  - File titles and descriptions
  - Upload timestamps
  - Keywords for enhanced searching

### Discussion System
- Course-specific discussion boards
- Create and participate in discussions
- Comment system for user interaction
- Filter discussions by enrolled courses

### File Management
- Amazon S3 integration for file storage
- Supported file formats:
  - PDF documents
  - Text files (.txt)
  - JPEG images
- File metadata and search functionality

## 🔧 Technical Requirements

- Python 3.12
- Django 5.1.1
- Additional packages:
  - django-storages
  - boto3
  - whitenoise
  - django-widget-tweaks

## 🚀 Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd project-a-04
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

## 💻 Configuration Required

1. Create a `.env` file with:
```
GOOGLE_OAUTH_CLIENT_ID=your_client_id
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_STORAGE_BUCKET_NAME=your_bucket_name
```

2. Configure `settings.py` with:
- Database settings
- AWS S3 configuration
- Google OAuth settings

## 🚀 Running the Application

Start the development server:
```bash
python manage.py runserver
```
Access at `http://localhost:8000`

## 📱 Features Overview

### User Features
- Google Sign-in/Sign-out
- Course enrollment
- Assignment creation and management
- File uploads with metadata
- Discussion participation

### Course Features
- Course listing
- Course-specific assignments
- Course-specific discussions
- File organization by course

### Assignment Features
- Create assignments with details
- Upload and manage files
- Track due dates
- Search by keywords

### Discussion Features
- Create course-specific discussions
- Add comments to discussions
- Filter discussions by course
- Track discussion timestamps

## 📂 Project Structure
```
project-a-04/
├── core/                 # Project settings
├── courses/              # Course management
├── assignments/          # Assignment functionality
├── discussions/          # Discussion system
├── users/                # User profiles
└── templates/            # HTML templates
```

## ⚠️ Important Notes

- Development project for CS 3240
- Not for production use
- Uses test/development credentials

## 👥 Team

- Isaac Coles
- Samuel Honigblum
- Jessica Choi
- Huyen Huynh

## 📄 License

This project is part of CS 3240 coursework at the University of Virginia.
