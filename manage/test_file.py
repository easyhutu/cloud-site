"""
CREAT: 2017/5/7
AUTHOR:　HEHAHUTU
"""
import os
from manage.models import *
from datetime import datetime

filename = r'../static/disk/admin_201705071236939437/readme.txt'
filesize = os.path.getsize(filename) / 1024
name = 'readme.txt'
file_path = '/'
folder_group = '/disk'
create = datetime.now()

folder_name = 'disk'
folder_path = '/'
folder = DiskFolder(folder_name, folder_path, 0, 1, 0, creat_time=create)
db.session.add(folder)
db.session.commit()
#
file = DiskFile(name, name, filesize, file_path, 1, 1, creat_time=create)
db.session.add(file)
db.session.commit()
print(filesize)