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
            "username": $("#email-login").val(),
            "password": $("#pwd-login").val()
        },
        function (response, status) {
            alert("Data: " + response.message.email + "\nStatus: " + status);
            console.log(response.message.email);
            var dropdown = "<li class='dropdown'><a class='dropdown-toggle' data-toggle='dropdown' "+ "href='#'>"+"Hi " + response.message.email +"<span class='caret'></span></a><ul class='dropdown-menu'></ul></li>";


            $("#current-login").empty();
            $("#current-login").append(dropdown);
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


    $('#logout').on('click',function () {

        $.ajax({
            type: "GET",
            url: "http://localhost:8000/logout/"
        }).function(response)
            {
                console.log(response.message)
            };

    })

