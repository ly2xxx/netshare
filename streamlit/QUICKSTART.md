# Quick Start Guide

## Installation & Setup

### Step 1: Install Dependencies

```bash
cd /mnt/h/code/yl/netshare/streamlit
pip install -r requirements.txt
```

**Note for Linux users**: You may need to install additional system packages for QR code scanning:

```bash
# Ubuntu/Debian
sudo apt-get install libzbar0

# Fedora
sudo dnf install zbar

# Arch Linux
sudo pacman -S zbar
```

### Step 2: Verify Installation

Test that all modules work correctly:

```bash
python3 -c "from greeting_formats import create_holiday_greeting; print('✅ Installation successful!')"
```

### Step 3: Launch the App

**Option A - Using launcher script (Linux/Mac)**:
```bash
./run.sh
```

**Option B - Using launcher script (Windows)**:
```batch
run.bat
```

**Option C - Direct command**:
```bash
streamlit run app.py
```

The app will automatically open in your browser at `http://localhost:8501`

## First Steps

### Create Your First Greeting

1. Navigate to the **"Create Greeting"** tab
2. Fill in the form:
   - **From**: Your name (e.g., "Alice")
   - **To**: Recipient name (e.g., "Bob")
   - **Occasion**: Select "Christmas 2025" or custom
   - **Theme**: Choose "snowflake" for a festive look
   - **Message**: Write your greeting (e.g., "Merry Christmas! Wishing you joy!")
3. Click **"Generate QR Code"**
4. Download the QR code image
5. Share it via email, messaging, or print it!

### Test Scanning

1. Navigate to the **"Scan QR Code"** tab
2. Upload the QR code you just created
3. View your decoded greeting message

## Example Usage

### Command Line Test

You can also test the greeting creation from command line:

```bash
cd /mnt/h/code/yl/netshare/streamlit

python3 << 'EOF'
from greeting_formats import create_holiday_greeting, compact_greeting
import qrcode
from PIL import Image

# Create greeting
greeting = create_holiday_greeting(
    from_name="Alice",
    to_name="Bob",
    message="Merry Christmas! 🎄",
    occasion="Christmas 2025",
    theme="snowflake"
)

# Generate QR code
greeting_json = compact_greeting(greeting)
qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_H)
qr.add_data(greeting_json)
qr.make(fit=True)

# Save QR code
img = qr.make_image(fill_color="black", back_color="white")
img.save("test_greeting.png")
print("✅ QR code saved to test_greeting.png")
print(f"📦 Data size: {len(greeting_json)} bytes")
EOF
```

## Troubleshooting

### Import Errors

If you see `ModuleNotFoundError`, install dependencies:
```bash
pip install -r requirements.txt
```

### QR Scanning Not Working

If QR scanning fails, make sure pyzbar and system libraries are installed:

```bash
# Install Python package
pip install pyzbar

# Install system library (Linux)
sudo apt-get install libzbar0
```

### Streamlit Won't Start

Make sure you're in the correct directory:
```bash
cd /mnt/h/code/yl/netshare/streamlit
pwd  # Should show the streamlit directory
ls   # Should show app.py
```

### Port Already in Use

If port 8501 is busy, specify a different port:
```bash
streamlit run app.py --server.port 8502
```

## Project Structure

```
streamlit/
├── app.py                    # Main Streamlit application
├── greeting_formats.py       # Greeting encoding/decoding
├── requirements.txt          # Python dependencies
├── README.md                # Full documentation
├── QUICKSTART.md            # This file
├── run.sh                   # Launch script (Linux/Mac)
├── run.bat                  # Launch script (Windows)
└── .streamlit/
    └── config.toml          # App configuration
```

## Next Steps

- Explore the **Examples** tab for inspiration
- Read the **About** tab for technical details
- Check **README.md** for comprehensive documentation
- Create multiple greetings for different occasions!

## Support

For detailed information, see [README.md](README.md)

For issues with:
- **netshare package**: Check PyPI page
- **Streamlit**: Visit [streamlit.io/docs](https://streamlit.io/docs)
- **QR codes**: Review the About tab in the app

---

Happy greeting! 🎄✨
