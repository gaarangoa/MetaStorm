var stringify = function (x) {
  if (typeof(x) === 'number' || x === undefined) {
    return String(x);
    // otherwise it won't work for:
    // NaN, Infinity, undefined
  } else {
    return JSON.stringify(x);
  }
};

var js_comparison_table = function () {
  var values = [true, false,
                'true', 'false',
                1, 0, -1,
                '1', '0', '-1',
                null, undefined,
                [], [[]],
                [0], [1],
                ['0'], ['1'],
                '',
                Infinity,
                -Infinity,
                NaN,
                {}];
  var values2 = [true, false,
                'true', 'false',
                1, 0, -1,
                '1', '0', '-1',
                null, undefined,
                [], [[]],
                [0], [1],
                ['0'], ['1'],
                '',
                Infinity,
                -Infinity,
                NaN,
                {}];
  // as for objects it makes difference if they are the same
  var rows = [];
  var row = [];
  var i, j;
  var val1, val2;

  //
  row = values2.map(Boolean).map(function (x) {
    return x ? 1 : -0.5;
  });
  rows.push([1].concat(row));
  for (i = 0; i < values.length; i++) {
    row = [Boolean(values[i]) ? 1 : -0.5];
    for (j = 0; j < values2.length; j++) {
      if (values[i] === values2[j]) {
        row.push(1.);
      } else if (values[i] == values2[j]) {
        row.push(0.5);
      } else if (values[i] == values[j]) {
        row.push(0);
      } else if (values[i] != values2[j]) {
        // row.push(-1);
        row.push(-0.5);  // purely for graphical reasons
      } else {
        row.push(0.);
      }
    }
    rows.push(row);
  }

  return {labels: ["Boolean(x)"].concat(values.map(stringify)),
          rows: rows};
};

