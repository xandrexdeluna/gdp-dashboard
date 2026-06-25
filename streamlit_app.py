import streamlit as st
import pandas as pd
import numpy as np

# -------------------------------
# PAGE CONFIGURATION
# -------------------------------
st.set_page_config(page_title="Philippines Internet User Growth Forecast", layout="wide")

st.title("Philippines Internet User Growth Forecasting Simulation")
st.markdown("---")

# -------------------------------
# SIDEBAR: SIMULATION PARAMETERS
# -------------------------------
st.sidebar.header("Simulation Parameters")

alpha = st.sidebar.slider(
    "Alpha (a) - Level Smoothing",
    min_value=0.0,
    max_value=1.0,
    value=0.20,
    step=0.01,
    help="Controls how much weight is given to the most recent observation."
)

beta = st.sidebar.slider(
    "Beta (b) - Trend Smoothing",
    min_value=0.0,
    max_value=1.0,
    value=0.20,
    step=0.01,
    help="Controls how quickly the trend estimate responds to changes in the data."
)

# -------------------------------
# DATA: PHILIPPINES INTERNET USERS
# 2014-2025 Historical Data
# -------------------------------
years = [2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]
users = [
    34.70,  # 2014 - World Bank / ITU
    36.90,  # 2015 - World Bank / ITU
    39.20,  # 2016 - World Bank / ITU
    41.60,  # 2017 - World Bank / ITU
    44.10,  # 2018 - World Bank / ITU
    43.03,  # 2019 - World Bank / ITU
    53.76,  # 2020 - World Bank / ITU
    66.91,  # 2021 - World Bank / ITU
    75.21,  # 2022 - World Bank / ITU
    77.87,  # 2023 - World Bank / ITU
    67.26,  # 2024 - World Bank / ITU
    97.50   # 2025 - DataReportal
]

df = pd.DataFrame({"Year": years, "Internet Users (Millions)": users})

# -------------------------------
# HOLT'S LINEAR TREND METHOD
# -------------------------------
def holts_linear_trend(data, alpha, beta, forecast_years):
    n = len(data)
    level = [data[0]]
    trend = [(data[1] - data[0])]
    
    for t in range(1, n):
        new_level = alpha * data[t] + (1 - alpha) * (level[t-1] + trend[t-1])
        new_trend = beta * (new_level - level[t-1]) + (1 - beta) * trend[t-1]
        level.append(new_level)
        trend.append(new_trend)
    
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
with st.expander("Mathematical Framework (Holt's Linear Trend Method)", expanded=True):
    st.markdown("**Level Equation**")
    st.markdown("L_t = a * A_t + (1 - a) * (L_(t-1) + T_(t-1))")
    st.markdown("")
    st.markdown("**Trend Equation**")
    st.markdown("T_t = b * (L_t - L_(t-1)) + (1 - b) * T_(t-1)")
    st.markdown("")
    st.markdown("**Forecast Equation**")
    st.markdown("F_(t+m) = L_t + m * T_t")
    st.markdown("")
    st.markdown("**Where:**")
    st.markdown("- L_t = Estimated internet user level in the Philippines at time t")
    st.markdown("- T_t = Estimated trend in the Philippines at time t")
    st.markdown("- A_t = Actual internet users in the Philippines at time t")
    st.markdown("- a = Level smoothing constant (current value: **" + str(alpha) + "**)")
    st.markdown("- b = Trend smoothing constant (current value: **" + str(beta) + "**)")
    st.markdown("- m = Number of years ahead being forecasted")

# -------------------------------
# METRICS DISPLAY - 2026, 2027, 2028
# -------------------------------
st.markdown("---")
st.subheader("Philippines Internet Growth Dashboard Metrics")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Philippines " + str(forecast_years_list[0]) + " (Forecast)",
        value=f"{forecast[0]:,.2f} Million",
        delta=f"{forecast[0] - historical_data[-1]:.2f} Million"
    )

with col2:
    st.metric(
        label="Philippines " + str(forecast_years_list[1]) + " (Forecast)",
        value=f"{forecast[1]:,.2f} Million",
        delta=f"{forecast[1] - forecast[0]:.2f} Million"
    )

with col3:
    st.metric(
        label="Philippines " + str(forecast_years_list[2]) + " (Forecast)",
        value=f"{forecast[2]:,.2f} Million",
        delta=f"{forecast[2] - forecast[1]:.2f} Million"
    )

# -------------------------------
# HISTORICAL DATA TABLE
# -------------------------------
st.markdown("---")
st.subheader("Philippines Historical Internet User Data (2014-2025)")

df_display = df.copy()
df_display["Internet Users (Millions)"] = df_display["Internet Users (Millions)"].apply(lambda x: f"{x:.2f}")

st.dataframe(df_display, use_container_width=True)

