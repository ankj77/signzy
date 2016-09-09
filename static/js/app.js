/**
 * Created by deepanshu on 9/9/16.
 */

$("#btn1").click(function () {
    var details = {
        "username": $("#email-login").val(),
        "password": $("#pwd-login").val(),
    }

    // $.ajax({
    //   type: "POST",
    //   url: "http://localhost:8000/login/",
    //   data: details,
    //   dataType: 'application/json',
    //   success: userSignIn
    // });
    //

    $.post("http://localhost:8000/login/",
        {
            "password": "helloworld",
            "username": "ddsr17@gmail.com"
        },
        function (response, status) {
            alert("Data: " + response.message.email + "\nStatus: " + status);
            console.log(response.message.email);
            var dropdown = "<ul class='dropdown-menu'><li>Hi" + response.message.email + "</li><li>My Account</li><li>Logout</li></ul>";
            $("#currentstatus").empty();
            $("#currentstatus").append(dropdown);
        });

});


$("#btn2").click(function () {

    var data = {
        "first_name": $("#firstname").val(),
        "last_name": $("#lastname").val(),
        "username": $("#username").val(),
        "email": $("#email").val(),
        "password": $("#pwd").val()
    }
    $.ajax({
        type: "POST",
        url: "http://localhost:8000/signup/",
        data: data,
        dataType: 'application/json'
    });

});


$('#logout').click(function () {

    $.ajax({
        type: "GET",
        url: "http://localhost:8000/logout/"


    }).function(response)
    {
        console.log(response.message
        )
    }
    ;
})

