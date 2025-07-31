# 🎬 CineScope AI

**CineScope AI** is a full-stack RESTful API built with Django and PostgreSQL that provides structured movie data from the IMDb dataset. It also integrates with large language models (LLMs) like Google Gemini to generate intelligent summaries, thematic insights, and recommendations based on movie titles or descriptions.

---

## 🚀 Features

- 📁 Load and manage large-scale IMDb movie and person data
- 🔍 Search, filter, and paginate movies and actors
- 📊 Optimized PostgreSQL queries for high performance
- 🤖 AI Integration (LLM) to:
  - Generate movie summaries
  - Analyze genre and themes
  - Recommend similar movies
- 🔐 JWT Authentication (optional for protected endpoints)
- 🐳 Docker support for local development and deployment

---

## 🧠 Tech Stack

| Layer        | Tech                     |
|--------------|--------------------------|
| Backend      | Django, Django REST Framework |
| Database     | PostgreSQL               |
| AI Integration | Google Gemini |
| DevOps       | Docker, Docker Compose   |

---

## 📂 Dataset

This project uses the official IMDb public dataset:

- `title.basics.tsv.gz` – movie titles, genres
- `title.ratings.tsv.gz` – ratings, vote counts
- `name.basics.tsv.gz` – actors, directors

👉 [IMDb Datasets](https://datasets.imdbws.com/)

---

## 📦 API Endpoints (Sample)

| Method | Endpoint                    | Description                    |
|--------|-----------------------------|--------------------------------|
| GET    | `/api/movies/`              | List all movies                |
| GET    | `/api/movies/<id>/`         | Get movie details              |
| GET    | `/api/search/?query=Inception` | Search by title or genre     |
| GET    | `/api/actors/`              | List actors                    |
| POST   | `/api/ai/summary/`          | Get AI summary for a movie     |

---

## ⚙️ Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/ankote/cinescope-ai.git
cd cinescope-ai
```

### 2. Start with Docker
```bash
docker-compose up --build
```
Make sure PostgreSQL is accessible and your .env variables are set properly.

### .ENV Template
```bash
# Django Configuration
DJANGO_SETTINGS_MODULE=CineBrain.settings  with your project name
DJANGO_SECRET_KEY=your_secret_key
DJANGO_DEBUG=True

# PostgreSQL Configuration
POSTGRES_DB=imdb_db
POSTGRES_USER=user
POSTGRES_PASSWORD=your_password
POSTGRES_HOST=db
POSTGRES_PORT=5432

DJANGO_SUPERUSER_USERNAME=username
DJANGO_SUPERUSER_EMAIL=admin@example.com
DJANGO_SUPERUSER_PASSWORD=password

# Adminer Configuration
ADMINER_DEFAULT_SERVER=db  # Default database server
ADMINER_DESIGN=price  # Optional: Change Adminer theme
ADMINER_PLUGINS=tables-filter  # Optional: Enable plugins
```
📬 Contact
Feel free to contribute or open issues!
Made with ❤️ by Ankote Ayoube.