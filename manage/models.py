"""
CREAT: 2017/5/6
AUTHOR:　HEHAHUTU
"""
from run import db
from datetime import datetime

"""
folder_path : 文件路径
group_id： 所属文件夹id
user_id： 所属用户id
user_group：该文件是否向用户组开放


"""


class DiskFolder(db.Model):
    __tablename_ = 'disk_folder'
    id = db.Column(db.INTEGER, primary_key=True)
    folder_name = db.Column(db.String(500))
    folder_path = db.Column(db.String(1000))
    group_id = db.Column(db.INTEGER)
    user_id = db.Column(db.INTEGER)
    is_trash = db.Column(db.INTEGER)
    is_share = db.Column(db.INTEGER)
    is_user_group = db.Column(db.INTEGER)
    create_time = db.Column(db.DATETIME)
    update_time = db.Column(db.DATETIME)

    def __init__(self, folder_name, folder_path, group_id, user_id, is_trash=0, is_share=0, is_user_group=None,
                 creat_time=None,
                 update_time=datetime.now()):
        self.folder_name = folder_name
        self.folder_path = folder_path
        self.group_id = group_id
        self.user_id = user_id
        self.is_trash = is_trash
        self.is_share = is_share
        self.is_user_group = is_user_group
        self.create_time = creat_time
        self.update_time = update_time

    def __repr__(self):
        return f'< id: {self.id}  folder name: {self.folder_name} create time: {self.create_time}>'

    def to_json(self):
        group_folder = self.folder_path.split('/')[-1]
        return dict(foldername=self.folder_name, update_time=self.update_time.strftime('%Y-%m-%d %H:%M:%S'), id=self.id,
                    group_folder=group_folder)


class DiskFile(db.Model):
    __tablename__ = 'disk_file'
    id = db.Column(db.INTEGER, primary_key=True)
    show_name = db.Column(db.String(500))
    file_name = db.Column(db.String(500))
    file_size = db.Column(db.INTEGER)
    file_path = db.Column(db.String(1000))
    folder_group_id = db.Column(db.INTEGER)
    user_id = db.Column(db.INTEGER)
    is_trash = db.Column(db.INTEGER)
    is_share = db.Column(db.INTEGER)
    is_user_group = db.Column(db.INTEGER)
    create_time = db.Column(db.DATETIME)
    update_time = db.Column(db.DATETIME)

    def __init__(self, show_name, file_name, file_size, file_path, folder_group_id, user_id, is_trash=0, is_share=0,
                 is_user_group=None,
                 creat_time=None,
                 update_time=datetime.now()):
        self.show_name = show_name
        self.file_name = file_name
        self.file_size = file_size
        self.file_path = file_path
        self.folder_group_id = folder_group_id
        self.user_id = user_id
        self.is_trash = is_trash
        self.is_share = is_share
        self.is_user_group = is_user_group
        self.create_time = creat_time
        self.update_time = update_time

    def __repr__(self):
        return f'< id: {self.id}  file name: {self.file_name} create time: {self.create_time}>'

    def to_json(self):
        if self.file_size > 1024:
            size = str(self.file_size / 1024).split('.')[0]
            new_size = f'{size}M'
        else:
            size = str(self.file_size).split('.')[0]
            new_size = f'{size}K'
        group_folder = self.file_path.split('/')[-1]
        return dict(file_size=new_size, update_time=self.update_time.strftime('%Y-%m-%d %H:%M:%S'), id=self.id,
                    showname=self.show_name, group_folder=group_folder)


class UseLog(db.Model):
    __tablename_ = 'use_log'
    id = db.Column(db.INTEGER, primary_key=True)
    user_id = db.Column(db.INTEGER)
    use_disk_size = db.Column(db.INTEGER)
    upload = db.Column(db.String(500))
    download = db.Column(db.String(500))
    creat_folder = db.Column(db.String(500))
    time = db.Column(db.DATETIME)

    def __init__(self, user_id, use_disk_size=0, upload=None, download=None, creat_folder=None, time=datetime.now()):
        self.user_id = user_id
        self.use_disk_size = use_disk_size
        self.upload = upload
        self.download = download
        self.creat_folder = creat_folder
        self.time = time

    def __repr__(self):
        return f'<id: {self.id} time: {self.time}>'


class ShareGroups(db.Model):
    __tablename__ = 'share_groups'
    id = db.Column(db.INTEGER, primary_key=True)
    user_id = db.Column(db.INTEGER)
    folders = db.Column(db.String(500))
    files = db.Column(db.String(500))
    vail_date = db.Column(db.DATETIME)
    share_key = db.Column(db.String(500))
    time = db.Column(db.DATETIME)

    def __init__(self, user_id, folders, files, vail_date, share_key, time=datetime.now()):
        self.user_id = user_id
        self.folders = folders
        self.files = files
        self.vail_date = vail_date
        self.share_key = share_key
        self.time = time
