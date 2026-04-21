# Technische Vereisten

## 1. Back-end Vereisten

### Framework & Taal

| Vereiste         | Keuze                | Alternatief        |
| ---------------- | -------------------- | ------------------ |
| Programmeertaal  | Python 3.10+         | Python 3.9+        |
| Web framework    | Flask 2.3+           | Django (zwaarder)  |
| ASGI/WSGI server | Gunicorn (productie) | Waitress (Windows) |

### Flask Extensions (verplicht)

```txt
Flask==2.3.3
Flask-Login==0.6.2        # Sessiebeheer
Flask-SQLAlchemy==3.1.1   # ORM (optioneel maar aanbevolen)
Flask-WTF==1.2.1          # Formulieren + CSRF
WTForms==3.0.1            # Form validatie
Werkzeug==2.3.7           # Wachtwoord hashing
```

### Optionele Extensions (aanbevolen)

```txt
Flask-Migrate==4.0.5      # Database migraties (Alembic)
Flask-Caching==2.1.0      # Caching voor dashboard queries
python-dotenv==1.0.0      # Environment variabelen
```

### API Ontwerp (REST-style)

| Endpoint             | Methode          | Functie                       |
| -------------------- | ---------------- | ----------------------------- |
| /register            | GET, POST        | Registratie                   |
| /login               | GET, POST        | Inloggen                      |
| /logout              | GET              | Uitloggen                     |
| /dashboard           | GET              | Hoofdpagina                   |
| /transactions        | GET, POST        | Lijst + toevoegen             |
| /transactions/\<id\> | GET, PUT, DELETE | Detail, bewerk, verwijder     |
| /categories          | GET, POST        | Categorieën beheren           |
| /categories/\<id\>   | PUT, DELETE      | Bewerk/verwijder categorie    |
| /export/csv          | GET              | Exporteer CSV                 |
| /profile             | GET, PUT         | Profiel + wachtwoord wijzigen |

---

## 2. Front-end Vereisten

### Basistechnologieën

| Vereiste     | Versie | Waarom                   |
| ------------ | ------ | ------------------------ |
| HTML5        | -      | Semantische markup       |
| CSS3         | -      | Styling + responsive     |
| JavaScript   | ES6+   | Interactie + API calls   |
| Bootstrap    | 5.3+   | Snelle responsive layout |
| Chart.js     | 4.4+   | Grafieken (lichtgewicht) |
| Font Awesome | 6.x    | Iconen (gratis)          |

### Template Structuur (Jinja2)

```text
templates/
├── base.html              # Navbar, footer, flash messages
├── auth/
│   ├── login.html
│   └── register.html
├── dashboard.html         # Hoofdpagina met grafieken
├── transactions/
│   ├── list.html          # Lijst met filters
│   ├── form.html          # Toevoegen/bewerken
│   └── _row.html          # Partial voor AJAX updates
├── categories/
│   └── manage.html
└── profile.html
```

### JavaScript Functionaliteiten

| Functie                      | Techniek                                 |
| ---------------------------- | ---------------------------------------- |
| Datumkiezer                  | HTML5 `<input type="date">` of Flatpickr |
| Bevestigingsdialoog          | `window.confirm()` of Bootstrap modal    |
| Filteren zonder page reload  | Fetch API + partial template update      |
| Grafieken laden              | Chart.js met data uit API endpoint       |
| Form validatie (client-side) | HTML5 `required` + custom JS             |

### Responsive Eisen

- Mobile first design (Bootstrap grid)
- Breakpoints: 576px, 768px, 992px, 1200px
- Navigatie: hamburger menu op mobiel (Bootstrap navbar toggler)
- Tabellen: horizontaal scrollbaar op mobiel (`overflow-x: auto`)

---

## 3. Database Vereisten

### Ontwikkelomgeving

| Item              | Specificatie                     |
| ----------------- | -------------------------------- |
| Database          | SQLite 3.35+                     |
| Bestandslocatie   | `instance/fintrack.db`           |
| Connection string | `sqlite:///instance/fintrack.db` |

