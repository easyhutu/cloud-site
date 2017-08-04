"""
CREAT: 2017/5/6
AUTHOR:　HEHAHUTU
"""
from datetime import datetime, timedelta
from flask.views import MethodView
from admin.models import *
from flask import jsonify, request, render_template, send_file, send_from_directory, make_response, redirect, url_for
from flask import session, flash, make_response
import os, shutil, json, time
from helper.creat_hash import creat_hash
from admin.login import check_login
from helper.sendemail import SendEmail
import threading


class Login(MethodView):
    def get(self):
        return render_template('admin/login.html')

    def post(self):
        save_password = True if request.form.get('save_password') else False
        name = request.form.get('name')
        password = request.form.get('password')
        if password and name:
            hash_pwd = creat_hash(password)
            check_user = db.session.query(Users).filter(Users.name == name, Users.password == hash_pwd).one_or_none()
            if check_user:
                if check_user.authority != 3:
                    session['show_name'] = check_user.show_name
                    session['name'] = check_user.name
                    session['user_id'] = check_user.id
                    login_time = str(time.time())
                    check_user.login_time = login_time
                    db.session.commit()
                    if save_password:
                        resp = make_response(redirect(url_for('manage.home')))
                        resp.set_cookie('user_name', check_user.name, expires=datetime.now() + timedelta(days=15))
                        resp.set_cookie('save_id', check_user.password, expires=datetime.now() + timedelta(days=15))
                        resp.set_cookie('login_time', login_time, expires=datetime.now() + timedelta(days=15))
                        return resp
                    resp = make_response(redirect(url_for('manage.home')))
                    resp.set_cookie('user_name', check_user.name)
                    resp.set_cookie('save_id', check_user.password)
                    resp.set_cookie('login_time', login_time)
                    return resp
                else:
                    return '您的账户处于封禁期，无法登陆！'
            else:
                flash('用户名和密码不匹配，请重新输入！')
                return render_template('admin/login.html')
        else:
            flash('用户名和密码必填，请输入！')
            return render_template('admin/login.html')


class Exit(MethodView):
    def get(self):
        if request.cookies.get('save_id'):
            resp = make_response(redirect(url_for('.exit')))
            resp.set_cookie('user_name', expires=0)
            resp.set_cookie('login_time', expires=0)
            resp.set_cookie('save_id', expires=0)
            return resp
        if session.get('name'):
            session.pop('name')
        if session.get('show_name'):
            session.pop('show_name')
        if session.get('user_id'):
            session.pop('user_id')
        return redirect(url_for('.login'))


# 在config.json 中可配置 is_register 是false时不允许注册， 目前新创建用户不会有任何权限
class Register(MethodView):
    def get(self):
        with open('config.json', encoding='utf8') as f:
            data = json.loads(f.read())
        if data['is_register']:
            return render_template('admin/register.html')
        else:
            return '抱歉，管理员关闭了注册通道！'

    def post(self):

        name = request.form.get('name')
        show_name = request.form.get('show_name')

        password = request.form.get('password')
        email = request.form.get('email')
        forget_password = request.form.get('forget_password')
        group_id = session.get('group_id')
        hash_pwd = creat_hash(password)
        if name and show_name and password and email:
            if name.isalnum():
                real_folder = '/' + name + datetime.now().strftime('%Y%m%d%H%M%f')
                vail_date = datetime.now() + timedelta(days=1500)
                os.mkdir(f'static/disk{real_folder}')
                if group_id:
                    user = Users(name, show_name, hash_pwd, forget_password, email, real_folder=real_folder,
                                 valid_date=vail_date, authority=2, user_group_id=group_id)
                else:
                    user = Users(name, show_name, hash_pwd, forget_password, email, real_folder=real_folder,
                                 valid_date=vail_date, authority=2)
                db.session.add(user)
                db.session.commit()
                return jsonify({'status': 'ok', 'msg': name})
            else:
                return jsonify({'status': 'error', 'msg': '抱歉用户名必须是字母或字母数字组合'})
        else:
            return jsonify({'status': 'error', 'msg': '获取的数据不完整，无法注册'})


class CheckUser(MethodView):
    def get(self):
        name = request.args.get('name').lower()
        check = db.session.query(Users).filter(Users.name == name).one_or_none()
        return jsonify(check is None)


