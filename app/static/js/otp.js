    $(".otp").click(() => {
        console.log("hi")
        $.ajax({
            type: "POST",
            url: "/otp",
            data: {
                email: $(".email").val(),
                username: $("#username").val()
            },
            success: function(data) {
                console.log(data)
                if (data.user == false) {
                    $(".label-otp").text(data.error)
                } else {
                    $(".label-otp").attr("class", " text-center text-success mx-2 label-otp")
                    $(".label-otp").text(data)
                    count()
                }
            },
            error: function(req, err, errth) {
                if (err) {
                    console.log(req, err, errth)
                    $(".card").prepend(`<div class="alert alert-warning alert-dismissible" role="alert" >
                    An error occured while sending otp. Please try again!!
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                    </div>`)
                    $(".label-otp").attr("class", "text-danger mx-2 label-otp")
                    $(".label-otp").text('Error!!')
                }
            }
        })
    });

    function count() {
        $(".otp-countdown").removeClass("d-none")
        expire_time.innerText = "5 : 00"
        var count = new Date("Jan 5, 2022 15:50:25").getTime();
        var countDownDate = new Date("Jan 5, 2022 15:45:25").getTime();
        var x = setInterval(function() {
            console.log(count, countDownDate)
            countDownDate += 1000
            var distance = count - countDownDate
            var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
            var seconds = Math.floor((distance % (1000 * 60)) / 1000);
            expire_time.innerText = minutes + " : " + seconds
            if (distance < 0) {
                clearInterval(x)
                expire_time.innerText = "expired"
            }
        }, 1000);
    }