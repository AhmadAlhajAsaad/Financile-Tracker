# ADR-001: Projectopzet en repositorystructuur

| Metadata   | Details           |
| ---------- | ----------------- |
| **Status** | Geaccepteerd      |
| **Datum**  | 2025-12-04        |
| **Auteur** | Ahmad Alhaj Asaad |

---

## Context

FinTrack is een persoonlijke financiële tracker waarmee gebruikers inkomsten en uitgaven kunnen bijhouden, categoriseren en visualiseren. Het project wordt door één ontwikkelaar gebouwd als leerproject en moet eenvoudig te starten, begrijpen en uitbreiden zijn.

Er moesten vroegtijdig beslissingen worden genomen over:

- De mappenstructuur van de codebase
- De keuze van programmeertaal, framework en database
- Hoe de frontend en backend samenwerken
- Welke tools gebruikt worden voor versiebeheer en documentatie

Zonder een bewuste structuurkeuze groeit een Flask-project snel uit tot een onoverzichtelijke verzameling losse bestanden. De ADR legt vast welke keuzes zijn gemaakt en waarom.

---

## Besluit

### Projectstructuur

Hierbij is gekozen voor een monorepo met een duidelijke scheiding tussen de verschillende lagen van het systeem. In de praktijk betekent dit dat elke map een eigen verantwoordelijkheid heeft. Een ontwikkelaar die aan de frontend werkt, hoeft niet door de backend-code te navigeren en andersom.

```
Financile-Tracker/
├── run.py                          # Startpunt
├── config.py                       # Dev/prod configuratie
├── requirements.txt
├── .env                            # Omgevingsvariabelen (niet in git)
├── .gitignore
├── app/
│   ├── __init__.py                 # App factory + blueprints
│   ├── models.py                   # User, Category, Transaction
│   ├── auth/routes.py              # Registreren, inloggen, uitloggen
│   ├── dashboard/routes.py         # Saldo, grafieken, recente transacties
│   ├── transactions/routes.py      # CRUD + CSV export + filteren
│   ├── categories/routes.py        # Beheer + blokkade bij transacties
│   └── profile/routes.py           # Profiel bekijken, wachtwoord, verwijderen
├── templates/
│   ├── base.html                   # Navbar, flash messages, Bootstrap 5 + Chart.js
│   ├── dashboard.html              # Saldo-kaarten + pie/bar grafieken
│   ├── profile.html
│   ├── auth/ (login, register)
│   ├── transactions/ (list + form)
│   └── categories/ (manage)
├── static/
│   ├── css/style.css               # Eigen stijlen bovenop Bootstrap
│   └── js/main.js                  # Verwijder-bevestiging + auto-close alerts
├── instance/                       # fintrack.db komt hier (niet in git)
├── docs/
│   ├── ADRs/                       # Architectuurbeslissingen
│   ├── Functionaliteiten.md        # Functionele & niet-functionele eisen
│   └── TechnischeR.md              # Technische vereisten
└── tests/                          # Pytest unit- en integratietests
```

### Technologiestack

| Laag                    | Technologie              | Waarom deze keuze                                                                       |
| ----------------------- | ------------------------ | --------------------------------------------------------------------------------------- |
| **Backend**             | Flask 2.3+ (Python)      | Lichtgewicht, minimale boilerplate, grote extensie-ecosysteem, goed gedocumenteerd      |
| **ORM**                 | Flask-SQLAlchemy 3.1+    | Abstractie over SQL, veilig tegen injectie, eenvoudige migraties via Flask-Migrate      |
| **Authenticatie**       | Flask-Login + Werkzeug   | Bewezen sessie­beheer, veilige PBKDF2-wachtwoord­hashing zonder externe afhankelijkheid |
| **Formulieren / CSRF**  | Flask-WTF + WTForms      | Automatische CSRF-tokens, server-side validatie, minder handmatig werk                  |
| **Frontend**            | HTML5 + Bootstrap 5.3    | Geen build-stap nodig, responsive grid out-of-the-box, snelle prototyping               |
| **Grafieken**           | Chart.js 4.4             | Lichtgewicht, interactieve tooltips, eenvoudige JSON-koppeling                          |
| **Database (dev)**      | SQLite 3.35+             | Geen serverinstallatie nodig, bestand in `instance/`, ideaal voor lokale ontwikkeling   |
| **Database (prod)**     | PostgreSQL 14+           | Betere concurrency, geschikt voor meerdere gelijktijdige gebruikers                     |
| **Migraties**           | Flask-Migrate (Alembic)  | Versiebeheer voor databaseschema, veilig upgraden zonder dataverlies                    |
| **Lokale ontwikkeling** | Python venv              | Geïsoleerde Python-omgeving, geen conflicten met systeempakketten                       |
| **Deployment**          | PythonAnywhere / Render  | Gratis tier beschikbaar, eenvoudig voor eerste livegang                                 |
| **Documentatie**        | Markdown + ADR-structuur | Versiebeheer naast de code, doorzoekbaar, geen externe tool nodig                       |
| **Versiebeheer**        | Git + GitHub             | Gedistribueerd versiebeheer, eenvoudig samenwerken en terugdraaien                      |
| **Testing**             | Pytest + pytest-flask    | Eenvoudige fixtures, goede Flask-integratie, breed gebruikt in Python-ecosysteem        |

