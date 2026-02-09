# KrizeMapa - Mapování na osnovu "NoSQL databáze + Flask"

**Dokument vysvětluje, jak každá kapitola osnovy je implementována v aplikaci KrizeMapa.**

---

## 0) Vymezení a cíle NoSQL

### Definice a cíle
- **Co je KrizeMapa?** Webová aplikace pro hlášení a správu krizových situací.
- **Databáze KrizeMapa = NOSQL hybrid:**
  - **MongoDB** = dokumentová NoSQL DB (data ukládána jako JSON)
  - **Redis** = key-value NoSQL cache
  - **Flask** = webový framework

### Implementace v KrizeMapa
```
Databáze má 3 komponenty:
1. MongoDB (persistent storage) - hlavní databáze
2. Redis (cache) - pro zrychlení čtení
3. Flask - REST API přístup
```

**Dokumentová struktura (`app/models.py`):**
```python
class CrisisEvent:
    {
        "_id": ObjectId,           # MongoDB auto-generuje
        "title": str,              # Název krize
        "description": str,        # Popis situace
        "location": str,           # Lokace
        "severity": int (1-5),     # Stupeň závažnosti
        "type": str,               # Typ krize (8 možností)
        "latitude": float,         # GPS souřadnice
        "longitude": float,        # GPS souřadnice
        "created_at": datetime     # Čas hlášení
    }
```

### Proč NoSQL místo SQL?
1. ✅ **Flexibilní schéma** - přidáme pole bez migrace
2. ✅ **Horizontální škálování** - Redis cache + MongoDB clustering
3. ✅ **Výkon** - cache v paměti (Redis) pro rychlé čtení
4. ✅ **Dokumenty místo relací** - data se nemusí normalizovat do tabulek

---

## 1) SQL vs NoSQL

### Porovnání v KrizeMapa

| Aspekt | SQL (relační) | KrizeMapa (NoSQL hybrid) |
|--------|---------------|--------------------------|
| **Schéma** | Pevné tabulky | Flexibilní JSON dokumenty |
| **Zápis** | Normalizace - více tabulek | Denormalizace - vše v jednom dokumentu |
| **Dotazy** | INNER JOIN mezi tabulkami | Agregační pipeline (MongoDB) |
| **Transakce** | ACID zaručené | BASE (eventual consistency) |
| **Škálování** | Obtížné horizontálně | Snadné - Redis + MongoDB |
| **Cache** | Navíc (Redis) | Integrální (Redis v app) |

### Konkrétní implementace
```
SQL by vyžadoval:
  - tabulka `users` (kdo hlásil)
  - tabulka `crises` (krize)
  - tabulka `events` (posloupnost zásahu)
  - JOINy při čtení = pomalé

NoSQL (KrizeMapa) má:
  - kolekce `events` v MongoDB
  - všechny data v jednom dokumentu
  - Redis cache pro top 6 posledních
  - denormalizace OK (málo aktualizací)
```

---

## 2) Škálovatelnost

### Vertikální škálování (scaling up)
❌ **V KrizeMapa NEIMPLEMENTOVÁNO:**
- Máme Docker kontejnery (ale jen 1 Flask instance)

### Horizontální škálování (scaling out)
✅ **V KrizeMapa ČÁSTEČNĚ IMPLEMENTOVÁNO:**

```yaml
docker-compose.yml:
  services:
    web:      # Flask - jeden kontejner (ale mohlo by jich být víc)
    redis:    # Redis - jeden instance (cache layer)
    mongodb:  # MongoDB - jeden kontejner (ale MongoDB umí sharding)
```

**Potenciál pro horizontální škálování:**
1. Přidat více Flask instancí s load balancerem (nginx)
2. MongoDB Replica Set (2-3 uzly)
3. Redis cluster (více Redis instancí)

**Nyní:**
- ✅ Redis cachuje data v paměti (zrychluje)
- ❌ Bez load balanceru (jen jeden Flask)
- ❌ Bez MongoDB replikace (jen jeden Mongo uzel)

---

## 3) CAP teorém a důsledky

### CAP = Consistency, Availability, Partition tolerance

**Jak se KrizeMapa řídí CAP?**

```
KrizeMapa je: AP systém (přiklání se k dostupnosti)
```

