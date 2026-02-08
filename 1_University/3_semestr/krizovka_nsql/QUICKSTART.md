# ⚡ QUICK START - KrizeMapa

Nejrychlejší způsob jak spustit aplikaci.

---

## 🚀 Za 5 minut

### 1. Spusť venv & aplikaci (bez Dockeru)

```powershell
cd c:\GitHub\University-stuff-and-small-scale-projects\1_University\3_semestr\krizovka_nsql

# Instaluj balíčky (poprvé, později ne)
.\venv\Scripts\pip install -r requirements.txt

# Spusť aplikaci
.\venv\Scripts\python run.py
```

**Výstup**:
```
🌍 Server running na http://localhost:5000
   Debug mode: ON
```

**Otevřeš v prohlížeči**: http://localhost:5000

---

## 🐳 S Dockerem (lokálně)

```powershell
cd c:\GitHub\University-stuff-and-small-scale-projects\1_University\3_semestr\krizovka_nsql

# Spusť všechny služby
docker-compose up --build

# Aplikace běží na http://localhost:5000
```

**Zastavení**:
```powershell
docker-compose down
```

---

## 📁 Co je kde?

| Cesta | Co | Popis |
|-------|-----|-------|
| `app/` | Flask app | Celá aplikace |
| `app/templates/` | HTML | Webové stránky |
| `app/static/css/style.css` | Styling | Design |
| `run.py` | Spuštění | Startovací soubor |
| `requirements.txt` | Balíčky | Python závislosti |
| `docker-compose.yml` | Docker | Multi-container orchestrace |
| `.env` | Konfigurace | Environment proměnné |
| `README.md` | Dokumentace | Kompletný průvodce |
| `DOCKER_TUTORIAL.md` | Docker Guide | Detaily o Dockeru |

---

## ✅ Checklist - Co jsme udělali

- [x] Vytvořili venv (python -m venv venv)
- [x] Nainstalovali Flask, Redis, MongoDB driver (pip install -r requirements.txt)
- [x] Napsali Flask aplikaci (app/__init__.py, routes.py, models.py, db.py)
- [x] Vytvořili HTML templates (6 šablon)
- [x] Napsali CSS styling (responsivní design)
- [x] Napsali Dockerfile (containerizace)
- [x] Napsali docker-compose.yml (orchestrace 3 služeb)
- [x] Spustili aplikaci na http://localhost:5000
- [x] Vytvořili dokumentaci (README.md, DOCKER_TUTORIAL.md)

---

## 🔧 Základní příkazy

### Python / Venv
```powershell
# Instaluj balíčky
.\venv\Scripts\pip install -r requirements.txt

# Spusť aplikaci
.\venv\Scripts\python run.py

# Python shell
.\venv\Scripts\python
```

### Docker
```powershell
# Spusť
docker-compose up -d --build

# Zastavit
docker-compose down

# Logy
docker-compose logs -f web
```

### Git
```powershell
git status
git add .
git commit -m "Popis změny"
git push
```

---

## 📞 Potřebuješ pomoc?

1. **Logy**: `docker-compose logs -f`
2. **Dokumentace**: Přečti `README.md` a `DOCKER_TUTORIAL.md`
3. **Venv chyby**: Zkontroluj že Python je z `.\venv\Scripts\python`
4. **Docker chyby**: Ujistý se že je Docker Desktop spuštěný

---

## 🎯 Dalších kroků

- [ ] Otestuj všechny funkce (submit, view, delete)
- [ ] Přidej login (Flask-Login)
- [ ] Přidej mapu (Leaflet.js)
- [ ] Přidej notifikace (WebSockets)
- [ ] Napíš testy (pytest)
- [ ] Deploy na server

---

**Hotovo!** Jsi připravený na seminárku! 🚀
