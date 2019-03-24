function download_csv(data) {

    //var data = [['name1', 'city1', 'some other info'], ['name2', 'city2', 'more info']];

    var csvContent = '';
    data.forEach(function(infoArray, index) {
        dataString = infoArray.join('\t');
        csvContent += index < data.length ? dataString + '\n' : dataString;
    });

    /*var download = function(content, fileName, mimeType) {
      var a = document.createElement('a');
      mimeType = mimeType || 'application/octet-stream';

      if (navigator.msSaveBlob) { // IE10
        return navigator.msSaveBlob(new Blob([content], { type: mimeType }), fileName);
      } else if ('download' in a) { //html5 A[download]
        a.href = 'data:' + mimeType + ',' + encodeURIComponent(content);
        a.setAttribute('download', fileName);
        document.body.appendChild(a);
        setTimeout(function() {
          a.click();
          document.body.removeChild(a);
        }, 100);
        return true;
      } else { //do iframe dataURL download (old ch+FF):
        var f = document.createElement('iframe');
        document.body.appendChild(f);
        f.src = 'data:' + mimeType + ',' + encodeURIComponent(content);

        setTimeout(function() {
          document.body.removeChild(f);
        }, 333);
        return true;
      }
    }*/


    //console.log(csvContent)
    //download(csvContent, 'sample_'+sid+'.tsv', 'text/csv');

    window.open().document.write('<p>Copy (Ctrl+A Ctrl+C) and paste the content of this textarea into any software such as Microsoft Excel</p></br><textarea style="width:100%; height:900px;">' + csvContent + "</textarea>");

}






