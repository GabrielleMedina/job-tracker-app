from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta


app = Flask(__name__) 
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db = SQLAlchemy(app)

class ApplicationEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String, nullable=False)
    position = db.Column(db.String, nullable=False)
    date_initiated = db.Column(db.Date)
    date_end = db.Column(db.Date)
    link = db.Column(db.String)
    status = db.Column(db.String, nullable=False)

with app.app_context():
    db.create_all()

@app.route("/")
def hello_world():
    return "<p>Hello, World! </p>"

@app.route("/applications")
def applications(): 
    applications = ApplicationEntry.query.order_by(ApplicationEntry.date_initiated.desc()).all()
    return render_template("applications.html", applications=applications)

@app.route("/new_application", methods=['POST', 'GET'])
def new_application(): 
    if request.method == 'POST':
        form_company_name = request.form['company_name'].strip()
        form_position = request.form['position'].strip()
        form_date_initiated = datetime.strptime(request.form['date_initiated'], "%Y-%m-%d").date()
        form_date_end = datetime.strptime(request.form['date_end'], "%Y-%m-%d").date() if request.form['date_end'] else None
        form_link = request.form['link'].strip()
        form_status = request.form['status'].strip()

        new_application = ApplicationEntry(
            company_name=form_company_name,
            position=form_position,
            date_initiated=form_date_initiated,
            date_end=form_date_end,
            link=form_link,
            status=form_status
        )
        try: 
            db.session.add(new_application)
            db.session.commit()
            return redirect(url_for('applications'))
        except Exception:
            db.session.rollback()
            flash('Something went wrong with saving your application. Please try again.', 'error')
        
    return render_template("new_application.html")

@app.route("/edit_application/<int:application_id", methods=["GET", "POST"])
def edit_application(application_id):
    application = db.get_or_404(ApplicationEntry, application_id)
    if request.method == 'POST':
        form_company_name = request.form['company_name'].strip()
        form_position = request.form['position'].strip()
        form_date_initiated = datetime.strptime(request.form['date_initiated'], "%Y-%m-%d").date()
        form_date_end = datetime.strptime(request.form['date_end'], "%Y-%m-%d").date() if request.form['date_end'] else None
        form_link = request.form['link'].strip()
        form_status = request.form['status'].strip()

        application.company_name=form_company_name,
        application.position=form_position,
        application.date_initiated=form_date_initiated,
        application.date_end=form_date_end,
        application.link=form_link,
        application.status=form_status
        try: 
            db.session.commit()
            return redirect(url_for('applications'))
        except Exception:
            db.session.rollback()
            flash('Something went wrong with saving your application. Please try again.', 'error')
            return redirect(url_for('edit_application', application_id=application_id))
    
    return render_template("edit_entry.html", application=application)

