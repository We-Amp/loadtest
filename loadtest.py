#!/usr/bin/env python

import copy
import datetime
import os
import re
import string
import subprocess
import time
from config import loadtest_config

def process_result(epoch, test_name, concurrency, output, pattern):
    filter(lambda x: x in string.printable, output)

    for line in output.split("\n"):
        match = re.search(pattern, line)
        if not match is None:
            key, val = (match.group("key"), match.group("val"))
            if key and val:
                with open("result/%s-%s-%s" % (test_name, concurrency, key), "a") as myfile:
                    myfile.write("%d %s\n" % (epoch, val))

def replace_placeholders(s,ph):
    for key,val in ph.items():
        if type(val) == str:
            s = s.replace("@%s@" % key, val)
    return s

def execute_test(epoch, testconfig):
    print "Execute [%s]" % test["name"]    
    for concurrency in testconfig["concurrencies"]:
        popen_args = copy.deepcopy(testconfig["popen_args"])
        testconfig["concurrency"] = str(concurrency)
        for idx, val in enumerate(popen_args):
            popen_args[idx] = replace_placeholders(val, testconfig)

        print popen_args

        with open(os.devnull, "w") as fnull:
            p = subprocess.Popen(popen_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # TODO(oschaaf): buffering the output might consume a lot of memory for siege.
            # it would be good to be able to send stdin to /dev/null for siege. Fix
            stdout,stderr = p.communicate()
            rc = p.wait()
            if rc != 0:
                print "load tool error [%d]" % (rc)
                return False
            else:
                pattern = re.compile(testconfig["re_parse"], re.IGNORECASE)
                process_result(epoch, testconfig["name"], concurrency, stdout + "\n" + stderr, pattern)

    return True


config = loadtest_config()
epoch = int(time.time())
result_dir = config["result_dir"]

if not os.path.exists(result_dir):
    os.makedirs(result_dir)

for test in config["tests"]:
    execute_test(epoch, test)

print "Load test done. Timestamp used in stats:"

with open("%slast" % result_dir, "w") as f:
    f.write(str(epoch))

print str(epoch)
