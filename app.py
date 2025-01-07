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

# Create two columns for charts
col1, col2 = st.columns(2)

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
col1.plotly_chart(chart1, use_container_width=True)

# Chart 2: Combined bar and line chart for average rating by month and hotel
chart2_data = df.groupby(['Month', 'Hotel'])['Rating'].mean().reset_index()
overall_avg = df.groupby('Month')['Rating'].mean().reset_index()
chart2_data['Month'] = chart2_data['Month'].astype(str)
overall_avg['Month'] = overall_avg['Month'].astype(str)

fig = go.Figure()

# Add bar chart for overall average rating by month
fig.add_trace(go.Bar(
    x=overall_avg['Month'],
    y=overall_avg['Rating'],
    name='Overall Average Rating',
    marker_color='#F2DD83'
))

# Add line chart for average rating by hotel
for hotel in chart2_data['Hotel'].unique():
    hotel_data = chart2_data[chart2_data['Hotel'] == hotel]
    fig.add_trace(go.Scatter(
        x=hotel_data['Month'],
        y=hotel_data['Rating'],
        mode='lines',  # Line chart without markers
        name=f'{hotel} Average Rating'
    ))

fig.update_layout(
    title="Average Rating by Month and Hotel",
    xaxis_title="Month",
    yaxis_title="Average Rating",
    yaxis_range=[4.4, 5],
    barmode='group',
    legend_title="Legend",
    template="plotly_white"
)
col2.plotly_chart(fig, use_container_width=True)
