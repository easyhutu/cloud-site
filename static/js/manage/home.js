/**
 * Created by Administrator on 2017/5/13.
 */
$(document).ready(function () {
    getList();


    $('#modal-del').click(function () {
        var data = $('#modal-val').val();
        // console.log(data);
        $.ajax({
            url: '/disk/delete/',
            method: 'POST',
            data: {key: data},
            datatype: 'json',
            error: function () {
                alert('服务器错误！');
            },
            success: function (resp) {
                if (resp.status == 'ok') {
                    getList();
                    getSize();
                    $('#modal').modal('hide');
                    $('#modal-msg').html('');
                    $('#modal-del').attr('style', 'display: none');
                } else {
                    alert(resp.msg);
                }
            }
        });
    });


    //maxFileSize 文件大小单位k
    $('#upload-file').fileinput({
        uploadUrl: '/disk/upload/',
        uploadExtraData: function (previewId, index) {
            var data = {path: $('#diskPath').val()};
            return data;
        },
        allowedFileExtensions: ["txt", "rar", "py", "json", "pdf", "xml", "csv", "xlsx", "xls", "log", "mp4", "rmvb", "png", "jpg", "pptx", "zip", "tar", "mp3", "mp4", "docx", "exe", "mm", "xmind"],
        theme: "explorer",
        language: "zh",
        maxNumberOfFiles: 2,
        maxFileSize: 100 * 1024,
        showUpload: true,
        maxFileCount: 10,
        showPreview: true,
        allowedPreviewTypes: ['image', 'video', 'audio'],
        overwriteInitial: false,
        initialPreviewAsData: true,
        success: function (fileInfo) {
            $('#upload-msg').html('操作状态：' + fileInfo.data);
        }
    });
    $('#upload-file').on('fileuploaded', function (event, data) {
        var response = data.response;
        //console.log(response);
        getSize();
        $('#upload-msg').html('操作状态：' + response.msg);
        getList();
    });
    $('.upload-btn').click(function () {
        var path = $('#diskPath').val();
        $('#upload-msg').html('提示 文件将上传至：' + path);
        $('#upload-modal').modal();
    });
});
function checkall() {
    var check = document.getElementsByName('check-addr');
    var allcheck = document.getElementById('check-box').checked;
    for (var i = 0; i < check.length; i++) {
        check[i].checked = allcheck
    }
}

function createFolder() {
    var path = $('#diskPath').val();
    $('#modal-msg').html('');
    $('#submit-btn').attr('style', 'display: block;');
    $('#submit-btn').attr('onclick', 'submitCreateFolder()');
    $('#modal-input').html('<div><label class="col-lg-10" for="folder_name">将新建在：' + path + '</label><input id="folder_name" class="form-group col-lg-6 col-sm-5" type="text"></div>');
    $('#modal-del').attr('style', 'display: none');
    $('#modal').modal();
}
function submitCreateFolder() {
    var folder = $('#folder_name').val();
    var path = $('#diskPath').val();
    if (folder == null) {
        $('#modal-msg').html('请输入文件名！')
    } else {
        if (folder.length > 20) {
            $('#modal-msg').html('您输入的文件名过长！')
        } else {
            if (folder.length < 1) {
                $('#modal-msg').html('您输入的文件名过短！')
            } else {
                $.ajax({
                    url: '/disk/createFolder/',
                    method: 'POST',
                    data: {folder: folder, path: path},
                    datatype: 'json',
                    error: function () {
                        $('#modal-msg').html('服务器异常！')
                    },
                    success: function (resp) {
                        if (resp.status == 'ok') {
                            $('#modal').modal('hide');
                            $('#submit-btn').attr('style', 'display: none;');
                            getList();
                        } else {
                            $('#modal-msg').html(resp.msg);
                        }

                    }
                });
            }

        }
    }
}

// 获取容量
function getSize() {
    $.ajax({
        url: '/disk/json/diskSize/',
        datatype: 'json',
        success: function (resp) {
            var da = '容量：' + resp.use + '/' + resp.all + 'M';
            $('#diskSize').html(da);
        }
    });

}

