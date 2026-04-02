# 🔍 DEEP EXPLANATION: Polyglot Steganography - Vše od Základů

**Audience:** Chceš pochopit **jak** a **proč** každý krok funguje  
**Úroveň:** Advanced (pochopit binární formáty, steganografii, polygloty)

---

## 📚 Obsah

1. [Co je polyglot?](#polyglot)
2. [LSB Steganography - Jak se schová data](#lsb)
3. [Binární struktura - EXE vs JPEG](#binary)
4. [Kompletní flow - Co se děje](#flow)
5. [Proč je design takový, jaký je](#why)

---

## <a id="polyglot"></a>🎭 CO JE POLYGLOT? (Základy)

### Jednoduchý příklad: Text vs Binární

Normální soubor má "průhled" - počítač ví, co je:
```
File: document.txt
Content: "Hello World"
Format: TXT (text)
Application that opens it: Notepad
```

**Polyglot** = Jeden soubor, který je **zároveň validní ve VÍCE formátech**.

### Příklad: Obrázek + Text
```
File: image_with_text.jpg
Content: 
  [JPEG binary] + [Text "secret message"]
  ↓                ↓
  JPEG viewer:   Text editor:
  "Je to obrázek!"  "Je to text!"
```

### Náš Polyglot: EXE + JPEG
```
File: vacation.jpg
Content:
  [EXE binary - Windows Program] + [JPEG binary - Image]
  ↓                                 ↓
  Windows (double-click):         Image Viewer:
  "Spusť program"                 "Je to obrázek!"
```

---

### Proč to funguje?

Klíč: **Jak si aplikace interpretuje soubor?**

```
JPEG viewer hledá tyto handlery:
  1. Hledá "FFD8" (JPEG start marker) - zkoumá od ZAČÁTKU
  2. Čte pixel data
  3. Hledá "FFD9" (JPEG end marker) - ZASTAVÍ SE TADY
  ⬇️
  Vůbec ji nezajímá co je ZA "FFD9" (obsah EXE programu)
```

```
Windows (EXE runner):
  1. Hledá "MZ" (EXE header) - zkoumá od ZAČÁTKU
  2. Čte PE (Portable Executable) strukturu
  3. Zjistí offset sekcí, kódu, importů, etc.
  4. SPUSTÍ program
  ⬇️
  JPEG obsah (na konci) je pro EXE "neviditelný" - je mimo PE strukturu
```

---

## <a id="lsb"></a>🔐 LSB STEGANOGRAPHY (Jak se schová payload)

### Co je LSB (Least Significant Bit)?

Každý pixel má barvu reprezentovanou v RGB - 3 čísla (0-255):
```
Pixel: Red=173, Green=92, Blue=201

V binárce:
  Red:   173 = 10101101  ← poslední bit (LSB) = 1
  Green:  92 = 01011100  ← poslední bit (LSB) = 0
  Blue:  201 = 11001001  ← poslední bit (LSB) = 1
```

### Schování 1 bitu dat

Řekni, že chceš schovat **0**:
```
Původní pixel:
  Red:   173 = 10101101 (LSB = 1)
  Green:  92 = 01011100 (LSB = 0)
  Blue:  201 = 11001001 (LSB = 1)

Máme bits: [1, 0, 1] → z toho si vezmeme první = 1

Ale chceme schovat 0, takže:
  Red:   173 → 172 = 10101100 (změnime LSB z 1 na 0)

Nový pixel: Red=172, Green=92, Blue=201
Rozdíl barvy: 173 → 172 = změna o 1
Lidské oko: "Není vidět rozdíl!"
```

### Proč to funguje?

Pixel barva má 256 možností (0-255). Změna LSB = změna barvy o 1.
```
173  vs  172
█        █  ← Jsou prakticky nerozlišitelné!
```

Oka jsou citlivá na velké skokové změny (100 → 200), nikoliv malé (173 → 172).

### Praktický příklad: Schování "A" (01000001)

Máme 8 pixelů, z každého vezmeme 1 LSB bit:

```
Pixel 1: LSB=0 (změnit na 0, pokud je 1)
Pixel 2: LSB=1 (změnit na 1, pokud je 0)
Pixel 3: LSB=0 (změnit na 0, pokud je 1)
Pixel 4: LSB=0 (změnit na 0, pokud je 1)
Pixel 5: LSB=0 (změnit na 0, pokud je 1)
Pixel 6: LSB=0 (změnit na 0, pokud je 1)
Pixel 7: LSB=0 (změnit na 0, pokud je 1)
Pixel 8: LSB=1 (změnit na 1, pokud je 0)

Bits: 01000001 = ASCII "A"
```

Tím že si změníme LSB jednotlivých pixelů, schovali jsme "A" do obrázku!

### Kapacita a Извлечение

**Kapacita obrázku:**
```
1920 x 1080 pixel obrázek (Full HD, RGB)
= 1920 * 1080 = 2,073,600 pixelů
= 2,073,600 * 3 kanály (R, G, B) = 6,220,800 bytů hodnot
= 6,220,800 * 1 bit na kanál = 6,220,800 bitů
= 6,220,800 / 8 = 777,600 bytů ≈ 760 KB

▶️ Máme 760 KB na schování payloadu!
```

**Извлечение (Extrakce):**
```
Čtení obrázku:
  Pixel 1: LSB = 0
  Pixel 2: LSB = 1
  Pixel 3: LSB = 0
  ... (8 pixelů)
  
Bits: 01000001 = ASCII "A"
```

---

## <a id="binary"></a>⚙️ BINÁRNÍ STRUKTURA (EXE vs JPEG)

### Struktura EXE (Portable Executable)

```
┌─────────────────────────────────────────────────────────┐
│ MZ Header (64 bytes)                                    │
│ Signature: 0x4D5A ("MZ" - charaktery M, Z)            │
│ Contains: DOS stub, PE offset, etc.                   │
├─────────────────────────────────────────────────────────┤
│ PE Header (20 bytes)                                    │
│ Signature: 0x50450000 ("PE\0\0")                      │
│ Machine type (x86, x64), etc.                         │
├─────────────────────────────────────────────────────────┤
│ Optional Header (224+ bytes - 32-bit executable)       │
│ Entry point, image base, section count, etc.         │
├─────────────────────────────────────────────────────────┤
│ Section Headers (40 bytes per sekci)                   │
│ .text (code)                                          │
│ .data (initialized data)                              │
│ .rsrc (resources)                                     │
├─────────────────────────────────────────────────────────┤
│ Section Data (.text section)                           │
│ [Actual program code - machine instructions]          │
│ [This is what CPU executes!]                          │
├─────────────────────────────────────────────────────────┤
│ Section Data (.data section)                           │
│ [Global variables, initialized data]                   │
├─────────────────────────────────────────────────────────┤
│ Section Data (.rsrc section)                           │
│ [Resources: icons, strings, etc.]                     │
└─────────────────────────────────────────────────────────┘
  ↑
  Vše to je PE struktura kterou Windows/CPU rozumí
```

**Klíčový bod:** Windows kernel čte PE headers a ví PŘESNĚ kde končí program. Cokoli za tím se **ignoruje!**

### Struktura JPEG

```
┌──────────────────────────────────────────────────────────┐
│ SOI Marker: 0xFFD8 (Start of Image)                    │
├──────────────────────────────────────────────────────────┤
│ APP0 Marker: 0xFFE0 (JFIF - JPEG File Interchange)    │
│ Length: 16 bytes                                        │
│ Identifier: "JFIF\0"                                  │
├──────────────────────────────────────────────────────────┤
│ DQT Marker: 0xFFDB (Define Quantization Table)         │
│ [Compression lookup table]                             │
├──────────────────────────────────────────────────────────┤
│ SOF Marker: 0xFFC0 (Start of Frame)                    │
│ [Image dimensions, components]                         │
├──────────────────────────────────────────────────────────┤
│ DHT Marker: 0xFFC4 (Define Huffman Table)              │
│ [Huffman encoding table]                               │
├──────────────────────────────────────────────────────────┤
│ SOS Marker: 0xFFDA (Start of Scan)                     │
├──────────────────────────────────────────────────────────┤
│ Compressed Image Data                                   │
│ [Actual pixel data - compressed s Huffman encoding]  │
├──────────────────────────────────────────────────────────┤
│ EOI Marker: 0xFFD9 (End of Image) ◄─── KLÍČOVÝ!      │
└──────────────────────────────────────────────────────────┘
  ↑
  JPEG viewer hledá 0xFFD8 a čte až po 0xFFD9
  Cokoli PO 0xFFD9 se ignoruje!
```

---

### Polyglot Struktura (Kombinace)

```
[
  MZ Header (0x4D5A)
  PE Header (0x50450000)
  Optional Header
  Section Headers
  Section Data (.text)
  Section Data (.data)
  Section Data (.rsrc)
  ... (program je kompletní)
  ← Windows vidí END programu tady
]
+
[
  FFD8 (JPEG start)
  JPEG metadata
  JPEG data
  FFD9 (JPEG end) ← JPEG viewer se zastavuje tady
  ← Cokoli za tím se ignoruje
]

┌──────────────────────┐
│ EXE PROGRAM COMPLETE │  ← Windows interpretuje takhle
└──────────────────────┘
  │
  │ (JPEG viewer ignoruje)
  │
  ├──────────────────────┐
  │ JPEG IMAGE COMPLETE  │  ← JPEG viewer ignoruje všechno před
  └──────────────────────┘
       (FFD8...FFD9 část)
```

Díky tomu **jeden soubor = 2 validní formáty**!

---

## <a id="flow"></a>🔄 KOMPLETNÍ FLOW (Co se děje)

### Fáze 1: Steganography - Schování payloadu do obrázku

```
INPUT:
  cover.jpg (1920x1080, 760 KB kapacita)
  script.ps1 (10 KB - PowerShell skript)

PROCES:
┌─────────────────────────────────────────────────┐
│ 1. Načti cover.jpg                             │
│    └─ Konvertuj na PNG (lossless!)            │
│       └─ Načti pixely do paměti               │
│           [Pixel 0]: R=173, G=92, B=201       │
│           [Pixel 1]: R=45, G=128, B=88        │
│           ...                                  │
│                                                │
│ 2. Přečti script.ps1                          │
│    └─ Konvertuj na binární (bytes)            │
│       10,000 bytes = 80,000 bitů              │
│       Bit 1: 0                                │
│       Bit 2: 1                                │
│       Bit 3: 0                                │
│       ...                                      │
│                                                │
│ 3. Vlož bity do LSB pixelů                    │
│    FOR each bit in data_bits:                 │
│      [ Pixel LSB ] ← data_bit                │
│       173 → 172 (LSB: 1→0)                   │
│       45 → 44 (LSB: 1→0)                     │
│       88 → 89 (LSB: 0→1)                     │
│       ...                                      │
│       [80,000 pixelů upraveno]               │
│                                                │
│ 4. Ulož jako PNG                              │
│    └─ PNG je LOSSLESS (bez komprese dat)     │
│       JPEG by data zničil (LOSSY compression) │
│                                                │
│ 5. Generuj metadata.json                      │
│    {                                           │
│      "payload_size": 10000,                   │
│      "image_size": [1920, 1080],              │
│      "image_mode": "RGB"                      │
│    }                                           │
│    ← Potřebujeme vědět kolik bytů dálkovat   │
└─────────────────────────────────────────────────┘

OUTPUT:
  hidden.png (nezměnená velikost, ale obsahuje payload)
  hidden_metadata.json (10000 bytů ke čtení)
```

---

### Fáze 2: Build Extractor - Vytvoření PowerShell wrapperu

```
INPUT:
  hidden.png (2.2 MB - obsahuje schovaný payload)
  metadata.json (payload_size: 10000)
  extractor.ps1 (modul - statický kód)

PROCES:
┌──────────────────────────────────────────────────┐
│ 1. Načti hidden.png do paměti                   │
│    └─ Přečti všechny bytes                      │
│       2,200,000 bytů (2.2 MB)                  │
│                                                 │
│ 2. Zakóduj na Base64                           │
│    └─ Binární data → textový řetězec           │
│       iVBORw0KGgoAAAANSUhEUgAAAA...           │
│       [~2.9 MB textu - každá 3 bytes → 4 znaky]│
│                                                 │
│ 3. Vytvoř wrapper.ps1                          │
│    ┌─────────────────────────────────┐         │
│    │ $imageBase64 = "iVBORw0K..."   │         │
│    │ # [2.9 MB Base64 řetězec]      │         │
│    │                                 │         │
│    │ # [EMBED: extractor.ps1 kód]   │         │
│    │ function Extract-LSBData { ... }│         │
│    │ function Invoke-Payload { ... } │         │
│    │                                 │         │
│    │ # MAIN                         │         │
│    │ $img = [Convert]::FromBase64...│         │
│    │ $payload = Extract-LSBData ... │         │
│    │ Invoke-ExtractedPayload ...   │         │
│    └─────────────────────────────────┘         │
│                                                 │
│    Soubor: ~3 MB PowerShell (Base64 img)      │
└──────────────────────────────────────────────────┘

OUTPUT:
  wrapper.ps1 (~3 MB - obsahuje veškerý kód + data)
  ← Vše co potřebujeme na extrakci + spuštění
```

---

### Fáze 3: Create Polyglot - Kombinování do polyglotu

```
INPUT:
  wrapper.ps1 (3 MB)
  cover.jpg (ORIGINÁLNÍ - pro návrat na vizuální obrázek)

PROCES:
┌───────────────────────────────────────────────────┐
│ 1. Kompiluj PowerShell na EXE (PS2EXE)           │
│    wrapper.ps1 → temp_executable.exe             │
│                                                   │
│    Co PS2EXE dělá:                              │
│    ┌──────────────────────────────────────────┐  │
│    │ Vezmi PowerShell skript (.ps1)           │  │
│    │ Vytvoř zjednodušený CLR host             │  │
│    │ Uprav skript tak aby běžel bez PS.EXE    │  │
│    │ Kompiluj do machine code                 │  │
│    │ Vytvoř validní Windows executable        │  │
│    │ Output: temp_executable.exe (~1-2 MB)   │  │
│    └──────────────────────────────────────────┘  │
│                                                   │
│ 2. Načti EXE a JPEG jako binární                │
│    ┌──────────────────────────────────────────┐  │
│    │ EXE bytes: [4D 5A 90 00 03 00 ...] (1 MB)│  │
│    │ JPEG bytes: [FF D8 FF E0 00 10 ...] (2 MB)│ │
│    └──────────────────────────────────────────┘  │
│                                                   │
│ 3. MERGE - Concatenate binární                   │
│    new_file = exe_bytes + jpeg_bytes            │
│    Struktura:                                    │
│    ┌──────────────────┐                         │
│    │ [EXE 1 MB]      │                         │
│    │ [JPEG 2 MB]     │                         │
│    │ = 3 MB celkem   │                         │
│    └──────────────────┘                         │
│                                                   │
│ 4. Ulož jako vacation.jpg                       │
│    └─ Název je důležitý! Lidi si myslí že je    │
│       to obrázek (.jpg přípona)                 │
└───────────────────────────────────────────────────┘

OUTPUT:
  vacation.jpg (3 MB binary file)
  ┌──────────────────────────────────────────────┐
  │ Binární struktura:                           │
  │ [MZ ... program ... sections ...] (EXE)     │
  │ [FFD8 ... image ... FFD9] (JPEG)           │
  │                                              │
  │ Windows (double-click): Spustí EXE        │
  │ JPEG viewer: Zobrazí obrázek              │
  └──────────────────────────────────────────────┘
```

---

### Loading & Execution - Co se stane když spustíš vacation.jpg

```
┌────────────────────────────────────────────────────────┐
│ 1. Uživatel double-clickne vacation.jpg             │
└────────────────────────────────────────────────────────┘
                        ↓
┌────────────────────────────────────────────────────────┐
│ 2. Windows vidí "MZ" header (0x4D5A)                │
│    └─ Pozná: "Toto je EXE program, spustím jej"  │
└────────────────────────────────────────────────────────┘
                        ↓
┌────────────────────────────────────────────────────────┐
│ 3. Kernel loader čte PE strukturu                  │
│    ├─ Přečte section headers                      │
│    ├─ Alokuje paměť podle SectionSizes           │
│    ├─ Mapuje .text section (code)                │
│    ├─ Mapuje .data section                       │
│    └─ Mapuje .rsrc section                       │
│    └─ ZASTAVÍ SE - JPEG část je mimo PE strukturu│
└────────────────────────────────────────────────────────┘
                        ↓
┌────────────────────────────────────────────────────────┐
│ 4. PowerShell CLR runtime se inicializuje        │
│    └─ PS2EXE wrapper spustí embedded PowerShell  │
└────────────────────────────────────────────────────────┘
                        ↓
┌────────────────────────────────────────────────────────┐
│ 5. Wrapper skript se spustí:                      │
│                                                    │
│    $imageBase64 = "iVBORw0KGgo..." (2.9 MB)     │
│    $imageBytes = [Convert]::FromBase64String(...)│
│    ↓                                              │
│    Dekóduje Base64 → binární PNG data do paměti │
│    (Bez zápisu na disk!)                        │
└────────────────────────────────────────────────────────┘
                        ↓
┌────────────────────────────────────────────────────────┐
│ 6. Volá Extract-LSBData funkci                   │
│    └─ Vezme PNG bytes a metadata:                │
│       ├─ payload_size = 10000                    │
│       ├─ image_bytes = [všechny PNG pixely]      │
│       └─ Iteruje 80,000 bitů:                    │
│          Bit 1: PNG_byte[0] & 1 = 0             │
│          Bit 2: PNG_byte[1] & 1 = 1             │
│          Bit 3: PNG_byte[2] & 1 = 0             │
│          ...                                     │
│          └─ Rekonstruuje: [0, 1, 0, ...]        │
│             → 10,000 bytů PAYLOAD               │
└────────────────────────────────────────────────────────┘
                        ↓
┌────────────────────────────────────────────────────────┐
│ 7. Volá Invoke-ExtractedPayload                  │
│    └─ Vezme 10,000 bytů a:                       │
│       ├─ Pokusí se UTF8 dekódovat:              │
│       │  "Write-Host 'Hello!'" ← Je to skript!  │
│       ├─ Rozpozná PowerShell syntax             │
│       └─ Spustí: Invoke-Expression $scriptText  │
│          ↓                                       │
│          "Hello!" se vypíše (nebo cokoliv v PS) │
└────────────────────────────────────────────────────────┘
                        ↓
┌────────────────────────────────────────────────────────┐
│ 8. Program skončí                                │
│    └─ Uživatel neví že se něco stalo (silent!)  │
└────────────────────────────────────────────────────────┘
```

---

## <a id="why"></a>❓ PROČ JE DESIGN TAKOVÝ?

### Proč Steganography.py? (Oddělený)

```
Důvod: MODULARITA
└─ Chceme aby šel payload schovat do LIBOVOLNÉHO obrázku
   ├─ JPG formát
   ├─ PNG
   ├─ BMP
   └─ Jakýkoliv obrázek s dostatečnou rezolucí

Proč oddělený skript?
├─ Dá se volat samostatně
├─ Dá se testovat bez polyglotu
├─ Dá se ladit kapacita
└─ Uživatel vidí: Onde se payload schoval?
```

### Proč Build_extractor.py? (Wrapper generator)

**Otázka kterou jsi položil:** Potřebujeme to?

Technicky NE, ale:

```
Důvody proč JE:
├─ Separace zájmů (Separation of Concerns)
│  └─ Steganography = Ukrývání dat
│  └─ Build_extractor = Příprava spouštěcího kódu
│  └─ Create_polyglot = Kombinování do souboru
│
├─ Debugging
│  └─ Máš wrapper.ps1 který vidíš a můžeš editovat
│  └─ Můžeš jej spustit přímo bez polyglotu
│
├─ Flexibilita
│  └─ Wrapper se dá upravit před polyglot-utworzením
│  └─ Můžeš přidat obfuskaci, logging, atd.
│
└─ Testin
   └─ Dá se testovat extraction bez polyglotu
```

**Alternativní design (čistší):**
```
Všechno by bylo v create_polyglot.py:
  1. Vloží payload do obrázku (steganography)
  2. Interně si generuje wrapper
  3. Kompiluje na EXE
  4. Merguje s JPEG

Výhoda: Méně souborů, jednodušší
Nevýhoda: Méně flexibility, těžší debug
```

---

### Proč Create_polyglot.py? (Kombinování)

```
Důvod: Windows kernel vyžaduje PŘESNOU strukturu

Pokud jen zkoncatenujeme:
  exe_bytes + jpeg_bytes = OK!
  ✓ EXE část: Windows rozumí PE struktuře
  ✓ JPEG část: JPEG viewer rozumí JPEG
  
Proč funguje?
└─ Windows čte EXE headers
   ├─ Zjistí kde program končí (podle PE struct)
   ├─ Mapuje paměť
   ├─ Spustí program
   └─ JPEG data jsou "mimo program" - nezajímá jej

JPEG viewer:
├─ Hledá 0xFFD8 (start)
├─ Čte pixel data
└─ Zůstane stát na 0xFFD9 (konec)
   └─ "EXE data před JPEG" ji vůbec nezajímá!
```

---

### Proč Extractor.ps1? (Statický modul)

```
Proč NE generovat?

Generovaný by vypadal:
  # Copy-pasted funkce
  # Copy-pasted Loop pro extraction
  # Custom parametry pro payload_size
  └─ Redundance, těžko se čte

Statický modul:
  ├─ Jedna verze funkce Extract-LSBData
  ├─ Přijímá parametry: $ImageBytes, $PayloadSize
  ├─ Generický - pracuje s JAKÝMKOLIV payloademem
  ├─ Testovatelný - můžeš jej volat zvlášť
  └─ Čitelný - vidíš přesně co dělá
```

---

## 🎯 SHRNUTÍ PROČ DESIGN VYPADÁ TAKTO

```
1. steganography.py
   └─ Libovolný obrázek + payload → schování do LSB pixelů
      ← Modular, testovatelné, vidíš co se děje

2. build_extractor.py
   └─ Vezme hidden.png, generuje wrapper.ps1
      ├─ Base64 obrázek
      ├─ Embedding kódu
      ├─ Testování bez polyglotu
      └─ optionálně modifikace

3. create_polyglot.py
   └─ Vezme wrapper.ps1, kompiluje na EXE
      ├─ PS2EXE → EXE binary
      ├─ Merguje s JPEG
      ├─ Verifikuje polyglot
      └─ Hotový soubor

4. orchestrator.py
   └─ Řetězí všechny 3 skripty
      └─ Uživatel musí znát jen: orchestrator.py --image --payload --output
```

---

## 🔬 BINÁRNÍ PŘÍKLAD (Co se opravdu v souboru děje)

### Originální obrázek

```
File: cover.jpg
Binární dump prvních 16 bytů:
  FF D8 FF E0 00 10 4A 46 49 46 00 01 01 00 00 01
  ↑  ↑  ↑  ↑
  FFD8 = JPEG start
         FFE0 = JFIF APP0 marker
```

### Po steganografii

```
File: hidden.png
Binární dump prvních 16 bytů:
  89 50 4E 47 0D 0A 1A 0A 00 00 00 0D 49 48 44 52
  ↑  ↑  ↑  ↑
  89 = PNG signature byte 1
     50 = P
           4E = N
              47 = G

Obsahuje: Originální pixely s upravenými LSB bity
  └─ 10,000 bytů payloadu schováno v LSB
```

### Po vytvoření polyglotu

```
File: vacation.jpg (binární struktura)
Bytes 0-100 (EXE header):
  4D 5A 90 00 03 00 00 00 04 00
  ↑  ↑
  MZ = EXE header

Bytes 100-400000 (EXE program sections):
  ... [Machine code, imports, resources]

Bytes 400001-2400000 (JPEG image):
  FF D8 FF E0 00 10 4A 46 46 46...
  ↑  ↑
  FFD8 = JPEG start marker
         ↑
         (Windows ignores everything before this)
  
  ... [JPEG pixel data]
  
  FF D9
  ↑  ↑
  FFD9 = JPEG end marker
```

---

## 🎓 CO JSME SE NAUČILI

1. **Polyglot:** Jeden soubor, více validních formátů
2. **LSB Steganography:** Schování bitů do nejméně důležitých bitů pixelů
3. **File Formats:** Jak Windows/JPEG viewer interpretují soubory (od začátku)
4. **Binary Merging:** EXE + JPEG = oba fungují
5. **PowerShell Runtime:** Wrapper spustí embedded kód a extrahuje payload
6. **Design:** Modularita vs. jednoduchost

