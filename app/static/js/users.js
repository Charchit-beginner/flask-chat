$(document).ready(function() {
    socket = io.connect(document.href);
    // last message shower
    socket.on("msg", data => {
        console.log(data)
        let unseen_msg_no = $(`a[href="/chat/${data.user}"]`).find("span.unseen")[0]
        let hasNumber = /\d/;
        if (data.rec_user == current_user.value) {
            $(`a[href="/chat/${data.user}"]`).find("span.span").text(data.msg)
            if (!hasNumber.test($("title")[0].innerText)){
                $("title").text("(1) ChatApp")
            }
            else{
                $("title").text(`(${parseInt($("title")[0].innerText.slice(1,2)) + 1}) ChatApp`)   
            }
            if (!hasNumber.test(unseen_msg_no.innerText)) {
                console.log("hi")
                unseen_msg_no.innerText = "1"
                $(unseen_msg_no).show()
            } else {
                console.log("bye")
                unseen_msg_no.innerText = parseInt(unseen_msg_no.innerText) + 1
            }
        } else {
            console.log("sfs")
            $(`a[href="/chat/${data.rec_user}"]`).find("span.span").text(`You: ${data.msg}`)
        }
    })
                socket.on("disconnect", (reason) => {
         $(".container").prepend(`<div class="alert  alert-success alert-dismissible fade show" role="alert" style="position:fixed; width:${$(".container").width()}px; z-index:11;">
           You have disconnected from the server. Reconnecting...
    <button aria-label="Close" class="btn-close" data-bs-dismiss="alert" type="button">
    </button>
</div>`)
        });
        socket.io.on("reconnect", () => {
           $(".container").prepend(`<div class="alert  alert-success alert-dismissible fade show" role="alert" style="position:fixed; width:${$(".container").width()}px; z-index:11;">
    You have successfully reconnected to server.
    <button aria-label="Close" class="btn-close" data-bs-dismiss="alert" type="button">
    </button>
</div>`)
          });
    
    unseen = document.querySelectorAll(".unseen")
    unseen.forEach(e => {
        console.log(e.innerText == "")
        if (e.innerText == "") $(e).hide()
    });
    document.querySelectorAll(".span").forEach(function(e) {
        if (e.innerText == "") {
            e.innerText = "Hey There"
        }
    })
    socket.on("regis", data => {
        $(".empty").remove()
        $(".user").append(`<a href="/chat/${data}">
                        <div class="align-items-center d-flex hover py-2">
                            <img class="rounded-circle border border-dark" height="40" src="/static/images/default.jpg" width="40">
                            
                            <div class="ps-2" style="white-space: nowrap;">
                                <span class="fw-bold text-dark fs-5 main-data">
                                        <i class="status fa fa-circle text-secondary ${data}" aria-hidden="true" ></i>

                                    <span  class="names"></span>

                                </span>
                                
                                <br>
                                    <span id="to_${data}" class="span fs-6 fw-lighter text-dark">
                                        Hey There
                                </span>

                            </div>
                            
                        </div>
                        <hr class="m-0 text-dark">
                    </a>
`)
        a = document.createTextNode(data)
        $(".main-data").last().append(a)
    })
    //  status shower
    socket.on("status", data => {
        if (data.status == "Online") {
            $(`.${data.user}`).attr("class", `status fa fa-circle text-success ${data.user}`)
        } else {
            $(`.${data.user}`).attr("class", `status fa fa-circle text-secondary ${data.user}`)
        }
    })


    //  typing
    arr = new Set()
    socket.on("type", data => {
        spans = $($($(`a[href="/chat/${data.user}"]`).children().children()[1]).children()[2])
        arr.add(spans.text())
        if (data.user != current_user.value) {
            if (data.typing == true) {
                spans.html("<span style='color:green;font-weight:bold;'>Typing..<span>")
            } else {
                var span_text = arr.values().next().value;
                spans.text(span_text)
            }
        }
    })
    socket.on("connect", () => {
        socket.emit("connected", document.location.pathname)
    }); // search of on
    $(".search").click(function() {
        $(this).hide()
        $("#my_inp").removeClass("d-none")
        $("#my_inp").focus()
        $(".p-desc").addClass("d-none")
        $(".close").removeClass("d-none")
    })
    $(".close").click(function() {
        $(".user a").css("display", "initial")
        $(".nouser").remove()
        $(this).addClass("d-none")
        $(".search").show()
        $(".p-desc").removeClass("d-none")
        $("#my_inp").addClass("d-none")
    })
})
//  search filter
const isnone = (currentValue) => currentValue.style.display == "none";
var search = () => {
    var filter = $("#my_inp").val().toUpperCase()
    var names = $(".user a .names")
    for (i = 0; i < names.length; i++) {
        if (names[i].innerText.toUpperCase().indexOf(filter) > -1) {
            $(".user a")[i].style.display = "initial"
        } else {
            $(".user a")[i].style.display = "none"
        }
    }
    if (Array.prototype.slice.call($(".user a")).every(isnone)) {
        if ($(".nouser").length == 0) {
            $(".user").append(` <div class=" nouser px-2 d-flex align-items-center justify-content-center h-100 empty">
                            <p class="text-center text-muted">
                                No user found
                            </p>
                        </div>`)
        }
    } else {
        $(".nouser").remove()
    }
}