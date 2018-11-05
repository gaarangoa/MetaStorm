machine = "/MetaStorm/"


wait_bar = function(value_now) {
    return '<div class="progress progress-sm active">' +
        '<div class="progress-bar progress-bar-success progress-bar-striped" role="progressbar" aria-valuenow=' + value_now + ' aria-valuemin="0" aria-valuemax="100" style="width: ' + value_now + '%">' +
        '<span class="sr-only">20% Complete</span>' +
        '</div>' +
        '</div>'
}

urlParam = function(name) {
    var results = new RegExp('[\?&]' + name + '=([^&#]*)').exec(window.location.href);
    if (results == null) {
        return null;
    } else {
        return results[1] || 0;
    }
}



logout = function(uid) {
    $.ajax({
        url: machine + "logout",
        type: "POST",
        async: true,
        data: JSON.stringify({
            uid: uid
        }),
        contentType: "application/json; charset=utf-8",
        success: function(x) {
            window.open(machine + "login", "_self")
        }
    });
}


vsession = function(uid) {
    $.ajax({
        url: machine + "vsession",
        type: "POST",
        async: true,
        data: JSON.stringify({
            uid: uid
        }),
        contentType: "application/json; charset=utf-8",
        success: function(x) {
            if (x == 'offline') {
                window.open(machine + "login", "_self");
            }
        }
    });
}



//format_names_taxonomy
fnt = function(name) {
    if (/unknown/.test(name)) {
        return "unknown"
    } else {
        //return d[names]
        out = name.split('__').slice(-1)[0]
        if (out == "") {
            return 'unknown'
        } else {
            return out
        }
    }
}

var get_checkbox = function(name) {
    var sel = $('input[name="' + name + '"]:checked').map(function(_, el) {
        return $(el).val().split("_")[0];
    }).get();
    return (sel)
}

var get_checkbox_text = function(name) {
    var sel = $('input[name="' + name + '"]:checked').map(function(_, el) {
        namep = $(el).val().split("_");
        namep.shift()
        return namep.join('_')
    }).get();
    return (sel)
}


var Base64 = {
    _keyStr: "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=",
    encode: function(e) {
        var t = "";
        var n, r, i, s, o, u, a;
        var f = 0;
        e = Base64._utf8_encode(e);
        while (f < e.length) {
            n = e.charCodeAt(f++);
            r = e.charCodeAt(f++);
            i = e.charCodeAt(f++);
            s = n >> 2;
            o = (n & 3) << 4 | r >> 4;
            u = (r & 15) << 2 | i >> 6;
            a = i & 63;
            if (isNaN(r)) {
                u = a = 64
            } else if (isNaN(i)) {
                a = 64
            }
            t = t + this._keyStr.charAt(s) + this._keyStr.charAt(o) + this._keyStr.charAt(u) + this._keyStr.charAt(a)
        }
        return t
    },
    decode: function(e) {
        var t = "";
        var n, r, i;
        var s, o, u, a;
        var f = 0;
        e = e.replace(/[^A-Za-z0-9\+\/\=]/g, "");
        while (f < e.length) {
            s = this._keyStr.indexOf(e.charAt(f++));
            o = this._keyStr.indexOf(e.charAt(f++));
            u = this._keyStr.indexOf(e.charAt(f++));
            a = this._keyStr.indexOf(e.charAt(f++));
            n = s << 2 | o >> 4;
            r = (o & 15) << 4 | u >> 2;
            i = (u & 3) << 6 | a;
            t = t + String.fromCharCode(n);
            if (u != 64) {
                t = t + String.fromCharCode(r)
            }
            if (a != 64) {
                t = t + String.fromCharCode(i)
            }
        }
        t = Base64._utf8_decode(t);
        return t
    },
    _utf8_encode: function(e) {
        e = e.replace(/\r\n/g, "\n");
        var t = "";
        for (var n = 0; n < e.length; n++) {
            var r = e.charCodeAt(n);
            if (r < 128) {
                t += String.fromCharCode(r)
            } else if (r > 127 && r < 2048) {
                t += String.fromCharCode(r >> 6 | 192);
                t += String.fromCharCode(r & 63 | 128)
            } else {
                t += String.fromCharCode(r >> 12 | 224);
                t += String.fromCharCode(r >> 6 & 63 | 128);
                t += String.fromCharCode(r & 63 | 128)
            }
        }
        return t
    },
    _utf8_decode: function(e) {
        var t = "";
        var n = 0;
        var r = c1 = c2 = 0;
        while (n < e.length) {
            r = e.charCodeAt(n);
            if (r < 128) {
                t += String.fromCharCode(r);
                n++
            } else if (r > 191 && r < 224) {
                c2 = e.charCodeAt(n + 1);
                t += String.fromCharCode((r & 31) << 6 | c2 & 63);
                n += 2
            } else {
                c2 = e.charCodeAt(n + 1);
                c3 = e.charCodeAt(n + 2);
                t += String.fromCharCode((r & 15) << 12 | (c2 & 63) << 6 | c3 & 63);
                n += 3
            }
        }
        return t
    }
}

