import streamlit as st
import pandas as pd
from datetime import datetime
from utils.parsers import parse_races
from visualizations.calendar import create_calendar_map

def show_calendar_tab(year):
    """
    Display the calendar tab with race schedule and map
    
    Args:
        year: The year to show calendar for
    """
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    with st.spinner("Loading calendar data..."):
        races = parse_races(year)
    
    if races.empty:
        st.info(f"No calendar data available for {year}.")
    else:
        st.markdown('<h2 class="subheader">Season Calendar</h2>', unsafe_allow_html=True)
        
        # Create map visualization if location data exists
        calendar_map = create_calendar_map(races)
        if calendar_map:
            st.plotly_chart(calendar_map, use_container_width=True)
        
        # Enhanced table formatting
        calendar_df = races[['round', 'raceName', 'Circuit.circuitName', 'date']].rename(
            columns={'round': 'Round', 'raceName': 'Race', 'Circuit.circuitName': 'Circuit', 'date': 'Date'}
        ).copy()
        
        # Format date column
        calendar_df['Date'] = calendar_df['Date'].dt.strftime('%d %b %Y')
        
        # Add next race indicator
        current_date = datetime.now()
        next_race_index = races[races['date'] > current_date].index.min()
        
        if pd.notnull(next_race_index):
            next_race_round = races.loc[next_race_index, 'round']
            styled_calendar = calendar_df.style.apply(
                lambda x: ['background-color: #e10600; color: white' if r == next_race_round else '' 
                          for r in calendar_df['Round']], axis=1
            )
            st.dataframe(styled_calendar, use_container_width=True)
        else:
            st.dataframe(calendar_df, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)