---
description: Refactoring plan to extract QR generation code into a Swagger API
---

# QR Code Generation API Refactoring Plan

## Overview

This document outlines the refactoring of the Holiday Greeting QR Code Generator app (`app.py`) to separate concerns by extracting QR generation logic into a standalone **Swagger/OpenAPI REST API**. The Streamlit frontend will call this API instead of generating QR codes directly.

---

## Current Architecture

```
┌──────────────────────────────────────────────────────┐
│                    app.py (1066 lines)               │
│  ┌─────────────────┐  ┌────────────────────────────┐ │
│  │ Streamlit UI    │  │ QR Generation Logic        │ │
│  │ - Forms         │  │ - generate_qr_code()       │ │
│  │ - Tabs          │  │ - load_theme_icon()        │ │
│  │ - Display       │  │ - display_qr_with_protection│ │
│  │ - Download      │  │ - Theme icon embedding     │ │
│  └─────────────────┘  └────────────────────────────┘ │
│                                                      │
│  ┌─────────────────────────────────────────────────┐ │
│  │ greeting_formats.py                             │ │
│  │ - create_holiday_greeting()                     │ │
│  │ - encode_greeting_to_url()                      │ │
│  │ - decode_greeting_from_url()                    │ │
│  │ - parse_greeting()                              │ │
│  │ - get_greeting_stats()                          │ │
│  └─────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────┘
```

---

## Target Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        STREAMLIT APP (app.py)                        │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │ Frontend Only:                                                │   │
│  │ - UI components (forms, tabs, layout)                         │   │
│  │ - User input handling                                         │   │
│  │ - Display QR code images (received from API)                  │   │
│  │ - Download management                                         │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                              │                                       │
│                              │ HTTP Requests                         │
│                              ▼                                       │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │               api_client.py (New)                             │   │
│  │ - QRApiClient class                                           │   │
│  │ - Handles API communication                                   │   │
│  │ - Error handling & retry logic                                │   │
│  └──────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
                               │
                               │ HTTP/REST
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     QR GENERATION API (New Service)                  │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │ FastAPI + Swagger UI (/docs)                                  │   │
│  │                                                               │   │
│  │ Endpoints:                                                    │   │
│  │ POST /api/v1/qr/generate        - Generate QR code           │   │
│  │ GET  /api/v1/qr/themes          - List available themes      │   │
│  │ GET  /api/v1/qr/themes/{name}   - Get theme icon preview     │   │
│  │ POST /api/v1/greeting/encode    - Encode greeting to URL     │   │
│  │ POST /api/v1/greeting/decode    - Decode greeting from URL   │   │
│  │ GET  /api/v1/health             - Health check               │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │ Core Modules (Extracted from app.py):                         │   │
│  │ - qr_generator.py   (QR code generation logic)               │   │
│  │ - theme_manager.py  (Theme icons, THEME_ICONS mapping)       │   │
│  │ - greeting_formats.py (Moved/shared)                         │   │
│  │ - schemas.py        (Pydantic models for API)                │   │
│  └──────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Code to Extract from app.py

### 1. QR Generation Core (`qr_generator.py`)
Lines 439-502 in app.py:

```python
def generate_qr_code(data: str, theme: str = "general", error_correction=qrcode.constants.ERROR_CORRECT_H) -> Image.Image:
    """
    Generate QR code from data string
    - Creates QR code with specified error correction
    - Embeds theme icon in center (if applicable)
    - Returns PIL Image
    """
```

### 2. Theme Management (`theme_manager.py`)
Lines 115-125 (THEME_ICONS constant) and Lines 317-377 (load_theme_icon, get_theme_display_icon):

```python
THEME_ICONS = {
    "snowflake": "❄️",
    "fireworks": "🎆",
    "lights": "✨",
    "stars": "⭐",
    "confetti": "🎉",
    "champagne": "🥂",
    "hearts": "❤️",
    "general": None
}

def load_theme_icon(theme: str, size: int = 100) -> Image.Image:
    ...

def get_theme_display_icon(theme: str, size: int = 60) -> Image.Image:
    ...
```

### 3. Greeting Encoding (Already in `greeting_formats.py`)
- `create_holiday_greeting()`
- `encode_greeting_to_url()`
- `decode_greeting_from_url()`
- `parse_greeting()`
- `get_greeting_stats()`

---

## New Project Structure

```
streamlit/
├── app.py                    # Streamlit frontend (simplified)
├── api_client.py             # NEW: HTTP client for QR API
├── greeting_formats.py       # Keep for URL encoding/decoding
├── icons/                    # Theme icons (used by API)
│   ├── snowflake.png
│   ├── fireworks.png
│   └── ...
├── requirements.txt          # Add 'requests' dependency
│
└── qr_api/                   # NEW: FastAPI service directory
    ├── __init__.py
    ├── main.py               # FastAPI app entry point
    ├── routers/
    │   ├── __init__.py
    │   ├── qr.py             # QR generation endpoints
    │   ├── greeting.py       # Greeting encode/decode endpoints
    │   └── themes.py         # Theme listing endpoints
    ├── services/
    │   ├── __init__.py
    │   ├── qr_generator.py   # Extracted QR generation logic
    │   └── theme_manager.py  # Extracted theme logic
    ├── schemas/
    │   ├── __init__.py
    │   ├── qr.py             # Pydantic models for QR
    │   └── greeting.py       # Pydantic models for greeting
    ├── icons/                # Copy of theme icons
    ├── requirements.txt      # FastAPI, qrcode, Pillow, uvicorn
    └── config.py             # API configuration
```