| Vlastnost | KrizeMapa | Vysvětlení |
|-----------|-----------|-----------|
| **C - Consistency** | Oslabená | Redis cache může být stará (5 min TTL) |
| **A - Availability** | Silná | Endpoint vrátí data i bez Mongo (graceful degradation) |
| **P - Partition** | Tolerance | Redis + Mongo = redundance |

### Praktická situace v KrizeMapa

```python
# app/__init__.py - Graceful degradation
try:
    db = DatabaseManager(mongo_uri, redis_url, db_name)
    app.db = db
except Exception as e:
    app.db = None  # Pokračuj bez DB!
```

**Při výpadku MongoDB:**
- ✅ Aplikace zůstane naživu (Availability)
- ❌ Bez čtení/zápisu krizí (dočasně)
- ❌ Dashboard zobrazí 0 krizí (konzistence ztracena)

**Při výpadku Redis:**
- ✅ Stále se čte z MongoDB (jen pomalejší)
- ✅ Cache se vybuduje při příštím čtení

---

## 4) ACID vs BASE

### ACID (by měl být ideál)
```
A - Atomicity: vše nebo nic
C - Consistency: po transakci platí pravidla
I - Isolation: transakce se neruší
D - Durability: data jsou trvalá
```

### BASE (co KrizeMapa má)
```
BA - Basically Available: systém funguje ✓
S - Soft state: Redis cache může být stará (5 min)
E - Eventual consistency: po 5 minutách se data srovnají
```

### Konkrétní případ: Vytvoření krize

```python
# app/db.py - create_event()
def create_event(self, event: CrisisEvent) -> str:
    collection = self.get_collection("events")
    result = collection.insert_one(event.to_dict())
    
    # Hned invaliduj cache!
    self.redis.delete("events:all")
    self.redis.delete("events:count")
    self.redis.delete("events:today")
    
    return str(result.inserted_id)
```

**Jaká ACID vlastnost je tu zachována?**
- ✅ **D - Durability**: MongoDB zapisuje na disk
- ❌ **A - Atomicity**: Pokud Redis selhá, cache není vymazáno
- ⚠️ **C - Consistency**: Dočasně mohou být stará data
- ❌ **I - Isolation**: Bez výslovných transakcí

---

## 5) Distribuce dat: Sharding a Replikace

### Homogenní vs Heterogenní Cluster

**KrizeMapa je:** HOMOGENNÍ cluster

```yaml
docker-compose.yml:
  services:
    web:      # 1 Flask (1 vCPU, 512MB RAM)
    redis:    # 1 Redis (paměť, vCPU)
    mongodb:  # 1 MongoDB (disk, vCPU)
```

Všechny kontejnery mají stejné parametry = homogenní. Kdyby byl cluster rozdělen:
- FastDB server (SSD, víc RAM) = hot data
- SlowDB server (HDD) = cold data
= HETEROGENNÍ

### Sharding v KrizeMapa

❌ **NEIMPLEMENTOVÁNO** (máme jen jeden Mongo uzel)

**Jak by se dalo implementovat:**

```
Sharding klíč by byl location nebo severity:

Shard 1: crises z Praha (location.startswith("Praha"))
Shard 2: crises z Brno (location.startswith("Brno"))
Shard 3: crises ostatní lokace

Výhody:
- Data se rozdělí na 3 servery
- Dotaz "all crises in Praha" jde jen na Shard 1

Riziko (hot-spot):
- Pokud všechny krize budou v Praze = hot shard
```

### Hot vs Cold data (v kontextu KrizeMapa)

Mělo by se počítat s:
```
HOT data:  Krize z posledních 24 hodin (aktuální)
COLD data: Staré krize (archiv)

V KrizeMapa:
- HOT: Redis cache (super rychlé)
- COLD: MongoDB disk (pomalé, ale durable)

TTL v Redis = 5 minut = dáme preference HOT datům
```

### Replikace v KrizeMapa

❌ **NEIMPLEMENTOVÁNO** (máme jen jednu kopii MongoDB)

**Jak by to bylo:**

```yaml
mongodb:
  replica_set:
    primary:   node1 (primary - zapisuje)
    secondary: node2 (replica - čte)
    secondary: node3 (replica - čte, failover)
```