function getList(key) {
    var path = $('#diskPath').val();
    var folder = $('#folder-key' + key).val();

    if (path == null) {
        var pa = null;
    } else {
        if (folder == null) {
            var pa = '?diskPath=' + path;
        } else {
            var pa = '?diskPath=' + path + '/' + folder;
        }
    }
    requestData(pa);

}
function navGetList(key) {
    var path = '?diskPath=' + $('#this' + key).val();
    //console.log(path);
    if (path == null) {
        getList()
    } else {
        requestData(path)
    }
}
function requestData(pa) {
    $.ajax({
        url: '/disk/json/path/' + pa,
        datatype: 'json',
        error: function () {
            window.location.href = '/404/';
        },
        success: function (resp) {
            if (resp.status == 'ok') {
                $('#diskList').html('');
                $('#path').html('');
                $('#path').append('<li></li>');
                $('#diskPath').val(resp.now_path);
                var path = resp.path;
                var folders = resp.folders;
                var files = resp.file;
                for (var i = 0; i < path.length; i++) {
                    var fo = resp.path[i];
                    var this_path = '';
                    for (var n = 0; n <= i; n++) {
                        this_path = this_path + '/' + resp.path[n];
                    }
                    //console.log(this_path);
                    $('#path').append('<li><a style="cursor: pointer" onclick="navGetList(' + i + ')">' + fo + '<input type="hidden" id="this' + i + '" value="' + this_path + '"></li>');
                }

                if (folders.length > 0) {
                    for (var i = 0; i < folders.length; i++) {
                        var data = resp.folders[i];

                        $('#diskList').append('<tr class="folder-ch" ><th><input name="check-addr" value=folder."' + data.id + '"  type="checkbox"><input class="check' + i + '" data-toggle="folder.' + data.id + '" type="hidden" id="folder-key' + data.id + '" value="' + data.foldername + '"><a class="folder-ch" style="cursor: pointer; color: #5bc0de;" onclick="getList(' + data.id + ')">&nbsp;&nbsp;<i class="iconfont icon-wenjianjia1"></i>' + data.foldername + '</a></th><th class=""><i title="下载" style="color: #5bc0de; " data-toggle="folder.' + data.id + '" class="download-ch iconfont icon-xiazai"></i>&nbsp;<i title="删除" style="color: #5bc0de;" data-template="' + data.foldername + '" data-toggle="folder.' + data.id + '" class="del-ch iconfont icon-shanchu"></i>&nbsp;<i title="分享" style="color: #5bc0de;" data-toggle="folder.' + data.id + '" class="share-ch iconfont icon-fenxiang1"></i>-</th><th class="hidden-xs hidden-sm"> ' + data.update_time + '</th></tr>');
                    }
                }
                if (files.length > 0) {
                    for (var i = 0; i < files.length; i++) {
                        var data = resp.file[i];
                        var flen = folders.length + i;
                        $('#diskList').append('<tr><th><input name="check-addr" value="file.' + data.id + '" type="checkbox"><input class="check' + flen + '" data-toggle="file.' + data.id + '" type="hidden" id="file-key' + data.id + '" value="' + data.id + '"><span style="cursor: pointer">&nbsp;&nbsp;<i class="iconfont icon-wenjian"></i>' + data.showname + '</span></th><th class=""><i title="下载" data-toggle="file.' + data.id + '" style="color: #5bc0de; display: " class="download-ch iconfont icon-xiazai"></i>&nbsp;<i title="删除" style="color: #5bc0de;" data-toggle="file.' + data.id + '" data-template="' + data.showname + '"  class="del-ch iconfont icon-shanchu"></i>&nbsp;<i title="分享" style="color: #5bc0de;" data-toggle="file.' + data.id + '" class="share-ch iconfont icon-fenxiang1"></i>' + data.file_size + '</th><th class="hidden-xs hidden-sm">' + data.update_time + '</th></tr>');
                    }
                }
                $('.download-ch').click(function () {
                    var da = $(this).attr('data-toggle');
                    $.ajax({
                        url: '/disk/download/',
                        datatype: 'json',
                        data: {data: da},
                        error: function () {
                            $('#modal-msg').html('服务器错误！');
                            $('#modal').modal()
                        },
                        success: function (resp) {
                            if (resp.status == 'ok') {
                                //console.log(resp.path);
                                $(document.body).append('<iframe src="/disk/responseFile/?key=' + resp.folder + '&filename=' + resp.filename + '" frameborder="0"></iframe>');
                                $('#downloads').submit();
                            } else {
                                $('#modal-msg').html('糟糕，下载异常：' + resp.msg);
                                $('#modal').modal();

                            }
                        }
                    });
                });

                $('.del-ch').click(function () {
                    var data = $(this).attr('data-toggle');
                    var name = $(this).attr('data-template');
                    $('#modal-input').html('');
                    $('#modal-msg').html('确认删除文件（目录）:' + name + '？');
                    $('#modal-val').val(data);
                    $('#modal-del').attr('style', 'display: block');
                    $('#modal').modal();
                });
                $('.share-ch').click(function () {
                    var data = $(this).attr('data-toggle');
                    $.ajax({
                        url: '/disk/createShareUrl/?key=' + data,
                        method: 'get',
                        datatype: 'json',
                        error: function () {

                        },
                        success: function (resp) {
                            if (resp.status == 'ok') {
                                $('#share-msg').html('该链接默认有效期为90天,您也可以随时在设置中关闭所有分享：<br>&nbsp;<input type="text" id="shareUrl" value="http://yuncluod.com:8000/disk/share/' + resp.msg + '/" > <button class="btn btn-xs bg-success" data-clipboard-target="#shareUrl"><i class="fa fa-copy"></i></button>');
                                $('#share-submit').attr('disabled', 'disabled');

                            } else {
                                $('#share-msg').html('<h4>点击确定即可创建分享链接</h4>');
                                $('#share-val').val(data);
                                $('#share-submit').removeAttr('disabled');
                            }

                        }
                    });
                    $('#share-msg').html('');
                    $('#share-modal').modal();
                });


            } else {
                $('#diskList').html(resp.msg);
            }
        }
    });
}