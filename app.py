import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Set Streamlit wide mode
st.set_page_config(layout="wide")

# Load data
uploaded_file = "Edit_Review.csv"
df = pd.read_csv(uploaded_file, encoding='ISO-8859-1')

# Define custom colors
colors = ['#F2DD83', '#9A8CB5','#CBD9EF', '#FCD5C6',  '#EB9861', '#72884B', '#567BA2']

# Header
st.title("Review Hotel Dashboard")

# Prepare data for Chart 1 (Stacked Bar Chart)
df['Review Group'] = df['Review Site'].apply(lambda x: 'Google' if x == 'Google' else 'OTA')
chart1_data = df.groupby(['Hotel', 'Review Group']).size().reset_index(name='Count')
chart1_pivot = chart1_data.pivot(index='Hotel', columns='Review Group', values='Count').fillna(0)
chart1_pivot['Total'] = chart1_pivot.sum(axis=1)
chart1_pivot = chart1_pivot.sort_values('Total', ascending=False)

# Stacked bar chart
fig1 = go.Figure()
for group in ['OTA', 'Google']:
    if group in chart1_pivot.columns:
        fig1.add_trace(go.Bar(
            x=chart1_pivot.index,
            y=chart1_pivot[group],
            name=group,
            text=[f"{(count / total * 100):.1f}%" if total > 0 else "0%" \
                  for count, total in zip(chart1_pivot[group], chart1_pivot['Total'])],
            textposition='inside'
        ))

fig1.update_layout(
    barmode='stack',
    title="Review Count by Hotel and Source",
    xaxis_title="Hotel",
    yaxis_title="Count of Reviews",
    legend_title="Review Source",
    template="plotly_white"
)

st.plotly_chart(fig1, use_container_width=True)

# Prepare data for Chart 2 (Line Chart)
df['Review Date'] = pd.to_datetime(df['Review Date'], format='%d/%m/%Y')
df['Month'] = df['Review Date'].dt.to_period('M')
avg_rating_data = df.groupby(['Month', 'Review Group']).agg({'Rating': 'mean'}).reset_index()
all_avg = df.groupby('Month').agg({'Rating': 'mean'}).reset_index()
all_avg['Review Group'] = 'All'
avg_rating_data = pd.concat([avg_rating_data, all_avg])

# Filter for Chart 2
selected_groups = st.multiselect(
    "Select Review Groups for Line Chart:", options=['All', 'Google', 'OTA'], default=['All', 'Google', 'OTA']
)
filtered_data = avg_rating_data[avg_rating_data['Review Group'].isin(selected_groups)]

# Line chart
fig2 = px.line(
    filtered_data,
    x='Month',
    y='Rating',
    color='Review Group',
    title="Average Rating by Month",
    labels={'Rating': 'Average Rating', 'Month': 'Month'},
    template="plotly_white"
)
fig2.update_xaxes(type='category')

st.plotly_chart(fig2, use_container_width=True)
