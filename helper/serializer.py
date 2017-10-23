"""
CREAT: 2017/10/23
AUTHOR:　HEHAHUTU
"""
from itsdangerous import URLSafeSerializer
from config import SECRET_KEY


def dumps_data(data):
    s = URLSafeSerializer(SECRET_KEY)
    return s.dumps(data)


def loads_data(data):
    s = URLSafeSerializer(SECRET_KEY)
    return s.loads(data)
