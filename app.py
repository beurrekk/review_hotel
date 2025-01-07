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
st.title("Review Hotel Dashboard")

# Overall Section
st.header("Overall")

# Chart 1: Pie chart for Altera Hotel And Residence
altera_data = df[df['Hotel'] == 'Altera Hotel And Residence']
altera_pie = px.pie(
    altera_data,
    names='Rating Group',
    title="Altera Hotel And Residence: Rating Distribution",
    color='Rating Group',
    color_discrete_map={'rating 4 up': '#9A8CB5', 'rating 0.5-3.9': '#F2DD83'}
)
st.plotly_chart(altera_pie, use_container_width=True)

# Chart 2: Pie chart for Arbour Hotel And Residence Pattaya, Thailand
arbour_data = df[df['Hotel'] == 'Arbour Hotel And Residence Pattaya, Thailand']
arbour_pie = px.pie(
    arbour_data,
    names='Rating Group',
    title="Arbour Hotel And Residence Pattaya: Rating Distribution",
    color='Rating Group',
    color_discrete_map={'rating 4 up': '#9A8CB5', 'rating 0.5-3.9': '#F2DD83'}
)
st.plotly_chart(arbour_pie, use_container_width=True)

# Chart 3: Pie chart for Arden Hotel and Residence
arden_data = df[df['Hotel'] == 'Arden Hotel and Residence']
arden_pie = px.pie(
    arden_data,
    names='Rating Group',
    title="Arden Hotel and Residence: Rating Distribution",
    color='Rating Group',
    color_discrete_map={'rating 4 up': '#9A8CB5', 'rating 0.5-3.9': '#F2DD83'}
)
st.plotly_chart(arden_pie, use_container_width=True)

# Chart 4: Pie chart for Aster Hotel and Residence Pattaya
aster_data = df[df['Hotel'] == 'Aster Hotel and Residence Pattaya']
aster_pie = px.pie(
    aster_data,
    names='Rating Group',
    title="Aster Hotel and Residence Pattaya: Rating Distribution",
    color='Rating Group',
    color_discrete_map={'rating 4 up': '#9A8CB5', 'rating 0.5-3.9': '#F2DD83'}
)
st.plotly_chart(aster_pie, use_container_width=True)

# Create a new row for the next set of charts
st.markdown("---")

# Chart 5: Pie chart for Hotel Amber Pattaya
amber_pattaya_data = df[df['Hotel'] == 'Hotel Amber Pattaya']
amber_pattaya_pie = px.pie(
    amber_pattaya_data,
    names='Rating Group',
    title="Hotel Amber Pattaya: Rating Distribution",
    color='Rating Group',
    color_discrete_map={'rating 4 up': '#9A8CB5', 'rating 0.5-3.9': '#F2DD83'}
)
st.plotly_chart(amber_pattaya_pie, use_container_width=True)

# Chart 6: Pie chart for Hotel Amber Sukhumvit 85
amber_sukhumvit_data = df[df['Hotel'] == 'Hotel Amber Sukhumvit 85']
amber_sukhumvit_pie = px.pie(
    amber_sukhumvit_data,
    names='Rating Group',
    title="Hotel Amber Sukhumvit 85: Rating Distribution",
    color='Rating Group',
    color_discrete_map={'rating 4 up': '#9A8CB5', 'rating 0.5-3.9': '#F2DD83'}
)
st.plotly_chart(amber_sukhumvit_pie, use_container_width=True)

# Chart 7: Pie chart for The Grass Serviced Suites Pattaya
grass_data = df[df['Hotel'] == 'The Grass Serviced Suites Pattaya']
grass_pie = px.pie(
    grass_data,
    names='Rating Group',
    title="The Grass Serviced Suites Pattaya: Rating Distribution",
    color='Rating Group',
    color_discrete_map={'rating 4 up': '#9A8CB5', 'rating 0.5-3.9': '#F2DD83'}
)
st.plotly_chart(grass_pie, use_container_width=True)

# Create a new row for the next chart
st.markdown("---")

# Chart 8: Stacked bar chart for count of reviews by Review Site
chart8_data = df.groupby(['Hotel', 'Review Site']).size().reset_index(name='Count')
chart8 = px.bar(
    chart8_data,
    x='Hotel',
    y='Count',
    color='Review Site',
    title="Review Count Distribution by Review Site",
    color_discrete_sequence=custom_colors
)
chart8.update_layout(xaxis={'categoryorder': 'total descending'})
st.plotly_chart(chart8, use_container_width=True)

# Create a new row for the next chart
st.markdown("---")

# Chart 9: Combined bar and line chart for average rating by month and hotel
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
