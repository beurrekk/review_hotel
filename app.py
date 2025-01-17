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

# Calculate percentages
agg_total = agg_data.groupby('Hotel')['Count'].transform('sum')
agg_data['Percentage'] = (agg_data['Count'] / agg_total) * 100

# Create stacked bar chart with percentages
fig = px.bar(
    agg_data,
    x='Hotel',
    y='Count',
    color='Review Category',
    text=agg_data['Percentage'].apply(lambda x: f"{x:.1f}%"),
    title='Count of Reviews by Hotel and Review Site Category',
    labels={'Count': 'Number of Reviews', 'Hotel': 'Hotel Name'},
    color_discrete_sequence=['#F2DD83', '#9A8CB5']  # Custom colors
)

fig.update_traces(textposition='inside')

# Header
st.title("Review Hotel Dashboard")

# Display the stacked bar chart
st.plotly_chart(fig, use_container_width=True)

# 2nd Chart: Horizontal bar chart for rating counts
st.header("Rating Distribution")

# Filter for selected hotel
selected_hotel = st.selectbox("Select a Hotel", options=df['Hotel'].unique())
filtered_df = df[df['Hotel'] == selected_hotel]

# Aggregate rating data
rating_data = filtered_df['Rating'].value_counts().reset_index()
rating_data.columns = ['Rating', 'Count']
rating_data.sort_values('Rating', inplace=True)

# Create horizontal bar chart
fig2 = px.bar(
    rating_data,
    x='Count',
    y='Rating',
    orientation='h',
    title=f'Rating Distribution for {selected_hotel}',
    labels={'Count': 'Number of Ratings', 'Rating': 'Rating'},
    color_discrete_sequence=['#EB9861']  # Custom color
)

# Display the horizontal bar chart
st.plotly_chart(fig2, use_container_width=True)
