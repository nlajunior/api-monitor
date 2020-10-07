# -*- coding: utf-8 -*-
from flask import Flask, request, redirect, render_template, Response, json, session
from flask_babelex import Babel

# config import
from config import app_config, app_active
from admin.Admin import start_views

from controller.user import UserController
from controller.historico import MedicaoController

config = app_config[app_active]

from flask_sqlalchemy import SQLAlchemy

def create_app(config_name):
    app = Flask(__name__, template_folder='templates')
    app.secret_key = config.SECRET
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['FLASK_ADMIN_SWATCH'] = 'paper'

    babel=Babel(app)

    db = SQLAlchemy(config.APP)
    start_views(app,db)

    db.init_app(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin','*')
        response.headers.add('Access-Control-Allow-Headers','Content-Type')
        response.headers.add('Access-Control-Allow-Methods','GET,PUT,POST,DELETE,OPTIONS')
        
        return response

    @babel.localeselector
    def get_locale():
        override = request.args.get('lang')
        
        if override:
            session['lang']=override
        return session.get('lang', 'pt_BR')


    @app.route('/')
    def index():
        return 'Hello World!'

    @app.route('/login/')
    def login():
        return 'Tela de login'

    @app.route('/login/', methods=['POST'])
    def login_post():
        user = UserController()
        email = request.form['email']
        password = request.form['password']

        result = user.login(email, password)

        if result:
            return redirect('/admin')
        else:
            return render_template('login.html', data={'status': 401, 'msg': 'Dados de usuário incorretos', 'type': None})

    @app.route('/recovery-password/')
    def recovery_password():
        return 'Tela de recuperação de senha'
    
    @app.route('/recovery-password/', methods=['POST'])
    def send_recovery_password():
        user = UserController()
        result = user.recovery(request.form['email'])
        if result:
            return render_template('recovery.html', data={'status': 200, 'msg': 'E-mail de recuperação enviado com sucesso'})
        else:
            return render_template('recovery.html', data={'status': 401, 'msg': 'Erro ao enviar e-mail de recuperação'})

    @app.route('/user/<user_id>', methods=['GET'])
    
    def get_user_profile(user_id):
        header = {}
        user = UserController()
        response = user.get_user_by_id(user_id=user_id)
        return Response(json.dumps(response, ensure_ascii=False), mimetype='application/json'), response[
            'status'], header
    
    @app.route('/medicoes/', methods=['GET'])
    @app.route('/medicoes/<limit>', methods=['GET'])
    def get_medicoes(limit=None):
        header = {}
        medicao = medicaoController()
        response = medicao.get_medicoes(limit=limit)
        return Response(json.dumps(response, ensure_ascii=False), mimetype='application/json'), response[
            'status'], header


   
    return app