"""
About Tab
Information about the application and its features
"""


import streamlit as st
from utils.download_tracker import get_download_count
from i18n import get_text as _


def render() -> None:
    """About the application"""
    st.markdown(f'<div class="main-header"><h1>{_("about_tab.header")}</h1></div>',
                unsafe_allow_html=True)

    st.write(_("about_tab.title"))
    st.write(_("about_tab.description"))

    st.markdown("---")
    # Video player in centered column
    col1, col2, col3 = st.columns([0.5, 2, 0.5], gap="medium")
    with col2:
        st.video("https://www.youtube.com/watch?v=6SuLXoRmykE")

    st.markdown("<div style='margin-bottom: 1.5rem;'></div>", unsafe_allow_html=True)

    # Video section with styled heading
    st.markdown(f"""
<div style="text-align: center; margin: 2rem 0 1rem 0;">
    <h3 style="color: #333; margin-bottom: 0.5rem;">{_('about_tab.video_section')}</h3>
    <p style="color: #666; margin-bottom: 1.5rem; font-size: 1rem;">
        {_('about_tab.video_description')}
    </p>
</div>
""", unsafe_allow_html=True)

    # Video player in centered column
    col1, col2, col3 = st.columns([0.5, 2, 0.5], gap="medium")
    with col2:
        st.video("https://www.youtube.com/watch?v=hJdGamlet5A")

    st.markdown("<div style='margin-bottom: 1.5rem;'></div>", unsafe_allow_html=True)

    # Core positioning messages
    st.markdown("---")
    st.subheader(_("about_tab.why_choose"))

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        {_('about_tab.environment.title')}

        {_('about_tab.environment.heading')}

        {_('about_tab.environment.description')}
        """)

    with col2:
        st.markdown(f"""
        {_('about_tab.secret.title')}

        {_('about_tab.secret.heading')}

        {_('about_tab.secret.description')}

        {_('about_tab.secret.benefit1')}
        {_('about_tab.secret.benefit2')}
        {_('about_tab.secret.benefit3')}
        {_('about_tab.secret.benefit4')}

        {_('about_tab.secret.tagline')}
        """)

    with col3:
        st.markdown(f"""
        {_('about_tab.device.title')}

        {_('about_tab.device.heading')}

        {_('about_tab.device.description')}
        """)

    st.markdown("---")

    # Business Value Proposition - Attention Economy
    st.subheader(_("about_tab.business.title"))

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown(f"""
        {_('about_tab.business.challenge')}

        {_('about_tab.business.solution_intro')}

        {_('about_tab.business.step1')}
        {_('about_tab.business.step2')}
        {_('about_tab.business.step3')}

        {_('about_tab.business.use_cases_title')}
        {_('about_tab.business.use_cases_list')}
        """)

    with col2:
        st.markdown(f"""
        {_('about_tab.business.stats_title')}

        {_('about_tab.business.stats_list')}
        """)

    st.markdown("---")

    st.write(f"""
    {_('about_tab.features.title')}
    {_('about_tab.features.custom')}
    {_('about_tab.features.scan')}
    {_('about_tab.features.themes')}
    {_('about_tab.features.download')}
    {_('about_tab.features.json')}

    {_('about_tab.how_it_works.title')}
    {_('about_tab.how_it_works.step1')}
    {_('about_tab.how_it_works.step2')}
    {_('about_tab.how_it_works.step3')}
    {_('about_tab.how_it_works.step4')}

    {_('about_tab.how_it_works.recipients')}

    {_('about_tab.technical.title')}
    {_('about_tab.technical.error_correction')}
    {_('about_tab.technical.json_format')}
    {_('about_tab.technical.message_length')}
    {_('about_tab.technical.built_with')}
    """)

    st.markdown("---")

    st.markdown(f"""
    {_('about_tab.privacy.title')}

    {_('about_tab.privacy.heading')}

    {_('about_tab.privacy.description')}

    {_('about_tab.privacy.no_ai')}
    {_('about_tab.privacy.no_training')}
    {_('about_tab.privacy.no_analysis')}
    {_('about_tab.privacy.no_cloud')}

    {_('about_tab.privacy.tagline')}
    """)

    st.write(f"""
    {_('about_tab.powered_by.title')}
    {_('about_tab.powered_by.netshare')}
    {_('about_tab.powered_by.streamlit')}
    {_('about_tab.powered_by.qrcode')}
    {_('about_tab.powered_by.pillow')}
    """)

    # Display download count (just the number)
    count = get_download_count()
    st.write(count)
