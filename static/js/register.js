window.onload = function() {
    machine = "/"
    $('#BRegister').click(function() {
        var form_data = new FormData($('#new_user_form')[0]);
        console.log(form_data)

        $.ajax({
            type: 'POST',
            url: machine + 'insert_new_user',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            async: true,
            success: function(data) {
                if (data.status == "ERROR") {
                    alert("This email address is already in use")
                } else {
                    //console.log(data)
                    window.open(machine + "/login", "_self")
                }
            },
        });
    });

};