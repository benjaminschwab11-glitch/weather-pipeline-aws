"""
Real-Time Weather Dashboard
Displays data from AWS RDS PostgreSQL
"""

import streamlit as st
import pandas as pd
import psycopg2
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(
    page_title="Weather Pipeline Dashboard",
    page_icon="🌤️",
    layout="wide"
)

# Database connection
@st.cache_resource
def get_db_connection():
    """Create database connection"""
    return psycopg2.connect(
        host=os.getenv('RDS_ENDPOINT'),
        database=os.getenv('RDS_DATABASE'),
        user=os.getenv('RDS_USERNAME'),
        password=os.getenv('RDS_PASSWORD'),
        port=os.getenv('RDS_PORT', '5432')
    )

# Load data with caching
@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_weather_data(hours=24):
    """Load recent weather data"""
    conn = get_db_connection()
    
    query = f'''
        SELECT 
            city,
            timestamp,
            temperature,
            feels_like,
            humidity,
            pressure,
            wind_speed,
            weather_condition,
            weather_description,
            data_quality_score,
            created_at
        FROM weather_observations
        WHERE timestamp >= NOW() - INTERVAL '{hours} hours'
        ORDER BY timestamp DESC
    '''
    
    df = pd.read_sql(query, conn)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    return df

# Header
st.title("🌤️ Real-Time Weather Pipeline Dashboard")
st.markdown("*Automated data collection every 15 minutes via AWS Lambda*")

# Sidebar
st.sidebar.header("Settings")
time_range = st.sidebar.selectbox(
    "Time Range",
    ["Last 24 Hours", "Last 48 Hours", "Last 7 Days"],
    index=0
)

hours_map = {
    "Last 24 Hours": 24,
    "Last 48 Hours": 48,
    "Last 7 Days": 168
}

# Load data
with st.spinner("Loading weather data..."):
    df = load_weather_data(hours_map[time_range])

if df.empty:
    st.warning("No data available for selected time range")
    st.stop()

# Current conditions
st.header("Current Conditions")

latest_df = df.groupby('city').first().reset_index()

cols = st.columns(5)
for i, (_, row) in enumerate(latest_df.iterrows()):
    with cols[i]:
        st.metric(
            label=row['city'],
            value=f"{row['temperature']:.1f}°F",
            delta=f"{row['feels_like'] - row['temperature']:.1f}°F feels like"
        )
        st.caption(f"💧 {row['humidity']}%")
        st.caption(f"🌬️ {row['wind_speed']:.1f} mph")
        st.caption(f"{row['weather_description'].title()}")

# Temperature trends
st.header("Temperature Trends")

fig_temp = px.line(
    df,
    x='timestamp',
    y='temperature',
    color='city',
    title=f"Temperature Over Time ({time_range})",
    labels={'temperature': 'Temperature (°F)', 'timestamp': 'Time'}
)
fig_temp.update_layout(height=400)
st.plotly_chart(fig_temp, use_container_width=True)

# Humidity comparison
col1, col2 = st.columns(2)

with col1:
    st.subheader("Humidity Distribution")
    fig_humidity = px.box(
        df,
        x='city',
        y='humidity',
        title="Humidity by City",
        labels={'humidity': 'Humidity (%)'}
    )
    st.plotly_chart(fig_humidity, use_container_width=True)

with col2:
    st.subheader("Temperature Distribution")
    fig_temp_box = px.box(
        df,
        x='city',
        y='temperature',
        title="Temperature by City",
        labels={'temperature': 'Temperature (°F)'}
    )
    st.plotly_chart(fig_temp_box, use_container_width=True)

# Pipeline stats
st.sidebar.header("Pipeline Stats")
total_records = len(df)
cities_tracked = df['city'].nunique()
latest_timestamp = df['timestamp'].max()
avg_quality = df['data_quality_score'].mean()

st.sidebar.metric("Total Records", f"{total_records:,}")
st.sidebar.metric("Cities Tracked", cities_tracked)
st.sidebar.metric("Avg Data Quality", f"{avg_quality:.1%}")
st.sidebar.info(f"Last updated: {latest_timestamp.strftime('%Y-%m-%d %H:%M:%S')}")

# Raw data
with st.expander("View Raw Data"):
    st.dataframe(
        df.sort_values('timestamp', ascending=False),
        use_container_width=True
    )

