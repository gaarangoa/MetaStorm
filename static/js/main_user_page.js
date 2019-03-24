window.onload = function() {

    var machine = Parameters.host;


    $.urlParam = function(name) {
        var results = new RegExp('[\?&]' + name + '=([^&#]*)').exec(window.location.href);
        if (results == null) {
            return null;
        } else {
            return results[1] || 0;
        }
    }

    userID = $.urlParam('uid')





    /// setup the map with all the locations where the metagenomes have been computed

    cmd = 'select cast(lat as real) lat,cast(lng as real) lng, sample_id sid, project_id pid from samples order by random() limit 10'
    $.ajax({
        //url: "/zhanglab/software/CMetAnn/start.wsgi/GetAllInfo",
        url: machine + "consult",
        type: "POST",
        data: JSON.stringify({
            sql: cmd
        }),
        contentType: "application/json; charset=utf-8",
        success: function(dat) {
            //console.log(dat)
            drop(dat.data)
        }
    });



    /// recent projects panel

    browse_table_fn = function(div, dataAdapter) {

        $("#" + div).jqxDataTable({
            width: "100%",
            pageable: true,
            pagerMode: 'advanced',
            source: dataAdapter,
            altRows: true,
            sortable: true,
            filterable: true,
            columns: [{
                    text: '<b>Biome</b>',
                    dataField: 'biome',
                    width: "15%",
                    align: 'center',
                    cellsAlign: 'center'
                },
                {
                    text: '<b>Project Name</b>',
                    dataField: 'project_name',
                    width: "20%",
                    align: 'center',
                    cellsAlign: 'left',
                    cellsRenderer: function(row, column, value, rowData) {
                        if (rowData.access == 'lock') {
                            return '<i class="fa fa-fw fa-lock" style="color:#cc0000"></i>' + value
                        } else {
                            return '<i class="fa fa-fw fa-unlock" style="color:#000099"></i>' + value
                        }
                    }
                },
                {
                    text: '<b>Description</b>',
                    dataField: 'project_description',
                    width: "35%",
                    align: 'center',
                    cellsAlign: 'left'
                },
                {
                    text: '<b>Analysis</b>',
                    dataField: 'pipeline',
                    width: "20%",
                    align: 'center',
                    cellsAlign: 'center',
                    cellsRenderer: function(row, column, value, rowData) {


                        if (rowData.access == 'unlock') {
                            pips = ''
                            pipsi = value.split(",").forEach(function(a, b, c) {
                                pips += '<a target="_blank" href="/ExploreProject?uid=' + userID + '&pid=' + rowData.project_id + '&pip=' + a + '">' + a + '</a> '
                            })
                            return pips
                        } else {
                            return value.replace(',', ' ')
                        }
                    }
                },
                {
                    text: '<b>Samples</b>',
                    dataField: 'samples',
                    width: "10%",
                    cellsAlign: 'center',
                    align: 'center'
                },
                //{ text: '<b>Access</b>', dataField: 'Access', width: 10%, align: 'center', cellsAlign: 'center'},
            ]
        });

    }


    cmd = 'select * from (select project_name, project_id, project_description, access, samples, pipeline, biome  from (select a.project_id, b.project_name, b.project_description, b.project_short_description access, sum(1) samples, a.environment biome from samples a join project b on a.project_id = b.project_id group by a.project_id ) c join (select pid,group_concat( distinct(pip)) pipeline from jobs group by pid) d on d.pid=c.project_id ) e join (select group_concat(distinct(user_id)) users , project_id pip from user_projects group by project_id) f where e.project_id=f.pip'
    $.ajax({
        //url: "/zhanglab/software/CMetAnn/start.wsgi/GetAllInfo",
        url: machine + "consult",
        type: "POST",
        data: JSON.stringify({
            sql: cmd
        }),
        contentType: "application/json; charset=utf-8",
        success: function(dat) {

            $("#browse_projects_overlay").remove()

            // console.log(dat.data)
            pron = 0
            dat.data.forEach(function(a, b, c) {
                return (pron += a.samples)
            })

            $("#total_number_of_projects").html(dat.data.length)

            var source = {
                localData: dat.data,
                dataType: "array",
                dataFields: [{
                        name: 'biome',
                        type: 'string'
                    },
                    {
                        name: 'project_name',
                        type: 'string'
                    },
                    {
                        name: 'project_description',
                        type: 'string'
                    },
                    {
                        name: 'pipeline',
                        type: 'string'
                    },
                    {
                        name: 'samples',
                        type: 'number'
                    },
                    {
                        name: 'project_id',
                        type: 'string'
                    },
                    {
                        name: 'access',
                        type: 'string'
                    },
                    {
                        name: 'users',
                        type: 'string'
                    }
                ]
            };
            var dataAdapter = new $.jqx.dataAdapter(source);


            // initialize jqxDataTable
            browse_table_fn('recent_projects', dataAdapter)
            browse_table_fn('browse_projects_comparison', dataAdapter)

        }
    });


    $("#browse_projects_comparison").on('rowSelect', function(event) {
        // event arguments
        var rowData = args.row;
        exp = new RegExp(userID);
        if (exp.test(rowData.users) || rowData.access == "unlock") {
            $("#projects_compare_list").append("<option selected name='PCL' value='" + rowData.project_id + "' > " + rowData.project_name + " </option>")
                // console.log(rowData);
        } else {
            alert("You DO NOT have access to this project.\nThis can happen because: \n1) the project is private and \n2) The project is not shared with you.")
        }

    });















    button_selected_projects = function(div) {

        var values = $(div + " option").map(function() {
            return $(this).val();
        });
        values = $("#projects_compare_list option")

        vv = [];
        vn = [];
        for (i = 0; i < values.length; i++) {
            vv.push($(values[i]).val());
            vn.push($(values[i]).text())
        }

        if (vv.length == 0) {
            alert('Select at least one project')
        } else {

            //console.log(vv)
            var x = window.open(machine + "compare_projects?uid=" + userID + "?pip=matches");
            x.pids = vv
            x.pnames = vn

            //console.log(vn)


        }
    }














    remove_selection = function(div) {
        $(div).empty()
    }





























    cmd = 'select * from samples'
    $.ajax({
        //url: "/zhanglab/software/CMetAnn/start.wsgi/GetAllInfo",
        url: machine + "consult",
        type: "POST",
        data: JSON.stringify({
            sql: cmd
        }),
        contentType: "application/json; charset=utf-8",
        success: function(dat) {
            //console.log(dat.data)
            $("#total_number_of_samples").html(dat.data.length)
        }
    });


    cmd = 'select count(1) cs from reference'
    $.ajax({
        //url: "/zhanglab/software/CMetAnn/start.wsgi/GetAllInfo",
        url: machine + "consult",
        type: "POST",
        data: JSON.stringify({
            sql: cmd
        }),
        contentType: "application/json; charset=utf-8",
        success: function(dat) {
            //console.log(dat.data)
            $("#total_number_of_reference_datasets").html(dat.data[0].cs)
        }
    });


    cmd = 'select count(1) cs from user'
    $.ajax({
        //url: "/zhanglab/software/CMetAnn/start.wsgi/GetAllInfo",
        url: machine + "consult",
        type: "POST",
        data: JSON.stringify({
            sql: cmd
        }),
        contentType: "application/json; charset=utf-8",
        success: function(dat) {
            //console.log(dat.data)
            $("#total_number_of_users").html(dat.data[0].cs)
        }
    });

    vsession(userID)



    /*Get the user, projects and samples info*/
    //$("#sidemenu").html('<li class="active"><a onclick="logout(\''+userID+'\')"><i class="fa fa-sign-out"></i> <span>Log out</span></a></li>')

    var update = function(userID) {
        $.ajax({
            //url: "/zhanglab/software/CMetAnn/start.wsgi/GetAllInfo",
            url: machine + "GetAllInfo",
            type: "POST",
            data: JSON.stringify({
                uid: userID
            }),
            contentType: "application/json; charset=utf-8",
            success: function(dat) {
                if (dat.status == "ERROR") {
                    //console.log(dat)
                    window.open(machine + "login", "_self")
                } else {
                    //console.log(dat)

                    $("#profile_user_name").val(dat.uname)
                    $("#profile_user_id").val(userID)
                    $("#profile_user_email").val(dat.email)
                    $("#profile_user_affiliation").val(dat.affiliation)
                    $("#pass_user_id").val(userID)

                    $("#UserName1").html(dat.uname)
                    $("#userID").html(dat.uid)
                    $("#UserContact").html(dat.email)
                    $("#ProjectNameSelect").html("")
                    for (i = 0; i < dat.projects.length; i++) {
                        $("#ProjectNameSelect").append('<option value=' + dat.projects[i]['project_id'] + '>' + dat.projects[i]['project_name'] + '</option>')
                    }
                }
                if (userID == "TesREPDooc73Ohw") {
                    $("#ifguest").html(
                        '<div class="callout callout-danger lead ">' +
                        '<p><b>Be aware!</b>: Despite guest session has access to all the resouces in MetaStorm, it <b>WILL NOT</b> run any analysis. However, you can visualize any MetaStorm Project</p>' +
                        '</div>')
                }

                $("#my_projects_overlay").remove()
                $("#create_new_project_overlay").remove()
                $("#customize_database_overlay").remove()
                $("#project_location_overlay").remove()

            }
        });
    }

    update(userID)







    /*Submit a new project*/

    $(document).on("click", "#SubmitNewProject", function() {
        window.open(machine + "metadata?uid=" + userID)
    });


    /*Remove a project*/

    $(document).on("click", "#RemoveProject", function() {
        projectID = $("#ProjectNameSelect option:selected").val();


        if (confirm("Do you want to remove the project?")) {

            $.ajax({
                url: machine + "remove_element",
                type: "POST",
                data: JSON.stringify({
                    pid: projectID,
                    uid: userID
                }),
                contentType: "application/json; charset=utf-8",
                success: function(dat) {
                    window.open(machine + "muser?uid=" + userID, "_self")
                }
            });
        }
    });















    $(document).on("click", "#matches_go", function() {
        projectID = $("#ProjectNameSelect option:selected").val();
        window.open(machine + "UpdateProject?uid=" + userID + "&pid=" + projectID + "&pip=matches")
    });


    $(document).on("click", "#assembly_go", function() {
        projectID = $("#ProjectNameSelect option:selected").val();
        window.open(machine + "UpdateProject?uid=" + userID + "&pid=" + projectID + "&pip=assembly")
    });








    $('#upload_reference').click(function() {
        window.open(machine + "upload_reference?uid=" + userID)
    })







    open_profile = function(uid) {
        $("#home_page_form").hide()
        $("#comparison_form").hide()
        $("#profile_page").show()
        $("#documentation_page").hide()
    }


    open_home_page_form = function(uid) {
        $("#home_page_form").show()
        $("#profile_page").hide()
        $("#comparison_form").hide()
        $("#documentation_page").hide()
    }

    open_comparison = function(uid) {
        $("#home_page_form").hide()
        $("#profile_page").hide()
        $("#comparison_form").show()
        $("#documentation_page").hide()
    }


    open_documentation = function() {
        $("#home_page_form").hide()
        $("#profile_page").hide()
        $("#comparison_form").hide()
        $("#documentation_page").show()
    }




    update_profile = function(uid) {

        $("#personal_information_homepage").append("<div class='overlay' id='personal_information_homepage_overlay'><i class='fa fa-refresh fa-spin'></i></div>")

        email = $("#profile_user_email").val()
        affiliation = $("#profile_user_affiliation").val()

        cmd = "UPDATE user SET user_affiliation='" + email + "', organization='" + affiliation + "'  WHERE user_id='" + uid + "'"


        $.ajax({
            url: machine + "consult",
            type: "POST",
            async: true,
            data: JSON.stringify({
                sql: cmd
            }),
            contentType: "application/json; charset=utf-8",
            success: function(x) {
                $("#personal_information_homepage_overlay").remove()
                    //console.log(x, cmd)
            }
        });
    }




    change_password = function() {
        // console.log('change password')

        $("#change_password_homepage").append("<div class='overlay' id='change_password_homepage_overlay'><i class='fa fa-refresh fa-spin'></i></div>")


        var form_data = new FormData($('#change_password_form')[0]);
        $.ajax({
            url: machine + "change_password",
            type: "POST",
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            async: true,
            success: function(x) {
                $("#change_password_homepage_overlay").remove()
                alert(x)
            }
        });

    }












    /*





    */





};