# -------------------------------
# FORECAST TABLE - 2026, 2027, 2028
# -------------------------------
st.subheader("Philippines Forecast Summary (2026-2028)")

forecast_data = {
    "Year": forecast_years_list,
    "Forecasted Internet Users in the Philippines (Millions)": [f"{f:.2f}" for f in forecast]
}

forecast_df = pd.DataFrame(forecast_data)
st.dataframe(forecast_df, use_container_width=True)

# -------------------------------
# GROWTH ANALYSIS
# -------------------------------
st.subheader("Philippines Growth Analysis")

historical_growth = []
for i in range(1, len(users)):
    growth = ((users[i] - users[i-1]) / users[i-1]) * 100
    historical_growth.append(growth)

avg_growth = sum(historical_growth) / len(historical_growth)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Philippines Average Historical Growth",
        value=f"{avg_growth:.1f}%",
        delta="per year (2014-2025)"
    )

with col2:
    st.metric(
        label="Philippines Starting Value (2014)",
        value=f"{users[0]:.1f} Million",
        delta=""
    )

with col3:
    st.metric(
        label="Philippines Current Value (2025)",
        value=f"{users[-1]:.1f} Million",
        delta=f"{users[-1] - users[0]:.1f} Million"
    )

# -------------------------------
# SCENARIO COMPARISON
# -------------------------------
st.subheader("Philippines Scenario Comparison (2026-2028)")

scenarios = [
    {"name": "Conservative", "alpha": 0.20, "beta": 0.20},
    {"name": "Moderate", "alpha": 0.50, "beta": 0.50},
    {"name": "Aggressive", "alpha": 0.80, "beta": 0.80},
]

scenario_data = []
for s in scenarios:
    _, _, fcast = holts_linear_trend(historical_data, s["alpha"], s["beta"], forecast_years)
    row = {
        "Scenario": s["name"],
        "Alpha": s["alpha"],
        "Beta": s["beta"],
        "Philippines " + str(forecast_years_list[0]): f"{fcast[0]:.2f}",
        "Philippines " + str(forecast_years_list[1]): f"{fcast[1]:.2f}",
        "Philippines " + str(forecast_years_list[2]): f"{fcast[2]:.2f}",
    }
    scenario_data.append(row)

scenario_df = pd.DataFrame(scenario_data)
st.dataframe(scenario_df, use_container_width=True)

# -------------------------------
# COMPLETE DATA SUMMARY
# -------------------------------
st.subheader("Philippines Complete Data Summary (2014-2028)")

complete_data = []
for i, year in enumerate(years):
    complete_data.append({
        "Year": year,
        "Type": "Historical",
        "Philippines Internet Users (Millions)": f"{users[i]:.2f}"
    })

for i, year in enumerate(forecast_years_list):
    complete_data.append({
        "Year": year,
        "Type": "Forecast",
        "Philippines Internet Users (Millions)": f"{forecast[i]:.2f}"
    })

complete_df = pd.DataFrame(complete_data)
st.dataframe(complete_df, use_container_width=True)

# -------------------------------
# DATA NOTE
# -------------------------------
st.markdown("---")
st.markdown("**Philippines Data Note:**")
st.markdown("""
- This study focuses on internet user growth in the **Philippines**
- A noticeable decline is observed in 2024 (67.26 million) compared to 2023 (77.87 million)
- The data shows a strong recovery in 2025 (97.50 million) based on DataReportal's Digital 2025 report
- This could be due to methodology changes, data reporting differences, or actual market recovery
- The forecast model accounts for these fluctuations in its trend calculation
- The Philippines had 97.5 million internet users at the start of 2025, with 83.8% internet penetration
""")

# -------------------------------
# COUNTRY CONTEXT
# -------------------------------
with st.expander("Philippines Digital Context (2025)", expanded=False):
    st.markdown("""
    **Philippines Digital Statistics (January 2025):**
    
    | Metric | Value |
    | :--- | :--- |
    | **Total Population** | ~116 million |
    | **Internet Users** | **97.5 million** |
    | **Internet Penetration** | 83.8% |
    | **Social Media Users** | 90.8 million |
    | **Cellular Mobile Connections** | 142 million |
    | **Mobile Connections per Person** | 122% |
    
    **Key Insights:**
    - The Philippines has one of the highest social media usage rates in the world
    - Mobile connections exceed the population, indicating multiple SIM usage
    - Internet adoption has grown significantly from 34.7 million in 2014 to 97.5 million in 2025
    """)

# -------------------------------
# FOOTER
# -------------------------------
st.markdown("---")
st.caption("Figure 1. Philippines Internet User Growth Forecasting Simulation System")
st.caption("Data sources: World Bank, ITU, DataReportal")
st.caption("Historical Data: 2014-2025 | Forecast Period: 2026-2028")
st.caption("Note: Values are in millions. 2025 data from DataReportal (97.50 million).")
