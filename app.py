import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Set Streamlit to wide mode
st.set_page_config(layout="wide")

# Load the dataset
data_file = "/path/to/your/Edit_Review.csv"
df = pd.read_csv(data_file, encoding="ISO-8859-1")  # Or other encoding if needed


# Header
st.title("Restaurant Dashboard")

# Overall Section
st.header("Overall")
