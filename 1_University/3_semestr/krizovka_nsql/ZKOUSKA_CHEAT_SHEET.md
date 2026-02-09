# KrizeMapa - Zkoušková příprava (Cheat Sheet)

Rychlý tahák na zkoušku - jak odpovídět o KrizeMapa.

---

## 1. CAP teorém - Co je KrizeMapa?

**Otázka:** "Jaký CAP má vaše aplikace?"

**Odpověď:**
```
KrizeMapa = AP systém (Availability + Partition tolerance)

- Availability ✅: Aplikace vrátí odpověď (i bez DB)
- Partition ✅: Funguje i když Redis padne (čte z Mongo)
- Consistency ❌: Redis cache může být 5 minut stará
```

**Příklad:**
```
1. User A hlásí krizi v 10:00
2. Data se uloží do MongoDB
3. Redis cache se invaliduje
4. User B hned vidí novou krizi (eventual consistency)
5. Po 5 minutách i Redis zapomene starou verzi
```

---

## 2. ACID vs BASE - Co vám chybí?

**Otázka:** "Proč nemáte ACID?"

**Odpověď:**
```
ACID = SQL (chcete konsistenci vždy)
BASE = NoSQL (přijmete dočasné nekonzistence)

KrizeMapa je BASE:
- BA ✅: Aplikace běží (even bez Mongo)
- S ✅: Redis cache má "soft state" (5 min TTL)
- E ✅: Eventual consistency - po 5 min jsou data stejná
```

**Praktický prípad:**
```
Zápis krize:
  1. MongoDB <- ulož (hned durable)
  2. Redis <- invaliduj cache
  3. User <- vrať potvrzení

Když Redis selhá v kroku 2:
  ❌ Cache není invalidován
  ✅ Ale data v Mongo jsou OK
  ✅ Za 5 minut se cache obnoví (eventual)
```

---

## 3. Sharding & Replikace - Co máte?

**Otázka:** "Jak máte rozděljena data?"

**Odpověď:**
```
❌ Sharding: NEMÁTE (jen 1 MongoDB uzel)
❌ Replikace: NEMÁTE (jen 1 kopie dat)

Máte:
✅ Redis cache (in-memory, rychlé)
✅ MongoDB persistent (na disku, durabilní)

Kdyby jste měli 3 MongoDB nody:
  PRIMARY (write) -> REPLICA 1 (read) -> REPLICA 2 (read+failover)
```

---

## 4. Kvórum - Nepoužíváte?

**Otázka:** "Máte kvórum?"

**Odpověď:**
```
❌ NE. Kvórum vyžaduje 3+ uzly.

Teď máte: 1 MongoDB uzel = nemůžete mít kvórum.

Kdybych měl 3 repiky:
  N = 3
  W = 2 (zápis musí potvrdit 2 uzly)
  R = 2 (čtení z 2 uzlů)
  
  Garantuje: W + R > N (2 + 2 > 3)
  Efekt: čtení se "potká" s posledním zápisem
```

---

## 5. Flask - Jaké máte endpointy?

**Otázka:** "Jakých 8 máte HTTP endpointů?"

**Odpověď:**

| Metoda | Endpoint | Funkce |
| - | - | - |
| GET | `/` | Dashboard (statistika) |
| GET | `/health` | Health check (Mongo + Redis) |
| GET | `/events/submit` | Vrť formulář |
| POST | `/events/submit` | Přijmi a ulož krizi |
| GET | `/events/view` | Paginated seznam |
| GET | `/events/<id>` | Detail jedné krize |
| POST | `/events/<id>/delete` | Smaž krizi |
| - | - | (8. neexistuje - máte 7) |

---

## 6. Validace - Severity Slider

**Otázka:** "Jak zajistíte, aby user pohýbal sliderem?"

**Odpověď:**

```javascript
// JavaScript validace:
- Defaultní hodnota: 1 (Zanedbatelná)
- Slider má data-touched="false" na začátku
- Když user klikne na slider -> data-touched="true"
- Při submitu: pokud data-touched="false" -> blokuj odeslání!
```

