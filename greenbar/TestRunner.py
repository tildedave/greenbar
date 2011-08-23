#!/usr/bin/python26

import sys
import os
import simplejson as json
import xml.dom.minidom
import time
from subprocess import Popen, PIPE

def displayTimestamp():
    return time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())

def getTestStatistics(testcase):
    classname = testcase.getAttribute("classname")
    name = testcase.getAttribute("name")
    time = testcase.getAttribute("time")
    
    return { 'class' : classname, 
             'name' : name,
             'time' : time }

def hasTestFailed(ele):
    return len(ele.getElementsByTagName("failure")) > 0

def failureDetails(ele):
    return ele.getElementsByTagName("failure")[0].firstChild.data

class TestCase:
    def __init__(self, node):
        self.node = node

    def hasChild(self, str):
        return len(self.node.getElementsByTagName(str)) > 0

    def hasFailed(self):
        return self.hasChild("failure")

    def hasErrored(self):
        return self.hasChild("error")

    def details(self, str):
        return self.node.getElementsByTagName(str)[0].firstChild.data

    def failureDetails(self):
        return self.details("failure")

    def errorDetails(self):
        return self.details("error")

    def to_dict(self):
        classname = self.node.getAttribute("classname")
        name = self.node.getAttribute("name")
        time = self.node.getAttribute("time")
        
        d =  { 'class' : classname, 
               'name' : name,
               'time' : time }

        if self.hasFailed():
            d["result"] = "failure"
            d["details"] = self.failureDetails()
        elif self.hasErrored():
            d["result"] = "error"
            d["details"] = self.errorDetails()
        else: 
            d["result"] = "success"

        return d
        

class TestRunner:
    def __init__(self, directory):
        self.directory = directory

    def run(self):
        ms_start = time.time()
        output = Popen( ["nosetests", self.directory, "--with-xunit" ], 
                        stderr=PIPE, stdout=PIPE).communicate()[1]
        dom1 = xml.dom.minidom.parse("nosetests.xml")
        print dom1.toprettyxml()

        testsuite = dom1.getElementsByTagName("testsuite")[0]
        
        errors = int(testsuite.getAttribute("errors"))
        failures = int(testsuite.getAttribute("failures"))
        numtests = int(testsuite.getAttribute("tests"))
        success = (errors is 0) and (failures is 0)

        tests = []
    
        for testcase in dom1.getElementsByTagName("testcase"):
            stats = getTestStatistics(testcase)
            if hasTestFailed(testcase):
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