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
    testname = testcase.getAttribute("name")
    time = testcase.getAttribute("time")
    
    return { 'classname' : classname, 
             'testname' : testname,
             'time' : time }

def testFailed(ele):
    return len(ele.getElementsByTagName("failure")) > 0

def failureDetails(ele):
    return ele.getElementsByTagName("failure")[0].firstChild.data


class TestRunner:
    def __init__(self, directory):
        self.directory = directory

    def run(self):
        output = Popen( ["nosetests", self.directory, "--with-xunit" ], 
                        stderr=PIPE, stdout=PIPE).communicate()[1]
        dom1 = xml.dom.minidom.parse("nosetests.xml")

        testsuite = dom1.getElementsByTagName("testsuite")[0]
        
        errors = testsuite.getAttribute("errors")
        failures = testsuite.getAttribute("failures")
        numtests = testsuite.getAttribute("tests")
     
        tests = []
    
        for testcase in dom1.getElementsByTagName("testcase"):
            stats = testStatistics(testcase)
            if testFailed(testcase):
                stats["result"] = "failure"
                stats["failure_details"] = failureDetails(testcase)
            else: 
                stats["result"] = "success"

            tests.append(stats)
            
        data = { 'errors' : errors, 
                 'failures': failures, 
                 'tests': tests, 
                 'output': output,
                 'nowtime': displayTimestamp() }
        return data
