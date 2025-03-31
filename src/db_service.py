from sqlalchemy import create_engine, func, text
from sqlalchemy.orm import sessionmaker
from models import Base, Company, Job, JobPosting
import pandas as pd
from datetime import datetime

class DatabaseService:
    def __init__(self):
        self.engine = create_engine('sqlite:///src/jobs.db')
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def get_total_jobs(self):
        return self.session.query(Job).count()

    def get_total_companies(self):
        return self.session.query(Company).count()

    def get_unique_sectors(self):
        """Get list of unique sectors"""
        return [sector[0] for sector in self.session.query(JobPosting.sector).distinct().all() if sector[0]]

    def get_avg_views(self, sector=None):
        """Get average views with optional sector filter"""
        query = self.session.query(func.avg(JobPosting.views_count))
        if sector:
            query = query.filter(JobPosting.sector == sector)
        result = query.scalar()
        return result if result else 0

    def get_avg_applications(self, sector=None):
        """Get average applications with optional sector filter"""
        query = self.session.query(func.avg(JobPosting.applications_count))
        if sector:
            query = query.filter(JobPosting.sector == sector)
        result = query.scalar()
        return result if result else 0

    def get_total_active_jobs(self, sector=None):
        """Get total active jobs with optional sector filter"""
        query = self.session.query(func.count(JobPosting.job_id))
        if sector:
            query = query.filter(JobPosting.sector == sector)
        return query.scalar() or 0

    def get_unique_states(self):
        locations = self.session.query(Company.location).distinct().all()
        states = []
        for loc in locations:
            if loc[0] and ',' in loc[0]:
                state = loc[0].split(',')[1].strip()
                if state not in states:
                    states.append(state)
        return sorted(states)

    def get_salary_rating_range(self):
        result = self.session.query(func.min(Job.salary_rating), func.max(Job.salary_rating)).first()
        if result and result[0] is not None and result[1] is not None:
            min_rating, max_rating = result
            # Ensure we have a valid range
            if min_rating >= max_rating:
                return (2.0, 5.0)  # Default range if min >= max
            return (min_rating, max_rating)
        return (2.0, 5.0)  # Default range if no data

    def get_contract_type_performance(self):
        query = self.session.query(
            Job.contract_type,
            func.avg(JobPosting.views_count).label('views_count'),
            func.avg(JobPosting.applications_count).label('applications_count')
        ).select_from(Job).join(JobPosting).group_by(Job.contract_type)
        df = pd.read_sql(query.statement, self.session.bind)
        # Round the values
        df['views_count'] = df['views_count'].round().astype(int)
        df['applications_count'] = df['applications_count'].round().astype(int)
        return df

    def get_sector_performance(self):
        query = self.session.query(
            JobPosting.sector,
            func.avg(JobPosting.views_count).label('views_count'),
            func.avg(JobPosting.applications_count).label('applications_count')
        ).group_by(JobPosting.sector)
        df = pd.read_sql(query.statement, self.session.bind)
        # Round the values and sort by total performance
        df['views_count'] = df['views_count'].round().astype(int)
        df['applications_count'] = df['applications_count'].round().astype(int)
        df['total'] = df['views_count'] + df['applications_count']
        df = df.sort_values('total', ascending=True).drop('total', axis=1)
        return df

    def get_experience_level_distribution(self):
        query = self.session.query(
            Job.experience_level,
            func.count(Job.job_id).label('applications_count')
        ).group_by(Job.experience_level)
        df = pd.read_sql(query.statement, self.session.bind)
        total = df['applications_count'].sum()
        df['percentage'] = (df['applications_count'] / total * 100).round(2)
        return df

    def get_views_applications_correlation(self):
        # Get raw data
        query = self.session.query(
            JobPosting.views_count,
            JobPosting.applications_count
        )
        df = pd.read_sql(query.statement, self.session.bind)
        
        # Convert "Over 200" to 200
        df['applications_count'] = df['applications_count'].apply(
            lambda x: 200 if isinstance(x, str) and 'Over 200' in x else x
        )
        
        # Convert to numeric, dropping any non-numeric values
        df['applications_count'] = pd.to_numeric(df['applications_count'], errors='coerce')
        df['views_count'] = pd.to_numeric(df['views_count'], errors='coerce')
        
        # Drop any rows with NaN values
        df = df.dropna()
        
        # Ensure reasonable ranges
        df = df[
            (df['views_count'] >= 0) & 
            (df['views_count'] <= 1000) &  # Cap views at 1000
            (df['applications_count'] >= 0) & 
            (df['applications_count'] <= 200)  # Cap applications at 200
        ]
        
        return df

    def get_monthly_trends(self, sector=None, experience_level=None):
        """Get monthly trends with optional filters"""
        base_query = """
            SELECT 
                strftime('%Y-%m', posted_time) as month,
                avg(views_count) as views_count,
                avg(applications_count) as applications_count
            FROM job_postings
            JOIN jobs ON jobs.job_id = job_postings.job_id
        """
        
        where_clauses = []
        if sector:
            where_clauses.append(f"job_postings.sector = '{sector}'")
        if experience_level:
            where_clauses.append(f"jobs.experience_level = '{experience_level}'")
        
        if where_clauses:
            base_query += " WHERE " + " AND ".join(where_clauses)
        
        query = base_query + " GROUP BY month ORDER BY month"
        
        df = pd.read_sql(text(query), self.session.bind)
        df['views_count'] = df['views_count'].round().astype(int)
        df['applications_count'] = df['applications_count'].round().astype(int)
        return df

    def get_current_distribution(self, sector=None, experience_level=None):
        """Get current job market distribution"""
        # First get distribution by sector
        sector_query = self.session.query(
            JobPosting.sector.label('category'),
            func.count(JobPosting.job_id).label('count')
        )
        if sector:
            sector_query = sector_query.filter(JobPosting.sector == sector)
        if experience_level:
            sector_query = sector_query.join(Job).filter(Job.experience_level == experience_level)
        sector_query = sector_query.group_by(JobPosting.sector)
        
        sector_df = pd.read_sql(sector_query.statement, self.session.bind)
        sector_df['type'] = 'By Sector'
        
        # Then get distribution by experience level
        exp_query = self.session.query(
            Job.experience_level.label('category'),
            func.count(Job.job_id).label('count')
        )
        if sector:
            exp_query = exp_query.join(JobPosting).filter(JobPosting.sector == sector)
        if experience_level:
            exp_query = exp_query.filter(Job.experience_level == experience_level)
        exp_query = exp_query.group_by(Job.experience_level)
        
        exp_df = pd.read_sql(exp_query.statement, self.session.bind)
        exp_df['type'] = 'By Experience'
        
        # Combine the results
        return pd.concat([sector_df, exp_df], ignore_index=True)

    def get_recent_jobs(self):
        query = self.session.query(
            JobPosting.job_url,
            JobPosting.posted_time,
            JobPosting.views_count,
            JobPosting.applications_count,
            Company.company_name,
            Company.location,
            Job.contract_type,
            Job.experience_level,
            Job.salary_rating
        ).join(Job).join(Company).order_by(JobPosting.posted_time.desc()).limit(10)
        return pd.read_sql(query.statement, self.session.bind)

    def __del__(self):
        self.session.close() 