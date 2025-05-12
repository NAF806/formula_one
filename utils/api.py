import streamlit as st
import requests

@st.cache_data(ttl=3600)
def get_f1_data(endpoint):
    """
    Base API call function with loading indicator
    
    Args:
        endpoint: The API endpoint to fetch data from
        
    Returns:
        JSON response from the API or None if error
    """
    BASE_URL = "http://api.jolpi.ca/ergast/f1"
    url = f"{BASE_URL}/{endpoint}"
    try:
        resp = requests.get(url)
        if resp.status_code == 200:
            return resp.json()
        else:
            st.error(f"API error {resp.status_code}: Could not fetch data from {endpoint}")
            return None
    except Exception as e:
        st.error(f"Connection error: {str(e)}")
        return None