---

## API Specification (OpenAPI/Swagger)

### POST /api/v1/qr/generate

Generate a QR code image with optional theme icon.

**Request Body:**
```json
{
  "data": "https://qr-greeting.streamlit.app/?tab=scan&f=Alice&t=Bob&th=snowflake&mc=...",
  "theme": "snowflake",
  "error_correction": "H",
  "output_format": "png",
  "size": 500
}
```

**Response:** Binary image/png (or base64 encoded in JSON wrapper)

**Response (JSON mode):**
```json
{
  "success": true,
  "image_base64": "iVBORw0KGgoAAAANSUhEUgAAA...",
  "mime_type": "image/png",
  "dimensions": { "width": 500, "height": 500 },
  "qr_version": 15,
  "data_size_bytes": 432
}
```

---

### GET /api/v1/qr/themes

List all available themes.

**Response:**
```json
{
  "themes": [
    { "key": "snowflake", "emoji": "❄️", "label": "Snowflake", "has_icon": true },
    { "key": "fireworks", "emoji": "🎆", "label": "Fireworks", "has_icon": true },
    { "key": "lights", "emoji": "✨", "label": "Lights", "has_icon": true },
    { "key": "stars", "emoji": "⭐", "label": "Stars", "has_icon": true },
    { "key": "confetti", "emoji": "🎉", "label": "Confetti", "has_icon": true },
    { "key": "champagne", "emoji": "🥂", "label": "Champagne", "has_icon": true },
    { "key": "hearts", "emoji": "❤️", "label": "Hearts", "has_icon": true },
    { "key": "general", "emoji": null, "label": "General (No Icon)", "has_icon": false }
  ]
}
```

---

### GET /api/v1/qr/themes/{theme_key}/icon

Get theme icon preview image.

**Path Parameters:**
- `theme_key`: Theme identifier (e.g., "snowflake")

**Query Parameters:**
- `size`: Icon size in pixels (default: 60)

**Response:** Binary image/png

---

### POST /api/v1/greeting/encode

Encode greeting data to a URL for QR code.

**Request Body:**
```json
{
  "from_name": "Alice",
  "to_name": "Bob",
  "message": "Merry Christmas! Wishing you joy...",
  "theme": "snowflake"
}
```

**Response:**
```json
{
  "url": "https://qr-greeting.streamlit.app/?tab=scan&f=Alice&t=Bob&th=snowflake&mc=...",
  "stats": {
    "byte_size": 245,
    "char_count": 245,
    "recommended_qr_version": 15,
    "fits_in_qr": true
  }
}
```

---

### POST /api/v1/greeting/decode

Decode greeting from URL parameters.

**Request Body:**
```json
{
  "url": "https://qr-greeting.streamlit.app/?tab=scan&f=Alice&t=Bob&th=snowflake&mc=..."
}
```

**Response:**
```json
{
  "success": true,
  "greeting": {
    "v": "1.0",
    "type": "greeting",
    "from": "Alice",
    "to": "Bob",
    "message": "Merry Christmas! Wishing you joy...",
    "theme": "snowflake",
    "created": "2024-12-14T15:03:30Z"
  }
}
```

---