window.onload=function(){
	//var rootdir=$("#rootdir").val()
	//var rootdir=$("#rootdir").val()

  var get_rootdir = function(){
    var rootdir=[]
    $("input[name='selProject']:checked").each(function() {
      rootdir=$(this).val();
      });
    return(rootdir)
  }
	$("#GetBroadInfo").on("click",function(rootdir){


		var rootdir=get_rootdir()
		$.getJSON($SCRIPT_ROOT + '/_get_broad_info', {
				rootdir: rootdir
			  }, function(data) {
				//$("#setup").html("<button class='md-trigger' style='font-size:1em;'> Samples </h1>");
				$('#SecondSection').html("<div  class='column' id='setup3' style='color:#000; width:30%;'></div>")

				$('#SecondSection').append("<div class='column' id='setup' style='color:#000; width:30%;'></div>")

				$("#setup").html("<h1 style='font-size:1pe;font-weight:100; width:100%; text-align: left;'> Samples to compare </h1>");
				$("#setup").append("<div id='samplesCheck'></div>")
				var samples=data.samples;
				for(var i=0;i<=samples.length-1;i++){
					var spaces = 5-samples[i].length
					$("#samplesCheck").append("<input type='checkbox' checked = 'checked' name='samplesBox' value='"+samples[i]+"' id='"+samples[i]+"' ><label for='"+samples[i]+"'>"+samples[i]+"</label></input>");
					}

				$("#setup").append("<div id=\"dbsC\"><h1 style='font-size:1pe;font-weight:100'> Reference datasets </h1></div>")
				for(var i=0;i<=data.dbs.length-1;i++){
					if(i!=2){$("#dbsC").append("<input type='radio' name='dbs' value='"+data.dbs[i]+"' id='"+data.dbs[i]+"' ><label for='"+data.dbs[i]+"'>"+data.dbs[i]+"</label><br></input>");}else{$("#dbsC").append("<input checked='checked' type='radio' name='dbs' value='"+data.dbs[i]+"' id='"+data.dbs[i]+"' ><label for='"+data.dbs[i]+"'>"+data.dbs[i]+"</label><br></input>")}
					}

				$('#SecondSection').append("<div  class='column' id='setup2' style='color:#000; width:20%'></div>")
				$("#setup2").html("<div id=\"taxoCheck\"><h1 style='font-size:1pe;font-weight:100'> Annotation </h1></div>")
				$("#taxoCheck").append("<input type='radio' id='taxo' name='type' value='taxonomy' ><label for='taxo'>Taxonomy annotation</label><br></input>")
				$("#taxoCheck").append("<input type='radio' id='fun' name='type' checked = 'checked' value='function'  ><label for='fun'>Functional annotation</label></input>")

				$("#setup2").append("<div id=\"parameters\"><h1 style='font-size:1pe;font-weight:100'> Parameters </h1></div>")
				$("#parameters").append("Evalue<input type='text' id='evalue' value=1e-10><br></input>")
				$("#parameters").append("Min Matches<input type='text' id='Matches' value=1><br></input>")

				$("#setup3").html("<h1 style='font-size:1pe;font-weight:100; width:100%; text-align: center;'> Options </h1>")
				$("#setup3").append("<div><button  id='assemblyStats' style='font-size:100%; margin: 10px 0px; width:100%; background:#e2674a'> Project Summary</button></div>")
        $("#setup3").append("<div><button  id='overview_button' style='font-size:1em; margin: 10px 0px; width:100%; background:#99CC00'> Samples Overview</button></div>")
        $("#setup3").append("<div><button  id='submit2' style='font-size:1em; margin: 10px 0px; width:100%; background:#C24747'>Comparative Analysis</button></div>")
        $("#setup3").append("<div><button  id='TaxonomyTree' style='font-size:100%; margin: 10px 0px; width:100%; background:#e2074c'> Taxonomy Tree</button></div>")
				$("#setup3").append("<div><button  id='none' style='font-size:1em; margin: 10px 0px; width:100%; background:#FFCC66'>Protocol</button></div>")
				$("#setup3").append("<div><button  id='goHome' style='font-size:1em; margin: 10px 0px; width:100%; background:#99CC99'>Home</button></div>")

				//$("#setup3").append("<div><button class='md-trigger' id='submit2' style='font-size:1em; margin: 10px 0px; width:100%; data-modal='modal-1''>Back</input></div>")

				$('#SecondSection').append("<div  class='column' id='setup4' style='color:#000; width:20%'></div>")
				$("#setup4").html("<div id='taxoorder'><h1 style='font-size:1pe;font-weight:100'> Taxo Order </h1></div>")
				$("#taxoorder").append("<div><select id='selTaxonomy'><option value='phylum'>phylum</option><option value='class'>class</option><option value='order'>order</option><option value='family'>family</option><option value='genus'>genus</option></select></div>")
			  });
	});

	$(document).on('click',"input[name='type']",function() {
		if ($(this).val() == 'taxonomy') {}
		if ($(this).val() == 'function') {}
	});


	var datax;

	$(document).on('click','#submit2', function() {
		// get unchecked samples
		//var rootdir=$("#rootdir").val()

		// get all samples
		var all_samples=[]
		$("input[name='samplesBox']").each(function() {
			all_samples.push($(this).val());
			});

		// get the checked databases
		var selected_db=[]
		$("input[name='dbs']:checked").each(function() {
			selected_db.push($(this).val());
			});

		// select analysis: taxo-function
		var selected_process=[]
		$("input[name='type']:checked").each(function() {
			selected_process=$(this).val();
			});

		// select taxonomy level if selected
		if(selected_process =='taxonomy'){
			var selected_level=$("#selTaxonomy").val()
		}else{
			var selected_level="none"
		}

		var selected_evalue=$("#evalue").val()


		$("#ThirdSection").html("<div class='column' id='ThirdSectionCol1' style='color:#000; width:24%'></div>")
		$("#ThirdSectionCol1").append("<div id='ThirdSectionCol1Title1'><h1 style='font-size:1pe;font-weight:100; text-align:center'> Filter </h1></div>")
		$("#ThirdSectionCol1Title1").append("<textarea id='fterms' type='text' style='width:100%; color:#000; bacground=rgba(0,0,0,0.2); text-align:left' ></textarea>")
		$("#ThirdSectionCol1Title1").append("<div><button  id='update' style='font-size:1em; margin: 10px 0px; width:100%; background:#669999'>Update</button></div>")

		$("#ThirdSection").append("<div class='column' id='ThirdSectionCol2' style='color:#000; width:76%'></div>")
		$("#ThirdSectionCol2").html("<div id='ThirdSectionCol2Title2' style='overflow:auto'><h1 style='font-size:1pe;font-weight:100;'> PieChart </h1></div>")
		$("#ThirdSectionCol2").append("<div id='ThirdSectionCol2Title1' style='overflow:auto'><h1 style='font-size:1pe;font-weight:100;'> HeatMap </h1></div>")

    var rootdir=get_rootdir()
		$.getJSON($SCRIPT_ROOT + '/_results', {
				rootdir: rootdir, samples: all_samples.join("*"), reference: selected_db.join("_"), process: selected_process, evalue: selected_evalue, level:selected_level
			  }, function(data){datax=data; load_all(data.matrix);});
	});

  // get overall statistics
	$(document).on('click',"#assemblyStats",function() {
		//var rootdir=$("#rootdir").val()
    var rootdir=get_rootdir()
		$.getJSON($SCRIPT_ROOT + '/_AssemblyStats', {
			rootdir: rootdir
		}, function(data){
      var w = window.open("index5");
      w.data=data;
		});

	});

  //make the taxonomy tree
  $(document).on('click',"#TaxonomyTree",function() {
		//var rootdir=$("#rootdir").val()
    var rootdir=get_rootdir()
		$.getJSON($SCRIPT_ROOT + '/_TaxonomyTree', {
			rootdir: rootdir
		}, function(data){
      var w = window.open("TaxonomyTree");
      w.data=data;
		});

	});

	$(document).on('click','#update', function(){
		//alert(datax)
		load_all(datax.matrix)
	});

	var load_all = function(data){

		// get unchecked samples
		var remove_samples=[]
		$("input[name='samplesBox']").each(function() {
			if(!$(this).is(':checked')){remove_samples.push($(this).val())}
			});
		var r_s=remove_samples.join(",").replace(/\s+/g,"")

		var pattern = $('#fterms').val();
		var patx=pattern


		pattern = new RegExp("^"+pattern.replace(/,|\s+|\n|,\s+/g,"#").replace(/#/g,"$|^").replace(/\*/g,".+")+"$",'g')
		remove_samples = new RegExp("^"+r_s.replace(/,|\s+|,\s+/g,"#").replace(/#/g,"$|^").replace(/\*/g,".+")+"$",'g')

		var label_col_full = Object.keys(data[0]);
		var label_row = [];
		var label_col=[];
		var rows = [];
		var row = [];
		var maxval=0;
		var uniquerow=0
		var count=0;
		var total_row=[]

		for(var i = 1; i < data.length; i++){
		if(data[i][0].match(pattern)!=null || patx==""){
			label_row.push(data[i][0]);
			row = [];
			rowsum=0
			for(var j = 1; j < label_col_full.length; j++){
				if(data[0][j].replace(/\s+/g,"").match(remove_samples)==null || r_s==""){
					var item=parseFloat(data[i][j])
					if(uniquerow==0){label_col.push(data[0][j])}
					if(item > maxval){maxval=item;}
					row.push(item);
					rowsum+=item;
				}
			}
			total_row.push([data[i][0], rowsum])
			rows.push(row);
			uniquerow++
			}

		}
		d3.select("svg").remove();
		draw_pie_chart("#ThirdSectionCol2Title2",total_row);
		main(d3.transpose(rows), label_row, label_col, maxval,'#ThirdSectionCol2Title1');
		//main(d3.transpose(rows), label_row, label_col_full.slice(1));

	};

};

var draw_pie_chart = function(tag, data){

	    data.sort(function(a, b) {
			return b[1] - a[1];
		});

		var ndata=[]

		var index, entry;
		for (index = 0; index < data.length; ++index) {
			entry = data[index];
			ndata.push([entry[0],entry[1]]);
		}
		data=ndata
		ndata=[]
		// Build the chart

		$(tag).highcharts({
			chart: {
				plotBackgroundColor: null,
				plotBorderWidth: null,
				plotShadow: false
			},
			title: {
				text: 'Main'
			},
			tooltip: {
				pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
			},
			plotOptions: {
				pie: {
					allowPointSelect: true,
					cursor: 'pointer',
					dataLabels: {
						enabled: true,
						format: '<b>{point.name}</b>: {point.percentage:.1f} %',
						style: {
							color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
						},
						connectorColor: 'silver'
					}
				}
			},
			series: [{
				type: 'pie',
				name: '',
				data: data
			}]
		});

		$(tag).prepend("<div id='ThirdSectionCol2Title2' style='overflow:auto'><h1 style='font-size:1pe;font-weight:100;'> PieChart </h1></div>")

}

var main = function(corr, label_col, label_row,maxval, tag){

	$(tag).html("<div id='ThirdSectionCol2Title2' style='overflow:auto'><h1 style='font-size:1pe;font-weight:100;'> HeatMap </h1></div>")

  var transition_time = 15;
  var body = d3.select('body');
  var disp= d3.select(tag)
  //disp=disp.select("div.column2")
  var tooltip = d3.select('body').select('div.tooltip');

  var row = corr;
  var col = d3.transpose(corr);


  // converts a matrix into a sparse-like entries
  // maybe 'expensive' for large matrices, but helps keeping code clean
  var indexify = function(mat){
      var res = [];
      for(var i = 0; i < mat.length; i++){
          for(var j = 0; j < mat[0].length; j++){
              res.push({i:i, j:j, val:mat[i][j]});
          }
      }
      return res;
  };

  var corr_data = indexify(corr);
  var order_col = d3.range(label_col.length + 1);
  var order_row = d3.range(label_row.length + 1);

  var color = d3.scale.linear()
      .domain([0,10,100,500,1000,5000,10000, maxval*0.9])
      .range(['white','#A020F0','#ADFF2F','#FF8C00',"#FF7F00",'#8B4500','#8B0000',"black"]);


  var scale = d3.scale.linear()
      .domain([0, 10])
      .range([0, 170]);

	var maxlen=0
	for(var j=0; j<label_row.length; j++){if(label_row[j].length>=maxlen){maxlen=label_row[j].length}}
	var label_spacex = 27*maxlen/2.5;

	maxlen=0
	for(var j=0; j<label_col.length; j++){if(label_col[j].length>=maxlen){maxlen=label_col[j].length}}
	var label_spacey = 27*maxlen/2.5;


  var svg = disp.append('svg')
    .attr('width', (label_spacex+label_col.length*17.05))
    .attr('height', (label_spacey+label_row.length*17))


  var matrix = svg.append('g')
      .attr('class','matrix')
      .attr('transform', 'translate(' + (label_spacex) + ',' + (0) + ')');

  var pixel = matrix.selectAll('rect.pixel').data(corr_data);

  // as of now, data not changable, only sortable ###################HERE#######################
  pixel.enter()
      .append('rect')
          .attr('class', 'pixel')
          .attr('width', scale(0.85))
          .attr('height', scale(0.85))
          .style('fill',function(d){ return color(d.val);})
          .style('opacity',1)
          .on('mouseover', function(d){pixel_mouseover(d);})
          .on('mouseout', function(d){mouseout(d);})
          .on('click', function(d){


	var sdata = label_row[d.i]+"_"+label_col[d.j];

});


  tick_col = svg.append('g')
      .attr('class','ticks')
      .attr('transform', 'translate(' + (label_spacex) + ',' + (label_row.length*17) + ')')
      .selectAll('text.tick')
      .data(label_col);

  tick_col.enter()
      .append('text')
          .attr('class','tick')
          .style('text-align', 'center')
          .style('text-anchor', 'end')
          .attr('transform', function(d, i){return 'rotate(270 ' + scale(order_col[i] + 0.7) + ',0)';})
          .attr('font-size', scale(0.8))
          .text(function(d){ return d; })
          .on('mouseover', function(d, i){tick_mouseover(d, i, col[i], label_row);})
          .on('mouseout', function(d){mouseout(d);})
          //.on('click', function(d, i){reorder_matrix(i, 'col');});
          //.on('click', function (d, i) { reorder_matrix(i, 'col'); });

  tick_row = svg.append('g')
      .attr('class','ticks')
      .style('text-align', 'right')
      .attr('transform', 'translate(' + (label_spacex) + ',' + (0) + ')')
      .selectAll('text.tick')
      .data(label_row);

  tick_row.enter()
      .append('text')
          .attr('class','tick')
          .style('text-anchor', 'end')
          .attr('font-size', scale(0.8))
          .text(function(d){ return d; })
          .on('mouseover', function(d, i){tick_mouseover(d, i, row[i], label_col);})
          .on('mouseout', function(d){mouseout(d);});
          //.on('click', function(){}); /*for rows*/

    // here the shady box is shown when you pass the pointer
  var pixel_mouseover = function(d){
    tooltip.style("opacity", 0.9)
      .style("left", (d3.event.pageX + 15) + "px")
      .style("top", (d3.event.pageY + 8) + "px")
      .html(label_row[d.i] + "<br>" + label_col[d.j] + "<br>" + "" + d.val.toFixed(0));
  };

  var mouseout = function(d){
    tooltip.style("opacity", 1e-6);
  };

  var tick_mouseover = function(d, i, vec, label){
    // below can be optimezed a lot
    var indices = d3.range(vec.length);
    // also value/abs val?
    indices.sort(function(a, b){ return Math.abs(vec[b]) - Math.abs(vec[a]); });
    res_list = [];
    for(var j = 0; j < Math.min(vec.length, 10); j++) {
      res_list.push((vec[indices[j]] > 0 ? "+" : "&nbsp;") + vec[indices[j]].toFixed(3) + "&nbsp;&nbsp;&nbsp;" + label[indices[j]]);
    }
    tooltip.style("opacity", 0.8)
      .style("left", (d3.event.pageX + 15) + "px")
      .style("top", (d3.event.pageY + 8) + "px")
      .html("" + i + ": " + d + "<br><br>" + res_list.join("<br>"));
  };


  var refresh_order = function(){
      tick_col.transition()
          .duration(transition_time)
              .attr('transform', function(d, i){return 'rotate(270 ' + scale(order_col[i] + 0.7) + ',0)';})
              .attr('x', function(d, i){return scale(order_col[i] + 0.7);});

      tick_row.transition()
          .duration(transition_time)
              .attr('y', function(d, i){return scale(order_row[i] + 0.7);});

      pixel.transition()
          .duration(transition_time)
              .attr('y', function(d){return scale(order_row[d.i]);})
              .attr('x', function(d){return scale(order_col[d.j]);});
  };

  refresh_order();

};
