# -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc, asc, func
from config import app_config, app_active

config = app_config[app_active]

db = SQLAlchemy(config.APP)

class Medicao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(400), unique=True, nullable=False)
    fhr_value = db.Column(db.Integer, nullable=False)
    duration = db.Column(db.Integer, nullable=False)   
    date_created = db.Column(db.DateTime(6), default=db.func.current_timestamp(), nullable=False)
    active = db.Column(db.Boolean(), default=1, nullable=True)

    def get_all(self, limit=None):
        try:
            if limit is None:
                res = db.session.query(Medicao).order_by(desc(Medicao.date_created)).all()
            else:
                res = db.session.query(Medicao).order_by(desc(Medicao.date_created)).limit(limit).all()
        except Exception as e:
            res = []
            print(e)
        finally:
            db.session.close()
            return res 

    def get_medicoes_toquen(self):

        try:
            if limit is None:
                res = db.session.query(Medicao).group_by(Medicao.toquen).all()
            else:
                res = db.session.query(Medicao).group_by(Medicao.toquen).limit(limit).all()
        except Exception as e:
            res = []
            print(e)
        finally:
            db.session.close()
            return res 
