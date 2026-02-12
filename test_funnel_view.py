"""Test funnel view rendering"""
from urllib.parse import parse_qs, urlparse

# The QR code URL
qr_url = "https://qr-greeting.streamlit.app/?tab=view&t=funnel&f=Pottery+to+the+People&th=fireworks&bg=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DEOJrHVfFHpE&m=Learn+to+make+this%3F+Get+the+template+%2B+10%25+off%21%0A%0A%E2%9C%93+Video+tutorial+included+%0A%E2%9C%93+Beginner-friendly%0A%E2%9C%93+Print+at+any+size&fh=%F0%9F%8E%81+Want+to+make+this%3F&fc=Shop+Now+%E2%86%92&fu=https%3A%2F%2Fwww.etsy.com%2Fuk%2Flisting%2F4394694207%2Fprintable-pottery-template-kit-for-slab%3Fref%3Dshop_home_feat_1%26sts%3D1%26dd%3D1%26logging_key%3Ddd841c6ca0be4ed9361f1441f9273362e3f81178%253A4394694207&fp=%F0%9F%8F%B7%EF%B8%8F+YOUTUBE10&fg=+%E2%8F%B0+YouTube+viewers+only+-+Expires+in+48+hours"

parsed = urlparse(qr_url)
params = {k: v[0] if len(v) == 1 else v for k, v in parse_qs(parsed.query).items()}

print("Extracted params:")
for k, v in params.items():
    print(f"  {k}: {v}")

print("\nChecking video conversion:")
from streamlit.utils.video_utils import convert_to_embed_url

bg_url = params.get('bg', '')
print(f"Original: {bg_url}")

embed_url = convert_to_embed_url(bg_url)
print(f"Embed: {embed_url}")

print("\nGreeting type check:")
print(f"  t={params.get('t', '')}")
print(f"  Is funnel: {params.get('t') == 'funnel'}")
