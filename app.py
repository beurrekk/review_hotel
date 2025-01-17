import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Set Streamlit to wide mode
st.set_page_config(layout="wide")

# Load data
uploaded_file = 'Edit_Review.csv'
df = pd.read_csv(uploaded_file, encoding='ISO-8859-1')

# Preprocess data
# Group review sites into 'Google' and 'OTA'
df['Review Group'] = df['Review Site'].apply(lambda x: 'Google' if x.lower() == 'google' else 'OTA')

# Chart 1: Stacked bar chart of review counts by hotel and review site
review_counts = df.groupby(['Hotel', 'Review Group']).size().reset_index(name='Count')
review_totals = review_counts.groupby('Hotel')['Count'].transform('sum')
review_counts['Percentage'] = review_counts['Count'] / review_totals * 100

fig1 = px.bar(
    review_counts,
    x='Hotel',
    y='Count',
    color='Review Group',
    text='Percentage',
    color_discrete_sequence=['#FCD5C6', '#567BA2'],  # OTA below, Google above
    title='Review Counts by Hotel and Review Site',
    labels={'Count': 'Number of Reviews', 'Hotel': 'Hotel Name', 'Review Group': 'Review Site'}
)
fig1.update_traces(texttemplate='%{text:.2f}%', textposition='inside')
fig1.update_layout(barmode='stack', xaxis={'categoryorder': 'total descending'})

# Chart 2: Horizontal bar chart of ratings distribution
filtered_hotel = st.selectbox('Select a Hotel for Rating Distribution:', df['Hotel'].unique())
filtered_data = df[(df['Hotel'] == filtered_hotel) & (df['Rating'] >= 4.0)]
rating_counts = filtered_data['Rating'].value_counts().reset_index()
rating_counts.columns = ['Rating', 'Count']

fig2 = px.bar(
    rating_counts.sort_values('Rating'),
    x='Count',
    y='Rating',
    orientation='h',
    title=f'Rating Distribution (4.0-5.0) for {filtered_hotel}',
    labels={'Count': 'Number of Ratings', 'Rating': 'Rating'},
    color_discrete_sequence=['#F2DD83']
)

# Chart 3: Scatter chart for Google vs OTA reviews by month
df['Revinate Collected Date'] = pd.to_datetime(df['Revinate Collected Date'], format='%d/%m/%Y')
df['Month'] = df['Revinate Collected Date'].dt.to_period('M')
monthly_counts = df.groupby(['Month', 'Review Group']).size().unstack(fill_value=0).reset_index()
monthly_counts.columns = ['Month', 'Google', 'OTA']

fig3 = px.scatter(
    monthly_counts,
    x='Google',
    y='OTA',
    title='Google vs OTA Reviews by Month',
    labels={'Google': 'Google Reviews Count', 'OTA': 'OTA Reviews Count'},
    text=monthly_counts['Month'].astype(str),
    color_discrete_sequence=['#9A8CB5']
)
fig3.update_traces(textposition='top center')

# Display the charts
st.title("Hotel Review Dashboard")
st.plotly_chart(fig1, use_container_width=True)
st.plotly_chart(fig2, use_container_width=True)
st.plotly_chart(fig3, use_container_width=True)
