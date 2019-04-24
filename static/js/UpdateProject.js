window.onload = function() {
    // Project setup table
    // table with all the results from the assembly -  this is an overall of the assembly performance


    var machine = Parameters.host;
    var upload_dir = Parameters.upload_dir;

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

            // render the metadata
            // setupNumberSamples()

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

    var add_table_samples = function(data) {
        var content = document.querySelector("#app_2_content")
        content.innerHTML = `
            <div class="col-md-12 no-gutters">
                <div class="box box-solid">
                    <table class="table table-hover">
                        <thead>
                            <tr>
                                <th scope="col">Identifier</th>
                                <th scope="col">Sample Name</th>
                                <th scope="col">Library</th>
                                <th scope="col">Environment</th>
                                <th scope="col">Fordward</th>
                                <th scope="col">Reverse</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="sample in samples">
                                <td>
                                    <a v-bind:href="sample.link" target="_blank">
                                        {{ sample.ID }}
                                    </a>
                                </td>
                                <td> {{ sample.Name }} </td>
                                <td> {{ sample.Library }} </td>
                                <td> {{ sample.Environment }} </td>
                                <td> {{ sample.Mate1 }} </td>
                                <td> {{ sample.Mate2 }} </td>
                            </tr>
                        </tbody>
                    </table>

                </div>
            </div>
            <br><br><br>
        `
        data = data.map(e => {
            e.link = "/metastorm2/ViewSample?sid=" + e.ID + '&pid=' + pid + '&uid=' + uid + '&pip=' + pip;
            return e;
        })

        var app2 = new Vue({
            el: '#app-2',
            data: {
                samples: data
            }
        })
    }



    /*Run pipeline ---- there are two options 1 is for reads mapping and 2 for metagenome assembly*/

    var submit_analysis = function(sample) {
        var rids = get_checkbox("selectedReferenceDatasets")

        if (sample.selected_fq_1 == "" || sample.selected_fq_2 == "") {
            alert('Error: Raw reads file (*.fastq.gz) is missing')
        } else {

            $("#tab_runo_box").append("<div class='overlay' id='tab_runo_box_overlay'><i class='fa fa-refresh fa-spin'></i></div>")
            $("#tab_runo_box").css('min-width', '400px');
            $("#run_button_" + sample.ID).prop('disabled', true)


            if (rids.length == 0) {
                alert('Please select a referece database')
                $("#RunMetaGen").disabled = false;
                $("#runstatusbar").html("")
            } else {

                rid_names = "<ul>" + get_checkbox("selectedReferenceDatasets").map(function(e, i, a) {
                    return ("<li><p>" + REFS[a[i]] + "</p></li>")
                }).join("") + "</ul>"

                msg = 'Dear MetaStorm user, <br><br>The sample <b>' + sample.Name +
                    '</b> has been queued into the <b>MetaStorm</b> server. ' +
                    ' The time for making the analysis depends on the current web traffic and availability of the server. ' +
                    'You can check the run status on MetaStorm. Also, you will receive an email once the analisis is done.  ' +
                    '<br><br><h3>Analysis</h3> You are currently running the </b>' + sample.pip +
                    ' Pipeline</b> with the following reference databases' + rid_names + "<br><br>Thank you<br>MetaStorm</b> Team"


                $("#runstatusbar").html(wait_bar(50))

                datasent = {
                    uid: sample.uid,
                    pid: sample.pid,
                    sid: sample.ID,
                    read1: sample.selected_fq_1,
                    read2: sample.selected_fq_2,
                    pip: sample.pip,
                    rids: rids,
                    msg: msg
                }
                console.log('Sending: ', datasent)
                $.ajax({
                    url: machine + "RunMetaGen",
                    type: "POST",
                    async: true,
                    data: JSON.stringify(datasent),
                    contentType: "application/json; charset=utf-8",
                    success: function(dat) {

                        console.log('Receiving:', dat);
                        $("#runstatusbar").html(wait_bar(100))
                        $("#runstatusbar").html = ""
                        $("#RunMetaGen").disabled = false;
                        $("#runstatusbar").html("")
                        send_email(sample.uid, msg, 'Processing sample: ' + sample.Name)
                        get_samples_info()


                        $("#tab_runo_box_overlay").remove()

                    }
                });

            }
        }
    }

    destroy_sample = function(sample) {

        $.ajax({
            url: machine + "removesample",
            type: "POST",
            async: true,
            data: JSON.stringify({
                sid: sample.ID,
                pid: sample.pid,
                pip: sample.pip,
                uid: sample.uid
            }),
            contentType: "application/json; charset=utf-8",
            success: function(dat) {

            }
        });
    }

    var add_table_run_samples = function(data) {
        var content = document.querySelector("#app_table_run_sample_content")
        content.innerHTML = `
            <div class="col-md-12">
                <button v-on:click="update_reads()" style="width: 20%" class="btn btn-success btn-xs"><strong>Update Raw Reads List</strong></button>
                <br><br><br>
            </div>
            <div class="col-md-4" v-for="(sample, index) in samples">
                <div class="box box-solid">
                    <div class="box-body">

                        <dl class="">
                            <dt>Sample Name: {{ sample.Name }}</dt>
                            <hr>
                            <dt>Forward Pair: </dt>
                            <dd>
                                <select class="form-control" v-bind:id="sample.fq_1_id" v-model="sample.selected_fq_1">
                                    <option selected="selected">{{ sample.Mate1 }}</option>
                                    <option v-for="read_file in all_read_files">
                                        {{read_file}}
                                    </option>
                                </select>
                            </dd>
                            <dt>Reverse Pair: </dt>
                            <dd>
                                <select class="form-control" v-bind:id="sample.fq_2_id" v-model="sample.selected_fq_2">
                                    <option selected="selected">{{ sample.Mate2 }}</option>
                                    <option v-for="read_file in all_read_files">
                                        {{read_file}}
                                    </option>
                                </select>
                            </dd>
                        </dl>

                        <hr>

                        <button  v-on:click="save_sample_vue(index)" style="width: 100%" class="btn btn-primary btn-xs"><strong>Run</strong></button>
                        <button  v-on:click="remove_sample_vue(index)" style="width: 100%" class="btn btn-warning btn-xs"><strong>Remove</strong></button>

                    </div>
                </div>
            </div>

        `


        var run_sample_section = new Vue({
            el: '#app_table_run_sample',
            data: {
                samples: [],
                all_read_files: [],
            },
            methods: {
                save_sample_vue: function(index) {
                    var sample = this.samples[index];
                    console.log(sample);
                    submit_analysis(sample);
                },

                remove_sample_vue: function(index) {
                    sample = this.samples[index];
                    destroy_sample(sample);
                    this.samples.splice(index, 1);
                },
                update_reads: function() {
                    fetch(machine + 'get_raw_reads_names', {
                            method: 'post',
                            headers: {
                                'Accept': 'application/json',
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({
                                pid: pid
                            })
                        })
                        .then(response => response.json())
                        .then(json => {
                            // console.log(json.files);
                            this.all_read_files = json.files;
                        })
                }

            },
            created() {
                fetch(machine + 'get_raw_reads_names', {
                        method: 'post',
                        headers: {
                            'Accept': 'application/json',
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            pid: pid
                        })
                    })
                    .then(response => response.json())
                    .then(json => {

                        this.all_read_files = json.files;
                        this.samples = data.map(e => {
                            e.link = "/ViewSample?sid=" + e.ID + '&pid=' + pid + '&uid=' + uid + '&pip=' + pip;
                            e.fq_1_id = "selected_fq_1_sample_" + e.ID;
                            e.fq_2_id = "selected_fq_2_sample_" + e.ID;
                            e.run_button_id = "run_button_" + e.ID;
                            e.remove_button_id = "remove_button_" + e.ID;
                            e.selected_fq_1 = e.Mate1;
                            e.selected_fq_2 = e.Mate2;
                            e.pid = pid;
                            e.uid = uid;
                            e.pip = pip;

                            return e;
                        });

                        console.log(this.samples);
                    })
            }
        })
    }


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


                add_table_samples(data);
                add_table_run_samples(data);


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

    // document.getElementById("setup_metadata_tab").onclick = function(e) {
    //     setupNumberSamples();
    // };

    var setupNumberSamples = function() {

        $('#table').html('')
            // $('#table').css('min-width', '800px');
            // $('#table').css('height', '500px');
        var container = document.getElementById('table'),
            hot;
        var totalsamples = document.getElementById("NumberSamples").value;

        matrix = [
                ['', '', '', '', '0', '0']
            ] //[['Sample Name','Sequence Method', 'Biome', 'Experiment Type', 'Latitude', 'Longitude']]
        for (var i = 1; i < totalsamples; i++) {
            matrix.push(['', '', '', '', '0', '0'])
        }

        hot = new Handsontable(container, {
            data: matrix,
            // colWidths: 150,
            // contextMenu: true,
            //autoWrapCol: true,
            // colHeaders: true,
            rowHeaders: true,
            //columnSorting: false,
            // stretchH: 'all',
            // width: 800,
            // maxRows: totalsamples,
            colHeaders: ['Sample Name', 'Sequence Method', 'Biome - Environment', 'Experiment Type', 'Latitude', 'Longitude'],
            columns: [{},
                    {
                        type: 'dropdown',
                        source: ['Illumina', 'Sanger', 'Pyrosequencing', 'abi-SOLiD', 'Ion-Torrent', '454', 'other']
                    },
                    {
                        type: 'autocomplete',
                        source: ['Air', 'Built environment', 'Human-associated', 'Human-oral', 'Human-skin', 'Human-vaginal', 'Microbial mat/biofilm', 'Miscellaneous natural or artificial environment', 'Plant-associated', 'Sediment', 'Soil', 'Wastewater', 'Water'],
                        strict: false,
                        visibleRows: 20,
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

                // $("#metadata_table").append("<div class='overlay' id='metadata_table_overlay'><i class='fa fa-refresh fa-spin'></i></div>")

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
                        setupNumberSamples();
                        alert('The metadata has been stored.');
                        // $("#metadata_table_overlay").remove()
                    }

                    //get_run_table()


                });

                $("#samplesTitle").html("Samples")
                    //$("#NumberSamples").prop("disabled", true);
                $("#buttonhide").hide();

                $("#UploadFilesMain").show()
                $("#setProjectNameinLoad").val(pid)

                $("#i1c").html('<i class="fa fa-plus">')
                get_samples_info()
                    // setupNumberSamples()
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
                alert('Project has been shared with: ' + shared_users);
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
                alert('The project has been open to public')
                $("#make_public_overlay").remove()
            }
        });

    });



































































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
                    // get_run_table()
            }
        });

        //get_run_table()
        //get_samples_info()
    })






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
                // get_run_table()
        }
    });




    /**/





};