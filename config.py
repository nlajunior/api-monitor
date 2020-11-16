import os
import random, string, json

with open('/home/nljunior/app/config.json') as config_file:
    config = json.load(config_file)

class Config(object):
    CSRF_ENABLED = True
    SECRET = config.get('SECRET')
    SQLALCHEMY_DATABASE_URI = config.get('SQLALCHEMY_DATABASE_URI')
    TEMPLATE_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    APP = None
    SENDGRID_API_KEY = 'API_KEY'

class DevelopmentConfig(Config):
    TESTING = False
    DEBUG = True
    IP_HOST = 'localhost'
    PORT_HOST = 5000
    URL_MAIN = 'http://%s:%s/' % (IP_HOST, PORT_HOST)

class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    IP_HOST = '0.0.0.0' # Aqui geralmente é um IP de um servidor na nuvem e não o endereço da máquina local
    PORT_HOST = 8000
    URL_MAIN = 'http://%s:%s/' % (IP_HOST, PORT_HOST)

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    IP_HOST = 'localhost' # Aqui geralmente é um IP de um servidor na nuvem e não o endereço da máquina local
    PORT_HOST = 80
    URL_MAIN = 'http://%s:%s/' % (IP_HOST, PORT_HOST)

app_config = {
    'development': DevelopmentConfig(),
    'testing': TestingConfig(),
    'production': ProductionConfig()
}

app_active= config.get('FLASK_ENV')