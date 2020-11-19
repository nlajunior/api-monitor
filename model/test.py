# -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc, asc, func
from config import app_config, app_active

config = app_config[app_active]

db = SQLAlchemy(config.APP)

class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    duration = db.Column(db.Integer, nullable=False) 
    fhr_value = db.Column(db.Integer, nullable=False) 
    date_created = db.Column(db.DateTime(6), default=db.func.current_timestamp(), nullable=False)
    token = db.Column(db.String(400), unique=False, nullable=False)
    device_mac = db.Column(db.String(100), nullable=False)
    active = db.Column(db.Boolean(), default=1, nullable=True)

    def get_all(self, limit=None):
        try:
            if limit is None:
                res = db.session.query(Test).order_by(desc(Test.date_created)).all()
            else:
                res = db.session.query(Test).order_by(desc(Test.date_created)).limit(limit).all()
        except Exception as e:
            res = []
            print(e)
        finally:
            db.session.close()
            return res 

    def get_tests_token(self, limit=None):
        try:
            if limit is None:
                res = db.session.query(Test).group_by(Test.token).all()
            else:
                res = db.session.query(Test).group_by(Test.token).limit(limit).all()
        except Exception as e:
            res = []
            print(e)
        finally:
            db.session.close()
            return res
   
    def get_tests_date(self):
        try:
           res = db.session.query(Test).filter(Test.date_created==self.date_created).all()
        except Exception as e:
            res =[]
            print(e)
        finally:
            db.session.close()
            return res