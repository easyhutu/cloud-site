"""
CREAT: 2017/7/18
AUTHOR:　HEHAHUTU
"""
import time
import sys
import threading


def cons():
    mem_len = get_arg()
    if mem_len:
        while True:
            a = 'a'*1024*1024*mem_len
    else:
        while True:
            time.sleep(2)
            try:
                threading.Thread(target=run_te).start()
            except:
                print('use over!')
                break


def get_arg():
    arg = sys.argv
    if str(arg[-1]).isdecimal():
        return int(arg[-1])
    else:
        return False


def run_te():
    while True:
        a = 'a' * 1024 * 1024 * 10
        print('use 10M')


if __name__ == '__main__':
    cons()
