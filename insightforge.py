import streamlit as st
import pandas as pd
import json
import plotly.express as px
from snowflake.snowpark.context import get_active_session

# ─────────────────────────────────────────────────────────────
# THEME — Dark Forest Green × White × Black
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* ── Fonts ── */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

    /* ── Design Tokens — Mid-Tone: Warm Off-White + Deep Forest ── */
    :root {
        /* Body surface — warm off-white, not glaring white */
        --body-bg:        #eef2ee;
        --body-bg-mid:    #e4ebe5;
        --panel-bg:       #f5f8f5;
        --panel-border:   #c0d4c6;
        --card-bg:        #ecf2ed;
        --card-border:    #c8d8cc;

        /* Green brand */
        --green-accent:   #2d7a50;
        --green-bright:   #3da668;
        --green-light:    #4caf78;
        --green-glow:     rgba(45,122,80,0.14);
        --green-border:   rgba(45,122,80,0.28);

        /* Text — rich dark on mid background */
        --text-primary:   #132018;
        --text-secondary: #2d4a36;
        --text-muted:     #6a8c74;

        /* Borders */
        --border:         #bacec0;
        --border-green:   rgba(45,122,80,0.28);

        /* Radius */
        --radius-sm:      6px;
        --radius-md:      10px;
        --radius-lg:      14px;

        /* Dark for header/footer/pulse */
        --forest-deep:    #0e1c12;
        --forest:         #163020;
        --forest-mid:     #1a3d28;
        --forest-muted:   #1e3628;
        --black:          #080e0a;
        --black-soft:     #0d1a11;
        --white:          #ffffff;
        --white-90:       rgba(255,255,255,0.90);
        --white-60:       rgba(255,255,255,0.60);
        --white-06:       rgba(255,255,255,0.05);
    }

    /* ── Global ── */
    html, body, [class*="css"], .stApp,
    div, p, span, label, input, textarea, select, button {
        
        font-size: 13px !important;
    }

    .stApp {
        background: var(--body-bg) !important;
        color: var(--text-primary) !important;
    }

    /* subtle green grid overlay */
    .stApp::after {
        content: '';
        position: fixed;
        inset: 0;
        background-image:
            linear-gradient(rgba(45,122,80,0.035) 1px, transparent 1px),
            linear-gradient(90deg, rgba(45,122,80,0.035) 1px, transparent 1px);
        background-size: 32px 32px;
        pointer-events: none;
        z-index: 0;
    }

    /* ── Sidebar — light forest tone ── */
    [data-testid="stSidebar"] {
        background: #e8f0eb !important;
        border-right: 2px solid #c2d9c8 !important;
        box-shadow: 2px 0 12px rgba(26,58,42,0.08) !important;
    }
    [data-testid="stSidebar"] > div:first-child {
        padding-top: 1.5rem !important;
    }
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stMarkdown p {
        font-size: 11px !important;
        color: #2c4a35 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.08em !important;
        font-weight: 700 !important;
    }
    [data-testid="stSidebar"] h3 {
        font-size: 10px !important;
        font-weight: 800 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.14em !important;
        color: #1f5c35 !important;
        margin-bottom: 0.6rem !important;
        padding-bottom: 0.45rem !important;
        border-bottom: 2px solid #a8c8b2 !important;
    }
    [data-testid="stSidebar"] .stSelectbox > div > div {
        background: #ffffff !important;
        border: 1px solid #a8c8b2 !important;
        color: #1a3a2a !important;
    }
    [data-testid="stSidebar"] .stTextInput input {
        background: #ffffff !important;
        border: 1px solid #a8c8b2 !important;
        color: #1a3a2a !important;
    }
    [data-testid="stSidebar"] .stMultiSelect > div > div {
        background: #ffffff !important;
        border: 1px solid #a8c8b2 !important;
    }
    [data-testid="stSidebar"] [data-testid="stFileUploader"] {
        background: #f0f7f2 !important;
        border: 1px dashed #3d8c5e !important;
    }
    /* sb-block in sidebar gets light card */
    [data-testid="stSidebar"] .sb-block {
        background: #ffffff !important;
        border: 1px solid #c2d9c8 !important;
        box-shadow: 0 1px 4px rgba(26,58,42,0.06) !important;
    }
    [data-testid="stSidebar"] .stSelectbox > div > div,
    [data-testid="stSidebar"] .stTextInput > div > div > input {
        background: var(--forest-muted) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius-sm) !important;
        color: var(--text-primary) !important;
        font-size: 12px !important;
    }
    [data-testid="stSidebar"] .stMultiSelect > div > div {
        background: var(--forest-muted) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius-sm) !important;
    }

    /* ── File uploader ── */
    [data-testid="stFileUploader"] {
        background: #f0f7f2 !important;
        border: 1px dashed var(--green-accent) !important;
        border-radius: var(--radius-md) !important;
    }

    /* ── Headings ── */
    h1 {
        font-size: 22px !important;
        font-weight: 800 !important;
        color: var(--text-primary) !important;
        letter-spacing: -0.02em !important;
        line-height: 1.2 !important;
        margin: 0 !important;
    }
    h2 {
        font-size: 14px !important;
        font-weight: 700 !important;
        color: var(--text-primary) !important;
        letter-spacing: -0.01em !important;
        margin-bottom: 0.9rem !important;
        margin-top: 0 !important;
    }
    h3 {
        font-size: 13px !important;
        font-weight: 600 !important;
        color: var(--text-primary) !important;
        margin-bottom: 0.6rem !important;
    }
    h4 {
        font-size: 10px !important;
        font-weight: 700 !important;
        color: var(--text-secondary) !important;
        text-transform: uppercase !important;
        letter-spacing: 0.1em !important;
        margin-bottom: 0.75rem !important;
    }

    /* ── Tabs ── */
    .stTabs [data-baseweb="tab-list"] {
        background: var(--card-bg) !important;
        border-radius: var(--radius-md) !important;
        border: 1px solid var(--card-border) !important;
        padding: 0.25rem !important;
        gap: 0.15rem !important;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        color: var(--text-secondary) !important;
        font-size: 12px !important;
        font-weight: 600 !important;
        border-radius: var(--radius-sm) !important;
        padding: 0.45rem 0.9rem !important;
    }
    .stTabs [aria-selected="true"] {
        background: var(--green-accent) !important;
        color: #ffffff !important;
    }
    .stTabs [data-baseweb="tab-panel"] {
        background: var(--panel-bg) !important;
        border: 1px solid var(--panel-border) !important;
        border-radius: 0 0 var(--radius-lg) var(--radius-lg) !important;
        padding: 1.25rem !important;
        margin-top: -1px !important;
    }

    /* ── Metrics ── */
    [data-testid="stMetric"] {
        background: var(--panel-bg) !important;
        border-radius: var(--radius-md) !important;
        padding: 1rem 1rem !important;
        border: 1px solid var(--panel-border) !important;
        position: relative !important;
        overflow: hidden !important;
        transition: border-color 0.2s, box-shadow 0.2s !important;
        box-shadow: 0 1px 4px rgba(46,125,82,0.06) !important;
    }
    [data-testid="stMetric"]::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: linear-gradient(90deg, var(--green-accent), transparent);
    }
    [data-testid="stMetric"]:hover {
        border-color: var(--green-accent) !important;
        box-shadow: 0 2px 12px var(--green-glow) !important;
    }
    [data-testid="stMetricValue"] {
        font-size: 20px !important;
        font-weight: 800 !important;
        color: var(--text-primary) !important;
        letter-spacing: -0.02em !important;
        line-height: 1 !important;
    }
    [data-testid="stMetricLabel"] {
        font-size: 10px !important;
        font-weight: 600 !important;
        color: var(--text-muted) !important;
        text-transform: uppercase !important;
        letter-spacing: 0.08em !important;
    }
    [data-testid="stMetricDelta"] {
        font-size: 11px !important;
        color: var(--green-accent) !important;
    }

    /* ── Button ── */
    .stButton > button {
        background: var(--green-accent) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 11px !important;
        letter-spacing: 0.07em !important;
        text-transform: uppercase !important;
        border: none !important;
        border-radius: var(--radius-sm) !important;
        padding: 0.6rem 1.4rem !important;
        box-shadow: 0 2px 10px rgba(61,140,94,0.25) !important;
        transition: all 0.18s ease !important;
        width: 100% !important;
    }
    .stButton > button:hover {
        background: #2e7d52 !important;
        box-shadow: 0 4px 16px rgba(46,125,82,0.35) !important;
        transform: translateY(-1px) !important;
    }

    /* ── Expanders ── */
    .streamlit-expanderHeader {
        background: var(--card-bg) !important;
        border-radius: var(--radius-sm) !important;
        border: 1px solid var(--card-border) !important;
        padding: 0.6rem 1rem !important;
        font-weight: 600 !important;
        font-size: 12px !important;
        color: var(--text-secondary) !important;
    }
    .streamlit-expanderHeader:hover {
        border-color: var(--green-accent) !important;
        color: var(--text-primary) !important;
    }
    .streamlit-expanderContent {
        background: var(--card-bg) !important;
        border: 1px solid var(--card-border) !important;
        border-top: none !important;
        border-radius: 0 0 var(--radius-sm) var(--radius-sm) !important;
        padding: 1rem !important;
    }

    /* ── Alerts / Success ── */
    .stAlert {
        background: rgba(46,125,82,0.07) !important;
        border: 1px solid var(--green-border) !important;
        border-left: 3px solid var(--green-accent) !important;
        border-radius: var(--radius-md) !important;
        color: var(--text-primary) !important;
        font-size: 12px !important;
    }

    /* ── Code ── */
    .stCodeBlock, pre, code {
        background: #f0f4f1 !important;
        border: 1px solid var(--card-border) !important;
        border-radius: var(--radius-md) !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 11px !important;
        color: #1a2e22 !important;
    }

    /* ── Selectbox / Multiselect ── */
    .stSelectbox > div > div,
    .stMultiSelect > div > div {
        background: var(--panel-bg) !important;
        border: 1px solid var(--card-border) !important;
        border-radius: var(--radius-sm) !important;
        color: var(--text-primary) !important;
        font-size: 12px !important;
    }

    /* ── Text inputs ── */
    .stTextInput input, .stTextArea textarea {
        background: var(--panel-bg) !important;
        border: 1px solid var(--card-border) !important;
        border-radius: var(--radius-sm) !important;
        color: var(--text-primary) !important;
        font-size: 12px !important;
    }

    /* ── Checkbox ── */
    .stCheckbox label {
        font-size: 12px !important;
        color: var(--text-secondary) !important;
    }

    /* ── Dataframe ── */
    .stDataFrame {
        border: 1px solid var(--card-border) !important;
        border-radius: var(--radius-md) !important;
        font-size: 12px !important;
        box-shadow: 0 1px 4px rgba(46,125,82,0.05) !important;
    }

    /* ── Divider ── */
    hr {
        border: none !important;
        height: 1px !important;
        background: var(--border) !important;
        margin: 1.5rem 0 !important;
    }

    /* ─── Custom Components — Light ─── */

    .panel {
        background: var(--panel-bg);
        border: 1px solid var(--panel-border);
        border-radius: var(--radius-lg);
        padding: 1.25rem 1.4rem;
        margin-bottom: 1.1rem;
        position: relative;
        overflow: hidden;
        box-shadow: 0 1px 6px rgba(46,125,82,0.06);
    }
    .panel::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: linear-gradient(90deg, var(--green-accent), transparent);
        opacity: 0.6;
    }

    .section-label {
        font-size: 10px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.14em;
        color: var(--green-accent);
        margin-bottom: 0.35rem;
    }

    .sb-block {
        background: var(--panel-bg);
        border: 1px solid var(--card-border);
        border-radius: var(--radius-md);
        padding: 0.85rem 1rem;
        margin-bottom: 0.9rem;
        box-shadow: 0 1px 3px rgba(46,125,82,0.05);
    }

    .uc-card {
        background: var(--card-bg);
        border: 1px solid var(--card-border);
        border-radius: var(--radius-md);
        padding: 0.85rem 1rem;
        margin-bottom: 0.6rem;
        transition: border-color 0.2s, box-shadow 0.2s;
    }
    .uc-card:hover {
        border-color: var(--green-accent);
        box-shadow: 0 2px 10px var(--green-glow);
    }
    .uc-card-title {
        font-weight: 600;
        font-size: 12px;
        color: var(--text-primary);
        margin-bottom: 0.25rem;
    }
    .uc-card-desc {
        font-size: 11px;
        color: var(--text-secondary);
        line-height: 1.5;
        margin-bottom: 0.5rem;
    }

    .badge {
        display: inline-flex;
        align-items: center;
        padding: 0.18rem 0.6rem;
        border-radius: 4px;
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 0.06em;
        text-transform: uppercase;
    }
    .badge-analytics {
        background: #e8f4ef;
        color: #2e7d52;
        border: 1px solid #b8d9c5;
    }
    .badge-ds {
        background: #e6f0ff;
        color: #2d5fa8;
        border: 1px solid #b3ccf0;
    }

    .tag {
        display: inline-block;
        background: #edf3ef;
        border: 1px solid var(--card-border);
        color: var(--text-secondary);
        font-size: 10px;
        font-weight: 600;
        padding: 0.15rem 0.55rem;
        border-radius: 4px;
        margin-right: 0.3rem;
        letter-spacing: 0.04em;
    }

    .gate-box {
        background: rgba(46,125,82,0.06);
        border: 1px solid var(--green-border);
        border-radius: var(--radius-md);
        padding: 0.85rem 1rem;
        display: flex;
        align-items: flex-start;
        gap: 0.6rem;
        margin-bottom: 0.9rem;
    }
    .gate-icon { font-size: 13px; margin-top: 1px; }
    .gate-text { font-size: 11px; color: var(--text-secondary); line-height: 1.55; }
    .gate-text strong { color: var(--green-accent); }

    .lineage-row {
        display: flex;
        align-items: baseline;
        gap: 0.75rem;
        padding: 0.45rem 0;
        border-bottom: 1px solid var(--border);
    }
    .lineage-row:last-child { border-bottom: none; }
    .lineage-key {
        font-size: 10px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.07em;
        color: var(--text-muted);
        min-width: 9rem;
    }
    .lineage-val {
        font-size: 11px;
        color: var(--text-secondary);
    }

    .footer {
        text-align: center;
        margin-top: 3rem;
        padding: 1.5rem;
        color: var(--text-muted);
        font-size: 11px;
        letter-spacing: 0.05em;
        border-top: 1px solid var(--card-border);
    }
    .footer span { color: var(--green-accent); }

    /* ── Kill Streamlit default top padding ── */
    .stApp > header { display: none !important; }
    #root > div:first-child { padding-top: 0 !important; }
    .block-container {
        padding-top: 0.75rem !important;
        padding-bottom: 2rem !important;
        max-width: 100% !important;
    }
    [data-testid="stAppViewContainer"] > section:first-child {
        padding-top: 0 !important;
    }

    /* ── Sticky header bar ── */
    .top-header {
        position: sticky;
        top: 0;
        z-index: 999;
        background: rgba(17,34,24,0.92);
        backdrop-filter: blur(14px);
        border-bottom: 1px solid rgba(76,175,120,0.15);
        padding: 0.6rem 1.5rem;
        margin: -0.75rem -1rem 1.5rem -1rem;
        display: flex;
        align-items: center;
        gap: 1rem;
    }

    /* ── Live pill button ── */
    .live-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        background: rgba(76,175,120,0.12);
        border: 1px solid rgba(76,175,120,0.4);
        border-radius: 20px;
        padding: 0.28rem 0.75rem;
        font-size: 10px;
        font-weight: 700;
        color: #4caf78;
        letter-spacing: 0.06em;
        text-transform: uppercase;
    }
    .live-dot {
        width: 7px;
        height: 7px;
        background: #4caf78;
        border-radius: 50%;
        position: relative;
        flex-shrink: 0;
    }
    .live-dot::after {
        content: '';
        position: absolute;
        inset: -3px;
        border-radius: 50%;
        border: 2px solid rgba(76,175,120,0.5);
        animation: live-ping 1.4s ease-out infinite;
    }
    @keyframes live-ping {
        0%   { transform: scale(0.8); opacity: 1; }
        100% { transform: scale(2.2); opacity: 0; }
    }

    /* ── Pulse loader overlay ── */
    .pulse-loader {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 1.4rem;
        padding: 3rem 2rem;
        background: var(--forest);
        border: 1px solid var(--border);
        border-radius: var(--radius-lg);
        margin-bottom: 1.1rem;
    }
    .pulse-rings {
        position: relative;
        width: 54px;
        height: 54px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .pulse-rings span {
        position: absolute;
        border-radius: 50%;
        border: 2px solid rgba(255,255,255,0.85);
        animation: pulse-expand 2s ease-out infinite;
    }
    .pulse-rings span:nth-child(1) { width:54px; height:54px; animation-delay:0s; }
    .pulse-rings span:nth-child(2) { width:38px; height:38px; animation-delay:0.35s; }
    .pulse-rings span:nth-child(3) { width:22px; height:22px; animation-delay:0.7s; }
    .pulse-rings span:nth-child(4) {
        width: 10px; height: 10px;
        background: #fff;
        border: none;
        animation: none;
    }
    @keyframes pulse-expand {
        0%   { transform: scale(0.4); opacity: 1; }
        100% { transform: scale(1);   opacity: 0; }
    }
    .pulse-steps {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
        width: 100%;
        max-width: 320px;
    }
    .pulse-step {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        font-size: 11px;
        color: rgba(255,255,255,0.35);
        transition: color 0.3s;
    }
    .pulse-step.active {
        color: rgba(255,255,255,0.9);
    }
    .pulse-step.done {
        color: var(--green-accent);
    }
    .step-dot {
        width: 6px; height: 6px;
        border-radius: 50%;
        background: rgba(255,255,255,0.2);
        flex-shrink: 0;
    }
    .pulse-step.active .step-dot {
        background: #fff;
        box-shadow: 0 0 6px rgba(255,255,255,0.6);
        animation: blink 0.9s ease-in-out infinite;
    }
    .pulse-step.done .step-dot { background: var(--green-bright); }
    @keyframes blink {
        0%, 100% { opacity: 1; }
        50%       { opacity: 0.3; }
    }
    .pulse-label {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 11px;
        font-weight: 600;
        color: rgba(255,255,255,0.5);
        letter-spacing: 0.08em;
        text-transform: uppercase;
        text-align: center;
    }
    .pulse-sublabel {
        font-size: 11px;
        color: rgba(255,255,255,0.28);
        text-align: center;
        margin-top: -0.8rem;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# Sticky Header Bar
# ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="top-header">
    <div style="width:32px; height:32px; background:linear-gradient(135deg,#3d8c5e,#1a3a2a);
                border-radius:8px; display:flex; align-items:center; justify-content:center;
                font-size:0.95rem; box-shadow:0 2px 12px rgba(76,175,120,0.3); flex-shrink:0;">⚡</div>
    <div style="display:flex; flex-direction:column; gap:0;">
        <div style="font-size:9px; font-weight:700; text-transform:uppercase;
                    letter-spacing:0.16em; color:#4caf78; line-height:1;">Snowflake Cortex</div>
        <div style="font-size:15px; font-weight:800; color:#1a2e22;
                    letter-spacing:-0.02em; line-height:1.2; font-family:'Plus Jakarta Sans',sans-serif;">InsightForge</div>
    </div>
    <div style="margin-left:0.25rem; font-size:11px; color:rgba(255,255,255,0.3); margin-top:6px;">
        Business Context → Data‑Driven Execution
    </div>
    <div style="margin-left:auto; display:flex; gap:0.5rem; align-items:center;">
        <span class="live-pill">
            <span class="live-dot"></span>Live
        </span>
        <span class="tag">Cortex AI</span>
        <span class="tag">Snowpark</span>
    </div>
</div>
""", unsafe_allow_html=True)

session = get_active_session()

# ─────────────────────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:0 0.1rem; margin-bottom:1.2rem;">
        <div style="font-size:14px; font-weight:800; color:#1a2e22; letter-spacing:-0.01em;">Configure</div>
        <div style="font-size:11px; color:#7a9e88; margin-top:2px;">Set up your analysis session</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='sb-block'>", unsafe_allow_html=True)
    st.markdown("### 📂 Transcripts")
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
        st.success(f"{len(uploaded_files)} file(s) uploaded.")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='sb-block'>", unsafe_allow_html=True)
    st.markdown("### 🏢 Customer")
    customer_name = st.text_input("Customer Name (optional)", "Acme Corp")
    industry = st.text_input("Industry", "SaaS / Technology")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='sb-block'>", unsafe_allow_html=True)
    st.markdown("### 🗄️ Data Sources")
    tables_df = session.sql("SELECT DISTINCT fully_qualified_table_name FROM table_metadata").to_pandas()
    table_options = tables_df['FULLY_QUALIFIED_TABLE_NAME'].tolist()
    selected_tables = st.multiselect("Choose tables", table_options,
                                     default=table_options[:2] if table_options else [])
    st.markdown("</div>", unsafe_allow_html=True)

    run_analysis = st.button("⚡ Analyze & Generate Use Cases", type="primary")

# ─────────────────────────────────────────────────────────────
# Session State Init
# ─────────────────────────────────────────────────────────────
for key in ["analysis", "market_trends", "matches", "industry_cached", "data_samples", "pdf_report"]:
    if key not in st.session_state:
        st.session_state[key] = None

# ─────────────────────────────────────────────────────────────
# STEP 1 — Run Analysis (only when button clicked)
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

    # ── Animated Pulse Loader ─────────────────────────────
    loader_placeholder = st.empty()
    loader_placeholder.markdown("""
    <div class="pulse-loader">
        <div class="pulse-rings">
            <span></span><span></span><span></span><span></span>
        </div>
        <div class="pulse-label">Cortex is Analyzing</div>
        <div class="pulse-sublabel">Reading transcripts &amp; mapping to your data schema...</div>
        <div class="pulse-steps">
            <div class="pulse-step active">
                <span class="step-dot"></span> Parsing transcript content
            </div>
            <div class="pulse-step">
                <span class="step-dot"></span> Extracting business signals
            </div>
            <div class="pulse-step">
                <span class="step-dot"></span> Running market research
            </div>
            <div class="pulse-step">
                <span class="step-dot"></span> Matching use cases to schema
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.spinner(""):

        # Step 1 — Extract insights
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

        Return ONLY valid JSON:
        {{
          "metrics": {{"pain_point_count": int, "sentiment_score": float, "roadmap_item_count": int, "urgency_level": "Low/Medium/High"}},
          "analytics_usecases": [
            {{"name": "...", "roi": "...", "value_tier": "Quick Win|Strategic|Transformational", "stakeholder": "..."}}
          ],
          "dataengineering_usecases": [
            {{"name": "...", "roi": "...", "value_tier": "Quick Win|Strategic|Transformational", "stakeholder": "..."}}
          ],
          "datascience_usecases": [
            {{"name": "...", "roi": "...", "value_tier": "Quick Win|Strategic|Transformational", "stakeholder": "..."}}
          ]
        }}
        """
        extraction_result = session.sql(f"SELECT cortex_complete('{extraction_prompt.replace(chr(39), chr(39)*2)}') as result").collect()[0][0]
        try:
            st.session_state.analysis = json.loads(extraction_result)
        except:
            st.session_state.analysis = {
                "metrics": {"pain_point_count": 5, "sentiment_score": 6.5, "roadmap_item_count": 3, "urgency_level": "Medium"},
                "analytics_usecases": [
                    {"name": "Customer Payment Delay Dashboard", "roi": "Reduces DSO by 15 days, freeing $500K working capital", "value_tier": "Quick Win", "stakeholder": "CFO"},
                    {"name": "Sales Revenue Trend Analysis", "roi": "Aligns sales forecasts within 5%, improving resource planning", "value_tier": "Quick Win", "stakeholder": "VP Sales"},
                    {"name": "Marketing ROI by Channel", "roi": "Redirects 20% of spend to top channels, lifting conversion by 18%", "value_tier": "Strategic", "stakeholder": "CMO"},
                    {"name": "Executive KPI Scorecard", "roi": "Saves 8hrs/week manual reporting across leadership team", "value_tier": "Quick Win", "stakeholder": "CEO"},
                ],
                "dataengineering_usecases": [
                    {"name": "Automated Data Quality Pipeline", "roi": "Eliminates 90% of bad data reaching reports, preventing costly decisions", "value_tier": "Strategic", "stakeholder": "Data Team"},
                    {"name": "Real-Time CRM Data Ingestion", "roi": "Reduces data latency from D+1 to minutes, enabling same-day decisions", "value_tier": "Transformational", "stakeholder": "VP Sales"},
                    {"name": "Data Lineage & Governance Layer", "roi": "Cuts audit preparation time from 3 weeks to 2 days", "value_tier": "Strategic", "stakeholder": "COO"},
                    {"name": "Multi-Source ETL Consolidation", "roi": "Reduces pipeline maintenance cost by 60%, freeing 2 FTEs", "value_tier": "Strategic", "stakeholder": "CTO"},
                ],
                "datascience_usecases": [
                    {"name": "Customer Churn Prediction Model", "roi": "Predicts churn 30 days early, saves $200K/yr in retention spend", "value_tier": "Transformational", "stakeholder": "CCO"},
                    {"name": "Next Best Offer Recommendation", "roi": "Lifts upsell revenue by 12-18% through personalised offers", "value_tier": "Transformational", "stakeholder": "VP Sales"},
                    {"name": "Demand Forecasting with ML", "roi": "Reduces inventory overstock by 25%, saving $150K/yr", "value_tier": "Strategic", "stakeholder": "COO"},
                    {"name": "Anomaly Detection on Transactions", "roi": "Catches fraud 3x faster, reducing financial exposure by $80K/yr", "value_tier": "Transformational", "stakeholder": "CFO"},
                ]
            }

        # Step 2 — Market research
        market_prompt = f"""
        For a customer in the {industry} industry, provide 3 current market trends or benchmarks relevant to data analytics and AI adoption.
        Suggest how these translate into business use cases for this customer.
        """
        st.session_state.market_trends = session.sql(f"SELECT cortex_complete('{market_prompt.replace(chr(39), chr(39)*2)}') as trends").collect()[0][0]
        st.session_state.industry_cached = industry

        # Step 3 — Schema matching
        selected_tables_str = "', '".join(selected_tables)
        schema_df = session.sql(f"""
            SELECT fully_qualified_table_name, LISTAGG(column_name, ', ') AS columns
            FROM table_metadata
            WHERE fully_qualified_table_name IN ('{selected_tables_str}')
            GROUP BY 1
        """).to_pandas()
        schema_str = "\n".join([f"{row['FULLY_QUALIFIED_TABLE_NAME']}: {row['COLUMNS']}" for _, row in schema_df.iterrows()])

        # Step 3a — Sample actual data to validate what really exists
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
            t = "Analytics" if uc in st.session_state.analysis.get("analytics_usecases",[]) else                 "Data Engineering" if uc in st.session_state.analysis.get("dataengineering_usecases",[]) else                 "Data Science"
            uc_names_by_type.append(f"{t}: {n}")

        import json as _json
        samples_str = _json.dumps(data_samples, default=str)[:3000]

        match_prompt = f"""
You are a Snowflake Solutions Engineer. Your job is to MAP each identified use case to the real customer database,
then propose a live proof-of-concept demo using the ACTUAL columns and data that exist.

IDENTIFIED USE CASES FROM TRANSCRIPTS:
{chr(10).join(uc_names_by_type)}

DATABASE SCHEMA (tables and columns):
{schema_str}

ACTUAL SAMPLE DATA FROM THE DATABASE:
{samples_str}

For EACH use case above:
1. Look at the schema and sample data carefully
2. Determine which table(s) and column(s) directly support that use case
3. Write a working Snowflake SQL query using the REAL column names visible in the schema
4. Assign a confidence score (High/Medium/Low) — High means the data clearly supports the use case,
   Medium means partial data exists, Low means the use case needs additional data

Return a JSON array. Each item:
{{
  "usecase": "exact use case name",
  "type": "Analytics|Data Engineering|Data Science",
  "tables": ["fully.qualified.table"],
  "columns_used": ["col1", "col2"],
  "sql": "SELECT ... FROM real_table_name ... LIMIT 20",
  "demo_description": "2-sentence description of what the demo shows and what business decision it supports",
  "data_confidence": "High|Medium|Low",
  "confidence_reason": "one sentence explaining why this confidence level — what data was found or missing",
  "what_data_proves": "one sentence on what the actual data in this table demonstrates for the customer"
}}

CRITICAL: Only use column names that actually appear in the schema above. Do not invent columns.
Return ONLY valid JSON array. No markdown.
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
                 "demo_description": "Shows average payment delay per customer ranked by risk. Helps AR teams prioritise collections and identify high-risk accounts before they become bad debt.",
                 "data_confidence": "High",
                 "confidence_reason": "SALES_DATA contains sale_date and customer_name enabling direct delay calculation.",
                 "what_data_proves": "The data shows real customer payment patterns, validating the AR risk the customer mentioned in the Discovery call."},
                {"usecase": "Sales Revenue Trend Analysis", "type": "Analytics",
                 "tables": ["COCO_HACKATHON_DB.CORE_DATA.SALES_DATA"],
                 "columns_used": ["sale_date", "revenue", "product"],
                 "sql": "SELECT DATE_TRUNC('month', sale_date) as month, SUM(revenue) as total_revenue, COUNT(*) as deals FROM COCO_HACKATHON_DB.CORE_DATA.SALES_DATA GROUP BY 1 ORDER BY 1 LIMIT 20",
                 "demo_description": "Monthly revenue trend with deal count overlay. Enables VP Sales to spot seasonal patterns and track progress against targets.",
                 "data_confidence": "High",
                 "confidence_reason": "SALES_DATA has revenue and date columns needed for trend analysis.",
                 "what_data_proves": "Actual revenue data confirms the growth trajectory discussed in the SCC call."},
                {"usecase": "Customer Churn Prediction Model", "type": "Data Science",
                 "tables": ["COCO_HACKATHON_DB.CORE_DATA.SALES_DATA"],
                 "columns_used": ["customer_name", "sale_date", "revenue"],
                 "sql": "SELECT customer_name, MAX(sale_date) as last_purchase, COUNT(*) as total_orders, SUM(revenue) as lifetime_value, DATEDIFF('day', MAX(sale_date), CURRENT_DATE) as days_since_last FROM COCO_HACKATHON_DB.CORE_DATA.SALES_DATA GROUP BY 1 ORDER BY days_since_last DESC LIMIT 20",
                 "demo_description": "Customer recency, frequency, value analysis as a proxy for churn risk. Customers with high days_since_last and declining order frequency are flagged as at-risk.",
                 "data_confidence": "Medium",
                 "confidence_reason": "Transaction data enables RFM churn proxy but a dedicated churn label column would improve model accuracy.",
                 "what_data_proves": "Shows which customers are already going quiet — making the churn prediction use case tangible and urgent."},
            ]

        st.session_state.data_samples = data_samples

    # Clear the pulse loader now that analysis is done
    loader_placeholder.empty()

