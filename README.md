# PlantCare App (Backend)

This is the backend for the PlantCare web application. It is built with Django and Django REST Framework, featuring user authentication via JWT, full CRUD operations for managing plants, and a smart recommendation system.

## Features

- User authentication using JWT
- Full CRUD functionality for managing plant data
- Smart care recommendations for each user
- PostgreSQL database integration
- Image upload support for plant photos
- RESTful API ready for integration with React frontend

## Tech Stack

- Python 3.11
- Django 5
- Django REST Framework
- Simple JWT
- PostgreSQL
- Pillow (for image handling)
- django-cors-headers

## Entity Relationship Diagram (ERD)

### User Table

| Field      | Type      | Description              |
|------------|-----------|--------------------------|
| id         | UUID      | Primary Key              |
| username   | String    | Unique username          |
| email      | String    | User email               |
| password   | String    | Hashed password          |
| date_joined| DateTime  | Account creation time    |

### Plant Table

| Field           | Type      | Description                          |
|-----------------|-----------|--------------------------------------|
| id              | UUID      | Primary Key                          |
| user_id         | FK (User) | Foreign key to User table            |
| name            | String    | Name of the plant                    |
| species         | String    | Plant species                        |
| image           | Image     | Uploaded photo of the plant          |
| date_planted    | Date      | Date when the plant was planted      |
| last_watered    | Date      | Last time the plant was watered      |
| next_watering   | Date      | Recommended next watering date       |
| notes           | Text      | Optional notes about the plant       |

### Recommendation Table (Optional / Future)

| Field           | Type      | Description                            |
|-----------------|-----------|----------------------------------------|
| id              | UUID      | Primary Key                            |
| user_id         | FK (User) | Foreign key to User table              |
| plant_id        | FK (Plant)| Foreign key to Plant table             |
| message         | Text      | Recommendation content                 |
| created_at      | DateTime  | Time the recommendation was generated  |

**Relationships:**

- One `User` has many `Plants`
- One `Plant` may have many `Recommendations`
- Each `Recommendation` belongs to a specific `User` and `Plant`

## API Endpoints

| Method | Endpoint                | Description                      |
|--------|-------------------------|----------------------------------|
| POST   | /api/token/             | Obtain JWT access & refresh tokens |
| POST   | /api/token/refresh/     | Refresh JWT access token        |
| POST   | /signup/                | Register a new user             |
| GET    | /plants/                | Get all plants (user-specific)   |
| POST   | /plants/                | Create a new plant entry        |
| PUT    | /plants/<id>/           | Update an existing plant        |
| DELETE | /plants/<id>/           | Delete a plant                  |
| GET    | /recommendations/       | Get smart plant recommendations  |

## Recommendation System

The app provides personalized plant care tips. Future updates will include image-based disease detection using AI to further enhance plant health analysis.

## Future Plans

- AI-based image disease detection
- Reminder system for watering and care
- Multi-language support
- Mobile app (PWA)

## Starting development server at http://127.0.0.1:8000/

## Author

Developed by Atha Alghamdi.
