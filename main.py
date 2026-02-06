import streamlit as st
import pandas as pd
import numpy as np

# Page Configuration
st.set_page_config(
    page_title="Datathon Project",
    page_icon="🚀",
    layout="wide"
)

# Title and Introduction
st.title("🚀 Datathon Case Study: Project Constipation")
st.markdown("""
Welcome to your new hackathon project! 
This is a starter template built with **Streamlit**.
""")

# Sidebar for controls
with st.sidebar:
    st.header("Settings")
    st.write("Configure your AI agent or data parameters here.")

# Application Logic
st.subheader("Data Overview")

# Example Data
data = pd.DataFrame(
    np.random.randn(10, 5),
    columns=['Metric A', 'Metric B', 'Metric C', 'Metric D', 'Metric E']
)

st.dataframe(data)

st.line_chart(data)

st.info("To start building, edit `main.py`! This interface will update automatically.")
