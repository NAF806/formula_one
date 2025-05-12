import plotly.express as px
from utils.helpers import get_team_colors

def create_driver_standings_chart(df):
    """
    Create a bar chart visualization for driver standings
    
    Args:
        df: DataFrame with driver standings data
        
    Returns:
        Plotly figure object or None if data is empty
    """
    if df.empty:
        return None
    
    team_colors = get_team_colors()
    
    # Create a copy for plotting and sort by position
    plot_df = df.copy().sort_values('Position')
    
    # Create list of colors matching each constructor
    colors = [team_colors.get(constructor, '#333333') for constructor in plot_df['Constructor']]
    
    fig = px.bar(
        plot_df, 
        x='Driver', 
        y='Points',
        text='Points',
        color='Constructor',
        color_discrete_map={team: color for team, color in zip(plot_df['Constructor'], colors)},
        height=500,
    )
    
    fig.update_layout(
        title="Driver Championship Points",
        xaxis_title="",
        yaxis_title="Points",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis={'categoryorder':'total descending'},
        showlegend=True,
        legend_title_text='Constructor',
        margin=dict(l=0, r=0, t=50, b=0),
    )
    
    fig.update_traces(
        texttemplate='%{text:.1f}',
        textposition='outside',
        marker_line_width=0,
        opacity=0.9,
    )
    
    return fig

def create_constructor_standings_chart(df):
    """
    Create a bar chart visualization for constructor standings
    
    Args:
        df: DataFrame with constructor standings data
        
    Returns:
        Plotly figure object or None if data is empty
    """
    if df.empty:
        return None
    
    team_colors = get_team_colors()
    
    # Create a copy for plotting and sort by position
    plot_df = df.copy().sort_values('Position')
    
    # Create list of colors matching each constructor
    colors = [team_colors.get(constructor, '#333333') for constructor in plot_df['Constructor']]
    
    fig = px.bar(
        plot_df, 
        x='Constructor', 
        y='Points',
        text='Points',
        color='Constructor',
        color_discrete_map={team: color for team, color in zip(plot_df['Constructor'], colors)},
        height=400,
    )
    
    fig.update_layout(
        title="Constructor Championship Points",
        xaxis_title="",
        yaxis_title="Points",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis={'categoryorder':'total descending'},
        showlegend=False,
        margin=dict(l=0, r=0, t=50, b=0),
    )
    
    fig.update_traces(
        texttemplate='%{text:.1f}',
        textposition='outside',
        marker_line_width=0,
        opacity=0.9,
    )
    
    return fig