### Productieomgeving

| Item               | Specificatie                                | Waarom                             |
| ------------------ | ------------------------------------------- | ---------------------------------- |
| Database           | PostgreSQL 14+                              | Betere concurrency, remote toegang |
| Connection string  | `postgresql://user:pass@localhost/fintrack` | Environment variable               |
| Connection pooling | 10-20 connections                           | Flask-SQLAlchemy pooling           |

### ORM Configuratie (SQLAlchemy)

```python
# models.py voorbeeld
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relaties
    categories = db.relationship('Category', backref='user', lazy=True, cascade='all, delete-orphan')
    transactions = db.relationship('Transaction', backref='user', lazy=True, cascade='all, delete-orphan')
```

### Migratie Tool

```bash
# Flask-Migrate commands
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

---

## 4. Ontwikkelomgeving (Local Setup)

### Vereiste Software

| Software                   | Versie | Doel            |
| -------------------------- | ------ | --------------- |
| Python                     | 3.10+  | Runtime         |
| pip                        | 23+    | Package manager |
| virtualenv/venv            | -      | Isolatie        |
| Git                        | 2.40+  | Version control |
| SQLite Browser (optioneel) | -      | Debuggen        |

### Virtuele Omgeving Setup

**Linux / Mac:**

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Environment Variabelen (.env bestand)

```env
FLASK_APP=run.py
FLASK_ENV=development
FLASK_DEBUG=1
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///instance/fintrack.db

# Voor productie:
# DATABASE_URL=postgresql://user:pass@localhost/fintrack
```

### Run Commands

```bash
# Ontwikkeling
flask run --host=0.0.0.0 --port=5000 --debug

# Productie (met Gunicorn)
gunicorn --bind 0.0.0.0:8000 wsgi:app
```

---

## 5. Security Vereisten

### Verplichte Maatregelen

| Categorie    | Maatregel                 | Implementatie                                    |
| ------------ | ------------------------- | ------------------------------------------------ |
| Wachtwoorden | Hashing met salt          | `generate_password_hash()` uit Werkzeug (PBKDF2) |
| Sessies      | Secure session cookie     | `SESSION_COOKIE_SECURE=True` (HTTPS)             |
| CSRF         | Tokens op alle POST forms | Flask-WTF automatisch                            |
| XSS          | Output escaping           | Jinja2 autoescape (standaard aan)                |
| SQL injectie | Parameterized queries     | SQLAlchemy of `?` placeholders                   |
| Headers      | Security headers          | Talisman extension (optioneel)                   |

### Flask Configuratie (Productie)

```python
class ProductionConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'pool_recycle': 3600,
    }
    DEBUG = False
    TESTING = False
```

### Rate Limiting (tegen brute force)

```python
# Flask-Limiter voor login endpoint
from flask_limiter import Limiter
limiter = Limiter(app, key_func=lambda: current_user.id)
limiter.limit("5 per minute")(login_endpoint)
```

---

## 6. Deployment Vereisten

### Hosting Opties (gratis tier)

| Provider           | Geschikt voor           | Beperkingen                               |
| ------------------ | ----------------------- | ----------------------------------------- |
| PythonAnywhere     | SQLite, kleine datasets | Geen PostgreSQL, background tasks beperkt |
| Render             | PostgreSQL gratis       | Slaapt na 15 min inactiviteit             |
| Railway            | Makkelijk               | 500 uur gratis per maand                  |
| Heroku             | Volledig                | Betaald na november 2022 (alternatief)    |
| VPS (DigitalOcean) | Volledige controle      | min. 6 euro/maand                         |

### Vereisten voor Productie

```txt
# requirements.txt voor productie
Flask==2.3.3
gunicorn==21.2.0          # WSGI server
psycopg2-binary==2.9.9    # PostgreSQL driver (indien gebruikt)
Flask-Migrate==4.0.5
python-dotenv==1.0.0
```

### Deployment Checklist

- `DEBUG=False` ingesteld
- `SECRET_KEY` is lange willekeurige string (geen default)
- Database indices gecreëerd
- Static files worden geserveerd via CDN of whitenoise
- Logging geconfigureerd (geen print statements)
- HTTPS geforceerd (via platform of Talisman)
- Environment variabelen veilig opgeslagen

---

## 7. Performance Vereisten

### Performance Targets

| Metriek            | Target                     | Hoe te bereiken                           |
| ------------------ | -------------------------- | ----------------------------------------- |
| Dashboard laadtijd | < 2 sec (1000 transacties) | Database indices, paginering              |
| Transactielijst    | < 500 ms                   | Limit 50 per page, lazy loading           |
| Grafiek queries    | < 300 ms                   | Geaggregeerde queries, geen N+1 problemen |
| Concurrent gebruik | 50 gebruikers tegelijk     | Connection pooling, caching               |

### Caching Strategie (optioneel)

```python
from flask_caching import Cache
cache = Cache(app, config={'CACHE_TYPE': 'SimpleCache'})

