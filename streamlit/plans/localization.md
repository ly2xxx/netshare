# Chinese Localization Plan for Streamlit Holiday Greeting QR

## Overview

**Goal**: Add Simplified Chinese (zh-CN) localization to the Streamlit Holiday Greeting QR application

**Key Decisions**:
- ✅ Simplified Chinese (zh-CN) - Mainland China variant
- ✅ Default language: English (user can switch to Chinese)
- ✅ Keep example greetings in English (show cross-language capability)
- ✅ Keep QR message content as user-entered (only translate UI elements)
- ✅ Approach: Session State + JSON dictionary (optimal for 2 languages)

**Scope**: ~250+ UI text strings across 11 Python files

**Note**: Streamlit has NO native localization support - custom implementation required

---

## Architecture

### New Files to Create

1. **`/mnt/e/code2/netshare/streamlit/i18n.py`**
   - Translation infrastructure module
   - Functions: `init_language()`, `get_text()`, `set_language()`, `get_current_language()`
   - Session state management
   - Fallback logic (zh → en → show key)

2. **`/mnt/e/code2/netshare/streamlit/translations.json`**
   - JSON structure with `en` and `zh` keys
   - Hierarchical key format: `{file}.{component}.{element}`
   - Example: `"app.sidebar.title": "Holiday Greeting QR | 节日问候二维码"`
   - ~250+ translation pairs

### Translation Function Pattern

```python
# Import in each file
from i18n import get_text as _

# Simple usage
st.write(_("file.key"))

# With dynamic content
st.write(_("file.greeting", name=user_name))

# Translations with variables
{
  "en": {"file.greeting": "Hello {name}!"},
  "zh": {"file.greeting": "你好 {name}！"}
}
```

### Language Selector

- **Location**: Top of sidebar in `app.py`
- **Component**: `st.selectbox` with callback
- **Persistence**: Session state only (resets on reload)
- **Default**: English

---

## Critical Files to Modify (Priority Order)

### Phase 1: Infrastructure ⭐
1. **`/mnt/e/code2/netshare/streamlit/i18n.py`** (NEW)
   - Create translation module (~100-150 lines)

2. **`/mnt/e/code2/netshare/streamlit/translations.json`** (NEW)
   - Start with base structure + 20 sample translations
   - Expand incrementally as we translate each file

3. **`/mnt/e/code2/netshare/streamlit/app.py`**
   - Import i18n module
   - Call `init_language()` at startup
   - Add language selector to sidebar (top position)
   - Translate sidebar content: title, tagline, tips, support section, tab names
   - ~15 strings to translate

### Phase 2: Core Tabs 🎯
4. **`/mnt/e/code2/netshare/streamlit/tabs/create_tab.py`**
   - Primary user interaction tab
   - ~70 strings: headers, tips, labels, buttons, messages
   - Add `from i18n import get_text as _` import
   - Replace all user-facing text with `_()` calls
   - **Note**: Keep default greeting message as-is (user content)

5. **`/mnt/e/code2/netshare/streamlit/tabs/components.py`**
   - Shared components used across tabs
   - ~30 strings: theme selector, QR options, validation messages
   - Theme names: translate display labels, keep internal keys unchanged
   - Example: Display "❄️ 雪花" but internal value remains "snowflake"

6. **`/mnt/e/code2/netshare/streamlit/tabs/demo_tab.py`**
   - Interactive demo experience
   - ~45 strings: step instructions, tips, buttons, status messages
   - Keep example greeting content in English

### Phase 3: Secondary Tabs 📄
7. **`/mnt/e/code2/netshare/streamlit/tabs/scan_tab.py`**
   - QR scanning interface
   - ~25 strings: upload prompts, status messages, errors

8. **`/mnt/e/code2/netshare/streamlit/tabs/about_tab.py`**
   - Information and marketing content
   - ~60 strings: feature descriptions, how it works, technical details
   - Important for Chinese users to understand the value proposition

9. **`/mnt/e/code2/netshare/streamlit/tabs/batch_tab.py`**
   - Batch QR generation
   - ~35 strings: instructions, template info, progress messages

10. **`/mnt/e/code2/netshare/streamlit/tabs/examples_tab.py`**
    - Example showcase
    - ~15 strings: titles and descriptions
    - **Keep example message content in English** (per user preference)

### Phase 4: Display & Utilities 🔧
11. **`/mnt/e/code2/netshare/streamlit/qr/display.py`**
    - QR display and rendering
    - ~10 strings: captions, labels, error messages

12. **`/mnt/e/code2/netshare/streamlit/tabs/view_page.py`**
    - Mobile greeting view page
    - ~5 strings: error messages, navigation buttons

