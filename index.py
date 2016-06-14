# Entry point for database web interface
#
# Written by Casey Primozic

from flask import Flask, render_template, send_from_directory, request
from helpers import conf, dbQuery, jinjaSetup
from views import compare, screener, screenResults, resCorrelations
from views.api import attrs

app = Flask(__name__)

jinjaSetup.register(app.jinja_env)

# All routes need to be given the `conf` object in their context
@app.route("/")
def main():
  return render_template("index.html", conf=conf)

@app.route("/screener")
def renderScreener():
  return screener.render()

@app.route("/compare/<networks>")
def renderCompare(networks):
  return compare.compare(networks, app.jinja_env)

@app.route("/compare")
def renderCookieCompare():
  return compare.compare(False, app.jinja_env, cookies=request.cookies)

@app.route("/info/<networkHash>")
def networkInfo(networkHash):
  network = dbQuery.getNetwork(networkHash)
  if type(network) == bool:
    return render_template("noNetwork.html", conf=conf)
  else:
    return render_template("info.html", network=network, conf=conf, dbQuery=dbQuery,
        networkHash=networkHash)

@app.route("/browse")
def browseNetworks():
  return render_template("browse.html", conf=conf, dbQuery=dbQuery)

@app.route("/parts/<page>")
def parts(page):
  if page == "browseResults":
    return render_template("mixins/browseResults.html", conf=conf, dbQuery=dbQuery)
  elif page == "screenResults":
    return screenResults.render(request.args)

@app.route("/admin")
def admin():
  return render_template("admin.html", conf=conf, dbQuery=dbQuery)

@app.route("/sources/<path:path>")
def serveData(path):
  return send_from_directory("sources", path)

@app.route("/sources/highcharts-historgram/<path:path>")
def highchartsHistogram(path):
  return send_from_directory("sources/highcharts-historgram", path)

@app.route("/export", methods=["GET", "POST"])
def serveExportUI():
  if request.method == "POST":
    return render_template("export.html", conf=conf, b64=request.form["b64"])
  else:
    return render_template("exportGetError.html", conf=conf)

# Export API endpoints
@app.route("/api/s/<method>/<shortname>")
def serverShortname(method, shortname):
  return attrs.shortlinkServe(method, shortname, request)

@app.route("/api/shortlinkgen", methods=["POST"])
def shortlinkGen():
  return attrs.shortlinkGen(request.form)

@app.route("/correlate", methods=["GET", "POST:"])
def correlations():
  if request.method == "POST":
    return resCorrelations.render(b64=request.form["b64"])
  else:
    return render_template("error.html", conf=conf)

@app.route("/correlate/data", methods=['POST'])
def pairData():
  if request.method == 'POST':
    return resCorrelations.data(request.form["b64"], request.form["calc1"],
        request.form["subcalc1"], request.form["calc2"], request.form["subcalc2"])

@app.route("/humans.txt")
def serverHumanstxt():
  return render_template("humans.txt"), 200, {'Content-Type': 'text/plain; charset=utf-8'}

if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
