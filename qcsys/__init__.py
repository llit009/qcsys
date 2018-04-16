# -*- coding:utf8 -*-
#encoding = utf-8

from flask import Flask

import logging

app = Flask(__name__, instance_relative_config=True)

app.config.from_pyfile('config.py')



from .admin.routes import adminApp
app.register_blueprint(adminApp,url_prefix='/admin')

from .report.routes import reportApp
app.register_blueprint(reportApp,url_prefix='/report')

from . import views

