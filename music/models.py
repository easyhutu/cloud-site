"""
CREAT: 2017/8/12
AUTHOR:　HEHAHUTU
"""

from run import db
from datetime import datetime


class Musics(db.Model):
    __tablename__ = 'music'
    id = db.Column(db.INTEGER, primary_key=True)
    user_id = db.Column(db.INTEGER)
    name = db.Column(db.TEXT, index=True)
    filename = db.Column(db.TEXT)
    path = db.Column(db.TEXT)
    size = db.Column(db.INTEGER)
    is_craw = db.Column(db.INTEGER)
    is_show = db.Column(db.INTEGER)
    is_trash = db.Column(db.INTEGER)
    star = db.Column(db.INTEGER)
    comment_count = db.Column(db.INTEGER)
    image = db.Column(db.TEXT)
    image_path = db.Column(db.TEXT)
    author = db.Column(db.TEXT)
    lrc = db.Column(db.TEXT)
    time = db.Column(db.DATETIME)

    def __init__(self, user_id, name, filename, path, size, is_craw=0, is_show=1, is_trash=0, star=0, comment_count=0,
                 image=None,
                 image_path=None, author=None, lrc=None, time=datetime.now()):
        self.user_id = user_id
        self.name = name
        self.filename = filename
        self.path = path
        self.size = size
        self.is_craw = is_craw
        self.is_show = is_show
        self.is_trash = is_trash
        self.star = star
        self.comment_count = comment_count
        self.image = image
        self.image_path = image_path
        self.author = author
        self.lrc = lrc
        self.time = time


class MusicComment(db.Model):
    __tablename__ = 'music_comment'
    id = db.Column(db.INTEGER, primary_key=True)
    music_id = db.Column(db.INTEGER, index=True)
    comment_id = db.Column(db.INTEGER)
    user_id = db.Column(db.INTEGER)
    body = db.Column(db.TEXT)
    user_ip = db.Column(db.String(50, convert_unicode=False))

    time = db.Column(db.DATETIME)
