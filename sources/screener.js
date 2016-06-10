$(document).ready(function(){
  // Sets the input box to the current value of the slider on slider change
  $(".normalSlider").on("change", function(){
    var calcName = this.id.split("-")[1];
    var type = this.id.replace("slider", "").split("-")[0];
    var diff = distrVals[calcName]["max"] - distrVals[calcName]["min"];
    $("#val" + type + "-" + calcName).val((this.value / 100) * diff + distrVals[calcName]["min"]);
  });

  // Sets the slider to the current value of the input box on input box change
  $(".valInput").change(function(){
    var calcName = this.id.split("-")[1];
    var type = this.id.replace("val", "").split("-")[0];
    var diff = distrVals[calcName]["max"] - distrVals[calcName]["min"];
    var sliderVal = ((this.value - distrVals[calcName]["min"]) / diff) * 100;
    $("#slider" + type + "-" + calcName).val(Math.round(sliderVal));
  });
});
