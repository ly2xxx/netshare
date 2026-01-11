import time
import webbrowser
import requests
import datetime
import sys

# Configuration
# The base URL of your Streamlit application
BASE_URL = "https://qr-greeting.streamlit.app/"

# Predefined QR code or URL parameters.
# If you want to open the scan tab with a specific message/QR code, set it here.
# Example: "?tab=scan&m=eyJtIjoiSGVsbG8gV29ybGQifQ=="
# For just the scan tab: "?tab=scan"
URL_PARAMS = "?tab=scan"

# Complete Target URL
TARGET_URL = f"{BASE_URL}{URL_PARAMS}"

# How often to open the URL (in hours)
INTERVAL_HOURS = 1

def keep_alive():
    """
    Script to keep the Streamlit app awake by accessing it periodically.
    """
    print("="*50)
    print(f"Keep-Alive Script for {BASE_URL}")
    print(f"Target URL: {TARGET_URL}")
    print(f"Interval: {INTERVAL_HOURS} hour(s)")
    print("="*50)
    print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Script started.")

    while True:
        try:
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"[{timestamp}] Accessing app...")
            
            # Method 1: Headless request using requests library
            # This is less intrusive and good for background running
            try:
                # Set a user-agent to look like a real browser (helps avoid some bot filters)
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }
                response = requests.get(TARGET_URL, headers=headers)
                print(f"[{timestamp}] Request successful. Status Code: {response.status_code}")
            except ImportError:
                 print(f"[{timestamp}] 'requests' library not found. Falling back to browser open.")
                 # Fallback/Alternative: Open in default web browser
                 # This matches your request to "open its scan tab"
                 webbrowser.open(TARGET_URL)
                 print(f"[{timestamp}] Opened in default web browser.")
            except Exception as e:
                print(f"[{timestamp}] HTTP Request failed: {e}")
                print(f"[{timestamp}] Attempting to open in browser as fallback...")
                webbrowser.open(TARGET_URL)

            # Note: You can force using browser by commenting out the requests block 
            # and uncommenting the line below:
            # webbrowser.open(TARGET_URL)

        except Exception as e:
            print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] General Error: {e}")
        
        # Wait for the defined interval
        print(f"Sleeping for {INTERVAL_HOURS} hour(s)...")
        time.sleep(INTERVAL_HOURS * 3600)

if __name__ == "__main__":
    # Check for requests library availability
    try:
        import requests
    except ImportError:
        print("Warning: 'requests' library not found. The script will use the web browser to open the link.")
        print("To install requests: pip install requests")
        print("-" * 20)

    try:
        keep_alive()
    except KeyboardInterrupt:
        print("\nScript stopped by user.")
        sys.exit(0)
