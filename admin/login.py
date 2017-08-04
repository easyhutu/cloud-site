"""
CREAT: 2017/5/7
AUTHOR:　HEHAHUTU
"""
from admin.models import *
from flask import session, redirect, url_for, request
from datetime import datetime


def check_login():
    name = request.cookies.get('user_name')
    login_time = request.cookies.get('login_time')
    password = request.cookies.get('save_id')
    if name and login_time and password:
        check = db.session.query(Users).filter(Users.name == name, Users.password == password,
                                           Users.login_time == login_time).one_or_none()

        if check:
            ch_date = check.valid_date - datetime.now() if check.valid_date is not None else 0
            if check.valid_date is None:
                session['show_name'] = check.show_name
                session['name'] = check.name
                if check.authority == 1 or check.authority == 0:
                    return 1
                else:
                    return None

            elif ch_date.days > 0:
                session['show_name'] = check.show_name
                session['name'] = check.name
                if check.authority in [0, 1, 2]:
                    return 1
                else:
                    return None
            else:
                return -1
        else:
            return None
    else:
        return None
