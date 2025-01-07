import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Set Streamlit to wide mode
st.set_page_config(layout="wide")

import os

data_file = "Edit_Review.csv"  # Replace with your file path
if os.path.exists(data_file):
    print("File exists!")
else:
    print("File not found. Check the path.")




# Preprocessing
df['Revinate Collected Date'] = pd.to_datetime(df['Revinate Collected Date'])
df['Review Date'] = pd.to_datetime(df['Review Date'])
df['Rating Category'] = df['Rating'].apply(lambda x: 'Good Review' if x >= 4.0 else 'Bad Review')
df['Review Month'] = df['Review Date'].dt.to_period('M').astype(str)




# Header
st.title("Restaurant Dashboard")

# Overall Section
st.header("Overall")




# Chart 1: Stacked Bar Chart
st.subheader("Chart 1: Review Count by Hotel and Rating Category")
bar_data = df.groupby(['Hotel', 'Rating Category']).size().reset_index(name='Count')
bar_chart = px.bar(
    bar_data, 
    x="Hotel", 
    y="Count", 
    color="Rating Category", 
    barmode="stack", 
    color_discrete_sequence=custom_colors, 
    title="Review Count by Hotel and Rating Category"
)
st.plotly_chart(bar_chart, use_container_width=True)

# Chart 2: Line Chart with Area
st.subheader("Chart 2: Average Monthly Ratings")
line_data = df.groupby(['Review Month'])['Rating'].mean().reset_index()
line_chart = px.area(
    line_data,
    x="Review Month",
    y="Rating",
    color_discrete_sequence=custom_colors,
    title="Average Monthly Ratings"
)
st.plotly_chart(line_chart, use_container_width=True)



