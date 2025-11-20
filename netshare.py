#!/usr/bin/env python3
"""
NetShare - Simple Network File Sharing Tool
Share Windows folders with Android devices over WiFi
"""

import os
import socket
import sys
import threading
import webbrowser
import logging
from pathlib import Path
from urllib.parse import quote, unquote
from functools import wraps
from collections import defaultdict
from time import time

import qrcode
from flask import Flask, render_template, send_from_directory, abort, request, jsonify

# Import configuration
try:
    from config import SecurityConfig, AppConfig
except ImportError:
    # Fallback if config.py is not available
    class SecurityConfig:
        MAX_FILE_SIZE = 10 * 1024 * 1024 * 1024
        BLOCKED_EXTENSIONS = ['.exe', '.bat', '.cmd', '.sh', '.ps1']
        ALLOW_DIRECTORY_LISTING = True
        ALLOW_FILE_DOWNLOAD = True
        MAX_PATH_DEPTH = 20
        RATE_LIMIT = 100
        DEBUG_ERRORS = False
        ALLOWED_EXTENSIONS = []
    
    class AppConfig:
        DEFAULT_PORT = 5000
        DEFAULT_HOST = '0.0.0.0'
        SERVER_NAME = "NetShare"
        VERSION = "1.0.0"
        ENABLE_ACCESS_LOG = True

# Try to import tkinter for GUI (optional on some systems)
try:
    import tkinter as tk
    from tkinter import filedialog, messagebox
    HAS_GUI = True
except ImportError:
    HAS_GUI = False
    print("Warning: tkinter not available. GUI folder selection disabled.")

app = Flask(__name__)

# Configure logging
if AppConfig.ENABLE_ACCESS_LOG:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)
else:
    logger = logging.getLogger(__name__)
    logger.addHandler(logging.NullHandler())

# Rate limiting storage
rate_limit_storage = defaultdict(list)


def rate_limit(f):
    """Rate limiting decorator"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not SecurityConfig.RATE_LIMIT:
            return f(*args, **kwargs)
        
        ip = request.remote_addr
        now = time()
        
        # Clean old requests
        rate_limit_storage[ip] = [
            req_time for req_time in rate_limit_storage[ip]
            if now - req_time < 60
        ]
        
        # Check rate limit
        if len(rate_limit_storage[ip]) >= SecurityConfig.RATE_LIMIT:
            logger.warning(f"Rate limit exceeded for {ip}")
            abort(429)  # Too Many Requests
        
        rate_limit_storage[ip].append(now)
        return f(*args, **kwargs)
    
    return decorated_function


def is_safe_path(base_path, target_path):
    """Verify that target_path is within base_path (prevents path traversal)"""
    base_path = os.path.abspath(base_path)
    target_path = os.path.abspath(target_path)
    
    # Check if target is within base
    if not target_path.startswith(base_path):
        return False
    
    # Check path depth
    relative_path = os.path.relpath(target_path, base_path)
    depth = len(Path(relative_path).parts)
    if depth > SecurityConfig.MAX_PATH_DEPTH:
        logger.warning(f"Path depth exceeded: {relative_path}")
        return False
    
    return True


def is_allowed_file(filename):
    """Check if file extension is allowed"""
    ext = os.path.splitext(filename)[1].lower()
    
    # Check blocked extensions first
    if ext in SecurityConfig.BLOCKED_EXTENSIONS:
        logger.warning(f"Blocked file extension: {ext}")
        return False
    
    # If allowed list is specified, check it
    if SecurityConfig.ALLOWED_EXTENSIONS:
        return ext in SecurityConfig.ALLOWED_EXTENSIONS
    
    return True

# Global configuration
class Config:
    """Application configuration"""
    shared_folders = []
    server_port = 5000
    host = '0.0.0.0'
    
config = Config()


def get_local_ip():
    """Get the local IP address of this machine"""
    try:
        # Create a socket to determine local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        return "127.0.0.1"


def generate_qr_code(url):
    """Generate QR code for the given URL"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    # Save as PNG
    img = qr.make_image(fill_color="black", back_color="white")
    qr_path = os.path.join(os.path.dirname(__file__), 'netshare_qr.png')
    img.save(qr_path)
    
    # Print to terminal
    print("\n" + "="*50)
    print("Scan this QR code with your mobile device:")
    print("="*50)
    qr.print_ascii(invert=True)
    print("="*50)
    print(f"QR code saved to: {qr_path}")
    
    return qr_path