var biome = ['Air',
    'Built Environment',
    'Host-associated',
    'Human-associated',
    'Human-oral',
    'Human-skin',
    'Human-vaginal',
    'Microbial mat/biofilm',
    'Miscellaneous natural or artificial environment',
    'Plant-associated',
    'Sediment',
    'Soil',
    'Wastewater',
    'Water',
    'Urban'
]
var experiment_type = ['Metagenome',
    'Amplicon 16S rRNA'
]
var sequencing_method = ['Illumina HiSeq 2500',
        'Illumina HiSeq 3/4000',
        'Illumina HiSeq X',
        'Illumina MiniSeq',
        'Illumina MiSeq',
        'Illumina NextSeq',
        'SOLiD'

    ]
    // this function returns the box with the selected projects:

function rpro(color, pname, numsamples, pdescription) {
    return ['<div class="info-box ' + color + '">' +
        '<span class="info-box-icon"><i class="ion ion-cube"></i></span>' +
        '<div class="info-box-content">' +
        '<span class="info-box-text">' + pname + '</span>' +
        '<span class="info-box-number">' + numsamples + '</span>' +
        '<div class="progress">' +
        '<div class="progress-bar" style="width: 100%"></div>' +
        '</div>' +
        '<span class="progress-description">' +
        pdescription +
        '</span>' +
        '</div>' +
        '<!-- /.info-box-content -->' +
        '</div>'
    ]
}


var html_progress_bar = function(title, value, ofmany, percent, color, id) {
    arg = ''
    if (id != 'none') {
        arg = '<a href="#"><i class="fa fa-fw fa-question-circle" style="color:#cc0000" id="tp_' + id + '"></i></a>'
    }
    return ['<div class="progress-group">' +
        '<span class="progress-text">' + title + ' ' + arg + '</span>' +
        '<span class="progress-number"><b>' + value + '</b> hits of ' + ofmany + '</span>' +
        '<div class="progress sm">' +
        '<div class="progress-bar progress-bar-' + color + '" style="width:' + percent + '%"></div>' +
        '</div>' +
        '</div>'
    ]
}


