var Greenbar = {

  go : function () {
    this.resultDisplayer = new Greenbar.ResultDisplayer();

    jQuery("#display-output").click(function () {
      var output = jQuery("#output");
      if (output.is(":hidden")) {
        output.show();
        jQuery(this).text("Hide Output");
      }
      else {
        output.hide();
        jQuery(this).text("Show Output");
      }
    });
    
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

Greenbar.ResultDisplayer.prototype.renderTestCases = function (data) {

  var testCases = jQuery("#testcase-container");
  testCases.empty();

  var testList = $("<ul></ul>");
  for(var i = 0, l = data.tests.length; i < l; ++i) {
    var testResult = data.tests[i];
    var tmpl = $("#testcase").tmpl( data.tests[i] );

    tmpl.appendTo(testList);
  }

  testList.appendTo(testCases);  
};

Greenbar.ResultDisplayer.prototype.renderTestHeader = function (data) {
  var tmpl = $("#testheader").tmpl( data );
  var testHeader = jQuery("#testheader-container");
  testHeader.empty();

  tmpl.appendTo(testHeader);
};

Greenbar.ResultDisplayer.prototype.render = function (data) {
  var outputContainer = jQuery("#output");
  outputContainer.html("<pre>" + data.output + "</pre>");
  outputContainer.hide();
  
  jQuery("#nowtime").html(data.nowtime);

  this.renderTestCases(data);
  this.renderTestHeader(data);
};

