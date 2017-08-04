"""
CREAt: 2017/3/23
AUTHOR: Hehahutu
"""
from test_scripts.page_object import Page
# from test_scripts.login_object import Login
from selenium.webdriver.common.by import By
import time


class ChangePwd(Page):
    username_loc = (By.ID, 'username')
    password_loc = (By.ID, 'password')
    login_btn_loc = (By.CLASS_NAME, 'login-btn')

    nav_btn_loc = (By.XPATH, '//*[@id="top"]/div[2]/span[1]')
    changepwd_btn_loc = (By.XPATH, '//*[@id="top"]/div[2]/div/ul/li[2]/label')
    oldpwd_input_loc = (By.XPATH, '//*[@id="changePwdDlg"]/table/tbody/tr[1]/td[2]/input')
    newpwd_input_loc = (By.XPATH, '//*[@id="changePwdDlg"]/table/tbody/tr[2]/td[2]/input')
    renewpwd_input_loc = (By.XPATH, '//*[@id="changePwdDlg"]/table/tbody/tr[3]/td[2]/input')
    submit_loc = (By.XPATH, '//*[@id="okBtn"]')

    def type_username(self):
        self.find_element(*self.username_loc).clear()
        self.find_element(*self.username_loc).send_keys(self.username)

    def type_password(self):
        self.find_element(*self.password_loc).send_keys(self.password)

    def login_submit(self):
        self.find_element(*self.login_btn_loc).click()
        time.sleep(2)

    def type_navbtn(self):
        self.find_element(*self.nav_btn_loc).click()

    def type_changepwd_btn(self):
        self.find_element(*self.changepwd_btn_loc).click()
        time.sleep(1)

    def type_oldpwd_input(self):
        self.find_element(*self.oldpwd_input_loc).send_keys(self.password)

    def type_newpwd_input(self):
        self.find_element(*self.newpwd_input_loc).send_keys(self.password)

    def type_renewpwd_input(self):
        self.find_element(*self.renewpwd_input_loc).send_keys(self.password)

    def type_submit(self):
        self.find_element(*self.submit_loc).click()
        time.sleep(6)

    def test_change_pwd(self):
        self.open_url()

        self.type_username()
        self.type_password()
        self.login_submit()
        time.sleep(2)
        self.type_navbtn()
        self.type_changepwd_btn()
        self.type_oldpwd_input()
        self.type_newpwd_input()
        self.type_renewpwd_input()
        self.type_submit()

        self.type_username()
        self.type_password()
        self.login_submit()
        time.sleep(2)