# 用户信息
class UsersInfo(MethodView):
    def get(self):
        check_user = check_login()
        if check_user is None:
            return redirect(url_for('admin.login'))
        if check_user == -1:
            return '抱歉您的账号过期，请联系管理员'

        user_id = session.get('user_id')
        username = db.session.query(Users).filter(Users.id == user_id).one_or_none()
        login_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(username.login_time)))
        user = {'login_time': login_time, 'name': username.show_name, 'valid_date': username.valid_date,
                'email': username.email, 'auth': username.authority}
        if username.authority == 0:
            ctrls = [['修改密码', 'change-pwd'], ['修改密保', 'change-fgpwd'], ['管理用户', 'mg-user'], ['反馈查看', 'msg-show'],
                     ['发公告', 'create-msg'], ['发群公告', 'create-group-msg'], ['发邮件', 'send-email'],
                     ['生成邀请码', 'create-key'], ['清除分享链', 'clear-share']]
        elif username.authority == 1:
            ctrls = [['修改密码', 'change-pwd'], ['修改密保', 'change-fgpwd'], ['管理组员', 'mg-user'], ['生成邀请码', 'create-key'],
                     ['反馈', 'msg-send'], ['发群公告', 'create-group-msg'], ['清除分享链', 'clear-share']]
        elif username.authority == 2:
            ctrls = [['修改密码', 'change-pwd'], ['修改密保', 'change-fgpwd'], ['反馈', 'msg-send'], ['清除分享链', 'clear-share']]
        else:
            ctrls = []
        return render_template('admin/userinfo.html', uu=user, ctrls=ctrls)


# 修改用户信息
class ChangeInfo(MethodView):
    def post(self):
        check_user = check_login()
        if check_user is None:
            return redirect(url_for('admin.login'))
        if check_user == -1:
            return '抱歉您的账号过期，请联系管理员'

        user_id = session.get('user_id')
        username = db.session.query(Users).filter(Users.id == user_id).one_or_none()
        show_name = request.form.get('show_name')
        email = request.form.get('email')
        oldpwd = request.form.get('oldpwd')
        newpwd = request.form.get('newpwd')
        pwd = request.form.get('pwd')
        fgpwd = request.form.get('fgpwd')
        user_id = session.get('user_id')
        reg_key = request.form.get('reg_key')
        if show_name:
            if len(show_name) > 15:
                return jsonify({'status': 'error', 'msg': '用户名长度不能大于15个字符！'})
            else:
                if len(show_name) < 3:
                    return jsonify({'status': 'error', 'msg': '用户名长度不能小于3个字符！'})
                elif username.authority in [0, 1]:
                    user = db.session.query(Users).filter(Users.id == user_id).one_or_none()
                    user.show_name = show_name
                    db.session.commit()
                    return jsonify({'status': 'ok', 'msg': '用户名修改成功'})
                else:
                    return jsonify({'status': 'error', 'msg': '您无法修改用户名，如需修改请联系管理员'})
        elif email:
            if len(email) < 50:
                user = db.session.query(Users).filter(Users.id == user_id).one_or_none()
                keys = creat_hash(str(time.clock()))
                user.share_key = keys
                db.session.commit()
                urls = f'http://yuncluod.com:8000/admin/changeInfo/?uId={user_id}&email={email}&key={keys}'
                body = f'您正在使用易云提供的服务，修改邮箱请点击链接,如您没有进行此操作，请忽略此邮件：　{urls}'
                try:
                    em = SendEmail()
                    # threading.Thread(target=em.Send, args=(email, 'yun cluod', body)).start()
                    em.Send(email, 'yun cluod', body)
                    return jsonify({'status': 'ok', 'msg': '请前往对应邮箱点击链接完成修改'})
                except Exception as e:
                    return jsonify({'status': 'error', 'msg': f'抱歉抱歉向目标邮箱发送邮件失败，code: {e}'})

            else:
                return jsonify({'status': 'error', 'msg': '抱歉邮箱字符长度不能大于50个字符！'})
        elif oldpwd and newpwd:
            haold = creat_hash(oldpwd)
            user = db.session.query(Users).filter(Users.id == user_id, Users.password == haold).one_or_none()
            if user:
                if len(newpwd) > 15:
                    return jsonify({'status': 'error', 'msg': '新密码长度不能大于15个字符！'})
                else:
                    if len(newpwd) < 3:
                        return jsonify({'status': 'error', 'msg': '新密码长度不能小于3个字符！'})
                    else:
                        hanew = creat_hash(newpwd)
                        user.password = hanew
                        db.session.commit()
                        return jsonify({'status': 'ok', 'msg': '密码修改成功'})
            else:
                return jsonify({'status': 'error', 'msg': '您输入的旧密码有误'})
        elif pwd and fgpwd:
            haold = creat_hash(pwd)
            user = db.session.query(Users).filter(Users.id == user_id, Users.password == haold).one_or_none()
            if user:
                if len(pwd) > 15:
                    return jsonify({'status': 'error', 'msg': '密保不能大于15个字符！'})
                else:
                    if len(pwd) < 3:
                        return jsonify({'status': 'error', 'msg': '密保不能小于3个字符！'})
                    else:
                        user.password_forget = fgpwd
                        db.session.commit()
                        return jsonify({'status': 'ok', 'msg': '密保修改成功'})
            else:
                return jsonify({'status': 'error', 'msg': '您输入的密码有误'})
        elif reg_key:
            user = db.session.query(Users).filter(Users.id == user_id).one_or_none()

            if user:
                key = creat_hash(user.name + str(time.time()))
                user.register_key = key
                db.session.commit()
                return jsonify({'status': 'ok', 'msg': key})
            else:
                return jsonify({'status': 'error', 'msg': 'failed'})
        else:
            user = db.session.query(Users).filter(Users.id == user_id).one_or_none()
            user.authority = 55
            db.session.commit()
            return {'status': 'error', 'msg': '系统判定您的操作非法！账户已被临时封禁'}

    def get(self):
        user_id = request.args.get('uId')
        email = request.args.get('email')
        key = request.args.get('key')
        if user_id and email and key:
            user = db.session.query(Users).filter(Users.id == user_id, Users.share_key == key).one_or_none()
            if user and len(email) < 50:
                user.email = email
                db.session.commit()
                return redirect(url_for('manage.home'))
            else:
                return '抱歉验证失败！'

        else:
            return '抱歉获取数据无效，请检查URL是否完整'