var ptree = function(treeData, domain, tag, clpd, names, Pcolor, width, height, rsize, condition, pip, rid, offset, stk) {

    if (!offset) {
        offset = 3
    }

    var color = d3.scale.linear()
        .domain([domain[0], domain[1], domain[2]])
        .range(['white', 'yellow', 'red'])

    var margin = {
        top: 10,
        right: 5,
        bottom: 10,
        left: 20
    }
    width = width - margin.top - margin.bottom
    height = height - margin.top - margin.bottom

    var i = 0,
        duration = 750,
        root;
    var tree = d3.layout.tree()
        .size([height, width]);
    var diagonal = d3.svg.diagonal()
        .projection(function(d) {
            return [d.y, d.x];
        });
    var svg = d3.select(tag).append("svg")
        .attr("width", width + margin.right + margin.left)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
    root = treeData[0];
    root.x0 = height / 2;
    root.y0 = 0;

    function collapse(d) {
        if (d.children) {
            d._children = d.children;
            d._children.forEach(collapse);
            d.children = null;
        }
    }

    if (clpd == 1) {
        root.children.forEach(collapse);
    }


    update(root);
    d3.select(self.frameElement).style("height", "auto");
    i = 0

    function update(source) {
        i++;
        //d3.select("svg").attr("height", 500+10*i)
        //d3.select("svg").attr("transform", "translate(" + margin.left + "," + (margin.top+100*i) + ")");


        // Compute the new tree layout.
        var nodes = tree.nodes(root).reverse(),
            links = tree.links(nodes);
        // Normalize for fixed-depth.
        nodes.forEach(function(d) {
            d.y = d.depth * 150;
        });
        // Update the nodes…
        var node = svg.selectAll("g.node")
            .data(nodes, function(d) {
                return d.id || (d.id = ++i);
            });


        // Enter any new nodes at the parent's previous position.
        var nodeEnter = node.enter().append("g")
            .attr("class", "node")
            .attr("transform", function(d) {
                return "translate(" + source.y0 + "," + source.x0 + ")";
            })
            .on("click", click);



        nodeEnter.append("circle")
            .attr("r", 10)
            .style("fill", function(d) {
                return d._children ? "lightsteelblue" : "#fff";
            });
        nodeEnter.append("text")
            .attr("x", function(d) {
                return d.children || d._children ? -12 : 12;
            })
            //.attr("y", function(d) { return d.children || d._children ? -8 : 8; })
            .attr("dy", ".35em")
            .attr("text-anchor", function(d) {
                return d.children || d._children ? "end" : "start";
            })
            .text(function(d) {
                if (/unknown/.test(d[names])) {
                    return "unknown"
                } else {
                    //return d[names]
                    out = d[names].split('__').slice(-1)[0]
                    if (out == "") {
                        return 'unknown'
                    } else {
                        return out
                    }
                }
            })
            .style("fill-opacity", 1e-6);


        // Transition nodes to their new position.
        var nodeUpdate = node.transition()
            .duration(duration)
            .attr("transform", function(d) {
                return "translate(" + (d.y + 0) + "," + (d.x + 0) + ")";
            });
        nodeUpdate.select("circle")
            .attr("r", function(d) {
                return rsize
            }) //!FIXME EDIT HERE!!!
            .style("fill", function(d) {
                return d._children ? color(d[Pcolor]) : color(d[Pcolor]);
            });
        nodeUpdate.select("text")
            .style("fill-opacity", 1);
        // Transition exiting nodes to the parent's new position.
        var nodeExit = node.exit().transition()
            .duration(duration)
            .attr("transform", function(d) {
                return "translate(" + source.y + "," + source.x + ")";
            })
            .remove();
        nodeExit.select("circle")
            .attr("r", 1e-6);
        nodeExit.select("text")
            .style("fill-opacity", 1e-6);
        // Update the links…
        var link = svg.selectAll("path.link")
            .data(links, function(d) {
                return d.target.id;
            });
        // Enter any new links at the parent's previous position.
        link.enter().insert("path", "g")
            .attr("class", "link")
            .style("stroke", "rgba(0,0,255,0.08)")
            .style("stroke-width", 15)
            //.style("stroke-border","solid 1px #000")
            .attr("d", function(d) {
                var o = {
                    x: source.x0,
                    y: source.y0
                };
                return diagonal({
                    source: o,
                    target: o
                });
            });
        // Transition links to their new position.
        link.transition()
            .duration(duration)
            .attr("d", diagonal)
            //.style('stroke','#000');
            // Transition exiting nodes to the parent's new position.
        link.exit().transition()
            .duration(duration)
            //.style('stroke','#000')
            .attr("d", function(d) {
                var o = {
                    x: source.x,
                    y: source.y
                };
                return diagonal({
                    source: o,
                    target: o
                });
            })
            .remove();
        // Stash the old positions for transition.
        nodes.forEach(function(d) {
            d.x0 = d.x;
            d.y0 = d.y;
        });
    }
    // Toggle children on click.
    function click(d) {
        //alert(condition)

        if (d.children) {
            d._children = d.children;
            d.children = null;

        } else {
            d.children = d._children;
            d._children = null;



            name = fnt(d.id)

            console.log(d)


            $("#node_click_plot").html("<p>" + d.level + ": <b>" + name + "</b></p>")
            total = d.matches




            children_stack = []
            d.children.forEach(function(item, index) {

                name = fnt(item.id)
                matches = Math.round(item.matches)

                //if (item.matches==0.5) {
                //  matches=1
                //}else{
                //   matches=item.matches
                //}

                //children_stack.push(stk[1][item.id])

                $("#node_click_plot").append(html_progress_bar(name, matches, d.matches, 100 * matches / d.matches, 'red', 'none'))
            })

            console.log(children_stack)

            //console.log(d, condition, pip, rid)
            //get_childs_of_taxonomy(d, condition, pip, rid)
        }
        update(d);
        //alert(rid)

        //set_taxonomy_small_pie_chart(d)
    }
}

