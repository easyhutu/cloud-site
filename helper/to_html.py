"""
CREAT: 2017/8/7
AUTHOR:　HEHAHUTU
"""


def create_html(data, file_type):
    ch = {
        '.py': type_py,
        '.txt': type_txt,
        '.json': type_py,
        '.csv': type_py,
        '.mp3': type_audio,
        '.jpg': type_image,
        '.png': type_image,
        '.gif': type_image,
        '.bmp': type_image
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
    das = ''.join(add_p).replace('\b', '&nbsp;').replace('\r', '<br>')
    add_code = f'<article>{das}</article>'
    return add_code


# audio <audio src="/mp3/juicy.mp3" preload="auto" />
def type_audio(data):
    # return f'<audio src="{data}" preload="auto">mp3</audio>'
    return f'<audio id="player" src="{data}" type="audio/mp3" controls></audio>'


# image <img src="" alt="">
def type_image(data):
    return f'<article><img src="{data}" alt="image" style="max-height: 100%; max-width: 100%"></article>'
