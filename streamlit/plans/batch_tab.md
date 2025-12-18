# Batch QR Code Generation Feature

## Goal
Add a hidden "Batch" tab that allows users to generate multiple QR codes from an Excel spreadsheet. The tab is shown/hidden via a sidebar checkbox.

## Proposed Changes

### `netshare/streamlit/app.py`

#### [MODIFY] [`main()`](file:///h:/code/yl/netshare/streamlit/app.py#L1127)

1.  **Add sidebar checkbox**: `show_batch = st.checkbox("Show Batch Tab")`.
2.  **Conditionally show 5th tab**: If `show_batch`, create tabs with 5 items including "Batch". Otherwise, 4 tabs as before.
3.  **Update `tab_map`** to include "batch": 4 when visible.

#### [NEW] `batch_greeting_tab()` function

1.  **Template Download**: Provide a button to download an Excel template (`.xlsx`).
2.  **File Uploader**: Allow user to upload filled Excel.
3.  **Parse Excel**: Use `pandas` or `openpyxl` to read.
4.  **Generate QR codes**: Loop through rows, call `generate_qr_code()` for each.
5.  **Provide download**: Zip file containing all generated QR images.

---

### Excel Template Columns

| Column | Description | Validation |
|--------|-------------|------------|
| From | Sender name | Required |
| To | Recipient name | Required |
| Message | Greeting message | Required |
| Theme | Icon theme | Dropdown: snowflake, fireworks, lights, stars, confetti, champagne, hearts, general |
| Background | Background for scanned view | Dropdown: Files in `keep/` folder (e.g., christmastree.mp4) or empty |
| VisibleMessage | Text below QR | Optional |

---

### Background in Greeting

#### [MODIFY] [`greeting_formats.py`](file:///h:/code/yl/netshare/streamlit/greeting_formats.py)

1.  Add `background` field to greeting JSON/URL encoding.
2.  Update `encode_greeting_to_url` and `decode_greeting_from_url` to handle `background`.

#### [MODIFY] [`display_greeting_letter()`](file:///h:/code/yl/netshare/streamlit/app.py)

1.  If `greeting.get('background')` is set:
    *   If it's a video (`.mp4`), embed as background video.
    *   If it's an image, set as CSS background.

---

### Dependencies

*   `pandas` - For reading Excel (likely already available via Streamlit ecosystem, but will add to requirements if needed).
*   `openpyxl` - For `.xlsx` support.

---

## Verification Plan

### Manual Verification
1.  Enable "Show Batch Tab" in sidebar.
2.  Download template.
3.  Fill template with test data.
4.  Upload and generate.
5.  Verify QR codes are generated correctly.
6.  Scan a QR code with background set and verify background displays.
