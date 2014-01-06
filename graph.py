#!/usr/bin/env python

import copy
import datetime
import imp
import os
import pprint
import re
import string
import subprocess
import time
import sys

CHART_COUNT = 0

def write_chart_values(values):
    return repr(values)[1:][:-1]


def get_chart(graph_name, x_title, y_title, test_stats, tuples):
    global CHART_COUNT
    CHART_COUNT = CHART_COUNT + 1
    for key, val in enumerate(test_stats):
        test_stats[key] = "'" + val + "'"

    s = "\n \
      google.setOnLoadCallback(drawChart_" + str(CHART_COUNT) + ");\n\
      function drawChart_" + str(CHART_COUNT) + "() {\n\
      var data = google.visualization.arrayToDataTable([\n\
          [" + string.join(test_stats, ",\n") + "],\n\
" + write_chart_values(tuples) + " \
        ]);\n\
        var options = {\n\
          title: '" + graph_name + "', \n\
          vAxis: {title: " + repr(y_title)  + "}, \n\
          hAxis: {title: " + repr(x_title) + "}, \n\
          pointSize: 5, \n\
          //curveType: 'function', \n\
          width:600, \n\
          height:500, \n\
        };\n\
        var div = document.createElement('div'); \n\
        div.id = 'chart_div_" + str(CHART_COUNT) + "'\n \
        div.style = 'width: 800px; height:600px;'\n \
        document.body.appendChild(div); \n\
        var chart = new google.visualization.LineChart(document.getElementById('chart_div_" + str(CHART_COUNT) + "'));\n\
        chart.draw(data, options);\n\
      }\n\
    "
    return s 

def find_graph_config(graph_name, config):
    graph_config = None

    for c in config["graphs"]:
        if c["name"].lower() == graph_name.lower():
            graph_config = c
            break
    
    return graph_config
    

def get_data(config, graph_config):
    files = []

    for (dirpath, dirnames, filenames) in os.walk(mypath):
        files.extend(filenames)
        break

    # filter out files that are not related to test results
    files = [a for a in files if len(a.split("-")) == 3]
    files = sorted(files, key=lambda x: (int(x.split("-")[2]), x.split("-")[0], x.split("-")[1] ))
    test_config = graph_config["tests"]
    stat_config = graph_config["stats"]

    result = {}
    headers = ["X"]
    rows = []
    x_values = []
    
    for f in files:
        tmp = f.split("-")
        file_test = tmp[0]
        file_stat = tmp[1]
        file_x = int(tmp[2])
        if len(x_values) == 0 or x_values[len(x_values)-1] < file_x:
            x_values.append(file_x)
    
    for x in x_values:
        row = []
        rows.append(row)
        row.append(x)
        for test in test_config:
            for stat in stat_config:
                try:
                    with open(mypath + test + "-" + stat + "-" + str(x)) as file:
                        lines = file.readlines()
                        row.append(float(lines[len(lines)-1].split(" ")[1].strip()))
                except:
                        row.append(-1)
                    
        if len(row) == 0:
            print "aarg"
                
    # TODO(oschaaf): make sure these are sorted
    for test in test_config:
        for stat in stat_config:
            headers.append(test + " - " + stat)

    result["headers"] = headers
    result["rows"] = rows
    return result


template = "<html>\n\
   <head>\n\
    <script type='text/javascript' src='https://www.google.com/jsapi'></script>\n\
    <script type='text/javascript'>\n\
      google.load('visualization', '1', {packages:['corechart']});\n\
@CHART_SCRIPT@ \n\
    </script> \n\
  </head>\n\
  <body>\n\
     <h1>Loadtest results</h1> \n\
  </body>\n\
</html>\n\
"

# TODO: remove code duplication with loadtest.py
# TODO: handle invalid files.
scripts = []
config_path = "config.py"

if len(sys.argv) == 2:
    config_path = sys.argv[1]

config_mod = imp.load_source("config", config_path)

config = config_mod.get_config()
# TODO(oschaaf): ensure ends with '/'
mypath = config["result_dir"]
epoch = "0"

try:
    with open(mypath + "last", 'r') as f:
        epoch = f.read()        
except IOError:
    print "No recent loadtests"

for key in config.keys():
    for test in config["tests"]:
        if not key in test.keys():
            test[key] = config[key]

for graph in config["graphs"]:
    graph_config = find_graph_config(graph["name"], config)
    data = get_data(config, graph_config)
    html = get_chart( graph["name"], config["x_axis_caption"], config["y_axis_caption"], data["headers"], data["rows"]  )
    scripts.append(html)


print template.replace("@CHART_SCRIPT@", string.join(scripts, "\n"))
