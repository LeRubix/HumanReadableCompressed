# Made by Rubix (@LeRubix on GitHub) 26/08/2024

import zlib
import lzma
import brotli
import struct
import json


# decompress the content based on the compression method
def decompress_content(compressed_data, compression_method='zlib'):
    if compression_method == 'zlib':
        return zlib.decompress(compressed_data)
    elif compression_method == 'lzma':
        return lzma.decompress(compressed_data)
    elif compression_method == 'brotli':
        return brotli.decompress(compressed_data)
    else:
        raise ValueError("Unsupported compression method")

# write the raw decompressed content to the original file type
def write_decompressed_file(filepath, decompressed_data, file_type):
    new_filepath = filepath.rsplit('.', 1)[0] + '.' + file_type
    
    decoded_data = decompressed_data.decode('utf-8')
    
    with open(new_filepath, 'w', encoding='utf-8') as f:
        if file_type == 'jsonl':
            # For JSONL, write each line separately
            for line in decoded_data.splitlines():
                f.write(line + '\n')
        elif file_type == 'json':
            # For JSON, parse and re-encode to ensure proper formatting
            parsed_data = json.loads(decoded_data)
            json.dump(parsed_data, f, ensure_ascii=False, indent=2)
        elif file_type == 'yaml':
            # For YAML, write as-is
            f.write(decoded_data)
        else:
            # For other file types, write the content as-is
            f.write(decoded_data)
    
    return new_filepath

# main function to decompress the file
def decompress_file(filepath):
    try:
        with open(filepath, 'rb') as f:
            header = f.read(8)  # read the first 8 bytes (4 bytes for file type, 4 bytes for compression method)
            file_type, compression_method = struct.unpack('4s4s', header)
            file_type = file_type.decode('utf-8').strip('\x00').lower()  # remove any null bytes and convert to lowercase
            compression_method = compression_method.decode('utf-8').strip('\x00')

            compressed_data = f.read()  # read the rest of the file (the compressed data)
        
        # decompress the content
        decompressed_data = decompress_content(compressed_data, compression_method)
        
        # write the raw decompressed content to the appropriate file type
        new_filepath = write_decompressed_file(filepath, decompressed_data, file_type)
        
        print(f"File decompressed successfully! New file: {new_filepath}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Decompress .hrc files and output the original file type based on the header.")
    parser.add_argument("filepath", help="Path to the .hrc file to be decompressed")

    args = parser.parse_args()

    decompress_file(args.filepath)