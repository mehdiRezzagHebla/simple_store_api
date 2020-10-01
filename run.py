from app import app
from db import dbalch

dbalch.init_app(app)

@app.before_first_request
def create_tables():
    dbalch.create_all()
