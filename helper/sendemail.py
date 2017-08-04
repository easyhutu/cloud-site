import smtplib
from email.message import Message
import urllib.parse
import time


class SendEmail():
    def __init__(self):

        self.info = {}
        self.info['name'] = 'mengjianhua93@gmail.com'
        self.info['password'] = 'meng1993'
        self.server = smtplib.SMTP('smtp.gmail.com', 587)
        self.server.ehlo_or_helo_if_needed()
        self.server.starttls()
        self.server.login(self.info['name'], self.info['password'])

    def Send(self, to='email', sub='title', text='pleace input some thing'):
        Body = '\r\n'.join(
            [f'To: {to}', 'From: {}'.format(self.info['name']), f'Subject: {sub}', '', urllib.parse.quote(text)])
        # message = Message()
        # message['Subject'] = sub  # 邮件标题
        # message['From'] = 'mengjianhua93@gmail.com'
        # message['To'] = to
        # message['Cc'] = to
        # te = str(text.encode('utf8')).split('\'')[1]
        # print(te)
        # message.set_payload(text)  # 邮件正文
        # msg = message.as_string(True)
        # print(msg)
        froms = 'From nobody ' + time.ctime(time.time()) + '\n'
        subs = f'Subject: {sub}\n'
        mfroms = 'From: mengjianhua93@gmail.com\n'
        Tos = f'To: {to}\n'
        Ccs = f'Cc: {to}\n\n'
        msgs = ''.join([froms, subs, mfroms, Tos, Ccs, text])
        print(msgs.encode('utf8'))
        try:
            self.server.sendmail(self.info['name'], to, msgs.encode('utf8'))
            print('send email success')
        except Exception as e:
            print(f'send email error: {e}')

        self.server.quit()


def send_email(content, to_email):
    sender = 'mengjianhua93@gmail.com'
    receiver = to_email
    host = 'smtp.gmail.com'
    port = 587
    msg = Message()
    msg['From'] = 'mengjianhua93@gmail.com'
    msg['To'] = to_email
    msg['Subject'] = 'yuncluod.com'
    try:
        smtp = smtplib.SMTP_SSL(host, port)
        smtp.login(sender, 'meng1993')
        smtp.sendmail(sender, receiver, msg.as_string())
        print('send ok')
    except Exception as e:
        print(e)

if __name__ == '__main__':
#     email = SendEmail()
#
#     email.Send(to='1711621009@qq.com', sub='yun cluod', text='hello python,哈哈还需要测试下新的编码方法')
    send_email('你好，哈哈', '1711621009@qq.com')