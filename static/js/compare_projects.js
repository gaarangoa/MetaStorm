

window.onload=function(){
   // Project setup table
   // table with all the results from the assembly -  this is an overall of the assembly performance

  uid=urlParam('uid')
  sid=urlParam('sid')
  pip=urlParam('pip')

  //pids=["6Jj08osyP0AG7T0", "SRFMW5bil52ieL0"]
  //pnames=["P1", "P2"]
  //vsession(uid)   

  
  machine="/MetaStorm/"
  //machine="/"

/*get list of all samples in the projet id*/
  //cmd='select c.sample_id,c.sample_name, c.status, c.sample_set from (select * from samples a inner join project_status b on a.project_id==b.project_id and a.sample_id==b.sample_id) c where project_id=="'+pid+'"'
  
  pids.forEach(function(pid,ipid,pids){
    
    cmd='select distinct a.sample_id sample_id, a.sample_name sample_name from (select * from samples where project_id=="'+pid+
        '") a inner join jobs b on a.sample_id == b.sid and b.pip=="'+pip+'" and b.status=="done"'
    
    //console.log(cmd)
    
    $.ajax({
        url: machine+"consult",
        type: "POST",
        async: true,
        data: JSON.stringify({sql:cmd}),
        contentType: "application/json; charset=utf-8",
        success: function(x) {
            //console.log(x)
            $("#selectSampleToCompare").append('<h2>'+pnames[ipid]+"</h2>")
          for(i=0; i<x.data.length;i++){
            //if(x.data[i]['']=="done"){
              //console.log(JSON.parse(Base64.decode(x.data[i].parameters)))
              $("#selectSampleToCompare").append('<input type="checkbox" name="selectSampleToCompare" value="'+x.data[i]['sample_id']+"_"+pid+":"+x.data[i]['sample_name']+'" checked > <b>'+x.data[i]['sample_name']+'</b>  ('+x.data[i]['sample_id']+')<br>')
            //}
          }
  
          $("#numSamples").append("<b>"+pnames[ipid]+"</b>. ("+x.data.length +" samples)<br><br>")
          $("#sidePipeline").html(pip+" pipeline")
          
          $('input').iCheck({
           checkboxClass: 'icheckbox_square-blue',
           radioClass: 'iradio_square-blue',
           increaseArea: '20%' // optional
          });
  
  
        }
    });
    
  });
  
  
  
  
  
  
  
  
  
  
  
  // get the databases where you have used to run
  
  rids={}
  pids.forEach(function(pid,ipid,pids){
    $.ajax({
        url: machine+"consult",
        type: "POST",
        async: true,
        //data: JSON.stringify({sql:'select distinct c.datasets, c.reference_name, c.reference_description, c.taxofile, c.functfile from (select a.project_id, a.datasets, b.reference_name, b.reference_description, b.taxofile, b.functfile from '+pip+' a inner join reference b on a.datasets=b.reference_id and b.status="done") c where c.project_id="'+pid+'"'}),
        data: JSON.stringify({sql:'select distinct c.datasets, c.reference_name, c.reference_description, c.taxofile, c.functfile from '+
                             ' (select a.project_id, a.datasets, b.reference_name, b.reference_description, b.taxofile, b.functfile from '+pip+
                             ' a inner join reference b on a.datasets=b.reference_id and b.status="done") c where c.project_id="'+pid+'"'}),
        contentType: "application/json; charset=utf-8",
        success: function(x) {
            //console.log(x)      
          for(i=0; i<x.data.length; i++){
              
              
              
              if (rids[x.data[i]['c.datasets']]!=true) {
                            
                if(x.data[i]['c.taxofile']!="none"){
                    $("#selectDataset").append('<option value='+x.data[i]['c.datasets']+'>'+x.data[i]['c.reference_name']+'</option>')
                }
                if(x.data[i]['c.functfile']!="none"){
                    $("#selectDatasetf").append('<option value='+x.data[i]['c.datasets']+'>'+x.data[i]['c.reference_name']+'</option>')
                }
                
                rids[x.data[i]['c.datasets']]=true
              }
              
          }
        }
    });
  });
  
  
  
  
  
  
  
  
enable_st_ht =  function(type,div){
  if (type=="ht") {
    $(div+"_ht").show()
    $(div).hide()
  }else{
    $(div+"_ht").hide()
    $(div).show()
  }
}  
  
  
  
  
var get_checkbox2=function(name){
    var sel=$('input[name="'+name+'"]:checked').map(function(_, el) {
        return $(el).val().split("_")[1];
    }).get();
    return(sel)
  }
  
  
  
  
  
var display_stack_taxonomy = function(level, div){

  //var pip = $( "#selectPipeline option:selected" ).val();
  var rid = $( "#selectDataset option:selected" ).val();
  sel = get_checkbox("selectSampleToCompare")
  var norm = $( "#selectNormalization option:selected" ).val();
  height=$("#pie1taxomain").height()
  var minA = parseFloat($( "#minA" ).val());
  
  //console.log(sel)
  
  snm =get_checkbox2("selectSampleToCompare")
  
  var b2 = parseFloat($( "#b2" ).val());
  var e2 = parseFloat($( "#e2" ).val());
  
  //$("#PieChart1Taxo").height(height)
  //$("#tree").html('')
  //$("#PieChart1Taxo").html("")
  sendv={uid:uid, pids:pids, sid:sel, pip:pip, rid:rid, lid:level, minA:minA, norm:norm, snames:snm, ib:b2, ie:e2}
  //console.log(sendv)
  
  
  $.ajax({
      url: machine+"get_multiple_projects",
      type: "POST",
      async: true,
      data: JSON.stringify(sendv),
      contentType: "application/json; charset=utf-8",
      success: function(x) {
          //console.log(x)
          //$("#tree").height("600")
          //ptree(x.tree,[0,pip.length/2,pip.length],"#tree",1,"id",'samples',width=3000, height=525, rsize=10, condition="mult", pip, rid)
          cl=x.heatmap.data.feature_names.length
          clsize=10*10 + 200;
          //console.log(x.heatmap)
          if(clsize>1000){clsize=1500}
          if(cl<100){clsize=800}
          clustergram(div+"_ht",x.heatmap, clsize)
          
          stk=process_stacked2(x.matrix, x.h)
          
          //console.log(stk)
          //return stk
          stacked("#"+div,stk[1],stk[0])
          //draw_heat_map("#PieChart1Taxo",x.data,x.xlabs, x.ylabs,250,0.1,1)
      }
  });
  
  
}
  
  
  
  
  /*Get combined tree when click on COMPARE*/
$(document).on("click","#compareSamplesButton", function(){
  var rid = $( "#selectDataset option:selected" ).val();
  var norm = $( "#selectNormalization option:selected" ).val();
  var minA = parseFloat($( "#minA" ).val());
  sel = get_checkbox("selectSampleToCompare")
  snm =get_checkbox_text("selectSampleToCompare")

  display_stack_taxonomy("Domain", "stack_domain")
  display_stack_taxonomy("Phylum", "stack_phylum")
  display_stack_taxonomy("Class", "stack_class")
  display_stack_taxonomy("Order", "stack_order")
  display_stack_taxonomy("Family", "stack_family")
  display_stack_taxonomy("Genus", "stack_genus")
  display_stack_taxonomy("Species", "stack_species")


});

  
  
  
































$(document).on("click","#compareSamplesButtonf", function(){
 
 
  var rid = $( "#selectDatasetf option:selected" ).val();
  var minA = parseFloat($( "#minA" ).val());
  var b = parseFloat($( "#b" ).val());
  var e = parseFloat($( "#e" ).val());
  sel = get_checkbox("selectSampleToCompare")
  snm =get_checkbox2("selectSampleToCompare")
  var norm = $( "#selectNormalizationF option:selected" ).val();
  
  console.log(rid, sel, snm, norm,b,e)
  
  $("#stackedplotf").html("")
  $("#stackedplot").height("600")
  $("#stackedplot").width('auto')
  //$("#PieChart1Taxo").html("")
  sent={uid:uid, pids:pids, sid:sel, pip:pip, rid:rid, lid:"Phylum", minA:minA, norm:norm, ib:b, ie:e, snames:snm}
  //console.log(sent)
  $.ajax({
      url: machine+"get_multiple_projects",
      type: "POST",
      async: true,
      data: JSON.stringify(sent),
      contentType: "application/json; charset=utf-8",
      success: function(x) {

          //$("#tree").attr("height","1200")
          clsize=x.heatmap.data.feature_names.length*10 + 200;
          if(clsize>1000){clsize=1000}
          
          clustergram("HeatMapFun",x.heatmap, clsize)
          stk=process_stacked2(x.matrix)
          stacked("#stackedplotf",stk[1],stk[0])

        
      }
  });

});
  

  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
}