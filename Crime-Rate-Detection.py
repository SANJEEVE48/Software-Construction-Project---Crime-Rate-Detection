import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

@st.cache_data
def load_data(num_rows):
    data = {
        'Latitude': np.random.uniform(12.90, 13.10, num_rows),  
        'Longitude': np.random.uniform(80.10, 80.30, num_rows), 
        'Crime Type': np.random.choice(['Theft', 'Assault', 'Burglary', 'Vandalism', 'Other'], num_rows),
        'Reported Date': pd.to_datetime(np.random.choice(pd.date_range('2024-01-01', '2024-12-31'), num_rows)),
        'Severity': np.random.choice(['Low', 'Medium', 'High'], num_rows)
    }
    return pd.DataFrame(data)

num_rows = st.sidebar.slider("Number of Crime Incidents to Simulate", 100, 5000, 1000)
crime_data = load_data(num_rows)

st.title("Simplified Crime Rate Visualization")
st.markdown("Explore simulated crime incidents in the Chennai area.")

st.sidebar.header("Filters")
selected_crime_types = st.sidebar.multiselect("Crime Type", crime_data['Crime Type'].unique())
selected_severity = st.sidebar.multiselect("Severity", crime_data['Severity'].unique())
default_start_date = crime_data['Reported Date'].min().date()
default_end_date = crime_data['Reported Date'].max().date()
date_range_input = st.sidebar.date_input("Date Range", [default_start_date, default_end_date])

start_date = date_range_input[0]
end_date = date_range_input[1]

filtered_data = crime_data[
    (crime_data['Crime Type'].isin(selected_crime_types) if selected_crime_types else True) &
    (crime_data['Severity'].isin(selected_severity) if selected_severity else True) &
    (crime_data['Reported Date'].dt.date >= start_date) &
    (crime_data['Reported Date'].dt.date <= end_date)
]

st.subheader(f"Filtered Crime Incidents: {len(filtered_data)}")
if not filtered_data.empty:
    st.dataframe(filtered_data)

    st.subheader("Crime Locations on Map")
    midpoint_lat = (crime_data['Latitude'].min() + crime_data['Latitude'].max()) / 2
    midpoint_lon = (crime_data['Longitude'].min() + crime_data['Longitude'].max()) / 2

    fig_map = px.scatter_mapbox(
        filtered_data,
        lat="Latitude",
        lon="Longitude",
        color="Crime Type",
        size_max=15,
        zoom=10,
        height=500,
        center={"lat": midpoint_lat, "lon": midpoint_lon},
        mapbox_style="open-street-map",
        title="Crime Incident Locations"
    )
    st.plotly_chart(fig_map)

    st.subheader("Crime Type Distribution")
    crime_counts = filtered_data['Crime Type'].value_counts().reset_index()
    crime_counts.columns = ['Crime Type', 'Count']
    fig_bar = px.bar(crime_counts, x='Crime Type', y='Count', title="Number of Incidents by Type")
    st.plotly_chart(fig_bar)

    st.subheader("Severity Distribution")
    severity_counts = filtered_data['Severity'].value_counts().reset_index()
    severity_counts.columns = ['Severity', 'Count']
    fig_pie = px.pie(severity_counts, names='Severity', values='Count', title="Distribution by Severity")
    st.plotly_chart(fig_pie)

else:
    st.warning("No crime incidents match the selected filters.")
