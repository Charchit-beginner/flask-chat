Pushy.register({ appId: '613cda4f85d9d7b816d44a92' }).then(function (deviceToken) {
   	    $.ajax({
        type: "POST",
        url: `${window.location.pathname}`,
        data: {
			id:deviceToken 
        },
        
        success: function(response) {
        },
    });
}).catch(function (err) {
   
});