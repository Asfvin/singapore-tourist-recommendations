import streamlit as st
import weather as ws
import streamlit.components.v1 as components
import folium
from streamlit_folium import st_folium
import location as lc

# Include widgets
# add_selectbox = st.sidebar.selectbox("Use Genie?", ("Yes", "No"))

st.title("Singapore Tourism App")
st.divider()

# Create three columns
col1, col2, col3 = st.columns(3)
col4, col5 = st.columns(2)
col6, col7 = st.columns(2)

col1.metric(label="Current Time", value=f"{ws.get_current_date_time()}", border=True)
col2.metric(label="Current Temperature", value=f"{ws.get_current_temp()} °C", border=True)
col3.metric(label="Current Weather", value=f"{ws.return_current_rainfall()}", border=True)

with col4.expander("Weather Forecasts...", expanded=False):
    temporal_weather = ws.get_weather_forecast()
    st.write(f"Current Forecasts for {temporal_weather[0]['timePeriod']['text']}")
    st.write(f"East {temporal_weather[0]['regions']['east']['text']}")
    st.write(f"Central {temporal_weather[0]['regions']['central']['text']}")
    st.write(f"South {temporal_weather[0]['regions']['south']['text']}")
    st.write(f"North {temporal_weather[0]['regions']['north']['text']}")

pollutant_data = ws.get_current_pollutant()
col5.dataframe(pollutant_data, use_container_width=True)


with col6.container():
    st.header("Databricks AI/ BI Dashboard")
    components.iframe("https://example.com", height=500)


with col7.container():
    user_lat, user_long = lc.get_current_location()
    # Create a folium map
    user_map = folium.Map(location=[user_lat, user_long], zoom_start=12)
    folium.Marker(
        location=[user_lat, user_long], popup="You are here!", icon=lc.icon_star
    ).add_to(user_map)

    for k, v in lc.SINGAPORE_ATTRACTIONS.items():
        folium.Marker(
            location=[v["lat"], v["lon"]],
            popup=k,
            icon=lc.icon_attraction,
        ).add_to(user_map)

    st.header("Interactive Map")
    st_folium(user_map, width=700, height=500)
