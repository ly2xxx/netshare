# Multi-Part Download Guide

## What is Multi-Part Download?

For very large files (>2GB), NetShare offers a multi-part download option that splits files into smaller chunks. This is helpful when:
- Your device can't download very large files in one go
- You want to download parts separately and resume if interrupted
- Your browser or device has file size limitations

## How to Use

### 1. Download Parts

1. Browse to a folder containing large files
2. Large files will show a **"LARGE FILE"** badge
3. Click **"Download Options"** button
4. Choose either:
   - **Download Complete File** - Standard download (if your device supports it)
   - **Download in Parts** - Click individual part numbers to download each chunk

### 2. Reassemble Parts

After downloading all parts, reassemble them on your computer:

#### Option 1: Using the Python Script (Recommended)

```bash
# Navigate to folder with downloaded parts
cd /path/to/downloads

# Run reassembly script
python reassemble_parts.py 'filename.part*.mkv'

# Or specify output filename
python reassemble_parts.py 'movie.part*.mp4' output.mp4
```

The script will:
- Find all matching part files
- Combine them in the correct order
- Create the original file
- Optionally delete the parts after reassembly

#### Option 2: Manual Reassembly (Command Line)

**On Windows (Command Prompt):**
```cmd
copy /b filename.part001.mkv + filename.part002.mkv + filename.part003.mkv output.mkv
```

**On Linux/Mac:**
```bash
cat filename.part001.mkv filename.part002.mkv filename.part003.mkv > output.mkv
```

## Configuration

You can customize multi-part download settings in `config.py`:

```python
class AppConfig:
    # Enable/disable multi-part download feature
    ENABLE_MULTIPART_DOWNLOAD = True

    # Files larger than this threshold will offer multi-part option
    MULTIPART_THRESHOLD = 2 * 1024 * 1024 * 1024  # 2GB

    # Size of each download chunk
    MULTIPART_CHUNK_SIZE = 1 * 1024 * 1024 * 1024  # 1GB per part
```

## Example

A 9.5GB movie file would be split into:
- `movie.part001.mkv` - 1GB
- `movie.part002.mkv` - 1GB
- `movie.part003.mkv` - 1GB
- ...
- `movie.part010.mkv` - 0.5GB

Download each part to your Quest 3 or mobile device, then transfer to PC and reassemble.

## Troubleshooting

**Q: Part files won't reassemble correctly**
- Make sure you downloaded ALL parts
- Check that part numbers are sequential
- Verify no parts are corrupted (check file sizes)

**Q: Reassembly script says "No files found"**
- Make sure you're in the correct directory
- Use quotes around the pattern: `'filename.part*.mkv'`
- Check that part files use the exact naming format

**Q: Can I download parts out of order?**
- Yes! Parts can be downloaded in any order
- The reassembly script will combine them correctly based on part numbers
