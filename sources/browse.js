"use strict";
$(document).ready(function(){
  $("#searchButton").click(function(){
    $("#results").html("Loading...");
    $.get("../parts/browseResults?sort=" + $("#sort").val() + "&results=" +
        $("#nResults").val() + "&direction=" + $("#sortDirection").val(), function(res){
      $("#results").html(res);
    });
  });
});
