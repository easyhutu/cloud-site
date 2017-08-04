from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.contrib.fixers import ProxyFix
import multiprocessing, threading

app = Flask(__name__, static_url_path='')
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./db/cloud.db'
app.config['SQLALCHEMY_ECHO'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.secret_key = 'saf678sf97as6#^**$#af670*^&^&%&$254'
app.wsgi_app = ProxyFix(app.wsgi_app)
db = SQLAlchemy(app)

from manage import manage

app.register_blueprint(manage, url_prefix='/disk')

from admin import admin

app.register_blueprint(admin, url_prefix='/admin')


@app.route('/')
def hello_world():
    return redirect(url_for('manage.home'))


@app.route('/404/')
def get_error():
    return '404-抱歉您无法访问此网页'


from manage.dropFiles import drop_files

"""
这里开的一个进程目的是为了执行定时回收站文件清理
在/manage/dropFiles
实测这里是没用的，所以只能手动把这个脚本起来。。。
"""
if __name__ == '__main__':
    app.run()
    #multiprocessing.Process(target=drop_files).start()
