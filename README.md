# Network Database Web Interface
This is the database and web UI for the network research project.  Its purpose is to hold networks and network calculations created from the processing pipeline and to present it a simple and accessible format.

## Overview
The web interface has the function of connecting with the database and providing a way for users to both insert their own networks into the database as well as search through networks submitted by others.  Submitted networks are sent through the processing pipeline first.  After that, they are inserted into the database and the calculated stats are used to attempt to classify it.

For users, each network will have a data page listing all of the calculated metrics and including graphs and other visualizations that both show the static statistics as well as how it fits in the models created from the other networks.

## Technical Specifications
The database itself is built on top of MongoDB, a document-based database very popular for its simplicity and utility.  The web server is Flask-based and will interface directly with the database backend.  For now, Highcharts will be used for the frontend visualizations.  Cutestrap is used as a CSS framework.

## Installation
1. `(sudo) pip install flask`
1. `(sudo) pip install pymongo`

You'll also have to install mongodb: `sudo apt-get install mongodb`

Then you'll have to populate mongodb with some data for the site to display.  Data can be imported from the [network_research](https://github.com/ameobea/network_research) repository's `results.json` file directly into mongo with the `utils/insertAndUpdate.sh` script; you'll have to edit that file and change the path of the `results.json` file to wherever it is located on your machine.

Finally, you'll have to copy the `helpers/conf.default.py` file to `helpers/conf.py` and edit the settings in there as needed for your installation.

### Common Issues
If you're getting errors when visiting pages, make sure that you actually have network data in mongo and that mongo is running.  This site assumes that there is data there when it tries to display it.

In addition, if the screener page is broken and the charts aren't appearing, make sure that the `highcharts-historgram` submodule was cloned correctly.  Git is very bad about cloning submodules reliably; you may have to run `git pull --recurse-submodules --force` or, if that fails, manually clone the repository yourself from [here](https://github.com/ameobea/highcharts-histogram).