@cache.cached(timeout=300, key_prefix='dashboard_%s' % current_user.id)
def get_dashboard_data(user_id):
    # Zware database queries hier
    pass
```

---

## 8. Testing Vereisten

### Testing Framework

```txt
pytest==7.4.0
pytest-flask==1.2.0
factory-boy==3.2.1
```

### Test Structuur

```text
tests/
├── conftest.py          # Fixtures (app, client, db)
├── test_auth.py         # Registratie, login, logout
├── test_transactions.py # CRUD operaties
├── test_categories.py   # Categorie beheer
├── test_dashboard.py    # Grafieken, saldo
└── test_integration.py  # End-to-end scenario's
```

### Minimale Test Coverage

| Module             | Coverage target |
| ------------------ | --------------- |
| models.py          | 90%             |
| auth/routes        | 85%             |
| transaction/routes | 80%             |
| category/routes    | 80%             |
| dashboard/routes   | 75%             |

---

## 9. Version Control & Documentatie

### Git Workflow

```text
main (productie) <- staging <- feature/username-storyname
```

### Commit Conventie

```text
feat: voeg transactie bewerken toe
fix: reparer datumfilter op dashboard
docs: update README met installatie instructies
test: voeg unit tests toe voor categorie validatie
```

### Vereiste Documentatie

- `README.md` - Installatie, configuratie, run instructies
- `CONTRIBUTING.md` - Hoe bijdragen (indien team)
- `API.md` - REST endpoints beschrijving
- `DEPLOYMENT.md` - Deployment stappenplan

---

## 10. Minimale Technische Stack (MVP Samenvatting)

| Laag          | Keuze                              |
| ------------- | ---------------------------------- |
| Backend       | Flask + Flask-Login + Flask-WTF    |
| Database      | SQLite (dev) -> PostgreSQL (prod)  |
| ORM           | SQLAlchemy (aanbevolen) of raw SQL |
| Frontend      | Bootstrap 5 + Chart.js + Jinja2    |
| Authenticatie | Werkzeug password hashing          |
| Deployment    | PythonAnywhere (gratis start)      |
| Testing       | Pytest                             |

---

## 11. Vereiste Configuratiebestanden

### requirements.txt (volledig)

```txt
Flask==2.3.3
Flask-Login==0.6.2
Flask-SQLAlchemy==3.1.1
Flask-WTF==1.2.1
Flask-Migrate==4.0.5
WTForms==3.0.1
Werkzeug==2.3.7
python-dotenv==1.0.0
email-validator==2.0.0
psycopg2-binary==2.9.9
gunicorn==21.2.0
pytest==7.4.0
pytest-flask==1.2.0
```

### docker-compose.yml (optioneel voor PostgreSQL)

```yaml
version: "3.8"

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/fintrack
    depends_on:
      - db

  db:
    image: postgres:14
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=fintrack
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

volumes:
  postgres_data:
```
