"""
CREAT: 2017/5/6
AUTHOR:　HEHAHUTU
"""
from flask import Blueprint

manage = Blueprint('manage', __name__)

from manage.views import *

manage.add_url_rule('/home/', view_func=IndexPage.as_view('home'))
manage.add_url_rule('/json/path/', view_func=GetFiles.as_view('path'))
manage.add_url_rule('/json/diskSize/', view_func=GetUseSize.as_view('diskSize'))
manage.add_url_rule('/createFolder/', view_func=CreateFolder.as_view('createFolder'))
manage.add_url_rule('/upload/', view_func=UploadFiles.as_view('upload'))
manage.add_url_rule('/download/', view_func=Download.as_view('download'))
manage.add_url_rule('/responseFile/', view_func=ResponseFile.as_view('responseFile'))
manage.add_url_rule('/delete/', view_func=DeleteFile.as_view('delete'))
manage.add_url_rule('/createShareUrl/', view_func=CreateShareUlr.as_view('createShareUrl'))
manage.add_url_rule('/share/<key>/', view_func=Share.as_view('share'))
manage.add_url_rule('/shareDownload/<key>/', view_func=ShareDownload.as_view('shareDownload'))
manage.add_url_rule('/trash/', view_func=Trash.as_view('trash'))
manage.add_url_rule('/recoverFile/', view_func=RecoverFile.as_view('recoverFile'))
manage.add_url_rule('/dropFile/', view_func=DropFile.as_view('dropFile'))
manage.add_url_rule('/group/', view_func=GroupFolder.as_view('group'))
manage.add_url_rule('/addGroup/', view_func=AddGroup.as_view('addGroup'))
manage.add_url_rule('/delGroup/', view_func=DelGroup.as_view('delGroup'))
manage.add_url_rule('/groupDownload/', view_func=GroupDownload.as_view('groupDownload'))
manage.add_url_rule('/clearShare/', view_func=ClearShare.as_view('clearShare'))