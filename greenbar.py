#!/usr/bin/python26

import bottle
import sys
import os
import simplejson as json
import xml.dom.minidom
import time

from StringIO import StringIO
from bottle import route, run, template, static_file
from optparse import OptionParser
from subprocess import Popen, PIPE

DIRECTORY = None

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

@route('/static/:filename')
def server_static(filename):
    return static_file(filename, 'static')

@route('/')
def index():
    nowtime = time.localtime()
    return template('greenbar', nowtime=displayTimestamp())

@route('/results')
def results():
    output = Popen( ["nosetests", DIRECTORY, "--with-xunit" ], 
                    stderr=PIPE, stdout=PIPE).communicate()[1]

    dom1 = xml.dom.minidom.parse("nosetests.xml")
    print dom1.toprettyxml()

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

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-d", "--directory", dest="directory",
                      help="test directory", metavar="DIRECTORY")

    (options, args) = parser.parse_args()

    if (not options.directory):
        parser.error("Must specify a directory with --directory")

    DIRECTORY=options.directory

    bottle.debug(True)
    run(host='localhost', port=7000, reloader=True)