import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np
from db_service import DatabaseService

# Page configuration
st.set_page_config(
    page_title="Job Posting Dashboard",
    page_icon="📊",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        background-color: white;
    }
    .stMetric {
        background-color: black;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 10px 0;
    }
    .stMetric:hover {
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .metric-value {
        color: #000000;
        font-weight: bold;
    }
    .metric-label {
        color: #666;
    }
    .chart-container {
        background-color: black;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 10px 0;
    }
    h1 {
        color: #8B4513;
        font-size: 2.5em;
        margin-bottom: 0.5em;
    }
    h2 {
        color: #A0522D;
        font-size: 1.8em;
        margin-bottom: 0.5em;
    }
    h3 {
        color: #8B4513;
        font-size: 1.4em;
        margin-bottom: 0.5em;
    }
    </style>
    """, unsafe_allow_html=True)

# Title and Header
st.title("Job Posting Effectiveness Dashboard")
#st.markdown("### Unlocking Trends in Job Postings, Views, and Applications")
#st.markdown(f"*Last updated: {datetime.now().strftime('%B %d, %Y')}*")

# Load and preprocess data


# Load data
df = DatabaseService()

if df is not None:
    # Sidebar filters
    st.sidebar.header("Filters")

    
    # State filter
    all_states=['All'] + sorted(df['state'].unique())
    selected_state = st.sidebar.selectbox(
        "Select State",
        options=all_states,
        index=0
    )
    
    # Salary rating filter
    min_rating, max_rating = st.sidebar.slider(
        "Select Salary Rating",
        min_value=1,
        max_value=5,
        value=(1, 5)
    )
    
    # Filter data based on selections
    filtered_df = df[
        ((selected_state == 'All') | (df['state'] == selected_state)) &
        (df['salaryRating'].between(min_rating, max_rating))
    ]
    
    st.sidebar.header("Recuirement Optimization")
    # Main metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        avg_applications = filtered_df['applicationsCount'].mean()
        st.metric(
            "Average Applications",
            f"{avg_applications:.1f}",
            delta=f"{avg_applications - df['applicationsCount'].mean():.1f}"
        )
    
    with col2:
        avg_views = filtered_df['viewsCount'].mean()
        st.metric(
            "Average Views",
            f"{avg_views:.1f}",
            delta=f"{avg_views - df['viewsCount'].mean():.1f}"
        )
    
    with col3:
        application_rate = (filtered_df['applicationsCount'] / filtered_df['viewsCount']).mean() * 100
        st.metric(
            "Application Rate",
            f"{application_rate:.1f}%",
            delta=f"{application_rate - (df['applicationsCount'] / df['viewsCount']).mean() * 100:.1f}%"
        )
    
    # Charts
    st.markdown("### Performance Analysis")
    
    # Contract Type Performance
    col1, col2 = st.columns(2)
    
    with col1:
        contract_performance = filtered_df.groupby('contractType').agg({
            'viewsCount': 'mean',
            'applicationsCount': 'mean'
        }).reset_index()
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='Views',
            x=contract_performance['contractType'],
            y=contract_performance['viewsCount'],
            marker_color='#8B4513'
        ))
        fig.add_trace(go.Bar(
            name='Applications',
            x=contract_performance['contractType'],
            y=contract_performance['applicationsCount'],
            marker_color='#A0522D'
        ))
        fig.update_layout(
            title='Job Posting Performance by Contract Type',
            barmode='group',
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Sector Performance
    with col2:
        sector_performance = filtered_df.groupby('sector')['applicationsCount'].mean().sort_values(ascending=True)
        fig = px.bar(
            sector_performance,
            orientation='h',
            title='Job Postings Performance by Sector',
            color_discrete_sequence=['#8B4513']
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Experience Level Distribution
    col1, col2 = st.columns(2)
    
    with col1:
        experience_dist = filtered_df['experienceLevel'].value_counts()
        fig = px.pie(
            values=experience_dist.values,
            names=experience_dist.index,
            title='Distribution of Applications by Experience Level',
            color_discrete_sequence=['#8B4513', '#A0522D', '#CD853F']
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Views vs Applications Scatter Plot
    with col2:
        fig = px.scatter(
            filtered_df,
            x='viewsCount',
            y='applicationsCount',
            title='Views vs Applications Correlation',
            color='experienceLevel',
            color_discrete_sequence=['#8B4513', '#A0522D', '#CD853F']
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Monthly Trends
    st.markdown("### Monthly Trends")
    monthly_trends = filtered_df.groupby('month').agg({
        'viewsCount': 'mean',
        'applicationsCount': 'mean'
    }).reset_index()
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=monthly_trends['month'],
        y=monthly_trends['viewsCount'],
        name='Views',
        line=dict(color='#8B4513')
    ))
    fig.add_trace(go.Scatter(
        x=monthly_trends['month'],
        y=monthly_trends['applicationsCount'],
        name='Applications',
        line=dict(color='#A0522D')
    ))
    fig.update_layout(
        title='Monthly Views and Applications Trends',
        height=400
    )
    st.plotly_chart(fig, use_container_width=True) 