import streamlit as st
import pandas as pd
import plotly.express as px

# Load Data
file_path = "/mnt/data/Job.csv"
df = pd.read_csv(file_path)

# Convert dateposted to datetime
df['dateposted'] = pd.to_datetime(df['dateposted'], format='%m/%d/%y')

# Sidebar Filters
st.sidebar.header("Filters")
state_selected = st.sidebar.selectbox("Select the State", ["All"] + list(df['state'].dropna().unique()))
salary_rating = st.sidebar.slider("Select Salary Rating", 0.0, 5.0, (0.0, 5.0))

# Filter Data
if state_selected != "All":
    df = df[df['state'] == state_selected]

# KPIs
avg_applications = round(df['applicationsCount'].mean(), 2)
avg_views = round(df['viewscount'].mean(), 2)

# Dashboard Title
st.markdown("<h1 style='text-align: center; color: brown;'>Job Posting Effectiveness Dashboard</h1>", unsafe_allow_html=True)
st.markdown("**Unlocking Trends in Job Postings, Views, and Applications**")

# KPI Cards
col1, col2 = st.columns(2)
col1.metric("Average Applications", avg_applications)
col2.metric("Average Views", avg_views)

# Bar Chart: Job Postings Performance by Contract Type
contract_chart = px.bar(df.groupby("contractType")[["viewscount", "applicationsCount"]].sum().reset_index(),
                        x="contractType", y=["viewscount", "applicationsCount"],
                        title="Job Postings Performance Comparison by Contract Type",
                        color_discrete_sequence=["#E98C55", "#C06030"])
st.plotly_chart(contract_chart, use_container_width=True)

# Horizontal Bar Chart: Job Postings by Sector
sector_chart = px.bar(df.groupby("sector")[["viewscount", "applicationsCount"]].sum().reset_index(),
                      x=["viewscount", "applicationsCount"], y="sector",
                      title="Job Postings Performance by Sector",
                      color_discrete_sequence=["#E98C55", "#C06030"], orientation='h')
st.plotly_chart(sector_chart, use_container_width=True)

# Pie Chart: Applications Distribution by Experience Level
experience_data = {'Experience Level': ['Junior', 'Mid-level', 'Senior'], 'Percentage': [40, 33.33, 26.67]}
exp_df = pd.DataFrame(experience_data)
pie_chart = px.pie(exp_df, values='Percentage', names='Experience Level',
                   title="Distribution of Applications by Experience Level",
                   color_discrete_sequence=["#E98C55", "#C06030", "#7A3B19"])
st.plotly_chart(pie_chart)

# Scatter Plot: Views vs Applications
scatter_chart = px.scatter(df, x="viewscount", y="applicationsCount",
                           title="Views Count Vs Applications Count",
                           color_discrete_sequence=["#E98C55"])
st.plotly_chart(scatter_chart, use_container_width=True)

# Line Chart: Views & Applications Over Time
time_data = df.groupby(df['dateposted'].dt.strftime('%b %y'))[['viewscount', 'applicationsCount']].sum().reset_index()
line_chart = px.line(time_data, x="dateposted", y=["viewscount", "applicationsCount"],
                     title="Views and Applications Over Time",
                     markers=True, color_discrete_sequence=["#E98C55", "#C06030"])
st.plotly_chart(line_chart, use_container_width=True)
