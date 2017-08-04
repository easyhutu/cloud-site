"""
CREAt: 2017/4/11
AUTHOR: Hehahutu
"""
from socket import *
# import socket
from tkinter import *
import json

"""
***************************接口定义******************************
获取时间同步状态：

POST /pu/001511223344/getOnvifTimeSyncReq RS/1.0\r\n
Host: %s:%d\r\n
Content-Length: 0\r\n
Session-Id:%s\r\n
Authentication: Basic %s\r\n
\r\n

设置时间同步开关：

POST /pu/001511223344/setOnvifTimeSyncReq RS/1.0\r\n
Host: %s:%d\r\n
Content-Length: %d\r\n
Session-Id:%s\r\n
Authentication: Basic %s\r\n
\r\n
setFlag=%d\r\n
***************************接口定义******************************
"""


class OnvifTime:
    # 初始化时，默认DMS服务器ip为内网，set_flag: 默认1打开时间同步，0关闭； is_get：否是获取nvr时间状态，默认True操作为获取，False为设置
    def __init__(self, nvr_mac, dms_ip='139.129.252.81', set_flag=1, is_get=True):
        self.ip = dms_ip  # 网管服务器ip
        self.port = 8809
        self.bufsiz = 4096
        self.nvr_mac = nvr_mac
        self.set_flag = set_flag
        self.is_get = is_get
        # self.client = socket(AF_INET, SOCK_STREAM)
        self.client = socket(AF_INET, SOCK_STREAM, 0)
        self.client.connect((self.ip, self.port))

    # 私有类，用于拼接请求头
    def _creat_get_url(self, is_get=True):
        if is_get:
            header = f'POST /pu/{self.nvr_mac}/getOnvifTimeSyncReq RS/1.0\r\n'
            host = f'Host: {self.ip}:{self.port}\r\n'
            content_length = 'Content-Length: 0\r\n'
            authentication = 'Authentication: Basic RGV2aWNlUmVnQWRtaW46RGV2aWNlUmVnQWRtaW4yMDEz\r\n'
            enter = '\r\n'
            # 返回获取的请求头
            return ''.join([header, host, content_length, authentication, enter, enter]).replace('\'', '"')
        elif is_get is False:
            header = f'POST /pu/{self.nvr_mac}/setOnvifTimeSyncReq RS/1.0\r\n'
            host = f'Host: {self.ip}:{self.port}\r\n'
            authentication = 'Authentication: Basic RGV2aWNlUmVnQWRtaW46RGV2aWNlUmVnQWRtaW4yMDEz\r\n'
            setflag = f'setFlag={self.set_flag}\r\n'
            content_length = f'Content-Length: {len(setflag)}\r\n'
            enter = '\r\n'
            # 返回设置的请求头
            return ''.join([header, host, content_length, authentication, enter, setflag, enter]).replace('\'', '"')

    #
    def get_onvif_time(self):

        data = self._creat_get_url(self.is_get)
        try:
            self.client.send(data.encode('utf8'))
            print(f'发送消息到{self.ip} mac: {self.nvr_mac}')
            recv_data = self.client.recv(self.bufsiz)
            da = recv_data.decode().split()[-1]
            # print(da)
            return json.loads(da)


        except Exception as e:
            print(f'error:{str(e)}')
            return {'onvifTimeSyncFlag': 'bad'}


