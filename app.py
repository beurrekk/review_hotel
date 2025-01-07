import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Custom colors
custom_colors = ['#F2DD83', '#CBD9EF', '#FCD5C6', '#9A8CB5', '#EB9861', '#72884B', '#567BA2']

# Configure Streamlit layout
st.set_page_config(page_title="Hotel Reviews Dashboard", layout="wide")

# Load data
uploaded_file = "/mnt/data/Edit_Review.csv"  # Replace with your actual file path
data = pd.read_csv(uploaded_file)

# Data preprocessing
data['Revinate Collected Date'] = pd.to_datetime(data['Revinate Collected Date'], format='%d/%m/%Y')
data['Review Date'] = pd.to_datetime(data['Review Date'], format='%d/%m/%Y')
data['Month'] = data['Review Date'].dt.to_period('M').astype(str)
data['Rating Group'] = data['Rating'].apply(lambda x: 'Rating 4 up' if x >= 4.0 else 'Rating 0.5-3.9')

# Sidebar
st.sidebar.header("Filters")
selected_hotel = st.sidebar.multiselect("Select Hotel(s)", options=data['Hotel'].unique(), default=data['Hotel'].unique())

# Filter data by selected hotels
filtered_data = data[data['Hotel'].isin(selected_hotel)]

# Text Header
st.title("Overall")

# Chart 1: Stacked Bar Chart
grouped_bar = filtered_data.groupby(['Hotel', 'Rating Group']).size().reset_index(name='Count')
bar_chart = px.bar(grouped_bar, x='Hotel', y='Count', color='Rating Group', 
                   color_discrete_sequence=custom_colors, barmode='stack', 
                   title="Count of Reviews by Hotel and Rating Group")
st.plotly_chart(bar_chart, use_container_width=True)

# Chart 2: Line Chart with Area
grouped_line = filtered_data.groupby(['Month'])['Rating'].mean().reset_index()
line_chart = px.area(grouped_line, x='Month', y='Rating', 
                     title="Average Rating by Month", 
                     color_discrete_sequence=[custom_colors[3]])
st.plotly_chart(line_chart, use_container_width=True)

# Instructions for Deployment
st.markdown("### Deployment Instructions")
st.write("To deploy this app on Streamlit Community Cloud:")
st.code("""1. Push this script and the CSV file to a GitHub repository.
2. Go to https://streamlit.io/cloud.
3. Connect your GitHub repository.
4. Deploy the app by selecting this script as the main file.
""", language="text")
