import streamlit as st
from utils.parsers import parse_driver_standings, parse_constructor_standings
from visualizations.standings import create_driver_standings_chart, create_constructor_standings_chart

def show_championship_tab(year):
    """
    Display the championship tab with driver and constructor standings
    
    Args:
        year: The year to show standings for
    """
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    # Show loading spinner while data loads
    with st.spinner("Loading championship data..."):
        ds = parse_driver_standings(year)
        cs = parse_constructor_standings(year)
    
    if ds.empty or cs.empty:
        st.info(f"No championship data available for {year}.")
    else:
        # Create two columns for standings
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<h2 class="subheader">Drivers Championship</h2>', unsafe_allow_html=True)
            
            # Format the dataframe
            styled_ds = ds.style.apply(lambda x: ['background-color: #e10600; color: white' if i == 0 
                                            else 'background-color: #0600EF; color: white' if i == 1 
                                            else 'background-color: #FFC0CB; color: black' if i == 2 
                                            else '' for i in range(len(x))], axis=0)
            
            st.dataframe(styled_ds, use_container_width=True)
            
            # Add visualization
            driver_chart = create_driver_standings_chart(ds)
            if driver_chart:
                st.plotly_chart(driver_chart, use_container_width=True)
        
        with col2:
            st.markdown('<h2 class="subheader">Constructors Championship</h2>', unsafe_allow_html=True)
            
            # Format the dataframe
            styled_cs = cs.style.apply(lambda x: ['background-color: #e10600; color: white' if i == 0 
                                            else 'background-color: #0600EF; color: white' if i == 1 
                                            else 'background-color: #FFC0CB; color: black' if i == 2 
                                            else '' for i in range(len(x))], axis=0)
            
            st.dataframe(styled_cs, use_container_width=True)
            
            # Add visualization
            constructor_chart = create_constructor_standings_chart(cs)
            if constructor_chart:
                st.plotly_chart(constructor_chart, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)