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

# Filter for Chart 2 and Chart 3
hotel_options = ['All'] + df['Hotel'].unique().tolist()
selected_hotel = st.selectbox("Filter by Hotel (Chart 2 and Chart 3):", hotel_options, index=0)

# Chart 2: Line chart for average rating by month
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

# Chart 3: Line chart for count of reviews by month
if selected_hotel == "All":
    filtered_chart3 = df
else:
    filtered_chart3 = df[df['Hotel'] == selected_hotel]

monthly_count = filtered_chart3.groupby(['Month', 'Review Group']).size().reset_index(name='Count')
monthly_count_all = filtered_chart3.groupby('Month').size().reset_index(name='Count')
monthly_count_all['Review Group'] = 'All'
monthly_count = pd.concat([monthly_count, monthly_count_all])

fig3 = px.line(
    monthly_count,
    x='Month',
    y='Count',
    color='Review Group',
    title='Count of Reviews by Month',
    labels={'Count': 'Number of Reviews', 'Month': 'Month'},
    color_discrete_sequence=colors
)
fig3.update_traces(mode='lines+markers')
fig3.update_xaxes(categoryorder='array', categoryarray=month_order)

# Display Chart 2 and Chart 3 in two columns
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig2)
with col2:
    st.plotly_chart(fig3)

# Filter for Chart 4 and Chart 5
hotel_options_chart45 = ['All'] + df['Hotel'].unique().tolist()
selected_hotel_chart45 = st.selectbox("Filter by Hotel (Chart 4 and Chart 5):", hotel_options_chart45, index=0, key="chart45_filter")

# Chart 4: Scatter chart for count of reviews (OTA vs Google) by month
if selected_hotel_chart45 == "All":
    scatter_data = df
else:
    scatter_data = df[df['Hotel'] == selected_hotel_chart45]

scatter_grouped = scatter_data.groupby(['Month', 'Review Group']).size().unstack(fill_value=0).reset_index()
scatter_grouped.columns.name = None

fig4 = px.scatter(
    scatter_grouped,
    x=scatter_grouped.get('OTA', 0),
    y=scatter_grouped.get('Google', 0),
    title='Scatter Chart: OTA vs Google Reviews by Month',
    labels={'x': 'Count of OTA Reviews', 'y': 'Count of Google Reviews'},
    color_discrete_sequence=colors
)
fig4.update_traces(marker=dict(size=10), hovertemplate='Count of OTA Reviews: %{x}<br>Count of Google Reviews: %{y}')

# Chart 5: Diverging Bar Chart for OTA and Google reviews by month
if selected_hotel_chart45 == "All":
    diverging_data = df.groupby(['Month', 'Review Group']).size().unstack(fill_value=0).reset_index()
else:
    diverging_data = df[df['Hotel'] == selected_hotel_chart45].groupby(['Month', 'Review Group']).size().unstack(fill_value=0).reset_index()
diverging_data.columns.name = None

diverging_data['Google'] = -diverging_data['Google']  # Make Google reviews negative for diverging effect

diverging_fig = px.bar(
    diverging_data,
    y='Month',
    x=['OTA', 'Google'],
    title='Diverging Bar Chart: OTA vs Google Reviews by Month',
    labels={'value': 'Quantity of Reviews', 'variable': 'Review Source', 'Month': 'Month'},
    orientation='h',
    color_discrete_sequence=['#9A8CB5', '#F2DD83']
)

# Display Chart 4 and Chart 5 in two columns
col3, col4 = st.columns(2)
with col3:
    st.plotly_chart(fig4)
with col4:
    st.plotly_chart(diverging_fig)