class ManageUsers(MethodView):
    def get(self):
        check_user = check_login()
        if check_user is None:
            return redirect(url_for('admin.login'))
        if check_user == -1:
            return '抱歉您的账号过期，请联系管理员'
        user_id = session.get('user_id')
        check_alib = db.session.query(Users).filter(Users.id == user_id).one_or_none()
        if check_alib.authority in [0, 1]:
            group = request.args.get('key')

            return render_template('admin/users.html', group=group)
        else:
            return '抱歉你无此权限！'


class UserList(MethodView):
    def post(self):
        check_user = check_login()
        if check_user is None:
            return jsonify({'status': 'error', 'msg': 'no authority'})
        if check_user == -1:
            return jsonify({'status': 'error', 'msg': 'user is valid'})
        user_id = session.get('user_id')
        check_alib = db.session.query(Users).filter(Users.id == user_id).one_or_none()
        if check_alib.authority == 0:
            page = int(request.form.get('page', 0))
            nums = (page - 1 if page >= 0 else 0) * 10
            group = request.form.get('group')
            if group == 'group':
                allus = db.session.query(Users).filter(Users.user_group_id == user_id).order_by(Users.id.desc())[
                        nums: nums + 10]
                counts = db.session.query(Users).filter(Users.user_group_id == user_id).count()
                all_page = int(counts / 10) + (1 if counts % 10 != 0 else 0)
            else:
                allus = db.session.query(Users).filter().order_by(Users.id.desc())[nums: nums + 10]
                counts = db.session.query(Users).filter().count()
                all_page = int(counts / 10) + (1 if counts % 10 != 0 else 0)
            return jsonify({'status': 'ok', 'data': [us.to_json() for us in allus], 'len': len(allus), 'now': page,
                            'all': all_page, 'auth': check_alib.authority})
        elif check_alib.authority == 1:
            page = int(request.form.get('page', 0))
            nums = (page - 1 if page >= 0 else 0) * 10
            allus = db.session.query(Users).filter(Users.user_group_id == user_id).order_by(Users.id.desc())[
                    nums: nums + 10]
            counts = db.session.query(Users).filter(Users.user_group_id == user_id).count()
            all_page = int(counts / 10) + (1 if counts % 10 != 0 else 0)
            return jsonify({'status': 'ok', 'data': [us.to_json() for us in allus], 'len': len(allus), 'now': page,
                            'all': all_page})
        else:
            return jsonify({'status': 'error', 'msg': 'user is valid'})


