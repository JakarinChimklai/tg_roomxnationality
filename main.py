# o.py

import streamlit as st
from config import BEACH_COLORS, beach_colors
from tab_1 import tab1_page
from tab_2 import tab2_page
from tab_3 import tab3_page
from tab_4 import tab4_page

# ----------------------- Page Configuration ----------------------- #
st.set_page_config(
    page_title="The Grass Serviced Suites",
    page_icon="🏝️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ----------------------- Load Custom CSS ----------------------- #
def load_custom_css(css_file):
    with open(css_file, "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_custom_css("style.css")

# ----------------------- Header ----------------------- #
st.markdown("""
<div class="main-header">
    <div>
        <h1>🏝️ The Grass Serviced Suites</h1>
        <h2>Room Map & Nationality Management</h2>
    </div>
    <div style="font-size: 2.8rem;">🏨 🌴 🌊</div>
</div>
""", unsafe_allow_html=True)

# ----------------------- Tabs ----------------------- #
st.write("")
tab1, tab2, tab3, tab4 = st.tabs(["📢 Announcement", "📊 Summary", "🏢 Floor View", "🔄 Room Movement"])

with tab1:
    tab1_page(BEACH_COLORS)

with tab2:
    tab2_page(BEACH_COLORS, beach_colors)

with tab3:
    tab3_page(beach_colors)

with tab4:
    tab4_page()
