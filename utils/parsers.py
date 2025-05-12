import pandas as pd
import streamlit as st
from datetime import datetime
from utils.api import get_f1_data

@st.cache_data(ttl=3600)
def parse_driver_standings(year):
    """
    Parse driver standings data from API
    
    Args:
        year: The year to fetch standings for
        
    Returns:
        DataFrame with driver standings
    """
    data = get_f1_data(f"{year}/driverStandings.json")
    if not data:
        return pd.DataFrame()
    
    lst = data['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']
    rows = []
    for e in lst:
        rows.append({
            'Position': int(e['position']),
            'Driver': f"{e['Driver']['givenName']} {e['Driver']['familyName']}",
            'Constructor': e['Constructors'][0]['name'],
            'Points': float(e['points']),
            'Wins': int(e['wins'])
        })
    return pd.DataFrame(rows)

@st.cache_data(ttl=3600)
def parse_constructor_standings(year):
    """
    Parse constructor standings data from API
    
    Args:
        year: The year to fetch standings for
        
    Returns:
        DataFrame with constructor standings
    """
    data = get_f1_data(f"{year}/constructorStandings.json")
    if not data:
        return pd.DataFrame()
    
    lst = data['MRData']['StandingsTable']['StandingsLists'][0]['ConstructorStandings']
    rows = []
    for e in lst:
        rows.append({
            'Position': int(e['position']),
            'Constructor': e['Constructor']['name'],
            'Points': float(e['points']),
            'Wins': int(e['wins'])
        })
    return pd.DataFrame(rows)

@st.cache_data(ttl=3600)
def parse_races(year):
    """
    Parse race calendar data from API
    
    Args:
        year: The year to fetch races for
        
    Returns:
        DataFrame with race calendar
    """
    data = get_f1_data(f"{year}/races.json")
    if not data:
        return pd.DataFrame()
    
    lst = data['MRData']['RaceTable']['Races']
    df = pd.json_normalize(lst)
    df['date'] = pd.to_datetime(df['date'])
    
    # Add a column for races that have already happened
    current_date = datetime.now()
    df['completed'] = df['date'] < current_date
    
    return df

@st.cache_data(ttl=3600)
def parse_results(year, rnd):
    """
    Parse race results data from API
    
    Args:
        year: The year of the race
        rnd: The round number
        
    Returns:
        DataFrame with race results
    """
    data = get_f1_data(f"{year}/{rnd}/results.json")
    if not data or 'MRData' not in data or 'RaceTable' not in data['MRData'] or 'Races' not in data['MRData']['RaceTable'] or len(data['MRData']['RaceTable']['Races']) == 0:
        return pd.DataFrame()
    
    lst = data['MRData']['RaceTable']['Races'][0]['Results']
    rows = []
    for e in lst:
        time = e.get('Time', {}).get('time', None)
        rows.append({
            'Position': int(e['position']),
            'Driver': f"{e['Driver']['givenName']} {e['Driver']['familyName']}",
            'Constructor': e['Constructor']['name'],
            'Grid': int(e['grid']),
            'Laps': int(e['laps']),
            'Time': time,
            'Status': e['status'],
            'Points': float(e['points'])
        })
    return pd.DataFrame(rows)

@st.cache_data(ttl=3600)
def parse_qualifying(year, rnd):
    """
    Parse qualifying results data from API
    
    Args:
        year: The year of the qualifying
        rnd: The round number
        
    Returns:
        DataFrame with qualifying results
    """
    data = get_f1_data(f"{year}/{rnd}/qualifying.json")
    if not data or 'MRData' not in data or 'RaceTable' not in data['MRData'] or 'Races' not in data['MRData']['RaceTable'] or len(data['MRData']['RaceTable']['Races']) == 0:
        return pd.DataFrame()
    
    lst = data['MRData']['RaceTable']['Races'][0].get('QualifyingResults', [])
    rows = []
    for e in lst:
        rows.append({
            'Position': int(e['position']),
            'Driver': f"{e['Driver']['givenName']} {e['Driver']['familyName']}",
            'Constructor': e['Constructor']['name'],
            'Q1': e.get('Q1'), 'Q2': e.get('Q2'), 'Q3': e.get('Q3')
        })
    return pd.DataFrame(rows)

