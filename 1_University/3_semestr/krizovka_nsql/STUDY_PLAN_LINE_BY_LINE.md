# KrizeMapa - Detailní studijní plán (Line-by-Line)

**Datum:** 9.2.2026  
**Cíl:** Úplné porozumění kódu (zápočet zítra)  
**Přístup:** Soubor po souboru, řádek po řádku, s otázkami na konci každé sekce

---

## 📚 POŘADÍ SOUBORŮ - Logické řazení

### **FÁZE 1: Datový model (co se ukládá)**
1. ✅ `app/models.py` - **CrisisEvent třída** (datová struktura)
2. ✅ `app/config.py` - **Konfigurace** (jak se připojit k DB)

### **FÁZE 2: Databázová vrstva (jak se pracuje s daty)**
3. ✅ `app/db.py` - **DatabaseManager** (MongoDB + Redis operace)

### **FÁZE 3: Web aplikace (jak se to všechno spouští)**
4. ✅ `app/__init__.py` - **Application Factory** (Flask inicializace)

### **FÁZE 4: HTTP endpointy (co vidí uživatel)**
5. ✅ `app/routes.py` - **Všech 7 endpointů** (GET, POST, DELETE)

### **FÁZE 5: Frontend (jak to vypadá)**
6. ✅ `app/templates/base.html` - **Základní šablona** (layout)
7. ✅ `app/templates/dashboard.html` - **Homepage** (statistika)
8. ✅ `app/templates/submit_event.html` - **Formulář** (vytváření)
9. ✅ `app/templates/view_events.html` - **Seznam** (pagináci)
10. ✅ `app/templates/event_detail.html` - **Detail** (jedné krize)
11. ✅ `app/static/css/style.css` - **Styling** (barvy, layout)

### **FÁZE 6: Pomocné věci**
12. ✅ `run.py` - **Entry point** (jak se aplikace spouští)
13. ✅ `app/initial_db_fill.py` - **Seed data** (testovací data)

---

## 🎯 STRUKTURA KAŽDÉ SEKCE

Každá sekce obsahuje:
```
📄 SOUBOR: XYZ.py
├─ CONTEXT: Co to dělá v aplikaci?
├─ ŘÁDKY: [X-Y] Přesná čísla řádků
├─ ANALÝZA: Řádek po řádku, s vysvětlením
├─ DIAGRAM: Vizualizace toku
└─ KONTROLNÍ OTÁZKY: 3-5 otázek na konec
```

---

## 📊 PŘEHLED SOUBORŮ (pro navigaci)

| # | Soubor | Řádky | Velikost | Složitost |
|-|-|-|-|-|
| 1 | models.py | 84 | Malý | 🟢 Jednoduchý |
| 2 | config.py | 40 | Malý | 🟢 Jednoduchý |
| 3 | db.py | 270 | Střední | 🟡 Střední |
| 4 | __init__.py | 68 | Střední | 🟡 Střední |
| 5 | routes.py | 170 | Střední | 🟡 Střední |
| 6 | base.html | 50 | Malý | 🟢 Jednoduchý |
| 7 | dashboard.html | 60 | Malý | 🟢 Jednoduchý |
| 8 | submit_event.html | 130 | Střední | 🟡 Střední |
| 9 | view_events.html | 80 | Malý | 🟢 Jednoduchý |
| 10 | event_detail.html | 60 | Malý | 🟢 Jednoduchý |
| 11 | style.css | 800 | Velký | 🟢 Jednoduchý |
| 12 | run.py | 40 | Malý | 🟢 Jednoduchý |
| 13 | initial_db_fill.py | 264 | Velký | 🟡 Střední |

**CELKEM: ~2000 řádků kódu**

---

## 🚀 JAK BUDEME POSTUPOVAT

### **Krok 1: Příprava (teď)**
- Vygeneroval jsem tento plán ✅
- Znáš pořadí souborů
- Máš všechny soubory otevřené / připravené

### **Krok 2: Učení (když řekneš "POJĎ NA MODELS.PY")**
1. Přečtu soubor řádek po řádku
2. Vysvětlím KAŽDÝ řádek
3. Dám kontextu ("proč to tady je?")
4. Budu ukazovat PŘÍKLADY

### **Krok 3: Kontrola (na konci sekce)**
- 3-5 otázek k otestování porozumění
- Ty odpovídáš
- Já potvrzuju / opravuji

### **Krok 4: Opakování (pokud nestíhá)**
- Pokud něco nechápeš → znovu to vysvětlím
- Jiným způsobem
- S více příklady

---

## 📝 COMMAND REFERENCE

