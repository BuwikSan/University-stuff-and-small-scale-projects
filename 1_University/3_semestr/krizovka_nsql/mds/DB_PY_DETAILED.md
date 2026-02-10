# db.py - Podrobné Vysvětlení

## 📚 STRUKTURA (286 řádků)

```
Imports (1-13)
  ↓
DatabaseManager class (18-286)
  ├─ __init__ (21-29) - Inicializace
  ├─ @property mongo (31-48) - Lazy-load MongoDB
  ├─ @property redis (50-62) - Lazy-load Redis
  ├─ @property db (64-69) - Přístup k DB
  ├─ get_collection (71-73) - Vrať MongoDB kolekci
  ├─ clear_all_events (76-89) - Smaž všechny eventy
  ├─ create_event (91-107) - Vytvoř nový event
  ├─ get_event (109-123) - Načti event podle ID
  ├─ get_all_events (125-173) - Načti všechny (s cachováním)
  ├─ get_events_by_severity (175-189) - Filtruj podle závažnosti
  ├─ count_events (191-213) - Počet eventů (s cachováním)
  ├─ count_today_events (215-246) - Dnešní eventy
  ├─ delete_event (248-262) - Smaž event
  ├─ _invalidate_events_cache (264-269) - Vymaž cache
  └─ health_check (271-286) - Ověř spojení
```

---

## 🔌 IMPORTS

```python
from typing import List, Dict, Any, Optional  # Type hints
from datetime import datetime                  # Pro created_at
import json                                    # Serialization
import logging                                 # Logování

from pymongo import MongoClient, DESCENDING   # MongoDB driver
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
import redis                                   # Redis cache

from .models import CrisisEvent                # Náš datový model
```

---

## 🏗️ ARCHITEKTURA: 2 DATABÁZE

```
┌─────────────────────────────────────────────────────────┐
│           DatabaseManager (Správce dat)                 │
├──────────────────┬──────────────────────────────────────┤
│                  │                                      │
│   MongoDB        │           Redis Cache                │
│  (Persistent)    │        (In-Memory)                   │
│                  │                                      │
│ ✓ Trvalý úklod   │  ✓ Rychlý přístup                   │
│ ✓ Zapytování     │  ✓ 5 minut TTL (auto-delete)        │
│ ✓ Filtrování     │  ✓ Invalidace na create/delete       │
│                  │                                      │
└──────────────────┴──────────────────────────────────────┘
```

---

## 🔧 LAZY LOADING - KLÍČOVÝ KONCEPT!

```python
def __init__(self, mongo_uri: str, redis_url: str, db_name: str):
    self.mongo_uri = mongo_uri
    self.redis_url = redis_url
    self.db_name = db_name
    
    # ZATÍM NIČEHO NEINICIALIZUJEME!
    self._mongo_client: Optional[MongoClient] = None
    self._redis_client: Optional[redis.Redis] = None
    self._db = None
```

**Co to znamená:**
- `self._mongo_client = None` → MongoDB není připojen
- Připojíme se až když si ho První zažádáme
- = Heší startup aplikace (všechna připojení se dějí asynchroně)

### **Příklad:**
```python
db = DatabaseManager(mongo_uri, redis_url, "krizove_udalosti")
# Zatím nic - MongoDB/Redis nevíme

event = db.get_event("123")
# TEĎ se poprvé připojí k MongoDB (lazy load)
```

---

## 🔗 LAZY-LOAD MONGODB

```python
@property
def mongo(self) -> MongoClient:
    """Lazy-load MongoDB connection"""
    if self._mongo_client is None:  # Pokud ještě není připojen
        try:
            # Připoj se s 5-sekundovým timeoutem
            self._mongo_client = MongoClient(self.mongo_uri, serverSelectionTimeoutMS=5000)
            
            # TEST: Zda je MongoDB online
            self._mongo_client.server_info()
            
            # Připoj se k databázi
            self._db = self._mongo_client[self.db_name]
            
            logger.info(f"✓ Připojen k MongoDB: {self.db_name}")
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            logger.error(f"✗ MongoDB spojení selhalo: {e}")
            self._mongo_client = None
            raise
    return self._mongo_client
```