**Efekt:**
✅ Uživatel MUSÍ kliknout na slider  
❌ Jinak dostane chybu: "Klikni na posuvník!"

---

## 7. MongoDB vs Redis

**Otázka:** "Proč máte obě databáze?"

**Odpověď:**

```
MongoDB = persistent storage (na disku)
- Durabilita: data zůstanou i po restartu
- Pomalost: disk je pomalý (ms)

Redis = cache (v paměti)
- Rychlost: ultra fast (µs)
- Dočasnost: zrušit po restartu
- TTL: auto-delete po 5 minutách

Workflow:
  1. GET /events -> zkontroluj Redis
  2. Hit? Vrať (super rychle)
  3. Miss? Načti z Mongo, ulož do Redis, vrať
  4. Po 5 min? Cache expiruje, příští request -> cache miss
```

---

## 8. Graceful Degradation

**Otázka:** "Co se stane, když MongoDB padne?"

**Odpověď:**

```python
try:
    db = DatabaseManager(mongo_uri, redis_url, db_name)
    app.db = db
except Exception as e:
    app.db = None  # <-- POKRAČUJ BEZ DB!
```

**Efekt:**
```
MongoDB DOWN:
✅ Aplikace běží
❌ Dashboard bez dat (0 krizí)
❌ Nelze hlásit krizi
✅ Error message: "Databáze není dostupná"

Redis DOWN:
✅ Čtení z Mongo (jen pomaleji)
❌ Cache nepoužívá
✅ Všechno funguje, jen E > milliseconds
```

---

## 9. Data Model - CrisisEvent

**Otázka:** "Jaké pole má crisis event?"

**Odpověď:**

```json
{
    "_id": "ObjectId(...)",      // MongoDB auto-generuje
    "title": "Požár v BCP",      // Název
    "description": "Velkej fuu", // Popis
    "location": "Praha",         // Místo
    "severity": 4,               // 1-5 (validace!)
    "type": "požár",             // Z CRISIS_TYPES enum
    "latitude": 50.0827,         // GPS (optional)
    "longitude": 14.4385,        // GPS (optional)
    "created_at": "2026-02-09T10:30:00Z"  // timestamp
}
```

**CRISIS_TYPES** (8 typů):
```python
1. přírodní_katastrofa
2. dopravní_nehoda
3. požár
4. zdravotnické_nouzové
5. průmyslová_havárie
6. teroristický_útok
7. únos
8. ostatní
```

---

## 10. REST API vs HTML Forms

**Otázka:** "Máte REST API?"

**Odpověď:**

```
Čistě REST by byl:
  POST /api/events          (vytvoř)
  GET  /api/events          (seznam)
  GET  /api/events/{id}     (detail)
  DELETE /api/events/{id}   (smaž)

KrizeMapa má:
  POST /events/submit       (HTML form - ne REST)
  GET  /events/view         (HTML stránka)
  GET  /events/{id}         (HTML stránka)
  POST /events/{id}/delete  (HTML form, ne pure DELETE)

Rozdíl:
- REST = pure JSON endpoints (bez HTML)
- KrizeMapa = HTML forms + Jinja2 šablony
```

---

## 11. Škálování

**Otázka:** "Můžete horizontálně škálovat?"

**Odpověď:**

```
Teď: 1 Flask + 1 Redis + 1 Mongo (scale-up limited)

Ideálně:
  nginx (load balancer)
    ├─ Flask 1
    ├─ Flask 2
    └─ Flask 3
  
  Redis Cluster (3 nody)
  MongoDB Replica Set (3 nody)
```

**Problém bez toho:**
- Flask: single point of failure
- Redis: single point of failure
- Mongo: single point of failure

---

## 12. Jak odpovědět "KOMPLETNĚ"?

**Ukázkový dialog:**

Q: "Vysvětlete CAP teorém a jak se to týka vaší aplikace."

