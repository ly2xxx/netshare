#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Holiday Greeting QR Code Generator
A Streamlit app for creating and reading holiday greeting QR codes
"""

import sys
import os

# Ensure the app's directory is in the Python path for local module imports
# This is required for Streamlit Cloud where the working directory may differ
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import streamlit.components.v1 as components

# Import configuration
from config import THEME_ICONS, PAGE_CONFIG, CSS_STYLES

# Import tab modules
from tabs import create_tab, scan_tab, examples_tab, batch_tab, about_tab, view_page, demo_tab, funnel_tab

# Import internationalization
from i18n import init_language, get_text as _, get_language_selector

# Import and start keepalive daemon for dependent services
from keepalive_daemon import start_keepalive_daemon
start_keepalive_daemon()

# Set page configuration
st.set_page_config(**PAGE_CONFIG)

# Initialize language support
init_language()

# Apply custom CSS
st.markdown(CSS_STYLES, unsafe_allow_html=True)

# Check if this is a view request (from QR code scan) - handle before main app
try:
    query_params = st.query_params
    tab_param = query_params.get('tab', 'create')
    # Read _tab param set by JavaScript tab click tracking
    tracked_tab = query_params.get('_tab')
except:
    # Fallback for older Streamlit versions
    query_params = st.experimental_get_query_params()
    tab_param = query_params.get('tab', ['create'])[0]
    tracked_tab = query_params.get('_tab', [None])[0]

# Show mobile-friendly greeting view if tab=view
if tab_param == "view":
    view_page.render()
    st.stop()


def main():
    """Main application"""

    # Sidebar
    with st.sidebar:
        # Language selector at the top
        get_language_selector()

        st.markdown("---")

        st.title(_("app.sidebar.title"))
        st.write(_("app.sidebar.tagline"))
        st.markdown(_("app.sidebar.greener"))

        st.markdown("---")

        st.write(_("app.sidebar.quick_tips.title"))
        st.info(f"""
        {_("app.sidebar.quick_tips.tip1")}

        {_("app.sidebar.quick_tips.tip2")}

        {_("app.sidebar.quick_tips.tip3")}
        """)

        st.markdown("---")

        st.write(_("app.sidebar.support.title"))
        st.write(_("app.sidebar.support.text"))
        st.link_button(_("common.buttons.buy_coffee"), "https://www.paypal.com/ncp/payment/NUQG396UTFRMG")

        st.markdown("---")

        # Marketing Funnel tab toggle
        # Enabled by default, ensures visibility
        default_show_funnel = True
        show_funnel = st.checkbox(
            "📈 Marketing Funnel",
            value=default_show_funnel,
            help="Create QR codes for marketing campaigns"
        )
        
        # Batch tab toggle
        # Auto-enable if URL has tab=batch parameter or _tab=batch
        default_show_batch = tab_param == "batch" or tracked_tab == "batch"
        show_batch = st.checkbox(
            _("app.sidebar.batch_checkbox"),
            value=default_show_batch,
            help=_("app.sidebar.batch_help")
        )

    # Define tab keys in order
    # Demo tab is first for visibility to new users
    tab_keys = ["demo", "create", "scan", "examples"]
    if show_funnel:
        tab_keys.append("funnel")
    if show_batch:
        tab_keys.append("batch")
    tab_keys.append("about")
    
    # Determine current tab index
    # Priority: 1. tracked_tab (from URL _tab), 2. tab_param (explicit in URL), 3. session state, 4. Default (0)
    tab_index = 0
    
    # Handle tracked_tab (from URL _tab)
    if tracked_tab:
        if tracked_tab in tab_keys:
            tab_index = tab_keys.index(tracked_tab)
        else:
            # Fallback for legacy integer indices or invalid values
            try:
                idx = int(tracked_tab)
                if 0 <= idx < len(tab_keys):
                    tab_index = idx
            except (ValueError, TypeError):
                pass
    # Handle explicit tab param (higher priority than session for deep linking support)
    elif "tab" in query_params and tab_param in tab_keys:
        tab_index = tab_keys.index(tab_param)
    # Handle session state (only if no URL tracking override, but URL tracking is usually superior for bookmarking)
    elif "current_tab_index" in st.session_state:
        tab_index = st.session_state.current_tab_index
    # Handle default tab param (if not explicit in URL)
    elif tab_param in tab_keys:
        tab_index = tab_keys.index(tab_param)
        
    # Update session state
    st.session_state.current_tab_index = tab_index

    # Inject JavaScript to:
    # 1. Click the correct tab if not the first tab
    # 2. Track tab clicks and store in session state via hidden query param using tab name
    import json
    tab_keys_json = json.dumps(tab_keys)
    
    components.html(f"""
        <script>
        (function() {{
            let attempts = 0;
            const maxAttempts = 10;
            const targetTabIndex = {tab_index};
            const tabKeys = {tab_keys_json};

            function clickTab() {{
                const tabs = window.parent.document.querySelectorAll('button[data-baseweb="tab"]');

                if (tabs && tabs.length > targetTabIndex) {{
                    // Click the target tab if not already on it (index 0)
                    if (targetTabIndex > 0) {{
                        tabs[targetTabIndex].click();
                    }}
                    
                    // Update tab keys on all tabs and add listeners
                    tabs.forEach((tab, index) => {{
                        // Always update the data-tab-key to match present state
                        // This fixes issues where DOM elements are reused but tab mapped changed
                        const tabKey = tabKeys[index] || index.toString();
                        tab.setAttribute('data-tab-key', tabKey);
                        
                        // Only add listener once
                        if (!tab.hasAttribute('data-tab-tracked')) {{
                            tab.setAttribute('data-tab-tracked', 'true');
                            tab.addEventListener('click', (e) => {{
                                // Read the latest key from the attribute
                                // This decoupling ensures we don't rely on stale closures
                                const currentTabKey = e.currentTarget.getAttribute('data-tab-key');
                                
                                // Store tab name in URL param for next rerun
                                const url = new URL(window.parent.location.href);
                                url.searchParams.set('_tab', currentTabKey);
                                // Use history.replaceState to avoid page reload
                                window.parent.history.replaceState({{}}, '', url.toString());
                            }});
                        }}
                    }});
                    return true;
                }} else if (attempts < maxAttempts) {{
                    attempts++;
                    setTimeout(clickTab, 100);
                }}
            }}

            clickTab();
        }})();
        </script>
    """, height=0)

    # Main tabs (conditionally include batch and/or funnel tabs)
    # Demo tab is first for visibility to new users
    # Build tab names dynamically
    tab_names = [
        _("app.tabs.demo"),
        _("app.tabs.create"),
        _("app.tabs.scan"),
        _("app.tabs.examples")
    ]
    if show_funnel:
        tab_names.append("📈 Marketing Funnel")
    if show_batch:
        tab_names.append(_("app.tabs.batch"))
    tab_names.append(_("app.tabs.about"))
    
    # Create tabs
    tabs = st.tabs(tab_names)
    
    # Render tabs
    tab_idx = 0
    
    with tabs[tab_idx]:  # Demo
        demo_tab.render()
    tab_idx += 1
    
    with tabs[tab_idx]:  # Create
        create_tab.render()
    tab_idx += 1
    
    with tabs[tab_idx]:  # Scan
        scan_tab.render()
    tab_idx += 1
    
    with tabs[tab_idx]:  # Examples
        examples_tab.render()
    tab_idx += 1
    
    if show_funnel:
        with tabs[tab_idx]:  # Funnel
            funnel_tab.render()
        tab_idx += 1
    
    if show_batch:
        with tabs[tab_idx]:  # Batch
            batch_tab.render()
        tab_idx += 1
    
    with tabs[tab_idx]:  # About
        about_tab.render()


if __name__ == "__main__":
    main()
