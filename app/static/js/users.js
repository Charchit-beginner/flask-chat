$(document).ready(function() {
    const audio = new Audio("/static/audio/notification.mp3")

    function vol(muted){
        if (muted){
        audio.muted = true
        $(".fa-volume-up").addClass("d-none")
        $(".fa-volume-mute").removeClass("d-none")
    }else{
        audio.muted = false
        $(".fa-volume-mute").addClass("d-none")
        $(".fa-volume-up").removeClass("d-none")
}

    }
    $(".fa-volume-up").click((e)=>{
        document.cookie = "muted=true;expires=Thu, 18 Dec 2100 12:00:00 UTC"
        vol(true)
    })
    $(".fa-volume-mute").click((e)=>{
        document.cookie = "muted=false;expires=Thu, 18 Dec 2100 12:00:00 UTC"
        vol(false)
    })
    const muted = ('; '+document.cookie).split(`; muted=`).pop().split(';')[0];
        if (muted == "true"){
          vol(true)
        }
        else{
          vol(false)
        }



    socket = io.connect(document.href);
    // last message shower
    socket.on("msg", data => {
        
        let unseen_msg_no = $(`a[href="/chat/${data.user}"]`).find("span.unseen")[0]
        let hasNumber = /\d/;
        if (data.rec_user == current_user.value) {
            $(`a[href="/chat/${data.user}"]`).find("span.span").text(data.msg)
                audio.play()
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
            dis("You have disconnected from the server. Reconnecting...")
        });
        socket.io.on("reconnect", () => {
            dis("You have successfully reconnected to server.")
          });
    
    var unseen = document.querySelectorAll(".unseen")
    unseen.forEach(e => {
        
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
        console.log(data)
        if (data.status == "Online") {
            $(`a[href="/chat/${data.user}"]`).find("i.status").attr("class", `status fa fa-circle text-success`)
        } else {
            $(`a[href="/chat/${data.user}"]`).find("i.status").attr("class", `status fa fa-circle text-secondary`)
        }
    })
    // update on change
    socket.on("username_changed",data =>{
        console.log(data)
          $(`a[href="/chat/${data.old}"]`).find("span.names").text(data.new)
          $(`a[href="/chat/${data.old}"]`).attr("href",`/chat/${data.new}`)
        })
    // user page change event
    $(document).on("visibilitychange",()=>{
            if (document.visibilityState == "hidden") {
                  socket.emit("idle",{status:"Idle"})
              } else  {
                setTimeout(function() {$("title").text("ChatApp")}, 2000);
                  socket.emit("idle",{status:"Online"})
                  
              }
        })

    // idle 
    socket.on("user_idle",data =>{
        console.log(data)
        if(data.stat == "Idle") {
            $(`a[href="/chat/${data.username}"]`).find("i.status").attr("class", `status fa fa-circle text-warning `)
        }else{
            $(`a[href="/chat/${data.username}"]`).find("i.status").attr("class", `status fa fa-circle text-success`)
        }
    })
    // editing profile
socket.on("editing_profile",data=>{
            console.log(data)
            $(`a[href="/chat/${data}"]`).find("i.status").attr("class", `status fa fa-circle text-warning `)
        })

    //  typing
    const arr = new Set()
    socket.on("type", data => {
        spans = $(`a[href="/chat/${data.user}"]`).find("span.span")
        arr.add(spans.text())
        console.log(arr)
        if (data.user != current_user.value) {
            if (data.typing == true) {
                spans.html("<span style='color:green;font-weight:bold;'>Typing..<span>")
            } else {
                var span_text = spans[0].innerText == "Typing.." ?arr.values().next().value:Array.from(arr).pop()
                console.log(arr,span_text)
                spans.text(span_text)
            }
        }
    })
    // show blocked users
    $(".block-users").click(e=>{
        
        if ($(e.target).text() == "Show Blocked Users"){
            $(".blocked").removeClass("d-none")
            $(".hidden-hr").removeClass("d-none")
            $(e.target).text("Hide Blocked Users")
            unseen.forEach(e => {if (e.innerText == "") $(e).hide()});
        }
        else{
            $(e.target).text("Show Blocked Users")
            $(".hidden-hr").addClass("d-none")
            $(".blocked").addClass("d-none")    
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
// togle between dark and white mode
let check = document.querySelector("input[type='checkbox']")
document.addEventListener("change",()=>{
    if (check.checked){
        document.cookie = "mode=Dark;expires=Thu, 18 Dec 2100 12:00:00 UTC"
        check_mode()
    }
    else{
        document.cookie = "mode=Light;expires=Thu, 18 Dec 2100 12:00:00 UTC"
        check_mode()
    }
    // hover:#202225
})
check_mode()

// funtions 
function check_mode(){
    const mode = ('; '+document.cookie).split(`; mode=`).pop().split(';')[0];
    if (mode == "Dark"){
              $("body").css({"background":"#000000c2"})
        $(".card").css({"background":"#141415","color":"#8e9297"})
        $(".btn-dark").css({"color":"white","background-color":"#252a41"})
        document.querySelectorAll(".hover").forEach((e)=>{
            e.style.setProperty('--td-background-color', '#202225')
    })
        $(".text-dark").addClass("text-light").removeClass("text-dark")
        $(".rounded").addClass("bg-dark").addClass("text-light")
    }
    else{
              $("body").css({"background":"#f4f4f4"})
        $(".card").css({"background":"white","color":"black"})
        $(".btn-dark").css({"color":"white","background-color":"#212529"})
        document.querySelectorAll(".hover").forEach((e)=>{
            e.style.setProperty('--td-background-color', '#ebebeb')
        })
        $(".rounded").removeClass("bg-dark").removeClass("text-light")
        $(".text-light").addClass("text-dark").removeClass("text-light")
        $(".unseen").addClass("text-light").removeClass("text-dark")
    }
    $(".mode").text(`${mode!="" ? mode:"Light"}  mode`)
}
function dis(msg){
    $(".container").prepend(`<div class="alert  alert-success alert-dismissible fade show" role="alert" style="position:fixed; width:${$(".container").width()}px; z-index:11;">
    ${msg}
    <button aria-label="Close" class="btn-close" data-bs-dismiss="alert" type="button">
    </button>
</div>`)
           setTimeout(function() {$(".show").hide()}, 2000);
}