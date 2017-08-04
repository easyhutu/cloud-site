"""
CREAt: 2017/4/25
AUTHOR: Hehahutu
"""
from tkinter import *
import json
import pymysql
import _thread, threading
import time
from socket import *


# 窗体结构类

class Windows():
    # 初始化窗体结构
    def __init__(self):
        self.win = Tk()
        self.win.title('NVR批量升级工具')
        self.win.geometry('760x450')  # 初始化窗体大小
        self.menus = Menu(self.win)

        self.types = [
            'PC4',
            'NVR1825-4HD-H-CS',
            'NVR1825-4HDA-H-CS',
            'NVR1825-9HD-H-CS',
            'NVR1825-9HDA-H-CS',
            'NVR1825-16HD-H-CS',
            'NVR1825-16HDA-H-CS',
            'NVR1822-9HDA-H-CS',
            'NVR1822-16HDA-H-CS',
            'NVR1825-32HD-H-CS',
            'NVR1822-32HDA-H-CS',
        ]

        self.msg = Listbox(self.win, width=50, height=1, fg='red')
        self.msg.grid(row=0, column=0, columnspan=11)
        Label(self.win, text='© ovopark.com').grid(row=0, columnspan=2, column=11)
        # Button(self.win, text='退出', width=8, command=lambda: self.quit()).grid(row=0, column=12, sticky=W)

        Label(self.win, text='企业').grid(row=1, column=0, sticky=W)
        self.enterprise_name = Entry(self.win, width=22)
        self.enterprise_name.grid(row=1, column=1, columnspan=5, sticky=W)
        # Label(self.win, text='设备类型').grid(row=1, column=5, sticky=W)

        self.change_type = Menubutton(text='设备类型')
        self.change_type.grid(row=1, column=5, sticky=W)
        self.change_type.menu = Menu(self.change_type, tearoff=0)
        self.change_type['menu'] = self.change_type.menu
        self.change_type.menu.add_command(label=self.types[0], command=lambda: self.device_type_menu(self.types[0]) )
        self.change_type.menu.add_command(label=self.types[1], command=lambda: self.device_type_menu(self.types[1]))
        self.change_type.menu.add_command(label=self.types[2], command=lambda: self.device_type_menu(self.types[2]))
        self.change_type.menu.add_command(label=self.types[3], command=lambda: self.device_type_menu(self.types[3]))
        self.change_type.menu.add_command(label=self.types[4], command=lambda: self.device_type_menu(self.types[4]))
        self.change_type.menu.add_command(label=self.types[5], command=lambda: self.device_type_menu(self.types[5]))
        self.change_type.menu.add_command(label=self.types[6], command=lambda: self.device_type_menu(self.types[6]))
        self.change_type.menu.add_command(label=self.types[7], command=lambda: self.device_type_menu(self.types[7]))
        self.change_type.menu.add_command(label=self.types[8], command=lambda: self.device_type_menu(self.types[8]))
        self.change_type.menu.add_command(label=self.types[9], command=lambda: self.device_type_menu(self.types[9]))
        self.change_type.menu.add_command(label=self.types[10], command=lambda: self.device_type_menu(self.types[10]))


        self.device_type = Entry(self.win, width=22)
        self.device_type.grid(row=1, column=6, columnspan=5, sticky=W)
        Label(self.win, text='门店').grid(row=1, column=11, sticky=W)
        self.shop_name = Entry(self.win, width=15)
        self.shop_name.grid(row=1, column=12, columnspan=5, sticky=W)
        Button(self.win, text='搜索', width=8,
               command=lambda: threading.Thread(target=self.get_device_info).start()).grid(row=1, column=14, sticky=W,
                                                                                           columnspan=5)

        Label(self.win, text='URL：').grid(row=2, column=0, sticky=W)
        self.update_url = Entry(self.win, width=75)
        self.update_url.grid(row=2, column=1, sticky=W, columnspan=20)
        Button(self.win, text='升级', width=8, bg='red', command=lambda: self.update_button()).grid(row=2, column=13,
                                                                                                  sticky=W)
        Button(self.win, text='重启', width=8, bg='red', command=lambda: self.reboot_button()).grid(row=2, column=14,
                                                                                                  sticky=W)
        self.labelframe = LabelFrame(self.win)
        self.labelframe.grid(row=3, column=0, columnspan=15)

        """
        **********************************************
        下面的这些画出来是一个表格，依赖于self.labelframe
        这个容器。
        **********************************************
        """
        self.show_all = StringVar(value=0)
        self.checkall = Checkbutton(self.labelframe, variable=self.show_all, command=lambda: self.check_change(0))
        self.checkall.grid(row=4, column=0, sticky=W)
        Label(self.labelframe, text='1').grid(row=4, column=2, sticky=W)
        Label(self.labelframe, text='所属门店').grid(row=4, column=2, sticky=W)
        Label(self.labelframe, text='设备类型').grid(row=4, column=3, sticky=W)
        Label(self.labelframe, text='MAC').grid(row=4, column=4, sticky=W)
        Label(self.labelframe, text='设备IP').grid(row=4, column=5, sticky=W)
        Label(self.labelframe, text='版本信息').grid(row=4, column=6, sticky=W)
        Label(self.labelframe, text='所属平台').grid(row=4, column=7, sticky=W)
        Label(self.labelframe, text='状态').grid(row=4, column=8, sticky=W)

        self.show1 = StringVar(value=0)
        self.check1 = Checkbutton(self.labelframe, variable=self.show1, command=lambda: self.check_change(1))
        self.check1.grid(row=5, column=0, sticky=W)
        self.box_shop1 = Listbox(self.labelframe, width=15, height=1)
        self.box_shop1.grid(row=5, column=2)
        self.box_device_name1 = Listbox(self.labelframe, width=15, height=1)
        self.box_device_name1.grid(row=5, column=3)
        self.box_mac1 = Listbox(self.labelframe, width=15, height=1)
        self.box_mac1.grid(row=5, column=4)
        self.box_ip1 = Listbox(self.labelframe, width=15, height=1)
        self.box_ip1.grid(row=5, column=5)
        self.box_version1 = Listbox(self.labelframe, width=15, height=1)
        self.box_version1.grid(row=5, column=6)
        self.box_dms1 = Listbox(self.labelframe, width=15, height=1)
        self.box_dms1.grid(row=5, column=7)
        self.box_status1 = Listbox(self.labelframe, width=10, height=1)
        self.box_status1.grid(row=5, column=8)

        self.show2 = StringVar(value=0)
        self.check2 = Checkbutton(self.labelframe, variable=self.show2, command=lambda: self.check_change(1))
        self.check2.grid(row=6, column=0, sticky=W)
        self.box_shop2 = Listbox(self.labelframe, width=15, height=1)
        self.box_shop2.grid(row=6, column=2)
        self.box_device_name2 = Listbox(self.labelframe, width=15, height=1)
        self.box_device_name2.grid(row=6, column=3)
        self.box_mac2 = Listbox(self.labelframe, width=15, height=1)
        self.box_mac2.grid(row=6, column=4)
        self.box_ip2 = Listbox(self.labelframe, width=15, height=1)
        self.box_ip2.grid(row=6, column=5)
        self.box_version2 = Listbox(self.labelframe, width=15, height=1)
        self.box_version2.grid(row=6, column=6)
        self.box_dms2 = Listbox(self.labelframe, width=15, height=1)
        self.box_dms2.grid(row=6, column=7)
        self.box_status2 = Listbox(self.labelframe, width=10, height=1)
        self.box_status2.grid(row=6, column=8)

        self.show3 = StringVar(value=0)
        self.check3 = Checkbutton(self.labelframe, variable=self.show3, command=lambda: self.check_change(1))
        self.check3.grid(row=7, column=0, sticky=W)
        self.box_shop3 = Listbox(self.labelframe, width=15, height=1)
        self.box_shop3.grid(row=7, column=2)
        self.box_device_name3 = Listbox(self.labelframe, width=15, height=1)
        self.box_device_name3.grid(row=7, column=3)
        self.box_mac3 = Listbox(self.labelframe, width=15, height=1)
        self.box_mac3.grid(row=7, column=4)
        self.box_ip3 = Listbox(self.labelframe, width=15, height=1)
        self.box_ip3.grid(row=7, column=5)
        self.box_version3 = Listbox(self.labelframe, width=15, height=1)
        self.box_version3.grid(row=7, column=6)
        self.box_dms3 = Listbox(self.labelframe, width=15, height=1)
        self.box_dms3.grid(row=7, column=7)
        self.box_status3 = Listbox(self.labelframe, width=10, height=1)
        self.box_status3.grid(row=7, column=8)

        self.show4 = StringVar(value=0)
        self.check4 = Checkbutton(self.labelframe, variable=self.show4, command=lambda: self.check_change(1))
        self.check4.grid(row=8, column=0, sticky=W)
        self.box_shop4 = Listbox(self.labelframe, width=15, height=1)
        self.box_shop4.grid(row=8, column=2)
        self.box_device_name4 = Listbox(self.labelframe, width=15, height=1)
        self.box_device_name4.grid(row=8, column=3)
        self.box_mac4 = Listbox(self.labelframe, width=15, height=1)
        self.box_mac4.grid(row=8, column=4)
        self.box_ip4 = Listbox(self.labelframe, width=15, height=1)
        self.box_ip4.grid(row=8, column=5)
        self.box_version4 = Listbox(self.labelframe, width=15, height=1)
        self.box_version4.grid(row=8, column=6)
        self.box_dms4 = Listbox(self.labelframe, width=15, height=1)
        self.box_dms4.grid(row=8, column=7)
        self.box_status4 = Listbox(self.labelframe, width=10, height=1)
        self.box_status4.grid(row=8, column=8)

        self.show5 = StringVar(value=0)
        self.check5 = Checkbutton(self.labelframe, variable=self.show5, command=lambda: self.check_change(1))
        self.check5.grid(row=9, column=0, sticky=W)
        self.box_shop5 = Listbox(self.labelframe, width=15, height=1)
        self.box_shop5.grid(row=9, column=2)
        self.box_device_name5 = Listbox(self.labelframe, width=15, height=1)
        self.box_device_name5.grid(row=9, column=3)
        self.box_mac5 = Listbox(self.labelframe, width=15, height=1)
        self.box_mac5.grid(row=9, column=4)
        self.box_ip5 = Listbox(self.labelframe, width=15, height=1)
        self.box_ip5.grid(row=9, column=5)
        self.box_version5 = Listbox(self.labelframe, width=15, height=1)
        self.box_version5.grid(row=9, column=6)
        self.box_dms5 = Listbox(self.labelframe, width=15, height=1)
        self.box_dms5.grid(row=9, column=7)
        self.box_status5 = Listbox(self.labelframe, width=10, height=1)
        self.box_status5.grid(row=9, column=8)

        self.show6 = StringVar(value=0)
        self.check6 = Checkbutton(self.labelframe, variable=self.show6, command=lambda: self.check_change(1))
        self.check6.grid(row=10, column=0, sticky=W)
        self.box_shop6 = Listbox(self.labelframe, width=15, height=1)
        self.box_shop6.grid(row=10, column=2)
        self.box_device_name6 = Listbox(self.labelframe, width=15, height=1)
        self.box_device_name6.grid(row=10, column=3)
        self.box_mac6 = Listbox(self.labelframe, width=15, height=1)
        self.box_mac6.grid(row=10, column=4)
        self.box_ip6 = Listbox(self.labelframe, width=15, height=1)
        self.box_ip6.grid(row=10, column=5)
        self.box_version6 = Listbox(self.labelframe, width=15, height=1)
        self.box_version6.grid(row=10, column=6)
        self.box_dms6 = Listbox(self.labelframe, width=15, height=1)
        self.box_dms6.grid(row=10, column=7)
        self.box_status6 = Listbox(self.labelframe, width=10, height=1)
        self.box_status6.grid(row=10, column=8)

        self.show7 = StringVar(value=0)
        self.check7 = Checkbutton(self.labelframe, variable=self.show7, command=lambda: self.check_change(1))
        self.check7.grid(row=11, column=0, sticky=W)
        self.box_shop7 = Listbox(self.labelframe, width=15, height=1)
        self.box_shop7.grid(row=11, column=2)
        self.box_device_name7 = Listbox(self.labelframe, width=15, height=1)
        self.box_device_name7.grid(row=11, column=3)
        self.box_mac7 = Listbox(self.labelframe, width=15, height=1)
        self.box_mac7.grid(row=11, column=4)
        self.box_ip7 = Listbox(self.labelframe, width=15, height=1)
        self.box_ip7.grid(row=11, column=5)
        self.box_version7 = Listbox(self.labelframe, width=15, height=1)
        self.box_version7.grid(row=11, column=6)
        self.box_dms7 = Listbox(self.labelframe, width=15, height=1)
        self.box_dms7.grid(row=11, column=7)
        self.box_status7 = Listbox(self.labelframe, width=10, height=1)
        self.box_status7.grid(row=11, column=8)

        self.show8 = StringVar(value=0)
        self.check8 = Checkbutton(self.labelframe, variable=self.show8, command=lambda: self.check_change(1))
        self.check8.grid(row=12, column=0, sticky=W)
        self.box_shop8 = Listbox(self.labelframe, width=15, height=1)
        self.box_shop8.grid(row=12, column=2)
        self.box_device_name8 = Listbox(self.labelframe, width=15, height=1)
        self.box_device_name8.grid(row=12, column=3)
        self.box_mac8 = Listbox(self.labelframe, width=15, height=1)
        self.box_mac8.grid(row=12, column=4)
        self.box_ip8 = Listbox(self.labelframe, width=15, height=1)
        self.box_ip8.grid(row=12, column=5)
        self.box_version8 = Listbox(self.labelframe, width=15, height=1)
        self.box_version8.grid(row=12, column=6)
        self.box_dms8 = Listbox(self.labelframe, width=15, height=1)
        self.box_dms8.grid(row=12, column=7)
        self.box_status8 = Listbox(self.labelframe, width=10, height=1)
        self.box_status8.grid(row=12, column=8)

        self.show9 = StringVar(value=0)
        self.check9 = Checkbutton(self.labelframe, variable=self.show9, command=lambda: self.check_change(1))
        self.check9.grid(row=13, column=0, sticky=W)
        self.box_shop9 = Listbox(self.labelframe, width=15, height=1)
        self.box_shop9.grid(row=13, column=2)
        self.box_device_name9 = Listbox(self.labelframe, width=15, height=1)
        self.box_device_name9.grid(row=13, column=3)
        self.box_mac9 = Listbox(self.labelframe, width=15, height=1)
        self.box_mac9.grid(row=13, column=4)
        self.box_ip9 = Listbox(self.labelframe, width=15, height=1)
        self.box_ip9.grid(row=13, column=5)
        self.box_version9 = Listbox(self.labelframe, width=15, height=1)
        self.box_version9.grid(row=13, column=6)
        self.box_dms9 = Listbox(self.labelframe, width=15, height=1)
        self.box_dms9.grid(row=13, column=7)
        self.box_status9 = Listbox(self.labelframe, width=10, height=1)
        self.box_status9.grid(row=13, column=8)

        self.show10 = StringVar(value=0)
        self.check10 = Checkbutton(self.labelframe, variable=self.show10, command=lambda: self.check_change(1))
        self.check10.grid(row=14, column=0, sticky=W)
        self.box_shop10 = Listbox(self.labelframe, width=15, height=1)
        self.box_shop10.grid(row=14, column=2)
        self.box_device_name10 = Listbox(self.labelframe, width=15, height=1)
        self.box_device_name10.grid(row=14, column=3)
        self.box_mac10 = Listbox(self.labelframe, width=15, height=1)
        self.box_mac10.grid(row=14, column=4)
        self.box_ip10 = Listbox(self.labelframe, width=15, height=1)
        self.box_ip10.grid(row=14, column=5)
        self.box_version10 = Listbox(self.labelframe, width=15, height=1)
        self.box_version10.grid(row=14, column=6)
        self.box_dms10 = Listbox(self.labelframe, width=15, height=1)
        self.box_dms10.grid(row=14, column=7)
        self.box_status10 = Listbox(self.labelframe, width=10, height=1)
        self.box_status10.grid(row=14, column=8)

        self.box_all_page_info = Listbox(self.labelframe, width=5, height=1)
        self.box_all_page_info.grid(row=15, column=2, columnspan=8)
        self.box_page_info = Listbox(self.labelframe, width=5, height=1)
        self.box_page_info.grid(row=15, column=3, columnspan=8)
        Button(self.labelframe, text='<', width=2, command=lambda: self.change_page(last_page=True)).grid(row=15,
                                                                                                          column=5,
                                                                                                          columnspan=8)
        Button(self.labelframe, text='>', width=2, command=lambda: self.change_page(next_page=True)).grid(row=15,
                                                                                                          column=6,
                                                                                                          columnspan=8)
        Button(self.labelframe, text='<<', command=lambda: self.change_page(start_page=True)).grid(row=15, column=4,
                                                                                                   columnspan=8)
        Button(self.labelframe, text='>>', command=lambda: self.change_page(end_page=True)).grid(row=15, column=7,
                                                                                                 columnspan=8)
        """
        **********************************************
            以下字典表是为了创建显示文本的索引，为插入和删除数据
        提供方便，以后有时间需要优化显示结构。
        **********************************************
        """
        self.check_dic = {'1': self.show1, '2': self.show2, '3': self.show3, '4': self.show4,
                          '5': self.show5, '6': self.show6, '7': self.show7, '8': self.show8,
                          '9': self.show9, '10': self.show10}

        self.shop_dic = {'1': self.box_shop1, '2': self.box_shop2, '3': self.box_shop3, '4': self.box_shop4,
                         '5': self.box_shop5, '6': self.box_shop6, '7': self.box_shop7, '8': self.box_shop8,
                         '9': self.box_shop9, '10': self.box_shop10}
        self.device_name_dic = {'1': self.box_device_name1, '2': self.box_device_name2, '3': self.box_device_name3,
                                '4': self.box_device_name4,
                                '5': self.box_device_name5, '6': self.box_device_name6, '7': self.box_device_name7,
                                '8': self.box_device_name8,
                                '9': self.box_device_name9, '10': self.box_device_name10}
        self.mac_dic = {'1': self.box_mac1, '2': self.box_mac2, '3': self.box_mac3, '4': self.box_mac4,
                        '5': self.box_mac5, '6': self.box_mac6, '7': self.box_mac7, '8': self.box_mac8,
                        '9': self.box_mac9, '10': self.box_mac10}
        self.ip_dic = {'1': self.box_ip1, '2': self.box_ip2, '3': self.box_ip3, '4': self.box_ip4,
                       '5': self.box_ip5, '6': self.box_ip6, '7': self.box_ip7, '8': self.box_ip8,
                       '9': self.box_ip9, '10': self.box_ip10}
        self.version_dic = {'1': self.box_version1, '2': self.box_version2, '3': self.box_version3,
                            '4': self.box_version4,
                            '5': self.box_version5, '6': self.box_version6, '7': self.box_version7,
                            '8': self.box_version8,
                            '9': self.box_version9, '10': self.box_version10}
        self.dms_dic = {'1': self.box_dms1, '2': self.box_dms2, '3': self.box_dms3, '4': self.box_dms4,
                        '5': self.box_dms5, '6': self.box_dms6, '7': self.box_dms7, '8': self.box_dms8,
                        '9': self.box_dms9, '10': self.box_dms10}
        self.status_dic = {'1': self.box_status1, '2': self.box_status2, '3': self.box_status3, '4': self.box_status4,
                           '5': self.box_status5, '6': self.box_status6, '7': self.box_status7, '8': self.box_status8,
                           '9': self.box_status9, '10': self.box_status10}

        self.msg.delete(0, END)
        self.msg.insert(0, '欢迎使用...')
        # 开一个测试连接的线程
        threading.Thread(target=self._init_sql).start()

        mainloop()

    # 退出
    def quit(self):
        self.win.quit()
        if self.api.con:
            self.api.conn.close()

    # 复选框全选
    def check_change(self, key):
        if key == 0:
            check_list = [self.show1, self.show2, self.show3, self.show4, self.show5, self.show6, self.show7,
                          self.show8, self.show9, self.show10]
            check_data = self.show_all.get()
            for show in check_list:
                show.set(check_data)
            print(check_data, 0)
        else:
            print(self.show1.get(), key)

    # 初始化数据库
    def _init_sql(self):
        self.api = DeviceApi('121.43.231.99', 'root', 'kdmkdm', 'shopwebdb', 3306, 5)
        self.msg.delete(0, END)
        self.msg.insert(0, '正在连接数据库...')
        if self.api.test_connect():
            self.msg.delete(0, END)
            self.msg.insert(0, '已成功连接数据库...')
        else:
            self.msg.delete(0, END)
            self.msg.insert(0, '连接数据库失败，无法操作！...')

    # 从数据库拉取数据
    def get_device_info(self):
        enterprise = self.enterprise_name.get().split()[0] if self.enterprise_name.get() else None
        shop = self.shop_name.get().split().split()[0] if self.shop_name.get() else None
        device_type = self.device_type.get().split()[0] if self.device_type.get() else None

        self.device_dic = {}

        if enterprise and device_type:
            print(enterprise, shop)

            self.msg.delete(0, END)
            self.msg.insert(0, '正在查找...')

            sql = 'select id, name from is_enterprise_groups WHERE name = %s'
            self.api.con.execute(sql, (enterprise,))
            enterprise_data = self.api.con.fetchone()
            if enterprise_data:
                self.device_dic['enterprise_id'] = enterprise_data[0]
                self.device_dic['enterprise'] = enterprise_data[1]

                if shop:
                    sql = 'select id, name from is_departments WHERE name = %s'
                    self.api.con.execute(sql, (shop,))
                    shop_data = self.api.con.fetchone()
                    self.device_dic['shop'] = shop_data[1]
                    self.device_dic['shop_id'] = shop_data[0]
                    sql = 'select mac, device_type, device_ip, version, platform_id, depId, group_id from is_device_status WHERE depId = %s AND device_type = %s'
                    self.api.con.execute(sql, (self.device_dic['shop_id'], device_type))
                    devices = self.api.con.fetchall()
                    de = []
                    for device in devices:
                        sql = 'select SERVER from is_platforms WHERE id = %s'
                        self.api.con.execute(sql, (device[4],))
                        dms = self.api.con.fetchone()[0]

                        de.append({'mac': device[0], 'device_type': device[1], 'ip': device[2], 'version': device[3],
                                   'dms': dms, 'shop': self.device_dic['shop']})
                    self.device_dic['devices'] = de
                    self.device_dic['devices_len'] = len(de)
                else:
                    sql = 'select mac, device_type, device_ip, version, platform_id, depId, group_id from is_device_status WHERE group_id = %s AND device_type = %s'
                    self.api.con.execute(sql, (self.device_dic['enterprise_id'], device_type))
                    devices = self.api.con.fetchall()
                    de = []
                    for device in devices:
                        sql = 'select SERVER from is_platforms WHERE id = %s'
                        self.api.con.execute(sql, (device[4],))
                        dms = self.api.con.fetchone()[0]

                        sql = 'select name from is_departments WHERE id = %s'
                        self.api.con.execute(sql, (device[5],))
                        shop = self.api.con.fetchone()[0]
                        de.append({'mac': device[0], 'device_type': device[1], 'ip': device[2], 'version': device[3],
                                   'dms': dms, 'shop': shop})

                    self.device_dic['devices'] = de
                    self.device_dic['devices_len'] = len(de)
                print(self.device_dic)
                self.msg.delete(0, END)
                self.msg.insert(0, '数据已检索完成...')

                self.change_page(start_page=True)
            else:
                self.msg.delete(0, END)
                self.msg.insert(0, '未检索到该企业...')


        else:
            self.msg.delete(0, END)
            self.msg.insert(0, '企业名和设备类型必填项，请输入企业完整名称...')

    # 翻页按钮控制
    def change_page(self, start_page=None, end_page=None, last_page=None, next_page=None):
        """self.device_dic这个字典表是从数据库拉取过来的数据，在未进行搜索前调用这个会抛一个未定义异常"""
        all_page = self.device_dic['devices_len'] / 10 if self.device_dic['devices_len'] % 10 == 0 else int(
            self.device_dic['devices_len'] / 10) + 1
        print(all_page)
        if start_page:
            pass
            if self.device_dic['devices_len'] >= 10:
                self.show_list = self.device_dic['devices'][0:10]
            else:
                self.show_list = self.device_dic['devices']
            self.box_page_info.delete(0, END)
            self.box_page_info.insert(0, 1)
        elif end_page:
            if self.device_dic['devices_len'] >= 10:
                self.show_list = self.device_dic['devices'][
                                 (all_page - 1) * 10:self.device_dic['devices_len']]
                self.box_page_info.delete(0, END)
                self.box_page_info.insert(0, all_page)
            else:
                self.show_list = self.device_dic['devices']
                self.box_page_info.delete(0, END)
                self.box_page_info.insert(0, 1)
        elif last_page:
            now_page = self.box_page_info.get(0, END)[0]
            print(now_page)
            if int(now_page) != 1:
                pg = (now_page - 2) * 10
                self.show_list = self.device_dic['devices'][pg:(pg + 10)]
                self.box_page_info.delete(0, END)
                self.box_page_info.insert(0, int(now_page) - 1)


        elif next_page:
            now_page = self.box_page_info.get(0, END)[0]
            if int(now_page) != all_page:
                pg = now_page * 10
                self.show_list = self.device_dic['devices'][pg:(pg + 10)]
                self.box_page_info.delete(0, END)
                self.box_page_info.insert(0, int(now_page) + 1)
                # if self.device_dic['devices_len'] % 10 == 0:
                #     self.show_list = self.device_dic['devices'][pg:(pg + 10)]
                # else:
                #     self.show_list = self.device_dic['devices'][pg:self.device_dic['devices_len']]
        self.box_all_page_info.delete(0, END)
        self.box_all_page_info.insert(0, all_page)
        print(self.show_list)
        print(len(self.show_list))
        self._creat_table_info(self.show_list)

    # 将数据写入表格
    def _creat_table_info(self, show_list):
        if len(show_list):
            for n, item in enumerate(show_list):
                num = str(n + 1)
                self.shop_dic[num].delete(0, END)
                self.shop_dic[num].insert(0, item['shop'])

                self.mac_dic[num].delete(0, END)
                self.mac_dic[num].insert(0, item['mac'])

                self.device_name_dic[num].delete(0, END)
                self.device_name_dic[num].insert(0, item['device_type'])

                self.ip_dic[num].delete(0, END)
                self.ip_dic[num].insert(0, item['ip'])

                self.version_dic[num].delete(0, END)
                self.version_dic[num].insert(0, item['version'])

                self.dms_dic[num].delete(0, END)
                self.dms_dic[num].insert(0, item['dms'])

                self.status_dic[num].delete(0, END)
            check_num = 10 - len(show_list)
            """
            *************************************************
            这里在正常情况下正好10条数据填充慢表格是没有问题的，
            在小于10条诗句时，会执行下面的命令，将未填充的表格清空
            *************************************************
            """
            if check_num != 0:
                n = len(show_list) + 1
                for num in range(n, 11):
                    num = str(num)
                    self.shop_dic[num].delete(0, END)

                    self.mac_dic[num].delete(0, END)

                    self.device_name_dic[num].delete(0, END)

                    self.ip_dic[num].delete(0, END)

                    self.version_dic[num].delete(0, END)

                    self.dms_dic[num].delete(0, END)

                    self.status_dic[num].delete(0, END)
        else:
            for num in range(1, 11):
                num = str(num)
                self.shop_dic[num].delete(0, END)

                self.mac_dic[num].delete(0, END)

                self.device_name_dic[num].delete(0, END)

                self.ip_dic[num].delete(0, END)

                self.version_dic[num].delete(0, END)

                self.dms_dic[num].delete(0, END)

                self.status_dic[num].delete(0, END)

    """
    *************************************************
    升级和重启：
        升级首先会检查复选框的状态，获得一个check_list的列表，
    然后会遍历列表中勾选的设备信息包括dms、mac、url， 在读取到正确数据
    后，会进入一个循环升级流程。升级前会先测试DMS平台是否可连，如果正常，
    会开一个线程调用self.api.update_nvr()对该设备升级，如果检测到升级
    正常会开另一个线程调用self.api.get_device_status()来获取升级进度
    0~100。
        重启的逻辑前面和升级一样，在升级时调用的方法是
    self.api.reboot_device()，重启后不会再获取该设备的状态。
    备注：
        1.nvr在接收到型号错误的FTP包时，会升级挂掉；
        2.nvr在接收错误的URL例如'aaa.ccc.ccc'时，由于nvr未做校验，
        返回的状态是已升级成功，此时获取到的升级进度一直是0，陷入死循环
        所以在这里我把获取升级进度的线程延时了15秒，然后把0从循环状态中
        剔除。
    *************************************************
    """

    def update_button(self):
        check_list = []
        data_list = []
        self.msg.delete(0, END)
        self.msg.insert(0, '正在进行升级前的必要操作...')
        for n in range(1, 11):
            check_list.append(self.check_dic[str(n)].get())
        print(check_list)
        if self.update_url.get():
            for n, check in enumerate(check_list):
                if check == '1':
                    key = str(n + 1)
                    if self.mac_dic[key].get(0, END) and self.dms_dic[key].get(0, END):
                        data_list.append({'dms': self.dms_dic[key].get(0, END)[0].split()[0],
                                          'mac': self.mac_dic[key].get(0, END)[0].split()[0],
                                          'url': self.update_url.get().split()[0],
                                          'key': key
                                          })

            if len(data_list) > 0:
                print(data_list)
                for item in data_list:
                    time.sleep(3)
                    mac = item['mac']
                    dms = item['dms']
                    url = item['url']
                    key = item['key']
                    self.msg.delete(0, END)
                    self.msg.insert(0, f'正在连接ip为：{mac} 的平台...')
                    # if threading.Thread(target=self.api.test_dms, args=(dms, )).start():
                    if self.api.test_dms(dms=dms):
                        self.msg.delete(0, END)
                        self.msg.insert(0, f'正在升级mac地址为：{mac} 的设备...')
                        threading.Thread(target=self._creat_device, args=(mac, url, dms, key)).start()
                    else:
                        self.msg.delete(0, END)
                        self.msg.insert(0, f'连接ip为：{mac} 的平台失败，无法升级！')

            else:
                self.msg.delete(0, END)
                self.msg.insert(0, '没有获取到数据，无法进行升级操作！...')
        else:
            self.msg.delete(0, END)
            self.msg.insert(0, '请先输入升级包URL...')

    def _creat_device_status(self, mac, dms, key):
        status_msg = self.api.get_device_status(mac=mac, dms=dms)
        while status_msg:
            self.status_dic[key].delete(0, END)
            print(f'test:{status_msg}')
            self.status_dic[key].insert(0, status_msg)

    def _creat_device(self, mac, url, dms, key):
        device_msg = self.api.update_nvr(mac=mac, url=url, dms=dms)
        # device_msg = threading.Thread(target=self.api.update_nvr, args=(mac, url, dms)).start()
        print(device_msg)
        self.status_dic[key].delete(0, END)
        self.status_dic[key].insert(0, device_msg)

        self.msg.delete(0, END)
        self.msg.insert(0, f'升级mac地址为：{mac} 的设备({device_msg})')
        if device_msg in ['请求升级成功', '设备升级中']:
            threading.Thread(target=self._creat_device_status, args=(mac, dms, key)).start()
            self.msg.delete(0, END)
            self.msg.insert(0, f'mac地址为：{mac} 的设备升级正常')

    def reboot_button(self):
        check_list = []
        data_list = []
        self.msg.delete(0, END)
        self.msg.insert(0, '正在进行重启前的必要操作...')
        for n in range(1, 11):
            check_list.append(self.check_dic[str(n)].get())
        print(check_list)

        for n, check in enumerate(check_list):
            if check == '1':
                key = str(n + 1)
                if self.mac_dic[key].get(0, END) and self.dms_dic[key].get(0, END):
                    data_list.append({'dms': self.dms_dic[key].get(0, END)[0].split()[0],
                                      'mac': self.mac_dic[key].get(0, END)[0].split()[0],
                                      'key': key
                                      })
        print(data_list)
        if len(data_list) > 0:
            for item in data_list:
                mac = item['mac']
                dms = item['dms']
                key = item['key']
                self.msg.delete(0, END)
                self.msg.insert(0, f'正在连接ip为：{mac} 的平台...')
                # if threading.Thread(target=self.api.test_dms, args=(dms, )).start():
                if self.api.test_dms(dms=dms):
                    self.msg.delete(0, END)
                    self.msg.insert(0, f'正在重启mac地址为：{mac} 的设备...')
                    threading.Thread(target=self.creat_reboot_device, args=(mac, dms, key)).start()
                else:
                    self.msg.delete(0, END)
                    self.msg.insert(0, f'连接ip为：{mac} 的平台失败，无法重启！')

        else:
            self.msg.delete(0, END)
            self.msg.insert(0, '没有获取到数据，无法进行重启操作！...')

    def creat_reboot_device(self, mac, dms, key):
        device_msg = self.api.reboot_device(mac=mac, dms=dms)
        print(device_msg)
        self.status_dic[key].delete(0, END)
        self.status_dic[key].insert(0, device_msg)
        self.msg.delete(0, END)
        self.msg.insert(0, f'重启mac地址为：{mac} 的设备({device_msg})')

    # 附加功能
    def device_type_menu(self, type=''):
        self.device_type.delete(0, END)
        self.device_type.insert(0, type)


