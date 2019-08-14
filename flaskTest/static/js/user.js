/*
 * @Description: In User Settings Edit
 * @Author: your name
 * @Date: 2019-08-10 14:36:14
 * @LastEditTime: 2019-08-14 20:05:30
 * @LastEditors: Please set LastEditors
 */
var image = '';

/**
 * @description: 预览选定的图片
 * @param {type} 
 * @return: 
 */
function showPreview(source, imgId) {
    var file = source.files[0];
    if (window.FileReader) {
        var fr = new FileReader();
        fr.onloadend = function (e) {
            image = e.target.result;
            document.getElementById(imgId).src = e.target.result;
            // document.getElementById("result_image").src = e.target.result;
        }
        fr.readAsDataURL(file);
    }
}

/**
 * @description: 上传图片，接收处理的图片，并显示
 * @param {type} 
 * @return: 
 */
function upload_image() {
    if(document.getElementById("inputs").files[0] == null)
        alert('你还没选图片');
    var fd = new FormData();
    fd.append("pic", document.getElementById("inputs").files[0]);
    $.ajax({
        url: "uploadImage",
        type: "post",
        data: fd,
        processData: false,
        contentType: false,
        success: function (res) {
            $('#result_image').attr("src", res.url);
        },
        error: function (err) {
            alert('网络故障')
        },
        dataType: "json"
    })

}

/**
 * @description: 注销+页面跳转
 * @param {type} 
 * @return: 
 */
var logout = function () {
    $.ajax({
        url: "logout",
        type: "get",
        success: function (res) {
            window.location.href = '/login'
        },
        error:function(err){
            window.location.href = '/login'
        }
    })
}