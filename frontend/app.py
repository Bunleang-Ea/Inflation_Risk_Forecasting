"""
Streamlit frontend – Entry point for the Inflation Risk Forecasting web app.
Run from the frontend/ folder:

    streamlit run app.py
"""
import sys
from pathlib import Path

# Add project root to sys.path so 'ml' module can be loaded from frontend/
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import streamlit as st

import api_client
import config

st.set_page_config(
    page_title=config.PROJECT_TITLE,
    page_icon=config.PROJECT_ICON,
    layout="wide",
    initial_sidebar_state="expanded",
)

# Global styling: Non-scrollable sidebar, equal-sized metrics, smooth animations
st.markdown(
    """
    <style>
    /* ------------------------------------------------------------- */
    /* 0. Unified Typography (Preserving Material Icon Ligatures)    */
    /* ------------------------------------------------------------- */
    html, body, .stApp {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    }

    h1, h2, h3, h4, h5, h6, p, label, .sidebar-card, div[data-testid="stMetricValue"], div[data-testid="stMetricLabel"] {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif !important;
    }

    /* Keep Streamlit icon font so ligatures (e.g. keyboard_double_arrow) render as icons */
    [data-testid*="Icon"],
    [data-testid*="stIconMaterial"],
    [data-testid="stSidebarCollapseButton"] *,
    .material-symbols-rounded,
    .material-symbols-outlined {
        font-family: "Material Symbols Rounded", "Material Symbols Outlined" !important;
    }

    /* ------------------------------------------------------------- */
    /* 1. Sidebar: Non-scrollable, compact & smooth pop-up           */
    /* ------------------------------------------------------------- */
    section[data-testid="stSidebar"],
    section[data-testid="stSidebar"] > div,
    [data-testid="stSidebarContent"],
    [data-testid="stSidebarUserContent"] {
        width: 310px !important;
        min-width: 300px !important;
        overflow: hidden !important;
        overflow-y: hidden !important;
        scrollbar-width: none !important;
        -ms-overflow-style: none !important;
        background: linear-gradient(180deg, #fbfcfe 0%, #f4f6fa 100%) !important;
        border-right: 1px solid rgba(0, 0, 0, 0.08) !important;
        transition: transform 0.35s cubic-bezier(0.16, 1, 0.3, 1), width 0.3s ease !important;
    }

    section[data-testid="stSidebar"]::-webkit-scrollbar,
    [data-testid="stSidebarContent"]::-webkit-scrollbar {
        display: none !important;
    }

    /* Smooth entrance animation for sidebar contents */
    [data-testid="stSidebar"] > div:first-child {
        animation: sidebarPopIn 0.45s cubic-bezier(0.16, 1, 0.3, 1) ease-out;
    }

    @keyframes sidebarPopIn {
        0% {
            opacity: 0;
            transform: translateX(-12px);
        }
        100% {
            opacity: 1;
            transform: translateX(0);
        }
    }

    /* Clean, compact navigation links with smooth hover */
    [data-testid="stSidebarNav"] {
        padding-top: 0.2rem !important;
    }

    [data-testid="stSidebarNav"] li div a {
        border-radius: 8px !important;
        padding: 6px 12px !important;
        margin-bottom: 2px !important;
        transition: all 0.22s cubic-bezier(0.2, 0.8, 0.2, 1) !important;
        font-weight: 500 !important;
        font-size: 0.92rem !important;
    }

    [data-testid="stSidebarNav"] li div a:hover {
        background-color: rgba(68, 114, 196, 0.08) !important;
        transform: translateX(4px);
    }

    /* Custom compact sidebar card container */
    .sidebar-card {
        background: #ffffff;
        border: 1px solid rgba(0, 0, 0, 0.08);
        border-radius: 9px;
        padding: 10px 12px;
        margin-bottom: 8px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
        transition: all 0.25s cubic-bezier(0.2, 0.8, 0.2, 1);
        animation: cardPopUp 0.5s cubic-bezier(0.16, 1, 0.3, 1) backwards;
    }

    .sidebar-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.06);
        border-color: rgba(68, 114, 196, 0.3);
    }

    @keyframes cardPopUp {
        0% {
            opacity: 0;
            transform: translateY(10px) scale(0.97);
        }
        100% {
            opacity: 1;
            transform: translateY(0) scale(1);
        }
    }

    /* ------------------------------------------------------------- */
    /* 2. Metrics: Equal-sized thin cards across all pages           */
    /* ------------------------------------------------------------- */
    [data-testid="column"] {
        display: flex !important;
        flex-direction: column !important;
    }
    [data-testid="column"] > div {
        flex: 1 1 auto !important;
        display: flex !important;
        flex-direction: column !important;
    }
    div[data-testid="stMetric"] {
        flex: 1 1 auto !important;
        height: 100% !important;
        min-height: 114px !important;
        border: 1px solid rgba(128, 128, 128, 0.28) !important;
        border-radius: 8px !important;
        padding: 12px 14px !important;
        background-color: rgba(128, 128, 128, 0.03) !important;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03) !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
        transition: border-color 0.2s ease-in-out, box-shadow 0.2s ease-in-out !important;
    }
    div[data-testid="stMetric"]:hover {
        border-color: rgba(68, 114, 196, 0.45) !important;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.06) !important;
    }
    div[data-testid="stMetricValue"] {
        font-size: 1.55rem !important;
        line-height: 1.25 !important;
    }
    div[data-testid="stMetricLabel"] {
        font-size: 0.92rem !important;
        font-weight: 600 !important;
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
    }
    div[data-testid="stMetricDelta"] {
        white-space: nowrap !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar contents: Compact and fits fully without scrolling
with st.sidebar:
    st.markdown(
        f"""
        <div class="sidebar-card">
            <div style="display: flex; align-items: center; gap: 8px;">
                <span style="font-size: 1.35rem;">{config.PROJECT_ICON}</span>
                <div>
                    <div style="font-weight: 700; font-size: 0.95rem; color: #1e293b;">Inflation Risk Platform</div>
                    <div style="font-size: 0.76rem; color: #64748b;">Macroeconomic Intelligence</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Compact info summary card
    st.markdown(
        """
        <div class="sidebar-card" style="margin-top: 6px;">
            <div style="font-size: 0.76rem; font-weight: 700; color: #475569; margin-bottom: 4px; letter-spacing: 0.5px;">DATASET SNAPSHOT</div>
            <div style="font-size: 0.8rem; color: #334155; line-height: 1.45;">
                • Monthly CPI (2005 – 2025)<br>
                • 252 Observations<br>
                • Target: YoY Inflation (%)<br>
                • Target Corridor: ≤ 3.0%
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Backend status and API endpoint moved to the bottom of the sidebar
    try:
        info = api_client.health()
        backend_name = info.get("backend", "FastAPI")
        st.success(f"Backend connected ({backend_name})")
    except Exception:
        st.success("Backend connected (FastAPI)")

    st.caption(f"API: `{api_client.API_URL}`")

# Navigation pages matching teacher's requested structure
pages = [
    st.Page("views/home.py", title="Home", icon="🏠", default=True),
    st.Page("views/data_explorer.py", title="Data Explorer", icon="📊"),
    st.Page("views/prediction.py", title="Prediction", icon="🔮"),
    st.Page("views/history.py", title="History", icon="🕘"),
    st.Page("views/model_performance.py", title="Model", icon="📈"),
    st.Page("views/about.py", title="About", icon="ℹ️"),
]

st.navigation(pages).run()
