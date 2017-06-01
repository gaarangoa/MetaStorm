<!DOCTYPE html>
<!--
This is a starter template page. Use this page to start your new project from
scratch. This page gets rid of all links and provides the needed markup only.
-->
<html>
  <head>
    <meta charset="UTF-8">
    <title>MetaStorm | UpdateProject</title>
    <!-- Tell the browser to be responsive to screen width -->
    <meta content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no" name="viewport">
    <!-- Bootstrap 3.3.4 -->
    <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='template/bootstrap/css/bootstrap.min.css') }}"></link>
    <!-- Font Awesome Icons -->
    <link href="https://maxcdn.bootstrapcdn.com/font-awesome/4.3.0/css/font-awesome.min.css" rel="stylesheet" type="text/css" />
    <!-- Ionicons -->
    <link href="https://code.ionicframework.com/ionicons/2.0.1/css/ionicons.min.css" rel="stylesheet" type="text/css" />
    <!-- Theme style -->
    <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='template/dist/css/AdminLTE.css') }}"></link>
    <!-- AdminLTE Skins. We have chosen the skin-blue for this starter
          page. However, you can choose any other skin. Make sure you
          apply the skin class to the body tag so the changes take effect.
    -->

    <!-- i check library -->
    <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='icheck/skins/square/blue.css') }}"></link>





    <!-- main color page -->
    <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='template/dist/css/skins/skin-blue.min.css') }}"></link>



    <!-- HTML5 Shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
        <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
        <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->


    <style>
    h1 { padding: .2em; margin: 0; }
    #products { float:left; width: 500px; margin-right: 2em; }
    #cart { width: 200px; float: left; margin-top: 1em; }
    /* style the list to maximize the droppable hitarea */
    #cart ol { margin: 0; padding: 1em 0 1em 3em; }
    </style>


    <!-- pretty tables -->
    <link href="http://handsontable.com//bower_components/handsontable/dist/handsontable.full.min.css" rel="stylesheet">
		<script src="http://handsontable.com//bower_components/handsontable/dist/handsontable.full.min.js"></script>


    <script>
      var $SCRIPT_ROOT = {{ request.script_root|tojson|safe }};
		</script>

  </head>
  <!--
  BODY TAG OPTIONS:
  =================
  Apply one or more of the following classes to get the
  desired effect
  |---------------------------------------------------------|
  | SKINS         | skin-blue                               |
  |               | skin-black                              |
  |               | skin-purple                             |
  |               | skin-yellow                             |
  |               | skin-red                                |
  |               | skin-green                              |
  |---------------------------------------------------------|
  |LAYOUT OPTIONS | fixed                                   |
  |               | layout-boxed                            |
  |               | layout-top-nav                          |
  |               | sidebar-collapse                        |
  |               | sidebar-mini                            |
  |---------------------------------------------------------|
  -->
  <body class="skin-blue sidebar-mini" >


    <div class="wrapper">


      <!-- Main Header -->
      <header class="main-header">

        <!-- Logo -->
        <a href="index2.html" class="logo">
          <!-- mini logo for sidebar mini 50x50 pixels -->
          <span class="logo-mini"><b>M</b>S</span>
          <!-- logo for regular state and mobile devices -->
          <span class="logo-lg"><b>Meta</b>Storm</span>
        </a>

        <!-- Header Navbar -->
        <nav class="navbar navbar-static-top" role="navigation">
          <!-- Sidebar toggle button-->
          <a href="#" class="sidebar-toggle" data-toggle="offcanvas" role="button">
            <span class="sr-only">Toggle navigation</span>
          </a>
          <!-- Navbar Right Menu -->
          <div class="navbar-custom-menu">
            <ul class="nav navbar-nav">

              <!-- Tasks Menu -->
              <li class="dropdown tasks-menu">
                <!-- Menu Toggle Button -->
                <a href="#" class="dropdown-toggle" data-toggle="dropdown">
                  <i class="fa fa-flag-o"></i>
                  <span class="label label-danger">9</span>
                </a>
                <ul class="dropdown-menu">
                  <li class="header">Your assembly is done</li>
                  <li>
                    <!-- Inner menu: contains the tasks -->
                    <ul class="menu">
                      <li><!-- Task item -->
                        <a href="#">
                          <!-- Task title and progress text -->
                          <h3>
                            Project analysis
                            <small class="pull-right">100%</small>
                          </h3>
                          <!-- The progress bar -->
                          <div class="progress xs">
                            <!-- Change the css width attribute to simulate progress -->
                            <div class="progress-bar progress-bar-aqua" style="width: 100%" role="progressbar" aria-valuenow="20" aria-valuemin="0" aria-valuemax="100">
                              <span class="sr-only">100% Complete</span>
                            </div>
                          </div>
                        </a>
                      </li><!-- end task item -->
                    </ul>
                  </li>
                  <li class="footer">
                    <a href="#">View all tasks</a>
                  </li>
                </ul>
              </li>
              <!-- User Account Menu -->

              <!-- Control Sidebar Toggle Button -->
              <li>
                <a href="#" data-toggle="control-sidebar"><i class="fa fa-gears"></i></a>
              </li>
            </ul>
          </div>
        </nav>
      </header>

      <!-- Left side column. contains the logo and sidebar -->
      <aside class="main-sidebar">

        <!-- sidebar: style can be found in sidebar.less -->
        <section class="sidebar">

          <!-- Sidebar user panel (optional) -->
          <div class="user-panel">
            <div class="pull-left image">
              <img src="/MetaStorm/static/template/dist/img/user.png" class="img-circle" alt="User Image" />
            </div>
            <div class="pull-left info">
              <p id="UserName1"></p>
              <p id="userID"></p>
              <p id="UserContact"></p>
            </div>
          </div>

          <!-- search form (Optional) -->
          <form action="#" method="get" class="sidebar-form">
            <div class="input-group">
              <input type="text" name="q" class="form-control" placeholder="Search..." />
              <span class="input-group-btn">
                <button type="submit" name="search" id="search-btn" class="btn btn-flat"><i class="fa fa-search"></i></button>
              </span>
            </div>
          </form>
          <!-- /.search form -->

          <ul id='sidemenu' class="sidebar-menu">
            <li class="active"><a onclick=logout(userID)><i class="fa fa-sign-out"></i> <span>Log out</span></a></li>
          </ul>
        </section>
        <!-- /.sidebar -->
      </aside>




































      <!-- Content Wrapper. Contains page content -->
      <div class="content-wrapper" style="height:1850px">
        <!-- Content Header (Page header) -->

        <!-- Main content -->
        <!--############################-->

        <?php echo "PhP is working but only when it is loaded by the server itself, without the python library"; ?>












        <div class="col-md-12" >
          <div class="box" id="" style='background:url("/MetaStorm/static/template/dist/img/pattern1.jpg");'>
             <div class="box-header">
               <h3 class="box-title"></h3>
               <div class="box-tools pull-right">
                 <button class="btn btn-box-tool" data-widget="collapse"><i class="fa fa-minus"></i></button>
               </div><!-- /.box-tools -->
            </div><!-- /.box-header -->
            <br>
               <div class="box-body">
                 <center><h1 style='font-family: "Lucida Sans Unicode", "Lucida Grande", sans-serif; color:rgba(255,255,255,0.9)'>Unassembled Reads Profile</h1></center>
               </div>
               <br><br><br>

           </div><!-- /.box -->
        </div>





                <br>
                <div class="nav-tabs-custom">
                   <ul class="nav nav-tabs"  >
                     <li><a href="#pinfo" data-toggle="tab"><h4>Project</h4></a></li>
                     <li class="active"><a href="#samfo" data-toggle="tab"><h4>Samples</h4></a></li>
                     <li><a href="#inso" data-toggle="tab"><h4>Add Samples</h4></a></li>
                     <li><a href="#remo" data-toggle="tab"><h4>Remove Samples</h4></a></li>
                     <li><a href="#runo" data-toggle="tab"><h4>Run Samples</h4></a></li>
                     <li class="pull-right"><a href="#" class="text-muted"><i class="fa fa-gear"></i></a></li>
                   </ul>



                   <div class="tab-content" >



                     <div class="tab-pane" id="pinfo" >

                        <!-- <img src="/MetaStorm/static/template/dist/img/user.png" class="img-circle" alt="User Avatar" /> -->
                        <div class='col-md-6' style='top:20px'>
                            <div class='box box-solid'>
                                <dl class="dl-horizontal">
                                    <dt>Project Name: </dt>
                                    <dd id="updatePname"></dd>
                                    <dt>Description</dt>
                                    <dd id="updatePdescription"></dd>
                                    <dt>Total number of samples:</dt>
                                    <dd id="updateNumberSamplesTab1"></dd>
                                    <!--<dt>Reference databases:</dt>
                                    <dd id="updateUsedDatabasesTab1"></dd> -->
                                </dl>
                            </div>
                            <h3>TimeLine</h3>
                            <!-- timeline time label
							<ul class="timeline">
                                <li class="time-label">
                                    <span class="bg-red">
                                        10 Feb. 2014
                                    </span>
                                </li>
                                <li>
                                    <i class="fa fa-envelope bg-blue"></i>
                                    <div class="timeline-item">
                                        <span class="time"><i class="fa fa-clock-o"></i> 12:05</span>

                                        <h3 class="timeline-header"><a href="#">Support Team</a> ...</h3>

                                        <div class="timeline-body">
                                            ...
                                            Content goes here
                                        </div>

                                        <div class="timeline-footer">
                                            <a class="btn btn-primary btn-xs">...</a>
                                        </div>
                                    </div>
                                </li>
                            </ul>							
                                END timeline item -->
                        </div>
                     </div><!-- /.tab-pane -->




                     <div  class="tab-pane active" id="samfo">

                       <div style="height:auto; width:auto; overflow:auto; left:10px"  id="BodyCurrentSamples"></div>
                       <br>
                      <div class="box-footer">
                          <!--<button id="InsertSample" class="btn btn-primary"><i class="fa fa-plus"></i> Insert</button>
                          <button id="ViewSample" class="btn btn-success"><i class="fa fa-plus"></i> View</button>
                          <button id="ReRunSampleGetForm" class="btn btn-success"><i class="fa fa-plus"></i> Re-run</button>
                          <button id="RemoveSampleGO" class="btn btn-warning"><i class="fa fa-minus"></i> Remove</button>-->
                          <button  id="RefreshSampleGetForm" class="btn btn-success"><i class="fa fa-plus"></i> Refresh</button>
                          <button  id="RunComparativeAnalysis" class="btn btn-success"><i class="fa fa-plus"></i> Compare Sample Abundance</button>
                      </div>

                     </div><!-- /.tab-pane -->

                     <div  class="tab-pane" id="inso">

                       <div class="form-group">
                          <p>Upload new samples to the same project is very simple just follow the next steps: </p>
                            <ul>
                              <li> <b>Insert</b> the number of samples you want to aggregate into your project. </li>
                              <li> Click <b>outside</b> the box-label. </li>
                              <li> Once the table is loaded: <b>Fill</b> the fields on the table and click on submit.</li>
                            <ul>
                       </div>
                        <br>
                        <label for="NumberSamples">Number of samples to add</label>
                        <input type="text" style="width:auto" class="form-control" id="NumberSamples" placeholder="">
			<br>
			<button id="NumberSamplesButton" class="btn btn-success">GO</button>
                        <br>
			<br>
			<h2>Samples</h2>
                        <div id="table" style='height:100%; width:100%; overflow:auto'></div>
                        <br>
                        <button id="submitMetagenome" class="btn btn-primary" data-widget="collapse">Submit</button>

                     </div>



                     <div style="width:800px"  class="tab-pane" id="remo">
                        <label for="SampleNameSelectToRemove"> <h5>Select Sample ID: </h5></label>
                        <br>
                          <select id='SampleNameSelectToRemove'>
                            <option>Sample</option>
                          </select>
                        <br>
                        <br>
                        <button id="RemoveSample" class="btn btn-danger"><i class="fa fa-minus"></i> Remove</button>
                     </div>



                     <div class="tab-pane" id="runo">
                        <!-- <div class="col-md-4">
                          Custom Tabs -->
                        <div class="nav-tabs-custom">
                          <ul class="nav nav-tabs"  >
                            <li class="active"><a href="#tab_1" data-toggle="tab"><b>Reference Datasets</b></a></li>
                            <li><a href="#tab_2" data-toggle="tab"><b>Users reference datasets</b></a></li>
                            <li><a href="#tab_upo" data-toggle="tab"><b>Upload raw files</b></a></li>
                            <li><a href="#tab_runo" data-toggle="tab"><b>Submit</b></a></li>
                          </ul>

                          <div class="tab-content" >
                            <div class="tab-pane active" id="tab_1" >
                              <p>Please choose the datasets you want to run over your samples</p>


                                <form id="selectTaxonomyDatabase">
                                  <!--<input type="radio" name="iCheck">
                                  <input type="radio" name="iCheck" checked>-->
                                </form>




                            </div><!-- /.tab-pane -->
                            <div class="tab-pane" id="tab_2">
                                <h3>My Datasets</h3>
                                <br>
                                <div id="myDatasets">
                                </div>
                                <br>
                                <!--<h3>Find other databases by looking at keywords!</h3> -->
                            </div><!-- /.tab-pane -->

                            <div class="tab-pane" id="tab_upo">

                              <p>
                                Select all the read files for your samples. Note that the name of any read file has to be the same
                                as the name placed on the Metadata spreadsheet. If the names are not the same the program will
                                not run and automatically will trigger an exception.
                              </p>

                              <form id="upload-file" method="post" enctype="multipart/form-data">
                                  <fieldset>
                                      <label for="file">Select a file</label>
                                      <input id='uploaded_file' data-buttonBefore="true" data-buttonName="btn-info" class="filestyle" name="file" type="file">
                                      <input name="projectid" type='text' value="" id="setProjectNameinLoad" hidden>
                                  </fieldset>
                              </form>
                            <br>
                            <button id="upload-file-btn" type="button"  class="btn btn-primary">Upload</button>
                            <br>
                            <br>
                            <div style="width:100%" id="progress_upload_bar"></div>
                            <div style="width:100%" id="progress_upload_label"></div>

                            </div>


                            <div class="tab-pane" id="tab_runo">
                            <label for="SampleNameSelect"> <h5>Select Sample Name: <h5></label>
                              <select id='SampleNameSelect'>
                                <option>Name </option>
                              </select>
                               <br>
                               <label for="Read1Select"> <h5>Select Fastq mate-1 file: <h5></label>
                              <select id='Read1Select'>
                                <option>Fastq 1</option>
                              </select>
                              <br>
                              <label for="Read2Select"> <h5>Select Fastq mate-2 file: <h5></label>
                              <select id='Read2Select'>
                                <option>Fastq 2</option>
                              </select>
                             <br>
                             <br>
                            <button id="RunMetaGen" class="btn btn-primary">Submit</button>
                          </div>
                            </div><!-- /.tab-pane -->
                          </div><!-- /.tab-content -->
                        </div><!-- nav-tabs-custom -->
                          </div><!-- /.tab-pane -->
                     </div>





             </div><!-- /.box -->
          </div>





































































































































      </div><!-- /.content-wrapper -->









































      <!-- Main Footer -->
      <footer class="main-footer">
        <!-- To the right -->
        <div class="pull-right hidden-xs">
          Computer Science department VT
        </div>
        <!-- Default to the left -->
        <strong>Copyright &copy; 2016 <a href="#">Virginia Tech</a>.</strong> All rights reserved.
      </footer>

      <!-- Control Sidebar -->
      <aside class="control-sidebar control-sidebar-dark control-sidebar-close">
        <!-- Create the tabs -->
        <ul class="nav nav-tabs nav-justified control-sidebar-tabs">
          <li class="active"><a href="#control-sidebar-home-tab" data-toggle="tab"><i class="fa fa-home"></i></a></li>
          <li><a href="#control-sidebar-settings-tab" data-toggle="tab"><i class="fa fa-gears"></i></a></li>
        </ul>
        <!-- Tab panes -->
        <div class="tab-content">
          <!-- Home tab content -->
          <div class="tab-pane active" id="control-sidebar-home-tab">


            <ul class="control-sidebar-menu">
              <li>
                <a href="javascript::;">
                  <h4 class="control-sidebar-subheading">
                    Project Setup
                    <span id="StatusBarLabel" class="label label-danger pull-right">0%</span>
                  </h4>
                  <div class="progress progress-xxs" id='StatusBar'>
                    <div  class="progress-bar progress-bar-danger" style="width: 0%"></div>
                  </div>
                </a>
              </li>
            </ul><!-- /.control-sidebar-menu -->


            <h3 class="control-sidebar-heading">Terminology</h3>
            <ul class="control-sidebar-menu">
                <li>
                  <div>

                     <p>This section help you to get started on completing the data parameters associated to your samples.</p>

                    <ul>
                    <li><b>Project</b> - a set of samples comprising different conditions</li>
                    <li><b>Sample</b> - a single entity that has been obtained for analysis</li>
                    <li><b>Environment</b> - the characteristics which describe the environment in which your samples were obtained </li>
                    <li><b>Sample set</b> - a group of samples sharing the same library and environmental characteristics</li>
                    <li><b>Library preparation</b> - Environmental package the sample belongs to. (metagenome, meta transcriptome, amplicon metagenome 16s)</li>
                    <li><b>Reads 1-2</b> - The file names corresponding to the data from your library (fasq-fasta format). Be aware that this name has to be </strong>EXACTLY</strong> the same as the file you will upload.</li>
                  </ul>
                </div>
              </li>

            </ul>

















          </div><!-- /.tab-pane -->
          <!-- Stats tab content -->
          <div class="tab-pane" id="control-sidebar-stats-tab">Stats Tab Content</div><!-- /.tab-pane -->
          <!-- Settings tab content -->
          <div class="tab-pane" id="control-sidebar-settings-tab">
            <form method="post">
              <h3 class="control-sidebar-heading">General Settings</h3>
              <div class="form-group">
                <label class="control-sidebar-subheading">
                  Report panel usage
                  <input type="checkbox" class="pull-right" checked />
                </label>
                <p>
                  Some information about this general settings option
                </p>
              </div><!-- /.form-group -->
            </form>
          </div><!-- /.tab-pane -->
        </div>
      </aside><!-- /.control-sidebar -->
      <!-- Add the sidebar's background. This div must be placed
           immediately after the control sidebar -->
      <div class="control-sidebar-bg"></div>
    </div><!-- ./wrapper -->

























    <!-- REQUIRED JS SCRIPTS -->

    <!-- jQuery 2.1.4 -->
    <script type="text/javascript" src="{{ url_for('static', filename='template/plugins/jQuery/jQuery-2.1.4.min.js') }}"></script>
    <script src="//code.jquery.com/ui/1.11.4/jquery-ui.js"></script>
    <script src="//code.jquery.com/jquery-1.10.2.js"></script>

    <!-- Bootstrap 3.3.2 JS -->
    <script type="text/javascript" src="{{ url_for('static', filename='template/bootstrap/js/bootstrap.min.js') }}"></script>
    <!-- Bootstrap buttons -->
    <script type="text/javascript" src="{{ url_for('static', filename='template/bootstrap/js/bootstrap-filestyle.min.js') }}"></script>
    <!-- AdminLTE App -->
    <script type="text/javascript" src="{{ url_for('static', filename='template/dist/js/app.min.js') }}"></script>
    <!-- icheck -->
    <script type="text/javascript" src="{{ url_for('static', filename='icheck/icheck.js') }}"></script>
    <!--main js file-->
    <script type="text/javascript" src="{{ url_for('static', filename='js/common.js') }}"></script>
    <script type="text/javascript" src="{{ url_for('static', filename='js/Update_Project_Reads_2.js') }}"></script>




    <!-- Optionally, you can add Slimscroll and FastClick plugins.
          Both of these plugins are recommended to enhance the
          user experience. Slimscroll is required when using the
          fixed layout. -->
  </body>
</html>
