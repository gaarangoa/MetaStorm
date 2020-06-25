window.onload = function ()
{

    var machine = '/';
    // var machine = '/metastorm2/';

    $('#Blogin').click(function ()
    {
        var form_data = new FormData($('#loginForm')[0]);
        //alert()
        $.ajax({
            type: 'POST',
            url: machine + 'lgn',
            //url: '/lgn',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            async: true,
            success: function (data)
            {
                if (data.status == "fatal") {
                    alert("The user and/or password don't match our records!")
                    //window.open(machine+"login","_self")
                } else {
                    console.log(data)
                    window.open(machine + "muser?uid=" + data.uid, "_self");
                }
            }
        });
    });


    forgot_pass = function ()
    {
        email = $("#loginEMAIL").val()


        $.ajax({
            url: machine + "forgot_pass",
            type: "POST",
            data: JSON.stringify({
                email: email
            }),
            async: true,
            contentType: "application/json; charset=utf-8",
            success: function (dat)
            {
                alert(dat.status)
            }
        });

    }


};