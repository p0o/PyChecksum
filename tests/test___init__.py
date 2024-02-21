import unittest
import os
import hashlib
from py_checksum.checksum import calculate_checksum, generate_checksums_for_directory

class TestChecksum(unittest.TestCase):
    def test_calculate_checksum(self):
        # Test with a small file
        file_path = "test_file.txt"
        with open(file_path, "w") as f:
            f.write("This is a test file.")
        expected_checksum = hashlib.sha256("This is a test file.".encode()).hexdigest()
        self.assertEqual(calculate_checksum(file_path), (file_path, expected_checksum))

        # Test with a non-existent file
        non_existent_file = "non_existent_file.txt"
        expected_error = f"Error calculating checksum: [Errno 2] No such file or directory: '{non_existent_file}'"
        self.assertEqual(calculate_checksum(non_existent_file), (non_existent_file, expected_error))

    def test_generate_checksums_for_directory(self):
        # Create a temporary directory with some files
        directory_path = "test_directory"
        os.makedirs(directory_path)
        file1_path = os.path.join(directory_path, "file1.txt")
        file2_path = os.path.join(directory_path, "file2.txt")
        with open(file1_path, "w") as f:
            f.write("This is file 1.")
        with open(file2_path, "w") as f:
            f.write("This is file 2.")

        # Test with excluded folders
        excluded_folders = ["subfolder"]
        os.makedirs(os.path.join(directory_path, "subfolder"))
        os.makedirs(os.path.join(directory_path, "excluded_folder"))
        file3_path = os.path.join(directory_path, "excluded_folder", "file3.txt")
        with open(file3_path, "w") as f:
            f.write("This is file 3.")
        expected_checksums = [
            hashlib.sha256("This is file 1.".encode()).hexdigest(),
            hashlib.sha256("This is file 2.".encode()).hexdigest()
        ]
        self.assertEqual(generate_checksums_for_directory(directory_path, excluded_folders, 64), expected_checksums)

        # Clean up the temporary directory
        os.remove(file1_path)
        os.remove(file2_path)
        os.remove(file3_path)
        os.rmdir(os.path.join(directory_path, "subfolder"))
        os.rmdir(os.path.join(directory_path, "excluded_folder"))
        os.rmdir(directory_path)

if __name__ == "__main__":
    unittest.main()