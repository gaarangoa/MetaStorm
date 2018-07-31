window.onload = function() {
    // Project setup table

    // table with all the results from the assembly -  this is an overall of the assembly performance

    uid = urlParam('uid')
    pid = urlParam('pid')
    sid = urlParam('sid')
    pip = urlParam('pip')




    vsession(uid)

    machine = "/"
    machine_http = "/"


    // Download buttons
    $('#btn01').click(function(e) {
        e.preventDefault(); //stop the browser from following
        var rid = $("#selectDataset option:selected").val();
        window.location.href = machine_http + 'download/' + Base64.encode("Files/PROJECTS/" + pid + "/assembly/idba_ud/" + '/' + sid + "/" + "scaffold.fa");
    });

    $('#btn02').click(function(e) {
        e.preventDefault(); //stop the browser from following
        var rid = $("#selectDataset option:selected").val();
        window.location.href = machine_http + 'download/' + Base64.encode("Files/PROJECTS/" + pid + "/assembly/idba_ud/" + '/' + sid + "/" + "contig.fa");
    });

    $('#btn03').click(function(e) {
        e.preventDefault(); //stop the browser from following
        var rid = $("#selectDataset option:selected").val();
        window.location.href = machine_http + 'download/' + Base64.encode("Files/PROJECTS/" + pid + "/assembly/idba_ud/" + '/' + sid + "/" + "pred.genes.prot.fa");
    });

    $('#btn04').click(function(e) {
        e.preventDefault(); //stop the browser from following
        var rid = $("#selectDataset option:selected").val();
        window.location.href = machine_http + 'download/' + Base64.encode('Files/PROJECTS/' + pid + "/assembly/idba_ud/" + '/' + sid + "/" + "pred.genes." + rid + ".matches");
    });

    $('#btn05').click(function(e) {
        e.preventDefault(); //stop the browser from following
        var rid = $("#selectDataset option:selected").val();
        window.location.href = machine_http + 'download/' + Base64.encode('Files/PROJECTS/' + pid + "/assembly/idba_ud/" + '/' + sid + "/" + "pred.genes." + rid + ".matches.taxonomy.abundance");
    });

    $('#btn06').click(function(e) {
        e.preventDefault(); //stop the browser from following
        var rid = $("#selectDataset option:selected").val();
        window.location.href = machine_http + 'download/' + Base64.encode('Files/PROJECTS/' + pid + "/assembly/idba_ud/" + '/' + sid + "/" + "pred.genes." + rid + ".matches.taxonomy.genes.abundance");
    });





    // Download buttons
    $('#fbtn01').click(function(e) {
        e.preventDefault(); //stop the browser from following
        var rid = $("#selectFuncDataset option:selected").val();
        window.location.href = machine_http + 'download/' + Base64.encode("Files/PROJECTS/" + pid + "/assembly/idba_ud/" + '/' + sid + "/" + "scaffold.fa");
    });

    $('#fbtn02').click(function(e) {
        e.preventDefault(); //stop the browser from following
        var rid = $("#selectFuncDataset option:selected").val();
        window.location.href = machine_http + 'download/' + Base64.encode("Files/PROJECTS/" + pid + "/assembly/idba_ud/" + '/' + sid + "/" + "contig.fa");
    });

    $('#fbtn03').click(function(e) {
        e.preventDefault(); //stop the browser from following
        var rid = $("#selectFuncDataset option:selected").val();
        window.location.href = machine_http + 'download/' + Base64.encode("Files/PROJECTS/" + pid + "/assembly/idba_ud/" + '/' + sid + "/" + "pred.genes.prot.fa");
    });

    $('#fbtn04').click(function(e) {
        e.preventDefault(); //stop the browser from following
        var rid = $("#selectFuncDataset option:selected").val();
        window.location.href = machine_http + 'download/' + Base64.encode('Files/PROJECTS/' + pid + "/assembly/idba_ud/" + '/' + sid + "/" + "pred.genes." + rid + ".matches");
    });

    $('#fbtn05').click(function(e) {
        e.preventDefault(); //stop the browser from following
        var rid = $("#selectFuncDataset option:selected").val();
        window.location.href = machine_http + 'download/' + Base64.encode('Files/PROJECTS/' + pid + "/assembly/idba_ud/" + '/' + sid + "/" + "pred.genes." + rid + ".matches.function.abundance");
    });

    $('#fbtn06').click(function(e) {
        e.preventDefault(); //stop the browser from following
        var rid = $("#selectFuncDataset option:selected").val();
        window.location.href = machine_http + 'download/' + Base64.encode('Files/PROJECTS/' + pid + "/assembly/idba_ud/" + '/' + sid + "/" + "pred.genes." + rid + ".matches.function.genes.abundance");
    });





































    $('#fbtn01').click(function(e) {
        e.preventDefault(); //stop the browser from following
        var rid = $("#selectDatasetf option:selected").val();
        window.location.href = machine_http + 'Files/PROJECTS/' + pid + "/assembly/RESULTS/" + '/' + rid + ".all_samples_tree.pk.db";
    });














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

            $("#updatePdescription").html("<b>Description: </b> " + x.data[0]['project_description'] + "<br>")
            $("#updatePname").html("<b>Name: </b>" + x.data[0]['project_name'] + "<br>")
            $("#updateProjectID").html("<b>Unique ID: </b>" + pid + "<br>")
            $("#updateSampleID").html("<b>Unique ID: </b>" + sid + "<br>")
        }
    });


    $.ajax({
        url: machine + "consult",
        type: "POST",
        async: true,
        data: JSON.stringify({
            sql: 'select * from samples where sample_id="' + sid + '"'
        }),
        contentType: "application/json; charset=utf-8",
        success: function(x) {
            //console.log(x.data)
            $("#updateSampleName").html("<b>Name: </b>" + x.data[0]['sample_name'] + "<br>")
            $("#sampleHead").html(x.data[0]['sample_set'])
            $("#sfName").html(x.data[0]['sample_name'])
            $("#updateSampleBiome").html("<b>Biome: </b>" + x.data[0]['environment'] + "<br>")
            $("#updateSampleLibrary").html("<b>Library Preparation: </b>" + x.data[0]['library_preparation'] + "<br>")
            $("#updateSampleF1").html("<b>Library R1: </b>" + x.data[0]['reads1'] + "<br>")
            $("#updateSampleF2").html("<b>Library R2: </b>" + x.data[0]['reads2'] + "<br>")

        }
    });

    // get the databases for taxonomy that you have used to run

    var breakdown = function(dataset) {
        sent = {
                uid: uid,
                pid: pid,
                sid: sid,
                rid: dataset,
                pip: 'matches'
            }
            //console.log('THIS:',sent)
        $.ajax({
            url: machine + "breakdown",
            type: "POST",
            async: true,
            data: JSON.stringify(sent),
            contentType: "application/json; charset=utf-8",
            success: function(x) {
                //console.log(x)
                draw_line("#taxo_breakdown", x.matrix[2], 'Taxonomy Annotation Hits')
                draw_line("#function_breakdown", x.matrix[3], 'Functional Annotation Hits')
                if (x.matrix[0].abcdefghij) {
                    str = '<div class="info-box bg-green" style="width:50%"><span class="info-box-icon"><i class="fa fa-bookmark-o"></i></span><div class="info-box-content"><span class="info-box-text">MetaPhlAn</span><span class="info-box-number" >' + x.matrix[0].abcdefghij.Ngenes + '</span><div class="progress"><div class="progress-bar" style="width: 100%"></div></div><span class="progress-description">MetaPhlAn predicts the number of gene matches. Use this number <b>with CAUTION<b>.</span></div></div> '
                    $("#ifmetaphlan").html(str)
                        //console.log(str)
                }

            }
        });
    }


    $.ajax({
        url: machine + "consult",
        type: "POST",
        async: true,
        data: JSON.stringify({
            sql: 'select distinct c.datasets, c.reference_name, c.reference_description, c.taxofile, c.functfile from (select a.project_id, a.datasets, b.reference_name, b.reference_description, b.taxofile, b.functfile from matches a inner join reference b on a.datasets=b.reference_id and b.status="done") c where c.project_id="' + pid + '"'
        }),
        contentType: "application/json; charset=utf-8",
        success: function(x) {
            //console.log(x.data, pip, pid)
            btaxo = []
            bfunc = []

            for (i = 0; i < x.data.length; i++) {
                if (x.data[i]['c.taxofile'] != "none") {
                    $("#selectDataset").append('<option value=' + x.data[i]['c.datasets'] + '>' + x.data[i]['c.reference_description'] + '</option>')
                    $("#sdatasets").append("<b>" + x.data[i]['c.reference_name'] + ": </b>" + x.data[i]['c.reference_description'] + " <br><br>")
                    btaxo.push([x.data[i]['c.datasets'], x.data[i]['c.reference_name']])
                }
                if (x.data[i]['c.functfile'] != "none") {
                    $("#selectFuncDataset").append('<option value=' + x.data[i]['c.datasets'] + '>' + x.data[i]['c.reference_description'] + '</option>')
                    $("#fdatasets").append("<b>" + x.data[i]['c.reference_name'] + ": </b>" + x.data[i]['c.reference_description'] + " <br><br>")
                    bfunc.push([x.data[i]['c.datasets'], x.data[i]['c.reference_name']])
                }
            }

            // Here I put the information for the dataset breakdown.
            breakdown([btaxo, bfunc])

        }
    });




    // when click on visualize compute with the selected database


    $(document).on("click", "#VisualizeDBR", function() {
        $("#tree").html('')
        var rid = $("#selectDataset option:selected").val();
        //console.log(rid)
        $.ajax({
            url: machine + "get_tree",
            type: "POST",
            async: true,
            data: JSON.stringify({
                uid: uid,
                pid: pid,
                sid: sid,
                pip: "assembly",
                value: "rpkm",
                rid: rid
            }),
            contentType: "application/json; charset=utf-8",
            success: function(x) {
                console.log(x)
                ptree(x.tree, x.range, "#tree", 1, "id", 'rpkm', width = 2000, height = 525, rsize = 10, condition = "one", pip = "assembly", rid = rid, offset = 10)
                    //treeData, domain,tag,clpd,names, Pcolor='rpkm', width=3000, height=525, rsize=10, condition="one"
                set_taxonomy_small_pie_chart("Phylum")
            }
        });
    });




    $(document).on("click", "#loadFunction", function() {
        var rid = $("#selectFuncDataset option:selected").val();
        //alert([d.level,uid,pid,sid])
        sent = {
            uid: uid,
            pid: pid,
            sid: sid,
            pip: "assembly",
            rid: rid
        }
        console.log(sent)
        $.ajax({
            url: machine + "get_functional_counts",
            type: "POST",
            async: true,
            data: JSON.stringify(sent),
            contentType: "application/json; charset=utf-8",
            success: function(x) {
                //console.log(x)
                draw_pie_chart("#PieChartFunction", x.matrix, 'Function', 'pie', true)
            }
        });
    });






















    //******************************************************************************
    // plot pie
    //******************************************************************************

    var set_taxonomy_small_pie_chart = function(lid) {
        var rid = $("#selectDataset option:selected").val();
        console.log(pip)
        $.ajax({
            url: machine + "get_taxo_by_name",
            type: "POST",
            async: true,
            data: JSON.stringify({
                uid: uid,
                pid: pid,
                sid: sid,
                tid: "none",
                lid: lid,
                pip: "assembly",
                rid: rid
            }),
            contentType: "application/json; charset=utf-8",
            success: function(x) {
                console.log(x)
                draw_pie_chart("#PieChart1Taxo", x.matrix, lid, 'pie', true)
            }
        });
    }

    //******************************************************************************
    // Update plot pie
    //******************************************************************************
    $(document).on("click", "#loadTaxoLevel", function() {
        var level = $("#LevelTaxoSelect option:selected").val();
        set_taxonomy_small_pie_chart(level)
    });




    console.log(pip)













    // By default it loads the silva database

    $.ajax({
        url: machine + "get_tree",
        type: "POST",
        async: true,
        data: JSON.stringify({
            uid: uid,
            pid: pid,
            sid: sid,
            pip: "assembly",
            value: "rpkm",
            rid: "abcdefghij"
        }),
        contentType: "application/json; charset=utf-8",
        success: function(x) {
            //console.log(x)
            ptree(x.tree, x.range, "#tree", 1, "id", 'rpkm', width = 2000, height = 525, rsize = 10, condition = "one", pip = "matches", rid = "isuezrouja")
                //treeData, domain,tag,clpd,names, Pcolor='rpkm', width=3000, height=525, rsize=10, condition="one"
                //set_taxonomy_small_pie_chart("Phylum")
                //ptree(x.tree,x.range,"#tree",1,"id",'rpkm', width=2000, height=525, rsize=10, condition="one", pip="matches",rid="isuezrouja")
                //treeData, domain,tag,clpd,names, Pcolor='rpkm', width=3000, height=525, rsize=10, condition="one"
                //set_taxonomy_small_pie_chart("Phylum")
        }
    });




































    // GET LOGS AND GENERAL STATISTICS OF THE Assembly

    $.ajax({
        url: machine + "get_assembly_logs",
        type: "POST",
        async: true,
        data: JSON.stringify({
            uid: uid,
            pid: pid,
            sid: sid,
            pip: "assembly"
        }),
        contentType: "application/json; charset=utf-8",
        success: function(x) {
            //console.log(x)
            $("#sfReads").html(x.matrix.reads.toLocaleString())
            $("#sfAvgReads").html(x.matrix.avgreads.toLocaleString())
            $("#sfScaffolds").html(x.matrix.scaffolds.toLocaleString())
            $("#sfAvgScaffold").html(x.matrix.avgScaff.toLocaleString())
            $("#sfn50").html(x.matrix.n50.toLocaleString())
            $("#sfGenes").html(x.matrix.NumGenes.toLocaleString())
            $("#sfAvgGenes").html(x.matrix.avgGene.toLocaleString())
            $("#areads").html(x.matrix.alreads.toLocaleString())
            preads = 100 * x.matrix.alreads / x.matrix.reads
            $("#areadsp").html(preads.toLocaleString())
                //draw_pie_chart("#PieChartFunction",x.matrix, 'Function','pie')
        }
    });





};