import plotly.express as px
import plotly.graph_objects as go
from utils.helpers import get_team_colors, time_to_seconds

def create_race_results_positions(results_df):
    """
    Create a visualization of position changes during a race
    
    Args:
        results_df: DataFrame with race results
        
    Returns:
        Plotly figure object or None if data is empty
    """
    if results_df.empty:
        return None
    
    team_colors = get_team_colors()
    
    # Create a copy for plotting
    plot_df = results_df.copy()
    
    # Create a color mapping for each constructor
    constructor_colors = {constructor: team_colors.get(constructor, '#333333') 
                         for constructor in plot_df['Constructor'].unique()}
    
    # Set up position gain/loss
    plot_df['PositionChange'] = plot_df['Grid'] - plot_df['Position'].astype(int)
    plot_df['ChangeColor'] = plot_df['PositionChange'].apply(
        lambda x: 'green' if x > 0 else ('red' if x < 0 else 'gray')
    )
    
    # Create horizontal bar chart for position changes
    fig = go.Figure()
    
    # Sort by finishing position
    plot_df = plot_df.sort_values('Position')
    
    # Add bars for each driver
    for _, row in plot_df.iterrows():
        fig.add_trace(go.Bar(
            y=[row['Driver']],
            x=[abs(row['PositionChange'])] if row['PositionChange'] != 0 else [0.5],
            orientation='h',
            marker_color=row['ChangeColor'] if row['PositionChange'] != 0 else 'gray',
            text=f"{'+' if row['PositionChange'] > 0 else ''}{row['PositionChange']}" if row['PositionChange'] != 0 else 'No change',
            textposition='outside',
            name=row['Driver'],
            showlegend=False,
            hoverinfo='text',
            hovertext=f"{row['Driver']} ({row['Constructor']})<br>Start: P{row['Grid']}<br>Finish: P{row['Position']}<br>Change: {'+' if row['PositionChange'] > 0 else ''}{row['PositionChange']}"
        ))
    
    # Customize layout
    fig.update_layout(
        title="Position Changes (Start → Finish)",
        xaxis_title="Positions Gained/Lost",
        yaxis_title="",
        barmode='relative',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=min(400, 100 + 30 * len(plot_df)),  # Dynamic height based on number of drivers
        margin=dict(l=0, r=0, t=50, b=0),
    )
    
    return fig

def create_lap_times_chart(laps_df, driver_id=None):
    """
    Create a visualization of lap times during a race
    
    Args:
        laps_df: DataFrame with lap time data
        driver_id: Optional driver ID to filter by
        
    Returns:
        Plotly figure object or None if data is empty
    """
    if laps_df.empty:
        return None
    
    # Convert lap times to seconds for better visualization
    laps_df['TimeSeconds'] = laps_df['Time'].apply(time_to_seconds)
    
    # Filter by driver if specified
    if driver_id:
        filtered_df = laps_df[laps_df['DriverID'] == driver_id]
    else:
        filtered_df = laps_df
    
    if filtered_df.empty:
        return None
    
    # Create line chart
    fig = px.line(
        filtered_df, 
        x='Lap', 
        y='TimeSeconds',
        color='DriverID',
        labels={'TimeSeconds': 'Lap Time (seconds)', 'Lap': 'Lap Number'},
        title=f"Lap Times" + (f" for {driver_id}" if driver_id else ""),
        height=400,
    )
    
    fig.update_layout(
        xaxis=dict(
            dtick=1,
            title="Lap Number",
        ),
        yaxis=dict(
            title="Lap Time (seconds)",
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=50, b=0),
    )
    
    return fig