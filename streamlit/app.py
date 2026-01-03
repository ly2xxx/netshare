#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Holiday Greeting QR Code Generator
A Streamlit app for creating and reading holiday greeting QR codes
"""

import streamlit as st
import streamlit.components.v1 as components

# Import configuration
from config import THEME_ICONS, PAGE_CONFIG, CSS_STYLES

# Import tab modules
from tabs import create_tab, scan_tab, examples_tab, batch_tab, about_tab, view_page, demo_tab

# Import internationalization
from i18n import init_language, get_text as _, get_language_selector

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
except:
    # Fallback for older Streamlit versions
    query_params = st.experimental_get_query_params()
    tab_param = query_params.get('tab', ['create'])[0]

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
    tab_index = tab_map.get(tab_param, 0)

    # Inject JavaScript to click the correct tab (only if not the first tab)
    if tab_index > 0:
        components.html(f"""
            <script>
            (function() {{
                let attempts = 0;
                const maxAttempts = 10;

                function clickTab() {{
                    const tabs = window.parent.document.querySelectorAll('button[data-baseweb="tab"]');

                    if (tabs && tabs.length > {tab_index}) {{
                        tabs[{tab_index}].click();
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