//******************************************************************************
// update the pie chart every time click on the tree
//******************************************************************************



var draw_pie_chart = function(tag, data, title, type, label_on) {
    //alert()
    type = 'pie'
    label_on = false
    data.sort(function(a, b) {
        return b[1] - a[1];
    });

    data = data.slice(0, 50) // top 20

    var ndata = []

    var index, entry;
    for (index = 0; index < data.length; ++index) {
        entry = data[index];
        ndata.push([fnt(entry[0]), entry[1]])
    }
    data = ndata
    ndata = []
        // Build the chart
    var chartx = new Highcharts.Chart({
        chart: {
            renderTo: tag.replace("#", ''),
            plotBackgroundColor: null,
            plotBorderWidth: 0,
            plotShadow: false,
            plotBorderWidth: 0,
            backgroundColor: null,
            marginTop: 1,
        },
        legend: {
            align: 'center',
            verticalAlign: 'bottom',
            layout: 'horizontal',
            //width: 10,
            y: 0,
            x: 0,
            //floating: false,
        },
        title: {
            text: null
        },
        tooltip: {
            pointFormat: '<b>{point.percentage:.1f}%</b>'
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                dataLabels: {
                    enabled: true,
                    //distance: -100,
                    //format: '<b>{point.percentage:.1f} %',
                    formatter: function() {
                        perc = Math.round(this.percentage * 100) / 100
                        if (perc >= 5) {
                            return perc + ' %';
                        }

                    },
                    style: {
                        color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
                    },
                    //connectorColor: 'silver'

                },
                showInLegend: true
            }
        },
        credits: {
            enabled: false
        },
        exporting: {
            enabled: true
        },
        series: [{
            innerSize: '0%',
            type: type,
            name: '',
            data: data
        }]
    });

    //$(tag).html(chartx.getCSV());

}



var draw_line = function(tag, data, title) {
    //alert()
    data.sort(function(a, b) {
        return b[1] - a[1];
    });

    var ndata = []

    var index, entry;
    for (index = 0; index < data.length; ++index) {
        entry = data[index];
        ndata.push([entry[0], entry[1]]);
    }
    data = ndata
    ndata = []
        // Build the chart
    $(tag).highcharts({
        chart: {
            plotBackgroundColor: null,
            plotBorderWidth: 1,
            plotShadow: true,
            plotBorderWidth: 0,
            backgroundColor: null,
            marginTop: 30
        },
        title: {
            text: title
        },
        //tooltip: {
        // pointFormat: '<b>{point.value:.1f}%</b>'
        //},
        plotOptions: {
            series: {
                allowPointSelect: false,
                borderColor: '#000',
                borderWidth: 2,
                shadow: true,
                showInLegend: false,
                pointPadding: 0.1, // Defaults to 0.1
                groupPadding: 0.01,
                dataLabels: {
                    enabled: true,
                    align: 'right',
                    color: '#FFFFFF',
                    x: -10
                },
            }
        },
        legend: {
            align: 'right',
            verticalAlign: 'top',
            layout: 'vertical',
            width: 300,
            y: 50,
            floating: false,
        },
        credits: {
            enabled: false
        },
        exporting: {
            enabled: false
        },
        series: [{
            data: data
        }],
        chart: {
            type: 'bar'
        },
    });
}













































































send_email = function(uid, msg, sub) {

    $.ajax({
        url: machine + "sendEmail",
        type: "POST",
        data: JSON.stringify({
            uid: uid,
            msg: msg,
            sub: sub
        }),
        async: true,
        contentType: "application/json; charset=utf-8",
        success: function(dat) {}
    });
}





















