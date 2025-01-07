import streamlit as st
import pandas as pd
import plotly.express as px

# Set Streamlit to wide mode
st.set_page_config(layout="wide")

# Define custom colors for charts
custom_colors = ['#F2DD83', '#CBD9EF', '#FCD5C6', '#9A8CB5', '#EB9861', '#72884B', '#567BA2']

# Load the dataset
data_file = "Edit_Review.csv"
try:
    df = pd.read_csv(data_file)
    st.success("Data loaded successfully!")
except Exception as e:
    st.error(f"Error loading CSV: {e}")
    st.stop()

# Preprocessing
df['Revinate Collected Date'] = pd.to_datetime(df['Revinate Collected Date'], errors='coerce')
df['Review Date'] = pd.to_datetime(df['Review Date'], errors='coerce')
df['Review Month'] = df['Review Date'].dt.to_period('M').astype(str)
df['Rating Category'] = df['Rating'].apply(lambda x: 'rating 4 up' if x > 3.9 else 'rating 0.5-3.9')

# Sidebar filter for hotels
hotels = ['All Hotels'] + sorted(df['Hotel'].unique())
selected_hotel = st.sidebar.selectbox("Select a Hotel", hotels)

# Filter data based on selected hotel
if selected_hotel != 'All Hotels':
    filtered_df = df[df['Hotel'] == selected_hotel]
else:
    filtered_df = df

# Main title
st.title("Hotel Review Dashboard")

# Text display: Overall
st.markdown("### Overall")

# Chart 1: Stacked Bar Chart - Count of Reviews by Hotel and Rating Category
st.subheader("Chart 1: Review Count by Hotel and Rating Category")
bar_data = filtered_df.groupby(['Hotel', 'Rating Category']).size().reset_index(name='Count')
bar_chart = px.bar(
    bar_data,
    x="Hotel",
    y="Count",
    color="Rating Category",
    barmode="stack",
    title="Review Count by Hotel and Rating Category",
    color_discrete_sequence=custom_colors
)
st.plotly_chart(bar_chart, use_container_width=True)

# Chart 2: Line Chart with Area - Average Monthly Ratings
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
