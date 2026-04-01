"""
Test harness for polyglot creation workflow
Validates each component independently before integration
"""

import os
import sys
import json
import subprocess
from pathlib import Path


class PolyglotTester:
    def __init__(self):
        self.script_dir = Path(__file__).parent
        self.passed = 0
        self.failed = 0
    
    def log(self, message, level="INFO"):
        symbols = {
            "PASS": "✓",
            "FAIL": "✗",
            "INFO": "ℹ",
            "TEST": "◆"
        }
        symbol = symbols.get(level, "•")
        print(f"{symbol} {message}")
    
    def test_dependencies(self):
        """Test if all dependencies are installed"""
        self.log("Testing dependencies...", "TEST")
        
        deps = {
            'PIL': 'Pillow',
            'cv2': 'opencv-python',
            'numpy': 'numpy'
        }
        
        for module, name in deps.items():
            try:
                __import__(module)
                self.log(f"{name} installed", "PASS")
                self.passed += 1
            except ImportError:
                self.log(f"{name} NOT installed - pip install {name}", "FAIL")
                self.failed += 1
        
        return self.failed == 0
    
    def test_powerhardy(self):
        """Test PowerShell availability"""
        self.log("Testing PowerShell...", "TEST")
        
        try:
            result = subprocess.run(
                ['powershell.exe', '-Command', 'Write-Host "OK"'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if "OK" in result.stdout:
                self.log("PowerShell available", "PASS")
                self.passed += 1
                return True
            else:
                self.log("PowerShell not responding", "FAIL")
                self.failed += 1
                return False
        except Exception as e:
            self.log(f"PowerShell error: {e}", "FAIL")
            self.failed += 1
            return False
    
    def test_ps2exe(self):
        """Test PS2EXE module availability"""
        self.log("Testing PS2EXE module...", "TEST")
        
        try:
            result = subprocess.run(
                ['powershell.exe', '-Command', 
                 'Get-Module PS2EXE -ListAvailable'],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0 and result.stdout.strip():
                self.log("PS2EXE module installed", "PASS")
                self.passed += 1
                return True
            else:
                self.log("PS2EXE module NOT installed", "FAIL")
                self.log("  Install with: Install-Module PS2EXE -Force", "INFO")
                self.failed += 1
                return False
        except Exception as e:
            self.log(f"PS2EXE check error: {e}", "FAIL")
            self.failed += 1
            return False
    
    def test_steganography_module(self):
        """Test steganography.py module"""
        self.log("Testing steganography module...", "TEST")
        
        try:
            result = subprocess.run(
                [sys.executable, str(self.script_dir / 'steganography.py'), '--help'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                self.log("Steganography module OK", "PASS")
                self.passed += 1
                return True
            else:
                self.log("Steganography module error", "FAIL")
                self.failed += 1
                return False
        except Exception as e:
            self.log(f"Steganography module error: {e}", "FAIL")
            self.failed += 1
            return False
    
    def test_extractor_builder(self):
        """Test build_extractor.py module"""
        self.log("Testing extractor builder...", "TEST")
        
        try:
            result = subprocess.run(
                [sys.executable, str(self.script_dir / 'build_extractor.py'), '--help'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                self.log("Extractor builder OK", "PASS")
                self.passed += 1
                return True
            else:
                self.log("Extractor builder error", "FAIL")
                self.failed += 1
                return False
        except Exception as e:
            self.log(f"Extractor builder error: {e}", "FAIL")
            self.failed += 1
            return False
    
    def test_polyglot_creator(self):
        """Test create_polyglot.py module"""
        self.log("Testing polyglot creator...", "TEST")
        
        try:
            result = subprocess.run(
                [sys.executable, str(self.script_dir / 'create_polyglot.py'), '--help'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                self.log("Polyglot creator OK", "PASS")
                self.passed += 1
                return True
            else:
                self.log("Polyglot creator error", "FAIL")
                self.failed += 1
                return False
        except Exception as e:
            self.log(f"Polyglot creator error: {e}", "FAIL")
            self.failed += 1
            return False
    
    def test_orchestrator(self):
        """Test orchestrator.py module"""
        self.log("Testing orchestrator...", "TEST")
        
        try:
            result = subprocess.run(
                [sys.executable, str(self.script_dir / 'orchestrator.py'), '--help'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                self.log("Orchestrator OK", "PASS")
                self.passed += 1
                return True
            else:
                self.log("Orchestrator error", "FAIL")
                self.failed += 1
                return False
        except Exception as e:
            self.log(f"Orchestrator error: {e}", "FAIL")
            self.failed += 1
            return False
    
    def test_create_test_image(self):
        """Create a minimal test image"""
        self.log("Creating test image...", "TEST")
        
        try:
            from PIL import Image
            import numpy as np
            
            # Create 100x100 solid gray image
            img_array = np.ones((100, 100, 3), dtype=np.uint8) * 128
            img = Image.fromarray(img_array)
            test_image_path = self.script_dir / 'test_image.jpg'
            img.save(test_image_path, 'JPEG')
            
            if test_image_path.exists():
                self.log(f"Test image created: {test_image_path}", "PASS")
                self.passed += 1
                return str(test_image_path)
            else:
                self.log("Failed to create test image", "FAIL")
                self.failed += 1
                return None
        except Exception as e:
            self.log(f"Test image creation error: {e}", "FAIL")
            self.failed += 1
            return None
    
    def test_create_test_payload(self):
        """Create a minimal test payload"""
        self.log("Creating test payload...", "TEST")
        
        try:
            test_payload_path = self.script_dir / 'test_payload.ps1'
            with open(test_payload_path, 'w') as f:
                f.write('Write-Host "Payload executed successfully!"')
            
            if test_payload_path.exists():
                self.log(f"Test payload created: {test_payload_path}", "PASS")
                self.passed += 1
                return str(test_payload_path)
            else:
                self.log("Failed to create test payload", "FAIL")
                self.failed += 1
                return None
        except Exception as e:
            self.log(f"Test payload creation error: {e}", "FAIL")
            self.failed += 1
            return None
    
    def run_all_tests(self):
        """Run all tests"""
        print("\n" + "=" * 60)
        print("POLYGLOT SETUP VALIDATION TESTS")
        print("=" * 60 + "\n")
        
        # Dependency tests
        print("DEPENDENCY CHECKS:")
        self.test_dependencies()
        self.test_powerhardy()
        self.test_ps2exe()
        
        # Module tests
        print("\nMODULE CHECKS:")
        self.test_steganography_module()
        self.test_extractor_builder()
        self.test_polyglot_creator()
        self.test_orchestrator()
        
        # Resource creation tests
        print("\nRESOURCE CREATION:")
        test_img = self.test_create_test_image()
        test_pay = self.test_create_test_payload()
        
        # Summary
        print("\n" + "=" * 60)
        print(f"RESULTS: {self.passed} passed, {self.failed} failed")
        print("=" * 60)
        
        if self.failed == 0:
            print("\n✓ All systems ready!")
            print("\nYou can now run:")
            if test_img and test_pay:
                print(f"  python orchestrator.py --image {test_img} --payload {test_pay}")
            return True
        else:
            print(f"\n✗ {self.failed} test(s) failed!")
            print("Please fix issues and re-run tests.")
            return False


def main():
    tester = PolyglotTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
