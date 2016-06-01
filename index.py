# Entry point for database web interface
#
# Written by Casey Primozic
from flask import Flask, render_template, send_from_directory
from helpers import conf
print(conf)
app = Flask(__name__)

@app.route('/')
def main():
  return render_template("index.html", conf=conf)

@app.route("/sources/<path:path>")
def serverData(path):
  return send_from_directory("sources", path)

if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
