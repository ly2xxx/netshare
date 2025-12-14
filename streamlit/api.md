# QR Code Generation API Documentation

## Overview

This document provides step-by-step instructions for using the QR Code Generation API. The API is built with FastAPI and provides endpoints for QR code generation, greeting encoding/decoding, and theme management.

**Base URL**: `http://localhost:8000`
**API Version**: `v1`
**API Prefix**: `/api/v1`

---

## Table of Contents

1. [Starting the API](#starting-the-api)
2. [Accessing Swagger Documentation](#accessing-swagger-documentation)
3. [API Endpoints](#api-endpoints)
4. [Testing with cURL](#testing-with-curl)
5. [Testing with Python](#testing-with-python)
6. [Common Use Cases](#common-use-cases)
7. [Troubleshooting](#troubleshooting)

---

## Starting the API

### Method 1: Standalone Mode (Development)

**Step 1**: Navigate to the streamlit directory
```bash
cd /mnt/h/code/yl/netshare/streamlit
```

**Step 2**: Ensure dependencies are installed
```bash
pip install -r requirements.txt
```

**Step 3**: Start the API server
```bash
uvicorn qr_api.main:app --reload --port 8000
```

**Expected output**:
```
INFO:     Will watch for changes in these directories: ['/mnt/h/code/yl/netshare/streamlit']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using StatReload
[QR API] Starting on port 8000
[QR API] Documentation: http://127.0.0.1:8000/api/v1/docs
INFO:     Application startup complete.
```

**Step 4**: Verify the API is running
```bash
curl http://localhost:8000/api/v1/health
```

**Expected response**:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:45.123456",
  "service": "qr-api"
}
```

---

### Method 2: Embedded Mode (with Streamlit)

The API automatically starts when you run the Streamlit app.

**Step 1**: Start the Streamlit app
```bash
cd /mnt/h/code/yl/netshare/streamlit
streamlit run app.py
```

**Step 2**: Look for API startup messages in the console
```
[API Server] Starting on port 8000
[API Server] Documentation: http://127.0.0.1:8000/api/v1/docs
```

**Step 3**: The API is now running alongside Streamlit
- Streamlit UI: `http://localhost:8501`
- API endpoints: `http://localhost:8000/api/v1/*`
- API docs: `http://localhost:8000/api/v1/docs`

---

## Accessing Swagger Documentation

### Step 1: Start the API
Follow either Method 1 or Method 2 above to start the API server.

### Step 2: Open your web browser
Navigate to: **http://localhost:8000/api/v1/docs**

### Step 3: Explore the Interactive Documentation

You should see the **Swagger UI** interface with:

#### **Top Section**:
- **Title**: "QR Code Generation API"
- **Description**: "Embedded API for QR code and greeting operations"
- **Version**: "v1"

#### **Endpoint Sections** (expandable):

**1. health** (green tag)
- `GET /api/v1/health` - Health check endpoint

**2. qr** (blue tag)
- `POST /api/v1/qr/generate` - Generate QR code
- `GET /api/v1/qr/themes` - List available themes
- `GET /api/v1/qr/themes/{theme}/icon` - Get theme icon
- `POST /api/v1/qr/decode` - Decode QR from image

**3. greeting** (purple tag)
- `POST /api/v1/greeting/encode` - Encode greeting to URL
- `POST /api/v1/greeting/decode` - Decode greeting
- `POST /api/v1/greeting/validate` - Validate greeting size

### Step 4: Test an Endpoint in Swagger UI

**Example: Testing the Health Check Endpoint**

1. Click on `GET /api/v1/health` to expand it
2. Click the **"Try it out"** button (top right of the section)
3. Click the **"Execute"** button
4. Scroll down to see the response:
   - **Response Code**: `200`
   - **Response Body**:
     ```json
     {
       "status": "healthy",
       "timestamp": "2024-01-15T10:30:45.123456",
       "service": "qr-api"
     }
     ```

**Example: Testing QR Code Generation**

1. Click on `POST /api/v1/qr/generate` to expand it
2. Click **"Try it out"**
3. Edit the request body:
   ```json
   {
     "data": "Hello, World!",
     "theme": "snowflake",
     "error_correction": "H"
   }
   ```
4. Click **"Execute"**
5. View the response:
   - **Response Code**: `200`
   - **Response Body**: Contains `image_base64` and `stats`

### Step 5: View Response Schema

Each endpoint shows:
- **Request Body** schema (what you send)
- **Response** schema (what you get back)
- **Parameter** descriptions
- **Example values**

Click the **"Schema"** tab to see the data structure definitions.

---

## API Endpoints

### 1. Health Check

**Endpoint**: `GET /api/v1/health`

**Description**: Check if the API is running and healthy.

**Request**: No parameters required

**Response**:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:45.123456",
  "service": "qr-api"
}
```

**cURL Example**:
```bash
curl http://localhost:8000/api/v1/health
```

---

### 2. Generate QR Code

**Endpoint**: `POST /api/v1/qr/generate`

**Description**: Generate a QR code with optional theme icon.

**Request Body**:
```json
{
  "data": "https://example.com",
  "theme": "snowflake",
  "error_correction": "H"
}
```

**Parameters**:
- `data` (required): Data to encode in QR code
- `theme` (optional): Theme name (`snowflake`, `fireworks`, `lights`, `stars`, `confetti`, `champagne`, `hearts`, `general`)
- `error_correction` (optional): Error correction level (`L`, `M`, `Q`, `H`). Default: `H`

**Response**:
```json
{
  "image_base64": "iVBORw0KGgoAAAANSUhEUgAAA...",
  "stats": {
    "byte_size": 245,
    "char_count": 245,
    "recommended_qr_version": 15,
    "fits_in_qr": true,
    "theme": "snowflake",
    "error_correction": "H"
  }
}
```

**cURL Example**:
```bash
curl -X POST http://localhost:8000/api/v1/qr/generate \
  -H "Content-Type: application/json" \
  -d '{
    "data": "Hello, World!",
    "theme": "snowflake",
    "error_correction": "H"
  }'
```

---

### 3. List Available Themes

**Endpoint**: `GET /api/v1/qr/themes`

**Description**: Get list of all available themes with metadata.

**Request**: No parameters required

**Response**:
```json
{
  "themes": [
    {
      "name": "snowflake",
      "emoji": "❄️",
      "has_icon": true
    },
    {
      "name": "fireworks",
      "emoji": "🎆",
      "has_icon": true
    },
    {
      "name": "lights",
      "emoji": "✨",
      "has_icon": true
    },
    {
      "name": "stars",
      "emoji": "⭐",
      "has_icon": true
    },
    {
      "name": "confetti",
      "emoji": "🎉",
      "has_icon": true
    },
    {
      "name": "champagne",
      "emoji": "🥂",
      "has_icon": true
    },
    {
      "name": "hearts",
      "emoji": "❤️",
      "has_icon": true
    },
    {
      "name": "general",
      "emoji": null,
      "has_icon": false
    }
  ]
}
```

**cURL Example**:
```bash
curl http://localhost:8000/api/v1/qr/themes
```

---

### 4. Get Theme Icon

**Endpoint**: `GET /api/v1/qr/themes/{theme}/icon`

**Description**: Get a theme icon preview as base64-encoded PNG.

**Path Parameters**:
- `theme` (required): Theme name (e.g., `snowflake`, `hearts`)

**Query Parameters**:
- `size` (optional): Icon size in pixels. Default: `60`

**Response**:
```json
{
  "theme": "snowflake",
  "size": 60,
  "icon_base64": "iVBORw0KGgoAAAANSUhEUgAAA..."
}
```

**cURL Example**:
```bash
curl http://localhost:8000/api/v1/qr/themes/snowflake/icon?size=100
```

---

### 5. Encode Greeting to URL

**Endpoint**: `POST /api/v1/greeting/encode`

**Description**: Encode greeting data into a URL with compression.

**Request Body**:
```json
{
  "from_name": "Alice",
  "to_name": "Bob",
  "message": "Merry Christmas! Wishing you joy and happiness!",
  "theme": "snowflake",
  "base_url": "https://qr-greeting.streamlit.app/"
}
```

**Parameters**:
- `from_name` (required): Sender's name
- `to_name` (required): Recipient's name
- `message` (required): Greeting message
- `theme` (optional): Theme identifier. Default: `general`
- `base_url` (optional): Base URL for greeting app. Default: `https://qr-greeting.streamlit.app/`

**Response**:
```json
{
  "url": "https://qr-greeting.streamlit.app/?tab=scan&f=Alice&t=Bob&th=snowflake&m=Merry+Christmas%21+Wishing+you+joy+and+happiness%21",
  "stats": {
    "byte_size": 125,
    "char_count": 125,
    "recommended_qr_version": 10,
    "fits_in_qr": true
  }
}
```

**Note**: Long messages (>50 chars) are automatically compressed using zlib.

**cURL Example**:
```bash
curl -X POST http://localhost:8000/api/v1/greeting/encode \
  -H "Content-Type: application/json" \
  -d '{
    "from_name": "Alice",
    "to_name": "Bob",
    "message": "Merry Christmas!",
    "theme": "snowflake"
  }'
```

---

### 6. Decode Greeting from URL

**Endpoint**: `POST /api/v1/greeting/decode`

**Description**: Decode greeting data from URL query parameters.

**Request Body**:
```json
{
  "query_params": {
    "f": "Alice",
    "t": "Bob",
    "th": "snowflake",
    "m": "Merry Christmas!"
  }
}
```

**Parameters**:
- `query_params` (required): Dictionary of URL query parameters

**Response**:
```json
{
  "success": true,
  "greeting": {
    "v": "1.0",
    "type": "greeting",
    "from": "Alice",
    "to": "Bob",
    "message": "Merry Christmas!",
    "theme": "snowflake",
    "created": "2024-01-15T10:30:45.123456"
  }
}
```

**cURL Example**:
```bash
curl -X POST http://localhost:8000/api/v1/greeting/decode \
  -H "Content-Type: application/json" \
  -d '{
    "query_params": {
      "f": "Alice",
      "t": "Bob",
      "th": "snowflake",
      "m": "Merry Christmas!"
    }
  }'
```

---

### 7. Validate Greeting Size

**Endpoint**: `POST /api/v1/greeting/validate`

**Description**: Check if a greeting will fit in a QR code.

**Request Body**:
```json
{
  "message": "Your message here...",
  "from_name": "Alice",
  "to_name": "Bob",
  "theme": "snowflake"
}
```

**Parameters**:
- `message` (required): Message to validate
- `from_name` (optional): Sender's name
- `to_name` (optional): Recipient's name
- `theme` (optional): Theme identifier. Default: `general`

**Response**:
```json
{
  "valid": true,
  "stats": {
    "byte_size": 125,
    "char_count": 125,
    "recommended_qr_version": 10,
    "fits_in_qr": true
  }
}
```

**QR Code Capacity Reference** (with High error correction):
- V10-H: 224 bytes
- V15-H: 432 bytes
- V20-H: 666 bytes
- V25-H: 952 bytes
- V30-H: 1276 bytes
- **V40-H: 1852 bytes (maximum)**

**cURL Example**:
```bash
curl -X POST http://localhost:8000/api/v1/greeting/validate \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Merry Christmas and Happy New Year! Wishing you joy, peace, and happiness!",
    "from_name": "Alice",
    "to_name": "Bob",
    "theme": "snowflake"
  }'
```

---

### 8. Decode QR Code from Image

**Endpoint**: `POST /api/v1/qr/decode`

**Description**: Decode QR code data from an uploaded image.

**Request Body**:
```json
{
  "image_base64": "iVBORw0KGgoAAAANSUhEUgAAA..."
}
```

**Parameters**:
- `image_base64` (required): Base64-encoded image (PNG, JPG, etc.)

**Response**:
```json
{
  "success": true,
  "data": "https://example.com"
}
```

**cURL Example**:
```bash
# First, convert image to base64
base64 -w 0 qr_code.png > qr_code_base64.txt

# Then send to API
curl -X POST http://localhost:8000/api/v1/qr/decode \
  -H "Content-Type: application/json" \
  -d "{\"image_base64\": \"$(cat qr_code_base64.txt)\"}"
```

---

## Testing with cURL

### Quick Test Script

Save this as `test_api.sh`:

```bash
#!/bin/bash

BASE_URL="http://localhost:8000/api/v1"

echo "=== Testing QR Code Generation API ==="
echo ""

# Test 1: Health Check
echo "1. Health Check"
curl -s "$BASE_URL/health" | jq .
echo ""

# Test 2: List Themes
echo "2. List Themes"
curl -s "$BASE_URL/qr/themes" | jq .
echo ""

# Test 3: Generate QR Code
echo "3. Generate QR Code"
curl -s -X POST "$BASE_URL/qr/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "data": "Hello, World!",
    "theme": "snowflake",
    "error_correction": "H"
  }' | jq '.stats'
echo ""

# Test 4: Encode Greeting
echo "4. Encode Greeting"
curl -s -X POST "$BASE_URL/greeting/encode" \
  -H "Content-Type: application/json" \
  -d '{
    "from_name": "Alice",
    "to_name": "Bob",
    "message": "Merry Christmas!",
    "theme": "snowflake"
  }' | jq .
echo ""

# Test 5: Validate Greeting
echo "5. Validate Greeting"
curl -s -X POST "$BASE_URL/greeting/validate" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Happy Holidays!",
    "from_name": "Alice",
    "to_name": "Bob",
    "theme": "snowflake"
  }' | jq .
echo ""

echo "=== All Tests Complete ==="
```

**Run the script**:
```bash
chmod +x test_api.sh
./test_api.sh
```

---

## Testing with Python

### Installation

```bash
pip install httpx pillow
```

### Python Test Script

Save this as `test_api.py`:

```python
#!/usr/bin/env python3
"""Test script for QR Code Generation API"""

import httpx
import base64
from PIL import Image
import io

BASE_URL = "http://localhost:8000/api/v1"


def test_health_check():
    """Test health check endpoint"""
    print("1. Testing Health Check...")
    response = httpx.get(f"{BASE_URL}/health")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    print()


def test_list_themes():
    """Test list themes endpoint"""
    print("2. Testing List Themes...")
    response = httpx.get(f"{BASE_URL}/qr/themes")
    data = response.json()
    print(f"   Status: {response.status_code}")
    print(f"   Found {len(data['themes'])} themes:")
    for theme in data['themes']:
        print(f"     - {theme['name']} {theme['emoji'] or ''}")
    print()


def test_generate_qr():
    """Test QR code generation"""
    print("3. Testing QR Code Generation...")
    response = httpx.post(
        f"{BASE_URL}/qr/generate",
        json={
            "data": "Hello, World!",
            "theme": "snowflake",
            "error_correction": "H"
        }
    )
    data = response.json()
    print(f"   Status: {response.status_code}")
    print(f"   Stats: {data['stats']}")

    # Decode and display QR code
    img_base64 = data['image_base64']
    img_bytes = base64.b64decode(img_base64)
    img = Image.open(io.BytesIO(img_bytes))

    # Save QR code
    img.save("test_qr_code.png")
    print(f"   QR code saved to: test_qr_code.png")
    print(f"   Size: {img.size}")
    print()


def test_encode_greeting():
    """Test greeting encoding"""
    print("4. Testing Greeting Encoding...")
    response = httpx.post(
        f"{BASE_URL}/greeting/encode",
        json={
            "from_name": "Alice",
            "to_name": "Bob",
            "message": "Merry Christmas! Wishing you joy and happiness!",
            "theme": "snowflake"
        }
    )
    data = response.json()
    print(f"   Status: {response.status_code}")
    print(f"   URL: {data['url'][:80]}...")
    print(f"   Stats: {data['stats']}")
    print()


def test_validate_greeting():
    """Test greeting validation"""
    print("5. Testing Greeting Validation...")

    # Test short message
    response = httpx.post(
        f"{BASE_URL}/greeting/validate",
        json={
            "message": "Happy Holidays!",
            "from_name": "Alice",
            "to_name": "Bob",
            "theme": "snowflake"
        }
    )
    data = response.json()
    print(f"   Short message:")
    print(f"     Valid: {data['valid']}")
    print(f"     Size: {data['stats']['byte_size']} bytes")

    # Test very long message
    long_message = "Merry Christmas! " * 100
    response = httpx.post(
        f"{BASE_URL}/greeting/validate",
        json={
            "message": long_message,
            "from_name": "Alice",
            "to_name": "Bob",
            "theme": "snowflake"
        }
    )
    data = response.json()
    print(f"   Long message:")
    print(f"     Valid: {data['valid']}")
    print(f"     Size: {data['stats']['byte_size']} bytes")
    print()


def test_decode_greeting():
    """Test greeting decoding"""
    print("6. Testing Greeting Decoding...")
    response = httpx.post(
        f"{BASE_URL}/greeting/decode",
        json={
            "query_params": {
                "f": "Alice",
                "t": "Bob",
                "th": "snowflake",
                "m": "Merry Christmas!"
            }
        }
    )
    data = response.json()
    print(f"   Status: {response.status_code}")
    print(f"   Success: {data['success']}")
    if data['success']:
        greeting = data['greeting']
        print(f"   From: {greeting['from']}")
        print(f"   To: {greeting['to']}")
        print(f"   Message: {greeting['message']}")
        print(f"   Theme: {greeting['theme']}")
    print()


if __name__ == "__main__":
    print("=== QR Code Generation API Test Suite ===\n")

    try:
        test_health_check()
        test_list_themes()
        test_generate_qr()
        test_encode_greeting()
        test_validate_greeting()
        test_decode_greeting()

        print("=== All Tests Complete ===")
    except Exception as e:
        print(f"Error: {e}")
```

**Run the script**:
```bash
python3 test_api.py
```

---

## Common Use Cases

### Use Case 1: Generate a Simple QR Code

**Goal**: Create a QR code for a URL.

**Steps**:
1. Open Swagger UI: `http://localhost:8000/api/v1/docs`
2. Expand `POST /api/v1/qr/generate`
3. Click "Try it out"
4. Enter request body:
   ```json
   {
     "data": "https://github.com",
     "theme": "general",
     "error_correction": "H"
   }
   ```
5. Click "Execute"
6. Copy the `image_base64` value
7. Decode base64 to get the PNG image

---

### Use Case 2: Create a Holiday Greeting QR Code

**Goal**: Generate a complete holiday greeting with QR code.

**Steps**:
1. **Encode the greeting**:
   ```bash
   curl -X POST http://localhost:8000/api/v1/greeting/encode \
     -H "Content-Type: application/json" \
     -d '{
       "from_name": "Alice",
       "to_name": "Bob",
       "message": "Merry Christmas and Happy New Year! Wishing you all the best!",
       "theme": "snowflake"
     }'
   ```

2. **Get the URL from the response**:
   ```json
   {
     "url": "https://qr-greeting.streamlit.app/?tab=scan&f=Alice&t=Bob&th=snowflake&mc=...",
     "stats": {...}
   }
   ```

3. **Generate QR code with the URL**:
   ```bash
   curl -X POST http://localhost:8000/api/v1/qr/generate \
     -H "Content-Type: application/json" \
     -d '{
       "data": "https://qr-greeting.streamlit.app/?tab=scan&f=Alice&t=Bob&th=snowflake&mc=...",
       "theme": "snowflake",
       "error_correction": "H"
     }'
   ```

4. **Save the QR code image**

---

### Use Case 3: Validate Message Size Before Creating QR

**Goal**: Check if a message fits in a QR code before generating.

**Steps**:
1. **Validate the message**:
   ```bash
   curl -X POST http://localhost:8000/api/v1/greeting/validate \
     -H "Content-Type: application/json" \
     -d '{
       "message": "Your very long message here...",
       "from_name": "Alice",
       "to_name": "Bob",
       "theme": "snowflake"
     }'
   ```

2. **Check the response**:
   ```json
   {
     "valid": true,  // ← Check this
     "stats": {
       "byte_size": 450,
       "recommended_qr_version": 15,
       "fits_in_qr": true  // ← Must be true
     }
   }
   ```

3. **If valid, proceed with encoding and QR generation**

---

### Use Case 4: Batch Generate QR Codes

**Python Script**:
```python
import httpx
import base64
from PIL import Image
import io

BASE_URL = "http://localhost:8000/api/v1"

# List of data to generate QR codes for
data_list = [
    ("https://example.com/page1", "snowflake"),
    ("https://example.com/page2", "hearts"),
    ("https://example.com/page3", "stars"),
]

for i, (data, theme) in enumerate(data_list, 1):
    # Generate QR code
    response = httpx.post(
        f"{BASE_URL}/qr/generate",
        json={
            "data": data,
            "theme": theme,
            "error_correction": "H"
        }
    )

    # Save image
    result = response.json()
    img_bytes = base64.b64decode(result['image_base64'])
    img = Image.open(io.BytesIO(img_bytes))
    img.save(f"qr_code_{i}.png")

    print(f"Generated: qr_code_{i}.png ({theme})")
```

---

## Troubleshooting

### Problem 1: Cannot Access Swagger UI

**Symptom**: Browser shows "This site can't be reached" at `http://localhost:8000/api/v1/docs`

**Solutions**:
1. Check if the API is running:
   ```bash
   curl http://localhost:8000/api/v1/health
   ```

2. Check if port 8000 is in use:
   ```bash
   lsof -i :8000
   # or
   netstat -ano | grep :8000
   ```

3. Try the alternate documentation:
   - ReDoc: `http://localhost:8000/api/v1/redoc`
   - OpenAPI JSON: `http://localhost:8000/api/v1/openapi.json`

4. Restart the API server:
   ```bash
   # Stop existing server (Ctrl+C)
   # Then restart
   uvicorn qr_api.main:app --reload --port 8000
   ```

---

### Problem 2: Import Errors When Starting API

**Symptom**: `ModuleNotFoundError: No module named 'fastapi'`

**Solution**: Install dependencies
```bash
cd /mnt/h/code/yl/netshare/streamlit
pip install -r requirements.txt
```

---

### Problem 3: API Returns 500 Internal Server Error

**Symptom**: Swagger UI shows red error responses

**Solutions**:
1. Check the server console for error messages
2. Verify request body matches the schema
3. Check if icon files exist in `icons/` directory
4. Test with a simpler request:
   ```json
   {
     "data": "test",
     "theme": "general",
     "error_correction": "H"
   }
   ```

---

### Problem 4: QR Code Won't Decode

**Symptom**: `/api/v1/qr/decode` returns `success: false`

**Solutions**:
1. Ensure `opencv-python-headless` is installed:
   ```bash
   pip install opencv-python-headless
   ```

2. Verify image is valid base64:
   ```bash
   echo "iVBORw0KGgo..." | base64 -d > test.png
   file test.png  # Should show "PNG image data"
   ```

3. Try with a known-good QR code image

---

### Problem 5: Embedded Mode Not Starting API

**Symptom**: Streamlit app runs but no API startup messages appear

**Solutions**:
1. Check session state:
   - Look for `[API Server] Starting on port 8000` in console
   - If missing, check for errors in console

2. Port 8000 might be in use:
   - Stop other services using port 8000
   - Or modify `qr_api/config.py` to use a different port

3. Restart Streamlit with clean cache:
   ```bash
   streamlit run app.py --server.headless true
   ```

---

## Advanced: CORS Configuration

If you need to access the API from a different domain, modify `qr_api/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://yourdomain.com"],  # Specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## API Response Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request succeeded |
| 404 | Not Found | Resource not found (e.g., invalid theme) |
| 422 | Unprocessable Entity | Validation error (check request body) |
| 500 | Internal Server Error | Server error (check logs) |

---

## Support

For issues or questions:
1. Check the console logs for error messages
2. Verify all dependencies are installed
3. Review this documentation
4. Check the GitHub issues page

---

**Last Updated**: 2024-01-15
**API Version**: v1
**Documentation Version**: 1.0
