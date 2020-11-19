# -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc, asc, func
from config import app_config, app_active

config = app_config[app_active]

db = SQLAlchemy(config.APP)

class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mac = db.Column(db.String(400), unique=False, nullable=False)
    date_created = db.Column(db.DateTime(6), default=db.func.current_timestamp(), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer)
    active = db.Column(db.Boolean(), default=1, nullable=True)