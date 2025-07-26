# TechNews API System

Welcome to the TechNews API System! This project is a scalable and modular backend system built with Django and Django REST Framework (DRF), designed to serve news articles with powerful filtering, tagging, and authentication mechanisms. The system is structured to support future feature expansion and real-time data ingestion.

---

## Features

This repository reflects the completion of 3 milestone challenges:

### Challenge 1 – REST API Implementation
- Designed and implemented Django models for News, Tag, and Source
- Built a DRF-powered API to:
  - List news items with title, tags, source
  - Filter news by tags
  - Filter news by included phrases
  - Filter news by excluded phrases
  - Combine 4–5 simultaneous filters
- Added unit tests for models, views, serializers, filters

### Challenge 2 – News Scraping System
- Implemented a Scrapy spider to collect news from Zoomit
- Returned structured news items compatible with Challenge 1 format

### Challenge 3 – Background Tasks & Dockerization
- Added Celery for scheduled scraping
- Used Celery Beat to run scraper every 10 minutes
- Configured Redis message broker
- Integrated Flower for task monitoring
- Dockerized all services via `Dockerfile` and `docker-compose.yml`

---
##  Documentation

Explore detailed documentation in the following markdown files:

1. [High-Level Documentation](docs/1.High_Level_Documentation.md)  
   Overview of system architecture, challenge goals, and design decisions.

2. [Setup & Development Guide](docs/2.Setup_and_Development.md)  
   Step-by-step installation, environment setup, Docker, Celery integration.

3. [Code Structure Reference](docs/3.Code_Structure.md)  
   Module layout, reusable apps, endpoint breakdown, and internal logic.

---
