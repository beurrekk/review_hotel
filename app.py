import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load data
uploaded_file = "Edit_Review.csv"
df = pd.read_csv(uploaded_file, encoding='ISO-8859-1')

# Load data
uploaded_file = "Edit_Review.csv"
df = pd.read_excel(uploaded_file)

# Define custom colors
colors = ['#F2DD83', '#9A8CB5','#CBD9EF', '#FCD5C6',  '#EB9861', '#72884B', '#567BA2']

# Header
st.title("Review Hotel Dashboard")

# Preprocess data
df['Review Site'] = df['Review Site'].apply(lambda x: 'Google' if x == 'Google' else 'OTA')
review_counts = df.groupby(['Hotel Name', 'Review Site']).size().reset_index(name='Count')
pivot_data = review_counts.pivot(index='Hotel Name', columns='Review Site', values='Count').fillna(0)

# Create the stacked bar chart
fig = go.Figure()

for idx, review_site in enumerate(pivot_data.columns):
    fig.add_trace(go.Bar(
        x=pivot_data.index,
        y=pivot_data[review_site],
        name=review_site,
        marker_color=colors[idx]
    ))

# Customize chart layout
fig.update_layout(
    barmode='stack',
    title='Review Counts by Hotel and Review Site',
    xaxis_title='Hotel Name',
    yaxis_title='Count of Reviews',
    legend_title='Review Site',
    template='plotly_white'
)

# Display the chart in Streamlit
st.plotly_chart(fig)
