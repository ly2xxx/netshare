# Holiday Greeting QR Implementation Plan

## Executive Summary

**Goal**: Generate animated QR codes with personalized holiday greeting messages

**Status**: ✅ Amazing-QR has excellent animated GIF QR support built-in - perfect for this use case!

**Timeline**: 2-3 hours for MVP, 3 days for full-featured version

---

## What Amazing-QR Already Has

### ✅ Animated GIF QR Generation (Lines 96-117 in amzqr.py)

**Process**:
1. Extract all frames from input GIF
2. Generate QR code for each frame with that frame as background
3. Recombine into animated GIF preserving timing

**Example**: `/mnt/h/code/3rd/amazing-qr/example/*.gif` - all remain scannable while animated!

**Key Features**:
- Colorization support
- Contrast/brightness adjustment
- Frame timing preservation
- Multiple output formats

---

## What We Need to Add

### 1. Greeting JSON Schema (`greeting_formats.py`)
**Purpose**: Structure greeting data in compact JSON format

```python
def create_holiday_greeting(from_name, to_name, message, occasion, theme):
    return {
        "v": "1.0",
        "type": "greeting",
        "from": from_name,
        "to": to_name,
        "occasion": occasion,
        "message": message,
        "theme": theme,
        "created": datetime.utcnow().isoformat()
    }

def compact_greeting(payload):
    """Minimize JSON - remove whitespace"""
    return json.dumps(payload, separators=(',', ':'))
```

**Size**: ~240 bytes for typical greeting

---

### 2. Optional Compression (Add to `data.py`)
**Purpose**: Fit longer messages in QR codes

```python
import zlib
import base64

def compress_text(text):
    compressed = zlib.compress(text.encode('utf-8'), level=9)
    return base64.b64encode(compressed).decode('ascii')

def decompress_text(encoded_text):
    try:
        compressed = base64.b64decode(encoded_text)
        return zlib.decompress(compressed).decode('utf-8')
    except:
        return encoded_text  # Not compressed
```

**Benefit**: 40-50% size reduction → 240 bytes → ~140 bytes

---

### 3. Holiday Theme GIFs (Create `themes/holiday/` directory)

**Required Themes** (6-8 animated GIFs):
- `snowflake.gif` - Falling snowflakes ❄️
- `fireworks.gif` - Bursting fireworks 🎆
- `lights.gif` - Twinkling holiday lights ✨
- `stars.gif` - Starry night ⭐
- `confetti.gif` - Celebration confetti 🎉
- `champagne.gif` - Clinking glasses 🥂

**Specs**:
- Size: 400x400 to 600x600 pixels
- Frames: 5-15 frames
- Duration: 100-200ms per frame
- File size: <500KB

---

### 4. Simple Generator Interface

**Option A: CLI Script** (`create_greeting_qr.py`)
```python
from amzqr import run
from amzqr.greeting_formats import create_holiday_greeting, compact_greeting

print("🎄 Holiday Greeting QR Generator")
from_name = input("From: ")
to_name = input("To: ")
message = input("Your message: ")
theme = input("Theme (snowflake/fireworks/lights): ")

greeting = create_holiday_greeting(from_name, to_name, message, "Holiday 2025", theme)
qr_data = compact_greeting(greeting)

ver, level, qr_path = run(
    words=qr_data,
    picture=f"themes/holiday/{theme}.gif",
    colorized=True,
    level='H',
    save_name=f"{to_name}_greeting.gif"
)

print(f"✅ Created: {qr_path}")
```

**Option B: Streamlit Web App** - See detailed code in main plan

---

## Implementation Steps

### Phase 1: Core Enhancement (2 hours)

**Files to Create**:
1. `/mnt/h/code/3rd/amazing-qr/amzqr/greeting_formats.py` (~50 lines)
   - `create_holiday_greeting()` function
   - `compact_greeting()` function
   - `parse_greeting()` function

**Files to Modify** (Optional - for compression):
2. `/mnt/h/code/3rd/amazing-qr/amzqr/mylibs/data.py`
   - Add `compress_text()` and `decompress_text()` functions

3. `/mnt/h/code/3rd/amazing-qr/amzqr/amzqr.py`
   - Add `compress=False` parameter to `run()` function
   - Call compression before QR generation if enabled

**Testing**:
- Create sample greeting JSON
- Test compression ratio
- Generate test QR and verify scannability

---

### Phase 2: Holiday Themes (1-2 hours)

**Tasks**:
1. Create directory: `/mnt/h/code/3rd/amazing-qr/themes/holiday/`
2. Source 6-8 holiday GIF animations:
   - Search Giphy/Tenor for "snowflake loop", "fireworks animation"
   - Download and optimize (resize to 500x500, reduce frames if needed)
   - Test each theme generates scannable QR

**Tools**:
- GIMP or Photoshop for GIF optimization
- Online GIF editors (ezgif.com)
- Reduce frames to 8-12 if file >500KB

---

### Phase 3: Generator Interface (2-4 hours)

**Simple CLI** (30 minutes):
- Create `create_greeting_qr.py` with interactive prompts
- Test with all themes

**Web App** (3-4 hours):
- Build Streamlit app with create/scan pages
- Add theme previews
- Add download button
- Deploy locally or to Streamlit Cloud