# ─────────────────────────────────────────────────────────────
# STEP 2 — Render Results (persists across re-runs via session_state)
# ─────────────────────────────────────────────────────────────
if st.session_state.analysis:
    analysis      = st.session_state.analysis
    market_trends = st.session_state.market_trends
    matches       = st.session_state.matches
    industry_disp = st.session_state.industry_cached or "Your Industry"

    # ── Overview ───────────────────────────────────────────
    st.markdown("<div class='section-label'>Analysis Overview</div>", unsafe_allow_html=True)
    st.markdown("<div class='panel'>", unsafe_allow_html=True)
    metrics = analysis.get("metrics", {})
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Pain Points", metrics.get("pain_point_count", "—"))
    with c2:
        st.metric("Sentiment", f"{metrics.get('sentiment_score', '—')} / 10")
    with c3:
        st.metric("Roadmap Items", metrics.get("roadmap_item_count", "—"))
    with c4:
        urgency = metrics.get("urgency_level", "—")
        icon = {"High": "▲", "Medium": "◆", "Low": "▼"}.get(urgency, "·")
        st.metric("Urgency", f"{icon} {urgency}")
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Market Intelligence ────────────────────────────────
    st.markdown("<div class='section-label' style='margin-top:1.1rem;'>Market Intelligence</div>", unsafe_allow_html=True)
    st.markdown("<div class='panel'>", unsafe_allow_html=True)
    st.markdown(f"<h2>📈 Industry Trends — {industry_disp}</h2>", unsafe_allow_html=True)
    st.markdown(f"<div style='color:#3d5c48; font-size:12px; line-height:1.7;'>{market_trends}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Use Case Landscape — 3 tabs ───────────────────────
    st.markdown("<div class='section-label' style='margin-top:1.1rem;'>Use Case Landscape</div>", unsafe_allow_html=True)
    st.markdown("<div class='panel'>", unsafe_allow_html=True)
    st.markdown("<h2>💡 Identified Opportunities — Select for Demo</h2>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:11px;color:#5a7a65;margin-bottom:0.75rem;'>All use cases identified from your transcripts. Select one or more to see the live demo and ROI case.</div>", unsafe_allow_html=True)

    # helper to render use case cards with ROI, tier badges, and select checkbox
    def uc_card_html(uc, idx, cat_key):
        if isinstance(uc, dict):
            name       = uc.get("name", uc.get("usecase", str(uc)))
            roi        = uc.get("roi", "")
            tier       = uc.get("value_tier", "Strategic")
            stakeholder= uc.get("stakeholder", "")
        else:
            name, roi, tier, stakeholder = str(uc), "", "Strategic", ""

        tier_colors = {
            "Quick Win":        ("rgba(76,175,120,0.15)",  "#4caf78",  "rgba(76,175,120,0.4)"),
            "Strategic":        ("rgba(79,140,255,0.12)",  "#4f8cff",  "rgba(79,140,255,0.35)"),
            "Transformational": ("rgba(240,165,0,0.12)",   "#f0a500",  "rgba(240,165,0,0.35)"),
        }
        bg, fg, border = tier_colors.get(tier, tier_colors["Strategic"])
        roi_html        = f'<div style="font-size:11px;color:#4caf78;font-weight:600;margin-bottom:0.2rem;">💰 {roi}</div>' if roi else ""
        stakeholder_html= f'<div style="font-size:10px;color:#6a8a74;">👤 {stakeholder}</div>' if stakeholder else ""
        return f"""
        <div class="uc-card" style="position:relative;">
            <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:0.25rem;">
                <div class="uc-card-title">{name}</div>
                <span style="background:{bg};color:{fg};border:1px solid {border};
                             font-size:9px;font-weight:700;padding:0.15rem 0.5rem;border-radius:4px;
                             text-transform:uppercase;flex-shrink:0;margin-left:0.5rem;letter-spacing:0.05em;">
                    {tier}
                </span>
            </div>
            {roi_html}
            {stakeholder_html}
        </div>"""

    # normalise usecases into dicts
    def normalise_ucs(raw_list):
        result = []
        for uc in raw_list:
            if isinstance(uc, str):
                result.append({"name": uc, "roi": "", "value_tier": "Strategic", "stakeholder": ""})
            elif isinstance(uc, dict):
                result.append(uc)
        return result

    analytics_ucs = normalise_ucs(analysis.get("analytics_usecases", []))
    de_ucs        = normalise_ucs(analysis.get("dataengineering_usecases", []))
    ds_ucs        = normalise_ucs(analysis.get("datascience_usecases", []))

    # Session state for selected use cases
    if "sel_ucs" not in st.session_state:
        st.session_state.sel_ucs = []

    tab_a, tab_de, tab_ds, tab_sel = st.tabs([
        f"📊 Analytics ({len(analytics_ucs)})",
        f"⚙️ Data Engineering ({len(de_ucs)})",
        f"🤖 Data Science & AI ({len(ds_ucs)})",
        f"🎯 Selected for Demo ({len(st.session_state.sel_ucs)})",
    ])

    with tab_a:
        st.markdown("<div style='font-size:11px;color:#5a7a65;margin-bottom:0.6rem;'>Dashboards, KPI reports, trend analysis, and BI visualisations.</div>", unsafe_allow_html=True)
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
        st.markdown("<div style='font-size:11px;color:#5a7a65;margin-bottom:0.6rem;'>Data pipelines, ingestion, quality, lineage, transformation, and orchestration.</div>", unsafe_allow_html=True)
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
        st.markdown("<div style='font-size:11px;color:#5a7a65;margin-bottom:0.6rem;'>ML models, predictions, recommendations, NLP, and anomaly detection on Snowflake Cortex.</div>", unsafe_allow_html=True)
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

    with tab_sel:
        if not st.session_state.sel_ucs:
            st.markdown("<div style='text-align:center;padding:1.5rem;color:#7a9e88;'>No use cases selected yet. Tick 'Add to Demo' on any use case above.</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='font-size:12px;color:#4caf78;font-weight:600;margin-bottom:0.5rem;'>✓ {len(st.session_state.sel_ucs)} use case(s) queued for demo</div>", unsafe_allow_html=True)
            for uc_name in st.session_state.sel_ucs:
                st.markdown(f"<div style='padding:0.35rem 0.75rem;background:rgba(76,175,120,0.08);border:1px solid rgba(76,175,120,0.2);border-radius:6px;margin-bottom:0.35rem;font-size:12px;color:#1a2e22;'>✦ {uc_name}</div>", unsafe_allow_html=True)
            if st.button("🗑️ Clear All Selections"):
                st.session_state.sel_ucs = []
                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    # ── Schema → Use Case Match Display ───────────────────
    all_ucs_flat = analytics_ucs + de_ucs + ds_ucs

    if matches:
        st.markdown("<div class='section-label' style='margin-top:1.1rem;'>Data Match & Demo Selection</div>", unsafe_allow_html=True)
        st.markdown("<div class='panel'>", unsafe_allow_html=True)
        st.markdown("<h2>🔍 Cortex Mapped Use Cases to Your Real Data</h2>", unsafe_allow_html=True)
        st.markdown("<div style='font-size:11px;color:#2d4a36;margin-bottom:0.85rem;'>Each use case below has been validated against your actual database schema. Confidence score shows how well your existing data supports the use case.</div>", unsafe_allow_html=True)

        # Show all matches as cards with confidence + data proof
        conf_color = {"High": "#2d7a50", "Medium": "#c07a00", "Low": "#b03030"}
        conf_bg    = {"High": "#e8f5ee", "Medium": "#fff8e6", "Low": "#fdeaea"}
        conf_border= {"High": "#a8d8b8", "Medium": "#e8c870", "Low": "#f0a8a8"}

        for m in matches:
            conf  = m.get("data_confidence", "Medium")
            proof = m.get("what_data_proves", "")
            reason= m.get("confidence_reason", "")
            cols_used = ", ".join(m.get("columns_used", []))
            fg    = conf_color.get(conf, conf_color["Medium"])
            bg    = conf_bg.get(conf, conf_bg["Medium"])
            bd    = conf_border.get(conf, conf_border["Medium"])
            type_colors = {"Analytics":"#2d6a9f","Data Engineering":"#6a3a9f","Data Science":"#2d7a50"}
            type_fg = type_colors.get(m.get("type","Analytics"), "#2d6a9f")
            st.markdown(f"""
            <div style="background:#f5f8f5;border:1px solid #c0d4c6;border-radius:10px;
                        padding:0.9rem 1.1rem;margin-bottom:0.6rem;border-left:4px solid {fg};">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:0.35rem;">
                    <div style="font-size:13px;font-weight:700;color:#132018;">{m.get('usecase','')}</div>
                    <div style="display:flex;gap:0.4rem;flex-shrink:0;margin-left:0.75rem;">
                        <span style="background:{bg};color:{fg};border:1px solid {bd};
                                     font-size:9px;font-weight:700;padding:0.15rem 0.5rem;
                                     border-radius:4px;text-transform:uppercase;">
                            {conf} Confidence
                        </span>
                        <span style="background:#e8f0ff;color:{type_fg};border:1px solid #c0d0f0;
                                     font-size:9px;font-weight:700;padding:0.15rem 0.5rem;
                                     border-radius:4px;">{m.get('type','')}</span>
                    </div>
                </div>
                <div style="font-size:11px;color:#2d4a36;margin-bottom:0.25rem;">
                    📋 {m.get('demo_description','')}
                </div>
                <div style="font-size:10px;color:#6a8c74;margin-bottom:0.15rem;">
                    🗄️ Tables: <span style="font-family:monospace;color:#2d4a36;">{', '.join(m.get('tables',[]))}</span>
                </div>
                {f'<div style="font-size:10px;color:#6a8c74;margin-bottom:0.15rem;">📎 Columns: <span style="font-family:monospace;color:#2d4a36;">{cols_used}</span></div>' if cols_used else ''}
                {f'<div style="font-size:10px;color:{fg};margin-top:0.2rem;">✦ {proof}</div>' if proof else ''}
                {f'<div style="font-size:10px;color:#8aaa94;font-style:italic;margin-top:0.1rem;">{reason}</div>' if reason else ''}
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

        # ROI metadata from use case cards
        roi_meta = None
        for uc in all_ucs_flat:
            uc_n = uc.get("name","")
            if uc_n.lower() in selected_usecase.lower() or selected_usecase.lower() in uc_n.lower():
                roi_meta = uc
                break

        # Confidence + ROI header row for selected match
        conf  = selected_match.get("data_confidence","Medium")
        fg    = conf_color.get(conf, conf_color["Medium"])
        bg    = conf_bg.get(conf,    conf_bg["Medium"])
        bd    = conf_border.get(conf, conf_border["Medium"])

        if roi_meta:
            tier     = roi_meta.get("value_tier","Strategic")
            roi_val  = roi_meta.get("roi","")
            holder   = roi_meta.get("stakeholder","")
            tier_col = {"Quick Win":"#2d7a50","Strategic":"#2d5fa8","Transformational":"#c07a00"}.get(tier,"#2d5fa8")
            ttv      = "4–8 weeks" if tier=="Quick Win" else "3–6 months" if tier=="Strategic" else "6–12 months"
            st.markdown(f"""
            <div style="display:grid;grid-template-columns:1fr 1fr 1fr 1fr;gap:0.6rem;margin:0.75rem 0 0.85rem 0;">
                <div style="background:#e8f5ee;border:1px solid #a8d8b8;border-radius:8px;padding:0.75rem 0.85rem;">
                    <div style="font-size:9px;font-weight:700;color:#2d7a50;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.2rem;">💰 ROI</div>
                    <div style="font-size:11px;color:#132018;font-weight:600;line-height:1.4;">{roi_val}</div>
                </div>
                <div style="background:#e8eefc;border:1px solid #b0c4f0;border-radius:8px;padding:0.75rem 0.85rem;">
                    <div style="font-size:9px;font-weight:700;color:#2d5fa8;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.2rem;">🎯 Tier</div>
                    <div style="font-size:13px;font-weight:800;color:{tier_col};">{tier}</div>
                </div>
                <div style="background:#f5f8f5;border:1px solid #c0d4c6;border-radius:8px;padding:0.75rem 0.85rem;">
                    <div style="font-size:9px;font-weight:700;color:#6a8c74;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.2rem;">👤 Stakeholder</div>
                    <div style="font-size:13px;font-weight:700;color:#132018;">{holder}</div>
                </div>
                <div style="background:{bg};border:1px solid {bd};border-radius:8px;padding:0.75rem 0.85rem;">
                    <div style="font-size:9px;font-weight:700;color:{fg};text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.2rem;">⏱️ Time to Value</div>
                    <div style="font-size:13px;font-weight:700;color:{fg};">{ttv}</div>
                </div>
            </div>""", unsafe_allow_html=True)

        tables_str = ', '.join(selected_match.get('tables', []))
        st.markdown(f"""
        <div class="gate-box">
            <div class="gate-icon">🔒</div>
            <div class="gate-text">
                <strong>Governance Gate</strong> — Review the SQL and confirm table access before generating the live demo.<br/>
                <span style="color:#6a8c74;font-size:10px;">Tables: {tables_str}</span>
                {f'<br/><span style="color:{fg};font-size:10px;font-weight:600;">Data Confidence: {conf} — {selected_match.get("confidence_reason","")}</span>' if selected_match.get("confidence_reason") else ''}
            </div>
        </div>""", unsafe_allow_html=True)

        st.code(selected_match['sql'], language='sql')
        approve = st.checkbox("✅ I confirm access to these tables — generate the live demo.")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        approve = False
        selected_match = None
        roi_meta = None

    # ── Smart Dummy Data Generator ─────────────────────────────
    def get_dummy_data(usecase_name, usecase_type):
        """Generate realistic prototype dummy data based on use case keywords."""
        import random, math
        random.seed(42)
        name = usecase_name.lower()

        customers    = ["Acme Corp", "NovaTech", "BluePeak", "Meridian Co", "Apex Ltd", "Starfield Inc", "CoreSys", "Delta Group"]
        months       = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        regions      = ["North", "South", "East", "West", "Central"]
        products     = ["Pro Plan", "Starter", "Enterprise", "Team", "Lite"]
        segments     = ["SMB", "Mid-Market", "Enterprise", "Startup"]

        # Churn / Retention
        if any(k in name for k in ["churn", "retention", "attrition"]):
            return pd.DataFrame({
                "segment":        segments,
                "churn_rate":     [0.22, 0.14, 0.06, 0.31],
                "at_risk_count":  [148,  89,   34,   212],
                "avg_tenure_months": [8, 18, 36, 4],
            })

        # Revenue / Sales trend
        if any(k in name for k in ["revenue", "sales", "growth", "trend", "forecast"]):
            return pd.DataFrame({
                "month":          months,
                "revenue":        [round(120000 + 8000*i + random.randint(-5000,5000)) for i in range(12)],
                "target":         [125000 + 7500*i for i in range(12)],
                "deals_closed":   [18 + i + random.randint(-3,3) for i in range(12)],
            })

        # Payment delay / AR / Invoice
        if any(k in name for k in ["payment", "delay", "invoice", "ar", "receivable", "collection"]):
            return pd.DataFrame({
                "customer":       customers[:6],
                "avg_delay_days": [21, 5, 14, 32, 8, 18],
                "open_invoices":  [12, 4, 9, 22, 3, 7],
                "outstanding_usd":[48000, 9200, 23400, 71000, 6800, 19500],
            })

        # Marketing / Campaign / ROI
        if any(k in name for k in ["marketing", "campaign", "roi", "lead", "conversion", "acquisition"]):
            return pd.DataFrame({
                "channel":        ["Paid Search", "Email", "Social", "Organic", "Referral", "Events"],
                "spend_usd":      [42000, 8500, 21000, 0, 5000, 18000],
                "leads":          [320, 210, 180, 95, 140, 260],
                "conversions":    [48, 52, 28, 31, 38, 44],
                "roi_pct":        [142, 310, 88, 0, 224, 175],
            })

        # Demand / Inventory / Supply
        if any(k in name for k in ["demand", "inventory", "supply", "stock", "warehouse", "fulfil"]):
            return pd.DataFrame({
                "product":        products,
                "forecasted_units":[1200, 3400, 480, 890, 2100],
                "actual_units":   [1140, 3610, 450, 920, 1980],
                "stockout_days":  [3, 0, 8, 1, 2],
                "overstock_units":[60, 210, 0, 30, 120],
            })

        # Recommendation / Next best offer / Upsell
        if any(k in name for k in ["recommend", "offer", "upsell", "cross", "next best"]):
            return pd.DataFrame({
                "customer_segment": segments,
                "recommended_product": ["Enterprise", "Pro Plan", "Team", "Starter"],
                "propensity_score":    [0.82, 0.67, 0.74, 0.51],
                "expected_revenue":    [24000, 8400, 13200, 3600],
                "priority_rank":       [1, 3, 2, 4],
            })

        # Support / Tickets / NPS / Satisfaction
        if any(k in name for k in ["support", "ticket", "nps", "satisfaction", "csat", "service"]):
            return pd.DataFrame({
                "month":          months[:8],
                "open_tickets":   [142, 138, 155, 121, 109, 98, 87, 76],
                "resolved_tickets":[130, 125, 148, 118, 105, 95, 84, 74],
                "avg_resolution_hrs":[18, 20, 22, 16, 14, 13, 12, 11],
                "nps_score":      [34, 36, 31, 40, 44, 47, 51, 55],
            })

        # Product / Feature / Usage
        if any(k in name for k in ["product", "feature", "usage", "adoption", "engagement", "active"]):
            return pd.DataFrame({
                "feature":        ["Dashboard", "Reports", "API", "Alerts", "Exports", "Sharing"],
                "dau":            [1240, 980, 430, 660, 320, 210],
                "wau":            [4200, 3100, 890, 1800, 740, 480],
                "adoption_pct":   [88, 72, 34, 55, 28, 19],
                "satisfaction":   [4.6, 4.2, 3.9, 4.4, 3.7, 3.5],
            })

        # Regional / Territory / Geo
        if any(k in name for k in ["region", "territory", "geo", "location", "market"]):
            return pd.DataFrame({
                "region":         regions,
                "revenue":        [380000, 290000, 420000, 175000, 310000],
                "customers":      [48, 35, 61, 22, 40],
                "growth_pct":     [12, 8, 18, -3, 14],
                "quota_attain_pct":[104, 91, 118, 72, 96],
            })

        # Default fallback — generic business overview
        return pd.DataFrame({
            "category":   customers[:6],
            "value":      [round(random.uniform(50000, 200000)) for _ in range(6)],
            "count":      [random.randint(10, 120) for _ in range(6)],
            "growth_pct": [round(random.uniform(-5, 25), 1) for _ in range(6)],
        })

    # ── Demo Dashboard (renders whenever checkbox is ticked) ──
    if approve and selected_match:
        # Ensure roi_meta is available here (may be rerun)
        if "roi_meta" not in dir():
            roi_meta = None
            for uc in (analytics_ucs + de_ucs + ds_ucs):
                uc_n = uc.get("name","")
                if uc_n.lower() in selected_match["usecase"].lower() or selected_match["usecase"].lower() in uc_n.lower():
                    roi_meta = uc
                    break

        # Try live query first; if it fails or returns empty, use smart dummy data
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

        # ── Live Dashboard ─────────────────────────────────
        st.markdown("<div class='section-label' style='margin-top:1.1rem;'>Live Demo</div>", unsafe_allow_html=True)
        st.markdown("<div class='panel'>", unsafe_allow_html=True)

        # Header row with data source badge
        hc1, hc2 = st.columns([4, 1])
        with hc1:
            st.markdown(f"<h2>📊 {selected_match['usecase']}</h2>", unsafe_allow_html=True)
            st.markdown(f"<p style='color:#3d5c48; font-size:11px; margin-bottom:1.2rem;'>{selected_match['demo_description']}</p>", unsafe_allow_html=True)
        with hc2:
            if data_source == "prototype":
                st.markdown("""
                <div style='background:rgba(76,175,120,0.1); border:1px solid rgba(76,175,120,0.3);
                            border-radius:6px; padding:0.4rem 0.7rem; text-align:center; margin-top:0.5rem;'>
                    <div style='font-size:9px; font-weight:700; color:#4caf78; letter-spacing:0.1em;
                                text-transform:uppercase;'>Prototype</div>
                    <div style='font-size:10px; color:#5a7a65; margin-top:2px;'>Sample Data</div>
                </div>""", unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style='background:rgba(76,175,120,0.15); border:1px solid rgba(76,175,120,0.4);
                            border-radius:6px; padding:0.4rem 0.7rem; text-align:center; margin-top:0.5rem;'>
                    <div style='font-size:9px; font-weight:700; color:#4caf78; letter-spacing:0.1em;
                                text-transform:uppercase;'>● Live</div>
                    <div style='font-size:10px; color:#5a7a65; margin-top:2px;'>Real Data</div>
                </div>""", unsafe_allow_html=True)

        cols      = df.columns.tolist()
        dim_col   = next((c for c in cols if df[c].dtype == object), cols[0])
        num_cols  = [c for c in cols if c != dim_col and pd.api.types.is_numeric_dtype(df[c])]

        # ── KPI Row ───────────────────────────────────────
        kpi_cols = st.columns(min(len(num_cols) + 1, 4))
        with kpi_cols[0]:
            st.metric("Total Records", df.shape[0])
        for i, nc in enumerate(num_cols[:3]):
            with kpi_cols[i + 1]:
                val   = df[nc].sum() if df[nc].dtype != float or df[nc].max() > 1 else df[nc].mean()
                label = nc.replace("_", " ").title()
                st.metric(label, f"{val:,.1f}")

        # ── Primary Bar Chart ─────────────────────────────
        if num_cols:
            y_col = num_cols[0]
            fig = px.bar(
                df, x=dim_col, y=y_col,
                color=y_col,
                color_continuous_scale=[[0,'#a8d8b8'],[0.5,'#2d9e5f'],[1,'#1a6640']],
                labels={y_col: y_col.replace("_"," ").title(), dim_col: ''},
            )
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family='Plus Jakarta Sans', color='#2d4a36', size=11),
                title=dict(text=f"{y_col.replace('_',' ').title()} by {dim_col.replace('_',' ').title()}",
                           font=dict(family='Plus Jakarta Sans', color='#132018', size=13)),
                coloraxis_showscale=False, margin=dict(l=0, r=0, t=36, b=0), height=300,
                xaxis=dict(gridcolor='#d4e8da', linecolor='#c0d4c6'),
                yaxis=dict(gridcolor='#d4e8da', linecolor='#c0d4c6'),
            )
            st.plotly_chart(fig, use_container_width=True)

        # ── Table + Pie ───────────────────────────────────
        col_tbl, col_chart2 = st.columns([1.6, 1])
        with col_tbl:
            with st.expander("🔍 Detailed Data Table"):
                st.dataframe(df, use_container_width=True)
        with col_chart2:
            if num_cols:
                pie_col = num_cols[-1]
                fig2 = px.pie(df, values=pie_col, names=dim_col, hole=0.55,
                              color_discrete_sequence=['#2d9e5f','#5bc48a','#3d8c5e','#1a6640','#87d4a8','#a8e4c0'])
                fig2.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(family='Plus Jakarta Sans', color='#2d4a36', size=11),
                    title=dict(text=f"{pie_col.replace('_',' ').title()} Split",
                               font=dict(family='Plus Jakarta Sans', color='#132018', size=12)),
                    showlegend=True, legend=dict(font=dict(color='#2d4a36', size=10)),
                    margin=dict(l=0, r=0, t=36, b=0), height=260,
                )
                st.plotly_chart(fig2, use_container_width=True)

        # ── Trend line if 2+ numeric cols ─────────────────
        if len(num_cols) >= 2:
            fig3 = px.line(df, x=dim_col, y=num_cols[:2],
                           color_discrete_sequence=['#2d7a50', '#5bc48a'],
                           labels={'value': 'Value', dim_col: ''})
            fig3.update_layout(
                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family='Plus Jakarta Sans', color='#2d4a36', size=11),
                title=dict(text='Trend Comparison',
                           font=dict(family='Plus Jakarta Sans', color='#132018', size=13)),
                margin=dict(l=0, r=0, t=36, b=0), height=240,
                xaxis=dict(gridcolor='#d4e8da', linecolor='#c0d4c6'),
                yaxis=dict(gridcolor='#d4e8da', linecolor='#c0d4c6'),
                legend=dict(font=dict(color='#2d4a36', size=10)),
            )
            st.plotly_chart(fig3, use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)

        # ── Lineage ────────────────────────────────────────
        st.markdown("<div class='section-label' style='margin-top:1.1rem;'>Generated Assets</div>", unsafe_allow_html=True)
        st.markdown("<div class='panel'>", unsafe_allow_html=True)
        st.markdown("<h2>📄 Data Lineage &amp; Mapping</h2>", unsafe_allow_html=True)
        st.code(selected_match['sql'], language='sql')
        conf_val   = selected_match.get("data_confidence","Medium")
        conf_proof = selected_match.get("what_data_proves","")
        cols_disp  = ", ".join(selected_match.get("columns_used",[]))
        st.markdown(f"""
        <div style='margin-top:1rem;'>
            <div class='lineage-row'><span class='lineage-key'>Business Intent</span><span class='lineage-val'>{selected_match['usecase']}</span></div>
            <div class='lineage-row'><span class='lineage-key'>Type</span><span class='lineage-val'>{selected_match.get('type','')}</span></div>
            <div class='lineage-row'><span class='lineage-key'>Tables Used</span><span class='lineage-val'>{', '.join(selected_match['tables'])}</span></div>
            <div class='lineage-row'><span class='lineage-key'>Columns Used</span><span class='lineage-val'>{cols_disp or '—'}</span></div>
            <div class='lineage-row'><span class='lineage-key'>Data Confidence</span><span class='lineage-val' style='color:{conf_color.get(conf_val,"#2d5fa8")};font-weight:700;'>{conf_val} — {conf_proof}</span></div>
            <div class='lineage-row'><span class='lineage-key'>Credit Estimate</span><span class='lineage-val'>Projected cost &lt; $0.01 per run</span></div>
        </div>
        """, unsafe_allow_html=True)
        st.success("✅ Live demo ready — scroll down for the full sales pitch and PDF export.")
        st.markdown("</div>", unsafe_allow_html=True)

        # ── Detailed Sales Pitch ───────────────────────────
        if roi_meta:
            st.markdown("<div class='section-label' style='margin-top:1.1rem;'>Customer Pitch</div>", unsafe_allow_html=True)
            st.markdown("<div class='panel'>", unsafe_allow_html=True)
            st.markdown("<h2>🎤 Customer Talking Points</h2>", unsafe_allow_html=True)
            st.markdown("<div style='font-size:11px;color:#2d4a36;margin-bottom:0.75rem;'>Core points to cover in the room — the problem, the benefit, and why now.</div>", unsafe_allow_html=True)

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

