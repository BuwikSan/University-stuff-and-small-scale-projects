# Models.py - Struktura JSON a Přidání Nového Sloupce

## 📊 SOUČASNÁ STRUKTURA JSON DOKUMENTU

```json
{
    "_id": ObjectId("507f1f77bcf86cd799439011"),
    "title": "Požár v obchodním centru",
    "description": "Vypukl požár v areálu centra",
    "location": "Praha, Václavské náměstí",
    "severity": 4,
    "type": "požár",
    "latitude": 50.0827,
    "longitude": 14.4385,
    "created_at": ISODate("2026-02-09T10:30:00Z")
}
```

---

## 🔍 ROZBOR KAŽDÉHO POLE

| Pole | Typ | Povinné? | Popis | Příklad |
|------|-----|---------|-------|---------|
| `_id` | ObjectId | ✅ | MongoDB auto-generuje | `ObjectId("...")` |
| `title` | String | ✅ | Název krize | `"Požár v obchodním centru"` |
| `description` | String | ✅ | Detailní popis | `"Vypukl požár v areálu..."` |
| `location` | String | ✅ | Místo (text nebo GPS) | `"Praha, Václavské náměstí"` |
| `severity` | Integer | ✅ | Stupeň závažnosti 1-5 | `4` |
| `type` | String | ✅ | Typ krize z CRISIS_TYPES | `"požár"` |
| `latitude` | Float | ❌ | GPS zeměpisná šířka | `50.0827` |
| `longitude` | Float | ❌ | GPS zeměpisná délka | `14.4385` |
| `created_at` | DateTime | ✅ | Čas hlášení | `ISODate("2026-02-09T10:30:00Z")` |

---

## 📝 JAK SE PŘIDÁVÁ NOVÝ SLOUPEC (FIELD)

Chceš přidat `expired: boolean` (jestli je krize vyřešená)

### **KROK 1: Uprav `__init__` metodu**

**PŘED:**
```python
def __init__(
    self,
    title: str,
    description: str,
    location: str,
    severity: int,
    event_type: str,
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
    _id: Optional[str] = None,
    created_at: Optional[datetime] = None,
):
```

**PO (s `expired`):**
```python
def __init__(
    self,
    title: str,
    description: str,
    location: str,
    severity: int,
    event_type: str,
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
    _id: Optional[str] = None,
    created_at: Optional[datetime] = None,
    expired: bool = False,  # ← NOVÝ PARAMETR (default False)
):
```

### **KROK 2: Přidej atribut do těla __init__**

**PŘED:**
```python
self.title = title
self.description = description
self.location = location
self.severity = min(5, max(1, severity))  # 1-5
self.event_type = event_type
self.latitude = latitude
self.longitude = longitude
self._id = _id
self.created_at = created_at or datetime.now()
```

**PO:**
```python
self.title = title
self.description = description
self.location = location
self.severity = min(5, max(1, severity))  # 1-5
self.event_type = event_type
self.latitude = latitude
self.longitude = longitude
self._id = _id
self.created_at = created_at or datetime.now()
self.expired = expired  # ← NOVÝ ATRIBUT
```

### **KROK 3: Přidej do `to_dict()` metody**

**PŘED:**
```python
def to_dict(self) -> Dict[str, Any]:
    """Konvertuj na dict pro MongoDB"""
    doc = {
        "title": self.title,
        "description": self.description,
        "location": self.location,
        "severity": self.severity,
        "type": self.event_type,
        "latitude": self.latitude,
        "longitude": self.longitude,
        "created_at": self.created_at,
    }
    if self._id is not None:
        doc["_id"] = self._id
    return doc
```

**PO:**
```python
def to_dict(self) -> Dict[str, Any]:
    """Konvertuj na dict pro MongoDB"""
    doc = {
        "title": self.title,
        "description": self.description,
        "location": self.location,
        "severity": self.severity,
        "type": self.event_type,
        "latitude": self.latitude,
        "longitude": self.longitude,
        "created_at": self.created_at,
        "expired": self.expired,  # ← NOVÝ
    }
    if self._id is not None:
        doc["_id"] = self._id
    return doc
```

### **KROK 4: Přidej do `from_dict()` metody**

**PŘED:**
```python
@staticmethod
def from_dict(data: Dict[str, Any]) -> "CrisisEvent":
    """Vytvoř CrisisEvent z dict (z MongoDB)"""
    if isinstance(data.get("created_at"), str):
        created_at = datetime.fromisoformat(data["created_at"])
    else:
        created_at = data.get("created_at")
    
    return CrisisEvent(
        title=data.get("title"),
        description=data.get("description"),
        location=data.get("location"),
        severity=data.get("severity", 1),
        event_type=data.get("type", "other"),
        latitude=data.get("latitude"),
        longitude=data.get("longitude"),
        _id=data.get("_id"),
        created_at=created_at,
    )
```

