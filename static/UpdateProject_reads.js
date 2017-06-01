

window.onload=function(){
   // Project setup table
   // table with all the results from the assembly -  this is an overall of the assembly performance


  uid=urlParam('uid')
  pid=urlParam('pid')
  pip=urlParam('pip')


  $("#setProjectNameinLoad").val(pid)
  console.log(pid)

  /*Get the user, projects and samples info*/

  $.ajax({
      url: "/GetAllInfo",
      type: "POST",
      data: JSON.stringify({uid:uid}),
      async: true,
      contentType: "application/json; charset=utf-8",
      success: function(dat) {
        $("#UserName1").html(dat.uname)
        $("#userID").html(dat.uid)
        $("#UserContact").html(dat.email)
      }
  });

  $.ajax({
      url: "/consult",
      type: "POST",
      async: true,
      data: JSON.stringify({sql:'select * from project where project_id="'+pid+'"'}),
      contentType: "application/json; charset=utf-8",
      success: function(x) {
        //alert(x.data[0])
        $("#updatePdescription").html("<b>Description: </b> "+x.data[0][3])
        $("#updatePname").html("<b>Name: </b>"+x.data[0][1])
      }
  });


 /*Load root reference databases*/
 $.ajax({
     url: "/consult",
     type: "POST",
     async: true,
     data: JSON.stringify({sql:'select reference_id, reference_name, status from reference where user_id="root"'}),
     contentType: "application/json; charset=utf-8",
     success: function(x) {
       //alert(x.data)
       for(i=0; i<x.data.length;i++){
         if(x.data[i][2]=="done" && x.data[i][0]!="MyTaxa"){
           $("#selectTaxonomyDatabase").append('<input type="checkbox" name="selectedReferenceDatasets" value="'+x.data[i][0]+'" > '+x.data[i][1]+'<br>')
         }
       }

       $('input').iCheck({
        checkboxClass: 'icheckbox_square-blue',
        radioClass: 'iradio_square-blue',
        increaseArea: '20%' // optional
       });

     }
 });

//


/*Load my reference databases*/
$.ajax({
    url: "/consult",
    type: "POST",
    async: true,
    data: JSON.stringify({sql:'select reference_id, reference_name, status from reference where user_id="'+uid+'"'}),
    contentType: "application/json; charset=utf-8",
    success: function(x) {
      //alert(x.data)
      $("#myDatasets").html('')
      for(i=0; i<x.data.length;i++){
        if(x.data[i][2]=="done"){
          $("#myDatasets").append('<input type="checkbox" name="selectedReferenceDatasets" value="'+x.data[i][0]+'" > '+x.data[i][1]+'<br>')
        }
      }

      $('input').iCheck({
       checkboxClass: 'icheckbox_square-blue',
       radioClass: 'iradio_square-blue',
       increaseArea: '20%' // optional
      });

    }
});

/*Load others reference databases search by keywords*/
$.ajax({
    url: "/consult",
    type: "POST",
    async: true,
    data: JSON.stringify({sql:'select reference_id, reference_name, status from reference where user_id="'+uid+'"'}),
    contentType: "application/json; charset=utf-8",
    success: function(x) {
      //alert(x.data)
      for(i=0; i<x.data.length;i++){
        if(x.data[i][2]=="done"){
          //$("#myDatasets").append('<input type="checkbox" name="selectedReferenceDatasets" value="'+x.data[i][0]+'" > '+x.data[i][1]+'<br>')
        }
      }

      $('input').iCheck({
       checkboxClass: 'icheckbox_square-blue',
       radioClass: 'iradio_square-blue',
       increaseArea: '20%' // optional
      });

    }
});
















  /*Load current samples the main table with the samples info*/

  var headerRenderer = function (instance, td, row, col, prop, value, cellProperties) {
    Handsontable.renderers.TextRenderer.apply(this, arguments);
    //td.style.fontWeight = 'bold';
    td.style.color = 'white'
    td.style.textAlign = 'center';
    td.style.backgroundColor = 'rgba(0,125,10,1)';
  };

  var actionHTML = function (instance, td, row, col, prop, value, cellProperties) {

    $(td).html("<a href='/ViewSample_reads?sid="+value+"&pid="+pid+"&uid="+uid+"&pip="+pip+"'>"+value+"</a>"); //empty is needed because you are rendering to an existing cell
  };

  var get_samples_info=function(){
      cmd='select sample_id, sample_name, sample_set, environment, library_preparation, reads1, reads2, "Reads" from samples where project_id=="'+pid+'"'
      $.ajax({
          url: "/consult",
          type: "POST",
          //data: JSON.stringify({sql:'select sample_id, sample_name, sample_set, environment, library_preparation, reads1, reads2 from samples where project_id="'+pid+'"'}),
          data: JSON.stringify({sql:cmd}),
          contentType: "application/json; charset=utf-8",
          success: function(x) {
            //alert(x.data[0])

            data=[{ID:"ID",Name:"Name",Condition:"Condition",Environment:"Environment",Library:"Library",Mate1:"Mate1",Mate2:"Mate2",Status:"Status"}]

            for(i=0; i<x.data.length; i++){
              item={ID:x.data[i][0],Name:x.data[i][1],Condition:x.data[i][2],Environment:x.data[i][3],Library:x.data[i][4],Mate1:x.data[i][5],Mate2:x.data[i][6],Status:x.data[i][7]}
              data.push(item)
            }

            $("#BodyCurrentSamples").html('')
            var container = document.getElementById('BodyCurrentSamples');

            var previous_samples = new Handsontable(container, {
              data:data,
              colHeaders: false,
              rowHeaders: false,
              columnSorting: true,
              //manualColumnResize: true,
              fixedRowsTop: 1,
              manualColumnMove: false,
              manualRowMove: false,
              columns:[{data:"ID",renderer:actionHTML},
                      {data:"Name"},
                      {data:"Condition"},
                      {data:"Environment"},
                      {data:"Library"},
                      {data:"Mate1"},
                      {data:"Mate2"},
                      {data:"Status"}],
              cells: function (row, col, prop) {
               var cellProperties = {};
               if (row === 0) {
                 cellProperties.renderer = headerRenderer;
               }

               return cellProperties;
              },
            });

            /*setup the samples for selection*/
            $("#SampleNameSelectToRemove").html('<option>Sample ID</option>')
            $("#SampleNameSelect").html("<option>Name</option>")
            $("#Read1Select").html("<option>Fastq 2</option>")
            $("#Read2Select").html("<option>Fastq 2</option>")

            for(i=0;i<x.data.length;i++){
              $("#SampleNameSelectToRemove").append('<option value='+x.data[i][0]+'>'+x.data[i][0]+'</option>')
              $("#SampleNameSelect").append('<option value='+x.data[i][0]+'>'+x.data[i][1]+'</option>')
              $("#Read1Select").append('<option value='+x.data[i][5]+'>'+x.data[i][5]+'</option>')
              $("#Read2Select").append('<option value='+x.data[i][6]+'>'+x.data[i][6]+'</option>')

            }

          }
      });
  }

  get_samples_info()





































/*send action to sql*/
// this function is useful if I want to send some sql-based code -  only works with the main database
var exql=function(consult){
  $.ajax({
      url: "/consult",
      type: "POST",
      async: true,
      data: JSON.stringify({sql:consult}),
      contentType: "application/json; charset=utf-8",
      success: function(dat) {get_samples_info()}
  });
}

/*remove samples*/
$(document).on("click","#RemoveSample", function(){
    var sid = $( "#SampleNameSelectToRemove option:selected" ).val();
    exql('delete from samples where project_id="'+pid+'" and sample_id="'+sid+'"')
    exql('delete from project_status where project_id="'+pid+'" and sample_id="'+sid+'"')
});






























/*compare samples*/
$(document).on("click","#RunComparativeAnalysis", function(){
  alert()
  window.open("/compare_samples?pid="+pid+"&uid="+uid+"&pip="+pip)
});

























/*when click on insert show the insert form*/
$(document).on("click","#InsertSample", function(){
  $("#SamplesSetupMain").show()
  $("#InsertSample").hide()

});



/*when click on insert show the remove sample form*/
$(document).on("click","#RemoveSampleGO", function(){
  $("#RemoveSampleForm").show()
});


/*when click refresh the sample list form*/
$(document).on("click","#RefreshSampleGetForm", function(){
  get_samples_info()
});


/*when click rerun show update and submit forms*/
$(document).on("click","#ReRunSampleGetForm", function(){
    $("#UploadFilesMain").show()
    $("#RunMetaGenMain").show()
});

















/*Insert new sample*/
   var countFilesUpload=0;


  document.getElementById("NumberSamples").onchange = function() {setupNumberSamples()};

  var setupNumberSamples = function(){

    $('#table').html('')
    var container = document.getElementById('table');
    var totalsamples = document.getElementById("NumberSamples").value;

    matrix=[['SampleName','Sample set','Environment','Library preparation']]
    for(var i=0; i<totalsamples; i++){
      matrix.push([])
    }

    var hot = new Handsontable(container, {
      data:matrix,
      colHeaders: false,
      rowHeaders: false,
      columnSorting: false,
      cells: function (row, col, prop) {
       var cellProperties = {};
       if (row === 0) {
         cellProperties.renderer = headerRenderer;
       }

       return cellProperties;
      },
    });
  };


  var retrieve_hst = function(x){
    var data=[]

    //split("</td>")[9].replace(/<*.*>/,"")
    var nested_data=x.split("<tr>")

    for(var i=2;i<nested_data.length;i++){
      var r=nested_data[i].split("</td>")
      var item=[]
      for(var j=0; j<r.length-1; j++){
        item.push(r[j].replace(/<*.*>/,""))
      }
      data.push(item)
    }
    return(data)
  }

// inser samples information into the sql database
  $(document).on("click","#submitMetagenome", function(){
      samples=retrieve_hst($("#table").html())

      $.ajax({
          url: "/insertsamples",
          type: "POST",
          data: JSON.stringify({samples: samples, pid:pid, uid:uid}),
          async: false,
          contentType: "application/json; charset=utf-8",
          success: function(data) {
            for(i=0; i<data.samples.length;i++){
              $("#SampleNameSelect").append('<option value='+data.samples[i].id+'>'+data.ids[data.samples[i].id]+'</option>')
            }
          }
      });

      //$("#samplesTitle").html("Samples")
      //$("#NumberSamples").prop("disabled", true);
      //$("#buttonhide").hide();

      $("#UploadFilesMain").show()
      $("#setProjectNameinLoad").val(pid)

      $("#i1c").html('<i class="fa fa-plus">')

    });



















/*Upload files*/
      $('#upload-file-btn').click(function() {
          var form_data = new FormData($('#upload-file')[0]);
          $.ajax({
              type: 'POST',
              url: '/uploadajax',
              data: form_data,
              //data: JSON.stringify({pid:pid}),
              contentType: false,
              cache: false,
              processData: false,
              async: true,
              success: function(data) {
                  $("#RunMetaGenMain").show()
                  $("#Read1Select").append('<option value='+data+'>'+data+'</option>')
                  $("#Read2Select").append('<option value='+data+'>'+data+'</option>')
              },
          });


          countFilesUpload++;
          TotalSamples=2*$("#NumberSamples").val()

          //alert(TotalSamples)

          $("#StatusBarLabel").text((60+countFilesUpload*40/TotalSamples).toString()+"%")
          $("#StatusBar").html('<div  class="progress-bar progress-bar-danger" style="width:' +(60+countFilesUpload*40/TotalSamples).toString()+'%"></div>')


      });

















































/*Run pipeline ---- there are two options 1 is for reads mapping and 2 for metagenome assembly*/


    $(document).on("click","#RunMetaGen", function(){
        var sid = $( "#SampleNameSelect option:selected" ).val();
        var read1 = $( "#Read1Select option:selected" ).val();
        var read2 = $( "#Read2Select option:selected" ).val();
        var rids = get_checkbox("selectedReferenceDatasets")

        $.ajax({
            url: "/RunMetaGen",
            type: "POST",
            async: true,
            data: JSON.stringify({uid:uid, pid:pid, sid:sid, read1:read1, read2:read2, pip:pip, rids:rids}),
            contentType: "application/json; charset=utf-8",
            success: function(dat) {
              alert('You are analyzing the sample: '+sid+'!')
              get_samples_info()
            }
        });
    });





































































/*****************************************************************************
               Setup databases and pipeline options
*****************************************************************************/

/*1. Read matching pipeline!*/














/**/





};
