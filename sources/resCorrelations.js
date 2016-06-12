"use strict";
/*jslint browser: true*/ /*global  $*/
$(document).ready(function(){
  $("#scatterplot").highcharts({
    chart: {
      type: 'scatter',
      zoomType: 'xy'
    },
    title: {
      text: "Network Attribute Correlation Plot"
    }
  });
});