**Co se děje:**
1. Když voláš `db.mongo`, Python zkontroluje `if self._mongo_client is None`
2. Pokud je `None`, vytvoří nové spojení
3. Zavolá `server_info()` = ověří že MongoDB běží
4. Pokud selhá → log error + vyhodí exception

**Chyby:**
- `ConnectionFailure` = MongoDB není dostupný
- `ServerSelectionTimeoutMS=5000` = maximálně 5 sekund čekání

---

## 🔗 LAZY-LOAD REDIS

```python
@property
def redis(self) -> redis.Redis:
    """Lazy-load Redis connection"""
    if self._redis_client is None:
        try:
            # Připoj se z URL (redis://localhost:6379/0)
            self._redis_client = redis.from_url(self.redis_url, decode_responses=True)
            
            # TEST: ping
            self._redis_client.ping()
            
            logger.info("✓ Připojen k Redis")
        except Exception as e:
            logger.error(f"✗ Redis spojení selhalo: {e}")
            self._redis_client = None
            raise
    return self._redis_client
```

**Klíčový parametr:**
- `decode_responses=True` = vrací stringy místo bytes
- Jinak by bylo: `b"hello"` místo `"hello"`

---

## 📊 PŘÍSLUŠNÁ METODA: GET COLLECTION

```python
def get_collection(self, name: str):
    """Vrať MongoDB kolekci"""
    return self.db[name]
```

**Příklad:**
```python
events_collection = db.get_collection("events")
# = db._db["events"]

users_collection = db.get_collection("users")
# = db._db["users"]
```

---

## 🔨 OPERACE S EVENTS

### **1. CLEAR_ALL_EVENTS - Smaž vše**

```python
def clear_all_events(self) -> int:
    """Smaž VŠECHNY eventy z databáze. Vrátí počet smazaných."""
    try:
        collection = self.get_collection("events")
        result = collection.delete_many({})  # {} = všechny dokumenty
        
        # Invaliduj všechny cache
        self._invalidate_events_cache()
        self.redis.delete("events:today")
        
        logger.info(f"✓ Smazáno {result.deleted_count} eventů")
        return result.deleted_count
    except Exception as e:
        logger.error(f"✗ Chyba: {e}")
        raise
```

**Rozklad:**
- `delete_many({})` = smaž všechny dokumenty
- Vrátí `result.deleted_count` = kolik bylo smazaných
- Invaliduje cache = další `.get_all_events()` přečte z DB

**Příklad:**
```python
deleted = db.clear_all_events()
print(deleted)  # Output: 17 (smazáno 17 eventů)
```

---

### **2. CREATE_EVENT - Vytvoř nový event**

```python
def create_event(self, event: CrisisEvent) -> str:
    """Vytvoř novou crisis event. Vrátí event ID."""
    try:
        collection = self.get_collection("events")
        event_dict = event.to_dict()  # CrisisEvent → dict
        result = collection.insert_one(event_dict)  # Ulož do MongoDB
        
        # Invaliduj cache
        self._invalidate_events_cache()
        
        logger.info(f"✓ Event vytořen: {result.inserted_id}")
        return str(result.inserted_id)
    except Exception as e:
        logger.error(f"✗ Chyba: {e}")
        raise
```

**Rozklad:**
1. `event.to_dict()` = konvertuj CrisisEvent na dict (viz models.py)
2. `insert_one(event_dict)` = vlož do MongoDB
3. MongoDB automaticky generuje `_id` (ObjectId)
4. `result.inserted_id` = vrať MongoDB ID
5. Vymaž cache (`events:all`, `events:count`) aby se příště přečetlo z DB

