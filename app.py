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

# Group Review Sites
valid_sites = ['Google', 'Ctrip', 'Booking.com', 'Agoda']
df['Review Site Grouped'] = df['Review Site'].apply(lambda x: x if x in valid_sites else 'Other')

# Define custom colors
custom_colors = ['#F2DD83', '#9A8CB5', '#CBD9EF', '#FCD5C6', '#EB9861', '#72884B', '#567BA2']

# Header
st.title("Review Hotel Dashboard")

# Overall Section
st.header("Overall")

# Hotel-specific pie charts (Charts 1-7)
hotel_list = [
    'Altera Hotel and Residence',
    'Arbour Hotel and Residence Pattaya, Thailand',
    'Arden Hotel and Residence',
    'Aster Hotel and Residence Pattaya',
    'Hotel Amber Pattaya',
    'Hotel Amber Sukhumvit 85',
    'The Grass Serviced Suites Pattaya',
]

# Render charts 1-4 in one row
st.markdown("### Ratings by Hotel")
col1, col2, col3, col4 = st.columns(4)
for i, hotel in enumerate(hotel_list[:4]):
    with [col1, col2, col3, col4][i]:
        hotel_data = df[df['Hotel'] == hotel]
        pie_chart = px.pie(
            hotel_data,
            names='Rating Group',
            title=hotel,
            color='Rating Group',
            color_discrete_map={'rating 4 up': '#F2DD83', 'rating 0.5-3.9': '#9A8CB5'}
        )
        st.plotly_chart(pie_chart, use_container_width=True)

# Render charts 5-7 in another row
col5, col6, col7 = st.columns(3)
for i, hotel in enumerate(hotel_list[4:]):
    with [col5, col6, col7][i]:
        hotel_data = df[df['Hotel'] == hotel]
        pie_chart = px.pie(
            hotel_data,
            names='Rating Group',
            title=hotel,
            color='Rating Group',
            color_discrete_map={'rating 4 up': '#F2DD83', 'rating 0.5-3.9': '#9A8CB5'}
        )
        st.plotly_chart(pie_chart, use_container_width=True)

# Chart 8: Bar chart for count of reviews by Review Site
st.markdown("---")
st.markdown("### Review Count by Review Site")
review_site_data = df.groupby(['Review Site Grouped', 'Hotel']).size().reset_index(name='Count')
review_site_chart = px.bar(
    review_site_data,
    x='Hotel',
    y='Count',
    color='Review Site Grouped',
    title="Review Count Distribution by Review Site",
    color_discrete_sequence=custom_colors
)
review_site_chart.update_layout(xaxis={'categoryorder': 'total descending'})
st.plotly_chart(review_site_chart, use_container_width=True)

# Chart 9: Combined bar and line chart for average rating by month and hotel
st.markdown("---")
st.markdown("### Average Rating by Month and Hotel")
chart9_data = df.groupby(['Month', 'Hotel'])['Rating'].mean().reset_index()
overall_avg = df.groupby('Month')['Rating'].mean().reset_index()
chart9_data['Month'] = chart9_data['Month'].astype(str)
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
for hotel in chart9_data['Hotel'].unique():
    hotel_data = chart9_data[chart9_data['Hotel'] == hotel]
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
st.plotly_chart(fig, use_container_width=True)
