# Plaintext API for QR Greeting

## Overview

This feature adds URL parameter support to automatically pre-fill greeting fields, enabling seamless integration with external applications.

## API Usage

### Base URL
```
https://qr-greeting.streamlit.app/?tab=create
```

### Supported Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `from` | string | Sender name | `Dream Tycoon Player` |
| `to` | string | Recipient name | `Fellow Tycoon` |
| `message` | string | Greeting message | `I grew my Dream Fund...` |
| `theme` | string | Visual theme | `confetti`, `snowflake`, `hearts`, etc. |
| `url` | string | Source URL (for attribution) | `https://risk-reward-game.streamlit.app` |

### Example URL

```
https://qr-greeting.streamlit.app/?tab=create&from=Dream+Tycoon+Player&to=Fellow+Tycoon&message=I+grew+my+Dream+Fund+from+%241%2C000+to+%241%2C416+%28%2B41.6%25+profit%29+in+2+rounds%21+Can+you+beat+my+score%3F&theme=confetti&url=https%3A%2F%2Frisk-reward-game.streamlit.app
```

## Implementation Details

### How It Works

1. **URL Parameter Detection**: On page load, the app checks for URL parameters
2. **Session State Population**: If parameters are found, they pre-fill the session state
3. **One-Time Load**: Parameters are only loaded once per session to avoid overwriting user edits
4. **Source Attribution**: If `url` parameter is provided, shows a banner: "✨ Pre-filled from: [url]"

### Code Flow

```python
def load_params_from_url():
    """Load greeting parameters from URL query params if present"""
    query_params = st.query_params
    
    if 'from' in query_params or 'message' in query_params:
        if 'params_loaded_from_url' not in st.session_state:
            st.session_state.params_loaded_from_url = True
            
            # Load parameters into session state
            if 'from' in query_params:
                st.session_state.create_from_name = query_params['from']
            # ... (other parameters)
```

## Integration Examples

### Python (urllib)

```python
import urllib.parse

# Build parameters
params = urllib.parse.urlencode({
    'from': 'Game Player',
    'to': 'Friend',
    'message': 'Check out my score!',
    'theme': 'confetti',
    'url': 'https://your-app.streamlit.app'
})

# Create URL
qr_url = f"https://qr-greeting.streamlit.app/?tab=create&{params}"
```

### JavaScript

```javascript
const params = new URLSearchParams({
    from: 'Game Player',
    to: 'Friend',
    message: 'Check out my score!',
    theme: 'confetti',
    url: 'https://your-app.streamlit.app'
});

const qrUrl = `https://qr-greeting.streamlit.app/?tab=create&${params.toString()}`;
```

### Curl

```bash
curl "https://qr-greeting.streamlit.app/?tab=create&from=Player&to=Friend&message=Hello&theme=confetti"
```

## Available Themes

- `snowflake` - Winter/Christmas theme
- `fireworks` - New Year celebration
- `lights` - Holiday lights
- `stars` - Starry night
- `confetti` - General celebration
- `champagne` - Celebration/party
- `hearts` - Valentine's Day / Love
- `farewell` - Goodbye
- `valentine` - Valentine's Day
- `burn_after_read` - Secret message
- `general` - Default theme

## Use Cases

### 1. Game Score Sharing
Allow players to share achievements via QR codes:
```
?from=Player123&to=Friends&message=Beat level 50!&theme=confetti
```

### 2. Event Invitations
Pre-fill event details:
```
?from=EventOrg&to=Guest&message=You're invited to our party!&theme=champagne
```

### 3. Cross-App Integration
Link from one app to QR greeting generator:
```
?from=MyApp User&to=Recipient&message=Message&url=https://myapp.com
```

## User Experience

1. User clicks link with parameters
2. QR Greeting app opens on "Create Greeting" tab
3. Form fields are pre-filled with provided values
4. Banner shows: "✨ Pre-filled from: [source-url]"
5. User can edit fields if needed
6. User clicks "Generate" to create QR code

## Technical Considerations

- **URL Encoding**: All parameters must be URL-encoded
- **Character Limits**: Messages should be kept under 300 characters for optimal QR code size
- **Session Persistence**: Parameters only load once per session
- **Reset Capability**: "Create Another" button clears URL parameters

## Benefits

✅ **Seamless Integration**: Apps can link directly to pre-filled forms  
✅ **User Convenience**: No manual data entry required  
✅ **Cross-Promotion**: Apps can reference each other via `url` parameter  
✅ **Viral Growth**: Easy sharing mechanism for user-generated content  

## Future Enhancements

- [ ] Add `background` parameter for GIF/video URLs
- [ ] Add `visible_message` parameter for QR code overlays
- [ ] Add `auto_generate` parameter to skip manual generation step
- [ ] Add webhook support for automated QR generation