"""
---------------------------------------------------------

APPS升级PU接口

POST /upgradeDevice RS/1.0\r\n
Host: %s:%d\r\n
Content-Length: %d\r\n
Session-Id:1869617355669396668486824512\r\n
Authentication: Basic RGV2aWNlUmVnQWRtaW46RGV2aWNlUmVnQWRtaW4yMDEz\r\n
\r\n
macaddr=%s&url=%s|macaddr=%s&url=%s…|macaddr=%s&url=%s\r\n

回复

RS/1.0 %d %s\r\n
Content-Length: %d\r\n
Session-Id:%s\r\n
\r\n
macaddr=%s&devstat=%d|macaddr=%s&devstat=%d…|macaddr=%s&devstat=%d\r\n

备注：devstat取值：

*********************************************************

APPS查询PU升级状态
POST /getDeviceStatus RS/1.0\r\n
Host: %s:%d\r\n
Content-Length: %d\r\n
Session-Id:%s\r\n
Authentication: Basic %s\r\n
\r\n
macaddr=%s|macaddr=%s…|macaddr=%s\r\n
回复
RS/1.0 %d %s\r\n
Content-Length: %d\r\n
Session-Id:%s\r\n
\r\n
macaddr=%s&upgrade_status=%d|macaddr=%s&upgrade_status=%d…|macaddr=%s&upgrade_status=%d\r\n
备注：upgrade_status取值：-3（不在升级），-2（离线），-1（无效），0-100（文件下载进度百分比），200（文件校验成功，安装中）

*********************************************************

控制PU（重启，恢复出厂）
POST /ctrlDevice RS/1.0\r\n
Host: %s:%d\r\n
Content-Length: %d\r\n
Session-Id:%s\r\n
Authentication: Basic %s\r\n
\r\n
macaddr=%s&reboot=%d&restore=%d\r\n

回复
RS/1.0 %d %s\r\n
Content-Length: %d\r\n
Session-Id:%s\r\n
\r\n
macaddr=%s&reboot=%d&restore=%d\r\n

备注：请求及回复消息中的reboot和restore取值：-1（无效），0（不执行），1（执行）。
---------------------------------------------------------
"""


