# -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy

from model.user import User
from sqlalchemy.orm import relationship

from sqlalchemy import desc, asc, and_, func
from config import app_config, app_active

config = app_config[app_active]

db = SQLAlchemy(config.APP)

class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mac = db.Column(db.String(400), unique=False, nullable=False)
    date_created = db.Column(db.DateTime(6), default=db.func.current_timestamp(), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    userid = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    active = db.Column(db.Boolean(), default=1, nullable=True)
    cliente = relationship(User)

    def get_devices_online(self):
        try:
            res = db.session.query(Device).filter(and_(Device.status == 'ON', Device.userid==self.userid)).all()
        except Exception as e:
            res = None
            print(e)
        finally:
            db.session.close()
            return res