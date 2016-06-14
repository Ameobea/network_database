"use strict";
/*jslint browser: true*/ /*global  $, console*/

function displayRes(shortlink, pernode, inserNone){
  var siteRoot = $("#siteRoot").val();
  var tackon = "";
  var tackSym = "?";
  if(inserNone){
    tackon += "?inserNone=true";
    tackSym = "&";
  }
  if(pernode){
    tackon += tackSym + "pernode=true";
    tackSym = "&";
  }
  var res =  "<b>CSV</b>:  <a href=\"" + siteRoot + "api/s/csv/" + shortlink + tackon + "\">" + siteRoot + "api/s/csv/" + shortlink + tackon + "</a><br>";
  res += "<b>JSON</b>: <a href=\"" + siteRoot + "api/s/json/" + shortlink + tackon + "\">" + siteRoot + "api/s/csv/" + shortlink + tackon + "</a>";
  $("#res").html(res);
}

$(document).ready(function(){
  $("#submitButton").click(function(){
    //var method = $("input[name='method']:checked").val();
    var decoded = atob($("#b64").val());
    var pernode = $("#pernode")[0].checked;
    var inserNone = $("#noneMissing")[0].checked;

    $("#res").html("Loading...");
    $.post("./api/shortlinkgen", {instr: decoded}, function(shortlink){
      displayRes(shortlink, pernode, inserNone);
    });
  });
});
