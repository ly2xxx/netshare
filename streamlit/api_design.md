# QR Code Generation API - Architecture & Design

## Overview

This document explains how the QR Code Generation API is architected, how Swagger/FastAPI/uvicorn work together, and the design decisions behind the implementation.

---

## Table of Contents

1. [High-Level Architecture](#high-level-architecture)
2. [Technology Stack](#technology-stack)
3. [How FastAPI Works](#how-fastapi-works)
4. [How Uvicorn Serves the Application](#how-uvicorn-serves-the-application)
5. [How Swagger Documentation is Generated](#how-swagger-documentation-is-generated)
6. [Request Flow](#request-flow)
7. [Layer Architecture](#layer-architecture)
8. [Design Patterns](#design-patterns)
9. [Embedded Deployment Model](#embedded-deployment-model)
10. [Code Organization](#code-organization)

---

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    CLIENT APPLICATIONS                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Streamlit UI │  │ Web Browser  │  │ curl/httpx   │      │
│  │ (Port 8501)  │  │ (Swagger UI) │  │ (CLI/Script) │      │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘      │
└─────────┼──────────────────┼──────────────────┼─────────────┘
          │                  │                  │
          └──────────────────┼──────────────────┘
                             │ HTTP/JSON
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                  ASGI WEB SERVER (Uvicorn)                   │
│                    http://localhost:8000                     │
│  ┌────────────────────────────────────────────────────┐     │
│  │                                                     │     │
│  │  Async Event Loop (asyncio)                        │     │
│  │  - Handles concurrent requests                     │     │
│  │  - Non-blocking I/O                                │     │
│  │  - ASGI protocol implementation                    │     │
│  │                                                     │     │
│  └────────────────────┬───────────────────────────────┘     │
└───────────────────────┼─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                    FASTAPI APPLICATION                       │
│  ┌────────────────────────────────────────────────────┐     │
│  │  Middleware Stack:                                 │     │
│  │  1. CORS Middleware                                │     │
│  │  2. Exception Handlers                             │     │
│  │  3. Request Validation (Pydantic)                  │     │
│  └────────────────────┬───────────────────────────────┘     │
│                       │                                      │
│  ┌────────────────────▼───────────────────────────────┐     │
│  │  Router Layer (URL → Function Mapping)             │     │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────────┐     │     │
│  │  │ health.py│  │  qr.py   │  │ greeting.py  │     │     │
│  │  │ /health  │  │  /qr/*   │  │ /greeting/*  │     │     │
│  │  └────┬─────┘  └────┬─────┘  └──────┬───────┘     │     │
│  └───────┼─────────────┼────────────────┼─────────────┘     │
└──────────┼─────────────┼────────────────┼───────────────────┘
           │             │                │
           ▼             ▼                ▼
┌─────────────────────────────────────────────────────────────┐
│                     SERVICE LAYER                            │
│  ┌─────────────────┐  ┌─────────────────┐  ┌────────────┐  │
│  │ theme_manager   │  │  qr_generator   │  │  greeting  │  │
│  │                 │  │                 │  │  _service  │  │
│  │ - Load icons    │  │ - Create QR     │  │ - Encode   │  │
│  │ - List themes   │  │ - Embed icons   │  │ - Decode   │  │
│  │ - Get base64    │  │ - Decode QR     │  │ - Validate │  │
│  └─────────────────┘  └─────────────────┘  └────────────┘  │
└─────────────────────────────────────────────────────────────┘
           │                      │                  │
           ▼                      ▼                  ▼
┌─────────────────────────────────────────────────────────────┐
│                   EXTERNAL DEPENDENCIES                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │  Pillow  │  │  qrcode  │  │   zlib   │  │   cv2    │   │
│  │  (Image  │  │  (QR gen)│  │(Compress)│  │(QR decode│   │
│  │  process)│  │          │  │          │  │         )│   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└─────────────────────────────────────────────────────────────┘
           │                      │                  │
           ▼                      ▼                  ▼
┌─────────────────────────────────────────────────────────────┐
│                      FILE SYSTEM                             │
│                   /icons/*.png files                         │
└─────────────────────────────────────────────────────────────┘
```

---

## Technology Stack

### Core Technologies

| Technology | Version | Purpose |
|------------|---------|---------|
| **FastAPI** | >=0.104.0 | Web framework - handles routing, validation, docs |
| **Uvicorn** | >=0.24.0 | ASGI server - serves the FastAPI app |
| **Pydantic** | >=2.0.0 | Data validation and serialization |
| **Python** | 3.8+ | Programming language |

### Supporting Libraries

| Library | Purpose |
|---------|---------|
| **qrcode** | QR code generation |
| **Pillow (PIL)** | Image processing and manipulation |
| **httpx** | HTTP client for API calls |
| **opencv-python** | QR code decoding from images |
| **zlib** | Message compression |

---

## How FastAPI Works

### What is FastAPI?

FastAPI is a modern Python web framework built on top of **Starlette** (web) and **Pydantic** (data validation).

### Key Features Used in This API

#### 1. **Automatic Request Validation**

```python
# In qr_api/routers/qr.py
@router.post("/generate", response_model=QRGenerateResponse)
async def generate_qr(request: QRGenerateRequest):
    # FastAPI automatically:
    # 1. Parses the JSON request body
    # 2. Validates it against QRGenerateRequest schema
    # 3. Returns 422 error if validation fails
    # 4. Passes validated data to the function
```

**What happens behind the scenes:**
```
Incoming Request
    ↓
JSON Body: {"data": "test", "theme": "snowflake", "error_correction": "H"}
    ↓
Pydantic Validation (QRGenerateRequest)
    ✓ data: str (required) ✓
    ✓ theme: str (default="general") ✓
    ✓ error_correction: Literal["L","M","Q","H"] ✓
    ↓
Validated Python Object
    ↓
Function receives: request.data, request.theme, request.error_correction
```

#### 2. **Automatic Response Serialization**

```python
# Function returns this
return QRGenerateResponse(
    image_base64=img_base64,
    stats=stats
)

# FastAPI automatically:
# 1. Validates the response matches QRGenerateResponse schema
# 2. Converts to JSON
# 3. Sets Content-Type: application/json header
# 4. Returns HTTP 200 with JSON body
```

#### 3. **Dependency Injection**

FastAPI can inject dependencies into route functions:

```python
# Example (not used in this API, but available)
from fastapi import Depends

def get_db():
    db = Database()
    try:
        yield db
    finally:
        db.close()

@router.get("/items")
async def get_items(db = Depends(get_db)):
    # db is automatically provided by FastAPI
    return db.query_items()
```

#### 4. **Automatic OpenAPI Schema Generation**

FastAPI introspects your code to generate OpenAPI specs:

```python
@router.post("/generate", response_model=QRGenerateResponse)
async def generate_qr(request: QRGenerateRequest):
    """
    Generate a QR code with optional theme icon  # ← Becomes description in docs

    Args:
        request: QR generation parameters  # ← Parameter documentation
    """
```

This becomes:
```json
{
  "paths": {
    "/api/v1/qr/generate": {
      "post": {
        "summary": "Generate QR code",
        "description": "Generate a QR code with optional theme icon",
        "requestBody": {...},
        "responses": {...}
      }
    }
  }
}
```

#### 5. **Async Support**

```python
async def generate_qr(request: QRGenerateRequest):
    # Functions can be async for non-blocking I/O
    # But our current implementation uses sync (no await)
    # This is fine - FastAPI handles both
```

**Why async matters:**
- Allows handling multiple requests concurrently
- Non-blocking I/O for database/API calls
- Better performance under high load

---

## How Uvicorn Serves the Application

### What is Uvicorn?

Uvicorn is an **ASGI (Asynchronous Server Gateway Interface)** web server that runs Python web applications.

### ASGI vs WSGI

| Feature | WSGI (old) | ASGI (modern) |
|---------|------------|---------------|
| Async support | ❌ No | ✅ Yes |
| WebSockets | ❌ No | ✅ Yes |
| HTTP/2 | ❌ No | ✅ Yes |
| Examples | Gunicorn, uWSGI | Uvicorn, Daphne |

### How Uvicorn Works

```
┌─────────────────────────────────────────┐
│         Uvicorn Process                 │
│                                         │
│  1. Binds to localhost:8000             │
│  2. Listens for HTTP requests           │
│  3. Parses HTTP protocol                │
│  4. Creates ASGI events                 │
│  5. Passes to FastAPI app               │
│  6. Gets response from FastAPI          │
│  7. Sends HTTP response to client       │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │   asyncio Event Loop            │   │
│  │                                 │   │
│  │   ┌─────────────────────────┐   │   │
│  │   │ Request 1 (in progress) │   │   │
│  │   ├─────────────────────────┤   │   │
│  │   │ Request 2 (waiting I/O) │   │   │
│  │   ├─────────────────────────┤   │   │
│  │   │ Request 3 (in progress) │   │   │
│  │   └─────────────────────────┘   │   │
│  │                                 │   │
│  │   All requests handled          │   │
│  │   concurrently without threads  │   │
│  └─────────────────────────────────┘   │
└─────────────────────────────────────────┘
```

### Starting Uvicorn

**Command line:**
```bash
uvicorn qr_api.main:app --reload --port 8000
#        ↑         ↑      ↑         ↑
#      module   variable  auto-    port
#      path               reload
```

**Programmatically (in app.py):**
```python
import uvicorn

config = uvicorn.Config(
    app=app,              # The FastAPI app instance
    host="127.0.0.1",     # Listen on localhost only
    port=8000,            # Port number
    log_level="warning",  # Reduce console noise
    access_log=False      # Don't log every request
)

server = uvicorn.Server(config)

# Run in background thread
import asyncio
asyncio.run(server.serve())
```

### What Happens During a Request

```
1. Client sends HTTP request
   POST /api/v1/qr/generate
   Content-Type: application/json
   {"data": "test", "theme": "snowflake"}

2. Uvicorn receives TCP connection
   - Parses HTTP headers
   - Reads request body

3. Uvicorn creates ASGI event
   {
     "type": "http.request",
     "body": b'{"data": "test", "theme": "snowflake"}',
     "headers": [("content-type", "application/json")],
     ...
   }

4. Uvicorn passes event to FastAPI

5. FastAPI processes request
   - Matches route: /api/v1/qr/generate
   - Validates request body
   - Calls generate_qr() function

6. Function returns response object

7. FastAPI serializes to JSON

8. Uvicorn sends HTTP response
   HTTP/1.1 200 OK
   Content-Type: application/json
   {"image_base64": "...", "stats": {...}}
```

---

## How Swagger Documentation is Generated

### OpenAPI Specification

FastAPI automatically generates an **OpenAPI 3.0** specification from your code.

### What Gets Extracted

```python
# From: qr_api/routers/qr.py

@router.post(
    "/generate",                           # ← Path
    response_model=QRGenerateResponse      # ← Response schema
)
async def generate_qr(                     # ← Function name → operationId
    request: QRGenerateRequest             # ← Request schema
):
    """
    Generate a QR code with optional theme icon  # ← Description

    Args:
        request: QR generation parameters         # ← Parameter docs

    Returns:
        Base64-encoded PNG image with stats       # ← Return docs
    """
```

**Becomes this OpenAPI JSON:**
```json
{
  "paths": {
    "/api/v1/qr/generate": {
      "post": {
        "operationId": "generate_qr_api_v1_qr_generate_post",
        "summary": "Generate Qr",
        "description": "Generate a QR code with optional theme icon\n\nArgs:\n    request: QR generation parameters\n\nReturns:\n    Base64-encoded PNG image with stats",
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "$ref": "#/components/schemas/QRGenerateRequest"
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/QRGenerateResponse"
                }
              }
            }
          }
        }
      }
    }
  },
  "components": {
    "schemas": {
      "QRGenerateRequest": {
        "type": "object",
        "properties": {
          "data": {"type": "string"},
          "theme": {"type": "string", "default": "general"},
          "error_correction": {"type": "string", "enum": ["L","M","Q","H"]}
        },
        "required": ["data"]
      }
    }
  }
}
```

### How Swagger UI Works

```
1. User opens http://localhost:8000/api/v1/docs

2. FastAPI serves swagger-ui HTML/JS/CSS

3. Browser loads Swagger UI (JavaScript app)

4. Swagger UI fetches OpenAPI spec
   GET http://localhost:8000/api/v1/openapi.json

5. FastAPI generates OpenAPI JSON dynamically
   - Introspects all routes
   - Extracts Pydantic schemas
   - Builds complete spec

6. Swagger UI renders the spec
   - Shows all endpoints
   - Displays schemas
   - Provides "Try it out" buttons

7. User clicks "Try it out"
   - Swagger UI makes real HTTP request to API
   - Displays the response
```

### Customizing Documentation

**In main.py:**
```python
app = FastAPI(
    title="QR Code Generation API",           # ← Shows in header
    description="Embedded API for QR code operations",  # ← Shows in intro
    version="v1",                             # ← Version number
    docs_url="/api/v1/docs",                  # ← Swagger UI path
    redoc_url="/api/v1/redoc",                # ← ReDoc path (alternative UI)
    openapi_url="/api/v1/openapi.json"        # ← OpenAPI spec path
)
```

### Pydantic Schema Contribution

```python
# From: qr_api/schemas/qr.py

class QRGenerateRequest(BaseModel):
    """Request to generate a QR code"""  # ← Schema description

    data: str = Field(
        ...,                               # ← Required field
        description="Data to encode in QR code"  # ← Field description
    )

    theme: str = Field(
        default="general",                 # ← Default value
        description="Theme icon to embed"  # ← Field description
    )

    error_correction: Literal["L", "M", "Q", "H"] = Field(
        default="H",
        description="Error correction level"  # ← Shows enum in docs
    )
```

**In Swagger UI, this appears as:**
```
QRGenerateRequest {
  data*        string    Data to encode in QR code
  theme        string    Theme icon to embed            default: general
  error_correction  enum  Error correction level        default: H
                         Available values: L, M, Q, H
}
```

---

## Request Flow

### Example: Generating a QR Code

**Step-by-step flow through the system:**

```
┌─────────────────────────────────────────────────────────┐
│ STEP 1: Client Request                                  │
└─────────────────────────────────────────────────────────┘

POST http://localhost:8000/api/v1/qr/generate
Content-Type: application/json

{
  "data": "Hello, World!",
  "theme": "snowflake",
  "error_correction": "H"
}

                    ↓

┌─────────────────────────────────────────────────────────┐
│ STEP 2: Uvicorn (ASGI Server)                           │
└─────────────────────────────────────────────────────────┘

1. Receives TCP connection on port 8000
2. Parses HTTP request
3. Extracts:
   - Method: POST
   - Path: /api/v1/qr/generate
   - Headers: Content-Type, Content-Length, etc.
   - Body: {"data": "Hello, World!", ...}
4. Creates ASGI scope and events
5. Passes to FastAPI application

                    ↓

┌─────────────────────────────────────────────────────────┐
│ STEP 3: FastAPI Middleware Stack                        │
└─────────────────────────────────────────────────────────┘

CORS Middleware:
  ✓ Check origin (allows all in dev mode)
  ✓ Add CORS headers

Exception Handler:
  - Wraps request in try/catch
  - Converts exceptions to HTTP errors

                    ↓

┌─────────────────────────────────────────────────────────┐
│ STEP 4: FastAPI Router Matching                         │
└─────────────────────────────────────────────────────────┘

FastAPI searches registered routes:
  ✗ GET /api/v1/health
  ✗ GET /api/v1/qr/themes
  ✓ POST /api/v1/qr/generate  ← MATCH!

Loads router: qr_api.routers.qr.generate_qr()

                    ↓

┌─────────────────────────────────────────────────────────┐
│ STEP 5: Request Validation (Pydantic)                   │
└─────────────────────────────────────────────────────────┘

Validates against QRGenerateRequest schema:
  ✓ data: "Hello, World!" (string, required) ✓
  ✓ theme: "snowflake" (string, valid theme) ✓
  ✓ error_correction: "H" (Literal["L","M","Q","H"]) ✓

Creates validated object:
  request = QRGenerateRequest(
    data="Hello, World!",
    theme="snowflake",
    error_correction="H"
  )

                    ↓

┌─────────────────────────────────────────────────────────┐
│ STEP 6: Router Function (qr.py)                         │
└─────────────────────────────────────────────────────────┘

File: qr_api/routers/qr.py
Function: generate_qr(request)

try:
    # Call service layer
    qr_img = generate_qr_code(
        data=request.data,
        theme=request.theme,
        error_correction=request.error_correction
    )

                    ↓

┌─────────────────────────────────────────────────────────┐
│ STEP 7: Service Layer (qr_generator.py)                 │
└─────────────────────────────────────────────────────────┘

File: qr_api/services/qr_generator.py
Function: generate_qr_code()

1. Create QRCode object
   qr = qrcode.QRCode(
     version=None,
     error_correction=ERROR_CORRECT_H,
     box_size=10,
     border=4
   )

2. Add data and generate
   qr.add_data("Hello, World!")
   qr.make(fit=True)
   img = qr.make_image(fill_color="black", back_color="white")

3. Load theme icon (if applicable)
   icon = load_theme_icon("snowflake", icon_size)

                    ↓

┌─────────────────────────────────────────────────────────┐
│ STEP 8: Theme Manager (theme_manager.py)                │
└─────────────────────────────────────────────────────────┘

File: qr_api/services/theme_manager.py
Function: load_theme_icon()

1. Build icon path
   icon_path = ICONS_DIR / "snowflake.png"

2. Load and resize image
   icon = Image.open(icon_path)
   icon = icon.resize((size, size), Image.Resampling.LANCZOS)

3. Return PIL Image object

                    ↓ (back to qr_generator.py)

┌─────────────────────────────────────────────────────────┐
│ STEP 9: Embed Icon in QR Code                           │
└─────────────────────────────────────────────────────────┘

1. Create white circular background
   background = Image.new('RGBA', (icon_size, icon_size))
   draw.ellipse([0, 0, icon_size, icon_size], fill=(255, 255, 255))

2. Paste background and icon on QR code
   pil_img.paste(background, icon_pos, background)
   pil_img.paste(icon, icon_pos, icon)

3. Convert to base64
   img_base64 = qr_image_to_base64(pil_img)

                    ↓ (back to router)

┌─────────────────────────────────────────────────────────┐
│ STEP 10: Get Statistics (greeting_service.py)           │
└─────────────────────────────────────────────────────────┘

File: qr_api/services/greeting_service.py
Function: get_greeting_stats()

Calculate size and QR version:
  stats = {
    "byte_size": 13,
    "char_count": 13,
    "recommended_qr_version": 10,
    "fits_in_qr": true
  }

                    ↓ (back to router)

┌─────────────────────────────────────────────────────────┐
│ STEP 11: Create Response Object (Router)                │
└─────────────────────────────────────────────────────────┘

return QRGenerateResponse(
    image_base64=img_base64,
    stats={
      "byte_size": 13,
      "char_count": 13,
      "recommended_qr_version": 10,
      "fits_in_qr": true,
      "theme": "snowflake",
      "error_correction": "H"
    }
)

                    ↓

┌─────────────────────────────────────────────────────────┐
│ STEP 12: Response Validation (Pydantic)                 │
└─────────────────────────────────────────────────────────┘

Validates against QRGenerateResponse schema:
  ✓ image_base64: str (required) ✓
  ✓ stats: dict (required) ✓

Serializes to JSON:
  {
    "image_base64": "iVBORw0KGgoAAAANSUhEUgAAA...",
    "stats": {...}
  }

except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))

                    ↓

┌─────────────────────────────────────────────────────────┐
│ STEP 13: FastAPI Response Handling                      │
└─────────────────────────────────────────────────────────┘

1. Serialize response to JSON
2. Set headers:
   Content-Type: application/json
   Content-Length: 1234
3. Set status code: 200 OK
4. Pass to Uvicorn

                    ↓

┌─────────────────────────────────────────────────────────┐
│ STEP 14: Uvicorn Sends HTTP Response                    │
└─────────────────────────────────────────────────────────┘

HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: 1234

{
  "image_base64": "iVBORw0KGgoAAAANSUhEUgAAA...",
  "stats": {
    "byte_size": 13,
    "char_count": 13,
    "recommended_qr_version": 10,
    "fits_in_qr": true,
    "theme": "snowflake",
    "error_correction": "H"
  }
}

                    ↓

┌─────────────────────────────────────────────────────────┐
│ STEP 15: Client Receives Response                       │
└─────────────────────────────────────────────────────────┘

Client (Streamlit/Browser/curl) receives:
- Status code: 200
- JSON body with base64 image and stats
- Decodes base64 to display QR code image
```

**Total time:** ~50-150ms depending on complexity

---

## Layer Architecture

### 1. Router Layer (`qr_api/routers/`)

**Purpose**: HTTP endpoint definitions and request/response handling

**Responsibilities:**
- Define API endpoints (paths, methods)
- Handle request validation errors
- Call service layer functions
- Return HTTP responses
- Document endpoints (docstrings)

**Example:**
```python
# qr_api/routers/qr.py

@router.post("/generate", response_model=QRGenerateResponse)
async def generate_qr(request: QRGenerateRequest):
    """
    Endpoint handler - thin layer
    Validates input, calls service, returns output
    """
    try:
        # Call service layer (business logic)
        qr_img = generate_qr_code(
            data=request.data,
            theme=request.theme,
            error_correction=request.error_correction
        )

        # Call another service
        img_base64 = qr_image_to_base64(qr_img)
        stats = get_greeting_stats(request.data)

        # Return response
        return QRGenerateResponse(
            image_base64=img_base64,
            stats=stats
        )
    except Exception as e:
        # Convert to HTTP error
        raise HTTPException(status_code=500, detail=str(e))
```

**Key principle**: Routers are **thin** - they don't contain business logic.

---

### 2. Service Layer (`qr_api/services/`)

**Purpose**: Business logic and core functionality

**Responsibilities:**
- Implement actual QR generation
- Handle theme icon loading
- Encode/decode greetings
- Perform calculations
- Interact with external libraries (qrcode, PIL, cv2)

**Example:**
```python
# qr_api/services/qr_generator.py

def generate_qr_code(data: str, theme: str, error_correction: str) -> Image.Image:
    """
    Pure business logic - no HTTP concerns
    Can be tested independently
    Can be reused in other contexts
    """
    # Create QR code
    qr = qrcode.QRCode(...)
    qr.add_data(data)
    img = qr.make_image(...)

    # Add theme icon if needed
    if theme != "general":
        icon = load_theme_icon(theme, size)
        img = embed_icon(img, icon)

    return img
```

**Key principle**: Services are **reusable** - they work without HTTP context.

---

### 3. Schema Layer (`qr_api/schemas/`)

**Purpose**: Data validation and serialization

**Responsibilities:**
- Define request/response structure
- Validate incoming data
- Provide type safety
- Generate OpenAPI documentation
- Serialize Python objects to JSON

**Example:**
```python
# qr_api/schemas/qr.py

class QRGenerateRequest(BaseModel):
    """
    Defines what the API accepts
    Pydantic validates automatically
    """
    data: str = Field(..., description="Data to encode")
    theme: str = Field(default="general")
    error_correction: Literal["L", "M", "Q", "H"] = Field(default="H")

    # Optional: custom validation
    @validator('data')
    def data_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('data cannot be empty')
        return v
```

**Key principle**: Schemas define the **contract** between client and server.

---

### 4. Configuration Layer (`qr_api/config.py`)

**Purpose**: Centralized configuration

**Responsibilities:**
- Store constants (API_HOST, API_PORT, etc.)
- Define file paths (ICONS_DIR)
- Store theme mappings (THEME_ICONS)
- Centralize settings for easy modification

**Example:**
```python
# qr_api/config.py

from pathlib import Path

# API Settings
API_HOST = "127.0.0.1"
API_PORT = 8000
API_PREFIX = "/api/v1"

# File Paths (absolute, not relative)
STREAMLIT_DIR = Path(__file__).parent.parent
ICONS_DIR = STREAMLIT_DIR / "icons"

# Business Logic Constants
THEME_ICONS = {
    "snowflake": "❄️",
    "hearts": "❤️",
    # ...
}
```

**Key principle**: Configuration is **centralized** and **portable**.

---

## Design Patterns

### 1. Layered Architecture Pattern

```
Presentation Layer (Routers)
        ↓
Business Logic Layer (Services)
        ↓
Data Access Layer (File System, External APIs)
```

**Benefits:**
- **Separation of concerns** - each layer has one responsibility
- **Testability** - can test services without HTTP
- **Reusability** - services can be used in other apps
- **Maintainability** - changes in one layer don't affect others

---

### 2. Dependency Injection Pattern

FastAPI uses dependency injection for shared resources:

```python
# Example: Sharing configuration
from fastapi import Depends

def get_config():
    return {"api_key": "...", "max_size": 1000}

@router.get("/items")
async def get_items(config = Depends(get_config)):
    # config is automatically injected
    return fetch_items(config["api_key"])
```

**Benefits:**
- **Loose coupling** - functions don't create their own dependencies
- **Testability** - easy to inject mocks
- **Reusability** - dependencies can be shared

---

### 3. Repository Pattern (Implicit)

Services act as repositories for data:

```python
# theme_manager.py acts as a "repository" for theme data

def get_available_themes() -> list[dict]:
    """Abstract away how themes are stored"""
    # Currently: hardcoded dict
    # Future: could be database, API, etc.
    return [...themes...]

def load_theme_icon(theme: str) -> Image:
    """Abstract away how icons are loaded"""
    # Currently: file system
    # Future: could be S3, CDN, etc.
    return icon
```

**Benefits:**
- **Abstraction** - callers don't know where data comes from
- **Flexibility** - can change storage without changing API
- **Testing** - easy to mock data sources

---

### 4. Factory Pattern (QR Code Creation)

```python
def generate_qr_code(data, theme, error_correction):
    """Factory function - creates QR codes based on input"""

    # Determine error correction level
    ec_level = ERROR_CORRECTION_MAP[error_correction]

    # Create appropriate QR code
    qr = qrcode.QRCode(error_correction=ec_level, ...)

    # Add theme-specific features
    if theme != "general":
        qr = add_theme_icon(qr, theme)

    return qr
```

**Benefits:**
- **Encapsulation** - creation logic is centralized
- **Flexibility** - easy to add new QR types
- **Consistency** - all QR codes created the same way

---

### 5. Adapter Pattern (Base64 Conversion)

```python
def qr_image_to_base64(img: Image.Image) -> str:
    """Adapts PIL Image to base64 string for JSON transport"""
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    return base64.b64encode(buf.read()).decode()
```

**Benefits:**
- **Interface compatibility** - PIL Image → JSON-compatible string
- **Reusability** - adapter can be used anywhere
- **Separation** - conversion logic is isolated

---

## Embedded Deployment Model

### Why Embedded?

Instead of running the API as a separate process, we embed it within the Streamlit app.

**Traditional Model:**
```
Terminal 1: uvicorn qr_api.main:app
Terminal 2: streamlit run app.py

User manages 2 processes
```

**Embedded Model:**
```
Terminal 1: streamlit run app.py
  └─ Automatically starts API in background thread

User manages 1 process
```

### How Embedding Works

**In `app.py`:**

```python
import threading
import uvicorn

def start_embedded_api_server():
    """Start FastAPI in background thread"""

    # 1. Import FastAPI app
    from qr_api.main import app
    from qr_api.config import API_HOST, API_PORT

    # 2. Create uvicorn server
    config = uvicorn.Config(
        app=app,
        host=API_HOST,
        port=API_PORT,
        log_level="warning"
    )
    server = uvicorn.Server(config)

    # 3. Run in daemon thread
    def run_server():
        import asyncio
        asyncio.run(server.serve())

    thread = threading.Thread(
        target=run_server,
        daemon=True,  # ← Dies when main thread dies
        name="QR-API-Server"
    )
    thread.start()

    # 4. Wait for startup
    time.sleep(3)
    return True
```

**Thread Model:**
```
┌────────────────────────────────────┐
│     Main Process (Python)          │
│                                    │
│  ┌──────────────────────────────┐ │
│  │ Main Thread (Streamlit)      │ │
│  │                              │ │
│  │ - Runs Streamlit UI          │ │
│  │ - Handles user interactions  │ │
│  │ - Renders web pages          │ │
│  └──────────────────────────────┘ │
│                                    │
│  ┌──────────────────────────────┐ │
│  │ Daemon Thread (API Server)   │ │
│  │                              │ │
│  │ - Runs uvicorn               │ │
│  │ - Handles API requests       │ │
│  │ - Independent event loop     │ │
│  └──────────────────────────────┘ │
│                                    │
│  Both threads share:               │
│  - Memory space                    │
│  - File system access              │
│  - Global Python interpreter       │
└────────────────────────────────────┘
```

### Benefits

1. **Simplified deployment** - one command to start everything
2. **Automatic lifecycle** - API starts/stops with Streamlit
3. **Shared resources** - both can access same files/config
4. **Development convenience** - easier testing

### Challenges

1. **Threading complexity** - must be careful with shared state
2. **Resource competition** - both consume CPU/memory
3. **Debugging** - harder to isolate issues
4. **Port conflicts** - must ensure port 8000 is available

### Mitigation with Session State

```python
# Prevent multiple API instances
if 'api_server_started' not in st.session_state:
    st.session_state.api_server_started = False

if not st.session_state.api_server_started:
    start_embedded_api_server()
    st.session_state.api_server_started = True
```

**Why this works:**
- `st.session_state` persists across Streamlit reruns
- Each user session gets own state
- API only starts once per session

---

## Code Organization

### Directory Structure Rationale

```
qr_api/
├── __init__.py              # Package marker
├── main.py                  # Application entry point
├── config.py                # Configuration (imported by all)
├── routers/                 # HTTP endpoints (organized by resource)
│   ├── __init__.py
│   ├── health.py           # Health check (simple, separate)
│   ├── qr.py               # QR operations (related endpoints)
│   └── greeting.py         # Greeting operations (related endpoints)
├── services/                # Business logic (organized by domain)
│   ├── __init__.py
│   ├── qr_generator.py     # QR code creation
│   ├── theme_manager.py    # Theme/icon management
│   └── greeting_service.py # Greeting encoding/decoding
└── schemas/                 # Data models (organized by router)
    ├── __init__.py
    ├── qr.py               # QR-related schemas
    └── greeting.py         # Greeting-related schemas
```

### Why This Structure?

**Scalability:**
- Easy to add new routers (e.g., `analytics.py`)
- Easy to add new services (e.g., `email_service.py`)
- Easy to add new schemas (e.g., `analytics.py`)

**Clarity:**
- Related code is grouped together
- Purpose of each file is clear
- Easy to navigate

**Maintainability:**
- Changes to QR logic don't affect greeting logic
- Each module has single responsibility
- Easy to test individual components

**Convention:**
- Follows FastAPI best practices
- Similar to Django/Flask project structures
- Familiar to most Python developers

---

## Summary

### Key Takeaways

1. **FastAPI** = Web framework that handles routing, validation, and docs
2. **Uvicorn** = ASGI server that runs the FastAPI app
3. **Swagger** = Auto-generated from code (Pydantic models + docstrings)
4. **Layers** = Routers → Services → External dependencies
5. **Embedded** = API runs in background thread alongside Streamlit

### Request Flow Summary

```
Client Request
  → Uvicorn (ASGI Server)
    → FastAPI Middleware (CORS, exceptions)
      → Router (endpoint handler)
        → Pydantic Validation (request)
          → Service Layer (business logic)
            → External Libraries (qrcode, PIL)
          ← Service Layer (returns data)
        ← Pydantic Serialization (response)
      ← Router (returns response object)
    ← FastAPI (JSON response)
  ← Uvicorn (HTTP response)
← Client Response
```

### Design Principles Applied

- ✅ **Separation of Concerns** - Each layer has one job
- ✅ **Single Responsibility** - Each function does one thing
- ✅ **Don't Repeat Yourself** - Shared logic in services
- ✅ **Open/Closed** - Easy to extend, hard to break
- ✅ **Dependency Inversion** - Depend on abstractions, not implementations

---

**Document Version**: 1.0
**Last Updated**: 2024-01-15
**Author**: QR Code Generation API Team