clustergram = function(target, heatmap, width) {
    window.inchlib = new InCHlib({ //instantiate InCHlib
        target: target, //ID of a target HTML element
        metadata: true, //turn on the metadata
        column_metadata: true, //turn on the column metadata
        //max_height: 800, //set maximum height of visualization in pixels
        width: 1000, //set width of visualization in pixels
        heatmap_colors: "BuYl", //set color scale for clustered data
        metadata_colors: "Reds", //set color scale for metadata
        draw_row_ids: true,
        max_column_width: 80,
        max_row_height: 20,
        min_percentil: 0,
        middle_percentile: 80,
        heatmap_font_color: "transparent",
        font: "Arial"
    });
    inchlib.add_color_scale("mine", {
        "start": {
            "r": 0,
            "g": 200,
            "b": 0
        },
        "middle": {
            "r": 0,
            "g": 0,
            "b": 0
        },
        "end": {
            "r": 255,
            "g": 0,
            "b": 0
        }
    });
    inchlib.read_data(heatmap); //read input json file
    inchlib.draw();
}






stacked = function(tag, data, categories) {

    /*Highcharts.setOptions({
        colors: ['#058DC7', '#50B432', '#ED561B', '#DDDF00', '#24CBE5', '#64E572', '#FF9655', '#FFF263', '#6AF9C4', '#000000', '#00FF5655']
    });*/


    $(tag).highcharts({
        chart: {
            type: 'column',
            //width: 100,
            height: 300,
            borderWidth: 0,
            plotBorderWidth: 0
        },
        legend: {
            align: 'right',
            verticalAlign: 'top',
            layout: 'vertical',
            width: 150,
            y: 0,
            floating: false,
        },
        title: {
            text: null
        },
        xAxis: {
            categories: categories
        },
        yAxis: {
            min: 0,
            title: {
                text: 'Relative Abundance (%)'
            },
            reversedStacks: true
        },
        tooltip: {
            pointFormat: '<span style="color:{series.color}"><b>{series.name}</b></span>:({point.percentage:.0f}%)<br/>',
            //shared: true
        },
        plotOptions: {
            column: {
                stacking: 'percent'
            },
            series: {
                allowPointSelect: true,
                borderColor: '#000',
                borderWidth: 0.1,
                shadow: false,
                pointPadding: 0.0, // Defaults to 0.1
                groupPadding: 0.0
            }
        },
        credits: {
            enabled: false
        },
        exporting: {
            enabled: true
        },
        series: data
    });
}



process_stacked = function(data) {
    categories = data[0].splice(1)
    d = []
    for (i = 1; i < data.length; i++) {
        d.push({
            name: fnt(data[i][0]),
            data: data[i].splice(1)
        })
    }
    return ([categories, d])
}




process_stacked2 = function(data) {
    categories = []
    data[0].splice(1).forEach(function(i, ix) {
        categories.push(i.split(":")[1])
    })

    d = []
    for (i = 1; i < data.length; i++) {
        d.push({
            name: fnt(data[i][0]),
            data: data[i].splice(1)
        })
    }

    return ([categories, d])
}



process_stacked_from_tree = function(data) {
    categories = []
    data[0].splice(1).forEach(function(i, ix) {
        categories.push(i.split(":")[1])
    })

    d = {}
    for (i = 1; i < data.length; i++) {
        key = fnt(data[i][0])
        d[key] = {
            name: fnt(data[i][0]),
            data: data[i].splice(1)
        }
    }

    return ([categories, d])
}








//when uploading a file, first setup the database to put the upload status to uploading
//g.db.execute()
loading_status_sql = function(pid, filename, status) {
    sql = "INSERT or REPLACE INTO fastqFiles VALUES ('" + pid + '_' + filename + "','" + pid + "','" + filename + "','" + status + "')"
        //sql='INSERT or REPLACE INTO fastqFiles VALUES ("a","b","c","d")'
        //console.log(sql)
    $.ajax({
        url: machine + "sqlgo",
        type: "POST",
        async: true,
        data: JSON.stringify({
            sql: Base64.encode(sql)
        }),
        contentType: "application/json; charset=utf-8",
        success: function(x) {
            ////console.log(x)
        }
    });

}



// google maps

var map;

var markers = [];

function initMap() {
    // 1st: get all the distinct latitud and altitud
    map = new google.maps.Map(document.getElementById('map'), {
        center: {
            lat: 20,
            lng: 10
        },
        zoom: 2,
        scrollwheel: false
    });
}


