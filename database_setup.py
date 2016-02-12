from sqlalchemy import Column, ForeignKey, Integer, String, Date, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Jobs(Base):
    __tablename__ = 'jobs'
    job_id = Column(Integer, primary_key=True)
    created = Column(DateTime)
    job_title = Column(String(250))
    job_url = Column(String(250))
    company_name = Column(String(250))
    company_url = Column(String(250))
    company_phone = Column(String(25))
    company_contact = Column(String(250))
    applied_on = Column(Date)
    cover_page = Column(String(8000))
    notes = Column(String(8000))
    first_interview = Column(Date)
    second_interview = Column(Date)
    third_interview = Column(Date)

engine = create_engine('sqlite:///jobs.db')
Base.metadata.create_all(engine)