**Příklad:**
```python
event = CrisisEvent(
    title="Požár",
    description="...",
    location="Praha",
    severity=4,
    event_type="požár"
)
event_id = db.create_event(event)
print(event_id)  # Output: "507f1f77bcf86cd799439011" (string!)
```

---

### **3. GET_EVENT - Načti event podle ID**

```python
def get_event(self, event_id: str) -> Optional[CrisisEvent]:
    """Vrať event podle ID"""
    try:
        from bson.objectid import ObjectId
        collection = self.get_collection("events")
        event_dict = collection.find_one({"_id": ObjectId(event_id)})
        if event_dict:
            return CrisisEvent.from_dict(event_dict)
        return None
    except Exception as e:
        logger.error(f"✗ Chyba: {e}")
        return None
```

**Rozklad:**
1. `ObjectId(event_id)` = konvertuj string na ObjectId (MongoDB formát)
2. `find_one({"_id": ObjectId(...)})` = najdi document s tím ID
3. Pokud je `None` → vrať `None` (event neexistuje)
4. Pokud existuje → `from_dict()` ho konvertuj na CrisisEvent objekt

**Příklad:**
```python
event = db.get_event("507f1f77bcf86cd799439011")
if event:
    print(event.title)  # Output: "Požár"
else:
    print("Event nenalezen")
```

---

### **4. GET_ALL_EVENTS - Nejdůležitější (s cachováním!)**

```python
def get_all_events(self, limit: int = 100, skip: int = 0) -> List[CrisisEvent]:
    """
    Vrať všechny eventy seřazené podle času (nejnovější první).
    Cache se používá jen když není pagination.
    """
    
    # KROK 1: ZKUS CACHE
    cache_key = "events:all"
    if limit == 100 and skip == 0:  # Jen pokud NENÍ pagination
        try:
            cached = self.redis.get(cache_key)
            if cached:
                data = json.loads(cached)  # Deserializuj JSON
                return [CrisisEvent.from_dict(d) for d in data]  # Vrať z cache
        except Exception as e:
            logger.warning(f"Cache failed: {e}")  # Fallback
    
    # KROK 2: POKUD CACHE SELHAL NEBO JE PAGINATION → MONGODB
    try:
        collection = self.get_collection("events")
        events_data = list(
            collection.find()                          # Najdi všechny
            .sort("created_at", DESCENDING)            # Seřaď nově → staré
            .limit(limit)                              # Omez výsledky
            .skip(skip)                                # Přeskoč
        )
        
        events = [CrisisEvent.from_dict(d) for d in events_data]
        
        # KROK 3: CACHUJ (jen bez pagination)
        if limit == 100 and skip == 0:
            try:
                self.redis.setex(
                    cache_key,
                    300,  # 5 minut TTL
                    json.dumps([e.to_dict() for e in events], default=str)
                )
            except Exception as e:
                logger.warning(f"Cache write failed: {e}")
        
        return events
    except Exception as e:
        logger.error(f"✗ Chyba: {e}")
        return []
```

**ARCHITEKTURA CACHOVÁNÍ:**

```
┌─────────────────────────────────────┐
│  Voláš: db.get_all_events()         │
├─────────────────────────────────────┤
│                                     │
│  Krok 1: limit=100 && skip=0?       │
│    ├─ ANO: Zkus Redis cache         │
│    │   ├─ Cache HIT: Vrať z Redis   │ (RYCHLE - millisekund)
│    │   └─ Cache MISS: Jdi na krok 2 │
│    └─ NE: Jdi na krok 2             │
│                                     │
│  Krok 2: Čti z MongoDB              │
│    ├─ find() všechny documenty      │ (POMALÉ - sekundy)
│    ├─ sort() od nejnovějšího        │
│    ├─ limit() max N resultů         │
│    └─ skip() přeskoč N              │
│                                     │
│  Krok 3: limit=100 && skip=0?       │
│    ├─ ANO: Cachuj do Redis na 5 min │
│    └─ NE: Necachuj                  │
│                                     │
│  Vrať CrisisEvent objekty           │
└─────────────────────────────────────┘
```

