import plotly.express as px

def create_calendar_map(races_df):
    """
    Create a world map visualization with race locations
    
    Args:
        races_df: DataFrame with race calendar data
        
    Returns:
        Plotly figure object or None if location data is missing
    """
    if races_df.empty:
        return None
    
    # Check if we have location data
    if not ('Circuit.Location.lat' in races_df.columns and 'Circuit.Location.long' in races_df.columns):
        return None
    
    # Create a DataFrame for mapping
    map_df = races_df[['round', 'raceName', 'Circuit.circuitName', 'date', 'Circuit.Location.lat', 'Circuit.Location.long', 'completed']].copy()
    map_df.rename(columns={
        'Circuit.Location.lat': 'lat',
        'Circuit.Location.long': 'lon',
        'raceName': 'Race',
        'Circuit.circuitName': 'Circuit'
    }, inplace=True)
    
    # Map colors based on race status (completed or upcoming)
    colors = map_df['completed'].map({True: 'red', False: 'blue'})
    
    fig = px.scatter_geo(
        map_df,
        lat='lat',
        lon='lon',
        hover_name='Race',
        hover_data=['Circuit', 'date'],
        color=map_df['completed'].map({True: 'Completed', False: 'Upcoming'}),
        color_discrete_map={'Completed': '#e10600', 'Upcoming': '#0600EF'},
        size=[10] * len(map_df),
        projection="natural earth",
        title="F1 Race Calendar",
        height=500,
    )
    
    fig.update_layout(
        margin=dict(l=0, r=0, t=50, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        geo=dict(
            showland=True,
            landcolor='rgb(243, 243, 243)',
            countrycolor='rgb(204, 204, 204)',
            showcountries=True,
            showocean=True,
            oceancolor='rgb(234, 242, 252)',
            showlakes=True,
            lakecolor='rgb(234, 242, 252)',
        ),
    )
    
    return fig