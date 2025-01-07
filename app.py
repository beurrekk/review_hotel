import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Set Streamlit to wide mode
st.set_page_config(layout="wide")

# Load the dataset
uploaded_file = '/mnt/data/Edit_Review.csv'
df = pd.read_csv(uploaded_file, encoding='ISO-8859-1')

# Parse dates and extract relevant fields
df['Review Date'] = pd.to_datetime(df['Review Date'], format='%d/%m/%Y')
df['Month'] = df['Review Date'].dt.to_period('M').astype(str)

# Categorize ratings
def categorize_rating(rating):
    return 'Rating 4 Up' if rating >= 4 else 'Rating 0.5-3.9'

df['Rating Group'] = df['Rating'].apply(categorize_rating)

# Chart 1: Bar chart for review count by hotel
bar_data = df.groupby(['Hotel', 'Rating Group']).size().reset_index(name='Count')
fig_bar = px.bar(
    bar_data, 
    x='Hotel', 
    y='Count', 
    color='Rating Group',
    title='Review Count by Hotel and Rating Group',
    color_discrete_sequence=['#9A8CB5', '#EB9861']
)

# Chart 2: Line chart for average rating by month
line_data = df.groupby('Month').agg({'Rating': 'mean'}).reset_index()
fig_line = px.area(
    line_data, 
    x='Month', 
    y='Rating', 
    title='Average Rating by Month',
    color_discrete_sequence=['#567BA2']
)

# Streamlit layout
st.title('Hotel Reviews Dashboard')
st.text('Overall')

# Display charts
st.plotly_chart(fig_bar, use_container_width=True)
st.plotly_chart(fig_line, use_container_width=True)

# Show raw data
st.write('Raw Data:')
st.dataframe(df)