### GET /api/v1/health

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2024-12-14T15:03:30Z"
}
```

---

## Implementation Steps

### Phase 1: Create API Service Structure (Backend First)

// turbo
1. Create directory structure for `qr_api/`

2. Create `qr_api/requirements.txt`:
   ```
   fastapi>=0.104.0
   uvicorn[standard]>=0.24.0
   qrcode>=7.4.2
   Pillow>=10.0.0
   pydantic>=2.0.0
   python-multipart>=0.0.6
   ```

3. Create `qr_api/config.py` with configuration settings

4. Create Pydantic schemas in `qr_api/schemas/`:
   - `qr.py`: QRGenerateRequest, QRGenerateResponse, ThemeInfo, ThemeListResponse
   - `greeting.py`: GreetingEncodeRequest, GreetingDecodeRequest, GreetingResponse

5. Extract and adapt services to `qr_api/services/`:
   - `qr_generator.py`: Move `generate_qr_code()` function
   - `theme_manager.py`: Move `THEME_ICONS`, `load_theme_icon()`, `get_theme_display_icon()`

6. Create API routers in `qr_api/routers/`:
   - `qr.py`: `/generate`, `/themes` endpoints
   - `greeting.py`: `/encode`, `/decode` endpoints
   - `themes.py`: Theme icon endpoints

7. Create main FastAPI app in `qr_api/main.py`:
   - Mount routers
   - Configure CORS
   - Add Swagger UI

8. Copy `icons/` directory to `qr_api/icons/`

---

### Phase 2: Create API Client for Streamlit

9. Create `api_client.py`:
   ```python
   import requests
   from PIL import Image
   import io
   import base64
   from typing import Optional, Dict

   class QRApiClient:
       def __init__(self, base_url: str = "http://localhost:8000"):
           self.base_url = base_url
           self.session = requests.Session()
       
       def generate_qr(
           self, 
           data: str, 
           theme: str = "general",
           error_correction: str = "H",
           output_format: str = "png"
       ) -> Image.Image:
           """Generate QR code via API and return PIL Image"""
           response = self.session.post(
               f"{self.base_url}/api/v1/qr/generate",
               json={
                   "data": data,
                   "theme": theme,
                   "error_correction": error_correction,
                   "output_format": output_format
               }
           )
           response.raise_for_status()
           
           # Decode base64 response to PIL Image
           result = response.json()
           img_bytes = base64.b64decode(result["image_base64"])
           return Image.open(io.BytesIO(img_bytes))
       
       def get_themes(self) -> list:
           """Get available themes"""
           response = self.session.get(f"{self.base_url}/api/v1/qr/themes")
           response.raise_for_status()
           return response.json()["themes"]
       
       def get_theme_icon(self, theme: str, size: int = 60) -> Optional[Image.Image]:
           """Get theme icon preview"""
           response = self.session.get(
               f"{self.base_url}/api/v1/qr/themes/{theme}/icon",
               params={"size": size}
           )
           if response.status_code == 200:
               return Image.open(io.BytesIO(response.content))
           return None
       
       def encode_greeting(self, from_name: str, to_name: str, message: str, theme: str) -> Dict:
           """Encode greeting to URL with stats"""
           response = self.session.post(
               f"{self.base_url}/api/v1/greeting/encode",
               json={
                   "from_name": from_name,
                   "to_name": to_name,
                   "message": message,
                   "theme": theme
               }
           )
           response.raise_for_status()
           return response.json()
       
       def health_check(self) -> bool:
           """Check if API is available"""
           try:
               response = self.session.get(f"{self.base_url}/api/v1/health")
               return response.status_code == 200
           except:
               return False
   ```

---

### Phase 3: Update app.py to Use API Client

10. Update `app.py` imports and initialization:
    - Import `QRApiClient`
    - Initialize client with configurable URL (env var or sidebar setting)
    - Add fallback to local generation if API unavailable

11. Modify `create_greeting_tab()`:
    - Replace direct `generate_qr_code()` call with `api_client.generate_qr()`
    - Use API response for statistics

12. Modify `render_theme_selector()`:
    - Optionally fetch themes from API
    - Keep local fallback for offline support

13. Modify `examples_tab()`:
    - Use API for QR generation

14. Update `requirements.txt`:
    - Add `requests>=2.31.0`

---

### Phase 4: Testing & Documentation

15. Create `qr_api/tests/` directory with tests:
    - `test_qr_generation.py`
    - `test_greeting_encoding.py`
    - `test_themes.py`

16. Add API documentation:
    - Update `README.md` with API usage
    - Swagger UI available at `/docs`

17. Create run scripts:
    - `run_api.bat` / `run_api.sh` for API server
    - Update `run.bat` / `run.sh` to optionally start API

---

## Configuration Options

### Environment Variables

```bash
# API Server
QR_API_HOST=0.0.0.0
QR_API_PORT=8000
QR_API_CORS_ORIGINS=["http://localhost:8501", "https://qr-greeting.streamlit.app"]

# Streamlit App
QR_API_URL=http://localhost:8000
QR_API_FALLBACK_LOCAL=true  # Use local generation if API unavailable
```

---

## Benefits of This Refactoring

1. **Separation of Concerns**: UI logic separated from QR generation business logic
2. **Scalability**: API can be deployed independently and scaled horizontally
3. **Reusability**: Other apps can use the QR generation API
4. **Testing**: Easier to unit test API endpoints independently
5. **Maintainability**: Smaller, focused modules are easier to maintain
6. **Swagger Documentation**: Auto-generated API docs for developers
7. **Fallback Support**: App still works if API is down (local generation)

---

## Migration Considerations

- **Backward Compatibility**: Keep local generation as fallback
- **Deployment**: API can run as sidecar or separate service
- **Icons**: Need to copy icons to API service directory
- **Streamlit Cloud**: May need external API hosting (Railway, Render, etc.)

---

## Estimated Effort

| Phase | Description | Estimated Time |
|-------|-------------|----------------|
| Phase 1 | Create API Service | 2-3 hours |
| Phase 2 | Create API Client | 30-45 min |
| Phase 3 | Update app.py | 1-2 hours |
| Phase 4 | Testing & Docs | 1-2 hours |
| **Total** | | **5-8 hours** |