Jakmile budeš připraven:
- `POJĎ NA MODELS.PY` - Začneme s datovým modelem
- `POJĎ NA CONFIG.PY` - Konfigurace
- `POJĎ NA DB.PY` - Databázová vrstva
- `POJĎ NA __INIT__.PY` - Flask inicializace
- `POJĎ NA ROUTES.PY` - HTTP endpointy
- `POJĎ NA ŠABLONY` - Frontend (všechny HTML)
- `POJĎ NA STATIC` - CSS styling
- `POJĎ NA RUN.PY` - Entry point
- `POJĎ NA INITIAL_DB_FILL.PY` - Seed data

Nebo buď konkrétnější:
- `POJĎ NA MODELS.PY řádky 10-30` - Konkrétní část

---

## 🎓 CO SE BUDEŠ UČIT

### **Po MODELS.PY:**
```
✅ Co je CrisisEvent
✅ Jaké pole má
✅ Jak se serializuje (to_dict, from_dict)
✅ Validace (severity 1-5)
✅ CRISIS_TYPES enum
```

### **Po CONFIG.PY:**
```
✅ Jak se nastavují MongoDB URI, Redis URL
✅ Co jsou environment proměnné
✅ Jak se vybírá config (dev/prod/test)
```

### **Po DB.PY:**
```
✅ Jak se vytváří DatabaseManager
✅ Lazy loading (MongoDB a Redis)
✅ CRUD operace (create, read, delete)
✅ Cache strategie
✅ Invalidace cache
```

### **Po __INIT__.PY:**
```
✅ Application factory pattern
✅ Jak se Flask aplikace spouští
✅ Blueprint registrace
✅ Error handling
```

### **Po ROUTES.PY:**
```
✅ Všech 7 endpointů
✅ GET vs POST
✅ Request/response
✅ Redirecty
✅ Chyby a error handling
```

### **Po ŠABLONÁCH:**
```
✅ Jinja2 templating
✅ Template inheritance
✅ Loops a podmínky
✅ URL generování
✅ JavaScript validace
```

### **Po STYLE.CSS:**
```
✅ Responsive design
✅ Severity barvy
✅ Layout struktura
```

### **Po RUN.PY + INITIAL_DB_FILL.PY:**
```
✅ Jak se aplikace spouští
✅ Jak se seedují testovací data
```

---

## ⏱️ ČASOVÝ ODHAD

| Fáze | Čas | Popis |
|-|-|-|
| Models.py | 15 min | Datový model |
| Config.py | 10 min | Konfigurace |
| Db.py | 45 min | Nejsložitější |
| __init__.py | 20 min | Flask setup |
| Routes.py | 40 min | 7 endpointů |
| Šablony | 30 min | HTML + JavaScript |
| CSS | 15 min | Styling |
| Run.py + Fill | 10 min | Pomocné věci |
| **CELKEM** | **~3 hodiny** | Kompletní porozumění |

---

## 🎯 KONEČNÝ CÍL

Až skončíme všechny soubory, **budeš umět:**

```
1. ✅ Vysvětlit, jak data teče aplikací (CrisisEvent -> DB -> HTML)
2. ✅ Odpovědět na JAKOUKOLI otázku o kódu
3. ✅ Procházet kód během zápočtu a ukazovat, co dělá
4. ✅ Modifikovat věci (přidat pole, změnit endpoint, atd.)
5. ✅ Debugovat problémy (vědět, kde hledat chybu)
```

---

## 💡 STRATEGIE BĚHEM ZÁPOČTU

```
Když tě zeptají:
"Jak se vytváří krize?"

Ty řekneš:
"Podívej se - otevřu routes.py linku 61..."
[Ukazuješ kód]
"Tady je submit_event() funkce, která..."
[Detailně vysvětliš]

= Vypadáš jako expert!
```

---

## ✅ PŘIPRAVENOST CHECKLIST

```
PŘEDTÍM NEŽ ZAČNEME:

□ Máš všechny soubory otevřené?
□ Máš Docker běžící? (docker-compose ps)
□ Máš aplikaci v prohlížeči? (localhost:5000)
□ Máš editor otevřený? (VS Code na souborech)
□ Máš tenhle plán přečtený?
□ Rozumíš pořadí souborů?
□ Jsi připraven na 3 hodiny intenzivního učení?

Až všechno OK -> napiš: "POJĎ NA MODELS.PY"
```

---

**VYKLEPÁNO! Čekám na tvůj signál. Když budeš připraven, řekni:**

```
POJĎ NA MODELS.PY
```

**A my začneme řádek po řádku.** 🚀
