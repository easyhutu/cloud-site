"""
CREAT: 2017/4/17
AUTHOR:　HEHAHUTU
"""
import requests
import time
import json
import os, shutil
from datetime import datetime


class GetCar():
    def __init__(self, appkey='你申请的appkey', save_num=100):
        self.url = 'http://api.jisuapi.com/car/brand?appkey='
        self.appkey = appkey
        self.save_num = save_num
        self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
                        'Cookie':'PHPSESSID=ed6le4ht8slq5hnm4atbrooag7; Hm_lvt_ff3b9dbe7bb4e4ec2cbf96a59930e5d0=1492432481; Hm_lpvt_ff3b9dbe7bb4e4ec2cbf96a59930e5d0=1492432798'
                        }
        if os.path.exists('car_img'):
            shutil.rmtree('car_img')
            os.mkdir('car_img')
        else:
            os.mkdir('car_img')

    def _get_car_url(self):
        html = requests.get(self.url + self.appkey)
        data = json.loads(html.content.decode())
        if data['status'] == "0":
            val = data['result']
            # print(val, len(data['result']))
            return {'val': val, 'len': len(val)}
        else:
            print('数据获取错误，错误信息：' + data['msg'])
            return None

    def save_car_logo(self):
        car_list = self._get_car_url()
        if car_list:
            num = self.save_num if self.save_num <= car_list['len'] else car_list['len']
            for i, car in enumerate(car_list['val'][0: num]):
                url = car['logo']
                data = requests.get(url, headers=self.headers, timeout=11)
                filename = car['name'] + '_' + str(time.time()).replace('.', '')
                time.sleep(1)
                if data.status_code == 200:
                    with open(f'car_img/{filename}.png', 'wb') as f:
                        f.write(data.content)
                    print(f'第{str(i+1)}图片:{filename}.png保存成功 url: {url}')


if __name__ == '__main__':
    car = GetCar()
    car.save_car_logo()