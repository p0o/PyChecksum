from .checksum import generate_checksums_for_directory
import argparse

# Directory to scan, adjust to your requirement
directory_path = '.'

def main():
    parser = argparse.ArgumentParser(
        prog='pychecksum',
        description='Create a checksum from the content of a directory',
        epilog='Thanks for using PyChecksum!'
    )

    parser.add_argument('-d', '--directory', help='Directory to scan, default is .', default=directory_path)
    parser.add_argument('-e', '--exclude', help='Files or sub directories to exclude from the scan', nargs='+', default=[])
    parser.add_argument('-s', '--size', help='Checksum size, default to SHA256 64 characters', default=64)
    parser.add_argument('-dd', '--debug', help='Provide diagnosis data in the standard output', action='store_true')

    args = parser.parse_args()
    generate_checksums_for_directory(args.directory, args.exclude, args.size, args.debug)

if __name__ == "__main__":
    main()