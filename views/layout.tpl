<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>piJukebox</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="">
    <meta name="author" content="">

    <!-- Le styles -->
    <link href="/public/css/bootstrap.css" rel="stylesheet">
    <style>
      body {
        padding-top: 60px; /* 60px to make the container go all the way to the bottom of the topbar */
        background-image: url('/public/img/navy_blue.png');
        background-repeat: repeat;
      }
    </style>
    <link href="/public/css/bootstrap-responsive.css" rel="stylesheet">

    <!-- HTML5 shim, for IE6-8 support of HTML5 elements -->
    <!--[if lt IE 9]>
      <script src="http://html5shim.googlecode.com/svn/trunk/html5.js"></script>
    <![endif]-->
  </head>

  <body>

    <div class="navbar navbar-inverse navbar-fixed-top">
      <div class="navbar-inner">
        <div class="container">
          <a class="btn btn-navbar" data-toggle="collapse" data-target=".nav-collapse">
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </a>
          <a class="brand" href="/">piJukebox</a>
          <div class="nav-collapse collapse">
            <ul class="nav">
              <li class="active"><a href="/">Player</a></li>
              <li><a href="#">Stations</a></li>
              <li><a href="#">Favorites</a></li>
              <li><a href="/about">About</a></li>
            </ul>
          </div><!--/.nav-collapse -->
        </div>
      </div>
    </div>

    <div class="container">

      %include

    </div> <!-- /container -->

    <!-- Le javascript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="/public/js/jquery-1.8.3.js"></script>
    <script src="/public/js/bootstrap.js"></script>
    <script src="/public/js/app.js"></script>

  </body>
</html>
