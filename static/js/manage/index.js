/**
 * Created by Administrator on 2017/5/6.
 */
/**
 * Created by sheyude on 2017/5/3.
 * 本模版由舍与得贡献，在此感谢！
 */
// 登陆界面
$(document).ready(function () {
    getSize();
    var li = $(".login-img li");
    // $(li[2]).animate({"opacity": "1"}, 2000);
    var sum = 1;
    var liTime = null;
    var imgTime = null;
    $(li).css({"opacity": "1"});
    $(li[1]).animate({"opacity": "1"}, 1000);

});
// 后台界面
$(document).ready(function () {
    // 后台左边栏
    var list = $("#left-list>li>a");
    list.click(function () {
        var on = $(this).attr("on");
        var ul = $(this).next();
        var li = ul.find("li");
        var height = li.length * li.height();
        //console.log(on);
        if (on == 0 || on == undefined) {
            ul.animate({"height": height + "px"});
            $(this).attr("on", "1").css({"color": "#fff"});
            $(this).find("i").css("color", "#f74e4d")
        } else if (on == 1) {
            ul.animate({"height": 0});
            $(this).attr("on", "0").removeAttr("style");
            $(this).find("i").removeAttr("style");
        }
        return false;
    })

    // 算右边高度
    onsize();
    window.onresize = function () {
        onsize();

    }
    function onsize() {
        var clientHeight = document.body.clientHeight;
        var contentHeight = clientHeight - 65;
        var listHeight = contentHeight - 150;
        $("#content").css({"height": contentHeight + "px", "overflow": "hidden"});
        $("#listHeight").css({"height": listHeight + "px", "overflow": "auto"});
    }


    // 搜索
    // $(".search").focus(function () {
    //     $(this).animate({"width": "140px"}).removeAttr("placeholder");
    // })
    // $(".search").blur(function () {
    //     $(this).animate({"width": "100px"}).attr("placeholder", "输入关键字");
    // });


    // 小屏面包屑
    var $left = $(".left");
    $("#sm-bar").click(function () {
        $("#left-hiden").show(300);
        $left.animate({"width": "100px", "display": "block"}).attr("smon", "1");
        // 修复bug
        $(".left-bar").show(300);

    })
    // 侧边栏按钮
    $("#left-bar").click(function () {
        if ($left.attr("smon") == undefined && ($left.attr("on") == 1 || $left.attr("on") == undefined)) {
            $("#left-hiden").hide();
            $left.animate({"width": "0",}).attr("on", "0");
            $(".right").animate({"margin-left": "10px"});

            $("#left-bar").html("<i class='fa fa-hand-o-right' title='显示'></i>");

        } else if ($left.attr("on") == 0) {
            $left.animate({"width": "100px"}).attr("on", "1");
            $(".right").animate({"margin-left": "100px"});
            $("#left-hiden").show(300);

            $("#left-bar").html("<i class='fa fa-hand-o-left' title='隐藏'></i>");
        }
        // 小屏
        if ($left.attr("on") == undefined && ($left.attr("smon") == 1 || $left.attr("smon") == undefined)) {
            $("#left-hiden").hide();
            $left.animate({"width": "0",}).attr("smon", "0");
            $("#left-bar").html("<i class='iconfont' title='显示'>&#xe61e;</i>");
        } else if ($left.attr("smon") == 0) {
            $left.animate({"width": "100px"}).attr("smon", "1");
            $("#left-hiden").show(300);
            $("#left-bar").html("<i class='iconfont' title='隐藏'>&#xe612;</i>");
        }
    })
});

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
