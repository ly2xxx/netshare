#!/usr/bin/env python3
"""
Holiday Greeting QR Code Generator
A Streamlit app for creating and reading holiday greeting QR codes
"""

import streamlit as st
import streamlit.components.v1 as components

# Import configuration
from config import THEME_ICONS, PAGE_CONFIG, CSS_STYLES

# Import tab modules
from tabs import create_tab, scan_tab, examples_tab, batch_tab, about_tab, view_page

# Set page configuration
st.set_page_config(**PAGE_CONFIG)

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
        st.title("Holiday Greeting QR")
        st.write("Create and share personalized holiday greetings via QR codes!")
        st.markdown("*A greener, smarter way to say happy holidays.*")

        st.markdown("---")

        st.write("### Quick Tips")
        st.info("""
        💡 Keep messages under 300 characters for best QR code size

        📱 Test QR codes with your phone camera app

        🎨 Choose themes that match your occasion
        """)

        st.markdown("---")

        # Batch tab toggle
        show_batch = st.checkbox("Show Batch Tab", value=False, help="Enable batch QR code generation from Excel")

    # Map tab names to indices (depends on whether batch tab is shown)
    if show_batch:
        tab_map = {"create": 0, "scan": 1, "examples": 2, "batch": 3, "about": 4}
    else:
        tab_map = {"create": 0, "scan": 1, "examples": 2, "about": 3}
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
    if show_batch:
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["Create Greeting", "Scan QR Code", "Examples", "Batch", "About"])

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
        tab1, tab2, tab3, tab4 = st.tabs(["Create Greeting", "Scan QR Code", "Examples", "About"])

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
