$(document).ready(function(){
  // Sets the input box to the current value of the slider
  $(".normalSlider").on("change", function(){
    var calcName = this.id.split("-")[1];
    var type = this.id.replace("slider", "").split("-")[0];
    $("#val" + type + "-" + calcName).val(this.value);
  });
});
