

window.onload=function(){

machine="/MetaStorm/"

   uid=urlParam('uid')
   /*Get the user, projects and samples info*/

   var update=function(){
    $.ajax({
       url: machine+"GetAllInfo",
       type: "POST",
       data: JSON.stringify({uid:uid}),
       contentType: "application/json; charset=utf-8",
       success: function(dat) {
         console.log(dat)
         $("#UserName1").html(dat.uname)
         $("#userID").html(dat.uid)
         $("#UserContact").html(dat.email)
          $("#ProjectNameSelect").html("")
       }
    });
   }

   update()


























/*register the new dataset*/

$(document).on("click","#register_dataset", function(){

  rname=$("#rname").val()
  rtype=$("#rtype").val()
  rdesc=$("#rdesc").val()

  if(rname.length==0 || rtype.length==0 || rdesc.length==0){alert("Error! you must fill all the filelds!");}
  else{

    $.ajax({
        url: machine+"register_dataset",
        type: "POST",
        data: JSON.stringify({uid:uid, rname:rname, rtype:rtype, rdesc:rdesc}),
        contentType: "application/json; charset=utf-8",
        success: function(dat) {
            console.log(dat)
          $("#r1s2").show()
          $("#register_dataset").hide()
          $("#uinfo").val([dat.rid])
        }
    });
  }


});



/* Upload a new reference dataset*/
$('#upload-file-btn').click(function() {

   $("#upload_data_panel").append("<div class='overlay' id='upload_data_panel_overlay'><i class='fa fa-refresh fa-spin'></i></div>")

    var form_data = new FormData($('#upload-file')[0]);
    $.ajax({
        type: 'POST',
        url: machine+'uploadref',
        data: form_data,
        //data: JSON.stringify({pid:pid}),
        contentType: false,
        cache: false,
        processData: false,
        async: true,
        success: function(data) {
            alert("File has been uploaded!")
            console.log(data)
          $("#rsequences").append('<option value="'+data.fname+'">'+data.fname+'</option>')
          $("#rtaxonomy").append('<option value="'+data.fname+'">'+data.fname+'</option>')
          $("#rfunction").append('<option value="'+data.fname+'">'+data.fname+'</option>')
          
          $("#upload_data_panel_overlay").remove()
          
        },
    });


});



/*Process dataset*/

$(document).on("click","#process_data_set", function(){

   
   $("#upload_data_panel").append("<div class='overlay' id='upload_data_panel_overlay'><i class='fa fa-refresh fa-spin'></i></div>")

  rname=$("#rname").val()
  rid=$("#uinfo").val()
  seqfile = $( "#rsequences option:selected" ).val();
  taxofile = $( "#rtaxonomy option:selected" ).val();
  functfile = $( "#rfunction option:selected" ).val();
  drequest={uid:uid, rname:rname, rid:rid, seqfile:seqfile, taxofile:taxofile, functfile:functfile}
  console.log(drequest)
  $.ajax({
      url: machine+"process_up_ref_dataset",
      type: "POST",
      data: JSON.stringify(drequest),
      contentType: "application/json; charset=utf-8",
      success: function(dat) {
        console.log(dat)
        $("#upload_data_panel_overlay").remove()
        alert("the dataset: "+rname+"has been stored and processed into the server!")
      }
  });

});












};