### Frontend-backend integratie

Flask gebruikt Jinja2 als templating engine. Alle HTML-pagina's worden server-side gerenderd. JavaScript (via Fetch API) wordt uitsluitend gebruikt voor:

1. **Grafieken** — Chart.js haalt geaggregeerde data op via het `/dashboard/chart-data` JSON-endpoint.
2. **Bevestigingsdialogen** — `window.confirm()` voordat een verwijder-formulier wordt ingediend.
3. **Auto-close alerts** — Flash messages verdwijnen na 5 seconden automatisch.

Er is bewust géén frontend-framework (React, Vue) gekozen. Server-side rendering met Jinja2 vereist geen build-tooling en is eenvoudiger te debuggen voor een beginnersvriendelijk project.

---

## Motivatie

### Waarom Flask en niet Django

Django biedt meer out-of-the-box (admin panel, eigen ORM-migraties, ingebouwde authenticatie), maar brengt ook meer verplichte structuur en een steilere leercurve mee. Voor een project van deze omvang — één ontwikkelaar, beperkte scope — is Flask beter geschikt: minder magie, meer controle, sneller opgestart.

### Waarom deze mappenstructuur

De `app/` map organiseert backend-logica per domein (auth, dashboard, transactions, categories, profile) via Flask Blueprints. Dit maakt het mogelijk om elk domein onafhankelijk te testen en later te verplaatsen of uit te breiden zonder andere modules te raken.

De `templates/` map spiegelt dezelfde domeinindeling, zodat elke route direct een bijbehorende template heeft. De `static/` map is gescheiden zodat stijlen en scripts centraal beheerd worden. De `instance/` map bevat de SQLite-database en staat bewust buiten versiebeheer (via `.gitignore`).

### Waarom SQLite in ontwikkeling en PostgreSQL in productie

SQLite vereist geen aparte serverinstallatie, wat lokale ontwikkeling sterk vereenvoudigt. De overstap naar PostgreSQL in productie is mogelijk via één omgevingsvariabele (`DATABASE_URL`), dankzij de abstractie van SQLAlchemy. Dit staat beschreven in `NF4` van de functionele eisen.

### Waarom geen Rust voor de backend

Rust biedt hoge prestaties en geheugenveiligheid, maar heeft een aanzienlijk steilere leercurve dan Python/Flask. De prestatiedoelen van dit project (< 2 seconden laadtijd bij < 1000 transacties, zie `F53`) zijn ruimschoots haalbaar met Flask. Rust is overwogen maar afgewezen vanwege de mismatch tussen complexiteit en projectomvang.

---

## Gevolgen

### Positieve uitkomsten

- Duidelijke scheiding van verantwoordelijkheden per domein
- Gemakkelijk te navigeren codebase voor nieuwe bijdragers
- Eenvoudige integratie van frontend en backend zonder build-tooling
- Lokale ontwikkeling zonder externe services (SQLite)
- Migreerbaar naar PostgreSQL via één omgevingsvariabele
- Geschikt voor kleine tot middelgrote projecten met ruimte om te groeien

### Beperkingen en risico's

- SQLite ondersteunt geen gelijktijdige schrijfoperaties; bij meer dan ~10 gelijktijdige gebruikers is migratie naar PostgreSQL vereist
- Server-side rendering zonder JavaScript-framework betekent volledige paginalading bij elke actie (geen SPA-gedrag)
- Flask heeft geen ingebouwd admin-panel; beheer gaat via CLI of een toekomstige adminpagina (`NF3`)

### Toekomstige overwegingen

- Bij schaalbaarheid: overweeg Gunicorn + Nginx als productie-webserver
- Bij grotere teams: overweeg een API-first architectuur (Flask REST + los frontend-framework)
- Bij complexere business-logica: overweeg domeinservices los van de route-handlers
