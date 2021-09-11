// togle between dark and white mode
let check = document.querySelector("input[type='checkbox']")
document.addEventListener("change",()=>{
    if (check.checked){
        document.cookie = "mode=Dark;expires=Thu, 18 Dec 2100 12:00:00 UTC;path=/"
        checkMode()
    }
    else{
        console.log("hi")
        document.cookie = "mode=Light;expires=Thu, 18 Dec 2100 12:00:00 UTC;path=/"
        checkMode()
    }
    // hover:#202225
})

function checkMode(){
const mode = ('; '+document.cookie).split(`; mode=`).pop().split(';')[0];
    if (mode == "Dark"){
        $("body").css({"background":"#000000c2"})
        $(".card").css({"background":"#1f212e","color":"white"})
        $("#status").css("color","#8e9297")
        $(".form-control").addClass("dark-input")
        $("#container").css("background","#252729c7")
        $(".input-group").css({"background":"#36393f","color": "white"})
        $(".btn-dark").css({"color":"white","background-color":"#252a41"})
        $(".dropdown-menu").css("background","black")
        $(".dropdown-item").css("color","white")
    }
    else{
                $("body").css({"background":"#f4f4f4"})
        $(".card").css({"background":"white","color":"black"})
        $(".btn-dark").css({"color":"white","background-color":"#212529"})
        $("#container").css("background","#f8f8f8")
        
        $(".form-control").removeClass("dark-input")
        $(".input-group").css({"background":"white","color": "black"})
        $("#status").css("color","black")
        $(".dropdown-menu").css("background","white")
        $(".dropdown-item").css("color","black")
    }
}

checkMode()