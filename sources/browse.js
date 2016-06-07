"use strict";
/*jslint browser: true*/ /*global  $*/
function showResults(sort, count, direction, start){
  $("#results").html("Loading...");
  $.get("../parts/browseResults?sort=" + sort + "&results=" +
      count + "&direction=" + direction +
      "&start=" + start, function(res){
    $("#results").html(res);
  });
}

$(document).ready(function(){
  $("#searchButton").click(function(){
    showResults($("#sort").val(), $("#nResults").val(), $("#sortDirection").val(), "0");
  });
});
