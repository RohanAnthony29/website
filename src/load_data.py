import pandas as pd
import sqlalchemy as sa
import sqlite3
import re
import random
from models import Base, Company, Job, JobPosting

def load_data():
    # Create database engine
    engine = sa.create_engine('sqlite:///src/jobs.db')
    
    # Create all tables
    Base.metadata.create_all(engine)
    
    # Read CSV files
    companies_df = pd.read_csv('src/Company.csv')
    job_postings_df = pd.read_csv('src/JobPosting.csv')
    
    # Rename columns in companies_df to match SQLAlchemy model
    companies_df = companies_df.rename(columns={
        'companyId': 'company_id',
        'companyName': 'company_name',
        'companyUrl': 'company_url'
    })
    
    # Rename columns in job_postings_df to match SQLAlchemy model
    job_postings_df = job_postings_df.rename(columns={
        'jobUrl': 'job_url',
        'Job id': 'job_id',
        'applyUrl': 'apply_url',
        'postedTime': 'posted_time',
        'applyType': 'apply_type',
        'viewsCount': 'views_count',
        'applicationsCount': 'applications_count'
    })
    
    # Extract company name from job URL
    def extract_company(url):
        # Pattern matches text between "at-" and either "-" or "?" or end of string
        match = re.search(r'at-([^-?]+)', url)
        if match:
            company = match.group(1).replace('-', ' ')
            # Remove any numbers and special characters
            company = re.sub(r'[0-9🌳]', '', company)
            # Remove extra spaces and convert to lowercase
            company = ' '.join(company.split()).lower()
            return company
        return None
    
    # Add company_name column
    job_postings_df['company_name'] = job_postings_df['job_url'].apply(extract_company)
    
    # Clean company names in both dataframes
    companies_df['company_name_clean'] = companies_df['company_name'].str.lower().str.strip()
    
    # Create jobs dataframe with additional fields
    jobs_df = pd.DataFrame({
        'job_id': job_postings_df['job_id'],
        'company_id': None,
        'contract_type': job_postings_df['apply_type'].map({'EXTERNAL': 'Full-time', 'INTERNAL': 'Contract'}),
        'experience_level': job_postings_df['job_url'].apply(lambda x: 'Senior' if 'senior' in x.lower() else 'Mid-level' if 'mid' in x.lower() else 'Junior'),
        'salary_rating': pd.Series([round(random.uniform(2.0, 5.0), 1) for _ in range(len(job_postings_df))])  # Random ratings between 2.0 and 5.0
    })
    
    # Create a mapping of clean company names to company IDs
    company_id_map = dict(zip(companies_df['company_name_clean'], companies_df['company_id']))
    
    # Update company_id in jobs dataframe based on the mapping
    for idx, row in job_postings_df.iterrows():
        if row['company_name'] in company_id_map:
            jobs_df.loc[jobs_df['job_id'] == row['job_id'], 'company_id'] = company_id_map[row['company_name']]
    
    # Add sector information to job postings
    job_postings_df['sector'] = job_postings_df['job_url'].apply(
        lambda x: 'AI' if 'ai' in x.lower() or 'machine-learning' in x.lower() else
                 'Blockchain' if 'blockchain' in x.lower() or 'crypto' in x.lower() else
                 'Data' if 'data' in x.lower() else 'Other'
    )
    
    # Convert applications count to numeric
    job_postings_df['applications_count'] = job_postings_df['applications_count'].apply(
        lambda x: 200 if 'Over 200' in str(x) else int(x) if str(x).isdigit() else 0
    )
    
    # Load data into tables
    companies_df.to_sql('companies', engine, if_exists='replace', index=False)
    jobs_df.to_sql('jobs', engine, if_exists='replace', index=False)
    job_postings_df.to_sql('job_postings', engine, if_exists='replace', index=False)
    
    print("Data loaded successfully!")

if __name__ == "__main__":
    load_data() 