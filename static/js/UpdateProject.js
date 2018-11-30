window.onload = function() {
    // Project setup table
    // table with all the results from the assembly -  this is an overall of the assembly performance


    machine = "/MetaStorm/"
    upload_dir = "/home/raid/www/MetaStorm/main/Files/PROJECTS/"

    uid = urlParam('uid')
    pid = urlParam('pid')
    pip = urlParam('pip')

    vsession(uid)

    REFS = {}

    $("#setProjectNameinLoad").val(pid)

    /*Get the user, projects and samples info*/

    $.ajax({
        url: machine + "GetAllInfo",
        type: "POST",
        data: JSON.stringify({
            uid: uid
        }),
        async: true,
        contentType: "application/json; charset=utf-8",
        success: function(dat) {
            ////console.log(dat)
            $("#UserName1").html(dat.uname)
            $("#userID").html(dat.uid)
            $("#UserContact").html(dat.email)
        }
    });

    $.ajax({
        url: machine + "consult",
        type: "POST",
        async: true,
        data: JSON.stringify({
            sql: 'select * from project where project_id="' + pid + '"'
        }),
        contentType: "application/json; charset=utf-8",
        success: function(x) {
            ////console.log(x)
            $("#updatePdescription").html(x.data[0]['project_description'])
            $("#updatePname").html("# " + x.data[0]['project_name'])
        }
    });



    var logs = function(date, sid, pip, status, processed) {
        if (status == "done") {
            color = 'blue'
        } else if (status == "queue") {
            color = "yellow"
        } else if (status == 'running') {
            color = 'black'
        } else {
            color = 'red'
        }
        return ['<li class="time-label">' +
            '<span class="bg-' + color + '">' +
            date +
            '</span>' +
            '</li>' +
            '<li>' +
            '<i class="fa fa-envelope bg-' + color + '"></i>' +
            '<div class="timeline-item">' +
            '<span class="time"><i class="fa fa-clock-o"></i> 00:00</span>' +
            '<h3 class="timeline-header"><a href="#">Sample: </a><b>' + sid + '</b></h3>' +
            '<h3 class="timeline-header"><a href="#">Submitted by: </a><b>' + processed + '</b></h3>' +
            '<div class="timeline-body">' +
            'The analysis of the sample <b>' + sid + '</b>, with the <b>' + pip + '</b> pipeline is: <code>' + status + "</code> " +
            '</div>' +
            '</div>' +
            '</li>'
        ]
    }






    // here collect the logs and see the status of each run:
    $.ajax({
        url: machine + "consult",
        type: "POST",
        async: true,
        data: JSON.stringify({
            sql: 'select * from (select * from (select * from jobs where pid="' + pid + '" and pip="' + pip +
                '" order by date desc) a join (select sample_name, sample_id from samples) b where b.sample_id=a.sid)  c join (select user_id, user_name from user ) d where c.uid=d.user_id'
        }),
        contentType: "application/json; charset=utf-8",
        success: function(x) {
            //console.log(x.data)
            x.data.forEach(function(item, index) {
                $("#logs").append(logs(item.date, item.sample_name, item.pip, item.status, item.user_name))
            })

        }
    });






    /*Load root reference databases*/
    $.ajax({
        url: machine + "consult",
        type: "POST",
        async: true,
        data: JSON.stringify({
            sql: 'select reference_id, reference_name, reference_description, status, user_id from reference'
        }),
        contentType: "application/json; charset=utf-8",
        success: function(x) {
            ////console.log(x)

            x.data.forEach(function(e, ix) { //element, index
                //console.log(e,ix)
                if (e['status'] == 'done') {



                    if (e['user_id'] == 'default') {
                        $("#selectTaxonomyDatabase").append('<input checked="true" type="checkbox" name="selectedReferenceDatasets" value="' +
                            e['reference_id'] + '"><label for="' + e['reference_id'] + '"> ' +
                            e['reference_name'] + ' <i class="fa fa-fw fa-question-circle" style="color:#cc0000" id="B_' + e['reference_id'] + '"></i> </label><br>')

                    } else if (e['user_id'] == 'ARG') {
                        $("#selectARGdatabases").append('<input checked="true" type="checkbox" name="selectedReferenceDatasets" value="' +
                            e['reference_id'] + '"><label for="' + e['reference_id'] + '"> ' +
                            e['reference_name'] + ' <i class="fa fa-fw fa-question-circle" style="color:#cc00FF" id="B_' + e['reference_id'] + '"></i> </label><br>')
                    } else if (e['user_id'] == uid) {
                        $("#selectMyDatabases").append('<input type="checkbox" name="selectedReferenceDatasets" value="' +
                            e['reference_id'] + '"><label for="' + e['reference_id'] + '"> ' +
                            e['reference_name'] + ' <i class="fa fa-fw fa-question-circle" style="color:#cc0000" id="B_' + e['reference_id'] + '"></i> </label><br>')
                    } else {
                        $("#selectCommunityDatabases").append('<input type="checkbox" name="selectedReferenceDatasets" value="' +
                            e['reference_id'] + '"><label for="' + e['reference_id'] + '"> ' +
                            e['reference_name'] + ' <i class="fa fa-fw fa-question-circle" style="color:#cc0000" id="B_' + e['reference_id'] + '"></i> </label><br>')
                    }


                    REFS[e['reference_id']] = e['reference_name']

                    Tipped.create('#B_' + e['reference_id'], function(element) {

                            return {
                                title: e['reference_name'],
                                content: '<div style="width:300px; min-height:50px; max-height:200px; overflow: auto">' + e['reference_description'] + '</div>'
                            };
                        }, {
                            skin: 'red'
                        }

                    );

                }
            })




            $('input').iCheck({
                checkboxClass: 'icheckbox_square-blue',
                radioClass: 'iradio_square-blue',
                increaseArea: '20%' // optional
            });


            $("#jqxNavigationBar").jqxNavigationBar({
                width: "100%",
                height: "auto",
                expandMode: 'toggle',
                expandMode: 'multiple',
                expandedIndexes: [0, 1]
            });

            var sid = $("#SampleNameSelect option:selected").val();
            upload_php("#uploader", sid, pid, pip, uid, upload_dir)
        }
    });

    //






    /*Load current samples the main table with the samples info*/

    var headerRenderer = function(instance, td, row, col, prop, value, cellProperties) {
        Handsontable.renderers.TextRenderer.apply(this, arguments);
        //td.style.fontWeight = 'bold';
        td.style.color = 'white'
        td.style.textAlign = 'center';
        td.style.backgroundColor = 'rgba(0,125,10,1)';
    };

    var actionHTML = function(instance, td, row, col, prop, value, cellProperties) {

        $(td).html("<a href=" + machine + 'ViewSample?sid=' + value + "&pid=" + pid + "&uid=" + uid + "&pip=" + pip + " target='_blank'>" + value + "</a>"); //empty is needed because you are rendering to an existing cell
    };

    var get_samples_info = function() {
        //cmd='select c.sample_id,c.sample_name, c.sample_set, c.environment, c.library_preparation, c.reads1, c.reads2, c.status from (select * from samples a inner join project_status b on a.project_id==b.project_id and a.sample_id==b.sample_id) c where project_id=="'+pid+'"'
        cmd = 'select c.sample_id,c.sample_name, c.sample_set, c.environment, c.library_preparation, c.reads1, c.reads2, c.lat, c.lng from (select * from samples) c where project_id=="' + pid + '"'
        $.ajax({
            url: machine + "consult",
            type: "POST",
            //data: JSON.stringify({sql:'select sample_id, sample_name, sample_set, environment, library_preparation, reads1, reads2 from samples where project_id="'+pid+'"'}),
            data: JSON.stringify({
                sql: cmd
            }),
            contentType: "application/json; charset=utf-8",
            success: function(x) {
                //console.log(x)
                //alert(x.data[0])

                data = [] //[{ID:"ID",Name:"Sample Name",Condition:"Sequence Method",Environment:"Biome",Library:"Experiment Type",Mate1:"FastQ1",Mate2:"FastQ2"}]

                for (i = 0; i < x.data.length; i++) {
                    item = {
                        ID: x.data[i]['c.sample_id'],
                        Name: x.data[i]['c.sample_name'],
                        Condition: x.data[i]['c.sample_set'],
                        Environment: x.data[i]['c.environment'],
                        Library: x.data[i]['c.library_preparation'],
                        Mate1: x.data[i]['c.reads1'],
                        Mate2: x.data[i]['c.reads2']
                    }
                    data.push(item)
                }

                //console.log("DATA:",data)

                $("#BodyCurrentSamples").html('')
                    // $("#BodyCurrentSamples").css('min-width','400px');
                var container = document.getElementById('BodyCurrentSamples');

                var previous_samples = new Handsontable(container, {
                    data: data,
                    autoWrapRow: true,
                    colHeaders: ['Name', 'Unique Identifier', 'Sequence Method', 'Biome', 'Experiment type', 'FastQ1', 'FastQ2'],
                    rowHeaders: true,
                    columnSorting: true,
                    //manualColumnResize: true,
                    stretchH: 'all',
                    // maxRows: data.length,
                    //fixedRowsTop: 1,
                    //manualColumnMove: false,
                    //manualRowMove: false,
                    columns: [{
                            data: "Name"
                        },
                        {
                            data: "ID",
                            renderer: actionHTML
                        },
                        {
                            data: "Condition"
                        },
                        {
                            data: "Environment"
                        },
                        {
                            data: "Library"
                        },
                        {
                            data: "Mate1"
                        },
                        {
                            data: "Mate2"
                        }
                    ],
                    dropdownMenu: true,
                    filters: true,
                    /*cells: function (row, col, prop) {
                     var cellProperties = {};
                     if (row === 0) {
                       //cellProperties.renderer = headerRenderer;
                     }

                     return cellProperties;
                    },*/
                });

                /*setup the samples for selection*/
                $("#SampleNameSelectToRemove").html('<option>Sample ID</option>')
                $("#SampleNameSelect").html("<option>Name</option>")
                $("#Read1Select").html("<option>Fastq 2</option>")
                $("#Read2Select").html("<option>Fastq 2</option>")

                for (i = 0; i < x.data.length; i++) {
                    $("#SampleNameSelectToRemove").append('<option value=' + x.data[i]['c.sample_id'] + '><b>' + x.data[i]['c.sample_name'] + '</b> (' + x.data[i]['c.sample_id'] + ')</option>')
                    $("#SampleNameSelect").append('<option value=' + x.data[i]['c.sample_id'] + '>' + x.data[i]['c.sample_name'] + '</b> (' + x.data[i]['c.sample_id'] + ')</option>')
                        //$("#Read1Select").append('<option value='+x.data[i]['c.reads1']+'>'+x.data[i]['c.reads1']+'</option>')
                        //$("#Read2Select").append('<option value='+x.data[i]['c.reads2']+'>'+x.data[i]['c.reads2']+'</option>')
                }

                //Add the number of samples to the project information tab
                $("#updateNumberSamplesTab1").html(x.data.length)

                //console.log(x)

            }
        });


        /* $.ajax({
             url: machine+"consult",
             type: "POST",
             async: true,
             data: JSON.stringify({sql:'select * from fastqFiles where pid="'+pid+'"'}),
             contentType: "application/json; charset=utf-8",
             success: function(x) {

                 for(i=0;i<x.data.length;i++){
                   $("#Read1Select").append('<option value='+x.data[i]['file']+'>'+x.data[i]['file']+'</option>')
                   $("#Read2Select").append('<option value='+x.data[i]['file']+'>'+x.data[i]['file']+'</option>')
                 }
             }
         }); */


    }

    get_samples_info()





































    /*send action to sql*/
    // this function is useful if I want to send some sql-based code -  only works with the main database
    var exql = function(consult) {
        $.ajax({
            url: machine + "consult",
            type: "POST",
            async: true,
            data: JSON.stringify({
                sql: consult
            }),
            contentType: "application/json; charset=utf-8",
            success: function(dat) {
                get_samples_info()
            }
        });
    }

    /*remove samples*/
    $(document).on("click", "#RemoveSample", function() {
        var sid = $("#SampleNameSelectToRemove option:selected").val();

        $.ajax({
            url: machine + "removesample",
            type: "POST",
            async: true,
            data: JSON.stringify({
                sid: sid,
                pid: pid,
                pip: pip,
                uid: uid
            }),
            contentType: "application/json; charset=utf-8",
            success: function(dat) {
                //console.log(dat)

            }
        });

        get_samples_info()

    });






























    /*compare samples*/
    $(document).on("click", "#RunComparativeAnalysis", function() {
        // alert()
        window.open(machine + "compare_samples?pid=" + pid + "&uid=" + uid + "&pip=" + pip)
    });

























    /*when click on insert show the insert form*/
    $(document).on("click", "#InsertSample", function() {
        $("#SamplesSetupMain").show()
        $("#InsertSample").hide()

    });



    /*when click on insert show the remove sample form*/
    $(document).on("click", "#RemoveSampleGO", function() {
        $("#RemoveSampleForm").show()
    });


    /*when click refresh the sample list form*/
    $(document).on("click", "#RefreshSampleGetForm", function() {

        get_samples_info()

        $("#logs").html("")

        $.ajax({
            url: machine + "consult",
            type: "POST",
            async: true,
            data: JSON.stringify({
                sql: 'select * from (select * from (select * from jobs where pid="' + pid + '" and pip="' + pip +
                    '" order by date desc) a join (select sample_name, sample_id from samples) b where b.sample_id=a.sid)  c join (select user_id, user_name from user ) d where c.uid=d.user_id'
            }),
            contentType: "application/json; charset=utf-8",
            success: function(x) {
                //console.log(x.data)
                x.data.forEach(function(item, index) {
                    $("#logs").append(logs(item.date, item.sample_name, item.pip, item.status, item.user_name))
                })

            }
        });


    });


    /*when click rerun show update and submit forms*/
    $(document).on("click", "#ReRunSampleGetForm", function() {
        $("#UploadFilesMain").show()
        $("#RunMetaGenMain").show()
    });















    /*Insert new sample*/



    document.getElementById("NumberSamplesButton").onclick = function() {
        setupNumberSamples();
        $("#submitMetagenome").removeAttr('disabled')
    };
    $("#NumberSamples").on('keydown', function(e) {
        if (e.keyCode == 13) {
            setupNumberSamples();
            $("#submitMetagenome").removeAttr('disabled')
        }
    });

    var setupNumberSamples = function() {

        $('#table').html('')
        $('#table').css('min-width', '800px');
        $('#table').css('min-height', '400px');
        var container = document.getElementById('table');
        var totalsamples = document.getElementById("NumberSamples").value;

        matrix = [
                ['', '', '', '', '0', '0']
            ] //[['Sample Name','Sequence Method', 'Biome', 'Experiment Type', 'Latitude', 'Longitude']]
        for (var i = 1; i < totalsamples; i++) {
            matrix.push(['', '', '', '', '0', '0'])
        }

        var hot = new Handsontable(container, {
            data: matrix,
            //autoWrapCol: true,
            colHeaders: true,
            rowHeaders: true,
            //columnSorting: false,
            // stretchH: 'all',
            // width: 800,
            maxRows: totalsamples,
            colHeaders: ['Sample Name', 'Sequence Method', 'Biome - Environment', 'Experiment Type', 'Latitude', 'Longitude'],
            columns: [{},
                    {
                        type: 'dropdown',
                        source: ['Illumina', 'Sanger', 'Pyrosequencing', 'abi-SOLiD', 'Ion-Torrent', '454', 'other']
                    },
                    {
                        type: 'dropdown',
                        source: ['Air', 'Built environment', 'Human-associated', 'Human-oral', 'Human-skin', 'Human-vaginal', 'Microbial mat/biofilm', 'Miscellaneous natural or artificial environment', 'Plant-associated', 'Sediment', 'Soil', 'Wastewater', 'Water']
                    },
                    {
                        type: 'dropdown',
                        source: ['Metagenome', 'Amplicon 16S']
                    },
                    {},
                    {}
                ]
                /*cells: function (row, col, prop) {
                 var cellProperties = {};
                 if (row === 0) {
                   cellProperties.renderer = headerRenderer;
                 }

                 return cellProperties;
                },*/
        });


    };


    //setupNumberSamples()



    var retrieve_hst = function(x) {
        var data = []
        var totalsamples = document.getElementById("NumberSamples").value;

        x = $("#table .ht_master .wtHolder .wtHider .wtSpreader .htCore tbody tr")

        y = []
        bad_samples = 0
        for (i = 0; i < totalsamples; i++) {
            e = $(x[i]).contents()
            xsm = $(e[2]).text();
            xsm = xsm.slice(0, xsm.length - 1)
            xbi = $(e[3]).text();
            xbi = xbi.slice(0, xbi.length - 1)
            xex = $(e[4]).text();
            xex = xex.slice(0, xex.length - 1)



            if ($(e[1]).text() != "" && xsm != "" && xbi != "" && xex != "") {
                y.push([$(e[1]).text(), xsm, xbi, xex, $(e[5]).text(), $(e[6]).text()])
            } else {
                bad_samples++
            }

        }

        if (bad_samples > 0) {
            alert('Please fill all the fields in the table')
            return 'error'
        }

        return y

    }

    // inser samples information into the sql database
    $(document).on("click", "#submitMetagenome", function() {


            samples = retrieve_hst($("#table").html())

            if (samples != 'error') {




                //console.log(samples)

                $("#metadata_table").append("<div class='overlay' id='metadata_table_overlay'><i class='fa fa-refresh fa-spin'></i></div>")

                $.ajax({
                    url: machine + "insertsamples",
                    type: "POST",
                    data: JSON.stringify({
                        samples: samples,
                        pid: pid,
                        uid: uid,
                        pip: pip
                    }),
                    async: true,
                    contentType: "application/json; charset=utf-8",
                    success: function(data) {
                        // console.log(data, pip)

                        for (i = 0; i < data.samples.length; i++) {
                            $("#SampleNameSelect").append('<option value=' + data.samples[i]['c.sample_name'] + '>' + data.ids[data.samples[i].id] + '</option>')
                        }
                        $("#metadata_table_overlay").remove()
                    }

                    //get_run_table()


                });

                //$("#samplesTitle").html("Samples")
                //$("#NumberSamples").prop("disabled", true);
                //$("#buttonhide").hide();

                $("#UploadFilesMain").show()
                $("#setProjectNameinLoad").val(pid)

                $("#i1c").html('<i class="fa fa-plus">')
                get_samples_info()
                setupNumberSamples()
            }

        }

    );



    //// share project

    $(document).on("click", "#ShareProject", function() {
        $("#box_share").append("<div class='overlay' id='share_overlay'><i class='fa fa-refresh fa-spin'></i></div>")
        shared_users = $("#sharedUsers").val().split(/\n/)
            //console.log(shared_users)

        $.ajax({
            url: machine + "ShareProject",
            type: "POST",
            async: true,
            data: JSON.stringify({
                users: shared_users,
                pid: pid
            }),
            contentType: "application/json; charset=utf-8",
            success: function(x) {
                $("#share_overlay").remove()
            }
        });

    });


    //// make public

    $(document).on("click", "#makePublic", function() {

        $("#box_make_public").append("<div class='overlay' id='make_public_overlay'><i class='fa fa-refresh fa-spin'></i></div>")
        cmd = 'UPDATE project SET project_short_description="unlock"  WHERE project_id="' + pid + '"'

        $.ajax({
            url: machine + "consult",
            type: "POST",
            async: true,
            data: JSON.stringify({
                sql: cmd
            }),
            contentType: "application/json; charset=utf-8",
            success: function(x) {
                $("#make_public_overlay").remove()
            }
        });

    });









    /*get raw reads file names*/
    $('#update_raw_reads').click(function() {
        $.ajax({
            type: 'POST',
            url: machine + 'get_raw_reads_names',
            data: JSON.stringify({
                pid: pid
            }),
            contentType: "application/json; charset=utf-8",
            async: true,
            success: function(data) {
                $("#Read1Select").html('')
                $("#Read2Select").html('')
                for (i = 0; i < data.files.length; i++) {
                    $("#Read1Select").append('<option value=' + data.files[i] + '>' + data.files[i] + '</option>')
                    $("#Read2Select").append('<option value=' + data.files[i] + '>' + data.files[i] + '</option>')
                }

            }
        }); //end ajax

    });

















































    /*Run pipeline ---- there are two options 1 is for reads mapping and 2 for metagenome assembly*/

    var submit_analysis = function(sid, read1, read2, sname) {
        var rids = get_checkbox("selectedReferenceDatasets")

        if (read1 == "" || read2 == "") {
            alert('Error: Raw reads file (*.fastq.gz) is missing')
        } else {

            $("#tab_runo_box").append("<div class='overlay' id='tab_runo_box_overlay'><i class='fa fa-refresh fa-spin'></i></div>")
            $("#tab_runo_box").css('min-width', '400px');
            $("#run_button_" + sid).prop('disabled', true)


            if (rids.length == 0) {
                alert('Please select a referece database')
                $("#RunMetaGen").disabled = false;
                $("#runstatusbar").html("")
            } else {

                rid_names = "<ul>" + get_checkbox("selectedReferenceDatasets").map(function(e, i, a) {
                    return ("<li><p>" + REFS[a[i]] + "</p></li>")
                }).join("") + "</ul>"

                msg = 'Dear MetaStorm user, <br><br>The sample <b>' + sname +
                    '</b> has been queued into the <b>MetaStorm</b> server. ' +
                    ' The time for making the analysis depends on the current web traffic and availability of the server. ' +
                    'You can check the run status on MetaStorm. Also, you will receive an email once the analisis is done.  ' +
                    '<br><br><h3>Analysis</h3> You are currently running the </b>' + pip +
                    ' Pipeline</b> with the following reference databases' + rid_names + "<br><br>Thank you<br>MetaStorm</b> Team"


                $("#runstatusbar").html(wait_bar(50))

                datasent = {
                        uid: uid,
                        pid: pid,
                        sid: sid,
                        read1: read1,
                        read2: read2,
                        pip: pip,
                        rids: rids,
                        msg: msg
                    }
                    //console.log(datasent)
                $.ajax({
                    url: machine + "RunMetaGen",
                    type: "POST",
                    async: true,
                    data: JSON.stringify(datasent),
                    contentType: "application/json; charset=utf-8",
                    success: function(dat) {



                        //console.log(dat)
                        $("#runstatusbar").html(wait_bar(100))
                        $("#runstatusbar").html = ""
                        $("#RunMetaGen").disabled = false;
                        $("#runstatusbar").html("")
                            //send_email(uid,msg,'Processing sample: '+sname)
                            //get_samples_info()


                        $("#tab_runo_box_overlay").remove()

                    }
                });

            }
        }
    }












    //load raw files















































    $(document).on("click", "#RefreshSampleTabRuno", function() {

        $.ajax({
            type: 'POST',
            url: machine + 'get_raw_reads_names',
            data: JSON.stringify({
                pid: pid
            }),
            contentType: "application/json; charset=utf-8",
            async: true,
            success: function(data) {
                $("#rawreads_list").text(data.files)
                get_run_table()
            }
        });

        //get_run_table()
        //get_samples_info()
    })




    /*****************************************************************************
                   Setup databases and pipeline options
    *****************************************************************************/

    /*1. Read matching pipeline!*/



    var get_run_table = function() {


        /// Get the raw reads


        rawreads = $("#rawreads_list").text().split(",")
            // console.log(rawreads)

        //cmd='select c.sample_id,c.sample_name, c.sample_set, c.environment, c.library_preparation, c.reads1, c.reads2, c.status from (select * from samples a inner join project_status b on a.project_id==b.project_id and a.sample_id==b.sample_id) c where project_id=="'+pid+'"'
        cmd = 'select project_id,sample_id,sample_name, pip, status, reads1, reads2 from (select * from samples a left join (select pid, sid, pip, status from jobs) b on b.sid=a.sample_id  and pip="' + pip + '") c where c.project_id="' + pid + '"'
        $.ajax({
            url: machine + "consult",
            type: "POST",
            //data: JSON.stringify({sql:'select sample_id, sample_name, sample_set, environment, library_preparation, reads1, reads2 from samples where project_id="'+pid+'"'}),
            data: JSON.stringify({
                sql: cmd
            }),
            contentType: "application/json; charset=utf-8",
            success: function(x) {
                // console.log(x)
                //alert(x.data[0])


                save_sample = function(arg) {
                    row = arg[0]
                    sample = table_samples_run.getCell(row, 0);
                    fq1 = table_samples_run.getCell(row, 1);
                    fq2 = table_samples_run.getCell(row, 2);

                    //if($(fq1).text().slice(0,-1)==""){console.log('Error: No fastq.gz file provided')}

                    submit_analysis(arg[1], $(fq1).text().slice(0, -1), $(fq2).text().slice(0, -1), $(sample).text())
                        // console.log(arg, $(sample).text(), $(fq1).text().slice(0, -1), $(fq2).text().slice(0, -1))
                }

                save_sample_2 = function(argv) {
                    console.log(argv)

                    // row = arg[0]
                    // sample = table_samples_run.getCell(row, 0);
                    // fq1 = table_samples_run.getCell(row, 1);
                    // fq2 = table_samples_run.getCell(row, 2);

                    //if($(fq1).text().slice(0,-1)==""){console.log('Error: No fastq.gz file provided')}

                    // submit_analysis(arg[1], $(fq1).text().slice(0, -1), $(fq2).text().slice(0, -1), $(sample).text())
                    // console.log(arg, $(sample).text(), $(fq1).text().slice(0, -1), $(fq2).text().slice(0, -1))
                }

                remove_sample = function(arg) {
                    $("#tab_runo_box").append("<div class='overlay' id='tab_runo_box_overlay'><i class='fa fa-refresh fa-spin'></i></div>")
                    $.ajax({
                        url: machine + "removesample",
                        type: "POST",
                        async: true,
                        data: JSON.stringify({
                            sid: arg[1],
                            pid: arg[3],
                            pip: arg[2],
                            uid: userID
                        }),
                        contentType: "application/json; charset=utf-8",
                        success: function(dat) {
                            $("#tab_runo_box_overlay").remove()
                                //console.log(dat)
                        }
                    });

                    //get_samples_info()
                    get_run_table()
                        //table_samples_run.render();
                }

                var runHTML = function(instance, td, row, col, prop, value, cellProperties) {
                    // console.log(td, row, col, prop, value)
                    // $("#table_of_samples_to_run").append(td)
                    if (value != "") {
                        value = value.split(':')
                        if (value[1] == 'done') {
                            avl = '';
                            type = 'primary'
                        } else if (value[1] == 'running' || value[1] == 'queue') {
                            // avl = 'disabled="true"';
                            avl = ''
                            type = 'primary'
                        } else {
                            avl = '';
                            type = 'primary'
                        }
                        if (value[1] == 'null') {
                            avl = '';
                            type = 'primary'
                        }
                        $(td).html('<center><button id="run_button_' + value[0] + '" class="btn btn-' + type + ' btn-xs" onclick=save_sample(["' + row + '","' + value[0] + '","' + pip + '","' + pid + '"]) ' + avl + '>Run</button> ' +
                                '<button id="run_button_' + value[0] + '" class="btn btn-' + 'danger' + ' btn-xs" onclick=remove_sample(["' + row + '","' + value[0] + '","' + pip + '","' + pid + '"]) ' + avl + '>Remove</button></center>')
                            //$(td).html("<a href="+machine+'ViewSample?sid='+value+"&pid="+pid+"&uid="+uid+"&pip="+pip+" target='_blank'>"+value+"</a>"); //empty is needed because you are rendering to an existing cell
                    }
                };


                var mate1HTML = function(instance, td, row, col, prop, value, cellProperties) {
                    Handsontable.renderers.TextRenderer.apply(this, arguments);
                    td.style.fontWeight = 'bold';
                    td.style.color = 'green';
                    td.style.background = '#CEC';
                }


                data = [] //[{ID:"ID",Name:"Sample Name",Condition:"Sequence Method",Environment:"Biome",Library:"Experiment Type",Mate1:"FastQ1",Mate2:"FastQ2"}]

                for (i = 0; i < x.data.length; i++) {

                    item = {
                        ID: x.data[i]['sample_id'] + ":" + x.data[i]['status'],
                        Sample: x.data[i]['sample_name'],
                        Mate1: x.data[i]['reads1'],
                        Mate2: x.data[i]['reads2'],
                        pip: pip,
                        pid: pid,

                        run: 0
                    }

                    // <div class="dropdown">
                    //     <button class="btn btn-primary dropdown-toggle" type="button" data-toggle="dropdown">Dropdown Example
                    //     <span class="caret"></span></button>
                    //     <ul class="dropdown-menu">
                    //     <li><a href="#">HTML</a></li>
                    //     <li><a href="#">CSS</a></li>
                    //     <li><a href="#">JavaScript</a></li>
                    //     </ul>
                    // </div>

                    $("#run_samples_tbody").append(
                        "<tr>" +
                        "<td>" + x.data[i]['sample_name'] + "</td>" +

                        // fastq1
                        "<td>" +
                        '<select class="form-control" id="selected_fq_1_sample_' + x.data[i]['sample_id'] + '">' +
                        "<option selected='selected'>" + x.data[i]['reads1'] + "</option>" +
                        "<option>" + rawreads.join("</option><option>") + "</option>" +
                        '</select>' +
                        "</td>" +

                        // fastq2
                        "<td>" +
                        '<select class="form-control" id="selected_fq_2_sample_' + x.data[i]['sample_id'] + '">' +
                        "<option selected='selected'>" + x.data[i]['reads2'] + "</option>" +
                        "<option>" + rawreads.join("</option><option>") + "</option>" +
                        '</select>' +
                        "<td>" +


                        '<button id="run_button_' + x.data[i]['sample_id'] + '" class="btn btn-' + 'primary' + ' btn-xs" onclick=save_sample_2( [' + btoa(JSON.stringify(item)) + '] ) ' + '>Run</button> ' +
                        '<button id="run_button_' + x.data[i]['sample_id'] + '" class="btn btn-' + 'danger' + ' btn-xs" onclick=remove_sample_2(["' + i + '","' + x.data[i]['sample_id'] + '","' + pip + '","' + pid + '"]) ' + '>Remove</button>' +
                        "</td>" +
                        "</tr>"
                    )

                    data.push(item)
                }

                if (x.data.length == 1) {
                    for (i = 0; i < 10; i++) {
                        item = {
                            ID: '',
                            Sample: '',
                            Mate1: '',
                            Mate2: ''
                        }
                        data.push(item)
                    }
                }


                // console.log("DATA:", data, data.length)

                $("#run_table").html('')

                // $("#run_table").css('height','500px');
                // $("#run_table").css('width','800px');

                var container = document.getElementById('run_table');

                var table_samples_run = new Handsontable(container, {
                    data: data,
                    width: "100%",
                    //stretchH: 'all',
                    // autoWrapRow: true,
                    colHeaders: ['Sample', 'FastQ1', 'FastQ2', 'Action'],
                    rowHeaders: true,
                    columnSorting: true,
                    manualColumnResize: true,
                    // colWidths: ["20%", "30%", "30%", "20%"],
                    rowHeights: 30,
                    maxRows: data.length,
                    disableVisualSelection: true,
                    wordWrapBoolean: true,
                    manualRowResizeBoolean: true,
                    //fixedRowsTop: 1,
                    //manualColumnMove: false,
                    //manualRowMove: false,
                    columns: [{
                            data: 'Sample',
                            editor: false
                        },
                        {
                            data: 'Mate1',
                            //renderer: mate1HTML,
                            type: 'dropdown',
                            source: rawreads
                        },
                        {
                            data: 'Mate2',
                            type: 'dropdown',
                            source: rawreads
                        },
                        {
                            data: 'ID',
                            renderer: runHTML,
                            editor: false
                        },
                    ],
                    dropdownMenu: true,
                    /*cells: function (row, col, prop) {
                     var cellProperties = {};
                     if (row === 0) {
                       //cellProperties.renderer = headerRenderer;
                     }

                     return cellProperties;
                    },*/
                });





            }
        });

    }






    $.ajax({
        type: 'POST',
        url: machine + 'get_raw_reads_names',
        data: JSON.stringify({
            pid: pid
        }),
        contentType: "application/json; charset=utf-8",
        async: true,
        success: function(data) {
            $("#rawreads_list").text(data.files)
            get_run_table()
        }
    });




    /**/





};