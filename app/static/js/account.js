$(document).ready(function() {
        $(".email_change").hide()
        $(".update-info").hide()

    $("img").click(() => {
        $("input[type=file]").click()
    })
    $("input[type=file]").on("change", (e) => {
        console.log("hi")
        console.log(e)
        if (e.target.files) {
            console.log("hsd")
            var img = document.getElementById("myImage");
            img.onload = () => {
                URL.revokeObjectURL(img.src);
            }
            img.src = URL.createObjectURL(e.target.files[0]);
        }
    })

    $(".delete").click(() => {
        console.log("hi112")
        $.ajax({
            type: "POST",
            url: "/otp",
            data: {},
            success: function(data) {
                var myModal = new bootstrap.Modal(document.getElementById('myModal'))
                myModal.show()
            },
            error: function(req, err, errth) {
                if (err) {
                    console.log(req, err, errth)
                    $(".card").prepend(`<div class="alert alert-warning alert-dismissible" role="alert" >
  An error occured while sending otp. Please try again!!
  <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
</div>`)
                }
            }
        })
    })
    $("#delete-otp-btn").click(()=>{
    $.ajax({
        type: "POST",
        url: "/delete_account",
        data: {
            otp:$("#delete-otp").val()
        },
        success: function(res) {
            console.log(res)
            if (res == "Invalid OTP"){
                $(".error").text(`Invalid OTP!!`)
            }
            else{
                document.location.replace("/signin")
            }
        },
    });
    })


})