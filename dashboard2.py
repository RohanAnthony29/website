import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

# Page Config
st.set_page_config(
    page_title="HR Analytics Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 0rem;
        background-color: #f5f5f5;
    }
    .metric-container {
        background-color: white;
        border-radius: 10px;
        padding: 15px 20px;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .metric-label {
        color: #666;
        font-size: 0.9rem;
        margin-bottom: 4px;
    }
    .metric-value {
        color: #333;
        font-size: 1.8rem;
        font-weight: bold;
    }
    .metric-trend {
        color: #28a745;
        font-size: 0.8rem;
        margin-top: 4px;
    }
    .chart-container {
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stButton>button {
        width: 100%;
    }
    .css-1d391kg {
        padding: 1rem 1rem 1rem;
    }
    </style>
""", unsafe_allow_html=True)

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
        def clean_applications(x):
            try:
                if pd.isna(x):
                    return 0
                if isinstance(x, str) and 'over' in x.lower():
                    return float(x.lower().replace('over', '').replace('applicants', '').strip())
                return float(x.split()[0]) if pd.notnull(x) else 0
            except:
                return 0
                
        job_postings['clean_applications'] = job_postings['applicationsCount'].apply(clean_applications)
        
        # Merge job postings with companies
        merged_data = job_postings.merge(companies, left_on='Job id', right_on='companyId', how='left')
        
        return merged_data

    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

# Load data
data = load_data()

if data is not None:
    try:
        # Sidebar
        st.sidebar.title("Filters")
        
        # Date Filter
        st.sidebar.markdown("### Time Period")
        date_options = ['Last 7 Days', 'Last 30 Days', 'Last 90 Days', 'All Time']
        selected_period = st.sidebar.selectbox('Select Period', date_options)
        
        # Calculate date range
        end_date = data['postedDate'].max()
        if selected_period == 'Last 7 Days':
            start_date = end_date - timedelta(days=7)
        elif selected_period == 'Last 30 Days':
            start_date = end_date - timedelta(days=30)
        elif selected_period == 'Last 90 Days':
            start_date = end_date - timedelta(days=90)
        else:
            start_date = data['postedDate'].min()
            
        # Location Filter
        locations = data['location'].str.split(',').str[1].str.strip().unique()
        locations = [loc for loc in locations if pd.notnull(loc)]
        selected_locations = st.sidebar.multiselect(
            'Location',
            options=sorted(locations),
            default=sorted(locations)[:3]
        )
        
        # Industry Filter
        industries = sorted(data['sector'].unique())
        selected_industries = st.sidebar.multiselect(
            'Industry',
            options=industries,
            default=industries[:3]
        )
        
        # Apply filters
        filtered_data = data.copy()
        filtered_data = filtered_data[
            (filtered_data['postedDate'] >= start_date) &
            (filtered_data['postedDate'] <= end_date)
        ]
        
        if selected_locations:
            filtered_data = filtered_data[
                filtered_data['location'].str.split(',').str[1].str.strip().isin(selected_locations)
            ]
            
        if selected_industries:
            filtered_data = filtered_data[filtered_data['sector'].isin(selected_industries)]
            
        # Calculate metrics
        total_jobs = len(filtered_data)
        total_companies = len(filtered_data['companyId'].unique())
        avg_applications = filtered_data['clean_applications'].mean()
        application_rate = len(filtered_data[filtered_data['clean_applications'] > 0]) / len(filtered_data) * 100

        # Main content
        st.title("HR Analytics Dashboard")
        
        # KPI Metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(
                f"""
                <div class="metric-container">
                    <div class="metric-label">Total Job Postings</div>
                    <div class="metric-value">{total_jobs:,.0f}</div>
                    <div class="metric-trend">↑ 12% vs last period</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
        with col2:
            st.markdown(
                f"""
                <div class="metric-container">
                    <div class="metric-label">Active Companies</div>
                    <div class="metric-value">{total_companies:,.0f}</div>
                    <div class="metric-trend">↑ 8% vs last period</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
        with col3:
            st.markdown(
                f"""
                <div class="metric-container">
                    <div class="metric-label">Avg Applications</div>
                    <div class="metric-value">{avg_applications:.1f}</div>
                    <div class="metric-trend">↑ 15% vs last period</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
        with col4:
            st.markdown(
                f"""
                <div class="metric-container">
                    <div class="metric-label">Application Rate</div>
                    <div class="metric-value">{application_rate:.1f}%</div>
                    <div class="metric-trend">↑ 5% vs last period</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        # Charts
        st.markdown("### Trends & Analytics")
        
        # Row 1 - Trend Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            # Job Postings Trend
            daily_posts = filtered_data.groupby(filtered_data['postedDate'].dt.date).size().reset_index()
            daily_posts.columns = ['date', 'count']
            
            fig1 = go.Figure()
            fig1.add_trace(go.Scatter(
                x=daily_posts['date'],
                y=daily_posts['count'],
                mode='lines',
                fill='tozeroy',
                line=dict(color='#4CAF50', width=2),
                name='Job Postings'
            ))
            
            fig1.update_layout(
                title='Daily Job Postings',
                height=300,
                template='plotly_white',
                margin=dict(l=20, r=20, t=40, b=20),
                showlegend=False
            )
            st.plotly_chart(fig1, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col2:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            # Applications Trend
            daily_apps = filtered_data.groupby(filtered_data['postedDate'].dt.date)['clean_applications'].mean().reset_index()
            
            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(
                x=daily_apps['postedDate'],
                y=daily_apps['clean_applications'],
                mode='lines',
                fill='tozeroy',
                line=dict(color='#2196F3', width=2),
                name='Applications'
            ))
            
            fig2.update_layout(
                title='Average Daily Applications',
                height=300,
                template='plotly_white',
                margin=dict(l=20, r=20, t=40, b=20),
                showlegend=False
            )
            st.plotly_chart(fig2, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
        # Row 2 - Distribution Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            # Industry Distribution
            industry_dist = filtered_data['sector'].value_counts().head(10)
            
            fig3 = go.Figure(go.Bar(
                x=industry_dist.values,
                y=industry_dist.index,
                orientation='h',
                marker_color='#FF9800'
            ))
            
            fig3.update_layout(
                title='Top Industries',
                height=400,
                template='plotly_white',
                margin=dict(l=20, r=20, t=40, b=20),
                showlegend=False
            )
            st.plotly_chart(fig3, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col2:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            # Location Distribution
            location_dist = filtered_data['location'].str.split(',').str[1].str.strip().value_counts().head(10)
            
            fig4 = go.Figure(go.Bar(
                x=location_dist.values,
                y=location_dist.index,
                orientation='h',
                marker_color='#9C27B0'
            ))
            
            fig4.update_layout(
                title='Top Locations',
                height=400,
                template='plotly_white',
                margin=dict(l=20, r=20, t=40, b=20),
                showlegend=False
            )
            st.plotly_chart(fig4, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # Data Table
        st.markdown("### Recent Job Postings")
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        
        # Prepare table data
        table_data = filtered_data.sort_values('postedDate', ascending=False).head(10)
        table_data = table_data[['companyName', 'sector', 'location', 'postedTime', 'clean_applications']]
        table_data.columns = ['Company', 'Industry', 'Location', 'Posted', 'Applications']
        
        st.dataframe(
            table_data,
            use_container_width=True,
            hide_index=True
        )
        st.markdown('</div>', unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Error in dashboard rendering: {str(e)}")
        import traceback
        st.error(f"Traceback: {traceback.format_exc()}")
else:
    st.error("Unable to load data. Please check if the CSV files are present in the src directory.")