**PO:**
```python
@staticmethod
def from_dict(data: Dict[str, Any]) -> "CrisisEvent":
    """Vytvoř CrisisEvent z dict (z MongoDB)"""
    if isinstance(data.get("created_at"), str):
        created_at = datetime.fromisoformat(data["created_at"])
    else:
        created_at = data.get("created_at")
    
    return CrisisEvent(
        title=data.get("title"),
        description=data.get("description"),
        location=data.get("location"),
        severity=data.get("severity", 1),
        event_type=data.get("type", "other"),
        latitude=data.get("latitude"),
        longitude=data.get("longitude"),
        _id=data.get("_id"),
        created_at=created_at,
        expired=data.get("expired", False),  # ← NOVÝ (default False pokud chybí)
    )
```

---

## 📦 NOVÝ JSON DOKUMENT S `expired`

```json
{
    "_id": ObjectId("507f1f77bcf86cd799439011"),
    "title": "Požár v obchodním centru",
    "description": "Vypukl požár v areálu centra",
    "location": "Praha, Václavské náměstí",
    "severity": 4,
    "type": "požár",
    "latitude": 50.0827,
    "longitude": 14.4385,
    "created_at": ISODate("2026-02-09T10:30:00Z"),
    "expired": false  # ← NOVÉ POLE (boolean)
}
```

---

## 🔄 CO SE DĚJE V APLIKACI

### **1. Vytvoření krize s `expired`:**
```python
# V routes.py při submit_event
event = CrisisEvent(
    title="Požár v obchodním centru",
    description="Vypukl požár...",
    location="Praha",
    severity=4,
    event_type="požár",
    expired=False  # ← Nová krize není vyřešená
)
```

### **2. Uložení do MongoDB:**
```python
# V db.py create_event()
event_dict = event.to_dict()
# to_dict() nyní vrátí:
{
    "title": "Požár...",
    ...
    "expired": False  # ← Uloží se do DB
}

result = collection.insert_one(event_dict)
```

### **3. Čtení z MongoDB:**
```python
# V db.py get_event()
event_dict = collection.find_one({"_id": ObjectId(event_id)})
# event_dict obsahuje:
{
    "title": "Požár...",
    ...
    "expired": False  # ← Přečte se z DB
}

event = CrisisEvent.from_dict(event_dict)
# from_dict() vytvoří CrisisEvent s expired=False
```

### **4. Použití v HTML šablonách:**
```html
<!-- V event_detail.html -->
{% if event.expired %}
    <span class="badge badge-success">✅ Vyřešeno</span>
{% else %}
    <span class="badge badge-danger">🚨 Aktivní</span>
{% endif %}
```

---

## ✅ CHECKLIST - CO VŠECHNO MUSÍŠ ZMĚNIT

Když přidáš nový field `expired: bool`:

- [ ] ✅ Přidej parametr do `__init__(self, ..., expired: bool = False)`
- [ ] ✅ Přidej `self.expired = expired` do těla `__init__`
- [ ] ✅ Přidej `"expired": self.expired` do `to_dict()`
- [ ] ✅ Přidej `expired=data.get("expired", False)` do `from_dict()`
- [ ] ✅ (VOLITELNÉ) Aktualizuj docstring modelu
- [ ] ✅ (VOLITELNÉ) Aktualizuj šablony aby pokazovaly `expired` status
- [ ] ✅ Testuj: `docker-compose restart web`

---

## 🧪 OVĚŘENÍ - JAK TESTOVAT

### **V Pythonu (command line):**
```python
from app.models import CrisisEvent

# Vytvoř event s expired
event = CrisisEvent(
    title="Test",
    description="Test",
    location="Praha",
    severity=3,
    event_type="požár",
    expired=True  # ← Nastavíme na True
)

# Konvertuj na dict
d = event.to_dict()
print(d)
# Output: {..., "expired": True, ...}

# Konvertuj zpátky
event2 = CrisisEvent.from_dict(d)
print(event2.expired)  # Output: True
```

### **V MongoDB (command line):**
```javascript
// Zkontroluj, že nové dokumenty mají expired pole
db.events.findOne()

// Output:
{
    _id: ObjectId("..."),
    title: "Požár...",
    ...
    expired: false
}
```

---

## 📝 SOUHRN

**Když chceš přidat JAKÝKOLI nový field:**

1. **`__init__` - přidej parametr** (s default hodnotou)
2. **`__init__` - přidej `self.pole = pole`**
3. **`to_dict()` - přidej `"pole": self.pole`**
4. **`from_dict()` - přidej `pole=data.get("pole", default)`**
5. **Testuj!**

**To je všechno!** MongoDB je flexibilní - nemusíš migrovat DB schéma.

---

## 🎓 OTÁZKY NA TEBE

1. **Co je `Optional[float]`?** (hint: `None` je povolená hodnota)
2. **Proč je v `to_dict()` řádek `if self._id is not None:`?** (hint: MongoDB si generuje _id)
3. **Jaký je rozdíl mezi `data.get("pole")` a `data["pole"]`?** (hint: KeyError)
4. **Když přidám nový field, co se stane se STARÝMI dokumenty v DB?** (hint: nic, mají starou strukturu, ale aplikace to řeší)

Odpověz si a pak vejdeme na **DB.PY**! 🚀
