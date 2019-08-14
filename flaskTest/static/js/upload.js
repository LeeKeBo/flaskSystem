var image = '';

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

function upload_image() {
    var fd = new FormData();
    fd.append("pic", document.getElementById("inputs").files[0]);
    $.ajax({
        url: "uploadImage",
        type: "post",
        data: fd,
        processData: false,
        contentType: false,
        success: function (res) {
            $('#result_image').attr("src",res.url);
        },
        error:function(err){
            alert('网络故障')
        },
        dataType: "json"
    })

}