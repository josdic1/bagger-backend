# BAGGER API

> **TL;DR for recruiters:**
> Production-structured Flask API with token authentication, layered architecture, and migration-driven schema control.
> Demonstrates real-world CRUD design, relational modeling, and separation of concerns.
> Built to reflect scalable backend patterns used in professional environments.

---

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Flask](https://img.shields.io/badge/Framework-Flask-black)
![SQLAlchemy](https://img.shields.io/badge/ORM-SQLAlchemy-red)
![Alembic](https://img.shields.io/badge/Migrations-Alembic-orange)
![Deploy](https://img.shields.io/badge/Deploy-Render%20%7C%20Railway%20Ready-brightgreen)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

---

# Overview

The Bagger API powers a structured developer knowledge system.

It provides:

* Token-based authentication
* Full CRUD for Cheats
* Platform + Topic taxonomy modeling
* Many-to-many relational joins
* Migration-driven schema evolution
* Seed and export utilities

Designed with clean separation between HTTP, domain, and persistence layers.

---

# Architecture

```
app.py                → Application entry point
config.py             → Environment-driven configuration

database.py           → Engine + session management

models/               → SQLAlchemy domain models
routes/               → HTTP controllers
schemas/              → Serialization + validation layer
utils/                → Auth utilities
migrations/           → Alembic migration history
```

## Architectural Principles

* Models isolated from transport layer
* Explicit schema serialization
* Centralized DB session management
* Auth boundary handled per-request
* Migration-first database discipline

---

# Core Domain Model

## User

* Authenticated entity
* Owns cheats

## Cheat

* title
* notes
* code
* Many-to-many → Platforms
* Many-to-many → Topics

## Platform

Technology classification layer.

## Topic

Concept grouping layer.

Join table: `user_cheat`

---

# Example Endpoints

## Get Cheats

```
GET /api/cheats
Authorization: Bearer <token>
```

### Response

```json
[
  {
    "id": 12,
    "title": "inEditMode Boolean",
    "notes": "Explicit boolean casting improves readability.",
    "code": "const inEditMode = Boolean(id);",
    "platformIds": [1],
    "topicIds": [3]
  }
]
```

---

## Create Platform

```
POST /api/platforms
Authorization: Bearer <token>
```

```json
{
  "name": "React"
}
```

---

# Authentication Flow

* Login endpoint issues token
* Token included via `Authorization: Bearer`
* Request validation handled server-side
* 401 responses returned consistently

Auth logic isolated in:

```
utils/auth.py
```

---

# Database & Migrations

Alembic-driven schema control.

Create migration:

```
flask db revision -m "add field"
flask db upgrade
```

Production mindset:

* No manual schema edits
* Version-controlled migrations
* Environment-based configuration

---

# Local Development

### Setup

```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Environment

```
FLASK_ENV=development
SECRET_KEY=change-me
DATABASE_URL=sqlite:///app.db
CORS_ORIGINS=http://localhost:5173
```

### Run

```
flask run --port 8080
```

---

# Production Readiness

Demonstrates:

* Token-based authentication
* Relational data modeling
* Migration-based schema evolution
* Clean HTTP/domain separation
* Environment-driven configuration
* CORS control

Structured intentionally to mirror professional Flask API architecture.

---

# License

MIT License

Copyright (c) 2026 Josh Dicker

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights

to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
