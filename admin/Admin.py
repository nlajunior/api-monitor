# -*- coding: utf-8 -*-
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from admin.Views import HomeView, UserView, RoleView

from flask_admin.menu import MenuLink

from model.role import Role
from model.user import User

def start_views(app, db):
  
  admin = Admin(app, name='appMonitor',base_template='admin/base.html', template_mode='bootstrap3', index_view=HomeView())
  admin.add_view(RoleView(Role, db.session, "Funções", category="Usuários"))
  admin.add_view(UserView(User, db.session, "Usuários",  category="Usuários"))

  admin.add_link(MenuLink(name='Logout', url='/logout'))
 