Teď máme jen PRIMARY (jeden uzel).

---

## 6) Replikace: Topologie, Konflikty, Kvórum

### Master-Slave (Primary-Replica) v KrizeMapa

❌ **Máme SINGLE PRIMARY** (žádné repliky):

```
MongoDB:
┌─────────────────┐
│  PRIMARY MONGO  │ ← všechny zápisy
│  (1 uzel)       │
└─────────────────┘
```

Kdyby měla n=3 repliky:
```
┌──────────────────┐
│  PRIMARY (write) │ ← zápisy sem
└──────────────────┘
        ↓ (replikuje)
┌──────────────────┐
│  REPLICA 1 (read)│
├──────────────────┤
│  REPLICA 2 (read)│
├──────────────────┤
│  REPLICA 3 (read)│
└──────────────────┘
```

### Konflikty v replikaci

**V KrizeMapa NEJSOU konflikty protože:**
1. Máme 1 MongoDB uzel (žádné konkurentní zápisy)
2. Flask je bezstavový - každý request je nezávislý

**Kdyby byly repliky, mohlo by dojít k:**

```
Write-read conflict:
  Uživatel A: nahlásí novou krizi (zápis na primary)
  Uživatel B: hned čte seznam (čte z replica co ještě nemá nový zápis)
  → Uživatel B nevidí krizi co zrovna přibyly (eventual consistency!)

Write-write conflict:
  Uživatel A: edituje krizi na replica 1
  Uživatel B: edituje stejnou krizi na replica 2
  → Jaká verzí se používá? (MongoDB nemá auto-merge)
```

### Kvórum (quorum) v KrizeMapa

❌ **NEPOUŽÍVÁ SE** (máme 1 uzel, nelze kvórum s 1)

**Kdyby měl 3 repliky:**

```
N = 3 (počet replik)
W = 2 (write quorum - majorita)
R = 1 (read quorum)

Podmínka: W + R > N
  2 + 1 > 3? Ne, je to 3 = 3, ale OK

Praktika:
- Zápis: potřeba potvrzení z 2 uzlů (majority)
- Čtení: stačí 1 uzel (fast read, ale mohou být stará data)
```

**Bez kvóra (nyní):**
```
Zápis: MongoDB potvrdí hned
Čtení: vrátí co je v DB

Bez ochrany proti write-write konfliktům!
```

---

## 7) Základní typy NoSQL databází

### Čtyři typu NoSQL

| Typ | Příklad | KrizeMapa | Popis |
|-----|---------|-----------|-------|
| **Key-Value** | Redis | ✅ Používáme | Cache: `events:all` → seznam |
| **Document** | MongoDB | ✅ Používáme | Kolekce: `events` → JSON docs |
| **Wide-Column** | Cassandra | ❌ Nepoužíváme | Analytika (OLAP) |
| **Graph** | Neo4j | ❌ Nepoužíváme | Vztahy mezi entitami |

---

## 8) Databáze typu klíč-hodnota: Redis (prakticky)

### Co je Redis?

Redis = **in-memory key-value store** (cache v paměti)

```python
# app/db.py - Redis operace
self.redis.set("key", "value", ex=300)  # ex = expiration (TTL)
self.redis.get("key")                   # Get value
self.redis.delete("key")                # Delete
```

### Redis jako cache v KrizeMapa

```
Workflow:

1. Uživatel: GET /events/view
2. Flask: Zkontroluj Redis
   - Hit: vrať z cache (velmi rychlé)
   - Miss: čti z MongoDB, ulož do Redis, vrať
3. Redis: data v paměti (µs - milisekundy)
4. Mongdo: data na disku (ms - milisekundy)
```

### Praktická implementace

```python
# app/db.py
def get_all_events(self, limit=100, skip=0):
    cache_key = "events:all"
    
    # Zkus cache
    cached = self.redis.get(cache_key)
    if cached:
        logger.info("Cache HIT")
        return json.loads(cached)
    
    # Cache miss - čti z DB
    logger.info("Cache MISS")
    events = self.db["events"].find().skip(skip).limit(limit)
    
    # Ulož do cache na 5 minut
    self.redis.set(cache_key, json.dumps(events), ex=300)
    
    return events
```

