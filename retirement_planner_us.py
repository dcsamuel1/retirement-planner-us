
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Retirement Planner US", layout="wide")
st.title("🇺🇸 Retirement Planner - US Economy")

# Inputs
current_age = st.number_input("Current Age", min_value=18, max_value=70, value=30)
retirement_age = st.number_input("Retirement Age", min_value=current_age + 1, max_value=80, value=65)
annual_salary = st.number_input("Current Annual Salary ($)", min_value=10000, step=1000, value=60000)
employee_contrib_pct = st.slider("Your Contribution (%)", 0.0, 100.0, 10.0)
employer_contrib_pct = st.slider("Employer Contribution (%)", 0.0, 100.0, 5.0)
expected_roi = st.slider("Expected Annual ROI (%)", 0.0, 15.0, 6.0)
annual_salary_growth = st.slider("Annual Salary Growth (%)", 0.0, 10.0, 3.0)
annual_inflation = st.slider("Annual Inflation Rate (%)", 0.0, 10.0, 2.5)

# Calculation
years = list(range(current_age, retirement_age))
df = pd.DataFrame(years, columns=["Age"])
df["Salary ($)"] = [annual_salary * ((1 + annual_salary_growth / 100) ** i) for i in range(len(years))]
df["Employee Contribution ($)"] = df["Salary ($)"] * (employee_contrib_pct / 100)
df["Employer Contribution ($)"] = df["Salary ($)"] * (employer_contrib_pct / 100)
df["Total Contribution ($)"] = df["Employee Contribution ($)"] + df["Employer Contribution ($)"]
df["ROI ($)"] = df["Total Contribution ($)"].cumsum() * (expected_roi / 100)
df["Total Savings ($)"] = df["Total Contribution ($)"].cumsum() + df["ROI ($)"]

# Inflation-adjusted
df["Total Savings (Adj)"] = df["Total Savings ($)"] / ((1 + annual_inflation / 100) ** df.index)

# Display
st.subheader("Projection Table")
st.dataframe(df.style.format("${:,.2f}"))

st.subheader("Savings Over Time")
fig, ax = plt.subplots()
sns.lineplot(data=df, x="Age", y="Total Savings ($)", label="Nominal", ax=ax)
sns.lineplot(data=df, x="Age", y="Total Savings (Adj)", label="Inflation Adjusted", ax=ax)
ax.set_ylabel("Total Savings ($)")
ax.set_title("Projected Retirement Savings")
st.pyplot(fig)
