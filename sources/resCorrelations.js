"use strict";
/*jslint browser: true*/ /*global  $, console, suboptMaps, networks*/

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
function genCorrelations(corr1, corr2, subcorr1, subcorr2){
  console.log(corr1, corr2, subcorr1, subcorr2);
  var res = [];
  for(var i=0;i<networks.length;i++){
    if(networks[i].calculations[corr1].data[subcorr1] &&
        networks[i].calculations[corr2].data[subcorr2]){ // both subcalcs exist
      res.push([
        networks[i].calculations[corr1].data[subcorr1],
        networks[i].calculations[corr2].data[subcorr2]
      ]);
    }
  }

  var scatterplot = $("#scatterplot").highcharts();
  scatterplot.series[0].remove(true);
  scatterplot.addSeries({data: res, name: corr1 + "-" +
      subcorr1 + " " + corr2 + "-" + subcorr2});
  scatterplot.xAxis.title = corr1 + "-" + subcorr1
  scatterplot.yAxis.title = corr2 + "-" + subcorr2
  scatterplot.redraw();
}

$(document).ready(function(){
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
      startOnTick: true,
      endOnTick: true,
      showLastLabel: true
    },
    yAxis: {
      title: {
        text: 'test'
      }
    },
    title: {
      text: "Network Attribute Correlation Plot"
    },
    plotOptions: {
      scatter: {
        marker: {
          radius: 5,
          states: {
            hover: {
              enabled: true,
              lineColor: 'rgb(100,100,100)'
            }
          }
        },
        states: {
          hover: {
            marker: {
              enabled: false
            }
          }
        }
      }
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
