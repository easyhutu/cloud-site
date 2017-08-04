"""
CREAT: 2017/5/6
AUTHOR:　HEHAHUTU
"""
from flask import Blueprint

admin = Blueprint('admin', __name__)

from admin.views import *

admin.add_url_rule('/login/', view_func=Login.as_view('login'))
admin.add_url_rule('/exit/', view_func=Exit.as_view('exit'))
admin.add_url_rule('/register/', view_func=Register.as_view('register'))
admin.add_url_rule('/checkuser/', view_func=CheckUser.as_view('checkuser'))
admin.add_url_rule('/userInfo/', view_func=UsersInfo.as_view('userInfo'))
admin.add_url_rule('/changeInfo/', view_func=ChangeInfo.as_view('changeInfo'))
admin.add_url_rule('/manageUsers/', view_func=ManageUsers.as_view('manageUsers'))
admin.add_url_rule('/userList/', view_func=UserList.as_view('userList'))
admin.add_url_rule('/setUser/', view_func=SetUser.as_view('setUser'))
admin.add_url_rule('/delUser/', view_func=DelUser.as_view('delUser'))
admin.add_url_rule('/findPwd/', view_func=FindPwd.as_view('findPwd'))
admin.add_url_rule('/joinGroup/', view_func=JoinGroup.as_view('joinGroup'))
admin.add_url_rule('/message/', view_func=Messages.as_view('message'))
admin.add_url_rule('/getMessage/', view_func=GetMessage.as_view('getMessage'))
admin.add_url_rule('/changeMessage/', view_func=ChangeMessage.as_view('changeMessage'))
