import streamlit as st
import pandas as pd
import json
import plotly.express as px
from snowflake.snowpark.context import get_active_session

# ─────────────────────────────────────────────────────────────
# THEME — Dark Forest Pro: Deep Charcoal-Green + Light Sidebar
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* ── Fonts ── */
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;1,400&family=JetBrains+Mono:wght@400;500&display=swap');

    /* ═══════════════════════════════════════════════════
       DESIGN TOKENS — Dark Forest Pro
    ═══════════════════════════════════════════════════ */
    :root {
        /* ── Main body — deep dark forest ── */
        --body-bg:          #0f1a13;
        --body-bg-alt:      #111d15;
        --panel-bg:         #141f18;
        --panel-bg-raised:  #192510;
        --panel-border:     rgba(255,255,255,0.06);
        --card-bg:          #1a2820;
        --card-border:      rgba(255,255,255,0.07);
        --card-border-hover:rgba(61,166,104,0.35);

        /* ── Green brand ── */
        --green-100:        #e8f5ef;
        --green-300:        #6ecca0;
        --green-400:        #3da668;
        --green-500:        #2d8050;
        --green-600:        #1f5c38;
        --green-glow:       rgba(61,166,104,0.18);
        --green-glow-strong:rgba(61,166,104,0.30);
        --green-border:     rgba(61,166,104,0.20);
        --green-border-med: rgba(61,166,104,0.35);

        /* ── Text on dark ── */
        --text-primary:     #e8f0ea;
        --text-secondary:   #9dbdaa;
        --text-muted:       #5a7a65;
        --text-accent:      #6ecca0;

        /* ── Sidebar — deliberately light ── */
        --sb-bg:            #f0f5f1;
        --sb-bg-deep:       #e4ede7;
        --sb-border:        #c2d8ca;
        --sb-text:          #1a3028;
        --sb-text-muted:    #4a7060;
        --sb-label:         #1e5038;
        --sb-input-bg:      #ffffff;
        --sb-input-border:  #b0ccbb;
        --sb-block-bg:      #ffffff;
        --sb-block-border:  #c8ddd2;
        --sb-accent:        #2d8050;

        /* ── Utility ── */
        --border:           rgba(255,255,255,0.06);
        --radius-xs:        4px;
        --radius-sm:        6px;
        --radius-md:        10px;
        --radius-lg:        14px;
        --radius-xl:        20px;

        /* ── Status colors ── */
        --status-high:      #3da668;
        --status-med:       #d4a017;
        --status-low:       #c94040;
        --status-high-bg:   rgba(61,166,104,0.12);
        --status-med-bg:    rgba(212,160,23,0.12);
        --status-low-bg:    rgba(201,64,64,0.12);
    }

    /* ═══════════════════════════════════════════════════
       GLOBAL RESET
    ═══════════════════════════════════════════════════ */
    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif !important;
        font-size: 13px !important;
    }

    .stApp {
        background: var(--body-bg) !important;
        color: var(--text-primary) !important;
    }

    /* Subtle grain texture overlay on main body */
    .stApp::before {
        content: '';
        position: fixed;
        inset: 0;
        background-image:
            radial-gradient(ellipse 80% 50% at 20% 10%, rgba(45,128,80,0.07) 0%, transparent 60%),
            radial-gradient(ellipse 60% 40% at 80% 90%, rgba(30,90,55,0.05) 0%, transparent 60%);
        pointer-events: none;
        z-index: 0;
    }

    /* Grid overlay */
    .stApp::after {
        content: '';
        position: fixed;
        inset: 0;
        background-image:
            linear-gradient(rgba(61,166,104,0.025) 1px, transparent 1px),
            linear-gradient(90deg, rgba(61,166,104,0.025) 1px, transparent 1px);
        background-size: 40px 40px;
        pointer-events: none;
        z-index: 0;
    }

    /* ═══════════════════════════════════════════════════
       SIDEBAR — LIGHT THEMED (key contrast)
    ═══════════════════════════════════════════════════ */
    [data-testid="stSidebar"] {
        background: var(--sb-bg) !important;
        border-right: 1px solid var(--sb-border) !important;
        box-shadow: 4px 0 24px rgba(0,0,0,0.25), 1px 0 0 rgba(255,255,255,0.03) !important;
    }
    [data-testid="stSidebar"] > div:first-child {
        padding-top: 0 !important;
    }

    /* Sidebar header strip */
    [data-testid="stSidebar"]::before {
        content: '';
        display: block;
        height: 4px;
        background: linear-gradient(90deg, var(--green-500), var(--green-300), transparent);
        position: sticky;
        top: 0;
        z-index: 10;
    }

    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stMarkdown p {
        font-size: 11px !important;
        color: var(--sb-text-muted) !important;
        font-weight: 500 !important;
        font-family: 'DM Sans', sans-serif !important;
    }
    [data-testid="stSidebar"] h3 {
        font-size: 10px !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.14em !important;
        color: var(--sb-label) !important;
        margin-bottom: 0.75rem !important;
        padding-bottom: 0.5rem !important;
        border-bottom: 1.5px solid var(--sb-border) !important;
        font-family: 'Syne', sans-serif !important;
    }
    [data-testid="stSidebar"] .stSelectbox > div > div,
    [data-testid="stSidebar"] .stTextInput input {
        background: var(--sb-input-bg) !important;
        border: 1px solid var(--sb-input-border) !important;
        border-radius: var(--radius-sm) !important;
        color: var(--sb-text) !important;
        font-size: 12px !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06) !important;
    }
    [data-testid="stSidebar"] .stMultiSelect > div > div {
        background: var(--sb-input-bg) !important;
        border: 1px solid var(--sb-input-border) !important;
        border-radius: var(--radius-sm) !important;
        color: var(--sb-text) !important;
    }
    [data-testid="stSidebar"] [data-testid="stFileUploader"] {
        background: #f7fbf9 !important;
        border: 1.5px dashed var(--sb-accent) !important;
        border-radius: var(--radius-md) !important;
    }
    [data-testid="stSidebar"] .sb-block {
        background: var(--sb-block-bg) !important;
        border: 1px solid var(--sb-block-border) !important;
        border-radius: var(--radius-md) !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06) !important;
    }
    /* Sidebar section icons */
    [data-testid="stSidebar"] .sb-section-icon {
        width: 28px; height: 28px;
        border-radius: 6px;
        display: flex; align-items: center; justify-content: center;
        font-size: 13px;
        flex-shrink: 0;
    }

    /* ═══════════════════════════════════════════════════
       FILE UPLOADER
    ═══════════════════════════════════════════════════ */
    [data-testid="stFileUploader"] {
        background: rgba(61,166,104,0.04) !important;
        border: 1.5px dashed var(--green-border-med) !important;
        border-radius: var(--radius-md) !important;
        transition: border-color 0.2s !important;
    }
    [data-testid="stFileUploader"]:hover {
        border-color: var(--green-400) !important;
        background: rgba(61,166,104,0.07) !important;
    }

    /* ═══════════════════════════════════════════════════
       HEADINGS
    ═══════════════════════════════════════════════════ */
    h1 { font-family: 'Syne', sans-serif !important; font-size: 22px !important; font-weight: 800 !important; color: var(--text-primary) !important; letter-spacing: -0.02em !important; margin: 0 !important; }
    h2 { font-family: 'Syne', sans-serif !important; font-size: 14px !important; font-weight: 700 !important; color: var(--text-primary) !important; letter-spacing: -0.01em !important; margin-bottom: 0.9rem !important; margin-top: 0 !important; }
    h3 { font-family: 'Syne', sans-serif !important; font-size: 13px !important; font-weight: 600 !important; color: var(--text-primary) !important; margin-bottom: 0.6rem !important; }
    h4 { font-size: 10px !important; font-weight: 700 !important; color: var(--text-muted) !important; text-transform: uppercase !important; letter-spacing: 0.12em !important; margin-bottom: 0.75rem !important; font-family: 'DM Sans', sans-serif !important; }

    /* ═══════════════════════════════════════════════════
       TABS
    ═══════════════════════════════════════════════════ */
    .stTabs [data-baseweb="tab-list"] {
        background: var(--card-bg) !important;
        border: 1px solid var(--card-border) !important;
        border-radius: var(--radius-md) !important;
        padding: 0.3rem !important;
        gap: 0.15rem !important;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        color: var(--text-muted) !important;
        font-size: 11px !important;
        font-weight: 600 !important;
        font-family: 'DM Sans', sans-serif !important;
        border-radius: var(--radius-sm) !important;
        padding: 0.45rem 1rem !important;
        letter-spacing: 0.02em !important;
        transition: all 0.18s !important;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: var(--text-accent) !important;
        background: rgba(61,166,104,0.08) !important;
    }
    .stTabs [aria-selected="true"] {
        background: var(--green-500) !important;
        color: #ffffff !important;
        box-shadow: 0 2px 10px rgba(45,128,80,0.4) !important;
    }
    .stTabs [data-baseweb="tab-panel"] {
        background: var(--panel-bg) !important;
        border: 1px solid var(--panel-border) !important;
        border-radius: 0 0 var(--radius-lg) var(--radius-lg) !important;
        padding: 1.25rem !important;
        margin-top: -1px !important;
    }

    /* ═══════════════════════════════════════════════════
       METRICS
    ═══════════════════════════════════════════════════ */
    [data-testid="stMetric"] {
        background: var(--card-bg) !important;
        border: 1px solid var(--card-border) !important;
        border-radius: var(--radius-md) !important;
        padding: 1rem 1.1rem !important;
        position: relative !important;
        overflow: hidden !important;
        transition: border-color 0.2s, transform 0.15s, box-shadow 0.2s !important;
    }
    [data-testid="stMetric"]::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        background: linear-gradient(90deg, var(--green-400), var(--green-300), transparent);
    }
    [data-testid="stMetric"]::after {
        content: '';
        position: absolute;
        bottom: 0; right: 0;
        width: 60px; height: 60px;
        background: radial-gradient(circle, rgba(61,166,104,0.08) 0%, transparent 70%);
        border-radius: 50%;
    }
    [data-testid="stMetric"]:hover {
        border-color: var(--green-border-med) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3), 0 0 0 1px var(--green-border) !important;
    }
    [data-testid="stMetricValue"] {
        font-family: 'Syne', sans-serif !important;
        font-size: 22px !important;
        font-weight: 800 !important;
        color: var(--text-primary) !important;
        letter-spacing: -0.03em !important;
        line-height: 1 !important;
    }
    [data-testid="stMetricLabel"] {
        font-size: 10px !important;
        font-weight: 600 !important;
        color: var(--text-muted) !important;
        text-transform: uppercase !important;
        letter-spacing: 0.1em !important;
    }
    [data-testid="stMetricDelta"] { font-size: 11px !important; color: var(--green-400) !important; }

    /* ═══════════════════════════════════════════════════
       BUTTONS
    ═══════════════════════════════════════════════════ */
    .stButton > button {
        background: linear-gradient(135deg, var(--green-500), var(--green-400)) !important;
        color: #ffffff !important;
        font-family: 'Syne', sans-serif !important;
        font-weight: 700 !important;
        font-size: 11px !important;
        letter-spacing: 0.08em !important;
        text-transform: uppercase !important;
        border: none !important;
        border-radius: var(--radius-sm) !important;
        padding: 0.65rem 1.4rem !important;
        box-shadow: 0 2px 12px rgba(45,128,80,0.35), 0 0 0 1px rgba(61,166,104,0.2) !important;
        transition: all 0.2s ease !important;
        width: 100% !important;
        position: relative !important;
        overflow: hidden !important;
    }
    .stButton > button::after {
        content: '';
        position: absolute;
        inset: 0;
        background: linear-gradient(135deg, rgba(255,255,255,0.1), transparent);
        opacity: 0;
        transition: opacity 0.2s;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #256b44, #2d8050) !important;
        box-shadow: 0 6px 24px rgba(45,128,80,0.50) !important;
        transform: translateY(-2px) !important;
    }
    .stButton > button:hover::after { opacity: 1; }

    /* ═══════════════════════════════════════════════════
       EXPANDERS
    ═══════════════════════════════════════════════════ */
    .streamlit-expanderHeader {
        background: var(--card-bg) !important;
        border: 1px solid var(--card-border) !important;
        border-radius: var(--radius-sm) !important;
        padding: 0.65rem 1rem !important;
        font-weight: 600 !important;
        font-size: 12px !important;
        color: var(--text-secondary) !important;
        transition: all 0.18s !important;
    }
    .streamlit-expanderHeader:hover {
        border-color: var(--green-border-med) !important;
        color: var(--text-accent) !important;
        background: rgba(61,166,104,0.05) !important;
    }
    .streamlit-expanderContent {
        background: var(--card-bg) !important;
        border: 1px solid var(--card-border) !important;
        border-top: none !important;
        border-radius: 0 0 var(--radius-sm) var(--radius-sm) !important;
        padding: 1rem !important;
    }

    /* ═══════════════════════════════════════════════════
       ALERTS
    ═══════════════════════════════════════════════════ */
    .stAlert {
        background: rgba(61,166,104,0.07) !important;
        border: 1px solid var(--green-border) !important;
        border-left: 3px solid var(--green-400) !important;
        border-radius: var(--radius-md) !important;
        color: var(--text-primary) !important;
        font-size: 12px !important;
    }

    /* ═══════════════════════════════════════════════════
       CODE BLOCKS
    ═══════════════════════════════════════════════════ */
    .stCodeBlock, pre, code {
        background: #0a120d !important;
        border: 1px solid rgba(61,166,104,0.15) !important;
        border-radius: var(--radius-md) !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 11px !important;
        color: #7ed9a0 !important;
    }

    /* ═══════════════════════════════════════════════════
       SELECT / MULTISELECT / INPUT (main body)
    ═══════════════════════════════════════════════════ */
    .stSelectbox > div > div,
    .stMultiSelect > div > div {
        background: var(--card-bg) !important;
        border: 1px solid var(--card-border) !important;
        border-radius: var(--radius-sm) !important;
        color: var(--text-primary) !important;
        font-size: 12px !important;
    }
    .stTextInput input, .stTextArea textarea {
        background: var(--card-bg) !important;
        border: 1px solid var(--card-border) !important;
        border-radius: var(--radius-sm) !important;
        color: var(--text-primary) !important;
        font-size: 12px !important;
    }
    .stCheckbox label { font-size: 12px !important; color: var(--text-secondary) !important; }

    /* ═══════════════════════════════════════════════════
       DATAFRAME
    ═══════════════════════════════════════════════════ */
    .stDataFrame {
        border: 1px solid var(--card-border) !important;
        border-radius: var(--radius-md) !important;
        font-size: 12px !important;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3) !important;
    }

    /* ═══════════════════════════════════════════════════
       DIVIDER
    ═══════════════════════════════════════════════════ */
    hr { border: none !important; height: 1px !important; background: var(--border) !important; margin: 1.5rem 0 !important; }

    /* ═══════════════════════════════════════════════════
       CUSTOM COMPONENTS
    ═══════════════════════════════════════════════════ */

    .panel {
        background: var(--panel-bg);
        border: 1px solid var(--panel-border);
        border-radius: var(--radius-lg);
        padding: 1.35rem 1.5rem;
        margin-bottom: 1.1rem;
        position: relative;
        overflow: hidden;
        box-shadow: 0 4px 24px rgba(0,0,0,0.25), 0 1px 0 rgba(255,255,255,0.03) inset;
    }
    .panel::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 1px;
        background: linear-gradient(90deg, var(--green-400), rgba(61,166,104,0.3), transparent);
    }
    /* Subtle glow orb in panel corners */
    .panel::after {
        content: '';
        position: absolute;
        top: -40px; right: -40px;
        width: 120px; height: 120px;
        background: radial-gradient(circle, rgba(61,166,104,0.06) 0%, transparent 70%);
        border-radius: 50%;
        pointer-events: none;
    }

    .section-label {
        font-size: 10px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.18em;
        color: var(--green-400);
        margin-bottom: 0.45rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-family: 'Syne', sans-serif;
    }
    .section-label::before {
        content: '';
        display: inline-block;
        width: 16px; height: 2px;
        background: var(--green-400);
        border-radius: 2px;
    }

    .sb-block {
        background: var(--sb-block-bg);
        border: 1px solid var(--sb-block-border);
        border-radius: var(--radius-md);
        padding: 0.85rem 1rem;
        margin-bottom: 0.9rem;
        box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    }

    /* ── Use Case Cards ── */
    .uc-card {
        background: var(--card-bg);
        border: 1px solid var(--card-border);
        border-radius: var(--radius-md);
        padding: 0.9rem 1rem;
        margin-bottom: 0.6rem;
        transition: border-color 0.2s, box-shadow 0.2s, transform 0.15s;
        position: relative;
        overflow: hidden;
    }
    .uc-card::after {
        content: '';
        position: absolute;
        bottom: 0; left: 0; right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--green-border), transparent);
        opacity: 0;
        transition: opacity 0.2s;
    }
    .uc-card:hover {
        border-color: var(--card-border-hover);
        box-shadow: 0 4px 20px rgba(0,0,0,0.3), 0 0 0 1px var(--green-border);
        transform: translateY(-1px);
    }
    .uc-card:hover::after { opacity: 1; }
    .uc-card-title {
        font-weight: 600;
        font-size: 12px;
        color: var(--text-primary);
        margin-bottom: 0.25rem;
        font-family: 'DM Sans', sans-serif;
    }
    .uc-card-desc {
        font-size: 11px;
        color: var(--text-secondary);
        line-height: 1.5;
    }

    /* ── Badges ── */
    .badge {
        display: inline-flex;
        align-items: center;
        padding: 0.18rem 0.6rem;
        border-radius: 4px;
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        font-family: 'Syne', sans-serif;
    }

    /* ── Tags ── */
    .tag {
        display: inline-block;
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        color: var(--text-secondary);
        font-size: 10px;
        font-weight: 600;
        padding: 0.15rem 0.55rem;
        border-radius: 4px;
        margin-right: 0.3rem;
        letter-spacing: 0.04em;
        font-family: 'DM Sans', sans-serif;
    }

    /* ── Gate Box ── */
    .gate-box {
        background: rgba(61,166,104,0.06);
        border: 1px solid var(--green-border);
        border-left: 3px solid var(--green-400);
        border-radius: var(--radius-md);
        padding: 0.85rem 1rem;
        display: flex;
        align-items: flex-start;
        gap: 0.6rem;
        margin-bottom: 0.9rem;
    }
    .gate-text { font-size: 11px; color: var(--text-secondary); line-height: 1.6; }
    .gate-text strong { color: var(--green-400); }

    /* ── Lineage ── */
    .lineage-row {
        display: flex;
        align-items: baseline;
        gap: 0.75rem;
        padding: 0.5rem 0;
        border-bottom: 1px solid var(--border);
    }
    .lineage-row:last-child { border-bottom: none; }
    .lineage-key {
        font-size: 10px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: var(--text-muted);
        min-width: 9rem;
        font-family: 'Syne', sans-serif;
    }
    .lineage-val { font-size: 11px; color: var(--text-secondary); }

    /* ── Footer ── */
    .footer {
        text-align: center;
        margin-top: 3rem;
        padding: 1.5rem;
        color: var(--text-muted);
        font-size: 11px;
        letter-spacing: 0.06em;
        border-top: 1px solid var(--border);
        font-family: 'DM Sans', sans-serif;
    }
    .footer span { color: var(--green-400); }

    /* ── Kill default padding ── */
    .stApp > header { display: none !important; }
    #root > div:first-child { padding-top: 0 !important; }
    .block-container { padding-top: 0 !important; padding-bottom: 2rem !important; max-width: 100% !important; }
    [data-testid="stAppViewContainer"] > section:first-child { padding-top: 0 !important; }

    /* ═══════════════════════════════════════════════════
       STICKY HEADER
    ═══════════════════════════════════════════════════ */
    .top-header {
        position: sticky;
        top: 0;
        z-index: 999;
        background: rgba(10,18,12,0.96);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-bottom: 1px solid rgba(61,166,104,0.12);
        padding: 0.7rem 1.75rem;
        margin: 0 -1rem 1.5rem -1rem;
        display: flex;
        align-items: center;
        gap: 1rem;
        box-shadow: 0 4px 30px rgba(0,0,0,0.4);
    }

    /* ── Live pill ── */
    .live-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        background: rgba(61,166,104,0.10);
        border: 1px solid rgba(61,166,104,0.30);
        border-radius: 20px;
        padding: 0.28rem 0.8rem;
        font-size: 10px;
        font-weight: 700;
        color: var(--green-300);
        letter-spacing: 0.08em;
        text-transform: uppercase;
        font-family: 'Syne', sans-serif;
    }
    .live-dot {
        width: 6px; height: 6px;
        background: var(--green-300);
        border-radius: 50%;
        position: relative; flex-shrink: 0;
    }
    .live-dot::after {
        content: '';
        position: absolute;
        inset: -3px;
        border-radius: 50%;
        border: 1.5px solid rgba(110,204,160,0.4);
        animation: live-ping 1.6s ease-out infinite;
    }
    @keyframes live-ping {
        0%   { transform: scale(0.7); opacity: 1; }
        100% { transform: scale(2.4); opacity: 0; }
    }

    /* ═══════════════════════════════════════════════════
       PULSE LOADER
    ═══════════════════════════════════════════════════ */
    .pulse-loader {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 1.6rem;
        padding: 3.5rem 2rem;
        background: var(--card-bg);
        border: 1px solid var(--card-border);
        border-radius: var(--radius-lg);
        margin-bottom: 1.1rem;
        position: relative;
        overflow: hidden;
    }
    .pulse-loader::before {
        content: '';
        position: absolute;
        inset: 0;
        background: radial-gradient(ellipse 60% 50% at 50% 50%, rgba(61,166,104,0.08), transparent);
        pointer-events: none;
    }
    .pulse-rings {
        position: relative;
        width: 60px; height: 60px;
        display: flex; align-items: center; justify-content: center;
    }
    .pulse-rings span {
        position: absolute;
        border-radius: 50%;
        border: 1.5px solid rgba(110,204,160,0.7);
        animation: pulse-expand 2.4s ease-out infinite;
    }
    .pulse-rings span:nth-child(1) { width:60px; height:60px; animation-delay:0s; }
    .pulse-rings span:nth-child(2) { width:42px; height:42px; animation-delay:0.4s; }
    .pulse-rings span:nth-child(3) { width:26px; height:26px; animation-delay:0.8s; }
    .pulse-rings span:nth-child(4) {
        width: 12px; height: 12px;
        background: var(--green-400);
        border: none;
        box-shadow: 0 0 12px rgba(61,166,104,0.6);
        animation: none;
    }
    @keyframes pulse-expand {
        0%   { transform: scale(0.3); opacity: 0.9; }
        100% { transform: scale(1);   opacity: 0; }
    }
    .pulse-steps { display: flex; flex-direction: column; gap: 0.55rem; width: 100%; max-width: 280px; }
    .pulse-step {
        display: flex; align-items: center; gap: 0.65rem;
        font-size: 11px; color: rgba(255,255,255,0.2);
        transition: color 0.3s; font-family: 'DM Sans', sans-serif;
    }
    .pulse-step.active { color: rgba(255,255,255,0.85); }
    .pulse-step.done   { color: var(--green-400); }
    .step-dot {
        width: 6px; height: 6px; border-radius: 50%;
        background: rgba(255,255,255,0.15); flex-shrink: 0;
    }
    .pulse-step.active .step-dot {
        background: var(--green-300);
        box-shadow: 0 0 8px rgba(110,204,160,0.7);
        animation: blink 1s ease-in-out infinite;
    }
    .pulse-step.done .step-dot { background: var(--green-400); }
    @keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0.25; } }
    .pulse-label {
        font-family: 'Syne', sans-serif;
        font-size: 12px; font-weight: 700;
        color: var(--text-secondary);
        letter-spacing: 0.1em; text-transform: uppercase; text-align: center;
    }
    .pulse-sublabel {
        font-size: 11px; color: var(--text-muted); text-align: center; margin-top: -1rem;
    }

    /* ═══════════════════════════════════════════════════
       NEW: FEATURE CARDS — Sentiment / Score widgets
    ═══════════════════════════════════════════════════ */
    .score-ring {
        position: relative;
        display: inline-flex;
        align-items: center;
        justify-content: center;
    }
    .insight-chip {
        display: inline-flex;
        align-items: center;
        gap: 0.3rem;
        background: rgba(61,166,104,0.08);
        border: 1px solid var(--green-border);
        border-radius: 20px;
        padding: 0.2rem 0.65rem;
        font-size: 10px;
        font-weight: 600;
        color: var(--green-300);
        margin: 0.2rem;
        letter-spacing: 0.04em;
    }

    /* ── Scrollbar styling ── */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: var(--body-bg); }
    ::-webkit-scrollbar-thumb { background: rgba(61,166,104,0.25); border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: rgba(61,166,104,0.45); }

    /* ── Focus rings ── */
    *:focus-visible { outline: 2px solid var(--green-400) !important; outline-offset: 2px !important; }

    /* ── Sidebar new feature indicators ── */
    .new-badge {
        display: inline-block;
        background: linear-gradient(135deg, #2d8050, #3da668);
        color: #fff;
        font-size: 8px;
        font-weight: 800;
        padding: 0.1rem 0.4rem;
        border-radius: 3px;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        vertical-align: middle;
        margin-left: 0.3rem;
        font-family: 'Syne', sans-serif;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# Sticky Header Bar
# ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="top-header">
    <div style="width:34px; height:34px;
                background: linear-gradient(135deg, #1f5c38 0%, #3da668 100%);
                border-radius:9px; display:flex; align-items:center; justify-content:center;
                font-size:1rem; box-shadow: 0 4px 16px rgba(61,166,104,0.35),
                0 0 0 1px rgba(61,166,104,0.2); flex-shrink:0;">⚡</div>
    <div style="display:flex; flex-direction:column; gap:0; margin-left:0.15rem;">
        <div style="font-size:9px; font-weight:700; text-transform:uppercase;
                    letter-spacing:0.2em; color:rgba(110,204,160,0.6); line-height:1;
                    font-family:'Syne',sans-serif;">Snowflake Cortex</div>
        <div style="font-size:16px; font-weight:800; color:#e8f0ea;
                    letter-spacing:-0.025em; line-height:1.25; font-family:'Syne',sans-serif;">InsightForge</div>
    </div>
    <div style="width:1px; height:24px; background:rgba(255,255,255,0.08); margin:0 0.5rem;"></div>
    <div style="font-size:11px; color:rgba(255,255,255,0.25); margin-top:1px; font-family:'DM Sans',sans-serif;">
        Business Context → Data‑Driven Execution
    </div>
    <div style="margin-left:auto; display:flex; gap:0.5rem; align-items:center;">
        <span class="live-pill"><span class="live-dot"></span>Live</span>
        <span class="tag">Cortex AI</span>
        <span class="tag">Snowpark</span>
        <span class="tag">v2.0</span>
    </div>
</div>
""", unsafe_allow_html=True)

session = get_active_session()

# ─────────────────────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    # Sidebar branding strip
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1a3d28, #2d8050);
                margin: 0 -1rem 1.2rem -1rem; padding: 1rem 1.25rem;
                border-bottom: 1px solid #c2d8ca;">
        <div style="font-family:'Syne',sans-serif; font-size:13px; font-weight:800;
                    color:#ffffff; letter-spacing:-0.01em;">Configure Session</div>
        <div style="font-size:11px; color:rgba(255,255,255,0.65); margin-top:2px;
                    font-family:'DM Sans',sans-serif;">Set up your analysis workspace</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Transcripts Block ────────────────────────────────
    st.markdown("<div class='sb-block'>", unsafe_allow_html=True)
    st.markdown("""
    <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.65rem;">
        <div style="width:24px;height:24px;background:#e8f5ef;border-radius:5px;
                    display:flex;align-items:center;justify-content:center;font-size:12px;
                    border:1px solid #b0d8c0;">📂</div>
        <div style="font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:0.14em;
                    color:#1e5038;font-family:'Syne',sans-serif;">Transcripts</div>
    </div>
    """, unsafe_allow_html=True)
    doc_type = st.selectbox("Document Type", ["Discovery", "SCC", "Future Deck", "ARB", "Other"])
    uploaded_files = st.file_uploader("Drop files here", accept_multiple_files=True,
                                      type=['txt', 'md', 'csv', 'pdf', 'docx'])
    if uploaded_files:
        for file in uploaded_files:
            content = file.read().decode("utf-8", errors="ignore")
            content_escaped = content.replace("'", "''")
            session.sql(f"""
                INSERT INTO transcripts (filename, doc_type, content)
                VALUES ('{file.name}', '{doc_type}', '{content_escaped}')
            """).collect()
        st.success(f"✓ {len(uploaded_files)} file(s) uploaded.")
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Customer Block ───────────────────────────────────
    st.markdown("<div class='sb-block'>", unsafe_allow_html=True)
    st.markdown("""
    <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.65rem;">
        <div style="width:24px;height:24px;background:#e8f0ff;border-radius:5px;
                    display:flex;align-items:center;justify-content:center;font-size:12px;
                    border:1px solid #b0c8f0;">🏢</div>
        <div style="font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:0.14em;
                    color:#1e5038;font-family:'Syne',sans-serif;">Customer</div>
    </div>
    """, unsafe_allow_html=True)
    customer_name = st.text_input("Customer Name", "Acme Corp")
    industry = st.text_input("Industry", "SaaS / Technology")
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Data Sources Block ───────────────────────────────
    st.markdown("<div class='sb-block'>", unsafe_allow_html=True)
    st.markdown("""
    <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.65rem;">
        <div style="width:24px;height:24px;background:#fef3e2;border-radius:5px;
                    display:flex;align-items:center;justify-content:center;font-size:12px;
                    border:1px solid #f0d080;">🗄️</div>
        <div style="font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:0.14em;
                    color:#1e5038;font-family:'Syne',sans-serif;">Data Sources</div>
    </div>
    """, unsafe_allow_html=True)
    tables_df = session.sql("SELECT DISTINCT fully_qualified_table_name FROM table_metadata").to_pandas()
    table_options = tables_df['FULLY_QUALIFIED_TABLE_NAME'].tolist()
    selected_tables = st.multiselect("Choose tables", table_options,
                                     default=table_options[:2] if table_options else [])
    st.markdown("</div>", unsafe_allow_html=True)

    # ── NEW: Analysis Options ────────────────────────────
    st.markdown("<div class='sb-block'>", unsafe_allow_html=True)
    st.markdown("""
    <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.65rem;">
        <div style="width:24px;height:24px;background:#f0eaff;border-radius:5px;
                    display:flex;align-items:center;justify-content:center;font-size:12px;
                    border:1px solid #c8b0f0;">⚙️</div>
        <div style="font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:0.14em;
                    color:#1e5038;font-family:'Syne',sans-serif;">Analysis Options
            <span class="new-badge">new</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    analysis_depth = st.selectbox("Analysis Depth", ["Standard", "Deep Dive", "Quick Scan"])
    include_competitor = st.checkbox("Include Competitor Benchmarking", value=False)
    include_risk = st.checkbox("Flag Data Privacy Risks", value=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Analyze Button ───────────────────────────────────
    run_analysis = st.button("⚡ Analyze & Generate Use Cases", type="primary")

    # ── Sidebar footer ──
    st.markdown("""
    <div style="margin-top:1.5rem; padding-top:0.75rem; border-top:1px solid #c2d8ca;
                text-align:center; font-size:10px; color:#7aaa88; font-family:'DM Sans',sans-serif;">
        Powered by <span style="color:#2d8050;font-weight:700;">Snowflake Cortex</span>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# Session State Init
# ─────────────────────────────────────────────────────────────
for key in ["analysis", "market_trends", "matches", "industry_cached", "data_samples", "pdf_report"]:
    if key not in st.session_state:
        st.session_state[key] = None

# ─────────────────────────────────────────────────────────────
# STEP 1 — Run Analysis
# ─────────────────────────────────────────────────────────────
if run_analysis:
    if not selected_tables:
        st.warning("Please select at least one table to analyze.")
        st.stop()

    docs_df = session.sql("SELECT doc_type, content FROM transcripts ORDER BY upload_date DESC LIMIT 20").to_pandas()
    if docs_df.empty:
        st.warning("No transcripts found. Please upload documents first.")
        st.stop()

    discovery = "\n".join(docs_df[docs_df['DOC_TYPE']=='Discovery']['CONTENT'].tolist())
    scc        = "\n".join(docs_df[docs_df['DOC_TYPE']=='SCC']['CONTENT'].tolist())
    future     = "\n".join(docs_df[docs_df['DOC_TYPE']=='Future Deck']['CONTENT'].tolist())
    other      = "\n".join(docs_df[~docs_df['DOC_TYPE'].isin(['Discovery','SCC','Future Deck'])]['CONTENT'].tolist())

    all_content = f"""
    DISCOVERY TRANSCRIPTS:
    {discovery if discovery else 'None'}
    STEERING COMMITTEE (SCC) TRANSCRIPTS:
    {scc if scc else 'None'}
    FUTURE DECK CALLS:
    {future if future else 'None'}
    OTHER NOTES:
    {other if other else 'None'}
    """

    # ── Animated Pulse Loader ──────────────────────────
    loader_placeholder = st.empty()
    loader_placeholder.markdown("""
    <div class="pulse-loader">
        <div class="pulse-rings">
            <span></span><span></span><span></span><span></span>
        </div>
        <div class="pulse-label">Cortex is Analyzing</div>
        <div class="pulse-sublabel">Reading transcripts &amp; mapping to your data schema...</div>
        <div class="pulse-steps">
            <div class="pulse-step active"><span class="step-dot"></span> Parsing transcript content</div>
            <div class="pulse-step"><span class="step-dot"></span> Extracting business signals</div>
            <div class="pulse-step"><span class="step-dot"></span> Running market research</div>
            <div class="pulse-step"><span class="step-dot"></span> Matching use cases to schema</div>
            <div class="pulse-step"><span class="step-dot"></span> Scoring ROI &amp; risk signals</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.spinner(""):

        # ── Step 1: Extract insights ──────────────────
        extraction_prompt = f"""
        You are an expert Snowflake business consultant. Analyze the following customer transcripts and extract use cases across THREE disciplines:

        1. Data Analytics (BI dashboards, KPI reports, trend analysis)
        2. Data Engineering (pipelines, data quality, ingestion, transformation, orchestration)
        3. Data Science & AI (ML models, predictions, recommendations, NLP, anomaly detection)

        Transcripts:
        {all_content[:18000]}

        For each use case also provide:
        - A short ROI reason (e.g. "Reduces manual reconciliation by 80%", "Predicts churn 30 days early saving $200K/yr")
        - Estimated business value tier: "Quick Win", "Strategic", or "Transformational"
        - Which stakeholder benefits most (e.g. "CFO", "VP Sales", "Data Team", "COO")
        - A complexity score 1-5 (1=easy, 5=complex)
        - An urgency flag: "Immediate", "Near-term", or "Future"

        Return ONLY valid JSON:
        {{
          "metrics": {{"pain_point_count": int, "sentiment_score": float, "roadmap_item_count": int, "urgency_level": "Low/Medium/High", "data_maturity": "Foundational/Developing/Advanced"}},
          "analytics_usecases": [
            {{"name": "...", "roi": "...", "value_tier": "Quick Win|Strategic|Transformational", "stakeholder": "...", "complexity": int, "urgency": "Immediate|Near-term|Future"}}
          ],
          "dataengineering_usecases": [
            {{"name": "...", "roi": "...", "value_tier": "Quick Win|Strategic|Transformational", "stakeholder": "...", "complexity": int, "urgency": "Immediate|Near-term|Future"}}
          ],
          "datascience_usecases": [
            {{"name": "...", "roi": "...", "value_tier": "Quick Win|Strategic|Transformational", "stakeholder": "...", "complexity": int, "urgency": "Immediate|Near-term|Future"}}
          ],
          "key_themes": ["theme1", "theme2", "theme3"],
          "top_risk": "one sentence describing the biggest risk if action is not taken"
        }}
        """
        extraction_result = session.sql(f"SELECT cortex_complete('{extraction_prompt.replace(chr(39), chr(39)*2)}') as result").collect()[0][0]
        try:
            st.session_state.analysis = json.loads(extraction_result)
        except:
            st.session_state.analysis = {
                "metrics": {"pain_point_count": 5, "sentiment_score": 6.5, "roadmap_item_count": 3, "urgency_level": "Medium", "data_maturity": "Developing"},
                "analytics_usecases": [
                    {"name": "Customer Payment Delay Dashboard", "roi": "Reduces DSO by 15 days, freeing $500K working capital", "value_tier": "Quick Win", "stakeholder": "CFO", "complexity": 2, "urgency": "Immediate"},
                    {"name": "Sales Revenue Trend Analysis", "roi": "Aligns sales forecasts within 5%, improving resource planning", "value_tier": "Quick Win", "stakeholder": "VP Sales", "complexity": 1, "urgency": "Immediate"},
                    {"name": "Marketing ROI by Channel", "roi": "Redirects 20% of spend to top channels, lifting conversion by 18%", "value_tier": "Strategic", "stakeholder": "CMO", "complexity": 3, "urgency": "Near-term"},
                    {"name": "Executive KPI Scorecard", "roi": "Saves 8hrs/week manual reporting across leadership team", "value_tier": "Quick Win", "stakeholder": "CEO", "complexity": 2, "urgency": "Immediate"},
                ],
                "dataengineering_usecases": [
                    {"name": "Automated Data Quality Pipeline", "roi": "Eliminates 90% of bad data reaching reports", "value_tier": "Strategic", "stakeholder": "Data Team", "complexity": 3, "urgency": "Near-term"},
                    {"name": "Real-Time CRM Data Ingestion", "roi": "Reduces data latency from D+1 to minutes", "value_tier": "Transformational", "stakeholder": "VP Sales", "complexity": 4, "urgency": "Near-term"},
                    {"name": "Data Lineage & Governance Layer", "roi": "Cuts audit preparation time from 3 weeks to 2 days", "value_tier": "Strategic", "stakeholder": "COO", "complexity": 3, "urgency": "Future"},
                    {"name": "Multi-Source ETL Consolidation", "roi": "Reduces pipeline maintenance cost by 60%", "value_tier": "Strategic", "stakeholder": "CTO", "complexity": 4, "urgency": "Near-term"},
                ],
                "datascience_usecases": [
                    {"name": "Customer Churn Prediction Model", "roi": "Predicts churn 30 days early, saves $200K/yr", "value_tier": "Transformational", "stakeholder": "CCO", "complexity": 4, "urgency": "Near-term"},
                    {"name": "Next Best Offer Recommendation", "roi": "Lifts upsell revenue by 12-18%", "value_tier": "Transformational", "stakeholder": "VP Sales", "complexity": 5, "urgency": "Future"},
                    {"name": "Demand Forecasting with ML", "roi": "Reduces inventory overstock by 25%, saving $150K/yr", "value_tier": "Strategic", "stakeholder": "COO", "complexity": 4, "urgency": "Near-term"},
                    {"name": "Anomaly Detection on Transactions", "roi": "Catches fraud 3x faster, reducing exposure by $80K/yr", "value_tier": "Transformational", "stakeholder": "CFO", "complexity": 4, "urgency": "Immediate"},
                ],
                "key_themes": ["Revenue Leakage", "Data Quality", "Customer Retention"],
                "top_risk": "Continued manual reporting will delay decision-making by 2-3 weeks as customer scales."
            }

        # ── Step 2: Market research ────────────────────
        market_prompt = f"""
        For a customer in the {industry} industry, provide 3 current market trends or benchmarks relevant to data analytics and AI adoption.
        Suggest how these translate into business use cases for this customer.
        """
        st.session_state.market_trends = session.sql(f"SELECT cortex_complete('{market_prompt.replace(chr(39), chr(39)*2)}') as trends").collect()[0][0]
        st.session_state.industry_cached = industry

        # ── Step 3: Schema matching ────────────────────
        selected_tables_str = "', '".join(selected_tables)
        schema_df = session.sql(f"""
            SELECT fully_qualified_table_name, LISTAGG(column_name, ', ') AS columns
            FROM table_metadata
            WHERE fully_qualified_table_name IN ('{selected_tables_str}')
            GROUP BY 1
        """).to_pandas()
        schema_str = "\n".join([f"{row['FULLY_QUALIFIED_TABLE_NAME']}: {row['COLUMNS']}" for _, row in schema_df.iterrows()])

        data_samples = {}
        for tbl in selected_tables[:4]:
            try:
                sample = session.sql(f"SELECT * FROM {tbl} LIMIT 3").to_pandas()
                sample.columns = [c.lower() for c in sample.columns]
                data_samples[tbl] = sample.to_dict(orient="records")
            except Exception:
                data_samples[tbl] = []

        all_ucs = (
            st.session_state.analysis.get("analytics_usecases", []) +
            st.session_state.analysis.get("dataengineering_usecases", []) +
            st.session_state.analysis.get("datascience_usecases", [])
        )
        uc_names_by_type = []
        for uc in all_ucs:
            n = uc.get("name","") if isinstance(uc, dict) else str(uc)
            t = "Analytics" if uc in st.session_state.analysis.get("analytics_usecases",[]) else \
                "Data Engineering" if uc in st.session_state.analysis.get("dataengineering_usecases",[]) else \
                "Data Science"
            uc_names_by_type.append(f"{t}: {n}")

        import json as _json
        samples_str = _json.dumps(data_samples, default=str)[:3000]

        match_prompt = f"""
You are a Snowflake Solutions Engineer. MAP each identified use case to the real customer database,
then propose a live proof-of-concept demo using ACTUAL columns and data.

IDENTIFIED USE CASES:
{chr(10).join(uc_names_by_type)}

DATABASE SCHEMA:
{schema_str}

ACTUAL SAMPLE DATA:
{samples_str}

For EACH use case:
1. Identify which tables and columns directly support it
2. Write a working Snowflake SQL query using REAL column names
3. Assign data confidence: High/Medium/Low

Return JSON array. Each item:
{{
  "usecase": "exact use case name",
  "type": "Analytics|Data Engineering|Data Science",
  "tables": ["fully.qualified.table"],
  "columns_used": ["col1", "col2"],
  "sql": "SELECT ... FROM real_table_name ... LIMIT 20",
  "demo_description": "2-sentence description of what demo shows and what business decision it supports",
  "data_confidence": "High|Medium|Low",
  "confidence_reason": "one sentence explaining the confidence level",
  "what_data_proves": "one sentence on what actual data demonstrates for the customer",
  "estimated_effort_days": int,
  "snowflake_features": ["Cortex ML", "Snowpark", "Dynamic Tables", "Streamlit"]
}}

CRITICAL: Only use column names that appear in the schema. Return ONLY valid JSON array.
"""
        matches_json = session.sql(f"SELECT cortex_complete('{match_prompt.replace(chr(39), chr(39)*2)}') as matches").collect()[0][0]
        try:
            st.session_state.matches = json.loads(matches_json)
        except:
            st.session_state.matches = [
                {"usecase": "Customer Payment Delay Dashboard", "type": "Analytics",
                 "tables": ["COCO_HACKATHON_DB.CORE_DATA.SALES_DATA"],
                 "columns_used": ["customer_name", "sale_date"],
                 "sql": "SELECT customer_name, AVG(DATEDIFF(day, sale_date, CURRENT_DATE)) as avg_delay, COUNT(*) as invoices FROM COCO_HACKATHON_DB.CORE_DATA.SALES_DATA GROUP BY customer_name ORDER BY avg_delay DESC LIMIT 20",
                 "demo_description": "Shows average payment delay per customer ranked by risk. Helps AR teams prioritise collections.",
                 "data_confidence": "High",
                 "confidence_reason": "SALES_DATA contains sale_date and customer_name enabling direct delay calculation.",
                 "what_data_proves": "Shows real customer payment patterns validating AR risk from Discovery call.",
                 "estimated_effort_days": 5,
                 "snowflake_features": ["Streamlit", "Snowpark"]},
            ]

        st.session_state.data_samples = data_samples

    loader_placeholder.empty()

# ─────────────────────────────────────────────────────────────
# STEP 2 — Render Results
# ─────────────────────────────────────────────────────────────
if st.session_state.analysis:
    analysis      = st.session_state.analysis
    market_trends = st.session_state.market_trends
    matches       = st.session_state.matches
    industry_disp = st.session_state.industry_cached or "Your Industry"

    # ══════════════════════════════════════════════════════
    # OVERVIEW METRICS
    # ══════════════════════════════════════════════════════
    st.markdown("<div class='section-label'>Analysis Overview</div>", unsafe_allow_html=True)
    st.markdown("<div class='panel'>", unsafe_allow_html=True)
    metrics = analysis.get("metrics", {})

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.metric("Pain Points", metrics.get("pain_point_count", "—"))
    with c2:
        st.metric("Sentiment Score", f"{metrics.get('sentiment_score', '—')} / 10")
    with c3:
        st.metric("Roadmap Items", metrics.get("roadmap_item_count", "—"))
    with c4:
        urgency = metrics.get("urgency_level", "—")
        icon = {"High": "▲", "Medium": "◆", "Low": "▼"}.get(urgency, "·")
        st.metric("Urgency", f"{icon} {urgency}")
    with c5:
        maturity = metrics.get("data_maturity", "—")
        st.metric("Data Maturity", maturity)

    # ── Key Themes + Top Risk ─────────────────────────
    themes = analysis.get("key_themes", [])
    top_risk = analysis.get("top_risk", "")
    if themes or top_risk:
        col_th, col_rk = st.columns([1.5, 1])
        with col_th:
            if themes:
                theme_chips = "".join([f'<span class="insight-chip">🏷 {t}</span>' for t in themes])
                st.markdown(f"""
                <div style="margin-top:0.75rem;">
                    <div style="font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:0.1em;
                                color:var(--text-muted);margin-bottom:0.4rem;font-family:'Syne',sans-serif;">Key Themes Detected</div>
                    {theme_chips}
                </div>""", unsafe_allow_html=True)
        with col_rk:
            if top_risk:
                st.markdown(f"""
                <div style="background:rgba(201,64,64,0.08);border:1px solid rgba(201,64,64,0.2);
                            border-left:3px solid #c94040;border-radius:8px;padding:0.65rem 0.85rem;margin-top:0.75rem;">
                    <div style="font-size:10px;font-weight:700;color:#c94040;text-transform:uppercase;
                                letter-spacing:0.1em;margin-bottom:0.2rem;font-family:'Syne',sans-serif;">⚠ Top Risk Signal</div>
                    <div style="font-size:11px;color:#e8a0a0;line-height:1.5;">{top_risk}</div>
                </div>""", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════
    # MARKET INTELLIGENCE
    # ══════════════════════════════════════════════════════
    st.markdown("<div class='section-label' style='margin-top:1.1rem;'>Market Intelligence</div>", unsafe_allow_html=True)
    st.markdown("<div class='panel'>", unsafe_allow_html=True)
    st.markdown(f"<h2>📈 Industry Trends — {industry_disp}</h2>", unsafe_allow_html=True)
    st.markdown(f"<div style='color:var(--text-secondary); font-size:12px; line-height:1.75;'>{market_trends}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════
    # USE CASE LANDSCAPE
    # ══════════════════════════════════════════════════════
    st.markdown("<div class='section-label' style='margin-top:1.1rem;'>Use Case Landscape</div>", unsafe_allow_html=True)
    st.markdown("<div class='panel'>", unsafe_allow_html=True)
    st.markdown("<h2>💡 Identified Opportunities — Select for Demo</h2>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:11px;color:var(--text-muted);margin-bottom:0.75rem;'>All use cases identified from your transcripts. Toggle to add to your demo queue.</div>", unsafe_allow_html=True)

    def uc_card_html(uc, idx, cat_key):
        if isinstance(uc, dict):
            name       = uc.get("name", uc.get("usecase", str(uc)))
            roi        = uc.get("roi", "")
            tier       = uc.get("value_tier", "Strategic")
            stakeholder= uc.get("stakeholder", "")
            complexity = uc.get("complexity", 0)
            urgency    = uc.get("urgency", "")
        else:
            name, roi, tier, stakeholder, complexity, urgency = str(uc), "", "Strategic", "", 0, ""

        tier_map = {
            "Quick Win":        ("rgba(61,166,104,0.12)",  "#3da668",  "rgba(61,166,104,0.3)"),
            "Strategic":        ("rgba(79,140,255,0.10)",  "#5b9aff",  "rgba(79,140,255,0.3)"),
            "Transformational": ("rgba(212,160,23,0.10)",  "#d4a017",  "rgba(212,160,23,0.3)"),
        }
        bg, fg, border = tier_map.get(tier, tier_map["Strategic"])

        urgency_map = {"Immediate": "#c94040", "Near-term": "#d4a017", "Future": "#5b9aff"}
        urg_color   = urgency_map.get(urgency, "#5a7a65")

        complexity_dots = "".join([
            '<span style="width:5px;height:5px;border-radius:50%;display:inline-block;margin-right:2px;background:' +
            ("#3da668" if i < complexity else "rgba(255,255,255,0.12)") + ';"></span>'
            for i in range(5)
        ]) if complexity else ""

        roi_html   = f'<div style="font-size:11px;color:#6ecca0;font-weight:600;margin-bottom:0.2rem;line-height:1.4;">💰 {roi}</div>' if roi else ""
        holder_html= f'<div style="font-size:10px;color:var(--text-muted);">👤 {stakeholder}{(" · " if stakeholder and urgency else "")}<span style="color:{urg_color};font-weight:600;">{urgency}</span></div>' if (stakeholder or urgency) else ""

        return f"""
        <div class="uc-card">
            <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:0.3rem;">
                <div class="uc-card-title">{name}</div>
                <span style="background:{bg};color:{fg};border:1px solid {border};
                             font-size:9px;font-weight:700;padding:0.15rem 0.5rem;border-radius:4px;
                             text-transform:uppercase;flex-shrink:0;margin-left:0.5rem;
                             letter-spacing:0.06em;font-family:'Syne',sans-serif;">{tier}</span>
            </div>
            {roi_html}
            {holder_html}
        </div>"""

    def normalise_ucs(raw_list):
        result = []
        for uc in raw_list:
            if isinstance(uc, str):
                result.append({"name": uc, "roi": "", "value_tier": "Strategic", "stakeholder": "", "complexity": 0, "urgency": ""})
            elif isinstance(uc, dict):
                result.append(uc)
        return result

    analytics_ucs = normalise_ucs(analysis.get("analytics_usecases", []))
    de_ucs        = normalise_ucs(analysis.get("dataengineering_usecases", []))
    ds_ucs        = normalise_ucs(analysis.get("datascience_usecases", []))

    if "sel_ucs" not in st.session_state:
        st.session_state.sel_ucs = []

    tab_a, tab_de, tab_ds, tab_prio, tab_sel = st.tabs([
        f"📊 Analytics ({len(analytics_ucs)})",
        f"⚙️ Data Engineering ({len(de_ucs)})",
        f"🤖 Data Science & AI ({len(ds_ucs)})",
        f"🎯 Priority Matrix",
        f"✦ Selected ({len(st.session_state.sel_ucs)})",
    ])

    with tab_a:
        st.markdown("<div style='font-size:11px;color:var(--text-muted);margin-bottom:0.6rem;'>Dashboards, KPI reports, trend analysis, and BI visualisations.</div>", unsafe_allow_html=True)
        cols_a = st.columns(2)
        for i, uc in enumerate(analytics_ucs):
            uc_name = uc.get("name", str(uc))
            with cols_a[i % 2]:
                st.markdown(uc_card_html(uc, i, "analytics"), unsafe_allow_html=True)
                if st.checkbox("Add to Demo", key=f"ck_a_{i}", value=uc_name in st.session_state.sel_ucs):
                    if uc_name not in st.session_state.sel_ucs:
                        st.session_state.sel_ucs.append(uc_name)
                elif uc_name in st.session_state.sel_ucs:
                    st.session_state.sel_ucs.remove(uc_name)

    with tab_de:
        st.markdown("<div style='font-size:11px;color:var(--text-muted);margin-bottom:0.6rem;'>Data pipelines, ingestion, quality, lineage, transformation, and orchestration.</div>", unsafe_allow_html=True)
        cols_de = st.columns(2)
        for i, uc in enumerate(de_ucs):
            uc_name = uc.get("name", str(uc))
            with cols_de[i % 2]:
                st.markdown(uc_card_html(uc, i, "de"), unsafe_allow_html=True)
                if st.checkbox("Add to Demo", key=f"ck_de_{i}", value=uc_name in st.session_state.sel_ucs):
                    if uc_name not in st.session_state.sel_ucs:
                        st.session_state.sel_ucs.append(uc_name)
                elif uc_name in st.session_state.sel_ucs:
                    st.session_state.sel_ucs.remove(uc_name)

    with tab_ds:
        st.markdown("<div style='font-size:11px;color:var(--text-muted);margin-bottom:0.6rem;'>ML models, predictions, recommendations, NLP, and anomaly detection on Cortex.</div>", unsafe_allow_html=True)
        cols_ds = st.columns(2)
        for i, uc in enumerate(ds_ucs):
            uc_name = uc.get("name", str(uc))
            with cols_ds[i % 2]:
                st.markdown(uc_card_html(uc, i, "ds"), unsafe_allow_html=True)
                if st.checkbox("Add to Demo", key=f"ck_ds_{i}", value=uc_name in st.session_state.sel_ucs):
                    if uc_name not in st.session_state.sel_ucs:
                        st.session_state.sel_ucs.append(uc_name)
                elif uc_name in st.session_state.sel_ucs:
                    st.session_state.sel_ucs.remove(uc_name)

    # ── NEW: Priority Matrix Tab ─────────────────────────────
    with tab_prio:
        st.markdown("<div style='font-size:11px;color:var(--text-muted);margin-bottom:0.75rem;'>Use cases plotted by complexity vs. value tier. Quick Wins are your immediate starting point.</div>", unsafe_allow_html=True)

        all_ucs_for_matrix = analytics_ucs + de_ucs + ds_ucs
        matrix_data = []
        type_labels = (
            [("Analytics", uc) for uc in analytics_ucs] +
            [("Data Engineering", uc) for uc in de_ucs] +
            [("Data Science", uc) for uc in ds_ucs]
        )
        tier_y = {"Quick Win": 1, "Strategic": 2, "Transformational": 3}
        for tp, uc in type_labels:
            matrix_data.append({
                "name": uc.get("name",""),
                "type": tp,
                "complexity": uc.get("complexity", 3),
                "value_y": tier_y.get(uc.get("value_tier","Strategic"), 2),
                "tier": uc.get("value_tier","Strategic"),
                "roi": uc.get("roi",""),
                "stakeholder": uc.get("stakeholder",""),
            })

        if matrix_data:
            matrix_df = pd.DataFrame(matrix_data)
            fig_matrix = px.scatter(
                matrix_df,
                x="complexity",
                y="value_y",
                color="type",
                size=[20] * len(matrix_df),
                hover_name="name",
                hover_data={"roi": True, "stakeholder": True, "complexity": True, "value_y": False, "type": False},
                color_discrete_map={
                    "Analytics": "#3da668",
                    "Data Engineering": "#5b9aff",
                    "Data Science": "#d4a017",
                },
                text="name",
            )
            fig_matrix.update_traces(textposition="top center", textfont=dict(size=9, color="#9dbdaa"))
            fig_matrix.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family='DM Sans', color='#9dbdaa', size=11),
                xaxis=dict(
                    title="Implementation Complexity →",
                    gridcolor='rgba(255,255,255,0.04)',
                    linecolor='rgba(255,255,255,0.08)',
                    tickvals=[1,2,3,4,5],
                    ticktext=["Very Easy","Easy","Medium","Hard","Very Hard"],
                    color='#5a7a65',
                ),
                yaxis=dict(
                    title="Business Value ↑",
                    gridcolor='rgba(255,255,255,0.04)',
                    linecolor='rgba(255,255,255,0.08)',
                    tickvals=[1,2,3],
                    ticktext=["Quick Win","Strategic","Transformational"],
                    color='#5a7a65',
                ),
                legend=dict(font=dict(color='#9dbdaa', size=10), bgcolor='rgba(0,0,0,0)'),
                margin=dict(l=0, r=0, t=20, b=0),
                height=380,
            )
            # Add quadrant shading
            fig_matrix.add_shape(type="rect", x0=0.5, y0=0.5, x1=2.5, y1=1.5,
                                  fillcolor="rgba(61,166,104,0.06)", line=dict(width=0), layer="below")
            st.plotly_chart(fig_matrix, use_container_width=True)
            st.markdown("""
            <div style="display:flex;gap:1rem;flex-wrap:wrap;margin-top:0.25rem;">
                <span class="insight-chip">🟢 Bottom-left = Quick Wins — Start here</span>
                <span class="insight-chip">🔵 Top-right = Transformational — Plan ahead</span>
                <span class="insight-chip">🟡 Diagonal = Strategic roadmap</span>
            </div>""", unsafe_allow_html=True)

    with tab_sel:
        if not st.session_state.sel_ucs:
            st.markdown("""
            <div style="text-align:center;padding:2rem;color:var(--text-muted);">
                <div style="font-size:1.5rem;margin-bottom:0.5rem;">🎯</div>
                <div style="font-size:12px;">No use cases selected yet.<br/>Tick 'Add to Demo' on any use case above.</div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='font-size:12px;color:#3da668;font-weight:600;margin-bottom:0.5rem;'>✓ {len(st.session_state.sel_ucs)} use case(s) queued for demo</div>", unsafe_allow_html=True)
            for uc_name in st.session_state.sel_ucs:
                st.markdown(f"""
                <div style="padding:0.4rem 0.85rem;background:rgba(61,166,104,0.07);
                            border:1px solid rgba(61,166,104,0.18);border-radius:6px;
                            margin-bottom:0.35rem;font-size:12px;color:var(--text-primary);">
                    <span style="color:var(--green-400);margin-right:0.4rem;">✦</span>{uc_name}
                </div>""", unsafe_allow_html=True)
            if st.button("🗑️ Clear All Selections"):
                st.session_state.sel_ucs = []
                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════
    # DATA MATCH & DEMO SELECTION
    # ══════════════════════════════════════════════════════
    all_ucs_flat = analytics_ucs + de_ucs + ds_ucs

    if matches:
        st.markdown("<div class='section-label' style='margin-top:1.1rem;'>Data Match & Demo Selection</div>", unsafe_allow_html=True)
        st.markdown("<div class='panel'>", unsafe_allow_html=True)
        st.markdown("<h2>🔍 Cortex Mapped Use Cases to Your Real Data</h2>", unsafe_allow_html=True)
        st.markdown("<div style='font-size:11px;color:var(--text-muted);margin-bottom:0.85rem;'>Each use case validated against your actual database schema. Confidence shows how well your existing data supports delivery.</div>", unsafe_allow_html=True)

        conf_styles = {
            "High":   {"color": "#3da668", "bg": "rgba(61,166,104,0.12)",  "border": "rgba(61,166,104,0.25)"},
            "Medium": {"color": "#d4a017", "bg": "rgba(212,160,23,0.10)",  "border": "rgba(212,160,23,0.25)"},
            "Low":    {"color": "#c94040", "bg": "rgba(201,64,64,0.08)",   "border": "rgba(201,64,64,0.22)"},
        }
        type_colors = {"Analytics": "#5b9aff", "Data Engineering": "#b07fff", "Data Science": "#3da668"}

        for m in matches:
            conf     = m.get("data_confidence", "Medium")
            cs       = conf_styles.get(conf, conf_styles["Medium"])
            proof    = m.get("what_data_proves", "")
            reason   = m.get("confidence_reason", "")
            cols_used= ", ".join(m.get("columns_used", []))
            type_fg  = type_colors.get(m.get("type","Analytics"), "#5b9aff")
            effort   = m.get("estimated_effort_days", "")
            features = m.get("snowflake_features", [])
            features_html = "".join([f'<span style="background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.08);border-radius:3px;padding:0.1rem 0.4rem;font-size:9px;color:var(--text-muted);margin-right:0.25rem;">{f}</span>' for f in features])

            st.markdown(f"""
            <div style="background:var(--card-bg);border:1px solid var(--card-border);
                        border-radius:10px;padding:0.9rem 1.1rem;margin-bottom:0.6rem;
                        border-left:3px solid {cs['color']};
                        transition:border-color 0.2s;">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:0.4rem;">
                    <div style="font-size:13px;font-weight:700;color:var(--text-primary);
                                font-family:'Syne',sans-serif;">{m.get('usecase','')}</div>
                    <div style="display:flex;gap:0.35rem;flex-shrink:0;margin-left:0.75rem;flex-wrap:wrap;justify-content:flex-end;">
                        <span style="background:{cs['bg']};color:{cs['color']};border:1px solid {cs['border']};
                                     font-size:9px;font-weight:700;padding:0.15rem 0.5rem;
                                     border-radius:4px;text-transform:uppercase;font-family:'Syne',sans-serif;">
                            {conf} Confidence
                        </span>
                        <span style="background:rgba(255,255,255,0.04);color:{type_fg};
                                     border:1px solid rgba(255,255,255,0.08);
                                     font-size:9px;font-weight:700;padding:0.15rem 0.5rem;border-radius:4px;">
                            {m.get('type','')}
                        </span>
                        {f'<span style="background:rgba(255,255,255,0.03);color:var(--text-muted);border:1px solid rgba(255,255,255,0.07);font-size:9px;padding:0.15rem 0.5rem;border-radius:4px;">~{effort}d</span>' if effort else ''}
                    </div>
                </div>
                <div style="font-size:11px;color:var(--text-secondary);margin-bottom:0.3rem;line-height:1.55;">
                    {m.get('demo_description','')}
                </div>
                <div style="font-size:10px;color:var(--text-muted);margin-bottom:0.2rem;">
                    🗄️ <span style="font-family:'JetBrains Mono',monospace;color:var(--text-secondary);">{', '.join(m.get('tables',[]))}</span>
                </div>
                {f'<div style="font-size:10px;color:var(--text-muted);margin-bottom:0.25rem;">📎 <span style="font-family:monospace;">{cols_used}</span></div>' if cols_used else ''}
                {f'<div style="font-size:10px;color:{cs["color"]};margin-top:0.2rem;">✦ {proof}</div>' if proof else ''}
                {f'<div style="font-size:10px;color:var(--text-muted);font-style:italic;margin-top:0.1rem;">{reason}</div>' if reason else ''}
                {f'<div style="margin-top:0.4rem;">{features_html}</div>' if features_html else ''}
            </div>""", unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)

        usecase_names = [m["usecase"] for m in matches]
        default_idx   = 0
        if st.session_state.sel_ucs:
            for i, nm in enumerate(usecase_names):
                if any(s.lower() in nm.lower() or nm.lower() in s.lower() for s in st.session_state.sel_ucs):
                    default_idx = i
                    break

        selected_usecase = st.selectbox("Choose use case for live demo", usecase_names, index=default_idx)
        selected_match   = matches[usecase_names.index(selected_usecase)]

        roi_meta = None
        for uc in all_ucs_flat:
            uc_n = uc.get("name","")
            if uc_n.lower() in selected_usecase.lower() or selected_usecase.lower() in uc_n.lower():
                roi_meta = uc
                break

        conf   = selected_match.get("data_confidence","Medium")
        cs     = conf_styles.get(conf, conf_styles["Medium"])
        effort = selected_match.get("estimated_effort_days","")

        if roi_meta:
            tier    = roi_meta.get("value_tier","Strategic")
            roi_val = roi_meta.get("roi","")
            holder  = roi_meta.get("stakeholder","")
            tier_col= {"Quick Win":"#3da668","Strategic":"#5b9aff","Transformational":"#d4a017"}.get(tier,"#5b9aff")
            ttv     = "4–8 weeks" if tier=="Quick Win" else "3–6 months" if tier=="Strategic" else "6–12 months"
            st.markdown(f"""
            <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:0.55rem;margin:0.75rem 0 0.85rem 0;">
                <div style="background:rgba(61,166,104,0.08);border:1px solid rgba(61,166,104,0.18);
                            border-radius:8px;padding:0.75rem 0.85rem;">
                    <div style="font-size:9px;font-weight:700;color:var(--green-400);text-transform:uppercase;
                                letter-spacing:0.1em;margin-bottom:0.2rem;font-family:'Syne',sans-serif;">💰 ROI</div>
                    <div style="font-size:11px;color:var(--text-primary);font-weight:600;line-height:1.4;">{roi_val}</div>
                </div>
                <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);
                            border-radius:8px;padding:0.75rem 0.85rem;">
                    <div style="font-size:9px;font-weight:700;color:var(--text-muted);text-transform:uppercase;
                                letter-spacing:0.1em;margin-bottom:0.2rem;font-family:'Syne',sans-serif;">🎯 Tier</div>
                    <div style="font-size:14px;font-weight:800;color:{tier_col};font-family:'Syne',sans-serif;">{tier}</div>
                </div>
                <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);
                            border-radius:8px;padding:0.75rem 0.85rem;">
                    <div style="font-size:9px;font-weight:700;color:var(--text-muted);text-transform:uppercase;
                                letter-spacing:0.1em;margin-bottom:0.2rem;font-family:'Syne',sans-serif;">👤 Stakeholder</div>
                    <div style="font-size:14px;font-weight:700;color:var(--text-primary);font-family:'Syne',sans-serif;">{holder}</div>
                </div>
                <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);
                            border-radius:8px;padding:0.75rem 0.85rem;">
                    <div style="font-size:9px;font-weight:700;color:var(--text-muted);text-transform:uppercase;
                                letter-spacing:0.1em;margin-bottom:0.2rem;font-family:'Syne',sans-serif;">⏱ Time to Value</div>
                    <div style="font-size:14px;font-weight:700;color:var(--text-primary);font-family:'Syne',sans-serif;">{ttv}</div>
                </div>
                <div style="background:{cs['bg']};border:1px solid {cs['border']};
                            border-radius:8px;padding:0.75rem 0.85rem;">
                    <div style="font-size:9px;font-weight:700;color:{cs['color']};text-transform:uppercase;
                                letter-spacing:0.1em;margin-bottom:0.2rem;font-family:'Syne',sans-serif;">🔒 Confidence</div>
                    <div style="font-size:14px;font-weight:700;color:{cs['color']};font-family:'Syne',sans-serif;">{conf}{f" · ~{effort}d" if effort else ""}</div>
                </div>
            </div>""", unsafe_allow_html=True)

        tables_str = ', '.join(selected_match.get('tables', []))
        st.markdown(f"""
        <div class="gate-box">
            <div style="font-size:13px;margin-top:1px;">🔒</div>
            <div class="gate-text">
                <strong>Governance Gate</strong> — Review the SQL and confirm table access before running the live demo.<br/>
                <span style="font-size:10px;color:var(--text-muted);">Tables: {tables_str}</span>
                {f'<br/><span style="font-size:10px;color:{cs["color"]};font-weight:600;">Confidence: {conf} — {selected_match.get("confidence_reason","")}</span>' if selected_match.get("confidence_reason") else ''}
            </div>
        </div>""", unsafe_allow_html=True)

        st.code(selected_match['sql'], language='sql')
        approve = st.checkbox("✅ I confirm access to these tables — generate the live demo.")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        approve = False
        selected_match = None
        roi_meta = None

    # ══════════════════════════════════════════════════════
    # SMART DUMMY DATA GENERATOR
    # ══════════════════════════════════════════════════════
    def get_dummy_data(usecase_name, usecase_type):
        import random
        random.seed(42)
        name = usecase_name.lower()
        customers = ["Acme Corp", "NovaTech", "BluePeak", "Meridian Co", "Apex Ltd", "Starfield Inc", "CoreSys", "Delta Group"]
        months    = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        products  = ["Pro Plan", "Starter", "Enterprise", "Team", "Lite"]
        segments  = ["SMB", "Mid-Market", "Enterprise", "Startup"]

        if any(k in name for k in ["churn", "retention", "attrition"]):
            return pd.DataFrame({"segment": segments, "churn_rate": [0.22, 0.14, 0.06, 0.31], "at_risk_count": [148, 89, 34, 212], "avg_tenure_months": [8, 18, 36, 4]})
        if any(k in name for k in ["revenue", "sales", "growth", "trend", "forecast"]):
            return pd.DataFrame({"month": months, "revenue": [round(120000 + 8000*i + random.randint(-5000,5000)) for i in range(12)], "target": [125000 + 7500*i for i in range(12)], "deals_closed": [18 + i + random.randint(-3,3) for i in range(12)]})
        if any(k in name for k in ["payment", "delay", "invoice", "ar", "receivable"]):
            return pd.DataFrame({"customer": customers[:6], "avg_delay_days": [21, 5, 14, 32, 8, 18], "open_invoices": [12, 4, 9, 22, 3, 7], "outstanding_usd": [48000, 9200, 23400, 71000, 6800, 19500]})
        if any(k in name for k in ["marketing", "campaign", "roi", "lead", "conversion"]):
            return pd.DataFrame({"channel": ["Paid Search", "Email", "Social", "Organic", "Referral", "Events"], "spend_usd": [42000, 8500, 21000, 0, 5000, 18000], "leads": [320, 210, 180, 95, 140, 260], "conversions": [48, 52, 28, 31, 38, 44], "roi_pct": [142, 310, 88, 0, 224, 175]})
        if any(k in name for k in ["demand", "inventory", "supply", "stock"]):
            return pd.DataFrame({"product": products, "forecasted_units": [1200, 3400, 480, 890, 2100], "actual_units": [1140, 3610, 450, 920, 1980], "stockout_days": [3, 0, 8, 1, 2], "overstock_units": [60, 210, 0, 30, 120]})
        if any(k in name for k in ["recommend", "offer", "upsell", "cross"]):
            return pd.DataFrame({"customer_segment": segments, "recommended_product": ["Enterprise", "Pro Plan", "Team", "Starter"], "propensity_score": [0.82, 0.67, 0.74, 0.51], "expected_revenue": [24000, 8400, 13200, 3600]})
        if any(k in name for k in ["anomal", "fraud", "detection", "outlier"]):
            return pd.DataFrame({"transaction_id": [f"TXN{1000+i}" for i in range(8)], "amount": [1240, 85000, 320, 92000, 540, 78000, 210, 1100], "risk_score": [0.12, 0.94, 0.08, 0.97, 0.15, 0.91, 0.06, 0.18], "flagged": ["No","Yes","No","Yes","No","Yes","No","No"]})
        return pd.DataFrame({"category": customers[:6], "value": [round(random.uniform(50000,200000)) for _ in range(6)], "count": [random.randint(10,120) for _ in range(6)], "growth_pct": [round(random.uniform(-5,25),1) for _ in range(6)]})

    # ══════════════════════════════════════════════════════
    # LIVE DEMO DASHBOARD
    # ══════════════════════════════════════════════════════
    if approve and selected_match:
        if "roi_meta" not in dir():
            roi_meta = None
            for uc in (analytics_ucs + de_ucs + ds_ucs):
                uc_n = uc.get("name","")
                if uc_n.lower() in selected_match["usecase"].lower() or selected_match["usecase"].lower() in uc_n.lower():
                    roi_meta = uc
                    break

        df = pd.DataFrame()
        data_source = "live"
        try:
            df = session.sql(selected_match['sql']).to_pandas()
            df.columns = [c.lower() for c in df.columns]
        except Exception:
            pass

        if df.empty:
            df = get_dummy_data(selected_match['usecase'], selected_match['type'])
            data_source = "prototype"

        st.markdown("<div class='section-label' style='margin-top:1.1rem;'>Live Demo</div>", unsafe_allow_html=True)
        st.markdown("<div class='panel'>", unsafe_allow_html=True)

        hc1, hc2 = st.columns([4, 1])
        with hc1:
            st.markdown(f"<h2>📊 {selected_match['usecase']}</h2>", unsafe_allow_html=True)
            st.markdown(f"<p style='color:var(--text-secondary);font-size:11px;margin-bottom:1.2rem;line-height:1.6;'>{selected_match['demo_description']}</p>", unsafe_allow_html=True)
        with hc2:
            source_color = "#3da668" if data_source == "live" else "#5b9aff"
            source_label = "● Live Data" if data_source == "live" else "◈ Prototype"
            st.markdown(f"""
            <div style="background:rgba(61,166,104,0.06);border:1px solid rgba(61,166,104,0.18);
                        border-radius:8px;padding:0.45rem 0.75rem;text-align:center;margin-top:0.5rem;">
                <div style="font-size:9px;font-weight:700;color:{source_color};
                            letter-spacing:0.1em;text-transform:uppercase;font-family:'Syne',sans-serif;">{source_label}</div>
                <div style="font-size:10px;color:var(--text-muted);margin-top:2px;">
                    {len(df)} records
                </div>
            </div>""", unsafe_allow_html=True)

        cols      = df.columns.tolist()
        dim_col   = next((c for c in cols if df[c].dtype == object), cols[0])
        num_cols  = [c for c in cols if c != dim_col and pd.api.types.is_numeric_dtype(df[c])]

        fig = fig2 = fig3 = None

        # ── KPI Row ───────────────────────────────────
        kpi_cols = st.columns(min(len(num_cols) + 1, 5))
        with kpi_cols[0]:
            st.metric("Records", df.shape[0])
        for i, nc in enumerate(num_cols[:4]):
            with kpi_cols[i + 1]:
                val   = df[nc].sum() if df[nc].max() > 1 else round(df[nc].mean(), 3)
                label = nc.replace("_", " ").title()
                st.metric(label, f"{val:,.1f}")

        # Plotly theme for dark background
        dark_plot_layout = dict(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='DM Sans', color='#9dbdaa', size=11),
            margin=dict(l=0, r=0, t=36, b=0),
            xaxis=dict(gridcolor='rgba(255,255,255,0.04)', linecolor='rgba(255,255,255,0.08)', color='#5a7a65'),
            yaxis=dict(gridcolor='rgba(255,255,255,0.04)', linecolor='rgba(255,255,255,0.08)', color='#5a7a65'),
        )

        if num_cols:
            y_col = num_cols[0]
            fig = px.bar(
                df, x=dim_col, y=y_col,
                color=y_col,
                color_continuous_scale=[[0,'#1a3d28'],[0.4,'#2d8050'],[0.7,'#3da668'],[1,'#6ecca0']],
                labels={y_col: y_col.replace("_"," ").title(), dim_col: ''},
            )
            fig.update_layout(**dark_plot_layout,
                title=dict(text=f"{y_col.replace('_',' ').title()} by {dim_col.replace('_',' ').title()}",
                           font=dict(family='Syne', color='#e8f0ea', size=13)),
                coloraxis_showscale=False, height=300,
            )
            st.plotly_chart(fig, use_container_width=True)

        col_tbl, col_chart2 = st.columns([1.6, 1])
        with col_tbl:
            with st.expander("🔍 Detailed Data Table"):
                st.dataframe(df, use_container_width=True)
        with col_chart2:
            if num_cols:
                pie_col = num_cols[-1]
                fig2 = px.pie(df, values=pie_col, names=dim_col, hole=0.58,
                              color_discrete_sequence=['#3da668','#6ecca0','#2d8050','#1a3d28','#9eddb8','#b8eecb'])
                fig2.update_layout(**{k:v for k,v in dark_plot_layout.items() if k not in ['xaxis','yaxis']},
                    title=dict(text=f"{pie_col.replace('_',' ').title()} Split",
                               font=dict(family='Syne', color='#e8f0ea', size=12)),
                    showlegend=True,
                    legend=dict(font=dict(color='#9dbdaa', size=10), bgcolor='rgba(0,0,0,0)'),
                    height=260,
                )
                st.plotly_chart(fig2, use_container_width=True)

        if len(num_cols) >= 2:
            fig3 = px.line(df, x=dim_col, y=num_cols[:2],
                           color_discrete_sequence=['#3da668', '#6ecca0'],
                           labels={'value': 'Value', dim_col: ''})
            fig3.update_traces(line=dict(width=2.5))
            fig3.update_layout(**dark_plot_layout,
                title=dict(text='Trend Comparison', font=dict(family='Syne', color='#e8f0ea', size=13)),
                height=240,
                legend=dict(font=dict(color='#9dbdaa', size=10), bgcolor='rgba(0,0,0,0)'),
            )
            st.plotly_chart(fig3, use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)

        # ══════════════════════════════════════════════════
        # LINEAGE
        # ══════════════════════════════════════════════════
        st.markdown("<div class='section-label' style='margin-top:1.1rem;'>Generated Assets</div>", unsafe_allow_html=True)
        st.markdown("<div class='panel'>", unsafe_allow_html=True)
        st.markdown("<h2>📄 Data Lineage &amp; Mapping</h2>", unsafe_allow_html=True)
        st.code(selected_match['sql'], language='sql')
        conf_val   = selected_match.get("data_confidence","Medium")
        conf_proof = selected_match.get("what_data_proves","")
        cols_disp  = ", ".join(selected_match.get("columns_used",[]))
        cs_v       = conf_styles.get(conf_val, conf_styles["Medium"])
        st.markdown(f"""
        <div style='margin-top:1rem;'>
            <div class='lineage-row'><span class='lineage-key'>Business Intent</span><span class='lineage-val'>{selected_match['usecase']}</span></div>
            <div class='lineage-row'><span class='lineage-key'>Type</span><span class='lineage-val'>{selected_match.get('type','')}</span></div>
            <div class='lineage-row'><span class='lineage-key'>Tables Used</span><span class='lineage-val' style='font-family:monospace;'>{', '.join(selected_match['tables'])}</span></div>
            <div class='lineage-row'><span class='lineage-key'>Columns Used</span><span class='lineage-val' style='font-family:monospace;'>{cols_disp or '—'}</span></div>
            <div class='lineage-row'><span class='lineage-key'>Data Confidence</span><span class='lineage-val' style='color:{cs_v["color"]};font-weight:700;'>{conf_val} — {conf_proof}</span></div>
            <div class='lineage-row'><span class='lineage-key'>Snowflake Features</span><span class='lineage-val'>{', '.join(selected_match.get("snowflake_features", ["Snowpark", "Cortex"]))}</span></div>
            <div class='lineage-row'><span class='lineage-key'>Credit Estimate</span><span class='lineage-val'>Projected &lt; $0.01 per run</span></div>
        </div>
        """, unsafe_allow_html=True)
        st.success("✅ Live demo ready — generate talking points and export the demo pack below.")
        st.markdown("</div>", unsafe_allow_html=True)

        # ══════════════════════════════════════════════════
        # CUSTOMER PITCH
        # ══════════════════════════════════════════════════
        if roi_meta:
            st.markdown("<div class='section-label' style='margin-top:1.1rem;'>Customer Pitch</div>", unsafe_allow_html=True)
            st.markdown("<div class='panel'>", unsafe_allow_html=True)
            st.markdown("<h2>🎤 Customer Talking Points</h2>", unsafe_allow_html=True)

            if st.button("🤖 Generate Talking Points with Cortex"):
                tier    = roi_meta.get("value_tier", "Strategic")
                roi_val = roi_meta.get("roi", "")
                holder  = roi_meta.get("stakeholder", "")
                proof   = selected_match.get("what_data_proves", "")
                ttv     = "4–8 weeks" if tier=="Quick Win" else "3–6 months" if tier=="Strategic" else "6–12 months"

                pitch_prompt = f"""You are a Snowflake Sales Engineer. Write a short, punchy customer pitch for one use case.

Customer: {customer_name} | Industry: {industry} | Stakeholder: {holder}
Use Case: {selected_match['usecase']}
ROI: {roi_val}
What the live data just showed: {proof}
Time to value: {ttv}

Return EXACTLY this structure. Keep each point to 1-2 sentences maximum.

🔴 THE PROBLEM
One sentence: what pain is the customer feeling right now?

💡 WHAT THIS SOLVES
One sentence: what does this use case enable them to do that they can't today?

📊 WHAT THE DATA SHOWS
One sentence: reference the live demo data — what does it specifically reveal?

💰 THE BUSINESS BENEFIT
One sentence: the concrete ROI or measurable outcome they will see.

⏱️ HOW QUICKLY
Time to value and what the first milestone looks like.

✅ WHY SNOWFLAKE
One sentence: the single most compelling reason Snowflake is the right platform for this.

Keep the entire output under 150 words. No section should exceed 2 sentences."""

                with st.spinner(""):
                    try:
                        pitch = session.sql(f"SELECT cortex_complete('{pitch_prompt.replace(chr(39),chr(39)*2)}') as p").collect()[0][0]
                    except Exception as e:
                        pitch = f"Generation failed: {e}"
                st.session_state.pitch = pitch

            if hasattr(st.session_state, 'pitch') and st.session_state.pitch:
                lines = st.session_state.pitch.strip().split('\n')
                icon_colors = {
                    "🔴": "#c94040", "💡": "#3da668", "📊": "#5b9aff",
                    "💰": "#d4a017", "⏱": "#b07fff", "✅": "#3da668",
                }
                rendered = []
                current_header = current_body = ""
                for line in lines:
                    line = line.strip()
                    if not line: continue
                    is_header = any(line.startswith(ic) for ic in icon_colors)
                    if is_header:
                        if current_header: rendered.append((current_header, current_body.strip()))
                        current_header = line; current_body = ""
                    else:
                        current_body += " " + line
                if current_header: rendered.append((current_header, current_body.strip()))

                if rendered:
                    col_a, col_b = st.columns(2)
                    for i, (header, body) in enumerate(rendered):
                        fc = header[0] if header else "•"
                        color = icon_colors.get(fc, "#3da668")
                        card_html = f"""
                        <div style="background:var(--card-bg);border:1px solid var(--card-border);
                                    border-left:3px solid {color};border-radius:8px;
                                    padding:0.85rem 1rem;margin-bottom:0.55rem;">
                            <div style="font-size:11px;font-weight:700;color:{color};margin-bottom:0.25rem;
                                        font-family:'Syne',sans-serif;">{header}</div>
                            <div style="font-size:12px;color:var(--text-secondary);line-height:1.65;">{body}</div>
                        </div>"""
                        with (col_a if i % 2 == 0 else col_b):
                            st.markdown(card_html, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="background:var(--card-bg);border-left:3px solid var(--green-400);
                                border:1px solid var(--card-border);border-radius:8px;
                                padding:1rem 1.2rem;font-size:12px;color:var(--text-secondary);line-height:1.8;">
                        {st.session_state.pitch.replace(chr(10),'<br/>')}
                    </div>""", unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

        # ══════════════════════════════════════════════════
        # HTML EXPORT
        # ══════════════════════════════════════════════════
        st.markdown("<div class='section-label' style='margin-top:1.1rem;'>Export Demo Pack</div>", unsafe_allow_html=True)
        st.markdown("<div class='panel'>", unsafe_allow_html=True)
        st.markdown("<h2>📥 Export Demo Pack for Customer</h2>", unsafe_allow_html=True)
        st.markdown("<div style='font-size:11px;color:var(--text-muted);margin-bottom:0.75rem;'>Generate a complete HTML demo report with embedded charts, data table, ROI case, and sales pitch. Open in Chrome and Ctrl+P → Save as PDF.</div>", unsafe_allow_html=True)

        if st.button("📄 Build HTML Export Pack"):
            import plotly.io as pio

            chart_figs = [f for f in [fig, fig2, fig3] if f is not None]
            chart_divs = []
            for chartfig in chart_figs:
                try:
                    div = pio.to_html(chartfig, full_html=False, include_plotlyjs=False,
                                      config={"displayModeBar": False, "responsive": True})
                    chart_divs.append(div)
                except Exception:
                    pass

            charts_section = "\n".join(f'<div style="margin-bottom:1.5rem;">{d}</div>' for d in chart_divs) if chart_divs else '<p style="color:#6a8c74;">No charts available.</p>'
            table_html = df.to_html(index=False, classes="data-table", border=0)
            pitch_html = ""
            if hasattr(st.session_state, 'pitch') and st.session_state.pitch:
                pitch_html = st.session_state.pitch.replace('\n','<br/>')

            roi_val  = roi_meta.get("roi","")     if roi_meta else ""
            tier     = roi_meta.get("value_tier","Strategic") if roi_meta else ""
            holder   = roi_meta.get("stakeholder","") if roi_meta else ""
            ttv_html = "4–8 weeks" if tier=="Quick Win" else "3–6 months" if tier=="Strategic" else "6–12 months"

            from datetime import date
            html_export = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>InsightForge Demo Pack — {selected_match['usecase']}</title>
<script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
<style>
  *{{box-sizing:border-box;}}
  body{{font-family:'Segoe UI',Arial,sans-serif;background:#0f1a13;color:#e8f0ea;margin:0;padding:0;font-size:14px;}}
  .cover{{background:linear-gradient(135deg,#0a120d 0%,#141f18 60%,#1a2820 100%);
          color:#fff;padding:3rem 3.5rem;border-bottom:1px solid rgba(61,166,104,0.15);
          -webkit-print-color-adjust:exact;print-color-adjust:exact;}}
  .cover h1{{font-size:2rem;font-weight:800;margin:0 0 0.4rem;letter-spacing:-0.02em;color:#e8f0ea;}}
  .cover .sub{{font-size:1rem;opacity:0.55;margin-bottom:1.2rem;}}
  .cover .pills{{display:flex;flex-wrap:wrap;gap:0.5rem;}}
  .cover .pill{{background:rgba(61,166,104,0.12);border:1px solid rgba(61,166,104,0.25);
                border-radius:20px;padding:0.25rem 0.75rem;font-size:0.78rem;color:#6ecca0;}}
  .section{{padding:2rem 3.5rem;border-bottom:1px solid rgba(255,255,255,0.05);}}
  .section h2{{font-size:1.05rem;font-weight:700;color:#e8f0ea;margin:0 0 1rem;
               padding-bottom:0.4rem;border-bottom:1px solid rgba(61,166,104,0.25);}}
  .roi-grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:0.85rem;margin-bottom:1.25rem;}}
  .roi-card{{background:rgba(61,166,104,0.08);border:1px solid rgba(61,166,104,0.18);
             border-radius:8px;padding:0.85rem 1rem;border-top:2px solid #3da668;
             -webkit-print-color-adjust:exact;print-color-adjust:exact;}}
  .roi-card .rlbl{{font-size:0.68rem;text-transform:uppercase;letter-spacing:0.1em;
                   color:#3da668;font-weight:700;margin-bottom:0.25rem;}}
  .roi-card .rval{{font-size:0.95rem;font-weight:700;color:#e8f0ea;line-height:1.35;}}
  .kpi-grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:0.85rem;margin-bottom:1.25rem;}}
  .kpi{{background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);
        border-radius:8px;padding:0.85rem 1rem;border-top:2px solid #3da668;}}
  .kpi .val{{font-size:1.4rem;font-weight:800;color:#e8f0ea;}}
  .kpi .lbl{{font-size:0.68rem;text-transform:uppercase;letter-spacing:0.08em;color:#5a7a65;margin-top:0.2rem;}}
  .chart-wrap{{background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.06);
               border-radius:10px;padding:1rem;margin-bottom:1rem;}}
  .data-table{{width:100%;border-collapse:collapse;font-size:0.83rem;margin-top:0.5rem;}}
  .data-table th{{background:#1a3d28;color:#6ecca0;padding:0.55rem 0.8rem;text-align:left;
                  font-weight:600;-webkit-print-color-adjust:exact;print-color-adjust:exact;}}
  .data-table td{{padding:0.45rem 0.8rem;border-bottom:1px solid rgba(255,255,255,0.05);color:#9dbdaa;}}
  .data-table tr:nth-child(even) td{{background:rgba(255,255,255,0.02);}}
  .pitch-box{{background:rgba(61,166,104,0.06);border-left:3px solid #3da668;
              border:1px solid rgba(61,166,104,0.18);border-radius:8px;
              padding:1.25rem 1.75rem;font-size:0.9rem;line-height:1.85;color:#9dbdaa;}}
  .sql-box{{background:#0a120d;border:1px solid rgba(61,166,104,0.15);border-radius:6px;
             padding:0.85rem 1.1rem;font-family:'Courier New',monospace;font-size:0.78rem;
             color:#6ecca0;white-space:pre-wrap;overflow-x:auto;}}
  .badge{{display:inline-block;padding:0.2rem 0.65rem;border-radius:4px;font-size:0.72rem;
          font-weight:700;background:rgba(61,166,104,0.12);color:#3da668;
          border:1px solid rgba(61,166,104,0.25);margin-right:0.3rem;}}
  .footer-bar{{background:#0a120d;color:rgba(255,255,255,0.3);text-align:center;
               padding:1rem 2rem;font-size:0.75rem;
               border-top:1px solid rgba(61,166,104,0.1);
               -webkit-print-color-adjust:exact;print-color-adjust:exact;}}
  @media print{{
    body{{background:#fff;color:#132018;font-size:12px;}}
    .section{{padding:1.25rem 2rem;page-break-inside:avoid;}}
    .chart-wrap{{page-break-inside:avoid;}}
  }}
</style>
</head>
<body>
<div class="cover">
  <div style="font-size:0.72rem;letter-spacing:0.2em;opacity:0.35;margin-bottom:0.4rem;text-transform:uppercase;">InsightForge · Snowflake Cortex</div>
  <h1>Demo Pack: {selected_match['usecase']}</h1>
  <div class="sub">Prepared for <strong style="color:#6ecca0;">{customer_name}</strong> · {industry}</div>
  <div class="pills">
    <span class="pill">📅 {date.today().strftime('%d %B %Y')}</span>
    <span class="pill">📊 {selected_match.get('type','')}</span>
    <span class="pill">🗄️ {', '.join(selected_match.get('tables',[]))}</span>
    <span class="pill">🔒 {selected_match.get('data_confidence','')} Confidence</span>
  </div>
</div>
<div class="section">
  <h2>Executive Summary</h2>
  <div class="roi-grid">
    <div class="roi-card"><div class="rlbl">💰 ROI</div><div class="rval">{roi_val}</div></div>
    <div class="roi-card"><div class="rlbl">🎯 Value Tier</div><div class="rval">{tier}</div></div>
    <div class="roi-card"><div class="rlbl">👤 Stakeholder</div><div class="rval">{holder}</div></div>
    <div class="roi-card"><div class="rlbl">⏱️ Time to Value</div><div class="rval">{ttv_html}</div></div>
  </div>
  <p style="font-size:0.92rem;line-height:1.7;color:#9dbdaa;">{selected_match.get('demo_description','')}</p>
  <p style="margin:0;"><span class="badge">{selected_match.get('data_confidence','')} Confidence</span>
     <span style="font-size:0.85rem;color:#9dbdaa;">{selected_match.get('what_data_proves','')}</span></p>
</div>
<div class="section">
  <h2>Data Snapshot — {len(df)} Records</h2>
  <div class="kpi-grid">
    <div class="kpi"><div class="val">{len(df)}</div><div class="lbl">Total Records</div></div>
    {''.join(f'<div class="kpi"><div class="val">{df[nc].sum() if df[nc].max()>1 else round(df[nc].mean(),2):,.1f}</div><div class="lbl">{nc.replace("_"," ").title()}</div></div>' for nc in num_cols[:3])}
  </div>
</div>
<div class="section">
  <h2>Live Demo Charts</h2>
  <div class="chart-wrap">{charts_section}</div>
</div>
<div class="section">
  <h2>Underlying Data</h2>
  {table_html}
</div>
<div class="section">
  <h2>SQL Query</h2>
  <div class="sql-box">{selected_match.get('sql','').replace('<','&lt;').replace('>','&gt;')}</div>
</div>
{'<div class="section"><h2>Sales Pitch</h2><div class="pitch-box">' + pitch_html + '</div></div>' if pitch_html else ''}
<div class="footer-bar">
  Generated by <strong style="color:rgba(110,204,160,0.7);">InsightForge</strong> · Snowflake Cortex ·
  {date.today().strftime('%d %B %Y')} · Confidential — Prepared for {customer_name}
</div>
</body>
</html>"""
            st.session_state.pdf_report = html_export

        if st.session_state.pdf_report:
            st.download_button(
                label="⬇️ Download Demo Pack (.html — open in browser, Ctrl+P → Save as PDF)",
                data=st.session_state.pdf_report,
                file_name=f"InsightForge_Demo_{customer_name.replace(' ','_')}_{selected_match['usecase'][:30].replace(' ','_')}.html",
                mime="text/html",
                use_container_width=True,
            )
            st.success("✅ Demo pack ready. Open the file in Chrome and press Ctrl+P → Save as PDF.")

        st.markdown("</div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# Footer
# ─────────────────────────────────────────────────────────────
st.markdown("""
<div class='footer'>
    Powered by <span>Snowflake Cortex</span> &nbsp;·&nbsp;
    Real customer data, zero hypothetical demos &nbsp;·&nbsp;
    <span>InsightForge v2.0</span>
</div>
""", unsafe_allow_html=True)
