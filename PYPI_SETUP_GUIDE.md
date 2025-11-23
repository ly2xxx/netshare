# NetShare PyPI Publication Guide

This guide contains all the steps to prepare and publish NetShare to PyPI.

## Current Status

✅ **Completed:**
- Created `netshare/` package directory
- Created `netshare/__init__.py`
- Created `netshare/__main__.py`
- Copied `netshare.py` → `netshare/app.py`
- Copied `config.py` → `netshare/config.py`
- Copied `templates/` → `netshare/templates/`
- Created `pyproject.toml`

⏳ **Remaining Steps:**
- Create LICENSE file
- Create MANIFEST.in
- Update imports in code
- Update README.md
- Test local installation
- Build and publish

---

## Step 1: Create LICENSE File

Create a file named `LICENSE` in the project root with the GPL-3.0 license text.

You can get the full license text from: https://www.gnu.org/licenses/gpl-3.0.txt

Or use this abbreviated version:

```
GNU GENERAL PUBLIC LICENSE
Version 3, 29 June 2007

Copyright (C) 2024 NetShare Contributors

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
```

**Quick command to download full license:**
```bash
curl https://www.gnu.org/licenses/gpl-3.0.txt -o LICENSE
```

---

## Step 2: Create MANIFEST.in

Create `MANIFEST.in` in the project root:

```
include README.md
include LICENSE
include requirements.txt
include *.ps1
recursive-include netshare/templates *.html
recursive-include image *
```

**Command:**
```bash
cat > MANIFEST.in << 'EOF'
include README.md
include LICENSE
include requirements.txt
include *.ps1
recursive-include netshare/templates *.html
recursive-include image *
EOF
```

---

## Step 3: Update Code Imports

The code in `netshare/app.py` needs to be updated to use relative imports for the config module.

**In `netshare/app.py`, change line 24:**

From:
```python
from config import SecurityConfig, AppConfig
```

To:
```python
from netshare.config import SecurityConfig, AppConfig
```

**Or use relative import:**
```python
from .config import SecurityConfig, AppConfig
```

**Command to update:**
```bash
cd /mnt/h/code/yl/netshare
sed -i 's/from config import/from netshare.config import/' netshare/app.py
```

---

## Step 4: Update AppConfig References

The config module references `AppConfig.FOLDERS_CONFIG_FILE` which may not be defined. Add this to `netshare/config.py` if missing:

```python
class AppConfig:
    DEFAULT_PORT = 5000
    DEFAULT_HOST = '0.0.0.0'
    SERVER_NAME = "NetShare"
    VERSION = "1.0.0"
    ENABLE_ACCESS_LOG = True
    MAX_SHARED_FOLDERS = 20
    FOLDERS_CONFIG_FILE = "shared_folders.json"  # Add this line if missing
```

---

## Step 5: Update README.md

Add PyPI installation instructions at the beginning of the README.md file.

**Add this section after the header:**

```markdown
## Installation

### From PyPI (Recommended)

```bash
pip install netshare
```

### From Source

```bash
git clone https://github.com/yourusername/netshare.git
cd netshare
pip install -r requirements.txt
```

## Quick Start

After installation via pip:

```bash
netshare --help
netshare --gui  # GUI folder selection (Windows/Mac/Linux with tkinter)
netshare --folder /path/to/share
```
```

---

## Step 6: Verify Package Structure

Your directory structure should now look like:

```
netshare/
├── pyproject.toml          ✅ Created
├── LICENSE                 ⏳ Create manually
├── MANIFEST.in             ⏳ Create manually
├── README.md               ✅ Exists (update with pip install)
├── requirements.txt        ✅ Exists
├── firewall_diagnostic.ps1 ✅ Exists
├── fix_firewall.ps1        ✅ Exists
├── image/                  ✅ Exists
├── netshare/               ✅ Created
│   ├── __init__.py         ✅ Created
│   ├── __main__.py         ✅ Created
│   ├── app.py              ✅ Created
│   ├── config.py           ✅ Created
│   └── templates/          ✅ Created
│       ├── browse.html
│       ├── error.html
│       └── index.html
└── (old files can remain for now)
```

---

## Step 7: Install Build Tools

```bash
pip install --upgrade build twine
```

## Verify installation
```bash
  python -m build --version
  twine --version
```
---

## Step 8: Test Local Installation

Before publishing, test that the package installs correctly:

