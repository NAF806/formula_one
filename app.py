import streamlit as st
from datetime import datetime
from components.styles import load_styles
from components.championship import show_championship_tab
from components.calendar import show_calendar_tab
from components.race_analysis import show_race_analysis_tab
from utils.api import get_f1_data
from utils.parsers import parse_driver_standings, parse_constructor_standings

# Set page configuration with a custom theme and dark mode
st.set_page_config(
    page_title="F1 Explorer",
    page_icon="🏎️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Load custom CSS
load_styles()

def main():
    # Title with dynamic F1 logo and styling
    st.markdown('<h1 class="main-header">🏎️ F1 Explorer Dashboard</h1>', unsafe_allow_html=True)
    
    # Sidebar for controls
    with st.sidebar:
        st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
        
        # Year selection
        years = list(range(2000, datetime.now().year + 1))
        year = st.selectbox("Select Season", years, index=len(years)-1)
        
        # Display current standings leaders
        ds = parse_driver_standings(year)
        cs = parse_constructor_standings(year)
        
        if not ds.empty:
            leader = ds.iloc[0]
            st.markdown(f"""
            <div style="margin-top: 20px; padding: 10px; background-color: rgba(255,255,255,0.1); border-radius: 5px;">
                <h3 style="margin: 0; font-size: 1rem;">Current Leaders</h3>
                <p style="margin-bottom: 5px; font-size: 0.9rem;">
                    <span style="color: #e10600; font-weight: bold;">Driver:</span> {leader['Driver']} ({leader['Points']} pts)
                </p>
                <p style="margin: 0; font-size: 0.9rem;">
                    <span style="color: #e10600; font-weight: bold;">Constructor:</span> {cs.iloc[0]['Constructor']} ({cs.iloc[0]['Points']} pts)
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Add F1 information
        st.markdown("""
        <div style="margin-top: 20px; padding: 10px; font-size: 0.8rem; color: #999;">
            <p>Built with 💻 and ❤️</p>
            <p>Using Streamlit & Ergast F1 API</p>
            <p>All F1 data © FIA Formula One World Championship</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Create tabs with enhanced styling
    tab1, tab2, tab3 = st.tabs(["📊 Championship", "🗓️ Calendar", "🏁 Race Analysis"])
    
    # Tab 1: Standings
    with tab1:
        show_championship_tab(year)
    
    # Tab 2: Calendar
    with tab2:
        show_calendar_tab(year)
    
    # Tab 3: Race Analysis
    with tab3:
        show_race_analysis_tab(year)
    
    # Footer
    st.markdown(f"""
    <div style="text-align: center; padding: 20px; margin-top: 30px; color: #666; font-size: 0.8rem;">
        <p>F1 Explorer Dashboard | Updated for {datetime.now().year}</p>
        <p>Data provided by Ergast F1 API | All F1 data © Formula One World Championship Ltd.</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()