**Proč se cachuje jen bez pagination?**
- `limit=100, skip=0` = všechny events (nejtypičtější dotaz)
- `limit=10, skip=10` = page 2 (ostatní stránky se nepoužívají často)
- Cache by zabrala moc paměti

**Příklady:**
```python
# CACHE HIT (čte se z Redis za ms)
events = db.get_all_events()  # limit=100, skip=0
# Redis vrátí: [{"_id": ..., "title": "Požár", ...}, ...]

# CACHE MISS (čte se z MongoDB za sekundy)
events = db.get_all_events(limit=10, skip=0)  # Pagination
# MongoDB: find().limit(10).skip(0)
# Neukládá se do Redis

# CACHE HIT (2. volání stejného dotazu)
events = db.get_all_events()  # limit=100, skip=0
# Redis vrátí STEJNÁ data (dokud nevyprší 5 minut)
```

---

### **5. GET_EVENTS_BY_SEVERITY - Filtruj**

```python
def get_events_by_severity(self, min_severity: int = 1, max_severity: int = 5) -> List[CrisisEvent]:
    """Vrať eventy určitého stupně závažnosti"""
    try:
        collection = self.get_collection("events")
        events_data = list(
            collection.find(
                {"severity": {"$gte": min_severity, "$lte": max_severity}}
            )
            .sort("created_at", DESCENDING)
        )
        return [CrisisEvent.from_dict(d) for d in events_data]
    except Exception as e:
        logger.error(f"✗ Chyba: {e}")
        return []
```

**MongoDB query:**
- `$gte` = greater than or equal (≥)
- `$lte` = less than or equal (≤)
- `{"severity": {"$gte": 3, "$lte": 5}}` = severity 3, 4 nebo 5

**Příklad:**
```python
# Jen kritické (severity 4-5)
critical = db.get_events_by_severity(4, 5)

# Všechny (severity 1-5)
all = db.get_events_by_severity(1, 5)
```

---

### **6. COUNT_EVENTS - Počet (s cachováním)**

```python
def count_events(self) -> int:
    """Vrať počet všech eventů"""
    try:
        # Zkus cache
        cache_key = "events:count"
        try:
            cached = self.redis.get(cache_key)
            if cached:
                return int(cached)  # Vrať z cache
        except:
            pass  # Pokud cache selže, pokračuj
        
        # Jdi do MongoDB
        collection = self.get_collection("events")
        count = collection.count_documents({})
        
        # Cachuj na 5 minut
        try:
            self.redis.setex(cache_key, 300, str(count))
        except:
            pass
        
        return count
    except Exception as e:
        logger.error(f"✗ Chyba: {e}")
        return 0
```

**Klíčový formát:**
- `redis.setex(key, ttl, value)` = set + expire
- `ttl=300` = 5 minut

---

### **7. COUNT_TODAY_EVENTS - Dnešní (s date range queryem)**

```python
def count_today_events(self) -> int:
    """Vrať počet eventů hlášených dnes"""
    try:
        # Zkus cache
        cache_key = "events:today"
        try:
            cached = self.redis.get(cache_key)
            if cached:
                return int(cached)
        except:
            pass
        
        # Spočítej od PŮLNOCI
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start + timedelta(days=1)  # Zítra v 00:00
        
        # MongoDB query: created_at >= dnešní 00:00 AND created_at < zítra 00:00
        collection = self.get_collection("events")
        count = collection.count_documents({
            "created_at": {
                "$gte": today_start,
                "$lt": today_end
            }
        })
        
        # Cachuj na 5 minut
        try:
            self.redis.setex(cache_key, 300, str(count))
        except:
            pass
        
        return count
    except Exception as e:
        logger.error(f"✗ Chyba: {e}")
        return 0
```

