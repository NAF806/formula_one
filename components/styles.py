import streamlit as st

def load_styles():
    """
    Load custom CSS styling for the application
    """
    st.markdown("""
    <style>
        /* Dark theme */
        body {
            background-color: #15151e;
            color: #ffffff;
        }
        
        .main-header {
            font-size: 2.5rem;
            color: #e10600;
            font-weight: 800;
            text-align: center;
            margin-bottom: 1rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }
        
        .subheader {
            font-size: 1.5rem;
            color: #ffffff;
            font-weight: 600;
            margin-top: 1rem;
            border-bottom: 2px solid #e10600;
            padding-bottom: 0.3rem;
        }
        
        .card {
            background-color: #1e1e2d;
            border-radius: 10px;
            padding: 1.5rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
            margin-bottom: 1rem;
            border: 1px solid #2c2c3a;
        }
        
        .info-text {
            color: #d1d1d1;
            font-size: 0.9rem;
        }
        
        .highlight {
            background-color: #e10600;
            padding: 0.2rem 0.5rem;
            color: white;
            border-radius: 4px;
            font-weight: 600;
        }
        
        .sidebar-content {
            background-color: #1e1e2d;
            padding: 1rem;
            border-radius: 10px;
            color: white;
            border: 1px solid #2c2c3a;
        }
        
        /* Custom tab styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 0;
            background-color: #15151e;
            border-radius: 10px;
            padding: 5px;
        }
        
        .stTabs [data-baseweb="tab"] {
            height: 50px;
            white-space: pre-wrap;
            background-color: #1e1e2d;
            border-radius: 5px;
            margin-right: 5px;
            padding: 10px 20px;
            font-weight: 600;
            border: none;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: #e10600 !important;
            color: white !important;
        }
        
        /* Remove whitespace */
        .block-container {
            padding-top: 1rem;
            padding-bottom: 0rem;
        }
        
        div[data-testid="stVerticalBlock"] {
            gap: 0.5rem;
        }
        
        /* Style dataframes */
        div[data-testid="stDataFrame"] {
            width: 100%;
        }
        
        div[data-testid="stDataFrame"] > div {
            background-color: #1e1e2d;
            border-radius: 10px;
            padding: 0.5rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            border: 1px solid #2c2c3a;
        }
        
        /* Remove extra padding from Streamlit containers */
        .css-1544g2n.e1tzin5v4 {
            padding: 1rem 1rem 0rem 1rem;
            margin: 0;
        }
        
        .css-9ycgxx.exg6vvm3 {
            padding-bottom: 0;
        }
        
        /* Fix container margins */
        .element-container {
            margin-bottom: 1rem;
        }
        
        /* Additional race styling */
        .race-info {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 1rem;
            color: white;
        }
        
        .loading-spinner {
            text-align: center;
            margin: 2rem 0;
        }
        
        /* Fix white bar */
        .stApp {
            background-color: #15151e;
        }
        
        div.stTabs > div:first-of-type > div:first-of-type > div:last-child {
            background-color: transparent !important;
            border: none !important;
        }
        
        .css-10pw50, .css-1cpxqw2 {
            background-color: #15151e !important;
        }
        
        /* Fix tab content area */
        div.stTabs > div:nth-child(2) {
            background-color: #15151e !important;
            padding: 0 !important;
            border: none !important;
        }
    </style>
    """, unsafe_allow_html=True)