### Files NOT Modified
- **`/mnt/e/code2/netshare/streamlit/config.py`** - Icons and theme config (universal, no text)
- **`/mnt/e/code2/netshare/streamlit/greeting_formats.py`** - Data handling (no UI text)
- **`/mnt/e/code2/netshare/streamlit/utils/*`** - Backend utilities (no UI text)

---

## Translation Strategy

### What to Translate
✅ **UI Elements**: Headers, labels, buttons, tips, instructions
✅ **Messages**: Info, warning, error, success messages
✅ **Help Text**: Tooltips, placeholder text, descriptions
✅ **Tab Names**: Main navigation tabs
✅ **Theme Display Names**: User-visible theme labels

### What NOT to Translate
❌ **Emojis**: Keep all emojis (universal visual language)
❌ **Example Messages**: Keep greeting content in English (per user preference)
❌ **User Content**: QR message content stays as user-entered
❌ **Internal Keys**: Theme keys, config values, session state keys
❌ **URLs**: External links, video URLs

### Dynamic Content Handling
```python
# Pattern for variables
st.write(_("qr.stats", bytes=data_size, version=qr_version))

# JSON translation
{
  "en": {"qr.stats": "Data size: {bytes} bytes, Version: {version}"},
  "zh": {"qr.stats": "数据大小：{bytes} 字节，版本：{version}"}
}
```

### Key Naming Convention
- Format: `{file}.{section}.{element}`
- Examples:
  - `app.sidebar.title`
  - `create_tab.step1.title`
  - `create_tab.step1.tip`
  - `common.buttons.generate`
  - `components.theme_selector.label`

---

## Implementation Steps

### Step 1: Create Translation Infrastructure
1. Create `i18n.py` with:
   - `init_language()` - Initialize session state with 'en' default
   - `get_text(key, **kwargs)` - Retrieve translation with variable substitution
   - `set_language(lang_code)` - Switch language and trigger rerun
   - `get_current_language()` - Return current language from session state
   - JSON loading and caching
   - Fallback chain: zh → en → `[missing: key]`

2. Create `translations.json` base structure:
```json
{
  "en": {},
  "zh": {}
}
```

### Step 2: Add Language Selector to App
1. Modify `app.py`:
   - Import `i18n` module
   - Call `init_language()` before main()
   - Add language selector at top of sidebar
   - Translate sidebar content (~15 strings)
   - Update tab names array

2. Test: Verify language switching works and sidebar translates

### Step 3: Translate Core Create Tab
1. Extract all ~70 strings from `create_tab.py` to `translations.json`
2. Add import: `from i18n import get_text as _`
3. Replace all hardcoded text with `_()` calls
4. Test: Create QR flow works in both languages

### Step 4: Translate Shared Components
1. Extract ~30 strings from `components.py`
2. Create theme name translation dictionary
3. Update theme selector to show translated names
4. Test: Components work across all tabs

### Step 5: Translate Demo Tab
1. Extract ~45 strings from `demo_tab.py`
2. Replace with `_()` calls
3. Keep demo greeting content in English
4. Test: Demo flow in both languages

### Step 6: Translate Remaining Tabs
1. Process each tab file (scan, about, batch, examples)
2. Extract strings to translations.json
3. Replace with `_()` calls
4. Test each tab individually

### Step 7: Translate Display & Utilities
1. Update `qr/display.py` with translations
2. Update `view_page.py` with translations
3. Test QR display and mobile view

### Step 8: Complete Chinese Translations
1. Review all translation keys for consistency
2. Ensure proper terminology (technical vs. casual tone)
3. Verify Chinese character accuracy
4. Check for missing translations

### Step 9: Layout Testing
1. Test all tabs with Chinese text (wider characters)
2. Check for text overflow in buttons, labels
3. Verify sidebar fits all content
4. Test responsive breakpoints
5. Adjust column widths if needed

### Step 10: End-to-End Testing
1. Complete user flow in Chinese: create → download → scan
2. Test batch generation in Chinese
3. Verify all error messages display correctly
4. Test language switching mid-session
5. Verify QR codes work regardless of UI language

---

## Sample Translations (Key Sections)

### Sidebar
```json
{
  "app.sidebar.title": "节日问候二维码",
  "app.sidebar.tagline": "创建并分享个性化节日问候二维码！",
  "app.sidebar.greener": "*更环保、更智能的节日问候方式。*",
  "app.sidebar.quick_tips.title": "快速提示",
  "app.sidebar.quick_tips.tip1": "💡 建议消息长度在300字以内，以获得最佳二维码尺寸",
  "app.sidebar.quick_tips.tip2": "📱 使用手机相机应用测试二维码",
  "app.sidebar.quick_tips.tip3": "🎨 选择与场合相配的主题",
  "app.sidebar.support.title": "支持",
  "app.sidebar.support.text": "如果您喜欢这个工具，请考虑支持它！",
  "app.sidebar.buy_coffee": "☕ 请我喝咖啡（£1）"
}
```

