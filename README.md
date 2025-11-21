# NetShare

A secure, Python-based network file sharing tool that enables easy sharing of folders from Windows, Mac, or Linux computers to Android devices, Quest VR headsets, and other devices over your local WiFi network.

## 🚀 Features

- **🔒 Security First**: Built-in rate limiting, file extension filtering, and path traversal protection
- **📱 Mobile Friendly**: QR code generation for instant mobile access
- **🎯 Simple Setup**: GUI and command-line options for easy folder selection
- **⚡ Fast Transfer**: Direct WiFi connection with no external servers
- **🛡️ Configurable Security**: Customizable file size limits, extension blocking, and access controls
- **🌐 Cross-Platform**: Works on Windows, macOS, and Linux
- **📊 Access Logging**: Optional request logging for monitoring

## 📋 Requirements

- Python 3.7 or higher
- Local WiFi network (same network for sharing device and receiving device)
- Modern web browser on receiving device

## 🔧 Installation

### Quick Install

1. **Clone or download this repository**:
   ```bash
   git clone https://github.com/yourusername/netshare.git
   cd netshare
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run NetShare**:
   ```bash
   python netshare.py --gui
   ```

### Using Virtual Environment (Recommended)

1. **Create virtual environment**:
   ```bash
   python -m venv netshare-env

   # Windows
   netshare-env\Scripts\activate

   # macOS/Linux
   source netshare-env/bin/activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python netshare.py --gui
   ```

## 🚀 Quick Start

### Method 1: GUI Mode (Easiest)
```bash
python netshare.py --gui
```
1. Select folders using the graphical interface
2. Server starts automatically
3. Scan the QR code with your mobile device or use the displayed URL

### Method 2: Command Line
```bash
python netshare.py --folder "C:\Users\YourName\Documents" --port 8000
```

### Method 3: Interactive Mode
```bash
python netshare.py
```
Follow the prompts to enter folder paths.

## 📖 Detailed Usage

### Command Line Options

```bash
python netshare.py [options]

Options:
  --gui                 Use GUI to select folders
  --folder FOLDER       Folder to share (can be used multiple times)
  --port PORT          Port to run server on (default: 5000)
  -h, --help           Show help message

Examples:
  netshare.py --gui                                    # GUI mode
  netshare.py --folder /path/to/share                  # Share single folder
  netshare.py --folder "C:\Documents" --folder "C:\Pictures" --port 8000   # Multiple folders, custom port
```

### Accessing Shared Files

1. **Start NetShare** using any method above
2. **Note the server URL** displayed in the terminal (e.g., `http://192.168.1.100:5000`)
3. **On your mobile/target device**:
   - Scan the QR code with your camera app, OR
   - Open a web browser and navigate to the displayed URL
4. **Browse and download** files through the web interface

### Using the Web Interface

- **Home Page**: Shows all shared folders
- **Browse**: Click folders to navigate directory structure
- **Download**: Click files to download them
- **Breadcrumbs**: Use the navigation path to go back to parent folders

## 🔧 Configuration

### Security Settings

Edit `config.py` to customize security settings:

```python
class SecurityConfig:
    # Maximum file size to serve (10GB default)
    MAX_FILE_SIZE = 10 * 1024 * 1024 * 1024

    # Block dangerous file extensions
    BLOCKED_EXTENSIONS = ['.exe', '.bat', '.cmd', '.sh', '.ps1']

    # Allow only specific extensions (empty = allow all)
    ALLOWED_EXTENSIONS = []  # e.g., ['.pdf', '.jpg', '.mp4']

    # Enable/disable features
    ALLOW_DIRECTORY_LISTING = True
    ALLOW_FILE_DOWNLOAD = True

    # Security limits
    MAX_PATH_DEPTH = 20
    RATE_LIMIT = 100  # requests per minute per IP
```

### Application Settings

```python
class AppConfig:
    DEFAULT_PORT = 5000
    SERVER_NAME = "NetShare"
    ENABLE_ACCESS_LOG = True  # Log all requests
```

## 🛠️ Advanced Usage

### Custom Port Configuration
```bash
# Use a different port if 5000 is occupied
python netshare.py --folder ~/Documents --port 8080
```

### Multiple Folder Sharing
```bash
# Share multiple folders simultaneously
python netshare.py --folder ~/Documents --folder ~/Pictures --folder ~/Downloads
```

### Running as Background Service
```bash
# Run in background (Linux/macOS)
nohup python netshare.py --folder ~/shared &

# Windows (run in separate command window)
start python netshare.py --folder C:\Shared
```

## 📱 Mobile Access Tips

### Android Devices
1. Use any web browser (Chrome, Firefox, etc.)
2. QR code scanner apps work with the generated codes
3. Bookmark the URL for easy future access

