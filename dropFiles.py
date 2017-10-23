"""
CREAT: 2017/5/20
AUTHOR:　HEHAHUTU
"""
from manage.models import *
import time
from datetime import datetime
import admin.models
import json
import os

"""
每天执行一次，时间为24点20分
"""


def drop_files():
    while True:
        trash_folders = db.session.query(DiskFolder).filter(DiskFolder.is_trash == 1).all()
        fol_count = []
        file_count = []
        if trash_folders:

            for item in trash_folders:
                vali_date = item.update_time - datetime.now()
                if vali_date.days < 0:
                    fol_count.append('1')
                    db.session.delete(item)
                    db.session.commit()
                    print('del ', item)
        trash_files = db.session.query(DiskFile).filter(DiskFile.is_trash == 1).all()
        if trash_files:

            for item in trash_files:
                vali_date = item.update_time - datetime.now()

                if vali_date.days < 0:
                    file_count.append('1')
                    user_id = item.user_id
                    user_folder = admin.models.db.session.query(admin.models.Users.real_folder).filter(
                        admin.models.Users.id == user_id).scalar()
                    filename = item.file_name
                    file_path = f'static/disk{user_folder}/{filename}'
                    os.remove(file_path)
                    db.session.delete(item)
                    db.session.commit()
                    print('del ', item)
        with open('drop_file.log', 'a', encoding='utf8') as f:
            f.write(
                f'[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] delete file: {len(file_count)}, folder: {len(fol_count)}\n')
        print('*'*50)
        time.sleep(60 * 60 * 24)


if __name__ == '__main__':
    drop_files()
