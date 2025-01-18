import streamlit as st
import pandas as pd
import plotly.express as px

# Set Streamlit wide mode
st.set_page_config(layout="wide")

# Define custom colors
colors = ['#F2DD83', '#9A8CB5','#CBD9EF', '#FCD5C6',  '#EB9861', '#72884B', '#567BA2']

# Load data
uploaded_file = "Edit_Review.csv"
df = pd.read_csv(uploaded_file, encoding='ISO-8859-1')

# Preprocess data
df['Revinate Collected Date'] = pd.to_datetime(df['Revinate Collected Date'], errors='coerce')
df['Review Date'] = pd.to_datetime(df['Review Date'], errors='coerce')
df['Month'] = df['Review Date'].dt.strftime('%B')

# Categorize Review Site
def categorize_site(site):
    return "Google" if site == "Google" else "OTA"

df['Review Group'] = df['Review Site'].apply(categorize_site)

# Order months
month_order = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
df['Month'] = pd.Categorical(df['Month'], categories=month_order, ordered=True)

# Header
st.title("Review Hotel Dashboard")

# Chart 1: Stacked bar chart for count of reviews by hotel and review site
grouped_data = df.groupby(['Hotel', 'Review Group']).size().reset_index(name='Count')
grouped_data_total = grouped_data.groupby('Hotel')['Count'].transform('sum')
grouped_data['Percentage'] = (grouped_data['Count'] / grouped_data_total) * 100

fig1 = px.bar(
    grouped_data,
    x='Hotel',
    y='Count',
    color='Review Group',
    text=grouped_data['Percentage'].round(1).astype(str) + '%',
    title='Count of Reviews by Hotel and Review Site',
    labels={'Count': 'Number of Reviews'},
    color_discrete_sequence=colors
)
fig1.update_layout(barmode='stack', xaxis={'categoryorder': 'total descending'})
st.plotly_chart(fig1)

# Chart 2: Line chart for average rating by month with filter
hotel_options = ['All'] + df['Hotel'].unique().tolist()
selected_hotel = st.selectbox("Filter by Hotel:", hotel_options, index=0)

if selected_hotel == "All":
    filtered_data = df
else:
    filtered_data = df[df['Hotel'] == selected_hotel]

monthly_avg = filtered_data.groupby(['Month', 'Review Group'])['Rating'].mean().reset_index()
monthly_avg_all = filtered_data.groupby('Month')['Rating'].mean().reset_index()
monthly_avg_all['Review Group'] = 'All'
monthly_avg = pd.concat([monthly_avg, monthly_avg_all])

fig2 = px.line(
    monthly_avg,
    x='Month',
    y='Rating',
    color='Review Group',
    title='Average Rating by Month',
    labels={'Rating': 'Average Rating', 'Month': 'Month'},
    color_discrete_sequence=colors
)
fig2.update_traces(mode='lines+markers')
fig2.update_xaxes(categoryorder='array', categoryarray=month_order)
st.plotly_chart(fig2)

# Chart 3: Scatter chart for count of reviews (OTA vs Google) by month with filter
hotel_options_scatter = ['All'] + df['Hotel'].unique().tolist()
selected_hotel_scatter = st.selectbox("Filter by Hotel for Scatter Chart:", hotel_options_scatter, index=0)

if selected_hotel_scatter == "All":
    scatter_data = df
else:
    scatter_data = df[df['Hotel'] == selected_hotel_scatter]

scatter_grouped = scatter_data.groupby(['Month', 'Review Group']).size().unstack(fill_value=0).reset_index()
scatter_grouped.columns.name = None

fig3 = px.scatter(
    scatter_grouped,
    x=scatter_grouped.get('OTA', 0),
    y=scatter_grouped.get('Google', 0),
    title='Scatter Chart: OTA vs Google Reviews by Month',
    labels={'x': 'Count of OTA Reviews', 'y': 'Count of Google Reviews'},
    color_discrete_sequence=colors
)
st.plotly_chart(fig3)
