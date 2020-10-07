# -*- coding: utf-8 -*-
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from admin.Views import UserView


from flask_admin.menu import MenuLink

from model.role import Role
from model.user import User

def start_views(app, db):
  
  admin = Admin(app, name='appMonitor', template_mode='bootstrap3')
  admin.add_view(ModelView(Role, db.session, "Funções", category="Usuários"))
  admin.add_view(UserView(User, db.session, "Usuários",  category="Usuários"))
 