### TTL (Time To Live)

```python
# Redis s TTL = automatické mazání po expiraci
self.redis.set("events:all", json.dumps(data), ex=300)
#                                              ex=300 → 5 minut

# Po 5 minutách: klíč zmizí, cache MISS se zopakuje
```

### Cache invalidace

```python
# Po vytvoření nové krize: smaž cache aby se neukazovaly stará data
def create_event(self, event):
    # Vytvoř event
    result = self.db["events"].insert_one(event.to_dict())
    
    # Invaliduj cache - aby se viděla nová krize
    self.redis.delete("events:all")
    self.redis.delete("events:count")
    self.redis.delete("events:today")
    
    return str(result.inserted_id)
```

---

## 9) Dokumentově orientované DB: MongoDB a JSONB

### MongoDB v KrizeMapa

MongoDB = dokumentová NoSQL DB

```javascript
// Kolekce: events
{
    "_id": ObjectId("..."),
    "title": "Požár v obchodním centru",
    "description": "Vypukl požár v areálu...",
    "location": "Praha, Václavské náměstí",
    "severity": 4,
    "type": "požár",
    "latitude": 50.0827,
    "longitude": 14.4385,
    "created_at": ISODate("2026-02-09T10:30:00Z")
}
```

### Embed vs Reference

**KrizeMapa používá: EMBED (vše v jednom dokumentu)**

```
EMBED (aktuální):
┌─────────────────────────────────┐
│ CrisisEvent (vše v jednom doc)  │
│ ├─ title                        │
│ ├─ description                  │
│ ├─ location                     │
│ └─ creator_info (vestavěno)     │
└─────────────────────────────────┘

Výhody: Jeden READ = všechna data, superbrzké
Nevýhody: Duplicita, obtížné updaty
```

**Kdyby měl REFERENCE (jako SQL):**

```
┌──────────────┐         ┌─────────────────┐
│ users (coll) │ ←────── │ events (coll)   │
├──────────────┤         ├─────────────────┤
│ user_id      │         │ creator_id: ref │
│ name         │         │ title           │
│ email        │         └─────────────────┘
└──────────────┘

Čtení: více DBqueries, ale bez duplicity
```

### MongoDB pipelines (agregace)

MongoDB umožňuje komplexní agregace přes `$match`, `$group`, `$sort` atd.

**KrizeMapa by mohl použít:**

```python
# Agregace: spočítej kolik krizí by typu
pipeline = [
    {"$match": {"type": "požár"}},           # Filtr
    {"$group": {"_id": "$severity",          # Seskupuj podle severity
                "count": {"$sum": 1}}},      # Počítej dokumenty
    {"$sort": {"_id": 1}}                    # Seřaď vzestupně
]
result = db["events"].aggregate(pipeline)
```

V KrizeMapa se to **nepoužívá** (máme prostší dotazy).

### Map-Reduce koncept

Map-Reduce = funkcionální programování pro agregace

```javascript
// Map: vytvoř páry (klíč, hodnota)
map = function() {
    emit(this.type, 1);  // key=type, value=1
}

// Reduce: agreguj podle klíče
reduce = function(key, values) {
    return Array.sum(values);  // Sečti všechny 1
}

// Výsledek: počet krizí podle typu
```

V KrizeMapa se **mapReduce** nepoužívá (pipeline je modernjší).

### PostgreSQL JSONB (hybrid)

❌ **KrizeMapa nepoužívá PostgreSQL**, ale pro srovnání:

```sql
-- PostgreSQL s JSONB = SQL transakcí + JSON flexibilita
CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    data JSONB  -- Celý dokument jako JSON!
);

-- Dotaz na JSON pole
SELECT data->>'title' FROM events 
WHERE data->>'severity' = '4';
```

**Výhoda:** ACID transakce + JSON flexibilita  
**Nevýhoda:** Pomalejší než čistě NoSQL na velké datové objemy

---

## 10) Sloupcově orientované systémy: Cassandra, HANA; analytické funkce

### Apache Cassandra (wide-column)

❌ **KrizeMapa nepoužívá**, ale pro zkoušku:

```
Cassandra = distribuovaná NoSQL pro zápisy
Optimalizace: horizontální škálování, tunable consistency

Modelování: query-driven (navrhneš tabulky podle dotazů, které budeš dělat)

Příklad pro KrizeMapa v Cassandře:
CREATE TABLE events_by_type (
    type TEXT,
    created_at TIMESTAMP,
    title TEXT,
    PRIMARY KEY (type, created_at)
);
```

**Charakteristika:**
- ✅ Vysoký throughput (zápisy)
- ✅ Distribuovaná (bez single point of failure)
- ✅ Tunable consistency (nastavuješ, kolik uzlů potvrdí zápis)
- ❌ Pomalá čtení na "nejnovější data"

### SAP HANA (relační columnar)

❌ **KrizeMapa nepoužívá**, ale:

```
HANA = sloupcové uložení dat
Optimalizace: agregace, SUM/AVG/GROUP BY (BI dotazy)

Rozdíl od MongoDB:
MongoDB: řádkově orientovaný (čti celý dokument)
HANA:    sloupcově orientovaný (čti jen sloupec)

Příklad HANA dotazu:
SELECT type, COUNT(*) as count
FROM events
GROUP BY type;

↓

Čte jen sloupce: [type, type, type, ...] a počítá
(bez toho aby četl title, description, apod)
```

### OLTP vs OLAP

| Vlastnost | OLTP | OLAP |
|-----------|------|------|
| **Příklad** | KrizeMapa (transaktce) | BI (analytika) |
| **Operace** | INSERT, UPDATE (malé) | SELECT, GROUP BY (velké) |
| **Struktura DB** | Řádková (MongoDB) | Sloupcová (HANA, Cassandra) |
| **Transakce** | Krátké, ACID | Dlouhé, batch |
| **Odpověď** | ms | seconds/minutes |

**KrizeMapa je: OLTP systém** (transaktce - hlášení krizí)

---

## 11) Grafově orientované DB: Neo4j

❌ **KrizeMapa nepoužívá**, ale pro zkoušku:

### Co je Graph DB?

Neo4j = data jako uzly + vztahy + vlastnosti

```
Příklad pro KrizeMapa:
Uzly:     Crisis, Location, User
Vztahy:   (Crisis)-[:LOCATED_IN]->(Location)
          (Crisis)-[:REPORTED_BY]->(User)

Dotaz (Cypher):
MATCH (u:User)-[:REPORTED_BY]-(c:Crisis)-[:LOCATED_IN]->(l:Location)
WHERE l.name = "Praha"
RETURN c.title, u.name, l.name;
```

### Kdy se hodí?

- ✅ Sociální sítě (kdo zná koho)
- ✅ Doporučovací systémy (co se lidem líbí)
- ✅ Vztahy mezi krizemi (spojené příčiny)
- ❌ Jednoduché CRUD operace (KrizeMapa)

---

## 12) Veledata (Big Data) a BI pojmy + ETL

### V-vlastnosti Big Data

| Vlastnost | KrizeMapa | Popis |
|-----------|-----------|-------|
| **Volume** | ❌ Málo | Máme jen ~20 testovacích krizí |
| **Velocity** | ❌ Nízká | Krize se hlašují zřídka |
| **Variety** | ✅ Střední | 8 typů krizí, flexibilní text |
| **Valence** | ✅ Ano | Krize mají různé atributy |

KrizeMapa **NENÍ Big Data** (příliš málo dat), ale **ARCHITEKTURA** je připravena na to.

### BI pojmy v KrizeMapa

| Pojem | Popis | V KrizeMapa |
|-------|-------|-----------|
| **Data Ocean** | Všechna data co existují | Nelze, máme jen krize |
| **Data Lake** | Data co plánujeme | MongoDB kolekce |
| **Data Warehouse** | Strukturovaná data (SQL) | MongoDB (dokumenty) |
| **Data Mart** | Část BI (např. jen lokace) | Filtrování events |
| **Data Cube (OLAP)** | 3D řezy dat (by-type, by-severity, by-location) | ❌ Neimplementováno |
| **Data Report** | Výstup analýzy | Dashboard HTML |

### ETL transformace (Extract-Transform-Load)

❌ **KrizeMapa NEIMPLEMENTUJE ETL formálně**, ale koncept existuje:

```
Extract (app/initial_db_fill.py):
  - Vytvoří 20 umělých krizí

Transform (models.py CrisisEvent):
  - Validace (severity 1-5, typy)
  - Formování do JSON/BSON

Load (db.py create_event):
  - INSERT do MongoDB
  - Invalidace Redis cache
```

---

## 13) Flask (web) – endpointy, šablony, statika, formuláře, REST

### Co je Flask (teorie)

Flask = mikroframework pro Python webové aplikace

**Komponenty:**
1. Routing (endpointy) - @app.route()
2. Request/Response - GET, POST
3. Šablony - Jinja2
4. Statika - CSS, JS, obrázky
5. REST API - JSON responses

### Koncové body (endpoints) a routing v KrizeMapa

```python
# app/routes.py

@main_bp.route("/")
def index():
    """GET / - Homepage/Dashboard"""
    return render_template("dashboard.html")

@events_bp.route("/submit", methods=["GET", "POST"])
def submit_event():
    """GET /events/submit - formulář
       POST /events/submit - ulož krizi"""
    if request.method == "POST":
        # Zpracuj formulář
        ...

@events_bp.route("/view")
def view_all():
    """GET /events/view - seznam krizí (paginated)"""
    return render_template("view_events.html", events=events)

@events_bp.route("/<event_id>")
def view_event(event_id):
    """GET /events/<id> - detail jedné krize"""
    return render_template("event_detail.html", event=event)

@events_bp.route("/<event_id>/delete", methods=["POST"])
def delete_event(event_id):
    """POST /events/<id>/delete - smaž krizi"""
    ...
```

### HTTP metody v KrizeMapa

| Metoda | Endpoint | Popis |
|--------|----------|-------|
| **GET** | `/` | Vrť dashboard |
| **GET** | `/events/submit` | Vrť formulář |
| **POST** | `/events/submit` | Přijmi data a vytvoř krizi |
| **GET** | `/events/view` | Vrť seznam krizí |
| **GET** | `/events/<id>` | Vrť detail krize |
| **POST** | `/events/<id>/delete` | Smaž krizi |
| **GET** | `/health` | Health check |

### Šablony (templates) a Jinja2

KrizeMapa má 6 šablon:

```
app/templates/
├── base.html          # Základ (navigation, footer)
├── dashboard.html     # Homepage (statistika)
├── submit_event.html  # Formulář pro hlášení
├── view_events.html   # Seznam krizí (paginated)
├── event_detail.html  # Detail krize
└── error.html         # Error stránka
```

**Template inheritance:**

```html
<!-- base.html -->
<html>
  <nav>...</nav>
  {% block content %}{% endblock %}
  <footer>...</footer>
</html>

<!-- dashboard.html -->
{% extends "base.html" %}
{% block content %}
  <h1>Dashboard</h1>
  <p>Total: {{ total_events }}</p>
{% endblock %}
```

**Jinja2 proměnné:**

```html
<p>Celkem hlášeno: {{ total_events }} krizí</p>
<p>Dnes: {{ today_events }} krizí</p>

{% for event in latest_events %}
  <li>{{ event.title }} - {{ event.severity }}/5</li>
{% endfor %}
```

### Kaskádové styly a statické soubory

```
app/static/
├── css/
│   └── style.css     (600+ řádků, responsive design)
└── js/
    └── main.js       (interaktivita, slider validation)
```

**Práce se statickými soubory:**

```html
<!-- V šabloně -->
<link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
<script src="{{ url_for('static', filename='js/main.js') }}"></script>

<!-- CSS vč. severity barev -->
:root {
    --severity-1: #2ecc71;  /* Zelená - Zanedbatelná */
    --severity-2: #f39c12;  /* Oranž - Nízká */
    --severity-3: #e67e22;  /* Oranž-červená - Střední */
    --severity-4: #e74c3c;  /* Červená - Vysoká */
    --severity-5: #2c3e50;  /* Černá - Kritická */
}
```

### Zpracování dat z formuláře

```python
# app/routes.py - POST /events/submit

if request.method == "POST":
    title = request.form.get("title")
    severity = int(request.form.get("severity"))
    
    # Validace
    if not title or severity < 1 or severity > 5:
        return render_template("submit_event.html", 
                             error="Vyplň všechna pole!")
    
    # Vytvoř event
    event = CrisisEvent(
        title=title,
        severity=severity,
        ...
    )
    
    # Ulož do DB
    event_id = app.db.create_event(event)
    
    return redirect(url_for("events.view_all"))
```

