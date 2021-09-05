let check = document.querySelector("input[type='checkbox']")
document.addEventListener("change",()=>{
    if (check.checked){
        document.cookie = "mode=Dark;expires=Thu, 18 Dec 2100 12:00:00 UTC;path=/"
        check_mode()
    }
    else{
        document.cookie = "mode=Light;expires=Thu, 18 Dec 2100 12:00:00 UTC;path=/"
        check_mode()
    }
})
    check_mode()
function check_mode(){
const mode = ('; '+document.cookie).split(`; mode=`).pop().split(';')[0];
    if (mode == "Dark"){
        $("body").css({"background":"#000000c2"})
        $(".card").css({"background":"#1f212e","color":"white"})
        
        $(".form-control").addClass("dark-input")
        $("#container").css("background","#252729c7")
        $(".input-group").css({"background":"#36393f","color": "white","border":"1px solid black"})
        $(".btn-dark").css({"color":"white","background-color":"#252a41"})
        $(".dropdown-menu").css("background","black")
        $(".dropdown-item").css("color","white")
        $(".text-dark").addClass("text-light").removeClass("text-dark")
        $(".dropdown-toggle").addClass("text-light").removeClass("text-muted")
        $(".modal-content").css({"background":"black","color":"white"})
    }

    else{
                $("body").css({"background":"#f4f4f4"})
        $(".card").css({"background":"white","color":"black"})
        $(".btn-dark").css({"color":"white","background-color":"#212529"})
        $("#container").css("background","#f8f8f8")
        
        $(".form-control").removeClass("dark-input")
        $(".input-group").css({"background":"white","color": "black","border":"1px solid white"})
        $(".dropdown-menu").css("background","white")
        $(".dropdown-item").css("color","black")
        $(".text-light").addClass("text-dark").removeClass("text-light")
        $(".dropdown-toggle").addClass("text-muted").removeClass("text-light")
        $(".modal-content").css({"background":"white","color":"black"})
    }

    

}