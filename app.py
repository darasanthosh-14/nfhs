import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(page_title="NFHS-5 Dashboard", layout="wide")

st.title("📊 All India National Family Health Survey (NFHS-5) Dashboard")

# -----------------------------
# Load Data
# -----------------------------
@st.cache_data
def load_data():
    file_path = "All India National Family Health Survey5.xlsx"
    df = pd.read_excel(file_path)
    return df

df = load_data()

# -----------------------------
# Clean Data
# -----------------------------
# Remove duplicate "Note of :" columns
df = df.loc[:, ~df.columns.str.contains("Note of")]

# Assume first column is State/UT name
state_column = df.columns[0]

# Remove rows with missing state names
df = df[df[state_column].notna()]

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("Filters")

selected_state = st.sidebar.selectbox(
    "Select State",
    sorted(df[state_column].unique())
)

# Extract indicator categories (text before " - ")
def get_category(col):
    if " - " in col:
        return col.split(" - ")[0]
    return "Other"

categories = list(set([get_category(col) for col in df.columns[1:]]))
categories.sort()

selected_category = st.sidebar.selectbox(
    "Select Indicator Category",
    categories
)

# Filter indicators based on category
filtered_indicators = [
    col for col in df.columns
    if col.startswith(selected_category)
]

selected_indicator = st.sidebar.selectbox(
    "Select Indicator",
    filtered_indicators
)

# -----------------------------
# Main Dashboard
# -----------------------------
state_data = df[df[state_column] == selected_state]
value = state_data[selected_indicator].values[0]

# KPI
st.metric(
    label=f"{selected_indicator}",
    value=round(value, 2)
)

# -----------------------------
# State Comparison Chart
# -----------------------------
st.subheader("📈 State Comparison")

chart_df = df[[state_column, selected_indicator]].dropna()

fig = px.bar(
    chart_df.sort_values(by=selected_indicator, ascending=False),
    x=state_column,
    y=selected_indicator,
)

fig.update_layout(
    xaxis_tickangle=-45,
    height=600
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Raw Data Table
# -----------------------------
st.subheader("📄 Data Table")
st.dataframe(chart_df)
