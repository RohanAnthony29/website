import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from db_service import DatabaseService

# Set page config
st.set_page_config(
    page_title="Job Posting Effectiveness Dashboard",
    page_icon="📊",
    layout="wide"
)

# Custom CSS for brown/orange theme
st.markdown("""
    <style>
    .main {
        background-color: #f5e6d3;
    }
    .stApp {
        background-color: #f5e6d3;
    }
    .css-1d391kg {
        background-color: #8b4513;
        color: white;
    }
    .stMetric {
        background-color: white;
        padding: 15px;
        border-radius: 5px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .metric-container {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    h1, h2, h3 {
        color: #8b4513;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize database service
db = DatabaseService()

# Title and Header
col1, col2 = st.columns([3, 1])
with col1:
    st.title("Job Posting Effectiveness Dashboard")
    st.subheader("Unlocking Trends in Job Postings, Views, and Applications")
with col2:
    st.write(f"Data Last Updated on | {datetime.now().strftime('%B %d, %Y')}")

# Create three columns layout
left_column, middle_column, right_column = st.columns([2, 2, 1])

# Left column - Job Postings Performance Comparison
with left_column:
    st.subheader("Job Postings Performance Comparison by Contract Type")
    contract_data = db.get_contract_type_performance()
    fig_contract = px.bar(
        contract_data,
        x='contract_type',
        y=['views_count', 'applications_count'],
        title='',
        labels={'value': 'Count', 'contract_type': 'Contract Type', 'variable': 'Metric'},
        color_discrete_sequence=['#e67e22', '#f1c40f'],
        barmode='group'
    )
    fig_contract.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        showlegend=True,
        legend_title_text=''
    )
    st.plotly_chart(fig_contract, use_container_width=True)

    # Line chart showing views and applications trends
    st.subheader("Views and Applications Trends")
    trend_data = db.get_views_applications_correlation()
    
    # Bin the data into groups of 20 jobs and calculate mean
    trend_data['bin'] = (trend_data.index // 20) * 20
    aggregated_data = trend_data.groupby('bin').agg({
        'views_count': 'mean',
        'applications_count': 'mean'
    }).reset_index()
    
    fig_trend = go.Figure()
    
    # Add traces with improved styling
    fig_trend.add_trace(
        go.Scatter(
            x=aggregated_data['bin'],
            y=aggregated_data['views_count'],
            name='Views',
            line=dict(color='#e67e22', width=3),
            mode='lines',
            hovertemplate='Bin: %{x}<br>Average Views: %{y:.0f}<extra></extra>'
        )
    )
    
    fig_trend.add_trace(
        go.Scatter(
            x=aggregated_data['bin'],
            y=aggregated_data['applications_count'],
            name='Applications',
            line=dict(color='#f1c40f', width=3),
            mode='lines',
            hovertemplate='Bin: %{x}<br>Average Applications: %{y:.0f}<extra></extra>'
        )
    )
    
    # Update layout with better styling
    fig_trend.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis=dict(
            title='Job Groups (20 jobs per group)',
            gridcolor='lightgray',
            showgrid=True,
            dtick=40
        ),
        yaxis=dict(
            title='Average Count',
            gridcolor='lightgray',
            showgrid=True,
            rangemode='nonnegative'
        ),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        margin=dict(l=60, r=30, t=50, b=50),
        hovermode='x unified'
    )
    st.plotly_chart(fig_trend, use_container_width=True)

# Middle column - Filters and Sector Performance
with middle_column:
    # Filters
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.selectbox("Select the State", ["All"] + db.get_unique_states())
        with col2:
            st.metric("Average Applications", "50")
            st.metric("Average Views", "300")
    
    # Sector Performance
    st.subheader("Job Postings Performance by Sector")
    sector_data = db.get_sector_performance()
    fig_sector = px.bar(
        sector_data,
        y='sector',
        x=['views_count', 'applications_count'],
        orientation='h',
        title='',
        labels={'value': 'Count', 'sector': 'Sector', 'variable': 'Metric'},
        color_discrete_sequence=['#e67e22', '#f1c40f'],
        barmode='group'
    )
    fig_sector.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        showlegend=True,
        legend_title_text=''
    )
    st.plotly_chart(fig_sector, use_container_width=True)

# Right column - Experience Distribution and Salary Rating
with right_column:
    # Salary Rating Slider
    st.subheader("Select Salary Rating")
    salary_range = st.slider("", 0.0, 5.0, (0.0, 5.0), step=0.1)
    
    # Experience Level Distribution
    st.subheader("Distribution of Applications by Experience Level")
    experience_data = db.get_experience_level_distribution()
    fig_exp = px.pie(
        experience_data,
        values='applications_count',
        names='experience_level',
        title='',
        color_discrete_sequence=['#e67e22', '#f1c40f', '#d35400']
    )
    fig_exp.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    st.plotly_chart(fig_exp, use_container_width=True) 