class SetUser(MethodView):
    def get(self):
        check_user = check_login()
        if check_user is None:
            return jsonify({'status': 'error', 'msg': 'no authority'})
        if check_user == -1:
            return jsonify({'status': 'error', 'msg': 'user is valid'})
        id = request.args.get('key')
        user_id = session.get('user_id')
        check_alib = db.session.query(Users).filter(Users.id == user_id).one_or_none()
        user = db.session.query(Users).filter(Users.id == id).one_or_none()
        if user:
            return jsonify({'status': 'ok', 'data': user.to_user(), 'auth': check_alib.authority})
        else:
            return jsonify({'status': 'error', 'msg': 'user is none'})

    def post(self):
        check_user = check_login()
        if check_user is None:
            return jsonify({'status': 'error', 'msg': 'no authority'})
        if check_user == -1:
            return jsonify({'status': 'error', 'msg': 'user is valid'})

        user_id = session.get('user_id')
        check_alib = db.session.query(Users).filter(Users.id == user_id).one_or_none()
        if check_alib.authority == 0:
            id = request.form.get('id')
            auth = request.form.get('auth')
            create = request.form.get('create')
            upload = request.form.get('upload')
            download = request.form.get('download')
            use_size = request.form.get('use_size')
            if id and int(auth) in [0, 1, 2, 3] and int(create) in [0, 1] and int(upload) in [0, 1] and int(
                    download) in [0, 1] and int(use_size) in [0, 1, 2]:
                user = db.session.query(Users).filter(Users.id == id).one_or_none()
                if user:
                    authority = int(auth)
                    create = int(create)
                    upload = int(upload)
                    download = int(download)
                    use_size = (int(use_size) + 1) * 512
                    user.authority = authority
                    user.is_create_folder = create
                    user.is_upload_folder = upload
                    user.is_download_folder = download
                    user.use_size = use_size
                    db.session.commit()
                    return jsonify({'status': 'ok', 'msg': 'save ok'})

                else:
                    return jsonify({'status': 'error', 'msg': 'ERROR user is none'})
            else:
                return jsonify({'status': 'error', 'msg': 'ERROR INFO'})
        elif check_alib.authority == 1:
            id = request.form.get('id')
            auth = request.form.get('auth')
            create = request.form.get('create')
            upload = request.form.get('upload')
            download = request.form.get('download')
            use_size = request.form.get('use_size')
            if id and int(auth) in [0, 1, 2, 3] and int(create) in [0, 1] and int(upload) in [0, 1] and int(
                    download) in [0, 1] and int(use_size) in [0, 1, 2]:
                user = db.session.query(Users).filter(Users.id == id).one_or_none()
                if user:
                    # authority = int(auth)
                    create = int(create)
                    upload = int(upload)
                    download = int(download)
                    # use_size = (int(use_size) + 1) * 512
                    # user.authority = authority
                    user.is_create_folder = create
                    user.is_upload_folder = upload
                    user.is_download_folder = download
                    # user.use_size = use_size
                    db.session.commit()
                    return jsonify({'status': 'ok', 'msg': 'save ok'})

                else:
                    return jsonify({'status': 'error', 'msg': 'ERROR user is none'})
            else:
                return jsonify({'status': 'error', 'msg': 'ERROR INFO'})
        else:
            return jsonify({'status': 'error', 'msg': 'user is valid'})


class DelUser(MethodView):
    def post(self):
        check_user = check_login()
        if check_user is None:
            return jsonify({'status': 'error', 'msg': 'no authority'})
        if check_user == -1:
            return jsonify({'status': 'error', 'msg': 'user is valid'})
        user_id = session.get('user_id')
        check_alib = db.session.query(Users).filter(Users.id == user_id).one_or_none()
        if check_alib.authority == 0:
            del_id = request.form.get('key')
            user = db.session.query(Users).filter(Users.id == del_id).one_or_none()
            if user:
                db.session.delete(user)
                db.session.commit()
                return jsonify({'status': 'ok'})
            else:
                return jsonify({'status': 'error', 'msg': f'无此用户，错误代码：{del_id}'})
        elif check_alib.authority == 1:
            del_id = request.form.get('key')
            user = db.session.query(Users).filter(Users.id == del_id).one_or_none()
            if user:
                user.user_group_id = 0
                db.session.commit()
                return jsonify({'status': 'ok'})
            else:
                return jsonify({'status': 'error', 'msg': f'无此用户，错误代码：{del_id}'})
        else:
            return jsonify({'status': 'error', 'msg': '抱歉您无此权限，如需删除请联系管理员'})


