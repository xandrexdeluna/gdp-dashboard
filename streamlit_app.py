import streamlit as st
import pandas as pd
import numpy as np

# -------------------------------
# PAGE CONFIGURATION
# -------------------------------
st.set_page_config(page_title="Internet User Growth Forecast", layout="wide")

st.title("🌐 Internet User Growth Forecasting Simulation")
st.markdown("---")

# -------------------------------
# SIDEBAR: SIMULATION PARAMETERS
# -------------------------------
st.sidebar.header("📊 Simulation Parameters")

# Alpha and Beta sliders
alpha = st.sidebar.slider(
    "Alpha (α) - Level Smoothing",
    min_value=0.0,
    max_value=1.0,
    value=0.20,
    step=0.01,
    help="Controls how much weight is given to the most recent observation."
)

beta = st.sidebar.slider(
    "Beta (β) - Trend Smoothing",
    min_value=0.0,
    max_value=1.0,
    value=0.20,
    step=0.01,
    help="Controls how quickly the trend estimate responds to changes in the data."
)

# -------------------------------
# DATA: INTERNET USERS (PHILIPPINES)
# -------------------------------
# Historical data (2014-2024)
years = list(range(2014, 2025))
users = [
    38.0,   # 2014
    42.0,   # 2015
    47.0,   # 2016
    52.0,   # 2017
    58.0,   # 2018
    65.0,   # 2019
    73.0,   # 2020
    80.0,   # 2021
    85.0,   # 2022
    89.0,   # 2023
    92.0    # 2024
]

df = pd.DataFrame({"Year": years, "Internet Users (Millions)": users})

# -------------------------------
# HOLT'S LINEAR TREND METHOD
# -------------------------------
def holts_linear_trend(data, alpha, beta, forecast_years):
    n = len(data)
    
    # Initialize level and trend
    level = [data[0]]
    trend = [(data[1] - data[0])]
    
    # Apply Holt's method
    for t in range(1, n):
        new_level = alpha * data[t] + (1 - alpha) * (level[t-1] + trend[t-1])
        new_trend = beta * (new_level - level[t-1]) + (1 - beta) * trend[t-1]
        level.append(new_level)
        trend.append(new_trend)
    
    # Generate forecast
    current_level = level[-1]
    current_trend = trend[-1]
    forecast = [current_level + (m + 1) * current_trend for m in range(forecast_years)]
    
    return level, trend, forecast

# -------------------------------
# APPLY HOLT'S METHOD
# -------------------------------
historical_data = df["Internet Users (Millions)"].values
forecast_years = 3
level, trend, forecast = holts_linear_trend(historical_data, alpha, beta, forecast_years)

last_year = df["Year"].iloc[-1]
forecast_years_list = [last_year + i + 1 for i in range(forecast_years)]

# -------------------------------
# MATHEMATICAL FRAMEWORK
# -------------------------------
with st.expander("📐 Mathematical Framework (Holt's Linear Trend Method)", expanded=True):
    st.markdown(f"""
    **Level Equation**  
    L_t = α × A_t + (1 - α) × (L_{t-1} + T_{t-1})

    **Trend Equation**  
    T_t = β × (L_t - L_{t-1}) + (1 - β) × T_{t-1}

    **Forecast Equation**  
    F_{t+m} = L_t + m × T_t

    **Where:**
    - L_t = Estimated internet user level at time t
    - T_t = Estimated trend at time t
    - A_t = Actual internet users at time t
    - α = Level smoothing constant (current value: **{alpha:.2f}**)
    - β = Trend smoothing constant (current value: **{beta:.2f}**)
    - m = Number of years ahead being forecasted
    """)

# -------------------------------
# METRICS DISPLAY
# -------------------------------
st.markdown("---")
st.subheader("📈 Internet Growth Dashboard Metrics")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label=f"📅 {forecast_years_list[0]}",
        value=f"{forecast[0]:,.2f} Million",
        delta=f"{forecast[0] - historical_data[-1]:.2f} Million"
    )

with col2:
    st.metric(
        label=f"📅 {forecast_years_list[1]}",
        value=f"{forecast[1]:,.2f} Million",
        delta=f"{forecast[1] - forecast[0]:.2f} Million"
    )

with col3:
    st.metric(
        label=f"📅 {forecast_years_list[2]}",
        value=f"{forecast[2]:,.2f} Million",
        delta=f"{forecast[2] - forecast[1]:.2f} Million"
    )

# -------------------------------
# HISTORICAL DATA TABLE
# -------------------------------
st.markdown("---")
st.subheader("📊 Historical Internet User Data")

# Display historical data as a table
st.dataframe(df, use_container_width=True)

# -------------------------------
# FORECAST TABLE
# -------------------------------
st.subheader("📋 Forecast Summary")

forecast_data = {
    "Year": forecast_years_list,
    "Forecasted Internet Users (Millions)": [f"{f:.2f}" for f in forecast]
}

forecast_df = pd.DataFrame(forecast_data)
st.dataframe(forecast_df, use_container_width=True)

# -------------------------------
# GROWTH ANALYSIS
# -------------------------------
st.subheader("📈 Growth Analysis")

# Calculate growth rates
historical_growth = []
for i in range(1, len(users)):
    growth = ((users[i] - users[i-1]) / users[i-1]) * 100
    historical_growth.append(growth)

avg_growth = sum(historical_growth) / len(historical_growth)

# Calculate forecast growth
forecast_growth = []
for i in range(1, len(forecast)):
    growth = ((forecast[i] - forecast[i-1]) / forecast[i-1]) * 100
    forecast_growth.append(growth)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="📈 Average Historical Growth",
        value=f"{avg_growth:.1f}%",
        delta="per year"
    )

with col2:
    st.metric(
        label="📊 Starting Value (2014)",
        value=f"{users[0]:.1f} Million",
        delta=""
    )

with col3:
    st.metric(
        label="📊 Current Value (2024)",
        value=f"{users[-1]:.1f} Million",
        delta=f"{users[-1] - users[0]:.1f} Million"
    )

# -------------------------------
# FOOTER
# -------------------------------
st.markdown("---")
st.caption("Figure 1. Internet User Growth Forecasting Simulation System")
st.caption("Data sources: DataReportal, World Bank, DICT")
