from flask import Flask, redirect, url_for, request, make_response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.contrib.fixers import ProxyFix
import multiprocessing, threading
import requests
from config import MYSQL_USERNAME, MYSQL_PASSWORD, MYSQL_HOTS, MYSQL_DB


app = Flask(__name__, static_url_path='')
app.debug = True
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./db/cloud.db'
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@{MYSQL_HOTS}/{MYSQL_DB}?charset=utf8'
app.config['SQLALCHEMY_ECHO'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.secret_key = 'saf678s@#%^&$%f97asfds6#^**$#af670*^&^&%&$254'
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


@app.route('/pycharmKey.exe/rpc/obtainTicket.action')
def pycharm():
    buildDate = request.args.get('buildDate')
    buildNumber = request.args.get('buildNumber')
    clientVersion = request.args.get('clientVersion')
    hostName = request.args.get('hostName')
    machineId = request.args.get('machineId')
    productCode = request.args.get('productCode')
    productFamilyId = request.args.get('productFamilyId')
    salt = request.args.get('salt')
    secure = request.args.get('secure')
    # userName = request.args.get('userName')
    userName = 'hehahutu'
    version = request.args.get('version')
    versionNumber = request.args.get('versionNumber')
    url = f'http://103.72.166.182:41017/rpc/obtainTicket.action?buildDate={buildDate}&buildNumber={buildNumber}&clientVersion={clientVersion}&hostName={hostName}&machineId={machineId}&productCode={productCode}&productFamilyId={productFamilyId}&salt={salt}&secure={secure}&userName={userName}&version={version}&versionNumber={versionNumber}'

    print(url)
    html = requests.get(url)
    data = str(html.content).replace('ilanyu', 'hehahutu')
    resp = make_response(html.content)
    # resp.headers = html.headers
    resp.headers['Content-Type'] = 'text/plain; charset=utf-8'
    resp.headers['Server'] = 'fasthttp'
    return resp


from manage.dropFiles import drop_files

"""
这里开的一个进程目的是为了执行定时回收站文件清理
在/manage/dropFiles
实测这里是没用的，所以只能手动把这个脚本起来。。。
"""
if __name__ == '__main__':
    app.run()
    # multiprocessing.Process(target=drop_files).start()