**Datetime logika:**
```python
# Pokud je teď 2026-02-09 14:30:45
today_start = datetime(2026, 2, 9, 0, 0, 0, 0)      # 2026-02-09 00:00:00
today_end = datetime(2026, 2, 10, 0, 0, 0, 0)       # 2026-02-10 00:00:00

# Query hledá: 2026-02-09 00:00:00 ≤ created_at < 2026-02-10 00:00:00
# = Všechny events hlášené DNES (během dne)
```

---

### **8. DELETE_EVENT - Smaž**

```python
def delete_event(self, event_id: str) -> bool:
    """Smaž event"""
    try:
        from bson.objectid import ObjectId
        collection = self.get_collection("events")
        result = collection.delete_one({"_id": ObjectId(event_id)})
        if result.deleted_count > 0:
            self._invalidate_events_cache()  # Vymaž cache
            logger.info(f"✓ Event smazán: {event_id}")
            return True
        return False
    except Exception as e:
        logger.error(f"✗ Chyba: {e}")
        return False
```

**Logika:**
- `delete_one()` = smaž jeden dokument
- `result.deleted_count` = kolik bylo smazaných (0 nebo 1)
- Pokud smazáno: invaliduj cache

---

### **9. _INVALIDATE_EVENTS_CACHE - Vynuluj cache**

```python
def _invalidate_events_cache(self):
    """Vynuluj relevantní cache klíče"""
    try:
        self.redis.delete("events:all", "events:count")
    except Exception as e:
        logger.warning(f"Cache invalidation failed: {e}")
```

**Kdy se volá:**
1. `create_event()` → nový event → seznam se změní → invaliduj
2. `delete_event()` → event pryč → seznam se změní → invaliduj
3. `clear_all_events()` → všechno pryč → invaliduj

**Příklad:**
```
1. db.get_all_events()
   └─ Redis cache: events:all = [event1, event2, event3]

2. db.create_event(new_event)
   └─ Zavolá _invalidate_events_cache()
   └─ Redis.delete("events:all")
   └─ Cache je PRYČ

3. db.get_all_events()
   └─ Cache miss → čte se z MongoDB
   └─ Vrátí [event1, event2, event3, new_event]
   └─ Cachuje znovu do Redis
```

---

### **10. HEALTH_CHECK - Ověř spojení**

```python
def health_check(self) -> Dict[str, bool]:
    """Ověř připojení ke všem databázím"""
    result = {"mongo": False, "redis": False}
    
    try:
        self.mongo.server_info()
        result["mongo"] = True
    except:
        pass
    
    try:
        self.redis.ping()
        result["redis"] = True
    except:
        pass
    
    return result
```

**Vrátí:**
```python
{
    "mongo": True,   # MongoDB je dostupný
    "redis": True    # Redis je dostupný
}
```

---

## 🎯 KLÍČOVÉ KONCEPTY

| Koncept | Kde se používá | Příklad |
|---------|---|---|
| **Lazy loading** | `@property mongo`, `@property redis` | Připojí se až když je potřeba |
| **Cachování** | `get_all_events()`, `count_events()` | Redis `setex(key, 300, value)` |
| **Cache invalidation** | `_invalidate_events_cache()` | Když se změní data → smaž cache |
| **MongoDB query** | `find()`, `count_documents()` | `{"severity": {"$gte": 3}}` |
| **Pagination** | `limit()`, `skip()` | Stránkování výsledků |
| **Error handling** | Všude `try/except` | Fallback na `None` nebo `[]` |
| **Logging** | `logger.info()`, `logger.error()` | Debug + monitoring |

---

## ❓ OTÁZKY NA TEBE

1. **Co by se stalo kdyby si zkusil `db.redis` když Redis není spuštěný?**
2. **Proč se cachuje jen `limit=100 && skip=0`?**
3. **Jaký je rozdíl mezi `delete_one()` a `delete_many()`?**
4. **Co je `DESCENDING` sorting?**
5. **Jak dlouho žije cache v Redisu?**

**Odpověz si - pak na `routes.py`!** 🚀
