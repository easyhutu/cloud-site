"""
CREAT: 2017/8/12
AUTHOR:　HEHAHUTU
"""

from run import db

class Musics(db.Model):
    __tablename__ = 'music'
    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.TEXT)
