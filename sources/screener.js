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

  // Sets up the submit button listener
  $("#submitButton").click(function(){
    showResults(0, 0, 0, 0, descrimGen());
  });
});

// Makes the request for the results sub-view and inserts it in the results div
function showResults(sort, count, direction, start, descrim){
  $("#results").html("Loading...");
  $.get("../parts/screenResults?sort=" + sort + "&results=" +
      count + "&direction=" + direction +
      "&start=" + start + "&descrim=" + btoa(JSON.stringify(descrim)), //encode descrim object in base64
      function(res){
    $("#results").html(res);
  });
}

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

// Takes the selection values from the histograms and converts them into
// a list to be made into a query for MongoDB
function descrimGen(){
  res = {};
  // get sliders
  $(".slider input").each(function(){
    var split = this.id.split("-");
    if(this.type == "text"){ // ignore the range selectors
      if(split[0] == "valMin"){
        if(!res[split[1]]){
          res[split[1]] = {};
        }
        res[split[1]]["min"] = parseFloat(this.value);
      }else{
        if(!res[split[1]]){
          res[split[1]] = {};
        }
        res[split[1]]["max"] = parseFloat(this.value);
      }
    }
  });

  // get true/false checkboxes
  $(".boolSelect input").each(function(){
    var split = this.id.split("-");
    if(!res[split[1]]){
      res[split[1]] = {};
    }
    if(this.value == "True"){
      res[split[1]]["True"] = this.checked;
    }else{
      res[split[1]]["False"] = this.checked;
    }
  });
  return res;
}
