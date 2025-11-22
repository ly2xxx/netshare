#!/usr/bin/env python3
"""
NetShare File Part Reassembly Script
Reassembles multi-part downloaded files back into the original file
"""

import os
import sys
import glob

def reassemble_file(parts_pattern, output_file=None):
    """
    Reassemble file parts into original file

    Args:
        parts_pattern: Pattern to match part files (e.g., "movie.part*.mkv")
        output_file: Output filename (optional, auto-detected from parts)
    """
    # Find all matching part files
    part_files = sorted(glob.glob(parts_pattern))

    if not part_files:
        print(f"❌ No files found matching pattern: {parts_pattern}")
        return False

    print(f"Found {len(part_files)} part files:")
    for pf in part_files:
        size_mb = os.path.getsize(pf) / (1024 * 1024)
        print(f"  ✓ {pf} ({size_mb:.1f} MB)")

    # Auto-detect output filename from first part if not specified
    if not output_file:
        # Remove .partXXX from filename
        import re
        output_file = re.sub(r'\.part\d+', '', part_files[0])
        print(f"\n📝 Output file: {output_file}")

    # Check if output file already exists
    if os.path.exists(output_file):
        response = input(f"⚠️  Output file '{output_file}' already exists. Overwrite? (y/N): ")
        if response.lower() != 'y':
            print("Aborted.")
            return False

    # Reassemble parts
    print(f"\n🔧 Reassembling {len(part_files)} parts...")
    total_bytes = 0

    try:
        with open(output_file, 'wb') as outfile:
            for i, part_file in enumerate(part_files, 1):
                print(f"  [{i}/{len(part_files)}] Reading {os.path.basename(part_file)}...")
                with open(part_file, 'rb') as infile:
                    chunk_size = 1024 * 1024  # 1MB chunks
                    while True:
                        chunk = infile.read(chunk_size)
                        if not chunk:
                            break
                        outfile.write(chunk)
                        total_bytes += len(chunk)

        total_mb = total_bytes / (1024 * 1024)
        total_gb = total_bytes / (1024 * 1024 * 1024)

        if total_gb >= 1:
            size_str = f"{total_gb:.2f} GB"
        else:
            size_str = f"{total_mb:.1f} MB"

        print(f"\n✅ Successfully reassembled file!")
        print(f"📦 Output: {output_file}")
        print(f"📊 Size: {size_str}")

        # Ask if user wants to delete parts
        response = input(f"\n🗑️  Delete part files? (y/N): ")
        if response.lower() == 'y':
            for part_file in part_files:
                os.remove(part_file)
                print(f"  Deleted: {part_file}")
            print("✅ Part files deleted.")

        return True

    except Exception as e:
        print(f"\n❌ Error during reassembly: {e}")
        return False


def main():
    print("=" * 60)
    print("NetShare - File Part Reassembly Tool")
    print("=" * 60)
    print()

    if len(sys.argv) < 2:
        print("Usage:")
        print(f"  {sys.argv[0]} <parts_pattern> [output_file]")
        print()
        print("Examples:")
        print(f"  {sys.argv[0]} 'movie.part*.mkv'")
        print(f"  {sys.argv[0]} 'video.part*.mp4' output.mp4")
        print()
        print("The script will automatically find all part files and")
        print("reassemble them into the original file.")
        sys.exit(1)

    parts_pattern = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    success = reassemble_file(parts_pattern, output_file)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
