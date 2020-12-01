# -*- coding: utf-8 -*-
from flask import Flask, request, redirect, render_template, Response, json, session, abort, jsonify
from flask_bootstrap import Bootstrap
from flask_babelex import Babel

# config import
from config import app_config, app_active
from admin.Admin import start_views

from controller.user import UserController
from controller.medicao import MedicaoController
from controller.device import DeviceController

from functools import wraps
from flask_login import LoginManager, login_user, logout_user

config = app_config[app_active]

from flask_sqlalchemy import SQLAlchemy

def create_app(config_name):
    app = Flask(__name__, template_folder='templates')

    login_manager = LoginManager()
    login_manager.init_app(app)
    
    app.secret_key = config.SECRET
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['FLASK_ADMIN_SWATCH'] = 'paper'

    babel=Babel(app)

    bootstrap = Bootstrap(app)

    db = SQLAlchemy(config.APP)
    start_views(app,db)

    db.init_app(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin','*')
        response.headers.add('Access-Control-Allow-Headers','Content-Type')
        response.headers.add('Access-Control-Allow-Methods','GET,PUT,POST,DELETE,OPTIONS')
        
        return response
    
    def auth_token_required(f):
        @wraps(f)
        def verify_token(*args, **kwargs):
            user = UserController()
            try:
                result = user.verify_auth_token(request.headers.get('token'))
                if result['status'] == 200:
                    return f(*args, **kwargs)
                else:
                    abort(result['status'], result['status'])
            except KeyError as e:
                abort(401, 'Você precisa enviar um token de acesso')

        return verify_token

    @babel.localeselector
    def get_locale():
        override = request.args.get('lang')
        
        if override:
            session['lang']=override
        return session.get('lang', 'pt_BR')
   
    @app.route('/')
    def login():
        return render_template('login.html', data={'status': 200, 'msg': None, 'type': None})

    @app.route('/login/', methods=['POST'])
    def login_post():
        user = UserController()
        email = request.form['email']
        password = request.form['password']

        result = user.login(email, password)

        if result:
            if result.role == 4:
                return render_template('login.html', data={'status': 401, 'msg': 'Seu usuário não tem permissão para acessar o admin', 'type':2})
            else:
                login_user(result)
                return redirect('/admin')
        else:
            return render_template('login.html', data={'status': 401, 'msg': 'Dados de usuário incorretos', 'type': 1})
    
    @app.route('/logout')
    def logout_send():
        logout_user()
        return render_template('login.html', data={'status': 200, 'msg': 'Usuário deslogado com sucesso!', 'type':3})   

    #================================================ API ======================================================================================= 
    @app.route('/organizations/', methods=['POST'])
    def login_api():
        header = {}

        user = UserController()
        
        organizationkey = request.json['organizationkey']
        password = request.json['password']
        result = user.auth_api(organizationkey, password)
        
        code = 401
        response = {"success": "false"}
        
        if result:
            if result.active:
                result = {
                    'id': result.id,
                    'username': result.username,
                    'organizationkey' : result.organizationkey                
                }

                header = {
                    "token": user.generate_auth_token(result),
                    "token_type": "JWT"
                }
                code = 200
                response["success"] = "true"
                response["devices"]= get_devices_online()
                              
        return jsonify ({
            
            'success': response.get('success'),
            'devices': response.get('devices')

            
        }), code, header

    @app.route('/tests/', methods=['GET'])
    @app.route('/tests/<limit>', methods=['GET'])
    @auth_token_required
    def get_all_tests(limit=None):
        header = {
            'token': request.headers['token'],
            "token_type": "JWT"
        }
        medicao = MedicaoController()
        response = medicao.get_tests(limit=limit)
        
        return jsonify({'result': response.get('result'), 'status':response.get('status')}), header

    @app.route('/tests/token/', methods=['GET'])
    @auth_token_required
    def get_tests_token(limit=None):
        header = {
            'token': request.headers['token'],
            "token_type": "JWT"
        }
        medicao = MedicaoController()
        response = medicao.get_tests_token(limit=limit)
        
        return jsonify({'result': response.get('result'), 'status':response.get('status')}), header

    @app.route('/tests/data/<string:date_created>', methods=['GET'])
    def get_test_date_created(date_created):
        header = {
            'token': request.headers['token'],
            "token_type": "JWT"
        }
        medicao = MedicaoController()
        response = medicao.get_tests_date_created(date_created)
             
        return jsonify({'result': response.get('result'), 'status':response.get('status')}), header
    
    #@app.route('/devices/', methods=['GET'])
    def get_devices_online():
        
        device = DeviceController()
        #response = device.get_devices_online()

        #return jsonify({'result': response.get('result')})
        return device.get_devices_online()
        
    @app.route('/test/', methods=['POST'])
    def save_test():
        medicao = MedicaoController()
        result= medicao.save_test(request.json)
            
        if result:
            status = '200'
            
        else:
            status = '401'
        return status
     
    @login_manager.user_loader
    def load_user(user_id):
        user = UserController()
        return user.get_admin_login(user_id)

    return app