<html>
  <head>
    <script type="text/javascript" src="http://code.jquery.com/jquery-1.6.2.min.js"></script>
    <script type="text/javascript" src="static/greenbar.js"></script>
    <link rel="stylesheet" href="static/greenbar.css" type="text/css" />
  </head>
  <title>Greenbar</title>
  <body>
    <script>
      Greenbar.go();
    </script>

    <input type="button" onclick="Greenbar.runTests()" value="Go!" class="go" />
    <div id="nowtime" class="time">{{nowtime}}</div>
    <div id="results"></div>
  </body>
</html>