```bash
# In the project root directory
pip install -e .

# Test the command works
netshare --help

# Test module execution
python -m netshare --help
```

**Expected output:** NetShare help message showing command-line options

---

## Step 9: Build Distribution Files

```bash
# Clean old builds (if any)
rm -rf dist/ build/ *.egg-info netshare.egg-info

# Build the package
python -m build
```

This creates:
- `dist/netshare-1.0.0.tar.gz` (source distribution)
- `dist/netshare-1.0.0-py3-none-any.whl` (wheel distribution)

---

## Step 10: Check Package with Twine

```bash
twine check dist/*
```

**Expected output:** `PASSED` for all files

---

## Step 11: Test Upload to TestPyPI

Before uploading to the real PyPI, test with TestPyPI:

**A. Create TestPyPI Account:**
- Go to https://test.pypi.org/account/register/
- Verify your email
- Create an API token at https://test.pypi.org/manage/account/token/

**B. Upload to TestPyPI:**
```bash
twine upload --repository testpypi dist/*
```

When prompted:
- Username: `__token__`
- Password: (paste your TestPyPI API token)

**C. Test Installation from TestPyPI:**
```bash
# In a fresh virtual environment
pip cache purge

pip install --no-cache-dir --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ netshare

# Test it works
netshare --help
```

---

## Step 12: Upload to Real PyPI

Once TestPyPI works:

**A. Create PyPI Account:**
- Go to https://pypi.org/account/register/
- Verify your email
- Create an API token at https://pypi.org/manage/account/token/

**B. Upload to PyPI:**
```bash
twine upload dist/*
```

When prompted:
- Username: `__token__`
- Password: (paste your PyPI API token)

---

## Step 13: Verify Publication

**Visit your package page:**
- https://pypi.org/project/netshare/

**Test installation:**
```bash
# In a fresh environment
pip install netshare

# Run it
netshare --help
```

---

## Step 14: Update GitHub Repository (Optional)

**A. Add PyPI badge to README.md:**

```markdown
[![PyPI version](https://badge.fury.io/py/netshare.svg)](https://badge.fury.io/py/netshare)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
```

**B. Update repository URL in pyproject.toml:**

Replace `https://github.com/yourusername/netshare` with your actual GitHub username/organization.

**C. Create a git tag for the release:**

```bash
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

---

## Troubleshooting

### Package name already taken?

If `netshare` is already taken on PyPI, choose an alternative:
- `netshare-wifi`
- `py-netshare`
- `simple-netshare`
- `local-netshare`

Update the name in `pyproject.toml`:
```toml
[project]
name = "your-alternative-name"
```

### Import errors after installation?

Make sure all imports in `netshare/app.py` use the package prefix:
```python
from netshare.config import SecurityConfig, AppConfig
```

### Templates not found?

Verify `MANIFEST.in` includes:
```
recursive-include netshare/templates *.html
```

And in `pyproject.toml`:
```toml
[tool.setuptools.package-data]
netshare = ["templates/*.html"]
```

---

## Future Updates

To release a new version:

1. Update version in `pyproject.toml` and `netshare/__init__.py`
2. Update CHANGELOG or README with changes
3. Rebuild: `python -m build`
4. Upload: `twine upload dist/*`
5. Tag release: `git tag v1.0.x && git push origin v1.0.x`

---

## Automation with GitHub Actions (Optional)

Create `.github/workflows/publish.yml`:

```yaml
name: Publish to PyPI

on:
  release:
    types: [created]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.x'
      - name: Install dependencies
        run: |
          pip install build twine
      - name: Build package
        run: python -m build
      - name: Publish to PyPI
        env:
          TWINE_USERNAME: __token__
          TWINE_PASSWORD: ${{ secrets.PYPI_TOKEN }}
        run: twine upload dist/*
```

Then add your PyPI API token as a GitHub secret named `PYPI_TOKEN`.

---

## Summary Checklist

- [ ] Create LICENSE file
- [ ] Create MANIFEST.in
- [ ] Update imports in netshare/app.py
- [ ] Update README.md with pip install instructions
- [ ] Install build tools: `pip install build twine`
- [ ] Test local install: `pip install -e .`
- [ ] Build package: `python -m build`
- [ ] Check package: `twine check dist/*`
- [ ] Test on TestPyPI
- [ ] Upload to PyPI: `twine upload dist/*`
- [ ] Verify: `pip install netshare`
- [ ] Update GitHub with badges and tags

---

**Good luck with your PyPI publication! 🚀**
