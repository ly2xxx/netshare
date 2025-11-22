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
import traceback
from pathlib import Path
from urllib.parse import quote, unquote
from functools import wraps
from collections import defaultdict
from time import time

import qrcode
from flask import Flask, render_template, send_from_directory, send_file, abort, request, jsonify
from waitress import serve

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

# Configure Flask for large file streaming
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = AppConfig.SEND_FILE_MAX_AGE
app.config['MAX_CONTENT_LENGTH'] = None  # Remove any content length limit

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


def get_system_drives():
    """Get list of available drives (Windows) or root directories (Unix)"""
    import platform

    if platform.system() == 'Windows':
        # Windows: Get available drives
        import string
        drives = []
        for letter in string.ascii_uppercase:
            drive = f"{letter}:\\"
            if os.path.exists(drive):
                try:
                    # Try to access to verify it's available
                    os.listdir(drive)
                    drives.append({
                        'name': f"{letter}: Drive",
                        'path': drive,
                        'accessible': True
                    })
                except (PermissionError, OSError):
                    drives.append({
                        'name': f"{letter}: Drive",
                        'path': drive,
                        'accessible': False
                    })
        return drives
    else:
        # Unix/Linux/Mac: Start from home directory or root
        home = os.path.expanduser("~")
        return [{
            'name': 'Home',
            'path': home,
            'accessible': True
        }, {
            'name': 'Root',
            'path': '/',
            'accessible': os.access('/', os.R_OK)
        }]


def list_directories(path):
    """List subdirectories in the given path"""
    directories = []

    try:
        # Normalize path
        path = os.path.abspath(path)

        if not os.path.exists(path):
            return None, "Path does not exist"

        if not os.path.isdir(path):
            return None, "Path is not a directory"

        # Get parent directory
        parent = os.path.dirname(path) if path != os.path.dirname(path) else None

        # List all items in directory
        try:
            items = os.listdir(path)
        except PermissionError:
            return None, "Permission denied"

        # Filter to only directories
        for item in sorted(items):
            item_path = os.path.join(path, item)
            try:
                if os.path.isdir(item_path):
                    accessible = os.access(item_path, os.R_OK)
                    directories.append({
                        'name': item,
                        'path': item_path,
                        'accessible': accessible
                    })
            except (OSError, PermissionError):
                # Skip items we can't access
                continue

        return {
            'current_path': path,
            'parent': parent,
            'directories': directories
        }, None

    except Exception as e:
        logger.error(f"Error listing directories in {path}: {str(e)}")
        return None, str(e)


def validate_folder_path(path):
    """Validate folder path for security and accessibility"""
    import json

    # Normalize path
    path = os.path.abspath(path)

    # Check if exists
    if not os.path.exists(path):
        return False, "Path does not exist"

    # Check if directory
    if not os.path.isdir(path):
        return False, "Path is not a directory"

    # Check read permissions
    if not os.access(path, os.R_OK):
        return False, "No read permission for this directory"

    # Check if already shared
    if path in config.shared_folders:
        return False, "Folder is already shared"

    # Check for parent-child conflicts
    for existing in config.shared_folders:
        if path.startswith(existing + os.sep):
            return False, f"This folder is inside already shared folder: {os.path.basename(existing)}"
        if existing.startswith(path + os.sep):
            return False, f"Shared folder '{os.path.basename(existing)}' is inside this folder"

    # Check max folders limit
    if len(config.shared_folders) >= AppConfig.MAX_SHARED_FOLDERS:
        return False, f"Maximum of {AppConfig.MAX_SHARED_FOLDERS} folders allowed"

    return True, "Valid"


def save_folders_to_file():
    """Save shared folders list to JSON file"""
    import json

    try:
        config_path = os.path.join(os.path.dirname(__file__), AppConfig.FOLDERS_CONFIG_FILE)
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config.shared_folders, f, indent=2)
        logger.info(f"Saved {len(config.shared_folders)} folders to {config_path}")
        return True
    except Exception as e:
        logger.error(f"Failed to save folders: {e}")
        return False


