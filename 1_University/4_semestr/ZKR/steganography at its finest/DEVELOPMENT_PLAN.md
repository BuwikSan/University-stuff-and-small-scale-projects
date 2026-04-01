# Red Team Polyglot Payload - Development Plan

## Overview
Create a single `.jpg` file that is actually a valid executable (EXE) containing:
1. **Cover image** (visual disguise)
2. **Hidden script** (embedded via LSB steganography)
3. **Payload** (PowerShell or executable)

---

## Phase 1: LSB Steganography Tool
**File:** `steganography.py`

### Purpose
Takes an image and hides data inside it using LSB (Least Significant Bit) steganography.

### Input
- `image.jpg` - Cover image (JPEG or PNG, preferably PNG for lossless)
- `data_to_hide` - PowerShell script or binary data to hide

### Output
- `image_with_hidden_data.png` - Image with embedded data (LSB modified)

### Key Points
- LSB steganography modifies the least significant bit of each pixel
- Change is imperceptible to human eye
- Extracting data requires knowing exact byte positions and data length
- Blue team must check pixel-level data to detect

### Implementation Notes
```python
# Pseudocode structure:
def embed_data_lsb(image_path, data_bytes, output_path):
    # 1. Load image using PIL/cv2
    # 2. Flatten image to 1D array of pixel values
    # 3. Convert data_bytes to binary
    # 4. Replace LSB of each pixel with data bits
    # 5. Save as PNG (lossless)
    # 6. Return: metadata (data_length, start_position, etc.)

def extract_data_lsb(image_path, data_length, start_position):
    # 1. Load image
    # 2. Extract LSB from pixels starting at start_position
    # 3. Reconstruct binary data
    # 4. Convert binary to bytes
    # 5. Return: extracted_data
```

---

## Phase 2: Extraction + Integration Script
**File:** `integrate_payload.py`

### Purpose
Takes the image with hidden data and creates a PowerShell script that:
1. Loads the image with hidden data
2. Extracts the hidden script
3. Executes it

### Input
- `image_with_hidden_data.png` - From Phase 1
- `steganography_metadata.json` - Location and size of hidden data
  ```json
  {
    "data_length": 1024,
    "start_position": 0,
    "extraction_method": "lsb"
  }
  ```

### Output
- `payload.ps1` - PowerShell script that extracts and runs hidden data

### Key Functionality
```powershell
# Pseudo-logic:
1. Load image_with_hidden_data.png from file
2. Extract LSB data using known positions
3. Decode to get original script/binary
4. Execute via Invoke-Expression or Start-Process
```

### Implementation Notes
- Encode the image as Base64 to embed in PowerShell
- Include extraction logic directly in payload.ps1
- Add obfuscation (encode commands, hide variable names)

---

## Phase 3: Polyglot Creation
**File:** `create_polyglot.py`

### Purpose
Creates the final `.jpg` file that is also a valid EXE.

### Input
- `payload.ps1` - From Phase 2
- `original_cover_image.jpg` - Real image for display

### Process
```
1. Read payload.ps1
2. Compile to EXE using PS2EXE
   Command: ps2exe -inputFile payload.ps1 -outputFile temp.exe -noConsole
3. Append original image binary to EXE
   Command: copy /b temp.exe + original_cover_image.jpg vacation.jpg
4. Verify polyglot
   - File is valid EXE (starts with MZ)
   - File is valid JPEG (has JPEG markers after JPEG end marker 0xFFD9)
5. Return: vacation.jpg
```

### Output
- `vacation.jpg` - Single polyglot file

---

## Phase 4: Integration Flow Diagram

```
INPUT PHASE:
┌─────────────────────┐
│   cover_image.jpg   │
│  + secret_script    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────────────────────┐
│ steganography.py                    │
│ Embed secret_script into image      │
│ Using LSB technique                 │
└──────────┬──────────────────────────┘
           │
           ▼
┌──────────────────────────────────┐
│ image_with_hidden_data.png       │
│ metadata.json                    │
└──────────┬───────────────────────┘
           │
           ▼
┌──────────────────────────────────────────┐
│ integrate_payload.py                     │
│ Create PowerShell extractor script       │
│ That reads LSB data from image           │
└──────────┬───────────────────────────────┘
           │
           ▼
┌──────────────────────────────────┐
│ payload.ps1                      │
│ - Extracts hidden data from PNG  │
│ - Executes it                    │
└──────────┬───────────────────────┘
           │
           ▼
┌──────────────────────────────────────────┐
│ create_polyglot.py                       │
│ 1. Compile payload.ps1 → EXE (PS2EXE)    │
│ 2. Append cover_image.jpg binary         │
│ 3. Create valid polyglot file            │
└──────────┬───────────────────────────────┘
           │
           ▼
┌──────────────────────────────┐
│ vacation.jpg                 │
│ (Valid EXE + Valid JPEG)     │
│ (Single file, no extensions) │
└──────────────────────────────┘
```

---

## File Structure

