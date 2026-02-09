# 🐳 Docker & Docker Compose Tutoriál - KrizeMapa

Kompletný průvodce pro pochopení Docker, containerizace a orchestrace.

---

## 📖 Table of Contents

1. [Co je Docker?](#co-je-docker)
2. [Základní pojmy](#základní-pojmy)
3. [Dockerfile vysvetlován](#dockerfile-vysvetlován)
4. [Docker Compose vysvetlován](#docker-compose-vysvetlován)
5. [Praktické příkazy](#praktické-příkazy)
6. [Workflow](#workflow)
7. [Networking & Volumes](#networking--volumes)
8. [Debugging](#debugging)

---

## 🤔 Co je Docker?

Docker je **kontejnerizační platforma**, která balí aplikaci + všechny závislosti do izolovaného "boxu" (kontejneru).

### Analogie
```
Traditional:  Windows → Python → Pip → Flask → App (chaos, ale funguje na mém PC!)
              ❌ Nefunguje na tvém PC - chybí nějaký balíček

Docker:       Windows → Docker Desktop → Kontejner [Python + Flask + App + dependencies]
              ✅ Pracuje stejně na tvém PC, měja PC, serveru
```

### Proč?
- **Reproducibilita**: Stejné prostředí wszędzie
- **Izolace**: Flask neruší MySQL, Redis neruší Flask
- **Jednoduchý deploy**: Jeden příkaz spustit/zastavit
- **Skalabilnost**: Může běžet 5x stejný kontejner (load balancing)

---

## 🎯 Základní pojmy

### Image
**Co to je**: Šablona/recept pro vytvoření kontejneru.  
**Analogie**: Je to jako ISO soubor, který si můžeš "nainstalovat".

```bash
docker image ls          # Seznám všech images
docker image build .     # Vytvoř image ze Dockerfile
```

### Container
**Co to je**: Běžící instance image.  
**Analogie**: Je to jako počítač, který běží.

```bash
docker container ls      # Seznám běžících kontejnerů
docker run <image>       # Spusť kontejner z image
```

### Registry
**Co to je**: Online "obchod" s images.

```bash
docker pull python:3.11-slim  # Stáhni image z Docker Hub
docker push myimage:latest    # Nahraj svůj image
```

---

## 🔧 Dockerfile vysvetlován

### Náš Dockerfile pro KrizeMapa

```dockerfile
FROM python:3.11-slim
```
- **Začni od**: Python 3.11 base image (slim = menší, bez zbytečností)

```dockerfile
WORKDIR /app
```
- **Pracovní adresář**: Všechny příkazy běží zde

```dockerfile
RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*
```
- **RUN**: Spusť command při buildu
- `apt-get install gcc`: Stáhni C compiler (potřeba pro MongoDB driver)
- `rm -rf`: Smaž cache (zmenšit velikost image)

```dockerfile
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
```
- **COPY**: Zkopíruj `requirements.txt` do kontejneru
- **RUN**: Instaluj Python balíčky

```dockerfile
COPY . .
```
- Zkopíruj celou aplikaci do kontejneru

```dockerfile
EXPOSE 5000
```
- Otevři port 5000 (oznamuje "poslouchám na 5000")

```dockerfile
ENV FLASK_ENV=production
ENV FLASK_APP=run.py
```
- Nastav environment proměnné

```dockerfile
CMD ["python", "run.py"]
```
- **Výchozí příkaz**: Když spustíš kontejner, spusť toto

### Build image
```powershell
cd c:\...\krizovka_nsql
docker build -t krizemap:latest .
```

`-t` = tag (jméno:verze)

### Spusť kontejner
```powershell
docker run -p 5000:5000 krizemap:latest
```

`-p` = port mapping (snímač portu:port v kontejneru)

---

## 🎼 Docker Compose vysvetlován

**Když máš 1 aplikaci**: Docker stačí.  
**Když máš 3+ služby**: Docker Compose!

### Náš docker-compose.yml

```yaml
version: '3.8'
```
- Verze Docker Compose API

```yaml
services:
  web:
    build: .
```
- Služba `web`: Vytvoř image ze Dockerfile v aktuálním adresáři

```yaml
    container_name: krizemap-web
```
- Jméno kontejneru (pro snadnější debugging)

```yaml
    ports:
      - "5000:5000"
```
- Port mapping: `localhost:5000` → `kontejner:5000`

```yaml
    environment:
      FLASK_ENV: production
      REDIS_URL: redis://redis:6379/0
      MONGO_URI: mongodb://admin:admin@mongodb:27017/...
```
- Environment proměnné (jak se služby vidí navzájem)

**KLÍČOVÉ**: `redis://redis:6379/0` - Docker DNS jméno `redis` je přeloženo na IP kontejneru!

```yaml
    depends_on:
      - redis
      - mongodb
```
- Spusť `web` AŽ PO `redis` a `mongodb`

```yaml
    volumes:
      - ./app:/app/app
```
- **Volume mapping**: Lokální `./app` → kontejner `/app/app`
- Umožňuje live editing bez rebuildu!

```yaml
    networks:
      - krizemap-network
```
- Všechny služby jsou v síti `krizemap-network` (mohou si "vidět")

```yaml
    restart: unless-stopped
```
- Auto-restart když padne (pokud ho ručně nezastavíš)

### Services - Redis

```yaml
  redis:
    image: redis:7-alpine
    container_name: krizemap-redis
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data
```
- Používá **oficialní Redis image**
- Port 6379 (standard Redis port)
- **Volume**: `redis-data` = pojmenovaný volume (data persisten mezi restarty)

### Services - MongoDB

```yaml
  mongodb:
    image: mongo:7
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: admin
```
- Aut admin:admin
- Automaticky vytvoří DB a uživatele

```yaml
    volumes:
      - mongo-data:/data/db
```
- Data se ukládají do `mongo-data` volume

### Volumes (na konci)

```yaml
volumes:
  redis-data:
  mongo-data:
```
- **Pojmenované volumes**: Docker se o ně stará automaticky
- Jsou persistentní (živé než `docker-compose down -v`)

### Networks

```yaml
networks:
  krizemap-network:
    driver: bridge
```
- **Bridge network**: Vytvoří virtuální síť kde si kontejnery "vidí"
- `web` se připojí k `redis` jako `redis://redis:6379`

---

## 💻 Praktické příkazy

### Build & Run

```powershell
# Build image (poprvé je pomalé)
docker build -t krizemap:latest .

# Spusť kontejner
docker run -p 5000:5000 krizemap:latest

# Spusť na pozadí
docker run -d -p 5000:5000 --name my-app krizemap:latest

# Zastavit
docker stop my-app

# Smazat kontejner
docker rm my-app
```

### Docker Compose

```powershell
# Spusť všechny služby
docker-compose up

# Build images poprvé
docker-compose up --build

# Na pozadí
docker-compose up -d

# Zastavit
docker-compose down

# Zastavit + smazat volumes
docker-compose down -v

# Restart jedné služby
docker-compose restart web

# Logs
docker-compose logs
docker-compose logs -f          # Live
docker-compose logs web         # Jen web služba
docker-compose logs --tail 50   # Posledních 50 řádků
```

### Inspekce

```powershell
# Seznám images
docker image ls

# Seznám kontejnerů (běžících)
docker container ls

# Všechny kontejnery (včetně zastavených)
docker container ls -a

# Info o kontejneru
docker inspect my-app

# Spusť command v běžícím kontejneru
docker exec -it my-app sh       # Shell
docker exec my-app python -c "print('hello')"

# Stats (CPU, memory)
docker stats
```

---

## 🔄 Workflow

### Vývojový cyklus s Docker Compose

```powershell
# 1. Startupy (poprvé)
cd krizovka_nsql
docker-compose up --build

# 2. Aplikace běží na http://localhost:5000

# 3. Chceš něco změnit?
# Edituj soubor (např. app/routes.py)
# Flask auto-reload stačí! (live editing díky volumes)

# 4. Vidíš error? Podívej se do logů
docker-compose logs -f web

# 5. Quando je hotovo
docker-compose down
```

### Když chceš změnit Python balíčky

```powershell
# 1. Instaluj lokálně (v venv)
.\venv\Scripts\pip install <new-package>

# 2. Aktualizuj requirements.txt
.\venv\Scripts\pip freeze > requirements.txt

# 3. Rebuild Docker image
docker-compose up --build

# 4. Docker stáhne a instaluje nový balíček
```

### Production vs Development

```powershell
# Development (s volume mappingem)
docker-compose up -d

# Production (bez volumes, read-only)
docker-compose -f docker-compose.yml up -d
# (ideálně by byl docker-compose.prod.yml se změnami)
```

---

## 🔗 Networking & Volumes

### Networking - Jak se vidí kontejnery?

**Docker interně**:
```
krizemap-network (Bridge network)
├── web (IP: 172.20.0.2)
├── redis (IP: 172.20.0.3)
└── mongodb (IP: 172.20.0.4)
```

**DNS resolution** (automaticky):
- `web` se připojí k `redis://redis:6379` ✅
- Docker překládá `redis` → 172.20.0.3

**Bez compose** (bez networking):
- Musil by si zadat IP ručně ❌
- Hrozný nightmare!

### Volumes - Persistenci & Live Editing

#### Pojmenované volumes
```yaml
volumes:
  redis-data:
```
- Spravuje Docker
- Data persisten mezi `docker-compose down/up`
- Cestu určuje Docker (obvykle `C:\ProgramData\Docker\volumes`)

#### Bind mounts (File mapping)
```yaml
volumes:
  - ./app:/app/app
```
- Mapují lokální adresář do kontejneru
- **Live editing**: Změny lokálně = vidítko v kontejneru
- Flask reload automaticky spustí aplikaci znovu

```powershell
# Smazat všechny volumes
docker volume prune

# Listovat volumes
docker volume ls
```

---

## 🔍 Debugging

### Logy

```powershell
# Všechny logy ze všech služeb
docker-compose logs

# Jen poslední 100 řádků
docker-compose logs --tail 100

# Živé logy (ctrl+c zastaví)
docker-compose logs -f

# Jen web služba
docker-compose logs web

# Jen Flask aplikace errors
docker-compose logs web | findstr "ERROR"
```

### Shell do kontejneru

```powershell
# Interaktivní shell
docker-compose exec web sh
# nebo bash
docker-compose exec web bash

# Jednorazový příkaz
docker-compose exec web python -c "print('hello')"
```

### Ověř konektivitu

```powershell
# Spusť Python v kontejneru
docker-compose exec web python

# V Python shellě
>>> import redis
>>> r = redis.from_url('redis://redis:6379/0')
>>> r.ping()  # Mělo by vrátit True
True

>>> from pymongo import MongoClient
>>> client = MongoClient('mongodb://admin:admin@mongodb:27017/krizove_udalosti?authSource=admin')
>>> client.server_info()  # Mělo by vrátit info o serveru
```

### Network issues

```powershell
# Zkontroluj síť
docker network ls
docker network inspect krizemap_krizemap-network

# Ping z jedné služby na druhou
docker-compose exec web ping redis
docker-compose exec web ping mongodb
```

---

## 🚨 Chyby & Řešení

### "Port 5000 is already in use"
```yaml
# docker-compose.yml
ports:
  - "5001:5000"  # Externě 5001, interně 5000
```

### "Connection refused" - MongoDB
- Vlož 10s `depends_on` se řeší i bez čekání
- Zkus manuálně:
```powershell
docker-compose down
docker-compose up --build
```

### "Image not found"
```powershell
docker-compose pull  # Stáhni images

# Nebo buildzování je pomalé:
docker-compose up --build  # Poraď si s tím!
```

### "Cannot connect from web to redis"
- Ověř `environment` v docker-compose:
```yaml
REDIS_URL: redis://redis:6379/0
```
- `redis` MUSÍ být jméno kontejneru nebo alias sítě

---

## 🎯 Best Practices

1. **Vždy používej Compose pro multi-container**: Docker příkazy jsou manuální
2. **Volumes pro data**: MongoDB/Redis data musí přeživou restarts
3. **Live editing**: Mapuj app directory (viz `./app:/app/app`)
4. **Health checks**: Přidej do services (auto-restart při selhání)
5. **Logy**: Vždy si podívej `docker-compose logs` když něco selhae
6. **Restart policy**: `restart: unless-stopped` = auto-recovery

---

## 📚 Užitečné zdroje

- **Docker Hub**: https://hub.docker.com (oficiální images)
- **Docker Docs**: https://docs.docker.com
- **Docker Cheat Sheet**: https://github.com/wsargent/docker-cheat-sheet

---

**Gratulace!** Teď chápáš Docker! 🎉

Pokud máš otázky, běž na dokumentaci nebo se zeptej mě.

Dalšího kroku: Pushni všechno do Githubu!