def load_folders_from_file():
    """Load shared folders list from JSON file"""
    import json

    try:
        config_path = os.path.join(os.path.dirname(__file__), AppConfig.FOLDERS_CONFIG_FILE)
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                folders = json.load(f)

            # Validate each folder still exists
            valid_folders = []
            for folder in folders:
                if os.path.isdir(folder):
                    valid_folders.append(folder)
                else:
                    logger.warning(f"Skipping non-existent folder from config: {folder}")

            config.shared_folders = valid_folders
            logger.info(f"Loaded {len(valid_folders)} folders from {config_path}")
            return True
    except Exception as e:
        logger.error(f"Failed to load folders: {e}")

    return False


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


def is_video_file(filename):
    """Check if file is a video file"""
    video_extensions = ['.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm', '.m4v', '.mpg', '.mpeg', '.3gp']
    ext = os.path.splitext(filename)[1].lower()
    return ext in video_extensions


def get_video_mimetype(filename):
    """Get appropriate MIME type for video files"""
    ext = os.path.splitext(filename)[1].lower()
    mime_types = {
        '.mp4': 'video/mp4',
        '.mkv': 'video/x-matroska',
        '.avi': 'video/x-msvideo',
        '.mov': 'video/quicktime',
        '.wmv': 'video/x-ms-wmv',
        '.flv': 'video/x-flv',
        '.webm': 'video/webm',
        '.m4v': 'video/x-m4v',
        '.mpg': 'video/mpeg',
        '.mpeg': 'video/mpeg',
        '.3gp': 'video/3gpp'
    }
    return mime_types.get(ext, 'application/octet-stream')


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

        # Warn for very large files
        if file_size > 5 * 1024 * 1024 * 1024:  # > 5GB
            logger.warning(f"Large file warning: {format_size(file_size)} - Some mobile/VR browsers may not support files this large")
            logger.warning(f"Client: {request.headers.get('User-Agent', 'Unknown')}")

        # Pre-flight diagnostics
        try:
            logger.info(f"File size: {file_size} bytes ({format_size(file_size)})")
            logger.info(f"File readable: {os.access(target_path, os.R_OK)}")
            logger.info(f"Request headers: {dict(request.headers)}")

            # Check if user explicitly wants to download (via ?download=1 parameter)
            force_download = request.args.get('download', '0') == '1'

            # Determine if this is a video file
            is_video = is_video_file(target_path)

            # For video files, serve for streaming (inline) unless download is forced
            # This allows VR/mobile devices to play videos directly without downloading
            if is_video and not force_download:
                logger.info(f"Serving video file for streaming: {os.path.basename(target_path)}")
                response = send_file(
                    target_path,
                    as_attachment=False,  # Inline - allows browser to play/stream
                    conditional=True,  # Enable range requests for seeking
                    max_age=0,
                    mimetype=get_video_mimetype(target_path)
                )
            else:
                # Non-video files or forced download
                logger.info(f"Serving file for download: {os.path.basename(target_path)}")
                response = send_file(
                    target_path,
                    as_attachment=True,
                    download_name=os.path.basename(target_path),
                    conditional=True,
                    max_age=0,
                    mimetype='application/octet-stream'
                )

            logger.info(f"Response created successfully for {os.path.basename(target_path)}")
            logger.info(f"Response status: {response.status}")
            logger.info(f"Response headers: {dict(response.headers)}")
            return response

        except Exception as e:
            logger.error(f"Error serving file {target_path}: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            abort(500)
    
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
                # Check if file is large enough for multi-part download
                is_large = (not info['is_dir'] and
                           AppConfig.ENABLE_MULTIPART_DOWNLOAD and
                           info['size_bytes'] >= AppConfig.MULTIPART_THRESHOLD)

                num_parts = 0
                if is_large:
                    num_parts = (info['size_bytes'] + AppConfig.MULTIPART_CHUNK_SIZE - 1) // AppConfig.MULTIPART_CHUNK_SIZE

                items.append({
                    'name': item_name,
                    'is_dir': info['is_dir'],
                    'size': info['size'],
                    'size_bytes': info['size_bytes'],
                    'is_large': is_large,
                    'num_parts': num_parts
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


@app.route('/download-part/<int:folder_index>/<int:part_num>/<path:subpath>')
@rate_limit
def download_part(folder_index, part_num, subpath=''):
    """Download a specific part of a large file"""
    if folder_index >= len(config.shared_folders):
        logger.warning(f"Invalid folder index: {folder_index}")
        abort(404)

    base_folder = config.shared_folders[folder_index]
    target_path = os.path.join(base_folder, subpath)

    # Security: ensure we're still within the shared folder
    if not is_safe_path(base_folder, target_path):
        logger.warning(f"Path traversal attempt: {target_path}")
        abort(403)

    if not os.path.exists(target_path) or not os.path.isfile(target_path):
        abort(404)

    # Check if file download is allowed
    if not SecurityConfig.ALLOW_FILE_DOWNLOAD:
        abort(403)

    # Check file extension
    if not is_allowed_file(target_path):
        abort(403)

    # Get file size
    file_size = os.path.getsize(target_path)
    chunk_size = AppConfig.MULTIPART_CHUNK_SIZE

    # Calculate total parts
    total_parts = (file_size + chunk_size - 1) // chunk_size

    # Validate part number (1-indexed for user-friendly URLs)
    if part_num < 1 or part_num > total_parts:
        logger.warning(f"Invalid part number: {part_num} (total: {total_parts})")
        abort(404)

    # Calculate byte range for this part
    start_byte = (part_num - 1) * chunk_size
    end_byte = min(start_byte + chunk_size, file_size)
    part_size = end_byte - start_byte

    logger.info(f"Serving part {part_num}/{total_parts} of {os.path.basename(target_path)} ({format_size(part_size)})")
    logger.info(f"Byte range: {start_byte}-{end_byte-1} (total: {file_size})")

    try:
        # Open file and seek to start position
        def generate_chunk():
            with open(target_path, 'rb') as f:
                f.seek(start_byte)
                remaining = part_size
                read_size = 1024 * 1024  # Read 1MB at a time

                while remaining > 0:
                    chunk = f.read(min(read_size, remaining))
                    if not chunk:
                        break
                    remaining -= len(chunk)
                    yield chunk

        # Create response with appropriate filename
        filename = os.path.basename(target_path)
        part_filename = f"{os.path.splitext(filename)[0]}.part{part_num:03d}{os.path.splitext(filename)[1]}"

        from flask import Response
        response = Response(generate_chunk(), mimetype='application/octet-stream')
        response.headers['Content-Disposition'] = f'attachment; filename="{part_filename}"'
        response.headers['Content-Length'] = str(part_size)
        response.headers['X-Part-Number'] = str(part_num)
        response.headers['X-Total-Parts'] = str(total_parts)
        response.headers['X-Original-Filename'] = filename

        return response

    except Exception as e:
        logger.error(f"Error serving file part: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        abort(500)


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


@app.route('/qr-code')
@rate_limit
def get_qr_code():
    """Serve the QR code image"""
    qr_path = os.path.join(os.path.dirname(__file__), 'netshare_qr.png')

    if not os.path.exists(qr_path):
        # Regenerate if missing
        local_ip = get_local_ip()
        url = f"http://{local_ip}:{config.server_port}"
        qr_path = generate_qr_code(url)

    return send_from_directory(
        os.path.dirname(qr_path),
        os.path.basename(qr_path),
        mimetype='image/png'
    )


@app.route('/api/browse-filesystem')
@rate_limit
def api_browse_filesystem():
    """Browse server filesystem for folder selection"""
    try:
        path = request.args.get('path', '').strip()

        # If no path specified, return drives/roots
        if not path:
            drives = get_system_drives()
            return jsonify({
                'success': True,
                'drives': drives,
                'current_path': None,
                'parent': None,
                'directories': []
            }), 200

        # List directories in the specified path
        result, error = list_directories(path)

        if error:
            return jsonify({
                'success': False,
                'message': error
            }), 400

        return jsonify({
            'success': True,
            'current_path': result['current_path'],
            'parent': result['parent'],
            'directories': result['directories'],
            'drives': []
        }), 200

    except Exception as e:
        logger.error(f"Error browsing filesystem: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Internal server error'
        }), 500


@app.route('/api/folders', methods=['POST'])
@rate_limit
def api_add_folder():
    """Add a new shared folder"""
    try:
        data = request.get_json()

        if not data or 'path' not in data:
            return jsonify({
                'success': False,
                'message': 'Missing path parameter'
            }), 400

        folder_path = data['path'].strip()

        # Validate path
        is_valid, message = validate_folder_path(folder_path)

        if not is_valid:
            logger.warning(f"Invalid folder add attempt: {folder_path} - {message} from {request.remote_addr}")
            return jsonify({
                'success': False,
                'message': message
            }), 400

        # Add to shared folders
        config.shared_folders.append(folder_path)

        # Save to file for persistence
        save_folders_to_file()

        logger.info(f"Folder added: {folder_path} from {request.remote_addr}")

        return jsonify({
            'success': True,
            'message': f'Successfully added folder: {os.path.basename(folder_path)}',
            'folders': [
                {'index': idx, 'name': os.path.basename(p), 'path': p}
                for idx, p in enumerate(config.shared_folders)
            ]
        }), 200

    except Exception as e:
        logger.error(f"Error adding folder: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Internal server error'
        }), 500


@app.route('/api/folders/<int:folder_index>', methods=['DELETE'])
@rate_limit
def api_remove_folder(folder_index):
    """Remove a shared folder by index"""
    try:
        if folder_index < 0 or folder_index >= len(config.shared_folders):
            return jsonify({
                'success': False,
                'message': 'Invalid folder index'
            }), 400

        removed_path = config.shared_folders.pop(folder_index)

        # Save to file for persistence
        save_folders_to_file()

        logger.info(f"Folder removed: {removed_path} from {request.remote_addr}")

        return jsonify({
            'success': True,
            'message': f'Successfully removed folder: {os.path.basename(removed_path)}',
            'folders': [
                {'index': idx, 'name': os.path.basename(p), 'path': p}
                for idx, p in enumerate(config.shared_folders)
            ]
        }), 200

    except Exception as e:
        logger.error(f"Error removing folder: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Internal server error'
        }), 500


@app.errorhandler(Exception)
def handle_exception(e):
    """Global exception handler for debugging"""
    logger.error(f"Unhandled exception: {str(e)}")
    logger.error(f"Traceback: {traceback.format_exc()}")
    logger.error(f"Request: {request.method} {request.path}")
    logger.error(f"Client: {request.remote_addr}")

    # Return 500 error
    if request.path.startswith('/api/'):
        return jsonify({
            'success': False,
            'message': 'Internal server error'
        }), 500
    else:
        return render_template('error.html', error='Internal server error'), 500


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

    # Start production WSGI server (Waitress)
    # Waitress is better for large file transfers than Flask's dev server
    print("Starting production server with Waitress...")
    print("Optimized for large file transfers with parallel connections...")
    serve(
        app,
        host=config.host,
        port=port,
        threads=12,  # Increased for parallel downloads
        channel_timeout=600,  # 10 minutes for very large files
        send_bytes=65536,  # 64KB chunks for better throughput
        outbuf_overflow=10485760,  # 10MB buffer overflow
        asyncore_use_poll=True  # Better performance for many connections
    )


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

    # Try to load folders from saved config first
    load_folders_from_file()

    # Determine folders to share
    if args.gui:
        if not HAS_GUI:
            print("Error: GUI not available on this system.")
            print("Please use --folder option instead.")
            sys.exit(1)
        config.shared_folders = select_folders_gui()
        # Save GUI-selected folders
        if config.shared_folders:
            save_folders_to_file()
    elif args.folder:
        config.shared_folders = [os.path.abspath(f) for f in args.folder]
        # Save command-line folders
        save_folders_to_file()
    elif not config.shared_folders:
        # Interactive mode (only if no saved folders)
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

        # Save interactively-selected folders
        if config.shared_folders:
            save_folders_to_file()
    else:
        # Using saved folders from config file
        print(f"Loaded {len(config.shared_folders)} folder(s) from saved configuration")

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
