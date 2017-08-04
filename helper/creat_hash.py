"""
CREAT: 2017/5/7
AUTHOR:　HEHAHUTU
"""
import hashlib


def creat_hash(data):
    ha = hashlib.md5(b'8sb02ab3@(&r&(s(%$$#!$%a$&~!@#fs68s$%*(^%<24546782376>?@^&*')
    ha.update(data.encode('utf8'))
    return ha.hexdigest()