@st.cache_data(ttl=3600)
def parse_sprint(year, rnd):
    """
    Parse sprint race results data from API
    
    Args:
        year: The year of the sprint
        rnd: The round number
        
    Returns:
        DataFrame with sprint results
    """
    data = get_f1_data(f"{year}/{rnd}/sprint.json")
    if not data:
        return pd.DataFrame()
    
    mr = data.get('MRData', {})
    # Safely get Sprint Races
    sprint_info = mr.get('SprintTable', {}).get('Races', [])
    if not sprint_info:
        return pd.DataFrame()
    
    results_list = sprint_info[0].get('SprintResults', [])
    rows = []
    for e in results_list:
        time_str = e.get('Time', {}).get('time', "")
        rows.append({
            'Position': int(e['position']),
            'Driver': f"{e['Driver']['givenName']} {e['Driver']['familyName']}",
            'Constructor': e['Constructor']['name'],
            'Time': time_str,
            'Points': float(e['points'])
        })
    return pd.DataFrame(rows)

@st.cache_data(ttl=3600)
def parse_pitstops(year, rnd):
    """
    Parse pit stop data from API
    
    Args:
        year: The year of the race
        rnd: The round number
        
    Returns:
        DataFrame with pit stop data
    """
    data = get_f1_data(f"{year}/{rnd}/pitstops.json")
    if not data or 'MRData' not in data or 'RaceTable' not in data['MRData'] or 'Races' not in data['MRData']['RaceTable'] or len(data['MRData']['RaceTable']['Races']) == 0:
        return pd.DataFrame()
    
    lst = data['MRData']['RaceTable']['Races'][0].get('PitStops', [])
    rows = []
    for e in lst:
        rows.append({
            'DriverID': e['driverId'],
            'Stop': int(e['stop']),
            'Lap': int(e['lap']),
            'Duration': e['duration']
        })
    return pd.DataFrame(rows)

@st.cache_data(ttl=3600)
def parse_laps(year, rnd, driver_id=None):
    """
    Parse lap time data from API
    
    Args:
        year: The year of the race
        rnd: The round number
        driver_id: Optional driver ID to filter by
        
    Returns:
        DataFrame with lap time data
    """
    # Safely fetch lap data; may not exist for all rounds/drivers
    ep = f"{year}/{rnd}/laps.json"
    if driver_id:
        ep = f"{year}/{rnd}/drivers/{driver_id}/laps.json"
    
    data = get_f1_data(ep)
    if not data:
        return pd.DataFrame()
    
    mr = data.get('MRData', {})
    # Navigate to RaceTable → Races → Laps
    races = mr.get('RaceTable', {}).get('Races', [])
    if not races or 'Laps' not in races[0]:
        return pd.DataFrame()
    
    laps_list = races[0].get('Laps', [])
    rows = []
    for lap in laps_list:
        lap_num = int(lap.get('number', 0))
        timings = lap.get('Timings', [])
        for e in timings:
            rows.append({
                'Lap': lap_num,
                'DriverID': e.get('driverId'),
                'Time': e.get('time')
            })
    
    # Return the dataframe
    if not rows:
        return pd.DataFrame()
    
    df = pd.DataFrame(rows)
    return df

@st.cache_data(ttl=3600)
def get_race_details(year, rnd):
    """
    Helper function to get race details for header
    
    Args:
        year: The year of the race
        rnd: The round number
        
    Returns:
        Dictionary with race details
    """
    races = parse_races(year)
    if races.empty:
        return None
    
    try:
        race = races[races['round'] == rnd].iloc[0]
        return {
            'name': race.get('raceName', f"Round {rnd}"),
            'circuit': race.get('Circuit.circuitName', ""),
            'date': race.get('date', ""),
            'locality': race.get('Circuit.Location.locality', ""),
            'country': race.get('Circuit.Location.country', ""),
        }
    except:
        return None