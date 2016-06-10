$(document).ready(function(){
  // Sets the input box to the current value of the slider on slider change
  $(".normalSlider").on("change", function(){
    var calcName = this.id.split("-")[1];
    var type = this.id.replace("slider", "").split("-")[0];
    var diff = distrVals[calcName]["max"] - distrVals[calcName]["min"];
    $("#val" + type + "-" + calcName).val((this.value / 100) * diff + distrVals[calcName]["min"]);
    zoneBars(parseFloat($("#valMin-" + calcName).val()), parseFloat($("#valMax-" + calcName).val()), calcName)
  });

  // Sets the slider to the current value of the input box on input box change
  $(".valInput").change(function(){
    var calcName = this.id.split("-")[1];
    var type = this.id.replace("val", "").split("-")[0];
    var diff = distrVals[calcName]["max"] - distrVals[calcName]["min"];
    var sliderVal = ((this.value - distrVals[calcName]["min"]) / diff) * 100;
    $("#slider" + type + "-" + calcName).val(Math.round(sliderVal));
    zoneBars(parseFloat($("#valMin-" + calcName).val()), parseFloat($("#valMax-" + calcName).val()), calcName)
  });
});

// Changes the colors of regions of a given chart to grey
function zoneBars(dataStart, dataEnd, calcName){
  var chart = $("#" + calcName + "Histogram").highcharts();
  chart.series[0].zoneAxis = "x";
  chart.series[0].zones = [
    {value: dataStart, color: "#c9c9c9"},
    {value: dataEnd, color: "#89457e"},
    {value: chart.series[0].xData, color: "#c9c9c9"}
  ];
  chart.redraw();
}
