"""
Phase 1: LSB Steganography - Hide data inside image using Least Significant Bit technique
Input: image.jpg + data_to_hide (script/exe)
Output: image_with_hidden_data.png + metadata.json
"""

import os
import json
import argparse
from pathlib import Path
import numpy as np
from PIL import Image


class LSBSteganography:
    def __init__(self, verbose=True):
        self.verbose = verbose
    
    def log(self, message):
        if self.verbose:
            print(f"[LSB] {message}")
    
    def embed(self, image_path, data_path, output_path):
        """
        Embed binary data into image using LSB steganography
        
        Args:
            image_path: Path to cover image (JPEG/PNG)
            data_path: Path to data file to hide (binary/text)
            output_path: Path to save image with hidden data
        
        Returns:
            dict: Metadata needed for extraction
        """
        self.log(f"Loading image: {image_path}")
        img = Image.open(image_path)
        
        # Convert to RGB if necessary
        if img.mode != 'RGB' and img.mode != 'RGBA':
            img = img.convert('RGB')
        
        self.log(f"Image size: {img.size}, Mode: {img.mode}")
        
        # Read data to hide
        self.log(f"Reading data from: {data_path}")
        with open(data_path, 'rb') as f:
            data = f.read()
        
        data_length = len(data)
        self.log(f"Data size: {data_length} bytes")
        
        # Calculate capacity
        img_array = np.array(img)
        capacity = (img_array.size // 8)  # 1 bit per 8 bits
        
        self.log(f"Image capacity: {capacity} bytes")
        
        if data_length > capacity:
            raise ValueError(f"Data too large! Max capacity: {capacity} bytes, Data size: {data_length} bytes")
        
        # Flatten image to 1D array
        img_flat = img_array.flatten()
        
        # Convert data to binary
        data_binary = ''.join(f'{byte:08b}' for byte in data)
        
        self.log(f"Converting {data_length} bytes to binary: {len(data_binary)} bits")
        
        # Embed data using LSB
        self.log("Embedding data into LSB...")
        bit_index = 0
        for i in range(len(data_binary)):
            # Find next modifiable pixel (skip alpha channel)
            if img.mode == 'RGBA' and (i + 1) % 4 == 0:
                continue
            
            # Replace LSB of pixel with data bit
            pixel_index = i
            img_flat[pixel_index] = (img_flat[pixel_index] & ~1) | int(data_binary[i])
        
        self.log("Reshaping array back to image...")
        result_img = img_flat.reshape(img_array.shape).astype(np.uint8)
        result_img = Image.fromarray(result_img, mode=img.mode)
        
        self.log(f"Saving image to: {output_path}")
        result_img.save(output_path, 'PNG')  # Use PNG (lossless)
        
        # Create metadata
        metadata = {
            'data_length': data_length,
            'image_size': list(img.size),
            'image_mode': img.mode,
            'extraction_method': 'lsb',
            'hidden_file_hash': self._sha256_hash(data)
        }
        
        self.log(f"Embedding complete!")
        self.log(f"Metadata: {json.dumps(metadata, indent=2)}")
        
        return metadata
    
    def extract(self, image_path, data_length, output_path=None):
        """
        Extract data from image using LSB steganography
        
        Args:
            image_path: Path to image with hidden data
            data_length: Number of bytes to extract
            output_path: Optional path to save extracted data
        
        Returns:
            bytes: Extracted data
        """
        self.log(f"Loading image: {image_path}")
        img = Image.open(image_path)
        img_array = np.array(img)
        img_flat = img_array.flatten()
        
        self.log(f"Extracting {data_length} bytes of data...")
        
        # Extract bits
        extracted_bits = ''
        for i in range(data_length * 8):
            # Skip alpha channel if present
            if img.mode == 'RGBA' and (i + 1) % 4 == 0:
                continue
            
            extracted_bits += str(img_flat[i] & 1)
        
        # Convert binary to bytes
        extracted_data = b''
        for i in range(0, len(extracted_bits), 8):
            byte = extracted_bits[i:i+8]
            if len(byte) == 8:
                extracted_data += bytes([int(byte, 2)])
        
        self.log(f"Extraction complete! Retrieved {len(extracted_data)} bytes")
        
        if output_path:
            with open(output_path, 'wb') as f:
                f.write(extracted_data)
            self.log(f"Saved extracted data to: {output_path}")
        
        return extracted_data
    
    @staticmethod
    def _sha256_hash(data):
        """Calculate SHA256 hash of data"""
        import hashlib
        return hashlib.sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser(description='LSB Steganography - Hide/Extract data in images')
    parser.add_argument('--mode', choices=['embed', 'extract'], required=True, help='Mode: embed or extract')
    parser.add_argument('--image', required=True, help='Path to image file')
    parser.add_argument('--data', help='Path to data file (for embed mode)')
    parser.add_argument('--output', required=True, help='Output path')
    parser.add_argument('--metadata', help='Path to metadata file (for extract mode)')
    parser.add_argument('--data-length', type=int, help='Data length in bytes (for extract mode)')
    
    args = parser.parse_args()
    
    stego = LSBSteganography()
    
    if args.mode == 'embed':
        if not args.data:
            print("Error: --data required for embed mode")
            return
        
        metadata = stego.embed(args.image, args.data, args.output)
        
        # Save metadata
        metadata_path = args.output.replace('.png', '') + '_metadata.json'
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        print(f"\nMetadata saved to: {metadata_path}")
    
    elif args.mode == 'extract':
        if not args.data_length:
            if args.metadata:
                with open(args.metadata, 'r') as f:
                    metadata = json.load(f)
                args.data_length = metadata['data_length']
            else:
                print("Error: --data-length or --metadata required for extract mode")
                return
        
        stego.extract(args.image, args.data_length, args.output)


if __name__ == '__main__':
    main()
