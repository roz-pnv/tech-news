# TechNews API System

Welcome to the TechNews API System! This project is a scalable and modular backend system built with Django and Django REST Framework (DRF), designed to serve news articles with powerful filtering, tagging, and authentication mechanisms. The system is structured to support future feature expansion and real-time data ingestion.

---

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Environment Setup](#environment-setup)
- [Settings Architecture](#settings-architecture)
- [Project Structure](#project-structure)

---

## Features

- **Modular project structure using reusable apps.**
- **REST API for managing and querying news articles.**
- **News filtering by tags, keyword inclusion/exclusion.**
- **Auto-managed slugs and media handling for news images.**
- **Token-based authentication using JWT (via Djoser).**
- **Admin enhancements for easier backend management.**
- **Unit tests for models, views, serializers, and signals.**
- **Environment-based configuration split into base, dev, and prod.**

### 1. Modular Architecture

- Structured the Django project into reusable and independent apps (`core`, `news`, `utils`).
- Ensures clean separation of concerns and promotes maintainability and scalability.

### 2. News App

- Contains models, views, serializers, urls, and signals related to the news content lifecycle.
- Implements Django signals for automatic behavior (e.g., slug creation, image management).

### 3. Timestamped Base Model

- All models inherit from `TimestampedModel` in `core.models.base`, providing `created_at` and `updated_at` fields.

### 4. News Model

- Fields include `title`, `body`, `slug`, `published_at`, and a many-to-many `tags` relationship.
- `published_at` is optional, enabling draft support.
- `slug` is generated uniquely using a signal and `utils.slug.generate_unique_slug()`.
- Index added on `title` for optimized search queries.

### 5. Tagging System

- The `Tag` model includes `name` and a unique `slug`.
- Tags are auto-created during news submission if not already present.
- Provides `get_absolute_url()` for future frontend integration.

### 6. News Images

- `NewsImage` model supports both `image_file` and `image_url` for flexibility.
- Uses `is_main` to mark the primary image and `position` to order them.
- Signal ensures one main image per news item.

### 7. Slug Utility

- Centralized slug logic in `utils.slug.generate_unique_slug()`.
- Prevents collisions using suffix incrementing strategy (e.g., `title`, `title-1`, `title-2`).

### 8. News API Endpoints

- DRF `GenericViewSet` for listing and creating news.
- `NewsListViewSet` supports:
  - Custom pagination via `utils.pagination.StandardResultsSetPagination`
  - Efficient tag fetching with `prefetch_related()`
  - Filters out unpublished items (`published_at <= now()`)
- `NewsCreateViewSet` supports nested creation of tags and images via DRF serializers.

### 9. Filtering System

- Advanced filters implemented in `news.views.filters`:
  - Filter by tag: `?tags=tag1,tag2`
  - Content inclusion: `?contains=keyword`
  - Content exclusion: `?not_contains=word1,word2`
- Filters are combinable for complex queries.

### 10. Testing

- Unit and integration tests written for models, views, and signals in `news.tests`.
- Includes:
  - Model tests (slug generation, timestamps, tag creation)
  - API tests for filtering, pagination, and nested serialization
  - Signal tests (slug assignment, image auto-positioning)

### 11. Admin Interface

- Custom admin setup for `News`, `Tag`, and `NewsImage`.
- Enhanced UX with `filter_horizontal` for tag assignment.
- Display configurations for easier content management.

### 12. Authentication with JWT

- User authentication powered by Djoser with JWT tokens.
- JWT login, logout, and token refresh supported.
- Public access allowed for read-only endpoints (list, detail), write operations require authentication.

### 13. Utility Modules

- `utils.pagination` provides API-wide pagination classes.
- `utils.slug` encapsulates reusable slug logic.

---

## Technologies Used

- **Backend:** Django, Django REST Framework
- **Authentication:** Djoser, JWT
- **Database:** SQLite (dev), PostgreSQL (prod ready)
- **Environment Management:** `django-environ`
- **Version Control:** Git, GitHub

---

## Getting Started

### Prerequisites

Before you begin, ensure you have the following installed on your system:

- Python 3.11+
- pip
- Git

### Installation

Clone the repository:

```bash
git clone https://github.com/roz-pnv/technews.git
cd technews
```

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate.bat 
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### Environment Setup

1. Copy the example `.env` file:

```bash
cp .env.example .env
```

2. Set your local variables inside `.env`

3. Apply migrations:

```bash
python manage.py migrate
```

4. Create a superuser:

```bash
python manage.py createsuperuser
```

5. Run the development server:

```bash
python manage.py runserver
```

Access the API at: [http://localhost:8000/api/](http://localhost:8000/api/)

---

## Settings Architecture

The project adopts a modularized settings architecture with separate configurations for `base`, `development`, and `production` environments to enhance maintainability and security.

### Structure

```
core/
├── settings/
│   ├── __init__.py           # Loads env-specific settings
│   ├── base.py               # Common settings shared across all environments
│   ├── dev.py                # Development-specific configuration
│   └── prod.py               # Production overrides
```


## Project Structure

```
technews/
├── core/                  # Base project settings and utilities
│   ├── settings/          # Split settings: base, dev, prod
│   └── models/            # Base abstract models
├── news/                  # App managing news logic
│   ├── models/            # News, Tag, NewsImage models
│   ├── serializers/       # DRF serializers for API
│   ├── views/             # ViewSets and filtering logic
│   ├── urls.py            # App-specific API routes
│   └── tests/             # Unit tests for news app
├── utils/                 # Reusable utilities (slugs, pagination)
└── manage.py
```

---

> Phase 2 focuses on automating data collection using tools like Scrapy to pull live news from sources. Stay tuned!

