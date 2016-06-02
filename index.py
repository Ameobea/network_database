# Entry point for database web interface
#
# Written by Casey Primozic
from flask import Flask, render_template, send_from_directory
from helpers import conf, dbQuery
print(conf)
app = Flask(__name__)

# All routes need to be given the `conf` object in their context
@app.route("/")
def main():
  return render_template("index.html", conf=conf)

@app.route("/screener")
def screener():
  return render_template("screener.html", conf=conf)

@app.route("/compare")
def compare():
  return render_template("compare.html", conf=conf)

@app.route("/info/<networkHash>")
def networkInfo(networkHash):
  network = dbQuery.getNetwork(networkHash)
  if type(network) == bool:
    return render_template("noNetwork.html", conf=conf)
  else:
    return render_template("info.html", network=network, conf=conf)

@app.route("/browse")
def browseNetworks():
  networkList = dbQuery.getNetworkList(50)
  return render_template("browse.html", conf=conf, networkList=networkList)

@app.route("/sources/<path:path>")
def serverData(path):
  return send_from_directory("sources", path)

if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
