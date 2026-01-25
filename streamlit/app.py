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
from tabs import create_tab, scan_tab, examples_tab, batch_tab, about_tab, view_page, demo_tab

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

# Update session state with tracked tab index if available
if tracked_tab is not None:
    try:
        st.session_state.current_tab_index = int(tracked_tab)
    except (ValueError, TypeError):
        pass

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

        # Batch tab toggle
        show_batch = st.checkbox(
            _("app.sidebar.batch_checkbox"),
            value=False,
            help=_("app.sidebar.batch_help")
        )

    # Map tab names to indices (depends on whether batch tab is shown)
    # Demo tab is first for visibility to new users
    if show_batch:
        tab_map = {"demo": 0, "create": 1, "scan": 2, "examples": 3, "batch": 4, "about": 5}
    else:
        tab_map = {"demo": 0, "create": 1, "scan": 2, "examples": 3, "about": 4}
    
    # Use session state tab index if available (preserves tab across locale switch)
    # Otherwise fall back to URL param or default to Demo (0)
    if "current_tab_index" in st.session_state:
        tab_index = st.session_state.current_tab_index
    else:
        tab_index = tab_map.get(tab_param, 0)
        st.session_state.current_tab_index = tab_index

    # Inject JavaScript to:
    # 1. Click the correct tab if not the first tab
    # 2. Track tab clicks and store in session state via hidden query param
    components.html(f"""
        <script>
        (function() {{
            let attempts = 0;
            const maxAttempts = 10;
            const targetTabIndex = {tab_index};

            function clickTab() {{
                const tabs = window.parent.document.querySelectorAll('button[data-baseweb="tab"]');

                if (tabs && tabs.length > targetTabIndex) {{
                    // Click the target tab if not already on it (index 0)
                    if (targetTabIndex > 0) {{
                        tabs[targetTabIndex].click();
                    }}
                    
                    // Add click listeners to all tabs to track selection
                    tabs.forEach((tab, index) => {{
                        if (!tab.hasAttribute('data-tab-tracked')) {{
                            tab.setAttribute('data-tab-tracked', 'true');
                            tab.addEventListener('click', () => {{
                                // Store tab index in URL param for next rerun
                                const url = new URL(window.parent.location.href);
                                url.searchParams.set('_tab', index.toString());
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

    # Main tabs (conditionally include batch tab)
    # Demo tab is first for visibility to new users
    if show_batch:
        tab0, tab1, tab2, tab3, tab4, tab5 = st.tabs([
            _("app.tabs.demo"),
            _("app.tabs.create"),
            _("app.tabs.scan"),
            _("app.tabs.examples"),
            _("app.tabs.batch"),
            _("app.tabs.about")
        ])

        with tab0:
            demo_tab.render()

        with tab1:
            create_tab.render()

        with tab2:
            scan_tab.render()

        with tab3:
            examples_tab.render()

        with tab4:
            batch_tab.render()

        with tab5:
            about_tab.render()
    else:
        tab0, tab1, tab2, tab3, tab4 = st.tabs([
            _("app.tabs.demo"),
            _("app.tabs.create"),
            _("app.tabs.scan"),
            _("app.tabs.examples"),
            _("app.tabs.about")
        ])

        with tab0:
            demo_tab.render()

        with tab1:
            create_tab.render()

        with tab2:
            scan_tab.render()

        with tab3:
            examples_tab.render()

        with tab4:
            about_tab.render()


if __name__ == "__main__":
    main()
