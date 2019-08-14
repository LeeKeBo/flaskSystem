function regist() {
    // var role_id = $('#role_id').val().trim(),
    var username = $('#username').val().trim(),
        pass1 = $("#password").val().trim(),
        pass2 = $('#check_password').val().trim();
    var allHaveInput = true;

    // if (role_id.length === 0) {
    //     $("#role_id").attr('placeholder', "这里还没有输入")
    //     allHaveInput = false;
    // }
    if (username.length === 0) {
        $("#username").attr('placeholder', "这里还没有输入")
        allHaveInput = false;
    }
    if (pass1.length < 6) {
        $("#password").val("");
        $("#password").attr('placeholder', "密码长度需大于等于6位")
        allHaveInput = false;
    }
    if (pass2.length === 0) {
        $("#check_password").attr('placeholder', "这里还没有输入")
        allHaveInput = false;
    }

    if (allHaveInput) {

        if (pass1 !== pass2) {
            alert('密码不一致')
            $('#check_password').val("");
        } else {
            var dataToSend = {"username":username,"password":pass1};
            $.ajax({
                url: "registForm",
                type: "post",
                data: dataToSend,
                success: function (res) {
                   if(res.success){
                        if(!res.error){
                            alert("注册成功，点击确定返回登录页面");
                            window.location.href = "login";
                        }else{
                            alert('注册失败');
                        }
                   }
                   else{
                    //    alert('error')
                    $('#username').val(""); 
                       $("#username").attr('placeholder','已有同名用户');
                   }
                },
                error:function(err){
                    alert('网络故障')
                },
                dataType: "json"
            })
        }
    }

}

function gotoLogin() {
    window.location.href = '/login'
}