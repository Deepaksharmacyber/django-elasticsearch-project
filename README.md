📘 Django + Elasticsearch Full-Text Search Project

A production-ready Django app integrated with Elasticsearch for real-time search, autocomplete suggestions, and fast text querying — all running inside Docker.

This project demonstrates modern, scalable search architecture using:

🔍 Elasticsearch (full-text + autocomplete)

🐍 Django (backend & API)

🐳 Docker (easy setup)

🎨 Bootstrap UI (modern search interface)

📁 SQLite (for simple development database)

🚀 Features
🔍 Elasticsearch Search

Full-text search across book titles

Prefix-based autocomplete (edge_ngram analyzer)

Real-time suggestions while typing

Fast, ranked results using ES scoring

Clean JSON-based ES queries

🖥 Frontend

Beautiful Bootstrap 5 UI

Live suggestions dropdown

Responsive, modern layout

Search icon, animations, and shadow effects

🐳 Docker Support

Elasticsearch container

Django app container

Automatic migrations

Easy environment configuration via .env

🗄 Django Features

Models, views, templates

Signals for auto-indexing

Admin panel

Clean separation of search logic

📦 Project Architecture
djangoes/
│
├── docker-compose.yml
├── web/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── .env
│   ├── manage.py
│   ├── djangoes/
│   │   ├── settings.py
│   │   ├── urls.py
│   ├── books/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── signals.py
│   │   ├── urls.py
│   │   ├── templates/books/
│   │   │   ├── index.html
│   │   │   ├── results.html
│   │   │   └── base.html
│   │   ├── management/commands/
│   │   │   ├── create_es_index.py
│   │   │   └── reindex_books.py
│
└── README.md

⚙️ Requirements

You need the following installed:

Docker

Docker Compose

Python 3.10+ (optional, only for editing/testing locally)

🐳 Running the Project (With Docker)
1️⃣ Clone the repository
git clone https://github.com/yourusername/django-elasticsearch-project.git
cd django-elasticsearch-project

2️⃣ Create a .env file

Inside the web/ folder:

SECRET_KEY="your-secret-here"
DEBUG=True
ALLOWED_HOSTS=*
ELASTICSEARCH_HOST=http://elasticsearch:9200

3️⃣ Build & run containers
docker compose up --build

4️⃣ Create the Elasticsearch index

Inside the running container:

docker compose exec web python manage.py create_es_index

5️⃣ Reindex books
docker compose exec web python manage.py reindex_books

6️⃣ Open the app

Visit:

http://localhost:8000

🔍 Search & Autocomplete

This project uses:

✔ Edge N-Gram Autocomplete
✔ multi_match prefix query
✔ Custom analyzers

This provides instant suggestions with smooth UX.

🛠 Development Commands
Create superuser:
docker compose exec web python manage.py createsuperuser

Check Elasticsearch health:
curl localhost:9200

Delete index:
docker compose exec web python manage.py shell -c "from elasticsearch import Elasticsearch; from django.conf import settings; Elasticsearch(settings.ELASTICSEARCH_HOST).indices.delete(index='books', ignore=[400,404])"

🧹 .gitignore Included

Important files excluded:

.env

db.sqlite3

__pycache__

staticfiles

virtual environments

📄 License

MIT License — free to use, modify, and learn from.

🙌 Contribution

Feel free to:

Open issues

Submit PRs

Improve UI / search logic