class FindPwd(MethodView):
    def get(self):
        user_id = request.args.get('key')
        if user_id:
            user = db.session.query(Users).filter(Users.id == user_id).one_or_none()
            if user:
                if user.register_key == 'ok':
                    newpwd = creat_hash('666666')
                    user.password = newpwd
                    user.register_key = '0'
                    db.session.commit()
                    return redirect(url_for('.login'))
                else:
                    return '修改错误'
            else:
                return '修改错误'

    def post(self):
        name = request.form.get('name')
        if name:
            user = db.session.query(Users).filter(Users.name == name).one_or_none()
            if user:
                if user.email:
                    email = user.email
                    urls = f'http://yuncluod.com:8000/admin/findPwd/?key={user.id}'
                    body = f'您正在使用易云提供的服务，点击此链接后您的账户密码将会重置为666666,如您没有进行此操作，请忽略此邮件：　{urls}'
                    user.register_key = 'ok'
                    db.session.commit()
                    try:
                        em = SendEmail()
                        # threading.Thread(target=em.Send, args=(email, 'yun cluod', body)).start()
                        em.Send(email, 'yun cluod', body)
                        return jsonify({'status': 'ok', 'msg': '请前往邮箱点击链接完成重置密码'})
                    except Exception as e:
                        return jsonify({'status': 'error', 'msg': f'抱歉向目标邮箱发送邮件失败，code: {e}'})


                else:
                    return jsonify({'status': 'error', 'msg': '抱歉，该账户未保存邮箱无法找回'})
            else:
                return jsonify({'status': 'error', 'msg': '无此用户'})
        else:
            return jsonify({'status': 'error', 'msg': f'无此用户'})


class JoinGroup(MethodView):
    def get(self):
        return render_template('admin/join.html')

    def post(self):
        key = request.form.get('key')
        user = db.session.query(Users).filter(Users.register_key == key).one_or_none()
        if user:
            session['group_id'] = user.id
            return render_template('admin/register.html', group_name='您的邀请人是：' + user.show_name)
        else:
            flash('您输入的邀请码不存在')
            return render_template('admin/join.html')


class Messages(MethodView):
    def get(self):
        key = request.args.get('key')
        if key == 'feedback':
            return render_template('admin/message.html', fb='@反馈意见')
        elif key == 'allUser':
            return render_template('admin/message.html', fb=f'@全体成员')
        elif key == 'groupUser':
            return render_template('admin/message.html', fb=f'@群组成员')
        elif key:
            return render_template('admin/message.html', fb=f'@{key}')
        else:
            return render_template('admin/message.html', fb='')

    def post(self):
        check_user = check_login()
        if check_user is None:
            return jsonify({'status': 'error', 'msg': 'no authority'})
        if check_user == -1:
            return jsonify({'status': 'error', 'msg': 'user is valid'})
        user_id = session.get('user_id')
        author = request.form.get('author')
        title = request.form.get('title')
        body = request.form.get('body')
        sender = db.session.query(Users).filter(Users.id == user_id).one_or_none()
        if author and title and body:
            if len(author) > 20 or len(title) > 20 or len(body) > 300:
                return jsonify({'status': 'error', 'msg': '输入字符过长'})
            else:

                if author == '@反馈意见':
                    users = db.session.query(Users).filter(Users.authority == 0).all()

                    for user in users:
                        me = Message(user_id=user_id, user_name=sender.name, user_showname=sender.show_name,
                                     to_id=user.id, to_name=user.name, to_showname=user.show_name, title=title,
                                     body=body, is_show=0,
                                     create_time=datetime.now(), group_id=0)
                        db.session.add(me)
                        db.session.commit()
                    return jsonify({'status': 'ok', 'msg': 'ok'})
                elif author == '@全体成员':
                    threading.Thread(target=send_all, args=(user_id, sender, title, body)).start()
                    return jsonify({'status': 'ok', 'msg': 'ok'})
                elif author == '@群组成员':
                    threading.Thread(target=send_all, args=(user_id, sender, title, body, True)).start()
                    return jsonify({'status': 'ok', 'msg': 'ok'})
                else:
                    user = db.session.query(Users).filter(Users.name == author.replace('@', '')).one_or_none()

                    if user:
                        me = Message(user_id=user_id, user_name=sender.name, user_showname=sender.show_name,
                                     to_id=user.id, to_name=user.name, to_showname=user.show_name, title=title,
                                     body=body, is_show=0,
                                     create_time=datetime.now(), group_id=0)
                        db.session.add(me)
                        db.session.commit()
                        return jsonify({'status': 'ok', 'msg': 'ok'})
                    else:
                        return jsonify({'status': 'error', 'msg': '没有改用户'})

        else:
            return jsonify({'status': 'error', 'msg': '输入内容不完整'})