function individual_samples(data) {

    //console.log(data)

    // get the data
    val2 = [
        ['sample_id', 'gene_id', 'gene_counts', 'gene_16S_normalization', 'gene_RPKM_normalization', 'gene_functional_category_id', 'gene_functional_category', 'description']
    ]
    val = []
    Object.keys(data.Cn16S).forEach(function(key) {

        data.Cn16S[key][1].split(",").forEach(function(item, index, arr) {
            category_id = data.D[item]

            if (data.A[category_id].counts > 0) {
                val.push({
                    'gene_id': key,
                    'gene_counts': parseFloat(data.Cn16S[key][2]),
                    'gene_N16s': parseFloat(data.Cn16S[key][3]),
                    'gene_RPKM': parseFloat(data.CRPKM[key][3]),
                    'category_id': category_id,
                    'function': data.B[category_id].X1,
                    'description': data.B[category_id].X2,
                    'category_counts': data.A[category_id].counts,
                    'category_N16s': data.A[category_id].n16s,
                    'category_RPKM': data.A[category_id].rpkm,
                    'num_categories_in_gene': arr.length
                })
                val2.push([
                    data.A[category_id].sample,
                    key,
                    parseFloat(data.Cn16S[key][2]),
                    parseFloat(data.Cn16S[key][3]),
                    parseFloat(data.CRPKM[key][3]),
                    category_id,
                    data.B[category_id].X1,
                    data.B[category_id].X2
                ])
            }

        })


    });

    console.log(val)

    var FunctionalCategoryChart = dc.pieChart("#chart-ring-year"),
        GenesPerFCategory = dc.rowChart("#chart-row-spenders");




    function remove_empty_bins(source_group) {
        return {
            all: function() {
                return source_group.all().filter(function(d) {
                    return d.value != 0;
                });
            }
        };
    }

    function define_height_bar(source_group) {
        //console.log(source_group)
        //dc.renderAll()
        return source_group

    }


    function getTops(source_group, top) {
        return {
            all: function() {
                //console.log(source_group)
                return source_group.top(top);
            }
        };
    }


    // "Grab the filters from the charts, set the filters on the charts to null,
    // do your Crossfilter data removal, then add the filters back to the charts.
    // The exact filter format is kind of screwy, and the fact that you have to put
    // the output of .filters() in an array to make it work with .filter() is a bit strange."
    function resetData(ndx, dimensions) {
        var CategoryChartFilters = FunctionalCategoryChart.filters();
        var GenesChartFilters = GenesPerFCategory.filters();
        FunctionalCategoryChart.filter(null);
        GenesPerFCategory.filter(null);
        ndx.remove();
        FunctionalCategoryChart.filter([CategoryChartFilters]);
        GenesPerFCategory.filter([GenesChartFilters]);
        //console.log(GenesPerFCategory.filters());
    }

    // set crossfilter with first dataset
    var ndx = crossfilter(val),
        CategoryDim = ndx.dimension(function(d) {
            return d.category_id;
        }),
        GeneDim = ndx.dimension(function(d) {
            return d.gene_id;
        }),

        FunctionalCategoryCounts = CategoryDim.group().reduceSum(function(d) {
            return +d.gene_counts;
        }),
        GeneCounts = GeneDim.group().reduceSum(function(d) {
            return d.gene_counts / d.num_categories_in_gene;
        }),
        //GeneCounts = GeneDim.group().reduce(reduceAdd, reduceRemove, reduceInit),
        GeneNum = GeneDim.group().reduceCount(),
        CategoryCounts = CategoryDim.group().reduceCount(),
        nonEmptyHist = remove_empty_bins(GeneCounts),
        fakeGroup = getTops(GeneCounts, 15),
        fakeGroup2 = getTops(FunctionalCategoryCounts, 50);

    console.log(GeneCounts)

    function render_plots(data) {
        FunctionalCategoryChart
            .height(200)
            .dimension(CategoryDim)
            .group(fakeGroup2)
            .ordering(function(d) {
                return -d.value
            })
            .innerRadius(0)
            .legend(dc.legend())
            .on('pretransition', function(chart) {
                chart.selectAll('text.pie-slice').text(function(d) {
                    perc = dc.utils.printSingleValue((d.endAngle - d.startAngle) / (2 * Math.PI) * 100)
                    if (perc >= 1.5) {
                        return perc + '%'
                    }
                })
            })
            //.title(function(d){return 'some'})
            .on('filtered.monitor', function(chart, filter) {

                $("#categories_metadata").html("<b>Category:</b> <code>" + filter +
                        "</code> <br> <b>Description: </b>" + data.B[filter].X1 +
                        //"<br> <b>Matches:</b> <code>"+ data.A[filter].counts+
                        "</code>. <br> <b> Definition:" + "</b> " + data.B[filter].X2 + " ")
                    //console.log(data.A[filter], data.B[filter])

            })



        GenesPerFCategory
            .width(500).height(450)
            .gap(2)
            .dimension(GeneDim)
            .group(fakeGroup)
            .ordering(function(d) {
                return -d.value
            })
            .elasticX(true)
            .fixedBarHeight(25)
            .title('Index Gain')
            //.valueAccessor(function(p) { return p.value.count > 0 ? p.value.total / p.value.count : 0; })





        dc.renderAll();
    }

    render_plots(data);

    $(document).on("click", "#clearMetadata", function() {
        $("#categories_metadata").html("")

    })



    // REFRESH DATA AFTER 5 SECONDS
    /*setTimeout(function() {
        console.log("data reset");
        resetData(ndx, [yearDim, spendDim, nameDim]);
        ndx.add(data2);
        dc.redrawAll();
    }, 5000);*/

}


$(document).on("click", "#download_one_sample_table_taxo", function(e) {

    e.preventDefault(); //stop the browser from following
    var rid = $("#selectDataset option:selected").val();
    if (pip = "matches") {
        window.location.href = machine + 'download/' + Base64.encode("Files/PROJECTS/" + pid + "/matches/" + sid + '/' + "alignment." + rid + ".matches.taxonomy.abundance.json");
    } else {
        // window.location.href = machine+'download/'+Base64.encode("Files/PROJECTS/"+pid+"/matches/"+sid+'/'+"alignment."+rid+".matches.taxonomy.abundance.json");
        window.location.href = machine + 'download/' + Base64.encode("Files/PROJECTS/" + pid + "/assembly/idba_ud/" + '/' + "alignment." + rid + ".matches.taxonomy.abundance.genes.json");
    }

})


$(document).on("click", "#download_one_sample_table_func", function(e) {


    // e.preventDefault();  //stop the browser from following
    // var rid = $( "#selectFuncDataset option:selected" ).val();
    // window.location.href = machine+'download/'+Base64.encode("Files/PROJECTS/"+pid+"/matches/"+sid+'/'+"alignment."+rid+".matches.function.abundance.16s");

    download_csv(val2)
})