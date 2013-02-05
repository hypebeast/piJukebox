<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>piJukebox</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="">
    <meta name="author" content="">

    <!-- Le styles -->
    <link href="/public/vendor/bootstrap/css/bootstrap.css" rel="stylesheet">
    <link href="/public/vendor/bootstrap/css/bootstrap-responsive.css" rel="stylesheet">
    <link href="/public/vendor/jquery-ui/css/ui-lightness/jquery-ui-1.9.2.custom.min.css" rel="stylesheet">
    <link href="/public/css/style.css" rel="stylesheet">

    <!-- HTML5 shim, for IE6-8 support of HTML5 elements -->
    <!--[if lt IE 9]>
      <script src="http://html5shim.googlecode.com/svn/trunk/html5.js"></script>
    <![endif]-->
  </head>

  <body>

    <div class="navbar navbar-inverse navbar-fixed-top">
      <div class="navbar-inner">
        <div class="container-fluid">
          <a class="btn btn-navbar" data-toggle="collapse" data-target=".nav-collapse">
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </a>
          <a class="brand" href="/">piJukebox</a>
          <div class="nav-collapse collapse">
            <ul class="nav">
              <li class="dropdown">
                <a href="#StartPage" class="dropdown-toggle" data-toggle="dropdown">
                  Music
                  <b class="caret"></b>
                </a>
                <ul class="dropdown-menu" data-bind="foreach: sections">
                  <li><a href="" data-bind="text: $data.name, click: $root.goToSection"></a></li>
                </ul>
              </li>
              <li>
                <a href="#settings">Settings</a>
              </li>
            </ul>
          </div><!--/.nav-collapse -->
        </div>
      </div>
    </div>

    <div class="container-fluid">
      <div class="row-fluid">
        <div class="span2">
          <div class="well sidebar-nav">
            <ul class="nav nav-list">
              <li class="nav-header" data-bind="text: chosenSection().name"></li>
              <div data-bind="foreach: activeSubSections">
                <li>
                  <a href="" data-bind="text: $data.name, click: $root.goToSubsection"></a>
                </li>
              </div>
            </ul>
          </div>
        </div>
        <div class="span10">

          <!-- Render the chosen template -->
          <div data-bind="template: { name: selectedTemplate() }">
          </div>

        </div>
      </div>
    </div> <!-- /container-fluid -->

    <div class="navbar navbar-fixed-bottom" id="player">
      <hr class="player">
      <div class="row-fluid" style="padding: 10px; height: 40px; background-image: url('/public/img/nasty_fabric.png');">
        <div class="span2" id="player-left">
          <button id="playPause" class="btn btn-inverse" style="margin-left: 10px;"><i class="icon-white icon-play"></i></button>
        </div>
        <div class="span8" id="nowPlayingInfo">
          <div id="title_label" class="player-title">
          </div>
          <div id="song_label" class="player-song">
          </div>
        </div>
        <div class="span2" id="volume-control-container">
          <span class="tooltip"></span>
          <div id="volume-slider"></div>
          <span class="volume"></span>
        </div>
      </div>
    </div>

    <!-- Le javascript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="/public/vendor/jquery/jquery-1.8.3.js"></script>
    <script src="/public/vendor/jquery-ui/js/jquery-ui-1.9.2.custom.min.js"></script>
    <script src="/public/vendor/knockout/knockout-2.2.0.js"></script>
    <script src="/public/js/sammy.js"></script>
    <script src="/public/js/koExternalTemplateEngine_all.js"></script>
    <script src="/public/vendor/bootstrap/js/bootstrap.js"></script>
    <script src="/public/js/app.js"></script>

  </body>
</html>
