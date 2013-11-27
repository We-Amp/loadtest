#!/usr/bin/env python

import copy
import datetime
import os
import re
import string
import subprocess
import time
import sys

from config import loadtest_config

config = loadtest_config()

# TODO: check, validate args, etc
epoch = sys.argv[1]

mypath = "result/"
files = [ f for f in os.listdir(mypath) ]
results = []

CHART_COUNT = 0

def get_chart(test_name, test_stat, tuples):
    global CHART_COUNT
    CHART_COUNT = CHART_COUNT + 1
    s = ""
    s = "\n \
      google.setOnLoadCallback(drawChart_" + str(CHART_COUNT) + ");\n\
      function drawChart_" + str(CHART_COUNT) + "() {\n\
      var data = google.visualization.arrayToDataTable([\n\
          ['Concurrency', '" + test_stat + "'],\n\
" + string.join(tuples, ",\n") + " \
        ]);\n\
        var options = {\n\
          title: 'Test [" + test_name  + "]', \n\
          vAxis: {title: '" + test_stat  + "'}, \n\
          hAxis: {title: 'Concurrency'}, \n\
          pointSize: 5, \n\
          curveType: 'function' \n\
        };\n\
        var div = document.createElement('div'); \n\
        div.id = 'chart_div_" + str(CHART_COUNT) + "'\n \
        document.body.appendChild(div); \n\
        var chart = new google.visualization.LineChart(document.getElementById('chart_div_" + str(CHART_COUNT) + "'));\n\
        chart.draw(data, options);\n\
      }\n\
"
    return s 

def write_stat(test_name, test_stat, results):
    tuples = []
    data = [a for a in results if a.startswith(test_name + "-" + test_stat + "-")]

    for key in data:
        tuples.append("[%s,  %s]" % (key.split("-")[2], key.split("-")[3]))

    return get_chart(test_name, test_stat, tuples)


for file in files:
    tmp = string.split(file, "-")
    # Unpack filename into its components
    name = tmp[0]
    concurrency = tmp[1]
    stat_name = tmp[2]

    # Find requested stat
    with open("result/%s" % file) as f:
        content = f.readlines()
        # TODO(oschaaf): efficiency
        content = [a for a in content if a.startswith(epoch)]
        
    # TODO(oschaaf): (handle bad array size (<>1)
    results.append(name + "-" + stat_name + "-" + concurrency + "-" + string.split(content[0]," ")[1].strip() )


# TODO(oschaaf): sorting the files instead of the contents would be a lot more efficient
results = sorted(results, key=lambda x: (x.split("-")[0], x.split("-")[1], int(x.split("-")[2])))

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

scripts = []
cur_test = ""
cur_stat = ""
for r in results:
    add_script = False
    if cur_test != r.split("-")[0]:
        add_script = True
        cur_test = r.split("-")[0]
    if cur_stat != r.split("-")[1]:
        add_script = True
        cur_stat = r.split("-")[1]

    if add_script:
        scripts.append(write_stat(cur_test, cur_stat, results))

print template.replace("@CHART_SCRIPT@", string.join(scripts, "\n"))
