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

def generate_checksums_for_directory(directory_path, excluded_items, checksum_size, is_debug_mode=False):
    """Generate checksums for all files in directory, excluding specified folders."""
    # To store file paths for checksum calculation
    files_to_process = []
    checksums = []
    diagnosis_data = []
    
    for root, dirs, files in os.walk(directory_path):
        # Exclude specified directories
        dirs[:] = [d for d in dirs if d not in excluded_items]
        files[:] = [f for f in files if f not in excluded_items]
        
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
            if (is_debug_mode):
                diagnosis_data.append("::CHECKSUM::{file_path} -> {checksum}".format(file_path=file_path, checksum=checksum))
    
    # sort checksums to ensure consistent final checksum
    checksums.sort()
    checksums_str =  ''.join(checksums)

    if (is_debug_mode):
        print("\n".join(diagnosis_data))
        print("\nFILES PROCESSED: {}\n\n".format(len(diagnosis_data)))

    final_checksum = hashlib.sha256(checksums_str.encode()).hexdigest()
    print(final_checksum[0:int(checksum_size)])