class DeviceApi():
    def __init__(self, host, user, passwd, db, port, timeout):
        self.dms_port = 8809
        self.bufsiz = 4096

        self.host = host
        self.user = user
        self.passwd = passwd
        self.db = db
        self.port = port
        self.timeout = timeout

        self.status_msg = ''

    def test_connect(self):
        try:
            self.conn = pymysql.connect(host=self.host, user=self.user, passwd=self.passwd, db=self.db, port=self.port,
                                        charset='utf8', connect_timeout=self.timeout)
            self.con = self.conn.cursor()
            return True
        except:
            return False

    def test_dms(self, dms=''):
        self.client = socket(AF_INET, SOCK_STREAM, 0)
        self.client.settimeout(5)
        try:
            print(f'now connect {dms}:{self.dms_port}')
            self.client.connect((dms, self.dms_port))
            print('connect dms success')
            return True
        except Exception as e:
            print(str(e))
            return False

    """
    *****************************************************************************
        所有的发消息方法在执行完成后都必须要关掉和服务器的连接，
    否则会引起socket连接异常。
    *****************************************************************************
    """

    def update_nvr(self, mac='', url='', dms=''):

        mac_info = f'macaddr={mac}&url={url}'
        post = 'POST /upgradeDevice RS/1.0\r\n'
        host = f'Host: {dms}:{self.dms_port}\r\n'
        content = f'Content-Length: {len(mac_info)}\r\n'
        session = 'Session-Id:1869617355669396668486824512\r\n'
        authen = 'Authentication: Basic RGV2aWNlUmVnQWRtaW46RGV2aWNlUmVnQWRtaW4yMDEz\r\n'
        enter = '\r\n'
        data = ''.join([post, host, content, session, authen, enter, mac_info, enter])
        print(data)
        try:
            self.client.send(data.encode('utf8'))
            recv_data = self.client.recv(self.bufsiz)
            recv = recv_data.decode()
            print(recv)
            self.client.close()
            key = recv.split()[-1].split('devstat=')[-1]

            msg = {'-2': '离线', '-1': '无效', '1': '请求升级成功', '2': '设备升级中'}
            return msg.get(key, '错误！')
        except Exception as e:
            print(str(e))
            self.client.close()
            return False

    def get_device_status(self, mac='', dms=''):
        mac_info = f'macaddr={mac}'
        post = 'POST /getDeviceStatus RS/1.0\r\n'
        host = f'Host: {dms}:{self.dms_port}\r\n'
        content = f'Content-Length: {len(mac_info)}\r\n'
        session = 'Session-Id:1869617355669396668486824512\r\n'
        authen = 'Authentication: Basic RGV2aWNlUmVnQWRtaW46RGV2aWNlUmVnQWRtaW4yMDEz\r\n'
        enter = '\r\n'
        data = ''.join([post, host, content, session, authen, enter, mac_info, enter])
        client = socket(AF_INET, SOCK_STREAM, 0)
        client.settimeout(5)
        client.connect((dms, self.dms_port))
        while True:
            time.sleep(15)
            client.send(data.encode('utf8'))
            recv_data = client.recv(self.bufsiz)
            recv = recv_data.decode()
            print(recv)
            self.client.close()
            key = recv.split()[-1].split('status=')[-1]
            status_msg = {'-3': '不在升级', '-1': '无效', '-2': '离线', '200': '文件校验成功，安装中'}
            if key in ['-3', '-1', '-2', '0']:
                client.close()
                break
            self.status_msg = status_msg.get(key, key)
            return status_msg.get(key, key)

    def reboot_device(self, dms='', mac=''):
        mac_info = f'macaddr={mac}&reboot=1'
        post = 'POST /ctrlDevice RS/1.0\r\n'
        host = f'Host: {dms}:{self.dms_port}\r\n'
        content = f'Content-Length: {len(mac_info)}\r\n'
        session = 'Session-Id:1869617355669396668486824512\r\n'
        authen = 'Authentication: Basic RGV2aWNlUmVnQWRtaW46RGV2aWNlUmVnQWRtaW4yMDEz\r\n'
        enter = '\r\n'
        data = ''.join([post, host, content, session, authen, enter, mac_info, enter])
        print(data)
        try:
            self.client.send(data.encode('utf8'))
            recv_data = self.client.recv(self.bufsiz)
            recv = recv_data.decode()
            print(recv)
            self.client.close()
            key = recv.split()[-1].split('&')[1].split('reboot=')[-1]

            msg = {'-1': '无效', '0': '不执行', '1': '已重启'}
            return msg.get(key, '错误！')
        except Exception as e:
            print(str(e))
            self.client.close()
            return False


if __name__ == '__main__':
    win = Windows()