class GetMessage(MethodView):
    def get(self):
        check_user = check_login()
        if check_user is None:
            return jsonify({'status': 'error', 'msg': 'no authority'})
        if check_user == -1:
            return jsonify({'status': 'error', 'msg': 'user is valid'})
        user_id = session.get('user_id')
        msgs = db.session.query(Message).filter(Message.to_id == user_id, Message.is_show == 0).all()
        count = len(msgs)
        return jsonify({'status': 'ok', 'count': count})

    def post(self):
        check_user = check_login()
        if check_user is None:
            return jsonify({'status': 'error', 'msg': 'no authority'})
        if check_user == -1:
            return jsonify({'status': 'error', 'msg': 'user is valid'})
        user_id = session.get('user_id')
        counts = db.session.query(Message).filter(Message.to_id == user_id).count()

        page = int(request.form.get('page', 0))
        nums = (page - 1 if page >= 0 else 0) * 5
        msgs = db.session.query(Message).filter(Message.to_id == user_id).order_by(Message.id.desc())[nums: nums + 5]

        all_page = int(counts / 5) + (1 if counts % 5 != 0 else 0)
        return jsonify({'status': 'ok', 'data': [msg.to_json() for msg in msgs], 'len': len(msgs), 'now': page,
                        'all': all_page})


class ChangeMessage(MethodView):
    def get(self):
        check_user = check_login()
        if check_user is None:
            return jsonify({'status': 'error', 'msg': 'no authority'})
        if check_user == -1:
            return jsonify({'status': 'error', 'msg': 'user is valid'})
        user_id = session.get('user_id')
        key = request.args.get('key')
        msg = db.session.query(Message).filter(Message.id == key, Message.to_id == user_id).one_or_none()
        msg.is_show = 1
        db.session.commit()
        return jsonify({'status': 'ok', 'msg': 'ok'})

    def post(self):
        check_user = check_login()
        if check_user is None:
            return jsonify({'status': 'error', 'msg': 'no authority'})
        if check_user == -1:
            return jsonify({'status': 'error', 'msg': 'user is valid'})
        user_id = session.get('user_id')
        key = request.form.get('key')
        msg = db.session.query(Message).filter(Message.id == key, Message.to_id == user_id).one_or_none()
        db.session.delete(msg)
        db.session.commit()
        return jsonify({'status': 'ok', 'msg': 'ok'})


def send_all(user_id, sender, title, body, is_group=False):
    from run import app
    with app.app_context():

        if is_group:
            users = db.session.query(Users).filter(Users.user_group_id == user_id).all()
            for user in users:
                me = Message(user_id=user_id, user_name=sender.name, user_showname=sender.show_name,
                             to_id=user.id, to_name=user.name, to_showname=user.show_name, title=title,
                             body=body, is_show=0,
                             create_time=datetime.now(), group_id=0)
                db.session.add(me)
                db.session.commit()
        else:
            users = db.session.query(Users).all()
            for user in users:
                me = Message(user_id=user_id, user_name=sender.name, user_showname=sender.show_name,
                             to_id=user.id, to_name=user.name, to_showname=user.show_name, title=title,
                             body=body, is_show=0,
                             create_time=datetime.now(), group_id=0)
                db.session.add(me)
                db.session.commit()
