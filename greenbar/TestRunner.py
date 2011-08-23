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
        
class TestSuite:

    def __init__(self, node):
        self.node = node

    def to_dict(self):
        errors = int(self.node.getAttribute("errors"))
        failures = int(self.node.getAttribute("failures"))
        numtests = int(self.node.getAttribute("tests"))
        success = (errors is 0) and (failures is 0)
        
        return {
            "errors": errors,
            "failures": failures,
            "numtests": numtests,
            "success": success
        }


class TestRunner:
    def __init__(self, directory):
        self.directory = directory

    
    def getTestOutput(self):
        return Popen( ["nosetests", self.directory, "--with-xunit" ], 
                      stderr=PIPE, stdout=PIPE).communicate()[1]

    def documentForTests(self):
        return xml.dom.minidom.parse("nosetests.xml")

    def getTests(self, doc):
        tests = []
    
        for testcase in doc.getElementsByTagName("testcase"):
            tests.append(TestCase(testcase).to_dict())

        return tests

    def run(self):
        ms_start = time.time()

        output = self.getTestOutput()
        dom1 = self.documentForTests()

        ts_node = dom1.getElementsByTagName("testsuite")[0]
        ts = TestSuite(ts_node)


        data = ts.to_dict()
        data["tests"] = self.getTests(dom1)
        data["output"] = output
        data["nowtime"] = displayTimestamp()

        ms_done = time.time()
        data["totaltime"] = "%.3f" % (ms_done - ms_start)

        return data