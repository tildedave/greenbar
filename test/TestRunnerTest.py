#!/usr/bin/python26

import unittest 

from xml.dom.minidom import Node, parseString
from greenbar.TestRunner import TestCase

class TestCaseTest(unittest.TestCase):

    def from_xml(self, xml):
        doc = parseString(xml)
        node = doc.getElementsByTagName("testcase")[0]
        return TestCase(node)

    def test_gets_basic_dict_for_case(self):
        t = self.from_xml("""
<testcase classname="AwesomeClass" name="tests_is_awesome" time="0.001"></testcase>
""")
        test_dict = t.to_dict()

        self.assertEquals("tests_is_awesome", test_dict["name"])
        self.assertEquals("AwesomeClass", test_dict["class"])
        self.assertEquals("0.001", test_dict["time"])

    def test_get_success_result_for_testcase(self):
        t = self.from_xml("""
<testcase classname="AwesomeClass" name="tests_is_awesome" time="0.001"></testcase>
""")
        test_dict = t.to_dict()
        self.assertEquals("success", test_dict["result"])
        
    def test_gets_failure_result_for_testcase(self):
        t = self.from_xml("""
<testcase classname="AwesomeClass" name="tests_is_awesome" time="0.001">
      <failure>
      </failure>
</testcase>                             
""")
        test_dict = t.to_dict()
        self.assertEquals("failure", test_dict["result"])


class TestRunnerTest(unittest.TestCase):

    def setUp(self):
        pass