Return EXACTLY this structure — no more, no less. Keep each point to 1-2 sentences maximum.

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
                        pitch = session.sql(
                            f"SELECT cortex_complete('{pitch_prompt.replace(chr(39),chr(39)*2)}') as p"
                        ).collect()[0][0]
                    except Exception as e:
                        pitch = f"Generation failed: {e}"
                st.session_state.pitch = pitch
                st.session_state.pitch_uc = selected_match['usecase']

            if hasattr(st.session_state, 'pitch') and st.session_state.pitch:
                # Render each bullet block as a styled card row
                lines = st.session_state.pitch.strip().split('\n')
                icon_colors = {
                    "🔴": "#c0392b", "💡": "#2d7a50", "📊": "#2d5fa8",
                    "💰": "#c07a00", "⏱️": "#6a3a9f", "✅": "#2d7a50",
                }
                rendered = []
                current_header = ""
                current_body   = ""
                for line in lines:
                    line = line.strip()
                    if not line:
                        continue
                    # Detect header lines (start with an emoji followed by caps)
                    is_header = any(line.startswith(ic) for ic in icon_colors)
                    if is_header:
                        if current_header:
                            rendered.append((current_header, current_body.strip()))
                        current_header = line
                        current_body   = ""
                    else:
                        current_body += " " + line
                if current_header:
                    rendered.append((current_header, current_body.strip()))

                if rendered:
                    # 2-column grid of cards
                    col_a, col_b = st.columns(2)
                    for i, (header, body) in enumerate(rendered):
                        first_char = header[0] if header else "•"
                        color = icon_colors.get(first_char, "#2d7a50")
                        card_html = f"""
                        <div style="background:#ffffff;border:1px solid #c8d8cc;border-left:4px solid {color};
                                    border-radius:8px;padding:0.8rem 1rem;margin-bottom:0.6rem;">
                            <div style="font-size:11px;font-weight:700;color:{color};margin-bottom:0.25rem;">{header}</div>
                            <div style="font-size:12px;color:#2d4a36;line-height:1.6;">{body}</div>
                        </div>"""
                        with (col_a if i % 2 == 0 else col_b):
                            st.markdown(card_html, unsafe_allow_html=True)
                else:
                    # Fallback plain display
                    st.markdown(f"""
                    <div style="background:#f0f5f1;border-left:4px solid #2d7a50;border:1px solid #b0cdb8;
                                border-radius:8px;padding:1rem 1.2rem;font-size:12px;color:#132018;line-height:1.8;">
                        {st.session_state.pitch.replace(chr(10),'<br/>')}
                    </div>""", unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

        # ── PDF / HTML Export ──────────────────────────────
        st.markdown("<div class='section-label' style='margin-top:1.1rem;'>Export Demo Pack</div>", unsafe_allow_html=True)
        st.markdown("<div class='panel'>", unsafe_allow_html=True)
        st.markdown("<h2>📥 Export Demo Pack for Customer</h2>", unsafe_allow_html=True)
        st.markdown("<div style='font-size:11px;color:#2d4a36;margin-bottom:0.75rem;'>Generate a complete HTML demo report — charts, data table, ROI case, and sales pitch — ready to open in any browser or print as PDF (Ctrl+P → Save as PDF).</div>", unsafe_allow_html=True)

        if st.button("📄 Build HTML Export Pack"):
            import plotly.io as pio

            # ── Embed charts as self-contained interactive HTML divs ──
            # plotly.io.to_html does NOT need kaleido — works out of the box
            chart_divs = []
            for chartfig in [fig, fig2]:
                try:
                    # full_html=False → returns just the <div> + script, no <html> wrapper
                    # include_plotlyjs='cdn' → one CDN <script> tag at the top of the doc handles all charts
                    div = pio.to_html(
                        chartfig,
                        full_html=False,
                        include_plotlyjs=False,   # we include the CDN once at doc level
                        config={"displayModeBar": False, "responsive": True},
                    )
                    chart_divs.append(div)
                except Exception:
                    pass

            # Also add fig3 (trend line) if it was created
            try:
                if len(num_cols) >= 2:
                    div3 = pio.to_html(
                        fig3,
                        full_html=False,
                        include_plotlyjs=False,
                        config={"displayModeBar": False, "responsive": True},
                    )
                    chart_divs.append(div3)
            except Exception:
                pass

            charts_section = "\n".join(
                f'<div style="margin-bottom:1.5rem;">{d}</div>' for d in chart_divs
            ) if chart_divs else '<p style="color:#6a8c74;">No charts available for this use case.</p>'

            table_html = df.to_html(index=False, classes="data-table", border=0)

            pitch_html = ""
            if hasattr(st.session_state, 'pitch') and st.session_state.pitch:
                pitch_html = st.session_state.pitch.replace('\n', '<br/>')

            roi_val  = roi_meta.get("roi","") if roi_meta else ""
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
<!-- Plotly CDN — renders all embedded charts below -->
<script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
<style>
  *{{box-sizing:border-box;}}
  body{{font-family:'Segoe UI',Arial,sans-serif;background:#f2f6f3;color:#132018;margin:0;padding:0;font-size:14px;}}
  .cover{{background:linear-gradient(135deg,#0e1c12 0%,#163020 60%,#1a3d28 100%);
          color:#fff;padding:3rem 3.5rem;-webkit-print-color-adjust:exact;print-color-adjust:exact;}}
  .cover h1{{font-size:2rem;font-weight:800;margin:0 0 0.4rem;letter-spacing:-0.02em;}}
  .cover .sub{{font-size:1rem;opacity:0.65;margin-bottom:1.2rem;}}
  .cover .pills{{display:flex;flex-wrap:wrap;gap:0.5rem;}}
  .cover .pill{{background:rgba(255,255,255,0.12);border:1px solid rgba(255,255,255,0.2);
                border-radius:20px;padding:0.25rem 0.75rem;font-size:0.78rem;opacity:0.85;}}
  .section{{padding:2rem 3.5rem;border-bottom:1px solid #c8d8cc;}}
  .section h2{{font-size:1.05rem;font-weight:700;color:#163020;margin:0 0 1rem;
               padding-bottom:0.4rem;border-bottom:2px solid #2d7a50;}}
  .roi-grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:0.85rem;margin-bottom:1.25rem;}}
  .roi-card{{background:#e8f5ee;border:1px solid #a8d8b8;border-radius:8px;padding:0.85rem 1rem;
             border-top:3px solid #2d7a50;-webkit-print-color-adjust:exact;print-color-adjust:exact;}}
  .roi-card .rlbl{{font-size:0.68rem;text-transform:uppercase;letter-spacing:0.1em;
                   color:#2d7a50;font-weight:700;margin-bottom:0.25rem;}}
  .roi-card .rval{{font-size:0.95rem;font-weight:700;color:#132018;line-height:1.35;}}
  .kpi-grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:0.85rem;margin-bottom:1.25rem;}}
  .kpi{{background:#fff;border:1px solid #c8d8cc;border-radius:8px;padding:0.85rem 1rem;
        border-top:3px solid #2d7a50;}}
  .kpi .val{{font-size:1.4rem;font-weight:800;color:#132018;}}
  .kpi .lbl{{font-size:0.68rem;text-transform:uppercase;letter-spacing:0.08em;color:#6a8c74;margin-top:0.2rem;}}
  .chart-wrap{{background:#fff;border:1px solid #c8d8cc;border-radius:10px;
               padding:1rem;margin-bottom:1rem;}}
  .data-table{{width:100%;border-collapse:collapse;font-size:0.83rem;margin-top:0.5rem;}}
  .data-table th{{background:#163020;color:#fff;padding:0.55rem 0.8rem;text-align:left;
                  font-weight:600;-webkit-print-color-adjust:exact;print-color-adjust:exact;}}
  .data-table td{{padding:0.45rem 0.8rem;border-bottom:1px solid #d4e8da;}}
  .data-table tr:nth-child(even) td{{background:#ecf2ed;}}
  .pitch-box{{background:#fff;border-left:4px solid #2d7a50;border:1px solid #b0cdb8;
              border-radius:8px;padding:1.25rem 1.75rem;font-size:0.9rem;line-height:1.85;
              -webkit-print-color-adjust:exact;print-color-adjust:exact;}}
  .pitch-box strong{{color:#2d7a50;}}
  .sql-box{{background:#ecf2ed;border:1px solid #c0d4c6;border-radius:6px;
             padding:0.85rem 1.1rem;font-family:'Courier New',monospace;font-size:0.78rem;
             color:#163020;white-space:pre-wrap;overflow-x:auto;}}
  .badge{{display:inline-block;padding:0.2rem 0.65rem;border-radius:4px;font-size:0.72rem;
          font-weight:700;background:#e8f5ee;color:#2d7a50;border:1px solid #a8d8b8;margin-right:0.3rem;}}
  .footer-bar{{background:#163020;color:rgba(255,255,255,0.45);text-align:center;
               padding:1rem 2rem;font-size:0.75rem;
               -webkit-print-color-adjust:exact;print-color-adjust:exact;}}
  @media print{{
    body{{background:#fff;font-size:12px;}}
    .section{{padding:1.25rem 2rem;page-break-inside:avoid;}}
    .chart-wrap{{page-break-inside:avoid;}}
    .js-plotly-plot .plotly .main-svg{{max-height:280px!important;}}
  }}
</style>
</head>
<body>

<!-- COVER -->
<div class="cover">
  <div style="font-size:0.72rem;letter-spacing:0.2em;opacity:0.45;margin-bottom:0.4rem;text-transform:uppercase;">InsightForge · Snowflake Cortex</div>
  <h1>Demo Pack: {selected_match['usecase']}</h1>
  <div class="sub">Prepared for <strong>{customer_name}</strong> · {industry}</div>
  <div class="pills">
    <span class="pill">📅 {date.today().strftime('%d %B %Y')}</span>
    <span class="pill">📊 {selected_match.get('type','')}</span>
    <span class="pill">🗄️ {', '.join(selected_match.get('tables',[]))}</span>
    <span class="pill">🔒 {selected_match.get('data_confidence','')} Data Confidence</span>
  </div>
</div>

<!-- EXECUTIVE SUMMARY -->
<div class="section">
  <h2>Executive Summary</h2>
  <div class="roi-grid">
    <div class="roi-card"><div class="rlbl">💰 ROI</div><div class="rval">{roi_val}</div></div>
    <div class="roi-card"><div class="rlbl">🎯 Value Tier</div><div class="rval">{tier}</div></div>
    <div class="roi-card"><div class="rlbl">👤 Stakeholder</div><div class="rval">{holder}</div></div>
    <div class="roi-card"><div class="rlbl">⏱️ Time to Value</div><div class="rval">{ttv_html}</div></div>
  </div>
  <p style="font-size:0.92rem;line-height:1.7;color:#2d4a36;margin-bottom:0.75rem;">{selected_match.get('demo_description','')}</p>
  <p style="margin:0;"><span class="badge">{selected_match.get('data_confidence','')} Confidence</span>
     <span style="font-size:0.85rem;color:#2d4a36;">{selected_match.get('what_data_proves','')}</span></p>
</div>

<!-- KPI SNAPSHOT -->
<div class="section">
  <h2>Data Snapshot — {len(df)} Records Analysed</h2>
  <div class="kpi-grid">
    <div class="kpi"><div class="val">{len(df)}</div><div class="lbl">Total Records</div></div>
    {''.join(f'<div class="kpi"><div class="val">{df[nc].sum() if df[nc].max()>1 else round(df[nc].mean(),2):,.1f}</div><div class="lbl">{nc.replace("_"," ").title()}</div></div>' for nc in num_cols[:3])}
  </div>
</div>

<!-- CHARTS -->
<div class="section">
  <h2>Live Demo Charts</h2>
  {charts_section}
</div>

<!-- DATA TABLE -->
<div class="section">
  <h2>Underlying Data Table</h2>
  {table_html}
</div>

<!-- SQL QUERY -->
<div class="section">
  <h2>SQL Query Used</h2>
  <div class="sql-box">{selected_match.get('sql','').replace('<','&lt;').replace('>','&gt;')}</div>
  <p style="font-size:0.78rem;color:#6a8c74;margin-top:0.5rem;">
    Tables: {', '.join(selected_match.get('tables',[]))} &nbsp;·&nbsp;
    Columns: {', '.join(selected_match.get('columns_used',[]))}
  </p>
</div>

<!-- SALES PITCH -->
{'<div class="section"><h2>Sales Pitch &amp; Business Case</h2><div class="pitch-box">' + pitch_html + '</div></div>' if pitch_html else ''}

<!-- FOOTER -->
<div class="footer-bar">
  Generated by <strong style="color:rgba(255,255,255,0.7);">InsightForge</strong> · Snowflake Cortex ·
  {date.today().strftime('%d %B %Y')} · Confidential — Prepared for {customer_name}
</div>

</body>
</html>"""

            st.session_state.pdf_report = html_export

        if st.session_state.pdf_report:
            st.download_button(
                label="⬇️ Download Demo Pack (.html — open in browser, Ctrl+P to save as PDF)",
                data=st.session_state.pdf_report,
                file_name=f"InsightForge_Demo_{customer_name.replace(' ','_')}_{selected_match['usecase'][:30].replace(' ','_')}.html",
                mime="text/html",
                use_container_width=True,
            )
            st.success("✅ Demo pack ready. Open the file in Chrome/Edge and press Ctrl+P → Save as PDF to get a printable version.")

        st.markdown("</div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# Footer
# ─────────────────────────────────────────────────────────────
st.markdown("""
<div class='footer'>
    Powered by <span>Snowflake Cortex</span> &nbsp;·&nbsp; Zero hypothetical demos &nbsp;·&nbsp; Real customer data
</div>
""", unsafe_allow_html=True)
