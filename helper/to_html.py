"""
CREAT: 2017/8/7
AUTHOR:　HEHAHUTU
"""


def create_html(data, file_type):
    ch = {
        '.py': type_py,
        '.txt': type_txt,
        '.json': type_py,
        '.csv': type_py
    }
    get_type = ch.get(file_type)
    if get_type:
        return get_type(data)
    else:
        return data


# py
def type_py(data):
    data = data.split('\n')
    add_p = []
    for da in data:
        add_p.append(f'<p>{da}</p>')
    das = ''.join(add_p).replace('\b', '&nbsp;').replace('\t', '&nbsp;' * 4).replace('\0', '&nbsp;')
    add_code = f'<pre><code>{das}</code></pre>'
    return add_code


# txt
def type_txt(data):
    data = data.split('\n')
    add_p = []
    for da in data:
        add_p.append(f'<p>{da}</p>')
    das = ''.join(add_p).replace('\b', '&nbsp;').replace('\t', '&nbsp;' * 4)
    add_code = f'<pre>{das}</pre>'
    return add_code