**HTML formulář:**

```html
<form method="POST">
    <input type="text" name="title" required>
    <textarea name="description" required></textarea>
    <input type="range" name="severity" min="1" max="5" value="1">
    <select name="type" required>
        {% for t in crisis_types %}
            <option value="{{ t }}">{{ t }}</option>
        {% endfor %}
    </select>
    <button type="submit">Odeslat</button>
</form>
```

**JavaScript validace (slider musí být kliknut):**

```javascript
// submit_event.html
const severitySlider = document.getElementById('severity');
severitySlider.setAttribute('data-touched', 'false');

severitySlider.addEventListener('input', function() {
    this.setAttribute('data-touched', 'true');
});

document.querySelector('form').addEventListener('submit', function(e) {
    if (severitySlider.getAttribute('data-touched') === 'false') {
        e.preventDefault();
        alert('Musíš kliknout na posuvník!');
    }
});
```

### REST API a CRUD mapování

KrizeMapa používá REST principy:

| CRUD | HTTP | Endpoint | Endpoint (alternativa) |
|------|------|----------|------------------------|
| **Create** | POST | `/events/submit` | `/api/events` |
| **Read** | GET | `/events/view` + `/<id>` | `/api/events` + `/<id>` |
| **Update** | PUT/PATCH | ❌ Není | `/api/events/<id>` |
| **Delete** | DELETE/POST | `/events/<id>/delete` | `/api/events/<id>` |

**REST API struktura (by měla být):**

```
GET  /api/events         → seznam
GET  /api/events/1       → detail
POST /api/events         → vytvoř
PUT  /api/events/1       → uprav
DELETE /api/events/1     → smaž
```

V KrizeMapa máme **HTML forms** (ne pure REST), ale koncept je stejný.

---

## Shrnutí: Co je v KrizeMapa implementováno vs co chybí

| Téma | Implementováno | Chybí |
|------|--------|------|
| **0) NoSQL definice** | ✅ | ❌ |
| **1) SQL vs NoSQL** | ✅ Hybrid | ❌ Normalizace |
| **2) Škálování** | ⚠️ Partial | ❌ Load balancer |
| **3) CAP teorém** | ✅ AP systém | ❌ Formal analysis |
| **4) ACID vs BASE** | ✅ BASE model | ❌ Transakcí |
| **5) Sharding** | ❌ Single shard | ❌ Replikace |
| **6) Replikace** | ❌ Single node | ❌ Failover |
| **7) NoSQL typy** | ✅ Key-Value + Document | ❌ Wide-column, Graph |
| **8) Redis** | ✅ Cache + TTL | ❌ Pub/Sub |
| **9) MongoDB** | ✅ Dokumenty | ❌ Pipelines |
| **10) Cassandra/HANA** | ❌ | ❌ |
| **11) Neo4j** | ❌ | ❌ |
| **12) Big Data/ETL** | ⚠️ Architektura | ❌ OLAP |
| **13) Flask** | ✅✅✅ Kompletní | ⚠️ Pure REST API |

---

## Závěr

KrizeMapa je **realistická webová aplikace** postavená na principech NoSQL a Flask. Aplikace **demonstruje:**

✅ **Silné stránky:**
- Dokumentová DB (MongoDB) s flexibilním schématem
- Cache layer (Redis) pro výkon
- Graceful degradation (funguje i bez DB)
- REST-like rozhraní s formuláři
- Responsive frontend (HTML/CSS/JS)
- Docker orchestration

⚠️ **Okrajové:**
- Bez replikace/shardings (single node)
- Bez agregačních pipelines (jednoduché dotazy)
- Bez formálního REST API (HTML forms)
- Bez transakcí (BASE model)

❌ **Chybí pro produkci:**
- Autentifikace/autorizace
- Validace na backend straně (jen frontend)
- Unit testy
- Load testing
- Monitoring/logging
- HTTPS

Ale **pro semestrální projekt** je to **akademicky správný a prakticky použitelný** proof-of-concept!