### Quest VR Headsets
1. Use the built-in browser
2. QR code scanning may require companion mobile app
3. Save URL in browser bookmarks for easy access

### iOS Devices
1. Use Safari or any web browser
2. Camera app can scan QR codes directly
3. Add to home screen for app-like experience

## 🚨 Troubleshooting

### Connection Issues

**Problem**: Cannot access from mobile device
```bash
Solutions:
1. Ensure both devices are on the same WiFi network
2. Check if firewall is blocking the port (5000 by default)
3. Try a different port: --port 8080
4. Verify the IP address is correct
```

**Problem**: "Connection refused" error
```bash
Solutions:
1. Make sure NetShare server is running
2. Check if another application is using the port
3. Try running as administrator (Windows) or with sudo (Linux/Mac)
```

### File Access Issues

**Problem**: Cannot download certain files
```bash
Solutions:
1. Check BLOCKED_EXTENSIONS in config.py
2. Verify file size under MAX_FILE_SIZE limit
3. Ensure ALLOW_FILE_DOWNLOAD = True in config.py
```

**Problem**: Folders not showing
```bash
Solutions:
1. Verify folder paths exist and are accessible
2. Check ALLOW_DIRECTORY_LISTING = True in config.py
3. Ensure proper read permissions on folders
```

### Network Connectivity

**Problem**: QR code doesn't work
```bash
Solutions:
1. Manually type the URL into browser
2. Check IP address is reachable: ping [IP_ADDRESS]
3. Restart router if needed
4. Use different QR code scanner app
```

### Performance Issues

**Problem**: Slow file transfers
```bash
Solutions:
1. Check WiFi signal strength
2. Reduce MAX_FILE_SIZE if memory limited
3. Close other network applications
4. Use 5GHz WiFi band if available
```

## 🔐 Security Best Practices

### Recommended Security Settings

1. **Limit file types**:
   ```python
   ALLOWED_EXTENSIONS = ['.pdf', '.jpg', '.png', '.mp4', '.doc', '.txt']
   ```

2. **Reduce file size limits** for better performance:
   ```python
   MAX_FILE_SIZE = 1 * 1024 * 1024 * 1024  # 1GB
   ```

3. **Enable access logging** to monitor usage:
   ```python
   ENABLE_ACCESS_LOG = True
   ```

4. **Use non-default ports** to reduce discovery:
   ```bash
   python netshare.py --folder ~/Documents --port 8543
   ```

### Network Security

- **Use on trusted networks only** (home/office WiFi)
- **Avoid public WiFi** for file sharing
- **Stop the server** when not needed (Ctrl+C)
- **Monitor access logs** for unusual activity
- **Share only necessary folders**, not entire drives

## 🔧 API Reference

NetShare provides a simple REST API:

### Get Shared Folders
```http
GET /api/folders
```
Returns JSON list of available shared folders.

Example response:
```json
[
  {
    "index": 0,
    "name": "Documents",
    "path": "/home/user/Documents"
  }
]
```

## 🏗️ Architecture

```
NetShare Architecture:

┌─────────────────┐    ┌──────────────┐    ┌─────────────────┐
│   Mobile Device │────│  WiFi Router │────│  NetShare Host  │
│   (Browser)     │    │              │    │  (Python Flask) │
└─────────────────┘    └──────────────┘    └─────────────────┘
         │                                           │
         │              HTTP Requests                │
         └───────────────────────────────────────────┘
                        (Port 5000)

Components:
- Flask web server for HTTP requests
- QR code generator for easy mobile access
- Security middleware for safe file access
- Path validation to prevent directory traversal
- Rate limiting to prevent abuse
```

## 📝 Technical Notes

### Dependencies
- **Flask 3.0.0**: Web server framework
- **qrcode 7.4.2**: QR code generation
- **Pillow 10.1.0**: Image processing for QR codes

### File Structure
```
netshare/
├── netshare.py      # Main application
├── config.py        # Configuration settings
├── requirements.txt # Python dependencies
└── README.md       # This documentation
```

### Supported File Operations
- ✅ Download files
- ✅ Browse directories
- ✅ View file information (size, type)
- ❌ Upload files (not supported)
- ❌ Delete files (not supported)
- ❌ Modify files (not supported)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source. Please check the repository for license details.

## 🆘 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Verify your Python and dependency versions
3. Check firewall and network settings
4. Review the access logs for error details

For persistent issues, please create an issue in the repository with:
- Operating system and Python version
- Complete error messages
- Steps to reproduce the problem

---

**⚠️ Security Notice**: NetShare is designed for local network file sharing. Only use on trusted networks and share folders containing non-sensitive files. Always stop the server when not in use.
