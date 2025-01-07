import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Set Streamlit to wide mode
st.set_page_config(layout="wide")

# Load the dataset
data_file = 'test_data.csv'
df = pd.read_csv(data_file)
