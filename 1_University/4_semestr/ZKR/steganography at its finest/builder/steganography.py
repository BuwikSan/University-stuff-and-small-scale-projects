"""
LSB Steganography Module - Hide/Extract data from PNG images
Supports any input format (JPEG, PNG, BMP, etc.) but always works with PNG internally
Uses Least Significant Bit technique for imperceptible data hiding
"""

import os
import json
import argparse
from pathlib import Path
import numpy as np
from PIL import Image
import hashlib


class LSBSteganography:
    """
    Modular LSB Steganography implementation
    - Always converts to PNG (lossless)
    - Supports arbitrary payloads (if they fit)
    - Works with input/carrier and input/payload folder structure
    """
    
    # Bits per channel (always 1 for LSB)
    BITS_PER_CHANNEL = 1
    
    def __init__(self, verbose=True):
        self.verbose = verbose
        self.script_dir = Path(__file__).parent.parent
    
    def log(self, message, level="INFO"):
        if self.verbose:
            prefix = f"[{level}]" if level != "INFO" else "[LSB]"
            print(f"{prefix} {message}")
    
    def convert_to_png(self, image_path):
        """
        Convert any image format to PNG (lossless)
        
        Args:
            image_path: Path to image (JPEG, PNG, BMP, etc.)
        
        Returns:
            PIL.Image: Image in PNG format (RGB mode)
        """
        img = Image.open(image_path)
        original_format = img.format
        
        # Convert to RGB if needed (removes alpha channel if RGBA)
        if img.mode != 'RGB':
            if img.mode == 'RGBA':
                self.log(f"Converting RGBA to RGB (removing transparency)", "DEBUG")
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[3])
                img = background
            else:
                self.log(f"Converting {img.mode} to RGB", "DEBUG")
                img = img.convert('RGB')
        
        if original_format and original_format.upper() != 'PNG':
            self.log(f"Converted {original_format} → PNG")
        
        return img
    
    def get_image_capacity(self, image_path):
        """
        Calculate maximum data capacity for an image
        
        Args:
            image_path: Path to image file (any format)
        
        Returns:
            int: Maximum bytes that can be hidden
        """
        img = self.convert_to_png(image_path)
        width, height = img.size
        
        # Always RGB (3 channels) after conversion
        channels = 3
        
        total_bits = width * height * channels * self.BITS_PER_CHANNEL
        capacity_bytes = total_bits // 8
        
        return capacity_bytes
    
    def embed(self, image_path, data_path, output_path):
        """
        Embed binary data into PNG image using LSB steganography
        - Converts input image to PNG if needed
        - Always outputs PNG (lossless)
        
        Args:
            image_path: Path to cover image (JPEG, PNG, BMP, etc.)
            data_path: Path to data file to hide (binary/text/executable)
            output_path: Path to save PNG with hidden data
        
        Returns:
            dict: Metadata needed for extraction
        
        Raises:
            ValueError: If data is too large for the image
            FileNotFoundError: If input files don't exist
        """
        # Validate inputs
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")
        if not os.path.exists(data_path):
            raise FileNotFoundError(f"Data file not found: {data_path}")
        
        # Load and convert image
        self.log(f"Loading image: {image_path}")
        img = self.convert_to_png(image_path)
        
        width, height = img.size
        self.log(f"Image: {width}x{height} (RGB)")
        
        # Read payload
        self.log(f"Reading payload: {data_path}")
        with open(data_path, 'rb') as f:
            payload = f.read()
        
        payload_size = len(payload)
        self.log(f"Payload size: {payload_size} bytes")
        
        # Check capacity
        capacity = self.get_image_capacity(image_path)
        self.log(f"Image capacity: {capacity} bytes")
        
        if payload_size > capacity:
            raise ValueError(
                f"Payload too large for image!\n"
                f"  Payload: {payload_size} bytes\n"
                f"  Capacity: {capacity} bytes\n"
                f"  Need: {payload_size - capacity} more bytes"
            )
        
        # Convert to array
        img_array = np.array(img, dtype=np.uint8)
        img_flat = img_array.flatten()
        
        # Convert payload to binary
        payload_binary = ''.join(f'{byte:08b}' for byte in payload)
        
        self.log(f"Embedding {payload_size} bytes ({len(payload_binary)} bits)...")
        
        # Embed LSB
        for bit_idx, bit_char in enumerate(payload_binary):
            bit_value = int(bit_char)
            # Clear LSB and set with data bit
            img_flat[bit_idx] = (img_flat[bit_idx] & 0xFE) | bit_value
        
        # Reshape and save as PNG (lossless!)
        result_array = img_flat.reshape(img_array.shape).astype(np.uint8)
        result_img = Image.fromarray(result_array, mode='RGB')
        
        self.log(f"Saving to: {output_path}")
        result_img.save(output_path, 'PNG')  # Always PNG (lossless)
        
        # Generate metadata
        metadata = {
            'version': 1,
            'payload_size': payload_size,
            'image_size': [width, height],
            'image_mode': 'RGB',
            'image_format': 'PNG',
            'payload_hash': hashlib.sha256(payload).hexdigest(),
            'capacity': capacity
        }
        
        self.log("Embedding complete!", "SUCCESS")
        return metadata
    
    def extract(self, image_path, payload_size, output_path=None):
        """
        Extract hidden data from PNG image using LSB steganography
        
        Args:
            image_path: Path to PNG image with hidden payload
            payload_size: Number of bytes to extract (from metadata)
            output_path: Optional path to save extracted payload
        
        Returns:
            bytes: Extracted payload
        
        Raises:
            FileNotFoundError: If image doesn't exist
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")
        
        # Load image
        self.log(f"Loading image: {image_path}")
        img = self.convert_to_png(image_path)
        
        # Extract to array
        img_array = np.array(img, dtype=np.uint8)
        img_flat = img_array.flatten()
        
        # Extract LSB bits
        self.log(f"Extracting {payload_size} bytes ({payload_size * 8} bits)...")
        extracted_bits = ''
        
        for bit_idx in range(payload_size * 8):
            bit_value = img_flat[bit_idx] & 1
            extracted_bits += str(bit_value)
        
        # Convert bits to bytes
        extracted_data = b''
        for i in range(0, len(extracted_bits), 8):
            byte_str = extracted_bits[i:i+8]
            if len(byte_str) == 8:
                extracted_data += bytes([int(byte_str, 2)])
        
        self.log(f"Extraction complete! Retrieved {len(extracted_data)} bytes", "SUCCESS")
        
        # Optionally save
        if output_path:
            with open(output_path, 'wb') as f:
                f.write(extracted_data)
            self.log(f"Saved to: {output_path}")
        
        return extracted_data

    
    @staticmethod
    def find_input_files():
        """
        Find carrier image and payload in default folders
        
        Returns:
            tuple: (carrier_path, payload_path) or raises FileNotFoundError
        """
        script_dir = Path(__file__).parent.parent
        carrier_dir = script_dir / 'input' / 'carrier'
        payload_dir = script_dir / 'input' / 'payload'
        
        # Find carrier image
        carrier_files = list(carrier_dir.glob('*.jpg')) + list(carrier_dir.glob('*.png')) + \
                       list(carrier_dir.glob('*.jpeg')) + list(carrier_dir.glob('*.bmp'))
        
        if not carrier_files:
            raise FileNotFoundError(f"No carrier image in {carrier_dir}")
        
        carrier_path = carrier_files[0]
        
        # Find payload
        payload_files = list(payload_dir.glob('*'))
        payload_files = [f for f in payload_files if f.is_file()]
        
        if not payload_files:
            raise FileNotFoundError(f"No payload in {payload_dir}")
        
        payload_path = payload_files[0]
        
        return carrier_path, payload_path


def main():
    parser = argparse.ArgumentParser(
        description='LSB Steganography - Modular data hiding in PNG images'
    )
    parser.add_argument('--mode', choices=['embed', 'extract', 'capacity', 'auto'], 
                       default='auto', help='Operation mode (default: auto-detect from input/)')
    parser.add_argument('--image', help='Image file path (overrides input/carrier/)')
    parser.add_argument('--data', help='Data file to hide (overrides input/payload/)')
    parser.add_argument('--output', help='Output file path')
    parser.add_argument('--metadata', help='Metadata JSON file (extract mode)')
    parser.add_argument('--payload-size', type=int, help='Payload size in bytes (extract mode)')
    parser.add_argument('--quiet', action='store_true', help='Suppress output')
    
    args = parser.parse_args()
    
    stego = LSBSteganography(verbose=not args.quiet)
    
    try:
        if args.mode == 'auto':
            # Auto-detect from input/ folder structure
            print("Auto-detecting input files...")
            try:
                carrier, payload = LSBSteganography.find_input_files()
                print(f"  Carrier: {carrier}")
                print(f"  Payload: {payload}")
                print(f"  Mode: embed")
                
                output = args.output or "output/hidden.png"
                os.makedirs(os.path.dirname(output) or '.', exist_ok=True)
                
                metadata = stego.embed(str(carrier), str(payload), output)
                
                # Save metadata
                metadata_path = output.replace('.png', '') + '_metadata.json'
                with open(metadata_path, 'w') as f:
                    json.dump(metadata, f, indent=2)
                
                print(f"\n✓ Metadata saved: {metadata_path}")
                print(f"✓ Image saved: {output}")
                return 0
            except FileNotFoundError as e:
                print(f"Auto-detect failed: {e}")
                return 1
        
        elif args.mode == 'capacity':
            if not args.image:
                print("capacity mode requires --image")
                return 1
            capacity = stego.get_image_capacity(args.image)
            print(f"Image capacity: {capacity} bytes (~{capacity / 1024:.1f} KB)")
        
        elif args.mode == 'embed':
            if not args.image or not args.data or not args.output:
                parser.error("embed mode requires --image, --data, and --output")
            
            metadata = stego.embed(args.image, args.data, args.output)
            
            # Save metadata
            metadata_path = args.output.replace('.png', '') + '_metadata.json'
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            print(f"\n✓ Metadata saved: {metadata_path}")
            print(f"✓ Image saved: {args.output}")
        
        elif args.mode == 'extract':
            if not args.output:
                parser.error("extract mode requires --output")
            
            # Get payload size
            if args.metadata:
                with open(args.metadata, 'r') as f:
                    metadata = json.load(f)
                payload_size = metadata['payload_size']
            elif args.payload_size:
                payload_size = args.payload_size
            else:
                parser.error("extract mode requires --metadata or --payload-size")
            
            stego.extract(args.image, payload_size, args.output)
            print(f"✓ Payload extracted: {args.output}")
    
    except Exception as e:
        print(f"\n✗ Error: {e}")
        return 1
    
    return 0


if __name__ == '__main__':
    exit(main())
