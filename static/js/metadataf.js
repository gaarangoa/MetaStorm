

window.onload=function(){
   // Project setup table
   // table with all the results from the assembly -  this is an overall of the assembly performance



  var headerRenderer = function (instance, td, row, col, prop, value, cellProperties) {
    Handsontable.renderers.TextRenderer.apply(this, arguments);
    td.style.fontWeight = 'bold';
    td.style.textAlign = 'center';
    td.style.backgroundColor = '#BDD7EE';
  };

  document.getElementById("NumberSamples").onchange = function() {setupNumberSamples()};

  var setupNumberSamples = function(){
      $('#table').html('')
      var container = document.getElementById('table');
      var totalsamples = document.getElementById("NumberSamples").value;

      matrix=[['Sample name','Sample set','Environment','Library preparation','Reads 1','Reads 2']]
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
    }

  $(document).on('click',"#SubmitProject",function() {

      var PyProjectName = $("#ProjectName").val()
      var PyProjectShortDescription = $("#ProjectShortDescription").val()
      var PyProjectDescription = $("#ProjectDescription").val()


      $.getJSON($SCRIPT_ROOT + '/_insertproject', {
  			PyProjectName: PyProjectName, PyProjectShortDescription:PyProjectShortDescription, PyProjectDescription:PyProjectDescription
      }, function(data){
        $("#LProjectID").html(data.ProjectID)
        $("#STProjectID").val(data.ProjectID)
      });
    });


  $(document).on('click',"#uploadFiles1",function() {

        $.getJSON($SCRIPT_ROOT + '/_test', {
    			PyProjectName: "test"
        }, function(data){
          alert(data)
        });
      });



  var retrieve_hst = function(x){
      var data=[]

      //split("</td>")[9].replace(/<*.*>/,"")
      var nested_data=x.split("<tr>")

      for(var i=1;i<nested_data.length;i++){
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
      var ProjectID=$("#LProjectID").text()
      //alert($("#table")())

      retrieve_hst($("#table").html())

    });

};
