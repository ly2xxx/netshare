https://qr-greeting.streamlit.app/

![qr](greeting.png)

# Holiday Greeting QR Code Generator

A beautiful Streamlit web application for creating and sharing personalized holiday greetings via QR codes.

## Features

- 🎁 **Create Custom Greetings**: Generate personalized holiday greeting QR codes
- 📱 **Scan QR Codes**: Upload and decode greeting QR codes to view messages
- 🎨 **Multiple Themes**: Choose from various holiday themes (snowflake, fireworks, lights, etc.)
- 📥 **Download & Share**: Download QR codes as PNG images
- 💾 **Compact Format**: Efficient JSON encoding for optimal QR code size

## Installation

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- streamlit - Web interface framework
- netshare - Network sharing and QR utilities
- qrcode - QR code generation
- Pillow - Image processing
- opencv-python-headless - Image processing for QR scanning
- pyzbar - QR code decoding

### Linux Additional Requirements

For QR code scanning on Linux, you may need to install zbar:

```bash
# Ubuntu/Debian
sudo apt-get install libzbar0

# Fedora
sudo dnf install zbar

# Arch
sudo pacman -S zbar
```

## Usage

### Start the Application

```bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`

### Create a Greeting

1. Go to the "Create Greeting" tab
2. Fill in:
   - **From**: Your name
   - **To**: Recipient's name
   - **Occasion**: Select or enter custom occasion
   - **Theme**: Choose a visual theme
   - **Message**: Your personalized greeting (recommended < 300 chars)
3. Click "Generate QR Code"
4. Download the QR code image

### Scan a Greeting

1. Go to the "Scan QR Code" tab
2. Upload a QR code image (PNG/JPG)
3. View the decoded greeting message

## Examples

The app includes several example greetings:

- Christmas greeting with snowflake theme
- New Year message with fireworks theme
- Wedding announcement with champagne theme

## Technical Details

### Greeting Format

Greetings are encoded as compact JSON with the following structure:

```json
{
  "v": "1.0",
  "type": "greeting",
  "from": "Alice",
  "to": "Bob",
  "occasion": "Christmas 2025",
  "message": "Your greeting message here...",
  "theme": "snowflake",
  "created": "2025-12-07T10:30:00Z"
}
```

### QR Code Specifications

- **Error Correction**: Level H (High) - 30% damage recovery
- **Auto Version Detection**: Automatically selects optimal QR version
- **Capacity**: Supports messages up to ~500 characters
- **Format**: PNG images with 4-pixel border

### Message Capacity Reference

| Message Length | Data Size | QR Version |
|---------------|-----------|------------|
| 100 chars     | ~150 bytes | V10-H     |
| 200 chars     | ~250 bytes | V15-H     |
| 300 chars     | ~350 bytes | V20-H     |
| 500 chars     | ~550 bytes | V30-H     |

## Project Structure

```
streamlit/
├── app.py                  # Main Streamlit application
├── greeting_formats.py     # Greeting JSON encoding/decoding
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── .streamlit/
    └── config.toml        # Streamlit configuration
```

## Use Cases

### Personal
- Holiday greeting cards
- Birthday wishes
- Thank you notes
- Time capsule messages for future dates

### Events
- Wedding save-the-date announcements
- Party invitations
- Celebration messages

### Creative
- Digital gift tags
- Memory keepsakes
- Photo album additions

## Powered By

- **[netshare](https://pypi.org/project/netshare/)** - PyPI package for network sharing and QR utilities
- **[Streamlit](https://streamlit.io)** - Interactive web framework
- **[qrcode](https://pypi.org/project/qrcode/)** - QR code generation library
- **[Pillow](https://python-pillow.org/)** - Python Imaging Library

## Tips

💡 **Best Practices**:
- Keep messages under 300 characters for optimal QR code size
- Test QR codes with multiple phone camera apps
- Choose themes that match your occasion
- Use high error correction for better scanning reliability

📱 **Scanning**:
- Most modern smartphones can scan QR codes with their camera app
- For older devices, download a QR scanner app
- Ensure good lighting when scanning

🎨 **Design**:
- Match themes to occasions (snowflake for Christmas, fireworks for New Year)
- Consider the recipient's preferences
- Add personal touches to messages

## License

This project uses the netshare package (GPL-3.0 license).

## Support

For issues or questions:
- Check the "About" tab in the application
- Review the examples for guidance
- Ensure all dependencies are properly installed

## Future Enhancements

Potential features for future versions:
- Animated QR codes with theme GIFs
- Custom color schemes
- Message templates
- Multi-language support
- QR code style customization
- Batch greeting generation

---

**Happy Greeting!** 🎄✨

https://www.techspot.com/guides/1676-qr-code-explained/

