import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Set Streamlit to wide mode
st.set_page_config(layout="wide")

import os

data_file = "Edit_Review.csv"  # Replace with your file path
if os.path.exists(data_file):
    print("File exists!")
else:
    print("File not found. Check the path.")


# Header
st.title("Restaurant Dashboard")

# Overall Section
st.header("Overall")
