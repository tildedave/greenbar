#!/usr/bin/python26

import sys
import os
import simplejson as json
import xml.dom.minidom
import time
from subprocess import Popen, PIPE

def displayTimestamp():
    return time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())

def testStatistics(testcase):
    classname = testcase.getAttribute("classname")
    name = testcase.getAttribute("name")
    time = testcase.getAttribute("time")
    
    return { 'class' : classname, 
             'name' : name,
             'time' : time }

def testFailed(ele):
    return len(ele.getElementsByTagName("failure")) > 0

def failureDetails(ele):
    return ele.getElementsByTagName("failure")[0].firstChild.data


class TestRunner:
    def __init__(self, directory):
        self.directory = directory

    def run(self):
        ms_start = time.time()
        output = Popen( ["nosetests", self.directory, "--with-xunit" ], 
                        stderr=PIPE, stdout=PIPE).communicate()[1]
        dom1 = xml.dom.minidom.parse("nosetests.xml")

        testsuite = dom1.getElementsByTagName("testsuite")[0]
        
        errors = int(testsuite.getAttribute("errors"))
        failures = int(testsuite.getAttribute("failures"))
        numtests = int(testsuite.getAttribute("tests"))
        success = (errors is 0) and (failures is 0)

        tests = []
    
        for testcase in dom1.getElementsByTagName("testcase"):
            stats = testStatistics(testcase)
            if testFailed(testcase):
                stats["result"] = "failure"
                stats["failure_details"] = failureDetails(testcase)
            else: 
                stats["result"] = "success"

            tests.append(stats)

        ms_done = time.time()
            
        data = { 'errors' : errors, 
                 'failures': failures, 
                 'numtests' : numtests,
                 'tests': tests, 
                 'output': output,
                 'success': success,
                 'nowtime': displayTimestamp(),
                 'totaltime': "%.3f" % (ms_done - ms_start) }

        return data
