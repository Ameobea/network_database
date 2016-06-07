# Entry point for database web interface
#
# Written by Casey Primozic
from flask import Flask, render_template, send_from_directory
from helpers import conf, dbQuery, networkUtils, jinjaSetup
from views import compare

app = Flask(__name__)

jinjaSetup.register(app.jinja_env)

# All routes need to be given the `conf` object in their context
@app.route("/")
def main():
  return render_template("index.html", conf=conf)

@app.route("/screener")
def screener():
  return render_template("screener.html", conf=conf)

@app.route("/compare/<networks>")
def renderCompare(networks):
  return compare.compare(networks, app.jinja_env)

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
  return render_template("browse.html", conf=conf,
      networkUtils=networkUtils, dbQuery=dbQuery)

@app.route("/parts/<page>")
def parts(page):
  if page == "browseResults":
    return render_template("mixins/browseResults.html", conf=conf, dbQuery=dbQuery,
        networkUtils=networkUtils)

@app.route("/admin")
def admin():
  return render_template("admin.html", conf=conf, dbQuery=dbQuery)

@app.route("/sources/<path:path>")
def serveData(path):
  return send_from_directory("sources", path)

@app.route("/sources/highcharts-historgram/<path:path>")
def highchartsHistogram(path):
  return send_from_directory("sources/highcharts-historgram", path)

if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
