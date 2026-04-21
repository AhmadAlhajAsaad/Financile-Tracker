# FinTrack — Persoonlijke Financiële Tracker

FinTrack is een webapplicatie waarmee je inkomsten en uitgaven bijhoudt, categoriseert en visualiseert. Gebouwd met Flask, SQLite en Bootstrap 5.

---

## Functionaliteiten

- Gebruikersregistratie en inloggen (met veilige wachtwoordhashing)
- Transacties toevoegen, bewerken en verwijderen
- Categorieën beheren per gebruiker
- Dashboard met totaalsaldo, maandoverzicht en interactieve grafieken (Chart.js)
- Filteren en zoeken in transacties (datum, categorie, type, trefwoord)
- Exporteren naar CSV
- Responsive design (Bootstrap 5, werkt op mobiel en desktop)

---

## Vereisten

- Python 3.10+
- pip

---

## Installatie

### 1. Repository klonen

```bash
git clone https://github.com/AhmadAlhajAsaad/Financile-Tracker.git
cd Financile-Tracker
```

### 2. Virtuele omgeving aanmaken en activeren

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux / Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Afhankelijkheden installeren

```bash
pip install -r requirements.txt
```

### 4. Omgevingsvariabelen instellen

Kopieer het `.env`-bestand en pas de waarden aan:

```bash
cp .env.example .env
```

Of bewerk `.env` direct:

```env
FLASK_APP=run.py
FLASK_ENV=development
FLASK_DEBUG=1
SECRET_KEY=verander-dit-naar-een-lange-willekeurige-string
DATABASE_URL=sqlite:///fintrack.db
```

> **Let op:** Gebruik nooit de standaard `SECRET_KEY` in productie.

### 5. Database initialiseren

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 6. Applicatie starten

```bash
flask run
```

Open [http://localhost:5000](http://localhost:5000) in je browser.

---

## Projectstructuur

```
Financile-Tracker/
├── run.py                    # Startpunt
├── config.py                 # Dev/prod configuratie
├── requirements.txt
├── .env                      # Omgevingsvariabelen (niet in git)
├── app/
│   ├── __init__.py           # App factory + blueprints
│   ├── models.py             # User, Category, Transaction
│   ├── auth/                 # Registreren, inloggen, uitloggen
│   ├── dashboard/            # Saldo, grafieken, recente transacties
│   ├── transactions/         # CRUD, filteren, CSV-export
│   ├── categories/           # Categoriebeheer
│   └── profile/              # Profiel, wachtwoord wijzigen
├── templates/                # Jinja2 HTML-templates
├── static/                   # CSS en JavaScript
├── instance/                 # SQLite-database (niet in git)
├── docs/                     # Documentatie en ADRs
└── tests/                    # Pytest unit- en integratietests
```

---

## Technologiestack

| Laag            | Technologie                  |
|-----------------|------------------------------|
| Backend         | Flask 2.3+ (Python 3.10+)    |
| Database (dev)  | SQLite                       |
| Database (prod) | PostgreSQL 14+               |
| ORM             | Flask-SQLAlchemy + Alembic   |
| Authenticatie   | Flask-Login + Werkzeug       |
| CSRF-beveiliging| Flask-WTF                    |
| Frontend        | Bootstrap 5.3 + Chart.js 4.4 |
| Testing         | Pytest + pytest-flask        |

---

## Tests uitvoeren

```bash
pytest
```

---

## Deployment (productie)

Zet de volgende omgevingsvariabelen:

```env
FLASK_ENV=production
SECRET_KEY=<lange-willekeurige-string>
DATABASE_URL=postgresql://user:pass@localhost/fintrack
```

Start met Gunicorn:

```bash
gunicorn --bind 0.0.0.0:8000 wsgi:app
```

Zie [docs/TechnischeR.md](docs/TechnischeR.md) voor uitgebreide deployment-instructies.

---

## Documentatie

| Document | Beschrijving |
|----------|--------------|
| [docs/Functionaliteiten.md](docs/Requirements/Functionaliteiten.md) | Functionele & niet-functionele eisen (MoSCoW) |
| [docs/TechnischeR.md](docs/TechnischeR.md) | Technische vereisten en configuratie |
| [docs/ADRs/](docs/ADRs/) | Architectuurbeslissingen (ADRs) |

---

## Licentie

Dit project is bedoeld als leerproject en heeft geen commerciële licentie.
