# View controller for the screener page

import sys
from os import path
from flask import render_template

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from helpers import dbQuery, conf

# Generates the HTML for the double sliders to control the
# ranges of the histogram selections
def sliderGen(calcName, distributions):
  res = "<div id=\"valueMin-" + calcName + "\" class=\"sliderVal ta-center\">"
  res += "<input value=\"" + str(min(distributions[calcName]))
  res += "\"size=\"7\" class=\"valInput\" type=\"text\" id=\"valMin-" + calcName
  res += "\"></div><input type=\"range\" min=\"0\" max=\"100\" class="
  res += "\"fullwidth normalSlider\" id=\"sliderMin-" + calcName
  res += "\" value=\"0\">"
  res += "<div><div id=\"valueMax-" + calcName + "\" class=\"sliderVal ta-center\">\n"
  res += "<input value=\"" + str(max(distributions[calcName]))
  res += "\"size=\"7\" class=\"valInput\" type=\"text\" id=\"valMax-"
  res += calcName + "\"></div><input type=\"range\" min=\"0\""
  res += " max=\"100\" class=\"fullwidth normalSlider\" id=\"sliderMax-" + calcName
  res += "\" value=\"100\"></div>\n"
  return res

# Generates the HTML for the histograms that display the distributions
# of network attributes above the sliders
def dHistogram(calcName, clearName, distributions):
  res = "<script type='text/javascript'>\n$(document).ready(function(){\nvar data=["
  data = distributions[calcName]
  for p in data:
    res += str(p) + ","
  res += "];\n"
  res += (
    "$('#" + calcName + "Histogram').highcharts({\n"
      "title: {text: \"\"},\n"
      "chart: {type: \"histogram\", height: 185, spacingLeft: 0, spacingRight: 0},\n"
      "series: [{data: data, showInLegend: false}],\n"
      "legend: {enabled: false},\n"
      "yAxis: {labels: {enabled: false}, title: {text: \"\" }}\n"
    "});\n"
    "});\n"
    "</script>"
    "<div id='" + calcName + "Histogram'></div>"
  )
  return res

# Injects helper functions into template and returns its rendered form
def render():
  # unpacks the [{"res": val}, ...] distributions into just [val, val, ...]
  distributions = {k: map(lambda x: x["res"], v) for k, v in dbQuery.getDistributions()["values"].items()}
  return render_template("screener.html", conf=conf, dHistogram=dHistogram, distributions=distributions,
      sliderGen=sliderGen)
