import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Set Streamlit to wide mode
st.set_page_config(layout="wide")

# Check if the file exists
data_file = "Edit_Review.csv"  # Replace with your file path
if os.path.exists(data_file):
    st.success("File exists!")
else:
    st.error("File not found. Please check the path and ensure 'Edit_Review.csv' is in the correct location.")
    st.stop()

# Load the dataset
df = pd.read_csv(data_file)

# Preprocessing
df['Revinate Collected Date'] = pd.to_datetime(df['Revinate Collected Date'], errors='coerce')
df['Review Date'] = pd.to_datetime(df['Review Date'], errors='coerce')
df['Rating Category'] = df['Rating'].apply(lambda x: 'Good Review' if x > 3.9 else 'Bad Review')
df['Review Month'] = df['Review Date'].dt.to_period('M').astype(str)

# Sidebar filter for hotels
hotels = ['All Hotels'] + sorted(df['Hotel'].unique().tolist())
selected_hotel = st.sidebar.selectbox("Select a Hotel", hotels)

# Filter data based on selection
if selected_hotel != 'All Hotels':
    filtered_df = df[df['Hotel'] == selected_hotel]
else:
    filtered_df = df

st.markdown("### Overall")

# Chart 1: Stacked Bar Chart
st.subheader("Chart 1: Review Count by Hotel and Rating Category")
bar_data = filtered_df.groupby(['Hotel', 'Rating Category']).size().reset_index(name='Count')
bar_chart = px.bar(
    bar_data,
    x="Hotel",
    y="Count",
    color="Rating Category",
    barmode="stack",
    title="Review Count by Hotel and Rating Category",
    color_discrete_sequence=['#F2DD83', '#9A8CB5']
)
st.plotly_chart(bar_chart, use_container_width=True)

# Chart 2: Line Chart with Area
st.subheader("Chart 2: Average Monthly Ratings")
line_data = filtered_df.groupby(['Review Month'])['Rating'].mean().reset_index()
line_chart = px.area(
    line_data,
    x="Review Month",
    y="Rating",
    title="Average Monthly Ratings",
    color_discrete_sequence=['#CBD9EF']
)
st.plotly_chart(line_chart, use_container_width=True)
