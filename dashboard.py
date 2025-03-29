import streamlit as st
import pandas as pd 
import plotly.express as px 
import plotly.graph_objects as go
import numpy as np 
from datetime import datetime, timedelta

# Page Config
st.set_page_config(
    page_title="Job Market Analytics Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed"  # Hide sidebar by default
)

# Custom CSS with modern styling matching the reference
st.markdown("""
    <style>
    .main {
        padding: 1rem;
        background-color: #f8f9fa;
    }
    .metric-card {
        background-color: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1a73e8;
    }
    .metric-label {
        font-size: 1rem;
        color: #5f6368;
    }
    .chart-container {
        background-color: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    h1 {
        color: #202124;
        font-size: 1.8rem;
        margin-bottom: 2rem;
    }
    h3 {
        color: #202124;
        font-size: 1.2rem;
        margin-bottom: 1rem;
    }
    .stDateInput {
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# Title section with date range
st.title("Job Market Analytics")

# Date filter row
col1, col2, col3, col4 = st.columns([2, 1, 1, 2])
with col2:
    start_date = st.date_input("Start Date", datetime.now() - timedelta(days=365))
with col3:
    end_date = st.date_input("End Date", datetime.now())

@st.cache_data
def load_data():
    try:
        jobs = pd.read_csv('src/Job.csv')
        companies = pd.read_csv('src/Company.csv')
        job_postings = pd.read_csv('src/JobPosting.csv')
        
        # Convert postedTime to datetime
        def extract_days(time_str):
            try:
                if pd.isna(time_str):
                    return None
                time_str = str(time_str).lower()
                if 'month' in time_str:
                    return float(time_str.split()[0]) * 30
                elif 'week' in time_str:
                    return float(time_str.split()[0]) * 7
                elif 'day' in time_str:
                    return float(time_str.split()[0])
                elif 'hour' in time_str:
                    return float(time_str.split()[0]) / 24
                return None
            except Exception as e:
                return None

        job_postings['days_ago'] = job_postings['postedTime'].apply(extract_days)
        job_postings['postedDate'] = pd.Timestamp.now() - pd.to_timedelta(job_postings['days_ago'], unit='D')
        
        # Clean applications count
        job_postings['clean_applications'] = job_postings['applicationsCount'].apply(
            lambda x: float(str(x).split()[0]) if pd.notnull(x) and str(x).split()[0].isdigit() else None
        )
        
        return jobs, companies, job_postings
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None, None, None

jobs, companies, job_postings = load_data()

if jobs is not None and companies is not None and job_postings is not None:
    try:
        # KPI Metrics Row
        st.markdown("### Main KPI's")
        metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
        
        with metric_col1:
            active_jobs = len(jobs)
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{active_jobs:,}</div>
                    <div class="metric-label">Active Jobs</div>
                </div>
                """, unsafe_allow_html=True)
            
        with metric_col2:
            total_companies = len(companies)
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{total_companies:,}</div>
                    <div class="metric-label">Companies</div>
                </div>
                """, unsafe_allow_html=True)
            
        with metric_col3:
            total_applications = job_postings['clean_applications'].sum()
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{int(total_applications):,}</div>
                    <div class="metric-label">Total Applications</div>
                </div>
                """, unsafe_allow_html=True)
            
        with metric_col4:
            avg_applications = job_postings['clean_applications'].mean()
            turnover_rate = f"{(avg_applications/total_applications*100):.1f}%"
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{turnover_rate}</div>
                    <div class="metric-label">Application Rate</div>
                </div>
                """, unsafe_allow_html=True)

        # Charts Row 1
        st.markdown("### Trends Over Time")
        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            # Job Posting Trend
            if 'postedDate' in job_postings.columns:
                valid_dates = job_postings.dropna(subset=['postedDate'])
                if not valid_dates.empty:
                    daily_posts = valid_dates.groupby(valid_dates['postedDate'].dt.date).agg({
                        'Job id': 'count',
                        'clean_applications': 'sum'
                    }).reset_index()
                    
                    fig1 = go.Figure()
                    
                    # Add bars for job postings
                    fig1.add_trace(go.Bar(
                        x=daily_posts['postedDate'],
                        y=daily_posts['Job id'],
                        name='New Jobs',
                        marker_color='#FF69B4'
                    ))
                    
                    # Add line for applications
                    fig1.add_trace(go.Bar(
                        x=daily_posts['postedDate'],
                        y=daily_posts['clean_applications'],
                        name='Applications',
                        marker_color='#FFA500',
                        opacity=0.7
                    ))
                    
                    fig1.update_layout(
                        title="Job Postings & Applications Over Time",
                        height=400,
                        barmode='group',
                        template="plotly_white",
                        legend=dict(
                            orientation="h",
                            yanchor="bottom",
                            y=1.02,
                            xanchor="right",
                            x=1
                        )
                    )
                    st.plotly_chart(fig1, use_container_width=True)

        with chart_col2:
            # Application Rate Trend
            if 'sector' in companies.columns:
                sector_data = companies.groupby('sector').agg({
                    'companyId': 'count'
                }).reset_index().sort_values('companyId', ascending=True).tail(10)
                
                fig2 = go.Figure(go.Bar(
                    x=sector_data['companyId'],
                    y=sector_data['sector'],
                    orientation='h',
                    marker_color='#4CAF50'
                ))
                
                fig2.update_layout(
                    title="Companies by Sector",
                    height=400,
                    template="plotly_white",
                    yaxis={'categoryorder':'total ascending'}
                )
                st.plotly_chart(fig2, use_container_width=True)

        # Charts Row 2
        chart_col3, chart_col4 = st.columns(2)
        
        with chart_col3:
            # Location Distribution
            if 'location' in companies.columns:
                location_data = companies['location'].str.split(',').str[1].str.strip().value_counts().head(10)
                
                fig3 = go.Figure(go.Bar(
                    x=location_data.index,
                    y=location_data.values,
                    marker_color='#2196F3'
                ))
                
                fig3.update_layout(
                    title="Jobs by Location",
                    height=400,
                    template="plotly_white",
                    xaxis_tickangle=-45
                )
                st.plotly_chart(fig3, use_container_width=True)

        with chart_col4:
            # Applications Distribution
            valid_applications = job_postings['clean_applications'].dropna()
            if not valid_applications.empty:
                bins = [0, 10, 50, 100, 200, float('inf')]
                labels = ['0-10', '11-50', '51-100', '101-200', '200+']
                applications_dist = pd.cut(valid_applications, bins=bins, labels=labels).value_counts()
                
                fig4 = go.Figure(go.Bar(
                    x=applications_dist.index,
                    y=applications_dist.values,
                    marker_color='#9C27B0'
                ))
                
                fig4.update_layout(
                    title="Applications Distribution",
                    height=400,
                    template="plotly_white"
                )
                st.plotly_chart(fig4, use_container_width=True)

    except Exception as e:
        st.error(f"Error in dashboard rendering: {str(e)}")
        import traceback
        st.error(f"Traceback: {traceback.format_exc()}")
else:
    st.error("Unable to load data. Please check if the CSV files are present in the src directory.")
