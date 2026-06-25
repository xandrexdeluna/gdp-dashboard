import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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
@st.cache_data
def load_data():
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
    return pd.DataFrame({"Year": years, "Internet Users (Millions)": users})

df = load_data()

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
    st.markdown(r"""
    **Level Equation**
    $L_t = \alpha A_t + (1 - \alpha)(L_{t-1} + T_{t-1})$

    **Trend Equation**
    $T_t = \beta (L_t - L_{t-1}) + (1 - \beta)T_{t-1}$

    **Forecast Equation**
    $F_{t+m} = L_t + mT_t$

    **Where:**
    - $L_t$ = Estimated internet user level at time $t$
    - $T_t$ = Estimated trend at time $t$
    - $A_t$ = Actual internet users at time $t$
    - $\alpha$ = Level smoothing constant (current value: **{:.2f}**)
    - $\beta$ = Trend smoothing constant (current value: **{:.2f}**)
    - $m$ = Number of years ahead being forecasted
    """.format(alpha, beta))

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
# GRAPH: HISTORICAL TRENDS VS PROJECTIONS
# -------------------------------
st.markdown("---")
st.subheader("📊 Historical Trends vs 3-Year Projections")

fig, ax = plt.subplots(figsize=(12, 6))

# Historical data
years_historical = df["Year"].values
users_historical = df["Internet Users (Millions)"].values
ax.plot(years_historical, users_historical, 'o-', 
        label='Actual Historical Data', 
        color='blue', 
        linewidth=2, 
        markersize=8)

# Forecast data
years_forecast = forecast_years_list
users_forecast = forecast
ax.plot(years_forecast, users_forecast, 'o-', 
        label="Holt's Forecast", 
        color='red', 
        linewidth=2, 
        markersize=8,
        linestyle='--')

# Vertical line at forecast start
ax.axvline(x=last_year, color='gray', linestyle=':', alpha=0.7, label='Forecast Start')

# Labels and title
ax.set_xlabel('Year', fontsize=12)
ax.set_ylabel('Internet Users (Millions)', fontsize=12)
ax.set_title('Internet User Growth: Historical Trends vs 3-Year Projections', fontsize=14, fontweight='bold')
ax.legend(loc='upper left', fontsize=10)
ax.grid(True, alpha=0.3)

# Format y-axis with commas
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:,.0f}'))

st.pyplot(fig)

# -------------------------------
# DATA ANALYSIS BREAKDOWN TABLE
# -------------------------------
st.markdown("---")
st.subheader("📋 Data Analysis Breakdown")

# Create forecast table
forecast_data = {
    "Year": forecast_years_list,
    "Forecasted Internet Users (Millions)": [f"{f:.2f}" for f in forecast]
}

forecast_df = pd.DataFrame(forecast_data)
st.dataframe(forecast_df, use_container_width=True)

# Display full historical data
with st.expander("📜 View Full Historical Data"):
    st.dataframe(df, use_container_width=True)

# -------------------------------
# FOOTER
# -------------------------------
st.markdown("---")
st.caption("Figure 1. Internet User Growth Forecasting Simulation System")
st.caption("Data sources: DataReportal, World Bank, DICT")
