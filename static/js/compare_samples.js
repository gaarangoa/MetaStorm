window.onload = function() {
    // Project setup table

    // table with all the results from the assembly -  this is an overall of the assembly performance

    uid = urlParam('uid')
    pid = urlParam('pid')
    sid = urlParam('sid')
    pip = urlParam('pip')

    vsession(uid)

    machine = "/MetaStorm/"
        //machine="/"


    // Download buttons
    $('#sqltable').click(function(e) {
        e.preventDefault(); //stop the browser from following
        var rid = $("#selectDataset option:selected").val();
        window.location.href = 'http://bioinformatics.cs.vt.edu/zhanglab/software/CMetAnn/Files/PROJECTS/' + pid + "/assembly/RESULTS/" + '/' + rid + ".all_samples_tree.pk.db";
    });

    $('#sqltablef').click(function(e) {
        e.preventDefault(); //stop the browser from following
        var rid = $("#selectDatasetf option:selected").val();
        window.location.href = 'http://bioinformatics.cs.vt.edu/zhanglab/software/CMetAnn/Files/PROJECTS/' + pid + "/assembly/RESULTS/" + '/' + rid + ".all_samples_tree.pk.db";
    });



    /*Get the user, projects and samples info*/





    $.ajax({
        url: machine + "GetAllInfo",
        type: "POST",
        data: JSON.stringify({ uid: uid }),
        async: true,
        contentType: "application/json; charset=utf-8",
        success: function(dat) {
            $("#UserName1").html(dat.uname)
            $("#userID").html(dat.uid)
            $("#UserContact").html(dat.email)



            $("#sel_categories").html(
                "<p> This tool shows up the <b>top 20 </b> categories based on their number of hits. The categories (functions) are ordered " +
                "in a descendent form. Thus, if you want to include more categories, just insert the interval to visualize in the below form. Once " +
                "you modify the interval, click on the <code>Compare</code> button </p>"
            )



        }
    });

    $.ajax({
        url: machine + "consult",
        type: "POST",
        async: true,
        data: JSON.stringify({ sql: 'select * from project where project_id="' + pid + '"' }),
        contentType: "application/json; charset=utf-8",
        success: function(x) {
            ////console.log(x)
            $("#updatePdescription").html("<b>Description: </b> " + x.data[0]['project_description'])
            $("#updatePname").html("<b>" + x.data[0]['project_name'] + "</b>")
        }
    });

    // get the databases where you have used to run
    $.ajax({
        url: machine + "consult",
        type: "POST",
        async: true,
        //data: JSON.stringify({sql:'select distinct c.datasets, c.reference_name, c.reference_description, c.taxofile, c.functfile from (select a.project_id, a.datasets, b.reference_name, b.reference_description, b.taxofile, b.functfile from '+pip+' a inner join reference b on a.datasets=b.reference_id and b.status="done") c where c.project_id="'+pid+'"'}),
        data: JSON.stringify({
            sql: 'select distinct c.datasets, c.reference_name, c.reference_description, c.taxofile, c.functfile from (select a.project_id, a.datasets, b.reference_name, b.reference_description, b.taxofile, b.functfile from ' + pip +
                ' a inner join reference b on a.datasets=b.reference_id and b.status="done") c where c.project_id="' + pid + '"'
        }),
        contentType: "application/json; charset=utf-8",
        success: function(x) {
            //console.log(x)
            for (i = 0; i < x.data.length; i++) {
                if (x.data[i]['c.taxofile'] != "none") {
                    $("#selectDataset").append('<option value=' + x.data[i]['c.datasets'] + '>' + x.data[i]['c.reference_name'] + '</option>')
                }
                if (x.data[i]['c.functfile'] != "none") {
                    $("#selectDatasetf").append('<option value=' + x.data[i]['c.datasets'] + '>' + x.data[i]['c.reference_name'] + '</option>')
                }
            }
        }
    });







    enable_st_ht = function(type, div) {
        if (type == "ht") {
            $(div + "_ht").show()
            $(div).hide()
        } else {
            $(div + "_ht").hide()
            $(div).show()
        }
    }






















































    /*get list of all samples in the projet id*/
    //cmd='select c.sample_id,c.sample_name, c.status, c.sample_set from (select * from samples a inner join project_status b on a.project_id==b.project_id and a.sample_id==b.sample_id) c where project_id=="'+pid+'"'
    cmd = 'select distinct a.sample_id sample_id, a.sample_name sample_name from (select * from samples where project_id=="' + pid + '") a inner join sample_status b on a.sample_id == b.sid and b.pip=="' + pip + '"'

    $.ajax({
        url: machine + "consult",
        type: "POST",
        async: true,
        data: JSON.stringify({ sql: cmd }),
        contentType: "application/json; charset=utf-8",
        success: function(x) {
            console.log(x)
            for (i = 0; i < x.data.length; i++) {
                //if(x.data[i]['']=="done"){
                $("#selectSampleToCompare").append('<input type="checkbox" name="selectSampleToCompare" value="' + x.data[i]['sample_id'] + "_" + x.data[i]['sample_name'] + '" checked > <b>' + x.data[i]['sample_name'] + '</b>  (' + x.data[i]['sample_id'] + ')<br>')
                    //}
            }

            $("#numSamples").html("Number of samples in this project: " + x.data.length)
            $("#sidePipeline").html(pip + " pipeline")

            $('input').iCheck({
                checkboxClass: 'icheckbox_square-blue',
                radioClass: 'iradio_square-blue',
                increaseArea: '20%' // optional
            });


        }
    });










































    /*Get combined tree when click on COMPARE*/
    $(document).on("click", "#compareSamplesButton", function() {
        var rid = $("#selectDataset option:selected").val();
        var norm = $("#selectNormalization option:selected").val();
        var minA = parseFloat($("#minA").val());
        var taxoLevel = $("#selectTaxonomyLevel option:selected").val();

        sel = get_checkbox("selectSampleToCompare")
        snm = get_checkbox_text("selectSampleToCompare")

        $("#tree").html("")
        $("#stackedplot").html("")
            //$("#stackedplot").height("600")
            //$("#stackedplot").width('auto')
            //$("#PieChart1Taxo").html("")
        sent = { uid: uid, pid: pid, sid: sel, pip: pip, rid: rid, lid: "Phylum", minA: minA, norm: norm, snames: snm }

        console.log(sent);

        // Display the tree
        $.ajax({
            url: machine + "get_all_samples_tree",
            type: "POST",
            async: true,
            data: JSON.stringify(sent),
            contentType: "application/json; charset=utf-8",
            success: function(x) {

                if (x.aid == "taxonomy") {
                    // show taxonomy relative abundance
                    display_stack_taxonomy(taxoLevel, "stack_taxo");

                    $("#tree").height("800")
                        //stk=process_stacked_from_tree(x.matrix2)
                    ptree(x.tree, [0, x.N[0].length / 2, x.N[0].length], "#tree", 1, "id", 'samples', width = 2000, height = 750, rsize = 10, condition = "one", pip = pip, rid, 10)
                }

            }
        });

        // display_stack_taxonomy("Phylum", "stack_taxo");
        // display_stack_taxonomy("Class", "stack_class");
        // display_stack_taxonomy("Order", "stack_order");
        // display_stack_taxonomy("Family", "stack_family");
        // display_stack_taxonomy("Genus", "stack_genus");
        // display_stack_taxonomy("Species", "stack_species");


    });
























    /*Get combined tree when click on COMPARE in the function tab*/
    $(document).on("click", "#compareSamplesButtonf", function() {


        var rid = $("#selectDatasetf option:selected").val();
        var minA = parseFloat($("#minA").val());
        var b = parseFloat($("#b").val());
        var e = parseFloat($("#e").val());
        sel = get_checkbox("selectSampleToCompare")
        snm = get_checkbox_text("selectSampleToCompare")
        var norm = $("#selectNormalizationF option:selected").val();



        $("#stackedplotf").html("")
        $("#stackedplot").height("600")
        $("#stackedplot").width('auto')
            //$("#PieChart1Taxo").html("")
        sent = { uid: uid, pid: pid, sid: sel, pip: pip, rid: rid, lid: "Phylum", minA: minA, norm: norm, ib: b, ie: e, snames: snm }
        console.log(sent)

        $.ajax({
            url: machine + "get_all_samples_tree",
            type: "POST",
            async: true,
            data: JSON.stringify(sent),
            contentType: "application/json; charset=utf-8",
            success: function(x) {
                console.log(x)
                    //alert(x.heatmap)
                if (x.aid == "taxonomy") {

                } else {
                    //$("#tree").attr("height","1200")
                    clsize = x.heatmap.data.feature_names.length * 10 + 200;
                    if (clsize > 1000) { clsize = 1000 }
                    //if(cl<100){clsize=300}
                    ////console.log(clsize)
                    //$("#tree").height("800")

                    clustergram("HeatMapFun", x.heatmap, clsize)
                    stk = process_stacked(x.matrix)
                    stacked("#stackedplotf", stk[1], stk[0])
                        ////console.log('done')
                    draw_table("function_table", x.table)



                }

                //treeData, domain,tag,clpd,names, Pcolor='rpkm', width=3000, height=525, rsize=10, condition="one"
                //$("#PieChart1Taxo").html("well well well")
                //set_taxonomy_small_pie_chart("Phylum")
            }
        });

    });
























    //******************************************************************************
    // UPDATE button under taxonomy ...
    //******************************************************************************
    var display_stack_taxonomy = function(level, div) {

        //var pip = $( "#selectPipeline option:selected" ).val();
        var rid = $("#selectDataset option:selected").val();
        sel = get_checkbox("selectSampleToCompare")
        var norm = $("#selectNormalization option:selected").val();
        height = $("#pie1taxomain").height()
        var minA = parseFloat($("#minA").val());

        snm = get_checkbox_text("selectSampleToCompare")

        var b2 = parseFloat($("#b2").val());
        var e2 = parseFloat($("#e2").val());

        //$("#PieChart1Taxo").height(height)
        //$("#tree").html('')
        //$("#PieChart1Taxo").html("")
        sendv = { uid: uid, pid: pid, sid: sel, pip: pip, rid: rid, lid: level, minA: minA, norm: norm, snames: snm, ib: b2, ie: e2 }
        console.log(sendv)
        $.ajax({
            url: machine + "get_all_samples_tree",
            type: "POST",
            async: true,
            data: JSON.stringify(sendv),
            contentType: "application/json; charset=utf-8",
            success: function(x) {
                console.log(x)
                    //$("#tree").height("600")
                    //ptree(x.tree,[0,pip.length/2,pip.length],"#tree",1,"id",'samples',width=3000, height=525, rsize=10, condition="mult", pip, rid)
                cl = x.heatmap.data.feature_names.length
                clsize = 10 * 10 + 200;
                //console.log(x.heatmap)
                if (clsize > 1000) { clsize = 1500 }
                if (cl < 100) { clsize = 800 }
                clustergram(div + "_ht", x.heatmap, clsize)

                stk = process_stacked(x.matrix)
                    //console.log(stk)
                stacked("#" + div, stk[1], stk[0])
                    //draw_heat_map("#PieChart1Taxo",x.data,x.xlabs, x.ylabs,250,0.1,1)
            }
        });
    }




    //******************************************************************************
    // when clicking on any node ... i need to update this!!!
    //******************************************************************************
    $(document).on("click", "#loadHeatMapLevel2", function() {

        var pip = $("#selectPipeline option:selected").val();
        var rid = $("#selectDataset option:selected").val();
        sel = get_checkbox("selectSampleToCompare")
        height = $("#pie1taxomain").height()
        var lid = $("#LevelTaxoSelect option:selected").val();
        //$("#PieChart1Taxo").height(height)

        $("#PieChart1Taxo").html("")
        $.ajax({
            url: machine + "get_all_samples_tree",
            type: "POST",
            async: true,
            data: JSON.stringify({ uid: uid, pid: pid, sid: sel, value: pip, rid: rid, lid: lid }),
            contentType: "application/json; charset=utf-8",
            success: function(x) {
                //alert(x.data)
                //ptree(x.tree,[0,pip.length/2,pip.length],"#tree",1,"id",'samples')

                draw_heat_map("#PieChart1Taxo", x.data, x.xlabs, x.ylabs, height - 120)

                //alert(x.ylabs)

                //$("#PieChart1Taxo").html("well well well")
                //set_taxonomy_small_pie_chart("Phylum")
            }
        });

    });


































};