A: 
```
CAP teorém říká, že v distribuovaném systému
nemůžete mít všechny 3 vlastnosti najednou:
- C: Consistency (data jsou vždy aktuální)
- A: Availability (systém vždy odpoví)
- P: Partition tolerance (funguje i při výpadku sítě)

KrizeMapa je AP systém:
- Máme AVAILABILITY: Flask vrátí odpověď i bez Mongo
- Máme PARTITION: Redis + Mongo = redundance
- NEMÁME CONSISTENCY: Redis cache je 5 minut stará

Praktické důsledky:
1. Když MongoDB padne -> zobrazí se 0 krizí (ale app běží)
2. Když Redis padne -> čteme z Mongo (pomalejší, ale bezpečné)
3. Když hlásím krizi -> za 5 minut se cache obnoví (eventual consistency)
```

---

## 13. Rychlý tahák - KOPÍRUJ A DRŽ V HLAVĚ

```
KrizeMapa:
✅ MongoDB (dokumenty) + Redis (cache) + Flask (web)
✅ 7 HTTP endpointů (get, post, delete)
✅ Jinja2 šablony + CSS responsive
✅ Docker (mongo + redis + flask)
✅ BASE model (ne ACID)
✅ AP CAP (ne C)
✅ Cache invalidace
✅ Graceful degradation
✅ Severity slider validation

❌ Žádné sharding
❌ Žádná replikace
❌ Žádný kvórum
❌ Žádné aggregation pipelines
❌ Žádný REST API (jen HTML forms)
❌ Žádná autentifikace
```

---

## 14. Jak NEJLÉPE odpovídět

**Klíč k zkoušce:**

1. **Definuj slovo** - co znamená "sharding"?
2. **Dej příklad** - jak by fungoval v KrizeMapa?
3. **Řekni implementaci** - to máte? To nemáte?
4. **Ukaž kód** - zde je konkrétní řádka z app/db.py

**Např.:**

Q: "Co je eventual consistency?"

A:
```
Eventual consistency = data se po čase srovnají (ne hned)

Definice:
  Při distribuovaném systému nejsou data hned konzistentní,
  ale po určitém čase se všechny uzly srovnají.

Příklad v KrizeMapa:
  1. User hlásí krizi (čas 10:00)
  2. MongoDB ji zapíše (hned durable)
  3. Redis cache se invaliduje
  4. User B v 10:00:01 čte seznam -> vidí novou krizi
  5. Jiný systém, který čte z Redis cache -> nevidí (stará cache)
  6. Po 5 minutách (10:05) -> cache expiruje -> vidí

BASE model (KrizeMapa):
  BA - Basically Available ✓
  S - Soft state ✓ (Redis cache je "měkký stav")
  E - Eventual consistency ✓ (po 5 min stejná data)
```

---

## 15. Nejčastější otázky na zkoušce

### 1. "CAP - jaký máte vy?"
→ AP (availability + partition), ne consistency

### 2. "ACID vs BASE"
→ BASE = pro distribuované systémy, přijímáme dočasné nekonzistence

### 3. "Sharding - proč nemáte?"
→ Máme jen 1 MongoDB uzel, sharding potřebuje 3+

### 4. "Redis vs Mongo - k čemu vám to?"
→ Redis cache (paměť, rychle) + Mongo persistent (disk, durabilní)

### 5. "Když Mongo padne?"
→ Graceful degradation - app běží, ale bez dat

### 6. "Jaké máte endpointy?"
→ Jmenuj: GET /, GET /health, GET/POST /events/submit, GET /events/view, GET/POST /events/<id>, POST /events/<id>/delete

### 7. "Flask - co je to blueprint?"
→ Modulární struktura routů (main_bp, events_bp)

### 8. "Validace - jak slider?"
→ JavaScript: data-touched="false" -> musí kliknout -> true

### 9. "TTL - co to je?"
→ Time To Live = cache se auto-smaže po X sekundách (5 min v KrizeMapa)

### 10. "Kvórum - máte?"
→ Ne, potřebujete 3+ MongoDB uzly, máte jen 1

---

**DOBROU ZKOUŠKU! 💪**
