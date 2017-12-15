window.onload = function() {
    // Project setup table

    // table with all the results from the assembly -  this is an overall of the assembly performance

    uid = urlParam('uid')
    pid = urlParam('pid')
    sid = urlParam('sid')
    pip = urlParam('pip')






    document.getElementById('download_tree').onclick = function() {

        var svgElement = $('#tree svg')[0];
        var simg = new Simg(svgElement);
        // Replace the current SVG with an image version of it.
        simg.replace();
        // And trigger a download of the rendered image.
        simg.download();
    };

    vsession(uid)

    machine = "/MetaStorm/"
    machine_http = "http://bench.cs.vt.edu/MetaStorm/"


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
            $("#which_pipeline").text(pip + " pipeline")
            $("#which_pipeline2").text(pip + " pipeline")
            $("#sidePipeline").text(pip + " pipeline")
        }
    });

    $.ajax({
        url: machine + "consult",
        type: "POST",
        async: true,
        data: JSON.stringify({ sql: 'select * from project where project_id="' + pid + '"' }),
        contentType: "application/json; charset=utf-8",
        success: function(x) {

            $("#updatePdescription").html(x.data[0]['project_description'] + "<br>")
            $("#updatePname").html(x.data[0]['project_name'] + "<br>")
            $("#updateProjectID").html("<b>Unique ID: </b>" + pid + "<br>")
            $("#updateSampleID").html("<b>Unique ID: </b>" + sid + "<br>")
        }
    });


    $.ajax({
        url: machine + "consult",
        type: "POST",
        async: true,
        data: JSON.stringify({ sql: 'select * from samples where sample_id="' + sid + '"' }),
        contentType: "application/json; charset=utf-8",
        success: function(x) {
            ////console.log(x.data)
            $("#updateSampleName").html('Sample: ' + x.data[0]['sample_name'] + "<br>")
            $("#sampleHead").html(x.data[0]['sample_set'])
            $("#sfName").html(x.data[0]['sample_name'])
            $("#updateSampleBiome").html(x.data[0]['environment'])
            $("#updateSampleLibrary").html(x.data[0]['library_preparation'])
            $("#updateSampleF1").append('<a href="#" onclick="download_f([1, pid,' + "'" + x.data[0].reads1 + "'" + ', sid, uid, 1])" ><i class="fa fa-fw fa-download"></i><b>FastQ1 </b></a><br>')
            $("#updateSampleF2").append('<a href="#" onclick="download_f([1, pid,' + "'" + x.data[0].reads2 + "'" + ', sid, uid, 2])" ><i class="fa fa-fw fa-download"></i><b>FastQ2 </b></a><br>')


            if (pip == "assembly") {
                $("#Dscaffolds").append('<a href="#" onclick="download_f([2, pid,' + "'scaffolds.fa'" + ', sid, uid, 1])" ><i class="fa fa-fw fa-download"></i><b>Scaffolds </b></a><br>')
                $("#Dgenes").append('<a href="#" onclick="download_f([3, pid,' + "'pred.genes.fa'" + ', sid, uid, 2])" ><i class="fa fa-fw fa-download"></i><b>Genes </b></a><br>')
            }


        }
    });

    // get the databases for taxonomy that you have used to run


    download_f = function(x) {

        var rid = $("#selectFuncDataset option:selected").val();
        arc_pro = "/groups/metastorm_cscee/MetaStorm/Files/PROJECTS/"

        if (x[0] == 1) { // code 1: fastq files
            file = arc_pro + x[1] + "/READS/" + x[2]
            $("#updateSampleF" + x[5]).append("<div class='overlay' id='updateSampleF" + x[5] + "_overlay'><i class='fa fa-refresh fa-spin'></i></div>")

        }

        if (x[0] == 2) { // scaffolds: fasta files
            file = arc_pro + x[1] + "/assembly/idba_ud/" + sid + "/scaffold.fa"
            $("#Dscaffolds").append("<div class='overlay' id='Dscaffolds_overlay'><i class='fa fa-refresh fa-spin'></i></div>")
        }

        if (x[0] == 3) { // genes: fasta files
            file = arc_pro + x[1] + "/assembly/idba_ud/" + sid + "/pred.genes.nucl.fa"
            $("#Dgenes").append("<div class='overlay' id='Dgenes_overlay'><i class='fa fa-refresh fa-spin'></i></div>")
        }

        if (x[0] == 4) { // alignment: Assembly
            file = arc_pro + x[1] + "/assembly/idba_ud/" + sid + "/pred.genes." + rid + '.matches'
            console.log(file);
            $("#download_function_alignment").append("<div class='overlay' id='Dgenes_overlay'><i class='fa fa-refresh fa-spin'></i></div>")
        }

        if (x[0] == 5) { // alignment: read-matching
            file = arc_pro + x[1] + "/matches/" + sid + "/alignment." + rid + '.matches'
            console.log(file);
            $("#Dgenes").append("<div class='overlay' id='Dgenes_overlay'><i class='fa fa-refresh fa-spin'></i></div>")
        }

        $.ajax({
            url: machine + "download_files",
            type: "POST",
            async: true,
            data: JSON.stringify({ file: file, uid: uid, sid: sid, pid: pid, name: x[2] }),
            contentType: "application/json; charset=utf-8",
            success: function(data) {

                console.log(data)

                //e.preventDefault();  //stop the browser from following
                window.location.href = machine_http + 'download/' + Base64.encode(data.fo);
                $("#updateSampleF" + x[5] + "_overlay").remove()
                $("#Dscaffolds_overlay").remove()
                $("#Dgenes_overlay").remove()
                    //alert()

            }
        });


    }




    var breakdown = function(dataset) {
        sent = { uid: uid, pid: pid, sid: sid, rid: dataset, pip: pip }
            ////console.log(sent)
            ////console.log('THIS:',sent)
        $.ajax({
            url: machine + "breakdown",
            type: "POST",
            async: true,
            data: JSON.stringify(sent),
            contentType: "application/json; charset=utf-8",
            success: function(x) {
                console.log('breakdown', x)
                total_hits = x.matrix[4]


                $("#blue_text_box").prepend(['<h3>Metagenome Summary</h3><p>' +
                    x.matrix[5] + '</p>'
                ])


                x.matrix[2].forEach(function(item, index) {
                    $("#databases_run").append(html_progress_bar(item[0], item[1], total_hits, 100 * item[1] / total_hits, 'black', item[2]))

                    Tipped.create('#tp_' + item[2], function(element) {
                        return {
                            title: item[0],
                            content: '<div style="width:300px; min-height:50px; max-height:200px; overflow: auto">' + item[3] + '</div>'
                        };
                    }, {
                        skin: 'red'
                    });

                })

                x.matrix[3].forEach(function(item, index) {
                    $("#databases_run_func").append(html_progress_bar(item[0], item[1], total_hits, 100 * item[1] / total_hits, 'blue', item[2]))

                    Tipped.create('#tp_' + item[2], function(element) {
                        return {
                            title: item[0],
                            content: '<div style="width:300px; min-height:50px; max-height:200px; overflow: auto">' + item[3] + '</div>'
                        };
                    }, {
                        skin: 'red'
                    });


                })
            }
        });
    }





    /// get the datasets that have been used in the study

    $.ajax({
        url: machine + "consult",
        type: "POST",
        async: true,
        data: JSON.stringify({
            sql: 'select distinct c.datasets,' +
                'c.reference_name, c.reference_description, c.reference_id, ' +
                'c.taxofile, c.functfile from (select a.sample_id, a.project_id, ' +
                'a.datasets, b.reference_name, b.reference_id, b.reference_description, ' +
                'b.taxofile, b.functfile from ' + pip + ' a inner join ' +
                'reference b on a.datasets=b.reference_id and b.status="done") c ' +
                'where c.sample_id="' + sid + '" order by c.reference_name'
        }),
        contentType: "application/json; charset=utf-8",
        success: function(x) {
            //console.log(x)


            btaxo = []
            bfunc = []

            for (i = 0; i < x.data.length; i++) {
                if (x.data[i]['c.taxofile'] != "none") {
                    $("#selectDataset").append('<option value=' + x.data[i]['c.datasets'] + '>' + x.data[i]['c.reference_name'] + '</option>')
                        //$("#sdatasets").append("<b>"+x.data[i]['c.reference_name']+": </b>" + x.data[i]['c.reference_description'] + " <br><br>")
                    btaxo.push([x.data[i]['c.datasets'], x.data[i]['c.reference_name'], x.data[i]['c.reference_description'], x.data[i]['c.reference_id']])
                }
                if (x.data[i]['c.functfile'] != "none") {
                    $("#selectFuncDataset").append('<option value=' + x.data[i]['c.datasets'] + '>' + x.data[i]['c.reference_name'] + '</option>')
                        //$("#fdatasets").append("<b>"+x.data[i]['c.reference_name']+": </b>" + x.data[i]['c.reference_description'] + " <br><br>")
                    bfunc.push([x.data[i]['c.datasets'], x.data[i]['c.reference_name'], x.data[i]['c.reference_description'], x.data[i]['c.reference_id']])
                }
            }

            // Here I put the information for the dataset breakdown.
            breakdown([btaxo, bfunc])

        }
    });



    /// TAXONOMY TAB
    // when click on visualize compute with the selected database

    $(document).on("click", "#VisualizeDBR", function() {
        $("#tree").html('')
        var rid = $("#selectDataset option:selected").val();
        ////console.log(rid)
        $.ajax({
            url: machine + "get_tree",
            type: "POST",
            async: true,
            data: JSON.stringify({ uid: uid, pid: pid, sid: sid, pip: pip, value: "rpkm", rid: rid }),
            contentType: "application/json; charset=utf-8",
            success: function(x) {
                console.log(x)


                //treeData, domain,tag,clpd,names, Pcolor='rpkm', width=3000, height=525, rsize=10, condition="one"
                set_taxonomy_small_pie_chart("Domain", '#tdomain')
                set_taxonomy_small_pie_chart("Phylum", '#tx2')
                set_taxonomy_small_pie_chart("Class", '#tx3')
                set_taxonomy_small_pie_chart("Order", '#tx4')
                set_taxonomy_small_pie_chart("Family", '#tx5')
                set_taxonomy_small_pie_chart("Genus", '#tx6')

                ptree(x.tree, x.range, "#tree", 1, "id", 'rpkm', width = 1500, height = 525, rsize = 10, condition = "one", pip = pip, rid = rid, offset = 10)

            }
        });
    });




    $(document).on("click", "#loadFunction", function() {
        var rid = $("#selectFuncDataset option:selected").val();
        //alert([d.level,uid,pid,sid])
        sent = { uid: uid, pid: pid, sid: sid, pip: pip, rid: rid }
            //console.log(sent)
        $.ajax({
            url: machine + "get_functional_counts",
            type: "POST",
            async: true,
            data: JSON.stringify(sent),
            contentType: "application/json; charset=utf-8",
            success: function(x) {
                console.log(x)
                individual_samples(x.m2)
                    //draw_pie_chart("#PieChartFunction",x.matrix, 'Function','pie',true)
            }
        });
    });



    //******************************************************************************
    // plot pie
    //******************************************************************************

    var set_taxonomy_small_pie_chart = function(lid, div) {
        var rid = $("#selectDataset option:selected").val();
        //console.log(pip)
        $.ajax({
            url: machine + "get_taxo_by_name",
            type: "POST",
            async: true,
            data: JSON.stringify({ uid: uid, pid: pid, sid: sid, tid: "none", lid: lid, pip: pip, rid: rid }),
            contentType: "application/json; charset=utf-8",
            success: function(x) {
                ////console.log(x)
                draw_pie_chart(div, x.matrix, lid, 'pie', true)
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








































    if (pip == 'assembly') {

        $("#buttonsF").html(["<p>" +
            //"<a id='fbtn01' download='counts'><button class='btn bg-maroon btn-flat margin'>Scaffolds</button></a>"+
            //"<a id='fbtn02' download='counts'><button class='btn bg-purple btn-flat margin'>Contigs</button></a>"+
            //"<a id='fbtn03' download='counts'><button class='btn bg-olive btn-flat margin'>Predicted Genes</button></a>"+
            //"<a id='fbtn04' download='counts'><button class='btn bg-orange btn-flat margin'>Gene Matches</button></a>"+
            "<a id='fbtn05' download='counts'><button class='btn bg-navy btn-flat margin'>Functional Abundance</button></a>" +
            "<a id='fbtn06' download='counts'><button class='btn bg-purple btn-flat margin'>Functional Gene Abundance</button></a>" +
            "</p>"
        ])

        $("#buttonsT").html(["<p>" +
            //"<a id='btn01' download='counts'><button class='btn bg-maroon btn-flat margin'>Scaffolds</button></a>"+
            //"<a id='btn02' download='counts'><button class='btn bg-purple btn-flat margin'>Contigs</button></a>"+
            //"<a id='btn03' download='counts'><button class='btn bg-olive btn-flat margin'>Predicted Genes</button></a>"+
            //"<a id='btn04' download='counts'><button class='btn bg-orange btn-flat margin'>Gene Matches</button></a>"+
            "<a id='btn05' download='counts'><button class='btn bg-navy btn-flat margin'>Taxonomy Abundance</button></a>" +
            "<a id='btn06' download='counts'><button class='btn bg-purple btn-flat margin'>Gene Abundance</button></a>" +
            "</p>"
        ])


        $('#btn05').click(function(e) {
            e.preventDefault(); //stop the browser from following
            var rid = $("#selectDataset option:selected").val();
            window.location.href = machine_http + 'download/' + Base64.encode('Files/PROJECTS/' + pid + "/assembly/idba_ud/" + '/' + sid + "/" + "pred.genes." + rid + ".matches.taxonomy.abundance.rpkm");
        });

        $('#btn06').click(function(e) {
            e.preventDefault(); //stop the browser from following
            var rid = $("#selectDataset option:selected").val();
            window.location.href = machine_http + 'download/' + Base64.encode('Files/PROJECTS/' + pid + "/assembly/idba_ud/" + '/' + sid + "/" + "pred.genes." + rid + ".matches.taxonomy.genes.abundance.rpkm");
        });

        $('#download_function_alignment').click(function(e) {
            e.preventDefault(); //stop the browser from following
            var rid = $("#selectFuncDataset option:selected").val();
            download_f([4, pid, sid + '.' + rid + '.alignment.txt', sid, uid, 2])
        });


        $('#fbtn05').click(function(e) {
            e.preventDefault(); //stop the browser from following
            var rid = $("#selectFuncDataset option:selected").val();
            window.location.href = machine_http + 'download/' + Base64.encode('Files/PROJECTS/' + pid + "/assembly/idba_ud/" + '/' + sid + "/" + "pred.genes." + rid + ".matches.function.abundance.rpkm");
        });

        $('#fbtn06').click(function(e) {
            e.preventDefault(); //stop the browser from following
            var rid = $("#selectFuncDataset option:selected").val();
            window.location.href = machine_http + 'download/' + Base64.encode('Files/PROJECTS/' + pid + "/assembly/idba_ud/" + '/' + sid + "/" + "pred.genes." + rid + ".matches.function.genes.abundance.rpkm");
        });


        $('#fbtn01').click(function(e) {
            e.preventDefault(); //stop the browser from following
            var rid = $("#selectDatasetf option:selected").val();
            window.location.href = machine_http + 'Files/PROJECTS/' + pid + "/assembly/RESULTS/" + '/' + rid + ".all_samples_tree.pk.db";
        });






        // GET LOGS AND GENERAL STATISTICS OF THE Assembly

        $.ajax({
            url: machine + "get_assembly_logs",
            type: "POST",
            async: true,
            data: JSON.stringify({ uid: uid, pid: pid, sid: sid, pip: pip }),
            contentType: "application/json; charset=utf-8",
            success: function(x) {

                $("#blue_text_box").html(['<p style="color:black">The dataset <b id="sfName"></b> contains <b id="sfReads"></b> high quality sequences for assembly (idba-fq2fa preprocess). Reads have an average length of ' +
                    '<b id="sfAvgReads"></b> bps. <br><br> Reads are assembled using <a target="_blank" href="http://i.cs.hku.hk/~alse/hkubrg/projects/idba_ud/"><b>IDBA-UD</b></a> software. <br> In total ' +
                    '<b id="areads"></b> reads were assembled (<b id="areadsp"></b>%) forming a total of <b id="sfScaffolds"> ' +
                    '</b> scaffolds with an average length of <b id="sfAvgScaffold"></b> bps, and n50 of <b id="sfn50"></b> ' +
                    'bps. A total of <b id="sfGenes"></b> genes were predicted from the assembled sequeces using the <a href="http://prodigal.ornl.gov/" target="_blank"><b>PRODIGAL</b></a> ' +
                    'software. The average length of the genes is <b id="sfAvgGenes"></b> bp. </p>'
                ])

                console.log(x)
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



    } else {



        $.ajax({
            url: machine + "get_matches_logs",
            type: "POST",
            async: true,
            data: JSON.stringify({ uid: uid, pid: pid, sid: sid, pip: pip }),
            contentType: "application/json; charset=utf-8",
            success: function(x) {
                console.log('this matrix', x)


                ////console.log(x)
                $("#sfReads").html(x.matrix.rawReads.toLocaleString())
                $("#hqReads").html(x.matrix.hqReads.toLocaleString())
                    //draw_pie_chart("#PieChartFunction",x.matrix, 'Function','pie')
            }
        });




        $("#buttonsF").html(["<p>" +
            //"<a id='fbtn01' download='counts'><button class='btn bg-maroon btn-flat margin'>Alignment</button></a>"+
            "<a id='fbtn02' download='counts'><button class='btn bg-navy btn-flat margin'>Functional Annotation (16s normalized)</button></a>" +
            "<a id='fbtn03' download='counts'><button class='btn bg-navy btn-flat margin'>Functional Annotation (rpkm normalized)</button></a>" +
            "<a id='fbtn04' download='counts'><button class='btn bg-purple btn-flat margin'>Matched Genes (16s normalized)</button></a>" +
            "<a id='fbtn05' download='counts'><button class='btn bg-purple btn-flat margin'>Matched Genes (rpkm normalized)</button></a>" +
            "</p>"
        ])


        /*$('#fbtn01').click(function(e) {
           e.preventDefault();  //stop the browser from following
           var rid = $( "#selectFuncDataset option:selected" ).val();
           window.location.href = machine_http+'download/'+Base64.encode("Files/PROJECTS/"+pid+"/matches/"+'/'+sid+"/"+"alignment."+rid+".matches");
        });*/

        $('#fbtn02').click(function(e) {
            e.preventDefault(); //stop the browser from following
            var rid = $("#selectFuncDataset option:selected").val();
            window.location.href = machine_http + 'download/' + Base64.encode("Files/PROJECTS/" + pid + "/matches/" + '/' + sid + "/" + "alignment." + rid + ".matches.function.abundance.16s");
        });

        $('#fbtn03').click(function(e) {
            e.preventDefault(); //stop the browser from following
            var rid = $("#selectFuncDataset option:selected").val();
            window.location.href = machine_http + 'download/' + Base64.encode("Files/PROJECTS/" + pid + "/matches/" + '/' + sid + "/" + "alignment." + rid + ".matches.function.abundance.rpkm");
        });

        $('#fbtn04').click(function(e) {
            e.preventDefault(); //stop the browser from following
            var rid = $("#selectFuncDataset option:selected").val();
            window.location.href = machine_http + 'download/' + Base64.encode("Files/PROJECTS/" + pid + "/matches/" + sid + '/' + "alignment." + rid + ".matches.function.genes.abundance.16s");
        });

        $('#fbtn05').click(function(e) {
            e.preventDefault(); //stop the browser from following
            var rid = $("#selectFuncDataset option:selected").val();
            window.location.href = machine_http + 'download/' + Base64.encode("Files/PROJECTS/" + pid + "/matches/" + sid + '/' + "alignment." + rid + ".matches.function.genes.abundance.rpkm");
        });

        $('#download_function_alignment').click(function(e) {
            e.preventDefault(); //stop the browser from following
            var rid = $("#selectFuncDataset option:selected").val();
            download_f([5, pid, sid + '.' + rid + '.alignment.txt', sid, uid, 2])
        });

        $("#buttonsT").html(["<p>" +
            //"<a id='btn01' download='counts'><button class='btn bg-maroon btn-flat margin'>Alignment</button></a>"+
            "<a id='btn02' download='counts'><button class='btn bg-navy btn-flat margin'>Taxonomy Annotation</button></a>" +
            "<a id='btn03' download='counts'><button class='btn bg-purple btn-flat margin'>Matched Genes</button></a>" +
            "</p>"
        ])



        /*$('#btn01').click(function(e) {
      e.preventDefault();  //stop the browser from following
      var rid = $( "#selectDataset option:selected" ).val();
      window.location.href = machine_http+'download/'+Base64.encode("Files/PROJECTS/"+pid+"/matches/"+'/'+sid+"/"+"alignment."+rid+".matches");
  });*/

        $('#btn02').click(function(e) {
            e.preventDefault(); //stop the browser from following
            var rid = $("#selectDataset option:selected").val();
            window.location.href = machine_http + 'download/' + Base64.encode("Files/PROJECTS/" + pid + "/matches/" + '/' + sid + "/" + "alignment." + rid + ".matches.taxonomy.abundance.rpkm");
        });

        $('#btn03').click(function(e) {
            e.preventDefault(); //stop the browser from following
            var rid = $("#selectDataset option:selected").val();
            window.location.href = machine_http + 'download/' + Base64.encode("Files/PROJECTS/" + pid + "/assembly/idba_ud/" + '/' + "alignment." + rid + ".matches.taxonomy.abundance.genes.rpkm");
        });






    }

}