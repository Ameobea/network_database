"use strict";
/*jslint browser: true*/ /*global  $, console*/

function displayRes(shortlink){
  var siteRoot = $("#siteRoot").val();
  var res =  "<b>CSV</b>:  <a href=\"" + siteRoot + "api/s/csv/" + shortlink + "\">" + siteRoot + "api/s/csv/" + shortlink + "</a><br>";
  res += "<b>JSON</b>: <a href=\"" + siteRoot + "api/s/json/" + shortlink + "\">" + siteRoot + "api/s/csv/" + shortlink + "</a>";
  $("#res").html(res);
}

$(document).ready(function(){
  $("#submitButton").click(function(){
    //var method = $("input[name='method']:checked").val();
    var decoded = atob($("#b64").val());
    $("#res").html("Loading...");
    $.post("./api/shortlinkgen", {instr: decoded}, function(shortlink){
      displayRes(shortlink);
    });
  });
});