---

### Phase 4: Testing & Polish (2-3 hours)

**Scanability Tests**:
- [ ] Test on iPhone (iOS Camera app)
- [ ] Test on Android (Google Lens)
- [ ] Test various message lengths (100, 300, 500 chars)
- [ ] Verify all themes scan correctly

**Quality Tests**:
- [ ] Animation smooth (no frame drops)
- [ ] Colors preserved
- [ ] File sizes reasonable (<1MB)

**Documentation**:
- [ ] Create README with examples
- [ ] Add usage instructions
- [ ] Create 3-4 demo greeting QRs

---

## Message Capacity Reference

| Message Length | Uncompressed | Compressed | QR Version |
|----------------|--------------|-----------|------------|
| 100 chars (~15 words) | ~150 bytes | ~90 bytes | V10-H |
| 200 chars (~30 words) | ~250 bytes | ~150 bytes | V15-H |
| 300 chars (~50 words) | ~350 bytes | ~210 bytes | V20-H |
| 500 chars (~80 words) | ~550 bytes | ~330 bytes | V30-H |
| 1000 chars (~150 words) | ~1050 bytes | ~630 bytes | V40-H |

**Recommendation**: Default to error correction level 'H' for maximum scan reliability

---

## Example Use Cases

### 1. Christmas Card Greeting
```python
greeting = create_holiday_greeting(
    from_name="Alice",
    to_name="Bob",
    message="Merry Christmas! Wishing you joy and happiness this season. Thank you for being a wonderful friend!",
    occasion="Christmas 2025",
    theme="snowflake"
)
# Output: Animated snowflake QR (200 bytes compressed)
```

### 2. New Year's Time Capsule
```python
greeting = create_holiday_greeting(
    from_name="Bob",
    to_name="Future Me",
    message="2025 was incredible! Here's to growth and new adventures in 2026!",
    occasion="New Year 2026",
    theme="fireworks"
)
# Output: Animated fireworks QR
```

### 3. Wedding Save the Date
```python
greeting = create_holiday_greeting(
    from_name="Emma & James",
    to_name="Friends and Family",
    message="We're getting married! Save the date: June 15, 2026. More details to follow!",
    occasion="Wedding Announcement",
    theme="champagne"
)
# Output: Animated champagne QR
```

---

## Critical Files Summary

### Files to Create:
1. **`amzqr/greeting_formats.py`** - JSON schemas and helpers (50 lines)
2. **`create_greeting_qr.py`** - CLI tool (40 lines)
3. **`themes/holiday/*.gif`** - 6-8 animated GIF themes
4. **`app.py`** (optional) - Streamlit web interface (150 lines)

### Files to Modify (Optional):
1. **`amzqr/mylibs/data.py`** - Add compression functions
2. **`amzqr/amzqr.py`** - Add compress parameter

### No Changes Needed:
- **`amzqr/amzqr.py` lines 96-117** - Animated GIF logic already perfect!

---

## Quick Start (Minimum Viable Product)

**Goal**: Working greeting QR generator in 2 hours

1. **Create `greeting_formats.py`** (30 min)
   - Basic JSON schema functions
   - No compression for MVP

2. **Find 2-3 GIF themes** (30 min)
   - Download from Giphy/Tenor
   - Save to `themes/holiday/`

3. **Create CLI script** (30 min)
   - Interactive prompts
   - Generate QR using existing amazing-qr

4. **Test** (30 min)
   - Generate sample greeting
   - Scan with phone
   - Verify animation works

**Result**: Working prototype without compression or web interface

---

## Full Featured Version (3 Days)

### Day 1: Core
- Morning: Create `greeting_formats.py` with all schemas
- Afternoon: Add compression to `data.py` and `amzqr.py`
- Evening: Test compression ratios and scannability

### Day 2: Content & Interface
- Morning: Curate 6-8 holiday theme GIFs
- Afternoon: Build Streamlit web interface
- Evening: Test theme combinations

### Day 3: Polish
- Morning: Add QR scanning to web app
- Afternoon: Create examples and documentation
- Evening: Final testing on multiple devices

---

## Success Criteria

- [x] Animated QR generation works (already ✅)
- [ ] Greeting JSON schema created
- [ ] 6-8 holiday theme GIFs ready
- [ ] CLI or web interface working
- [ ] QRs scan on iOS and Android (>95% success)
- [ ] Animations smooth and beautiful
- [ ] File sizes <1MB for sharing

---

## Why This Will Work

1. **Built on Proven Tech**: Animated QR already working in amazing-qr
2. **Low Risk**: Minimal code changes, mostly new files
3. **High Value**: Beautiful, shareable greeting cards
4. **Quick to Build**: 2-3 hours for MVP
5. **Delightful UX**: Animated QRs are visually appealing

---

## Next Steps

Ready to implement! Choose your path:

**Path A - Quick MVP** (2-3 hours):
1. Create `greeting_formats.py`
2. Download 3 GIF themes
3. Build simple CLI script
4. Test and iterate

**Path B - Full Version** (3 days):
1. All MVP features
2. Add compression support
3. Build Streamlit web app
4. Create complete theme library
5. Polish and document

**Recommendation**: Start with MVP, then enhance based on feedback!
