import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime, timedelta

# Page Configuration
st.set_page_config(
    page_title="Job Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with sidebar styling
st.markdown("""
    <style>
    [data-testid="stHeader"] {
        background-color: #000000;
    }
    
    .main {
        background-color: #000000;
    }
    
    .block-container {
        padding: 1rem 5rem 10rem !important;
    }
    
    div[data-testid="stMetricValue"] {
        font-size: 40px;
        background-color: #000000;
        padding: 1rem;
        border-radius: 8px;
        color: white !important;
    }
    
    div[data-testid="stMetricLabel"] {
        font-size: 14px;
        color: white;
    }
    
    div[data-testid="stMetricDelta"] {
        color: black;
    }
    
    div[data-testid="stHorizontalBlock"] {
        background-color: #f5e6e0;
        padding: 1rem;
        border-radius: 8px;
    }
    
    div.stSelectbox > div > div {
        background-color: black;
        border-radius: 4px;
    }
    
    div.stSlider > div > div {
        background-color: black;
        border-radius: 4px;
        padding: 1rem;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #8B4513;
    }
    
    .plot-container {
        background-color: black;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #8B4513;
        padding-top: 2rem;
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        color: white;
    }
    
    .sidebar-content {
        padding: 1rem;
        color: white;
    }
    
    .sidebar-nav {
        margin-top: 2rem;
    }
    
    .nav-link {
        color: white;
        text-decoration: none;
        padding: 0.5rem 1rem;
        border-radius: 4px;
        display: block;
        margin-bottom: 0.5rem;
    }
    
    .nav-link:hover {
        background-color: rgba(255, 255, 255, 0.1);
    }
    
    .profile-section {
        margin-top: 2rem;
        padding: 1rem;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    # User Profile Section
    st.markdown("""
        <div class="sidebar-content">
            <div style="text-align: center;">
                <h3 style="color: white;">👤 User Profile</h3>
                <p>Welcome, Admin</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Navigation Links
    st.markdown("""
        <div class="sidebar-nav">
            <h4 style="color: white; padding-left: 1rem;">Navigation</h4>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("🏠 Dashboard", use_container_width=True):
        st.switch_page("app.py")
    
    if st.button("📊 Analytics", use_container_width=True):
        st.switch_page("pages/1_📊_Analytics.py")
    
    if st.button("📈 Reports", use_container_width=True):
        st.switch_page("pages/2_📈_Reports.py")
    
    if st.button("⚙️ Settings", use_container_width=True):
        st.switch_page("pages/3_⚙️_Settings.py")
    
    # Additional Sidebar Content
    st.markdown("""
        <div class="profile-section">
            <p style="color: white; font-size: 0.8rem;">
                Last Login: Today at 9:00 AM<br>
                Status: Online
            </p>
        </div>
    """, unsafe_allow_html=True)

# Load and prepare data
try:
    # Try to load the actual CSV file
    file_path = "new/Job.csv"
    df = pd.read_csv(file_path)
    df['dateposted'] = pd.to_datetime(df['dateposted'], format='%m/%d/%y')
except:
    st.error("Could not load Job.csv file. Please make sure it exists in the correct location.")
    df = pd.DataFrame()  # Create empty DataFrame if file not found

# Dashboard Header with back button and date
st.markdown("""
    <div style='display: flex; justify-content: space-between; align-items: center; padding: 1rem; background-color: #8B4513; color: white; border-radius: 8px;'>
        <div style='display: flex; align-items: center;'>
            <span style='font-size: 24px; margin-right: 10px;'>←</span>
            <h2 style='margin: 0; color: white;'>Job Posting Effectiveness Dashboard</h2>
        </div>
        <div style='color: white;'>
            Data Last Updated on | February 6th, 2025
        </div>
    </div>
    <div style='background-color: #8B4513; color: white; padding: 0.5rem 1rem; border-radius: 0 0 8px 8px; margin-bottom: 2rem;'>
        Unlocking Trends in Job Postings, Views, and Applications
    </div>
""", unsafe_allow_html=True)

# Create four columns for filters and metrics with specific ratios
col1, col2, col3, col4 = st.columns([2, 2, 2, 3])

with col1:
    st.markdown("<div style='background-color: #8B4513; padding: 0.5rem; border-radius: 8px; color: white;'><h4 style='margin:0; color: white;'>Select the State</h4></div>", unsafe_allow_html=True)
    state_selected = st.selectbox("", ["All"] + list(df['state'].dropna().unique()), label_visibility="collapsed")

with col2:
    st.markdown("<div style='background-color: #8B4513; padding: 0.5rem; border-radius: 8px; color: white;'><h4 style='margin:0; color: white;'>Average Applications</h4></div>", unsafe_allow_html=True)
    st.metric("", value=round(df['applicationsCount'].mean()))

with col3:
    st.markdown("<div style='background-color: #8B4513; padding: 0.5rem; border-radius: 8px; color: white;'><h4 style='margin:0; color: white;'>Average Views</h4></div>", unsafe_allow_html=True)
    st.metric("", value=round(df['viewscount'].mean()))

with col4:
    st.markdown("<div style='background-color: #8B4513; padding: 0.5rem; border-radius: 8px; color: white;'><h4 style='margin:0; color: white;'>Select Salary Rating</h4></div>", unsafe_allow_html=True)
    salary_rating = st.slider("", 0.0, 5.0, (0.0, 5.0), label_visibility="collapsed")

# Filter Data
if state_selected != "All":
    df = df[df['state'] == state_selected]

# Create main content columns
left_col, right_col = st.columns([0.65, 0.35])

with left_col:
    with st.container():
        # Contract Type Performance Chart
        contract_chart = px.bar(
            df.groupby("contractType")[["viewscount", "applicationsCount"]].mean().reset_index(),
            x="contractType",
            y=["viewscount", "applicationsCount"],
            title="Job Postings Performance Comparison by Contract Type",
            color_discrete_sequence=["#E98C55", "#8B4513"],
            barmode='group',
            height=300
        )
        contract_chart.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            title_font_color='#8B4513',
            title_x=0.5,
            margin=dict(l=40, r=40, t=60, b=40),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        st.plotly_chart(contract_chart, use_container_width=True)

        # Sector Performance Chart
        # Define sector mapping for better grouping
        sector_mapping = {
            'Software Development': ['Software Development', 'Software', 'Internet Publishing'],
            'Technology & IT': ['Technology', 'Information Technology', 'IT Services', 'IT System', 'Information Services'],
            'Financial Services': ['Financial Services', 'Banking', 'Capital Markets', 'Insurance'],
            'Healthcare': ['Health Care', 'Mental Health', 'Hospitals', 'Medical'],
            'Entertainment & Media': ['Entertainment Providers', 'Media Production', 'Online Audio and Video'],
            'Manufacturing': ['Manufacturing', 'Electronics Manufacturing', 'Semiconductor'],
            'Consulting': ['Consulting', 'Business Consulting'],
            'Retail & Consumer': ['Retail', 'Consumer Services', 'Food and Beverage']
        }

        def map_sector(sector):
            # Convert to lowercase for better matching
            sector_lower = sector.lower()
            for main_category, keywords in sector_mapping.items():
                if any(keyword.lower() in sector_lower for keyword in keywords):
                    return main_category
            return 'Other'

        # Apply the mapping to create sector groups
        df['sector_group'] = df['sector'].apply(map_sector)
        
        # Calculate sector performance
        sector_data = df.groupby("sector_group")[["viewscount", "applicationsCount"]].agg({
            "viewscount": "mean",
            "applicationsCount": "mean"
        }).reset_index()
        
        # Add total performance and get top sectors
        sector_data["total_performance"] = sector_data["viewscount"] + sector_data["applicationsCount"]
        sector_data = sector_data.nlargest(8, "total_performance")
        
        # Create the sector chart
        sector_chart = px.bar(
            sector_data,
            x=["viewscount", "applicationsCount"],
            y="sector_group",
            title="Top Industry Sectors by Performance",
            color_discrete_sequence=["#E98C55", "#8B4513"],
            orientation='h',
            height=400,
            labels={
                "sector_group": "Industry Sector",
                "viewscount": "Average Views",
                "applicationsCount": "Average Applications",
                "variable": "Metric Type"
            }
        )
        sector_chart.update_layout(
            plot_bgcolor='black',
            paper_bgcolor='black',
            title_font_color='#8B4513',
            title_x=0.5,
            margin=dict(l=40, r=40, t=60, b=40),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                font=dict(color='white')
            ),
            yaxis=dict(
                tickfont=dict(color='white'),
                title_font=dict(color='white')
            ),
            xaxis=dict(
                tickfont=dict(color='white'),
                title_font=dict(color='white')
            )
        )
        st.plotly_chart(sector_chart, use_container_width=True)

with right_col:
    # Scatter Plot
    scatter_chart = px.scatter(
        df,
        x="viewscount",
        y="applicationsCount",
        title="Views Count Vs Applications Count",
        color_discrete_sequence=["#E98C55"],
        height=300
    )
    scatter_chart.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        title_font_color='#8B4513',
        title_x=0.5,
        margin=dict(l=40, r=40, t=60, b=40)
    )
    st.plotly_chart(scatter_chart, use_container_width=True)

    # Pie Chart
    experience_data = {'Experience Level': ['Junior', 'Mid-level', 'Senior'],
                      'Percentage': [40, 33.33, 26.67]}
    exp_df = pd.DataFrame(experience_data)
    pie_chart = px.pie(
        exp_df,
        values='Percentage',
        names='Experience Level',
        title="Distribution of Applications by Experience Level",
        color_discrete_sequence=["#E98C55", "#C06030", "#8B4513"],
        height=300
    )
    pie_chart.update_layout(
        title_font_color='#8B4513',
        title_x=0.5,
        margin=dict(l=40, r=40, t=60, b=40),
        paper_bgcolor='white'
    )
    st.plotly_chart(pie_chart, use_container_width=True)

# Timeline Chart
line_chart = px.line(
    df.groupby(df['dateposted'].dt.strftime('%b %y'))[['viewscount', 'applicationsCount']].mean().reset_index(),
    x="dateposted",
    y=["viewscount", "applicationsCount"],
    title="Views and Applications Over Time",
    markers=True,
    color_discrete_sequence=["#E98C55", "#8B4513"],
    height=300
)
line_chart.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    title_font_color='#8B4513',
    title_x=0.5,
    margin=dict(l=40, r=40, t=60, b=40),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    )
)
st.plotly_chart(line_chart, use_container_width=True)
