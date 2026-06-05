from flask import Flask
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__) 
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db = SQLAlchemy(app)

class Application(db.Model):
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