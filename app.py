import streamlit as st
import pandas as pd
import plotly.express as px

# Set Streamlit wide mode
st.set_page_config(layout="wide")

# Load data
uploaded_file = "Edit_Review.csv"
df = pd.read_csv(uploaded_file, encoding='ISO-8859-1')

# Preprocessing: Create a new column to categorize review sites
def categorize_review_site(site):
    if site.strip().lower() == 'google':
        return 'Google'
    else:
        return 'OTA'

df['Review Category'] = df['Review Site'].apply(categorize_review_site)

# Aggregate data for the stacked bar chart
agg_data = df.groupby(['Hotel', 'Review Category']).size().reset_index(name='Count')

# Create stacked bar chart
fig = px.bar(
    agg_data,
    x='Hotel',
    y='Count',
    color='Review Category',
    title='Count of Reviews by Hotel and Review Site Category',
    labels={'Count': 'Number of Reviews', 'Hotel': 'Hotel Name'},
    color_discrete_sequence=['#F2DD83', '#9A8CB5']  # Custom colors
)

# Header
st.title("Review Hotel Dashboard")

# Display the chart
st.plotly_chart(fig, use_container_width=True)
