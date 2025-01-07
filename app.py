import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Set Streamlit wide mode
st.set_page_config(layout="wide", page_title="Hotel Reviews Dashboard")

# Load data
uploaded_file = "Edit_Review.csv"
df = pd.read_csv(uploaded_file, encoding='ISO-8859-1')

# Data preprocessing
df['Rating Group'] = df['Rating'].apply(lambda x: 'rating 4 up' if x >= 4 else 'rating 0.5-3.9')
df['Review Date'] = pd.to_datetime(df['Review Date'], format="%d/%m/%Y")
df['Month'] = df['Review Date'].dt.to_period('M')

# Define custom colors
custom_colors = ['#F2DD83', '#9A8CB5','#CBD9EF', '#FCD5C6',  '#EB9861', '#72884B', '#567BA2']



# Header
st.title("Restaurant Dashboard")

# Overall Section
st.header("Overall")


# Chart 1: Bar chart for count of reviews by hotel
chart1_data = df.groupby(['Hotel', 'Rating Group']).size().reset_index(name='Count')
chart1 = px.bar(
    chart1_data,
    x='Hotel',
    y='Count',
    color='Rating Group',
    barmode='stack',
    color_discrete_sequence=['#9A8CB5', '#F2DD83'],
    title="Review Counts by Hotel and Rating Group"
)
st.plotly_chart(chart1, use_container_width=True)

# Chart 2: Line chart with area for average rating by month
chart2_data = df.groupby('Month')['Rating'].mean().reset_index()
chart2_data['Month'] = chart2_data['Month'].astype(str)
chart2 = px.area(
    chart2_data,
    x='Month',
    y='Rating',
    title="Average Rating by Month",
    color_discrete_sequence=['#9A8CB5']
)
st.plotly_chart(chart2, use_container_width=True)

