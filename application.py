import datetime

from flask import Flask, render_template, request, redirect
from flask import session as login_session, url_for, flash, make_response
from werkzeug import secure_filename
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Jobs

app = Flask(__name__)

engine = create_engine('sqlite:///jobs.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
def home():
    return 'Home!'
    
@app.route('/jobs')
def show_jobs():
    ttl_jobs = session.query(Jobs).count()
    page = 1
    if request.args.get('p') != None:
        page = int(request.args.get('p'))
    per_page = 10
    if request.args.get('pp') != None:
        per_page = int(request.args.get('pp'))
    ttl_pages=(ttl_jobs / per_page)
    if ttl_pages < 1:
        ttl_pages = 1
    job_list = session.query(Jobs).limit(per_page).offset((page - 1) * per_page)
    return render_template('jobs.html', job_list=job_list, page=page, 
        per_page=per_page, ttl_pages=ttl_pages)
    
@app.route('/job/new', methods=['GET', 'POST'])
def new_job():
    if request.method == 'POST':
        appliedOnDate = None
        if request.form['applied_on'] != '':
            appliedOnDate = datetime.datetime.strptime(request.form['applied_on'], '%Y-%m-%d').date()
        newJob = Jobs(job_title=request.form['job_title'], created=datetime.datetime.now(), 
            job_url=request.form['job_url'], company_name=request.form['company_name'],
            company_url=request.form['company_url'], company_phone=request.form['company_phone'],
            company_contact=request.form['company_contact'], applied_on=appliedOnDate,
            cover_page=request.form['cover_page'], notes=request.form['notes'])
        session.add(newJob)
        session.commit()
        return redirect(url_for('show_jobs'))
    else:
        return render_template('new_job.html')

@app.route('/job/edit/<int:job_id>', methods=['GET', 'POST'])
def edit_job(job_id):
    if request.method == 'POST':
        #update code here
        return redirect(url_for('show_jobs'))
    else:
        job = session.query(Jobs).filter_by(job_id=job_id).one()
        return render_template('edit_job.html', job_id=job_id, job_title=job.job_title, 
            job_url=job.job_url, company_name=job.company_name, company_url=job.company_url,
            company_phone=job.company_phone, company_contact=job.company_contact)
        
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