```
ZKR/
├── DEVELOPMENT_PLAN.md           (THIS FILE)
├── steganography.py              (Phase 1)
├── integrate_payload.py           (Phase 2)
├── create_polyglot.py             (Phase 3)
├── payload.ps1                    (Generated)
├── metadata.json                  (Generated)
├── image_with_hidden_data.png     (Generated)
└── vacation.jpg                   (FINAL OUTPUT)
```

---

## Step-by-Step Execution

### Step 1: Prepare data
```bash
# Create secret_script.ps1 with your payload
# Place cover_image.jpg in ZKR folder
```

### Step 2: Run steganography
```bash
python steganography.py --image cover_image.jpg --data secret_script.ps1 --output image_with_hidden_data.png
```

**Output:**
- `image_with_hidden_data.png`
- `metadata.json` (contains extraction info)

### Step 3: Generate extractor
```bash
python integrate_payload.py --image image_with_hidden_data.png --metadata metadata.json
```

**Output:**
- `payload.ps1` (PowerShell extractor + executor)

### Step 4: Create polyglot
```bash
python create_polyglot.py --script payload.ps1 --image cover_image.jpg --output vacation.jpg
```

**Output:**
- `vacation.jpg` (Final polyglot - EXE + JPEG)

### Step 5: Test
```bash
# Click vacation.jpg
# Should:
# 1. Open image in Photo Viewer
# 2. Execute hidden script silently
# 3. No suspicious behavior visible
```

---

## Technical Details

### LSB Steganography
- **Data capacity:** ~12% of image size (1 bit per 8 bits per color channel)
- **For 1920x1080 image:** ~312 KB capacity
- **Detection:** Requires pixel-level analysis; simple image comparison won't reveal it

### Polyglot Structure
```
[EXE Header - MZ...]
[PE Sections]
[Payload.ps1 data]
[Original image binary data]
[JPEG EOI marker - 0xFFD9]
```

- EXE parser reads until section table end
- JPEG parser reads from start, stops at 0xFFD9
- Both formats coexist independently

### Security Implications
- File starts with `MZ` (EXE magic) → Windows executes as binary
- File contains valid JPEG markers → Image viewer reads as JPEG
- LSB data imperceptible to human eye
- Blue team must check:
  1. File entropy
  2. Magic bytes
  3. Pixel data for anomalies
  4. Process spawning

---

## Blue Team Detection Points

### Easy (Surface Level)
- [ ] Check file extension (.jpg vs .exe)
- [ ] Check magic bytes (starts with MZ?)
- [ ] File size unusually large for JPG?

### Medium (Behavioral)
- [ ] Monitor process creation
- [ ] Check suspicious registry modifications
- [ ] Network traffic anomalies

### Hard (Forensic)
- [ ] Statistical analysis of pixel data
- [ ] LSB extraction and analysis
- [ ] Memory dumping during execution
- [ ] PowerShell script deobfuscation

---

## Obfuscation Opportunities

### For payload.ps1
- Encode commands in Base64
- Use variable name obfuscation
- Split strings to avoid detection
- Use aliases instead of full cmdlet names
- Encode LSB extraction coordinates

### For hidden script
- Compress before embedding
- Encrypt then embed
- Spread across multiple LSB layers

---

## Dependencies

### steganography.py
```
pip install Pillow opencv-python numpy
```

### integrate_payload.py
```
pip install
```

### create_polyglot.py
```
Requires:
- PowerShell
- PS2EXE module (Install-Module PS2EXE)
```

---

## Timeline Estimate

| Phase | Task | Time |
|-------|------|------|
| 1 | Write steganography.py | 2-3 hours |
| 2 | Write integrate_payload.py | 1-2 hours |
| 3 | Write create_polyglot.py | 1-2 hours |
| 4 | Testing & debugging | 2-3 hours |
| **Total** | | **6-10 hours** |

---

## Success Criteria

✓ Single file named `vacation.jpg`
✓ File is valid EXE (double-clickable, executes)
✓ File is valid JPEG (openable in Photo Viewer)
✓ Hidden script executes without visible window
✓ No double extensions or suspicious naming
✓ No external dependencies required on fresh Windows
✓ Blue team cannot easily determine how attack works

---

## Notes for Red Team

- Keep metadata.json secret - it contains extraction coordinates
- Test on fresh Windows VM to verify no dependencies
- Document all techniques used for report
- Prepare defense explanations for blue team
- Consider detection evasion techniques (entropy manipulation, etc.)

---

## Known Challenges

1. **PS2EXE availability** - Requires PowerShell module
   - Solution: Pre-compile EXE on your machine, distribute only polyglot
   
2. **JPEG compression** - Lossy format could corrupt LSB data
   - Solution: Use PNG for embedding, JPEG as display fallback
   
3. **File size** - Polyglot will be larger than normal image
   - Solution: Use genuine large-resolution image as cover
   
4. **Windows Defender** - May flag suspicious EXE
   - Solution: Code signing, delay execution, obfuscation

---

**Created:** 2025-04-01
**Purpose:** Advanced Cybersecurity Course - Red Team Assignment
