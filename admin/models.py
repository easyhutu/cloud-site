"""
CREAT: 2017/5/6
AUTHOR:　HEHAHUTU
"""
from run import db
from datetime import datetime

"""
authority: 权限目前定义 0 网管 1 用户组成员 2 普通用户 3 封禁用户
login_time: c = datetime.utcfromtimestamp(1494254503.9756198) 保存为时间戳字符串在使用过程中调用此方法
valid_date 过期时间
is_upload_folder： 上传文件权限
is_create_folder： 创建文件夹权限
is_download_folder： 下载文件权限
use_size： 可用空间 单位 M

"""


class Users(db.Model):
    __tablename_ = 'users'
    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.String(300))
    show_name = db.Column(db.String(300))
    password = db.Column(db.String(300))
    password_forget = db.Column(db.String(300))
    email = db.Column(db.String(500))
    login_time = db.Column(db.String(200))
    real_folder = db.Column(db.String(200))
    valid_date = db.Column(db.DATETIME)
    register_key = db.Column(db.String(200))
    share_key = db.Column(db.String(200))
    sync_key = db.Column(db.String(200))
    authority = db.Column(db.INTEGER)
    use_size = db.Column(db.INTEGER)
    is_upload_folder = db.Column(db.INTEGER)
    is_create_folder = db.Column(db.INTEGER)
    is_download_folder = db.Column(db.INTEGER)
    user_group_id = db.Column(db.INTEGER)
    create_time = db.Column(db.DATETIME)

    def __init__(self, name, show_name, password, password_forget, email, login_time=None, real_folder=None,
                 valid_date=None, register_key=None, share_key=None, sync_key=None,
                 authority=1, use_size=500, is_upload_folder=0, is_create_folder=0, is_download_folder=0,
                 user_group_id=0, create_time=datetime.now()):
        self.name = name
        self.show_name = show_name
        self.password = password
        self.password_forget = password_forget
        self.email = email
        self.login_time = login_time
        self.real_folder = real_folder
        self.valid_date = valid_date
        self.register_key = register_key
        self.share_key = share_key
        self.sync_key = sync_key
        self.authority = authority
        self.use_size = use_size
        self.is_upload_folder = is_upload_folder
        self.is_create_folder = is_create_folder
        self.is_download_folder = is_download_folder
        self.user_group_id = user_group_id
        self.create_time = create_time

    def to_user(self):
        return dict(name=self.name, auth=self.authority, id=self.id, valid=self.valid_date, use_size=self.use_size,
                    upload=self.is_upload_folder, create=self.is_create_folder, download=self.is_download_folder)

    def to_json(self):
        return dict(name=self.name, auth=self.authority, id=self.id, )


class Message(db.Model):
    __tablename_ = 'message'
    id = db.Column(db.INTEGER, primary_key=True)
    user_id = db.Column(db.INTEGER)
    user_name = db.Column(db.String(200))
    user_showname = db.Column(db.String(200))
    to_id = db.Column(db.INTEGER)
    to_name = db.Column(db.String(200))
    to_showname = db.Column(db.String(200))
    group_id = db.Column(db.INTEGER)
    title = db.Column(db.String(1000))
    body = db.Column(db.String(1000))
    is_show = db.Column(db.INTEGER)
    create_time = db.Column(db.DATETIME)

    def __init__(self, user_id, user_name, user_showname, to_id, to_name, to_showname, group_id, title, body, is_show=0,
                 create_time=datetime.now()):
        self.user_id = user_id
        self.user_name = user_name
        self.user_showname = user_showname
        self.to_id = to_id
        self.to_name = to_name
        self.to_showname = to_showname
        self.group_id = group_id
        self.title = title
        self.body = body
        self.is_show = is_show
        self.create_time = create_time

    def to_json(self):
        return dict(user_name=self.user_name, user_showname=self.user_showname, to_name=self.to_name,
                    to_showname=self.to_showname, title=self.title, body=self.body,
                    time=self.create_time.strftime('%Y-%m-%d %H:%M:%S'), id=self.id, is_show=self.is_show)