function drop(neighborhoods) {
    clearMarkers();
    for (var i = 0; i < neighborhoods.length; i++) {
        addMarkerWithTimeout(neighborhoods[i], i * 200);
    }

}

function addMarkerWithTimeout(position, timeout) {
    window.setTimeout(function() {
        markers.push(new google.maps.Marker({
            position: position,
            map: map,
            animation: google.maps.Animation.DROP
        }));
    }, timeout);
}

function clearMarkers() {
    for (var i = 0; i < markers.length; i++) {
        markers[i].setMap(null);
    }
    markers = [];
}














// load php

function upload_php(obj, sid, pid, pip, uid, upload_dir) {

    $(obj).plupload({
        // General settings
        runtimes: 'html5,flash,silverlight,html4',
        url: 'https://bench.cs.vt.edu/plupload/examples/upload.php',

        // User can upload no more then 20 files in one go (sets multiple_queues to false)
        max_file_count: 50,

        chunk_size: '1mb',

        filters: {
            // Maximum file size
            max_file_size: '100gb',
            // Specify what files to browse for
            mime_types: [{
                    title: "Raw NGS files",
                    extensions: "fastq,gz,fasta,fa,fq"
                },
                {
                    title: "Compressed NGS files",
                    extensions: "gz"
                }
            ]
        },

        // Rename files by clicking on their titles
        rename: true,

        // Sort files
        sortable: true,

        // Enable ability to drag'n'drop files onto the widget (currently only HTML5 supports that)
        dragdrop: true,

        multipart_params: {
            "upload_dir": upload_dir + "/" + pid + "/READS/",
            "arc_dir": "/groups/metastorm_cscee/MetaStorm/Files/PROJECTS/" + pid + "/READS/"
        }
    });

    // Handle the case when form was submitted before uploading has finished
    /* $('#form').submit(function(e) {
    	// Files in queue upload them first
    	if ($('#uploader').plupload('getFiles').length > 0) {

    		// When all files are uploaded submit form
    		$('#uploader').on('complete', function() {
    			$('#form')[0].submit();
    		});

    		$('#uploader').plupload('start');
    	} else {
    		alert("You must have at least one file in the queue.");
    	}
    	return false; // Keep the form from submitting
    }); */
}







































var draw_table = function(div, data) {

    var headerRenderer = function(instance, td, row, col, prop, value, cellProperties) {
        Handsontable.renderers.TextRenderer.apply(this, arguments);
        //td.style.fontWeight = 'bold';
        td.style.color = 'white'
        td.style.textAlign = 'center';
        td.style.backgroundColor = 'rgba(0,125,10,1)';
    };

    var rowOrder = function(data) {
        x = []
        x.push({
            data: "samples"
        })
        Object.keys(data[0]).forEach(function(element, index, array) {
            //return d.children || d._children ? "end" : "start";
            if (element != 'Long_Description' && element != "description" && element != "samples") {
                x.push({
                    data: element
                })
            }
        })
        x.push({
            data: "description"
        })
        x.push({
            data: "Long_Description"
        })
        return (x)
    }

    var colWidth = function(data) {
        x = []
        x.push(100)
        Object.keys(data[0]).forEach(function(element, index, array) {
            //return d.children || d._children ? "end" : "start";
            if (element != 'Long_Description' && element != "description" && element != "samples") {
                x.push(50)
            }
        })
        x.push(200)
        x.push(300)
        return (x)
    }


    $("#" + div).html('')
    var container = document.getElementById(div),
        previous_samples;

    var previous_samples = new Handsontable(container, {
        data: data,
        colHeaders: false,
        rowHeaders: false,
        columnSorting: false,
        //manualColumnResize: true,
        // fixedRowsTop: 1,
        manualColumnMove: false,
        manualRowMove: false,
        fixedRowsTop: 1,
        colWidths: colWidth(data),
        currentRowClassName: 'currentRow',
        currentColClassName: 'currentCol',
        fixedColumnsLeft: 1,
        columns: rowOrder(data),

        cells: function(row, col, prop) {
            var cellProperties = {};
            if (row === 0) {
                cellProperties.renderer = headerRenderer;
            }

            return cellProperties;
        },
    });

    //previous_samples.selectCell(2,2);
}






//