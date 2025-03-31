from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Company(Base):
    __tablename__ = 'companies'
    
    company_id = Column(Integer, primary_key=True)
    company_name = Column(String)
    company_url = Column(String)
    location = Column(String)
    sector = Column(String)
    
    # Relationship with jobs
    jobs = relationship("Job", back_populates="company")

class Job(Base):
    __tablename__ = 'jobs'
    
    job_id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey('companies.company_id'))
    contract_type = Column(String)
    experience_level = Column(String)
    salary_rating = Column(Float)
    
    # Relationship with company
    company = relationship("Company", back_populates="jobs")
    # Relationship with job posting
    job_posting = relationship("JobPosting", back_populates="job", uselist=False)

class JobPosting(Base):
    __tablename__ = 'job_postings'
    
    job_id = Column(Integer, ForeignKey('jobs.job_id'), primary_key=True)
    job_url = Column(String)
    apply_url = Column(String)
    posted_time = Column(String)
    apply_type = Column(String)
    views_count = Column(Integer)
    applications_count = Column(Integer)
    sector = Column(String)
    
    # Relationship with job
    job = relationship("Job", back_populates="job_posting")

# Create database engine
engine = create_engine('sqlite:///src/jobs.db')

# Create all tables
Base.metadata.create_all(engine) 