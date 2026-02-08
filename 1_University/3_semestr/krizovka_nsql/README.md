# KrizeMapa - Crisis Management System

Webová aplikace pro hlášení a správu krizových situací.  
**Stack**: Flask + MongoDB + Redis + Docker

---

## Table of Contents

1. [Struktura projektu](#struktura-projektu)
2. [Setup - Local Development](#setup---local-development)
3. [Docker & Docker Compose](#docker--docker-compose)
4. [Workflow](#workflow)
5. [API](#api)
6. [Troubleshooting](#troubleshooting)

---

## Struktura projektu

```
krizovka_nsql/
├── app/                          # Flask aplikace
│   ├── __init__.py              # App factory
│   ├── config.py                # Konfigurace (Redis, MongoDB)
│   ├── models.py                # Data modely (CrisisEvent)
│   ├── db.py                    # Database manager (MongoDB + Redis)
│   ├── routes.py                # Všechny HTTP routes
│   ├── templates/               # HTML szablony
│   │   ├── base.html           # Základ
│   │   ├── dashboard.html      # Homepage/dashboard
│   │   ├── submit_event.html   # Formulář na hlášení krize
│   │   ├── view_events.html    # Seznam všech krizí
│   │   ├── event_detail.html   # Detail jedné krize
│   │   └── error.html          # Error stránka
│   └── static/
│       ├── css/style.css       # Styling
│       └── js/main.js          # Frontend JS
├── venv/                         # Python virtual environment
├── run.py                        # Spuštění aplikace
├── requirements.txt              # Python balíčky
├── Dockerfile                    # Docker image
├── docker-compose.yml            # Docker orchestration
├── .env                         # Environment proměnné (development)
└── .gitignore                   # Git ignore
```

---

## Setup - Local Development

### Krok 1: Virtual Environment (DŮLEŽITÉ!)

**Venv musí být POUZE v adresáři `krizovka_nsql`, nikoliv nikde jinde!**

```powershell
# Jdi do adresáře
cd c:\GitHub\University-stuff-and-small-scale-projects\1_University\3_semestr\krizovka_nsql

# Vytvoř venv
python -m venv venv

# Aktivuj venv - bez Activation.ps1 (behaves)
.\venv\Scripts\pip install -r requirements.txt
```

**Poznámka**: Pokud máš problém s execution policy na Windows, lze:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSignedhoc -Scope CurrentUser
```

### Krok 2: Instalace balíčků

```powershell
.\venv\Scripts\pip install -r requirements.txt
```

**Výstup by měl vypadat**:
```
Successfully installed Flask-3.1.2 redis-7.0.1 pymongo-4.15.3 python-dotenv-1.2.1 Werkzeug-3.1.3 ...
```

### Krok 3: Database Setup (bez Dockeru)

Pokud chceš testovat **bez Dockeru** na localhost:

#### MongoDB
```powershell
# Stažení a instalace https://www.mongodb.com/try/download/community
# Nebo přes chocolatey:
choco install mongodb-community

# Spusťtí
mongod
```

#### Redis
```powershell
# Stažení https://github.com/microsoftarchive/redis/releases
# Nebo chocolatey:
choco install redis

# Spusť
redis-server
```

Poté uprav `.env`:
```env
REDIS_URL=redis://localhost:6379/0
MONGO_URI=mongodb://localhost:27017/krizove_udalosti
```

### Krok 4: Spusť aplikaci

```powershell
cd c:\GitHub\University-stuff-and-small-scale-projects\1_University\3_semestr\krizovka_nsql

# Spusť Flask
.\venv\Scripts\python run.py
```

**Výstup**:
```
╔════════════════════════════════════════╗
║       KrizeMapa - Crisis Manager       ║
║        Flask + MongoDB + Redis         ║
║                                        ║
║  Environment: DEVELOPMENT              ║
╚════════════════════════════════════════╝

🌍 Server running na http://localhost:5000
   Debug mode: ON
```

Otevřeš v prohlížeči: **http://localhost:5000**

---

## 🐳 Docker & Docker Compose

### Proč Docker?

- **Izolace**: MongoDB, Redis, Flask každý v vlastním kontejneru
- **Reproducibilita**: Stejné prostředí na każdém počítači
- **Jednoduchá správa**: Jeden příkaz spustit/zastavit všechno

### Instalace Dockeru

1. **Windows**: https://www.docker.com/products/docker-desktop
2. Instaluj a restartuj počítač
3. Ověř: `docker --version`

### Spuštění s Dockerem

```powershell
cd c:\GitHub\University-stuff-and-small-scale-projects\1_University\3_semestr\krizovka_nsql

# Spustí všechny kontejnery (web, redis, mongodb)
docker-compose up --build

# Nebo na pozadí:
docker-compose up -d --build
```

**Výstup**:
```
Creating krizemap-redis ... done
Creating krizemap-mongo ... done
Creating krizemap-web ... done
```

**Poté**:
- 🌍 Aplikace: http://localhost:5000
- 🔴 Redis: localhost:6379
- 🍃 MongoDB: localhost:27017

### Zastavení kontejnerů

```powershell
docker-compose down

# Zastavit bez smazání volumes:
docker-compose down -v
```

### Podívej se do logů

```powershell
# Všechny logy
docker-compose logs

# Jen web kontejner
docker-compose logs web

# Živé logy (real-time)
docker-compose logs -f web
```

---

## 🔄 Workflow

### Vývojový cyklus

1. **Vytvoř venv** (jestliže ještě nemáš)
   ```powershell
   python -m venv venv
   ```

2. **Aktivuj balíčky** (pokud jsi přidal nový)
   ```powershell
   .\venv\Scripts\pip install -r requirements.txt
   ```

3. **Spusť lokalně** (bez Dockeru)
   ```powershell
   .\venv\Scripts\python run.py
   ```

4. **Testuj v prohlížeči** (http://localhost:5000)

5. **Když je hotovo, testuj v Dockeru**
   ```powershell
   docker-compose down
   docker-compose up --build
   ```

### Přidání nových balíčků

```powershell
.\venv\Scripts\pip install <package-name>
.\venv\Scripts\pip freeze > requirements.txt
```

**Poté aktualizuj Docker** (aby měl nové balíčky):
```powershell
docker-compose up --build
```

---

## 📡 API

### Health Check
```bash
GET /health
```

**Odpověď**:
```json
{
  "status": "ok",
  "database": {
    "mongo": true,
    "redis": true
  }
}
```

### Stats
```bash
GET /events/api/stats
```

**Odpověď**:
```json
{
  "total_events": 5,
  "events_by_severity": {
    "critical": 1,
    "high": 2,
    "medium": 2,
    "low": 0
  }
}
```

### Routes

| Route | Method | Popis |
|-------|--------|-------|
| `/` | GET | Dashboard |
| `/events/submit` | GET/POST | Hlásit krizi |
| `/events/view` | GET | Všechny krize |
| `/events/<id>` | GET | Detail krize |
| `/events/<id>/delete` | POST | Smazat krizi |
| `/health` | GET | Health check |
| `/events/api/stats` | GET | JSON stats |

---

## 🐛 Troubleshooting

### Venv problémy

**Q: "Soubor ...\Activate.ps1 cannot be loaded"**  
A: Místo `Activate.ps1` zavolej přímo pip:
```powershell
.\venv\Scripts\pip install -r requirements.txt
```

**Q: "ModuleNotFoundError: No module named 'flask'"**  
A: Ujisti se, že používáš správný Python z venv:
```powershell
# Ověř cestu
.\venv\Scripts\python -c "import sys; print(sys.executable)"
```

### Docker problémy

**Q: "Port 5000 is already in use"**  
A: Změní port v docker-compose.yml:
```yaml
ports:
  - "5001:5000"  # Externě 5001, interně 5000
```

**Q: "Connection refused" - MongoDB/Redis**  
A: Počkej chvíli až se kontejnery spustí (~5s), poté:
```powershell
docker-compose logs
```

**Q: "Cannot find image mongo:7"**  
A: Docker musí stáhnout image (první spuštění je pomalé):
```powershell
docker-compose pull
docker-compose up --build
```

### Database problémy

**Q: "MongoDB connection failed"**  
A: Zkontroluj `.env`:
```env
MONGO_URI=mongodb://admin:admin@mongodb:27017/krizove_udalosti?authSource=admin
```

**Q: "Redis connection failed"**  
A: Zkontroluj `.env`:
```env
REDIS_URL=redis://redis:6379/0
```

### Git

Pokud se ti commituje `venv/` (nechceme to!), musíš smazat z caching:
```powershell
git rm --cached -r venv/
git commit -m "Remove venv from tracking"
```

---

## 📚 Užitečné příkazy

### Docker
```powershell
# Spusť
docker-compose up -d --build

# Zastavit
docker-compose down

# Logy
docker-compose logs -f

# Restart kontejneru
docker-compose restart web
```

### Python/Venv
```powershell
# Instaluj balíčky
.\venv\Scripts\pip install -r requirements.txt

# Spusť app
.\venv\Scripts\python run.py

# Python shell (pro testování)
.\venv\Scripts\python
```

### Git
```powershell
git status
git add .
git commit -m "Message"
git push
```

---

## 🎯 Další krůčky

- [ ] Přidat login/autentizaci
- [ ] Přidat GPS mapu (Leaflet.js)
- [ ] Přidat real-time notifikace (WebSockets)
- [ ] Unit testy (pytest)
- [ ] CI/CD pipeline (GitHub Actions)
- [ ] Deployment (AWS/Heroku)

---

**Vše hotovo!** 🚀 Těš se na seminárku! 🎉
