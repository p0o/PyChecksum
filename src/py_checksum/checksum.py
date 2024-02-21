import os
import hashlib
from concurrent.futures import ThreadPoolExecutor, as_completed

def calculate_checksum(file_path):
    """Calculate SHA256 checksum of a file."""
    sha256_hash = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return file_path, sha256_hash.hexdigest()
    except Exception as e:
        return ""

def generate_checksums_for_directory(directory_path, excluded_folders, checksum_size):
    """Generate checksums for all files in directory, excluding specified folders."""
    # To store file paths for checksum calculation
    files_to_process = []
    checksums = []
    
    for root, dirs, files in os.walk(directory_path):
        # Exclude specified directories
        dirs[:] = [d for d in dirs if d not in excluded_folders]
        
        for file in files:
            file_path = os.path.join(root, file)
            files_to_process.append(file_path)
    
    # Using ThreadPoolExecutor to parallelize checksum computation
    with ThreadPoolExecutor() as executor:
        future_to_file = {executor.submit(calculate_checksum, file_path): file_path for file_path in files_to_process}
        for future in as_completed(future_to_file):
            file_path = future_to_file[future]
            file_path, checksum = future.result()
            checksums.append(checksum)
    
    # sort checksums to ensure consistent final checksum
    checksums.sort()
    checksums_str =  ''.join(checksums)

    final_checksum = hashlib.sha256(checksums_str.encode()).hexdigest()
    print(final_checksum[0:int(checksum_size)])
