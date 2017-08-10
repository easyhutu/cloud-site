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

        '.audio': type_audio,

        '.image': type_image,

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
    # return f'<audio id="player" type="audio/mp3" src="{data}"controls></audio>'
    return audio_html


# image <img src="" alt="">
def type_image(data):
    return f'<article><img src="{data}" alt="image" style="max-height: 100%; max-width: 100%"></article>'


audio_html = """
<input type="hidden" id="songs">
<div class="audio-box">
		<div class="audio-container">
			<div class="audio-view">
				<div class="audio-cover" ></div>
				<div class="audio-body">
					<h3 class="audio-title">未知歌曲</h3>
					<div class="audio-backs">
						<div class="audio-this-time">00:00</div>
						<div class="audio-count-time">00:00</div>
						<div class="audio-setbacks">
							<i class="audio-this-setbacks">
								<span class="audio-backs-btn"></span>
							</i>
							<span class="audio-cache-setbacks">
							</span>
						</div>
					</div>
				</div>
				<div class="audio-btn">
					<div class="audio-select">
						<div class="audio-prev"></div>
						<div class="audio-play"></div>
						<div class="audio-next"></div>
						<div class="audio-menu"></div>
						<div class="audio-volume"></div>
					</div>
					<div class="audio-set-volume">
						<div class="volume-box">
							<i><span></span></i>
						</div>
					</div>
					<div class="audio-list">
						<div class="audio-list-head">
							<p>歌单</p>
							<span class="menu-close">关闭</span>
						</div>
						<ul class="audio-inline">
						</ul>
					</div>
				</div>
			</div>
		</div>
	</div>
"""
