# Made by Rubix (@LeRubix on GitHub) 26/08/2024

import json
import yaml
import zlib
import lzma
import brotli
import struct

# detects file format and reads content
def read_file(filepath):
    with open(filepath, 'r', errors="ignore") as f:
        if filepath.endswith('.json'):
            return json.load(f), 'json'
        elif filepath.endswith('.jsonl'):
            return f.readlines(), 'jsonl'
        elif filepath.endswith('.yaml') or filepath.endswith('.yml'):
            return yaml.safe_load(f), 'yaml'
        else:
            raise ValueError("Unsupported file format")

# compress the content using zlib, lzma or brotli
def compress_content(content, compression_method='zlib'):
    content_bytes = content.encode('utf-8')
    
    if compression_method == 'zlib':
        return zlib.compress(content_bytes)
    elif compression_method == 'lzma':
        return lzma.compress(content_bytes)
    elif compression_method == 'brotli':
        return brotli.compress(content_bytes)
    else:
        raise ValueError("Unsupported compression method")

# Function to format the header string to 5 bytes
def format_header_string(s):
    s = s.strip()  # Remove leading/trailing spaces
    return (s + '     ')[:5].encode('utf-8')  # Pad to 5 bytes

# write the compressed content with a header indicating file type and compression method
def write_compressed_file(filepath, compressed_data, file_type, compression_method):
    new_filepath = filepath.rsplit('.', 1)[0] + '.hrc'
    
    # Format file_type and compression_method to 5 bytes
    file_type = format_header_string(file_type)
    compression_method = format_header_string(compression_method)
    
    # header; 5 bytes for the file type and 5 bytes for the compression method
    header = struct.pack('5s5s', file_type, compression_method)
    
    with open(new_filepath, 'wb') as f:
        f.write(header)
        f.write(compressed_data)
    
    return new_filepath

# main function for compressing the file
def compress_file(filepath, compression_method='zlib'):
    try:
        content, file_type = read_file(filepath)
        
        # convert content to a string representation for compression
        if isinstance(content, dict):
            content = json.dumps(content)
        elif isinstance(content, list):
            if file_type == 'jsonl':
                content = '\n'.join(line.strip() for line in content)
            else:
                content = json.dumps(content)
        
        compressed_data = compress_content(content, compression_method)
    
        # write the compressed content with the header
        new_filepath = write_compressed_file(filepath, compressed_data, file_type, compression_method)
        
        print(f"File compressed successfully! New file: {new_filepath}")
        return new_filepath  # Return the path of the compressed file
    except Exception as e:
        print(f"Error: {str(e)}")
        return None  # Return None if compression fails

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Compress JSON/JSONL/YAML files into a highly compressed custom file type with a header.")
    parser.add_argument("filepath", help="Path to the JSON/JSONL/YAML file to be compressed")
    parser.add_argument("--method", choices=["zlib", "lzma", "brotli"], default="zlib", help="Compression method to use (default: zlib)")

    args = parser.parse_args()

    compressed_file_path = compress_file(args.filepath, args.method)
    if compressed_file_path:
        print(f"Compressed file saved at: {compressed_file_path}")
    else:
        print("Compression failed.")
