import sys
import os
sys.path.append(os.path.abspath("e:/code2/netshare/streamlit"))

from utils.url_utils import classify_background, convert_facebook_to_embed_url

test_url = "https://www.facebook.com/share/r/1GzVWWtk3P/"

print(f"Testing URL: {test_url}")

# Test Classification
bg_type = classify_background(test_url)
print(f"Classification: {bg_type}")
assert bg_type == 'facebook', f"Expected 'facebook', got '{bg_type}'"

# Test Conversion
embed_url = convert_facebook_to_embed_url(test_url)
print(f"Embed URL: {embed_url}")
assert embed_url is not None, "Embed URL should not be None"
assert "facebook.com/plugins/video.php" in embed_url, "Should be a Facebook video plugin URL"

print("✅ Validation successful!")
