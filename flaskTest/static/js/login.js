/*
 * @Description: 登录页js
 * @Author:lkb
 * @Date: 2019-08-09 17:37:03
 * @LastEditTime: 2019-08-14 19:57:44
 * @LastEditors: Please set LastEditors
 */

/**
 * @description: 判断全填写以及查询数据库是否匹配
 * @param {type} 
 * @return: 
 */ 
var login2 = function () {
    var username = document.getElementById("username");
    var pass = document.getElementById("password");
    if (username.value == "") {

        alert("请输入用户名");

    } else if (pass.value == "") {

        alert("请输入密码");

    } else {
        var data = {
            'username': username.value,
            'password': pass.value
        }
        $.post("/loginForm", data, function (result) {
            var key = "wrong";
            console.log(result[key]);

            if (result["wrong"]) {
                //window.location.href(result.url);
                alert("无此用户或密码错误");
            } else {
                window.location.href = "/user";
            }

        }, dataType = "json");
    }
}

function gotoRegist() {
    window.location.href = '/regist';
}

function gotoForget(){
    window.location.href = '/forgetPass'
}

// $( "#btn_login" ).on( "click", login2()); 

//document.getElementById('btn_login').onclick = login2();

// $("#btn_login").bind(onclick = login2(); 
//document.getElementById("btn_login").onclick = login2();