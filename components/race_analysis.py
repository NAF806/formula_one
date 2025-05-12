import streamlit as st
from utils.parsers import parse_races, parse_results, parse_qualifying, parse_sprint, parse_pitstops, parse_laps, get_race_details
from visualizations.race_analysis import create_race_results_positions, create_lap_times_chart

def show_race_analysis_tab(year):
    """
    Display the race analysis tab with race results, qualifying, etc.
    
    Args:
        year: The year to show race analysis for
    """
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    with st.spinner("Loading race data..."):
        races = parse_races(year)
    
    if races.empty:
        st.info(f"No race data available for {year}.")
    else:
        # Race selector with enhanced UI
        col1, col2 = st.columns([1, 2])
        
        with col1:
            race_rounds = races['round'].tolist()
            rnd = st.selectbox("Select Round", race_rounds)
        
        # Get race details
        race_details = get_race_details(year, rnd)
        
        if race_details:
            with col2:
                st.markdown(f"""
                <div class="race-info">
                    <div>
                        <h3 style="margin:0;">{race_details['name']}</h3>
                        <p style="margin:0;">{race_details['circuit']}</p>
                        <p style="margin:0; color:#666;">{race_details['locality']}, {race_details['country']}</p>
                    </div>
                    <div>
                        <h4 style="margin:0;">{race_details['date'].strftime('%d %b %Y')}</h4>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # Create tabs for different race data
        race_tab1, race_tab2, race_tab3, race_tab4 = st.tabs(["🏆 Results", "⏱️ Qualifying", "🚀 Sprint", "📊 Analysis"])
        
        with race_tab1:
            show_race_results_tab(year, rnd)
        
        with race_tab2:
            show_qualifying_tab(year, rnd)
        
        with race_tab3:
            show_sprint_tab(year, rnd)
        
        with race_tab4:
            show_race_analysis_details_tab(year, rnd)
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_race_results_tab(year, rnd):
    """
    Display race results tab
    
    Args:
        year: The year of the race
        rnd: The round number
    """
    with st.spinner("Loading race results..."):
        results_df = parse_results(year, rnd)
    
    if results_df.empty:
        st.info("No race results available for this round.")
    else:
        st.markdown('<h3 class="subheader">Race Results</h3>', unsafe_allow_html=True)
        
        # Position change visualization
        positions_chart = create_race_results_positions(results_df)
        if positions_chart:
            st.plotly_chart(positions_chart, use_container_width=True)
        
        # Include only relevant columns first
        display_cols = ['Position', 'Driver', 'Constructor', 'Grid', 'Status', 'Points']
        if 'Time' in results_df.columns:
            display_cols.insert(5, 'Time')
        
        # Then style the filtered dataframe
        styled_results = results_df[display_cols].style.apply(
            lambda x: ['background-color: #e10600; color: white' if pos == 1 
                      else 'background-color: #0600EF; color: white' if pos == 2
                      else 'background-color: #FFC0CB; color: black' if pos == 3
                      else '' for pos in results_df['Position']], axis=0
        )
        
        st.dataframe(styled_results, use_container_width=True)

def show_qualifying_tab(year, rnd):
    """
    Display qualifying results tab
    
    Args:
        year: The year of qualifying
        rnd: The round number
    """
    with st.spinner("Loading qualifying data..."):
        quali_df = parse_qualifying(year, rnd)
    
    if quali_df.empty:
        st.info("No qualifying results available for this round.")
    else:
        st.markdown('<h3 class="subheader">Qualifying Results</h3>', unsafe_allow_html=True)
        
        # Style the qualifying dataframe
        styled_quali = quali_df.style.apply(
            lambda x: ['background-color: #e10600; color: white' if pos == 1 
                      else 'background-color: #0600EF; color: white' if pos == 2
                      else 'background-color: #FFC0CB; color: black' if pos == 3
                      else '' for pos in quali_df['Position']], axis=0
        )
        
        st.dataframe(styled_quali, use_container_width=True)
        
        # Add visualization - Q1, Q2, Q3 comparison if data exists
        if 'Q1' in quali_df.columns and 'Q2' in quali_df.columns and 'Q3' in quali_df.columns:
            # Convert session times to seconds for comparison
            def session_to_seconds(time_str):
                if not isinstance(time_str, str):
                    return None
                try:
                    if ":" in time_str:
                        minutes, rest = time_str.split(':')
                        return int(minutes) * 60 + float(rest)
                    else:
                        return float(time_str)
                except:
                    return None
            
            plot_df = quali_df.copy()
            for session in ['Q1', 'Q2', 'Q3']:
                if session in plot_df.columns:
                    plot_df[f"{session}_seconds"] = plot_df[session].apply(session_to_seconds)
            
            # Filter drivers who participated in all sessions (front-runners)
            plot_df = plot_df.dropna(subset=['Q1_seconds', 'Q2_seconds', 'Q3_seconds'])
            
            if not plot_df.empty and len(plot_df) >= 3:  # Ensure we have enough data
                # Create session comparison chart
                import plotly.graph_objects as go
                
                fig = go.Figure()
                
                for session in ['Q1', 'Q2', 'Q3']:
                    fig.add_trace(go.Bar(
                        x=plot_df['Driver'],
                        y=plot_df[f"{session}_seconds"],
                        name=session,
                        hovertemplate='%{y:.3f}s'
                    ))
                
                fig.update_layout(
                    title="Qualifying Session Comparison",
                    xaxis_title="",
                    yaxis_title="Time (seconds)",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    barmode='group',
                    margin=dict(l=0, r=0, t=50, b=0),
                )
                
                st.plotly_chart(fig, use_container_width=True)

def show_sprint_tab(year, rnd):
    """
    Display sprint results tab
    
    Args:
        year: The year of the sprint race
        rnd: The round number
    """
    with st.spinner("Loading sprint data..."):
        sprint_df = parse_sprint(year, rnd)
    
    if sprint_df.empty:
        st.info("No sprint results available for this round.")
    else:
        st.markdown('<h3 class="subheader">Sprint Results</h3>', unsafe_allow_html=True)
        
        # Style the sprint dataframe
        styled_sprint = sprint_df.style.apply(
            lambda x: ['background-color: #e10600; color: white' if pos == 1 
                      else 'background-color: #0600EF; color: white' if pos == 2
                      else 'background-color: #FFC0CB; color: black' if pos == 3
                      else '' for pos in sprint_df['Position']], axis=0
        )
        
        st.dataframe(styled_sprint, use_container_width=True)

def show_race_analysis_details_tab(year, rnd):
    """
    Display detailed race analysis tab with lap times and pit stops
    
    Args:
        year: The year of the race
        rnd: The round number
    """
    st.markdown('<h3 class="subheader">Race Analysis</h3>', unsafe_allow_html=True)
    
    # Create multi-tab analysis
    analysis_tab1, analysis_tab2 = st.tabs(["Lap Times", "Pit Stops"])
    
    with analysis_tab1:
        show_lap_times_tab(year, rnd)
    
    with analysis_tab2:
        show_pit_stops_tab(year, rnd)

def show_lap_times_tab(year, rnd):
    """
    Display lap times analysis tab
    
    Args:
        year: The year of the race
        rnd: The round number
    """
    with st.spinner("Loading lap data..."):
        # First get driver ID for selection
        results_df = parse_results(year, rnd)
        
        if not results_df.empty:
            # Create driver selector
            drivers = results_df['Driver'].tolist()
            selected_driver = st.selectbox("Select Driver", drivers)
            
            # Extract driver_id from full name for API call (extract last name and use lowercase)
            driver_id = selected_driver.split()[-1].lower()
            
            # Get lap times for the selected driver
            lap_times_df = parse_laps(year, rnd, driver_id)
            
            if lap_times_df.empty:
                st.info(f"No lap time data available for {selected_driver}.")
            else:
                # Create lap time chart
                lap_chart = create_lap_times_chart(lap_times_df, driver_id)
                if lap_chart:
                    st.plotly_chart(lap_chart, use_container_width=True)
                
                # Display table of lap times
                st.dataframe(lap_times_df, use_container_width=True)
        else:
            st.info("No race results available to select drivers.")

def show_pit_stops_tab(year, rnd):
    """
    Display pit stops analysis tab
    
    Args:
        year: The year of the race
        rnd: The round number
    """
    with st.spinner("Loading pit stop data..."):
        pitstop_df = parse_pitstops(year, rnd)
    
    if pitstop_df.empty:
        st.info("No pit stop data available for this round.")
    else:
        # Create a pit stop visualization
        import plotly.express as px
        
        fig = px.scatter(
            pitstop_df, 
            x='Lap', 
            y='DriverID',
            size=[3] * len(pitstop_df),
            color='Duration',
            color_continuous_scale='Reds_r',  # Red scale (reversed so darker = slower)
            title="Pit Stop Strategy",
            labels={'Lap': 'Lap Number', 'DriverID': 'Driver'},
            height=400,
        )
        
        fig.update_layout(
            xaxis=dict(
                title="Lap Number",
            ),
            yaxis=dict(
                title="",
                categoryorder='category ascending',
            ),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=50, b=0),
            coloraxis_colorbar=dict(
                title="Duration (s)",
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Show pit stop table
        st.dataframe(pitstop_df, use_container_width=True)