# -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc, asc, func
from sqlalchemy import and_
from config import app_config, app_active
from datetime import date

config = app_config[app_active]

db = SQLAlchemy(config.APP)

class Medicao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(400), unique=False, nullable=False)
    fhr_value = db.Column(db.Float, nullable=False)
    duration = db.Column(db.Integer, nullable=False)   
    device_id = db.Column(db.Integer, nullable=True)
    date_created = db.Column(db.DateTime(6), default=db.func.current_timestamp(), nullable=False)
    active = db.Column(db.Boolean(), default=1, nullable=True)

    def get_all(self, limit=None):
        try:
            if limit is None:
                res = db.session.query(Medicao).order_by(desc(Medicao.id)).filter(Medicao.date_created==str(date.today())).all()
            else:
                res = db.session.query(Medicao).order_by(desc(Medicao.id)).filter(Medicao.date_created==str(date.today())).limit(limit).all()
             
        except Exception as e:
            res = []
            print(e)
        finally:
            db.session.close()
            return res 

    def get_for_session_id(self, limit=None):
        try:
            if limit is None:
                
                #res = db.session.query(Medicao).filter(Medicao.session_id==self.session_id).all()
                res = db.session.query(Medicao).filter(and_(Medicao.session_id == self.session_id, Medicao.date_created == self.date_created)).all()
            else:
                
                res = db.session.query(Medicao).filter(Medicao.session_id==self.session_id).limit(limit).all()
                #res = db.session.query(Medicao).filter(and_(Medicao.session_id == self.session_id, Medicao.date_created == self.date_created)).all()
        except Exception as e:
            res = []
            print(e)
        finally:
            db.session.close()
            return res
   
    def get_for_date_created(self):
        try:
            res = db.session.query(Medicao).filter(Medicao.date_created==str(self.date_created)).all()
        except Exception as e:
            res =[]
            print(e)
        finally:
            db.session.close()
            return res
    
    def save_test(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            db.session.rollback()
            return False

            