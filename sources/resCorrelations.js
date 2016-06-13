"use strict";
/*jslint browser: true*/ /*global  $, console, suboptMaps, networkListb64*/

// Used to keep track of the names of networks in the scatter plor
var corrNetworks = [];

// Generates the HTML for the option tags that go inside the suboption <select> tag
function suboptGen(suboptName, suboptMap, num){
  var res = "<select id=\"suboptSel" + num + "\">\n";
  for(var i=0;i<suboptMap.length;i++){
    if(!(suboptMap.length > 1 && suboptMap[i] == "res")){ // Ignore res if we have processed calculations instead
      res += "<option value=\"" + suboptMap[i] + "\">" + suboptMap[i] + "</option>\n";
    }
  }
  res += "</select>";
  return res;
}

// Generates a list of correlation data to be plotted for each network
// that contains valid data, inserts into chart series, and redraws chart
function genCorrelations(calc1, calc2, subcalc1, subcalc2){
  $.post("./correlate/data", {b64: networkListb64 , calc1: calc1, subcalc1: subcalc1,
      calc2: calc2, subcalc2: subcalc2}, function(res){
    res = JSON.parse(res);
    corrNetworks = res.hashList;
    var scatterplot = $("#scatterplot").highcharts();
    scatterplot.series[0].remove(true);
    scatterplot.addSeries({data: res.data, name: calc1 + "-" +
        subcalc1 + " " + calc2 + "-" + subcalc2});
    scatterplot.xAxis.title = calc1 + "-" + subcalc1;
    scatterplot.yAxis.title = calc2 + "-" + subcalc2;
    scatterplot.redraw();
  });
}

$(document).ready(function(){
  // Make the graph's div a square
  var scatterplot = $("#scatterplot");
  $("#scatterplot").html(scatterplot.height(scatterplot.width())[0]);

  // Create blank scatter plot
  $("#scatterplot").highcharts({
    chart: {
      type: 'scatter',
      zoomType: 'xy'
    },
    xAxis: {
      title: {
        enabled: true,
        text: 'test'
      },
      gridLineDashStyle: "solid",
      gridLineWidth: 1,
      startOnTick: true,
      endOnTick: true,
      showLastLabel: true
    },
    yAxis: {
      title: {
        text: 'test'
      }
    },
    plotOptions: {
      scatter: {
        animation: false,
        marker: {
          radius: 10
        }
      }
    },
    tooltip: {
      formatter: function(){
        var index = this.series.data.indexOf(this.point);
        var xName = $("#attrSelector1").val() + "-" + $("#suboptSel1").val();
        var yName = $("#attrSelector2").val() + "-" + $("#suboptSel2").val();

        var res = "<b><a target=\"_blank\" href=\"info/";
        res += corrNetworks[index].hash;
        res += "\">" + corrNetworks[index].name + "</a></b><br>";
        res += "<b>" + xName + "</b>:<br> " + this.x + "<br>";
        res += "<b>" + yName + "</b>:<br> " + this.y;

        return res;
      },
      useHTML: true
    },
    title: {
      text: "Network Attribute Correlation Plot"
    },
    series: [{
      name: "Correlations",
      data: [[null, null]]
    }]
  });

  // Set up attribute selector change listeners
  $(".attrSelector").change(function(){
    if(suboptMaps[this.value] != [] && suboptMaps[this.value] != ["res"]){
      var num = this.id.split("tor")[1];
      $("#subOption" + num).html(suboptGen(this.value, suboptMaps[this.value], num));
    }
  });

  // Draw button click listener
  $("#drawButton").click(function(){
    genCorrelations($("#attrSelector1").val(), $("#attrSelector2").val(),
        $("#suboptSel1").val(), $("#suboptSel2").val());
  });
});
