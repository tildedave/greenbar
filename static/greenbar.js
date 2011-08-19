var Greenbar = {

  go : function () {
    this.resultDisplayer = new Greenbar.ResultDisplayer();
    Greenbar.runTests();
  },

  runTests : function () {
    var resultDisplayer = this.resultDisplayer;
    jQuery.get('/results', function (data) {
      resultDisplayer.render(data);
    });
  }
  
};

Greenbar.ResultDisplayer = function () {
};

Greenbar.ResultDisplayer.prototype.render = function (data) {
  var results = 
  jQuery("#results").html("<pre>" + data.output + "</pre>");
  jQuery("#nowtime").html(data.nowtime);
  
};