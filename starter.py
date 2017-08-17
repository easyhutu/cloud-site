"""
CREAT: 2017/8/17
AUTHOR:　HEHAHUTU
"""
import os
from datetime import datetime
import time
import threading

"""
/var/www/cloud_venv/bin/python3 /var/www/cloud_venv/bin/gunicorn -w3 -b127.0.0.1:6000 run:app
"""


def now():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def start_gun():
    os.system('/var/www/cloud_venv/bin/python3 /var/www/cloud_venv/bin/gunicorn -w3 -b127.0.0.1:6000 run:app')


try:
    ps_data = os.popen('ps -aux|grep gunicorn')

    pid = ps_data.read()
    print(pid)
    try:
        pids = pid.split()[1]
        print(pids)

        os.popen(f'kill -9 {pids}')
    except Exception as e:
        print(e)
    print('kill ok')
    time.sleep(1)
    threading.Thread(target=start_gun).start()
    print('restart ok')
except Exception as e:
    print(e)
    base_path = os.getcwd()
    with open(os.path.join(base_path, 'start_error.log'), 'w', encoding='utf8') as f:
        f.write(f'[{now()}] error code: {e}')
