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
  res += "\"></div><input type=\"range\" min=\"-1\" max=\"101\" class="
  res += "\"fullwidth normalSlider\" id=\"sliderMin-" + calcName
  res += "\" value=\"-1\">"
  res += "<div><div id=\"valueMax-" + calcName + "\" class=\"sliderVal ta-center\">\n"
  res += "<input value=\"" + str(max(distributions[calcName]))
  res += "\"size=\"7\" class=\"valInput\" type=\"text\" id=\"valMax-"
  res += calcName + "\"></div><input type=\"range\" min=\"-1\""
  res += " max=\"101\" class=\"fullwidth normalSlider\" id=\"sliderMax-" + calcName
  res += "\" value=\"101\"></div>\n"
  return res

# Generates the HTML for the True/False selection options
def boolGen(calcName, distributions):
  res  = "<label class=\"checkbox\">"
  res += "<input value=\"False\"type=\"checkbox\" class="
  res += "\"valCheckbox\" id=\"boolFalse-" + calcName + "\" checked>"
  res += "<span class=\"checkbox__label\">False</label>"
  res += "<label class=\"checkbox\">"
  res += "<input value=\"True\"type=\"checkbox\" class="
  res += "\"valCheckbox\" id=\"boolTrue-" + calcName + "\" checked>"
  res += "<span class=\"checkbox__label\">True</label>"
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
      "if(data && data.length > 0){"
        "$('#" + calcName + "Histogram').highcharts({\n"
          "title: {text: \"" + clearName + "\"},\n"
          "chart: {type: \"histogram\", height: 185, spacingLeft: 0, spacingRight: 0},\n"
          "plotOptions: {series: {color: \"#89457e\"}},\n"
          "series: [{data: data, showInLegend: false}],\n"
          "legend: {enabled: false},\n"
          "yAxis: {labels: {enabled: false}, title: {text: \"\" }}\n"
        "});\n"
      "}\n"
    "});\n"
    "</script>"
    "<div id='" + calcName + "Histogram'></div>"
  )
  return res

def dBoolgram(calcName, clearName, distributions):
  distributions[calcName] = map(lambda x: int(x), distributions[calcName]) # Convert True to 1 and False to 0
  return dHistogram(calcName, clearName, distributions)

# Injects helper functions into template and returns its rendered form
def render():
  # unpacks the [{"res": val}, ...] distributions into just [val, val, ...]
  distributions = {k: map(lambda x: x["res"], v) for k, v in dbQuery.getDistributions()["values"].items()}
  return render_template("screener.html", conf=conf, dHistogram=dHistogram, distributions=distributions,
      sliderGen=sliderGen, dBoolgram=dBoolgram, boolGen=boolGen)