def format_size(size_bytes):
    """Format file size in human-readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} PB"


def get_file_info(filepath):
    """Get file information including size and type"""
    stat_info = os.stat(filepath)
    return {
        'size': format_size(stat_info.st_size),
        'size_bytes': stat_info.st_size,
        'is_dir': os.path.isdir(filepath)
    }


@app.route('/')
@rate_limit
def index():
    """Home page showing all shared folders"""
    folders = []
    for folder_path in config.shared_folders:
        if os.path.exists(folder_path):
            folders.append({
                'name': os.path.basename(folder_path),
                'path': folder_path,
                'full_path': folder_path
            })
    
    return render_template('index.html', 
                         folders=folders,
                         server_url=f"http://{get_local_ip()}:{config.server_port}")


@app.route('/browse/<int:folder_index>')
@app.route('/browse/<int:folder_index>/<path:subpath>')
@rate_limit
def browse(folder_index, subpath=''):
    """Browse files in a shared folder"""
    if folder_index >= len(config.shared_folders):
        logger.warning(f"Invalid folder index: {folder_index}")
        abort(404)
    
    base_folder = config.shared_folders[folder_index]
    target_path = os.path.join(base_folder, subpath)
    
    # Security: ensure we're still within the shared folder
    if not is_safe_path(base_folder, target_path):
        logger.warning(f"Path traversal attempt: {target_path}")
        abort(403)
    
    if not os.path.exists(target_path):
        abort(404)
    
    # If it's a file, serve it
    if os.path.isfile(target_path):
        # Check if file download is allowed
        if not SecurityConfig.ALLOW_FILE_DOWNLOAD:
            logger.warning(f"File download disabled: {target_path}")
            abort(403)
        
        # Check file extension
        if not is_allowed_file(target_path):
            logger.warning(f"Blocked file access: {target_path}")
            abort(403)
        
        # Check file size
        file_size = os.path.getsize(target_path)
        if file_size > SecurityConfig.MAX_FILE_SIZE:
            logger.warning(f"File too large: {target_path} ({file_size} bytes)")
            abort(413)  # Request Entity Too Large
        
        logger.info(f"Serving file: {target_path} to {request.remote_addr}")
        
        return send_from_directory(
            os.path.dirname(target_path),
            os.path.basename(target_path),
            as_attachment=True
        )
    
    # If it's a directory, list contents
    if not SecurityConfig.ALLOW_DIRECTORY_LISTING:
        logger.warning(f"Directory listing disabled: {target_path}")
        abort(403)
    
    items = []
    try:
        for item_name in sorted(os.listdir(target_path)):
            item_path = os.path.join(target_path, item_name)
            try:
                # Skip if file extension is blocked
                if os.path.isfile(item_path) and not is_allowed_file(item_path):
                    continue
                
                info = get_file_info(item_path)
                items.append({
                    'name': item_name,
                    'is_dir': info['is_dir'],
                    'size': info['size'],
                    'size_bytes': info['size_bytes']
                })
            except (OSError, PermissionError):
                # Skip files we can't access
                continue
    except (OSError, PermissionError) as e:
        error_msg = "Cannot access folder" if not SecurityConfig.DEBUG_ERRORS else str(e)
        return render_template('error.html', error=error_msg), 403
    
    # Build breadcrumb navigation
    breadcrumbs = []
    if subpath:
        parts = subpath.split(os.sep)
        current_path = ''
        for part in parts:
            current_path = os.path.join(current_path, part) if current_path else part
            breadcrumbs.append({
                'name': part,
                'path': current_path
            })
    
    return render_template('browse.html',
                         folder_index=folder_index,
                         folder_name=os.path.basename(base_folder),
                         current_path=subpath,
                         breadcrumbs=breadcrumbs,
                         items=items)


@app.route('/api/folders', methods=['GET'])
@rate_limit
def api_folders():
    """API endpoint to get list of shared folders"""
    folders = []
    for idx, folder_path in enumerate(config.shared_folders):
        if os.path.exists(folder_path):
            folders.append({
                'index': idx,
                'name': os.path.basename(folder_path),
                'path': folder_path
            })
    return jsonify(folders)


def select_folders_gui():
    """GUI for selecting folders to share"""
    if not HAS_GUI:
        print("Error: GUI not available. Please use command-line mode.")
        return []
    
    root = tk.Tk()
    root.withdraw()  # Hide main window
    
    folders = []
    while True:
        folder = filedialog.askdirectory(
            title="Select a folder to share (Cancel to finish)"
        )
        if not folder:
            break
        folders.append(folder)
        
        result = messagebox.askyesno(
            "Add More?",
            f"Added: {folder}\n\nDo you want to add another folder?"
        )
        if not result:
            break
    
    root.destroy()
    return folders


def start_server(port=5000):
    """Start the Flask server"""
    local_ip = get_local_ip()
    url = f"http://{local_ip}:{port}"
    
    print("\n" + "="*60)
    print(f"NetShare Server Started!")
    print("="*60)
    print(f"Local URL: {url}")
    print(f"Sharing {len(config.shared_folders)} folder(s)")
    for idx, folder in enumerate(config.shared_folders):
        print(f"  [{idx}] {folder}")
    print("="*60)
    
    # Generate QR code
    generate_qr_code(url)
    
    print("\nTo stop the server, press Ctrl+C")
    print("="*60 + "\n")
    
    # Try to open browser
    try:
        threading.Timer(1.5, lambda: webbrowser.open(url)).start()
    except:
        pass
    
    # Start Flask server
    app.run(host=config.host, port=port, debug=False, threaded=True)


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='NetShare - Share folders over local network',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  netshare.py --gui                    # Use GUI to select folders
  netshare.py --folder /path/to/share  # Share specific folder
  netshare.py --folder "C:\\Users\\Documents" --port 8000
        """
    )
    
    parser.add_argument('--gui', action='store_true',
                       help='Use GUI to select folders')
    parser.add_argument('--folder', '-f', action='append',
                       help='Folder to share (can be specified multiple times)')
    parser.add_argument('--port', '-p', type=int, default=5000,
                       help='Port to run server on (default: 5000)')
    
    args = parser.parse_args()
    
    # Determine folders to share
    if args.gui:
        if not HAS_GUI:
            print("Error: GUI not available on this system.")
            print("Please use --folder option instead.")
            sys.exit(1)
        config.shared_folders = select_folders_gui()
    elif args.folder:
        config.shared_folders = [os.path.abspath(f) for f in args.folder]
    else:
        # Interactive mode
        print("NetShare - Network File Sharing Tool")
        print("="*50)
        print("Enter folders to share (one per line, empty line to finish):")
        
        while True:
            folder = input("Folder path: ").strip()
            if not folder:
                break
            if os.path.isdir(folder):
                config.shared_folders.append(os.path.abspath(folder))
                print(f"  ✓ Added: {folder}")
            else:
                print(f"  ✗ Not a valid folder: {folder}")
        
    if not config.shared_folders:
        print("\nNo folders selected. Exiting.")
        sys.exit(0)
    
    # Validate all folders exist
    valid_folders = []
    for folder in config.shared_folders:
        if os.path.isdir(folder):
            valid_folders.append(folder)
        else:
            print(f"Warning: Skipping non-existent folder: {folder}")
    
    config.shared_folders = valid_folders
    
    if not config.shared_folders:
        print("\nNo valid folders to share. Exiting.")
        sys.exit(0)
    
    config.server_port = args.port
    
    # Start the server
    try:
        start_server(config.server_port)
    except KeyboardInterrupt:
        print("\n\nServer stopped.")
    except Exception as e:
        print(f"\nError starting server: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