### Tab Names
```json
{
  "app.tabs.demo": "🎁 试用演示",
  "app.tabs.create": "创建问候",
  "app.tabs.scan": "扫描二维码",
  "app.tabs.examples": "示例",
  "app.tabs.batch": "批量生成",
  "app.tabs.about": "关于"
}
```

### Theme Names
```json
{
  "themes.snowflake": "雪花",
  "themes.fireworks": "烟花",
  "themes.lights": "灯光",
  "themes.stars": "星星",
  "themes.confetti": "彩纸",
  "themes.champagne": "香槟",
  "themes.hearts": "爱心",
  "themes.farewell": "告别",
  "themes.burn_after_read": "阅后即焚",
  "themes.general": "通用（无图标）"
}
```

### Common Buttons
```json
{
  "common.buttons.generate": "✨ 生成二维码",
  "common.buttons.download": "📥 下载二维码",
  "common.buttons.create_another": "🔄 创建另一个问候",
  "common.buttons.scan_another": "📤 扫描另一个二维码"
}
```

### Create Tab Steps
```json
{
  "create_tab.step1.title": "### 步骤 1：选择主题和背景",
  "create_tab.step1.tip": "💡 **提示：** 选择与场合相配的主题。颜色会自动适配！",
  "create_tab.step2.title": "### 步骤 2：预览和个性化",
  "create_tab.step2.tip": "💡 **提示：** 这是您的问候的显示效果。您可以在下方编辑详细信息！",
  "create_tab.step3.title": "### 步骤 3：创建魔法",
  "create_tab.step3.tip": "💡 **提示：** 准备好了吗？点击下方生成您的专属问候二维码！"
}
```

---

## Testing Checklist

### Translation Completeness
- [ ] All 11 Python files updated with `from i18n import get_text as _`
- [ ] No hardcoded English text visible in UI (except examples)
- [ ] All ~250+ strings present in translations.json
- [ ] All translations have both `en` and `zh` values
- [ ] No missing translation keys (fallback to English works)

### Functionality Testing (Chinese UI)
- [ ] Language selector switches immediately
- [ ] Create greeting flow: select theme → preview → generate → download
- [ ] Scan QR code: upload → decode → display message
- [ ] Demo tab: full interactive demo works
- [ ] Batch generation: upload CSV → generate all → download ZIP
- [ ] About tab: all information displayed correctly
- [ ] Examples tab: all examples shown

### Layout Testing (Chinese Text)
- [ ] Sidebar: all content fits without horizontal scrolling
- [ ] Tab names: fit in tab bar without wrapping
- [ ] Buttons: text doesn't overflow
- [ ] Cards/containers: accommodate wider Chinese text
- [ ] Help tooltips: display correctly
- [ ] Multi-column layouts: maintain balance
- [ ] Mobile view: responsive design works

### Edge Cases
- [ ] Switch language mid-session → all tabs update
- [ ] Create QR in Chinese UI → QR data intact
- [ ] Error messages display in correct language
- [ ] Missing translation → falls back to English gracefully
- [ ] Special characters in messages → handled correctly
- [ ] Long messages → QR code generation warning in Chinese

---

## Risk Mitigation

### Layout Issues
- **Risk**: Chinese text 20-40% wider may break layouts
- **Mitigation**: Use flexible containers, test all responsive breakpoints, adjust column ratios if needed

### Character Encoding
- **Risk**: UTF-8 encoding issues with Chinese characters
- **Mitigation**: Ensure all files saved as UTF-8, add encoding declarations

### Missing Translations
- **Risk**: Forgetting to translate some strings
- **Mitigation**: Systematic file-by-file approach, automated completeness check

### Performance
- **Risk**: Loading translations adds overhead
- **Mitigation**: Cache in session state, JSON load is ~1ms (negligible)

---

## Future Enhancements (Out of Scope)

- Additional languages (Traditional Chinese, Spanish, French, Japanese)
- Browser language auto-detection
- Persistent language preference (cookies/URL parameter)
- Translation management UI
- Translate example greeting messages
- RTL language support

---

## Success Criteria

✅ Complete Chinese translation of all UI elements (~250+ strings)
✅ Language selector in sidebar working smoothly
✅ All core functionality (create, scan, batch) works in both languages
✅ No layout breaking with Chinese text
✅ No English text visible in UI when Chinese selected (except examples/user content)
✅ Fallback to English for missing translations
✅ Clean, maintainable code with clear translation key structure
