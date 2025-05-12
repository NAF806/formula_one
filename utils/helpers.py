def get_team_colors():
    """
    Create F1-style color scheme for teams
    
    Returns:
        Dictionary with team names as keys and colors as values
    """
    return {
        'Red Bull': '#0600EF',
        'Ferrari': '#DC0000',
        'Mercedes': '#00D2BE',
        'McLaren': '#FF8700',
        'Aston Martin': '#006F62',
        'Alpine': '#0090FF',
        'Williams': '#005AFF',
        'AlphaTauri': '#2B4562',
        'Alfa Romeo': '#900000',
        'Haas F1 Team': '#FFFFFF',
        'Racing Point': '#F596C8',
        'Renault': '#FFF500',
        'Toro Rosso': '#469BFF',
        'Sauber': '#9B0000',
        'Force India': '#FF80C7',
        'Manor Marussia': '#323232',
        'Lotus F1': '#FFB800',
        'Marussia': '#6E0000',
        'Caterham': '#00A014',
        'Lotus': '#FFB800',
        'HRT': '#858585',
        'Virgin': '#C81118',
        'Brawn': '#00FF00',
        'Toyota': '#FF1E00',
        'Super Aguri': '#E2001A',
        'Honda': '#0D0028',
        'Spyker': '#FF6600',
        'Red Bull Racing': '#0600EF',
        'Midland': '#FF6600',
        'BMW Sauber': '#006DF0',
        'RBR-Honda': '#0600EF',
        'RB F1 Team': '#0600EF',
        'VCARB': '#5E8FAA'
    }

def time_to_seconds(time_str):
    """
    Convert lap time string to seconds
    
    Args:
        time_str: Time string in format "m:ss.ms" or "ss.ms"
        
    Returns:
        Float representing time in seconds, or None if invalid
    """
    if not time_str:
        return None
    try:
        if ":" in time_str:
            minutes, rest = time_str.split(':')
            seconds = float(rest)
            return int(minutes) * 60 + seconds
        else:
            return float(time_str)
    except:
        return None