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
STAT_FILE_ERROR = -1
STAT_NO_VALUE = -2


def write_chart_values(values):
    return repr(values)[1:][:-1]


def get_column_chart(graph_name, x_title, y_title, test_stats, tuples):
    global CHART_COUNT
    CHART_COUNT = CHART_COUNT + 1
    for key, val in enumerate(test_stats):
        test_stats[key] = "'" + val + "'"
    for key,val in enumerate(tuples):
        val[0]=repr(val[0])
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
          height:500, \n\
        };\n\
        var div = document.createElement('div'); \n\
        div.id = 'chart_div_" + str(CHART_COUNT) + "';\n \
        div.style = 'width: 800px; height:600px;'\n \
        document.body.appendChild(div); \n\
        var chart = new google.visualization.ColumnChart(document.getElementById('chart_div_" + str(CHART_COUNT) + "'));\n\
        chart.draw(data, options);\n\
      }\n\
    "
    return s 

def get_line_chart(graph_name, x_title, y_title, test_stats, tuples):
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

def find_stat(lines, epoch):
    epoch = int(epoch)
    if epoch == 0:
        return lines[len(lines)-1]
    else:
        for line in reversed(lines):
            tmp = line.split(" ")
            if int(tmp[0].strip()) == epoch:
                return float(tmp[1].strip());
    return None


def filter_invalid_rows(result):
    rows = result["rows"]
    invalid_row_indexes = []

    for row_idx, row in enumerate(rows):
        valid = False
        for idx, val in enumerate(row):
            # not interested in the x-axis, skip
            if idx == 0: continue
            if val != STAT_FILE_ERROR and val != STAT_NO_VALUE:
                valid = True
                break
        if valid == False:
            invalid_row_indexes.append(row_idx)

    for idx in reversed(invalid_row_indexes):
        del rows[idx]

    return result

def filter_invalid_columns(result):
    rows = result["rows"]
    row_count = len(rows)
    invalid_column_indexes = []
    if row_count > 0:
        first_row = rows[0]
        row_len = len(first_row)
        
        for i in range(0, row_len):
            valid = False
            for j in range(0, row_count):
                if rows[j][i] != STAT_FILE_ERROR and rows[j][i] != STAT_NO_VALUE:
                    valid = True
                    break
            if not valid:
                invalid_column_indexes.append(i)
    for idx in reversed(invalid_column_indexes):
        for row in rows:
            del row[idx]
        del result["headers"][idx]

    return result

def get_data(config, graph_config, epoch):
    files = []

    for (dirpath, dirnames, filenames) in os.walk(mypath):
        files.extend(filenames)
        break

    # filter out files that are not related to test results
    files = [a for a in files if len(a.split("-")) == 3]
    files = sorted(files, key=lambda x: (int(x.split("-")[2]), x.split("-")[0], x.split("-")[1] ))
    test_config = graph_config["tests"]
    stat_config = graph_config["stats"]

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
                        stat_value = find_stat(lines, epoch);
                        if not stat_value is None:
                            row.append(stat_value)
                        else:
                            row.append(STAT_NO_VALUE)
                except IOError:
                        # TODO(oschaaf): improve/no magic numbers
                        row.append(STAT_FILE_ERROR)


    # TODO(oschaaf): make sure these are sorted
    for test in test_config:
        for stat in stat_config:
            headers.append(test + " - " + stat)

    result = {}
    result["headers"] = headers
    result["rows"] = rows
    result = filter_invalid_columns(result)
    result = filter_invalid_rows(result)
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
    data = get_data(config, graph_config, epoch)

    # TODO(oschaaf): 'inherit' y_axis_caption from the global config.
    # Perhaps that should be done for other properties too.
    y_axis_caption = config["y_axis_caption"]
    if  "y_axis_caption" in graph:
        y_axis_caption = graph['y_axis_caption']

    graph_type = "line"
    if "type" in graph:
        graph_type = graph["type"]
    if graph_type == "line":
        html = get_line_chart( graph["name"], config["x_axis_caption"], y_axis_caption, data["headers"], data["rows"]  )
    elif graph_type == "column":
        html = get_column_chart( graph["name"], config["x_axis_caption"], y_axis_caption, data["headers"], data["rows"]  )
    else:
        raise Error("Invalid chart type: [%s]" % graph_type)
    scripts.append(html)


print template.replace("@CHART_SCRIPT@", string.join(scripts, "\n"))
