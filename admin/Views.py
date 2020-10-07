# -*- coding: utf-8 -*-
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from config import app_config, app_active

config = app_config[app_active]



class UserView(ModelView):

  column_labels = {
    'funcao': 'Função',
    'username': 'Nome de usuário',
    'email': 'E-mail',
    'date_created': 'Data de criação',
    'last_update': 'Última atualização',
    'active': 'Ativo',
    'password': 'Senha',
}

  column_exclude_list = ['password', 'recovery_code']
  form_excluded_columns = ['last_update', 'recovery_code']
  
  form_widget_args = {
    'password': {
      'type': 'password'
    }
  }
  can_set_page_size = True
  can_view_details = True
  column_searchable_list = ['username', 'email']
  column_filters = ['username', 'email', 'funcao']
  column_editable_list = ['username', 'email', 'funcao', 'active']
  create_modal = True
  edit_modal = True
  can_export = True
  column_sortable_list = ['username']
  column_default_sort = ('username', True)
  column_details_exclude_list = ['password', 'recovery_code']
  column_export_exclude_list = ['password', 'recovery_code']
  export_types = ['json', 'yaml', 'csv', 'xls', 'df']

  def on_model_change(self, form, User, is_created):
    if 'password' in form:
      if form.password.data is not None:
        User.set_password(form.password.data)
    else:
        del form.password