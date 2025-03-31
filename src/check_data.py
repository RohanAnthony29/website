from sqlalchemy import create_engine
import pandas as pd
from models import Company, Job, JobPosting

def check_data():
    # Create database connection
    engine = create_engine('sqlite:///src/jobs.db')
    
    # Check companies table
    print("\nCompanies table:")
    companies_df = pd.read_sql("SELECT * FROM companies LIMIT 5", engine)
    print(companies_df)
    print(f"Total companies: {len(pd.read_sql('SELECT * FROM companies', engine))}")
    
    # Check jobs table
    print("\nJobs table:")
    jobs_df = pd.read_sql("SELECT * FROM jobs LIMIT 5", engine)
    print(jobs_df)
    print(f"Total jobs: {len(pd.read_sql('SELECT * FROM jobs', engine))}")
    
    # Check job_postings table
    print("\nJob postings table:")
    job_postings_df = pd.read_sql("SELECT * FROM job_postings LIMIT 5", engine)
    print(job_postings_df)
    print(f"Total job postings: {len(pd.read_sql('SELECT * FROM job_postings', engine))}")

if __name__ == "__main__":
    check_data() 