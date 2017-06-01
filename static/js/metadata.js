
   // Project setup table
   // table with all the results from the assembly -  this is an overall of the assembly performance


  userID=urlParam('uid')
  /*Get the user, projects and samples info*/

machine="/MetaStorm/"

  $.ajax({
      //url: "/zhanglab/software/CMetAnn/start.wsgi/GetAllInfo",
      url: machine+"GetAllInfo",
      type: "POST",
      data: JSON.stringify({uid:userID}),
      contentType: "application/json; charset=utf-8",
      success: function(dat) {
        $("#UserName1").html(dat.uname)
        $("#userID").html(dat.uid)
        $("#UserContact").html(dat.email)
        $("#NewSampleBody").append(dat.projects)
      }
  });


   var countFilesUpload=0;

  var headerRenderer = function (instance, td, row, col, prop, value, cellProperties) {
    Handsontable.renderers.TextRenderer.apply(this, arguments);
    td.style.fontWeight = 'bold';
    td.style.textAlign = 'center';
    td.style.backgroundColor = '#BDD7EE';
  };


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


















  $(document).on('click',"#SubmitProject",function() {

      userID=$.urlParam('uid')

      var PyProjectName = $("#ProjectName").val()
      var PyProjectShortDescription = $("#ProjectShortDescription").val()
      var PyProjectDescription = $("#ProjectDescription").val()

      //$("#MainProjectSetup").remove()

      //$("#updateProjectSetupForm").show()

      $.ajax({
          url: machine+"insertproject",
          type: "POST",
          data: JSON.stringify({name: PyProjectName, description: PyProjectDescription, userID: userID}),
          contentType: "application/json; charset=utf-8",
          success: function(dat) {
              console.log(dat)
              //update_project(dat)
              alert("The project has been created")
              location.reload()
          }
      });
    });


  var update_project = function(x){
    pname=x.name;
    pid=x.id;
    pdescription=x.description;

    $("#updatePname").text(pname)
    $("#updatePid").text(pid)
    $("#updatePdescription").text(pdescription)

    $("#setProjectNameinLoad").val(pid)
    $("#SamplesSetupMain").show()

    $("#StatusBarLabel").text("20%")
    $("#StatusBar").html('<div  class="progress-bar progress-bar-danger" style="width: 20%"></div>')
  }
















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

  $(document).on("click","#submitMetagenome", function(){
      var ProjectID=$("#updatePid").text()
      //alert($("#table")())

      samples=retrieve_hst($("#table").html())



      $.ajax({
          url: "/insertsamples",
          type: "POST",
          data: JSON.stringify({samples: samples, pid:ProjectID}),
          contentType: "application/json; charset=utf-8",
          success: function(data) {
            for(i=0; i<data.samples.length;i++){
              $("#SampleNameSelect").append('<option value='+data.samples[i].id+'>'+data.ids[data.samples[i].id]+'</option>')
            }
          }
      });

      $("#samplesTitle").html("Samples")
      $("#NumberSamples").prop("disabled", true);
      $("#buttonhide").hide();

      $("#UploadFilesMain").show()

      $("#StatusBarLabel").text("60%")
      $("#StatusBar").html('<div  class="progress-bar progress-bar-danger" style="width: 60%"></div>')

    });






















      $('#upload-file-btn').click(function() {
          var form_data = new FormData($('#upload-file')[0]);
          $.ajax({
              type: 'POST',
              url: '/uploadajax',
              data: form_data,
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



















    $(document).on("click","#RunMetaGen", function(){
        var ProjectID=$("#updatePid").text()

        var sid = $( "#SampleNameSelect option:selected" ).val();
        var read1 = $( "#Read1Select option:selected" ).val();
        var read2 = $( "#Read2Select option:selected" ).val();
        var pipeline = $( "#PipelineSelect option:selected" ).val();

        $.ajax({
            url: "/RunMetaGen",
            type: "POST",
            async: true,
            data: JSON.stringify({uid:userID, pid:ProjectID, sid:sid, read1:read1, read2:read2, pipeline:pipeline}),
            contentType: "application/json; charset=utf-8",
            success: function(dat) {alert(sid+'done!')}
        });

    });
