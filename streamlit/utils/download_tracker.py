"""
Download tracking utility for logging QR code downloads
Thread-safe CSV-based tracking with file locking support
"""

import csv
import sys
from datetime import datetime
from pathlib import Path


def log_download(filename: str) -> None:
    """
    Log a QR code download event to track.csv

    Args:
        filename: Name of the downloaded file

    Thread-safe implementation using file locking
    """
    # CSV file path (parent directory of utils/)
    csv_path = Path(__file__).parent.parent / "track.csv"
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    try:
        # Create file with headers if it doesn't exist
        if not csv_path.exists():
            with open(csv_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['filename', 'timestamp'])

        # Append with exclusive lock (prevents concurrent write corruption)
        with open(csv_path, 'a', newline='') as f:
            # Acquire exclusive lock (blocks other processes)
            try:
                import fcntl
                fcntl.flock(f.fileno(), fcntl.LOCK_EX)
            except (ImportError, AttributeError):
                # fcntl not available on Windows, skip locking
                pass

            try:
                writer = csv.writer(f)
                writer.writerow([filename, timestamp])
            finally:
                # Release lock if fcntl is available
                try:
                    import fcntl
                    fcntl.flock(f.fileno(), fcntl.LOCK_UN)
                except (ImportError, AttributeError):
                    pass
    except Exception as e:
        # Silent failure - don't interrupt user experience
        print(f"Warning: Failed to log download: {e}", file=sys.stderr)


def get_download_count() -> int:
    """
    Read and count total downloads from track.csv

    Returns:
        Number of downloads, or 0 if file doesn't exist or error occurs
    """
    csv_path = Path(__file__).parent.parent / "track.csv"

    try:
        if not csv_path.exists():
            return 0

        with open(csv_path, 'r', newline='') as f:
            reader = csv.reader(f)
            # Skip header row
            next(reader, None)
            # Count remaining rows
            count = sum(1 for _ in reader)
            return count
    except Exception as e:
        # Return 0 on error (graceful degradation)
        print(f"Warning: Failed to read download count: {e}", file=sys.stderr)
        return 0