class Windows():
    def __init__(self):
        self.win = Tk()
        self.win.title('NVR时间同步设置')
        self.win.geometry('500x300')
        self.menus = Menu(self.win)
        self.onvif = OnvifTime('001410145431')
        self.dms = {'139.129.252.81': '内网', '112.124.30.215': '外网'}

        Label(self.win, text='DMS平台地址').grid(row=0, column=0)
        self.lisbox = Entry(self.win, width=25)
        self.lisbox.grid(row=0, column=1, columnspan=4)
        Button(self.win, text='切换DMS地址', width=12, command=lambda: self._change_dms()).grid(row=0, column=5, sticky=E)
        Button(self.win, text='退出', width=8, command=lambda: self._quit()).grid(row=0, column=10, sticky=W)

        Label(self.win, text='操作').grid(row=1, column=0)
        Button(self.win, text='获取', width=8, command=lambda: self._get_info()).grid(row=1, column=2, sticky=E)
        Button(self.win, text='设置', width=8, command=lambda: self._set_info()).grid(row=1, column=3, sticky=E)

        self.box_status = Entry(self.win, width=25)
        self.box_status.grid(row=1, column=5, columnspan=4)

        Label(self.win, text='NVR MAC地址').grid(row=3, column=0)
        self.nvr_mac1 = Entry(self.win, width=25)
        self.nvr_mac1.grid(row=3, column=1, columnspan=4)
        self.nvr_mac1_val = Entry(self.win, width=5)
        Label(self.win, text='状态').grid(row=3, column=5)
        self.nvr_mac1_val.grid(row=3, column=6, columnspan=4)

        Label(self.win, text='NVR MAC地址').grid(row=4, column=0)
        self.nvr_mac2 = Entry(self.win, width=25)
        self.nvr_mac2.grid(row=4, column=1, columnspan=4)
        self.nvr_mac2_val = Entry(self.win, width=5)
        Label(self.win, text='状态').grid(row=4, column=5)
        self.nvr_mac2_val.grid(row=4, column=6, columnspan=4)

        Label(self.win, text='NVR MAC地址').grid(row=5, column=0)
        self.nvr_mac3 = Entry(self.win, width=25)
        self.nvr_mac3.grid(row=5, column=1, columnspan=4)
        self.nvr_mac3_val = Entry(self.win, width=5)
        Label(self.win, text='状态').grid(row=5, column=5)
        self.nvr_mac3_val.grid(row=5, column=6, columnspan=4)

        Label(self.win, text='NVR MAC地址').grid(row=6, column=0)
        self.nvr_mac4 = Entry(self.win, width=25)
        self.nvr_mac4.grid(row=6, column=1, columnspan=4)
        self.nvr_mac4_val = Entry(self.win, width=5)
        Label(self.win, text='状态').grid(row=6, column=5)
        self.nvr_mac4_val.grid(row=6, column=6, columnspan=4)

        Label(self.win, text='NVR MAC地址').grid(row=7, column=0)
        self.nvr_mac5 = Entry(self.win, width=25)
        self.nvr_mac5.grid(row=7, column=1, columnspan=4)
        self.nvr_mac5_val = Entry(self.win, width=5)
        Label(self.win, text='状态').grid(row=7, column=5)
        self.nvr_mac5_val.grid(row=7, column=6, columnspan=4)

        Label(self.win, text='NVR MAC地址').grid(row=8, column=0)
        self.nvr_mac6 = Entry(self.win, width=25)
        self.nvr_mac6.grid(row=8, column=1, columnspan=4)
        self.nvr_mac6_val = Entry(self.win, width=5)
        Label(self.win, text='状态').grid(row=8, column=5)
        self.nvr_mac6_val.grid(row=8, column=6, columnspan=4)

        self.nvr_mac_dict = {'nvr1': self.nvr_mac1, 'nvr2': self.nvr_mac2, 'nvr3': self.nvr_mac3, 'nvr4': self.nvr_mac4,
                             'nvr5': self.nvr_mac5, 'nvr6': self.nvr_mac6, }
        self.nvr_val_dict = {'val1': self.nvr_mac1_val, 'val2': self.nvr_mac2_val, 'val3': self.nvr_mac3_val,
                             'val4': self.nvr_mac4_val, 'val5': self.nvr_mac5_val, 'val6': self.nvr_mac6_val, }

        self._change_dms()

        self.box_status.insert(0, '务必保证ip和mac对应！')
        mainloop()

    def _change_dms(self):
        dms_val = self.lisbox.get()
        # print(dms_val)
        self.lisbox.icursor(0)
        self.lisbox.delete(0, END)
        if dms_val:
            # dms_ip = dms_val.split(':')[-1]
            for ip in self.dms.keys():
                if dms_val != ip:
                    # value = ip
                    self.lisbox.insert(0, ip)

        else:
            ip = [ip for ip in self.dms.keys()][0]
            # value = f'{self.dms[ip]}:{ip}'
            self.lisbox.insert(0, ip)

    def _quit(self):
        self.win.quit()

    def _get_info(self):
        self.box_status.delete(0, END)
        self.box_status.insert(0, '正在获取请稍后...')
        mac_list = {}
        dms_val = self.lisbox.get().split()[0]
        for n, key in enumerate(self.nvr_mac_dict.keys()):
            if self.nvr_mac_dict[key].get():
                mac_list[str(n + 1)] = self.nvr_mac_dict[key].get().split()[0]
        print(mac_list)

        if mac_list:
            for key in mac_list.keys():
                onvif = OnvifTime(mac_list[key], dms_ip=dms_val)
                status = onvif.get_onvif_time()['onvifTimeSyncFlag']
                self.nvr_val_dict[f'val{key}'].icursor(0)
                self.nvr_val_dict[f'val{key}'].delete(0, END)
                self.nvr_val_dict[f'val{key}'].insert(0, status)
        self.box_status.delete(0, END)
        self.box_status.insert(0, '已成功获取')

    def _set_info(self):
        self.box_status.delete(0, END)
        self.box_status.insert(0, '正在设置请稍后...')
        mac_list = {}
        mac_status = {}
        dms_val = self.lisbox.get().split()[0]
        for n, key in enumerate(self.nvr_mac_dict.keys()):
            if self.nvr_mac_dict[key].get():
                mac_list[str(n + 1)] = self.nvr_mac_dict[key].get().split()[0]
        print(mac_list)
        for n, key in enumerate(self.nvr_val_dict.keys()):
            if self.nvr_val_dict[key].get():
                mac_status[str(n + 1)] = self.nvr_val_dict[key].get().split()[0]
        print(mac_status)
        for key in mac_status.keys():
            onvif = OnvifTime(mac_list[key], set_flag=mac_status[key], is_get=False, dms_ip=dms_val)
            onvif.get_onvif_time()
        self.box_status.delete(0, END)
        self.box_status.insert(0, '已成功设置')


if __name__ == '__main__':
    onvif = OnvifTime('001410145431', set_flag=1, is_get=True)
    print(onvif.get_onvif_time()['onvifTimeSyncFlag'])
    # Win = Windows()
