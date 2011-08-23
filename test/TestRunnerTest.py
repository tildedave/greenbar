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
<testcase classname="AwesomeClass" name="tests_basic_dict" time="0.001"></testcase>
""")
        test_dict = t.to_dict()

        self.assertEquals("tests_basic_dict", test_dict["name"])
        self.assertEquals("AwesomeClass", test_dict["class"])
        self.assertEquals("0.001", test_dict["time"])

    def test_get_success_result_for_testcase(self):
        t = self.from_xml("""
<testcase classname="AwesomeClass" name="tests_success_result" time="0.001"></testcase>
""")
        test_dict = t.to_dict()
        self.assertEquals("success", test_dict["result"])
        
    def test_gets_failure_result_for_testcase(self):
        t = self.from_xml("""
<testcase classname="AwesomeClass" name="tests_failure_result" time="0.001">
      <failure>
      </failure>
</testcase>                             
""")
        test_dict = t.to_dict()
        self.assertEquals("failure", test_dict["result"])

    def test_gets_failure_details_for_testcase(self):
        t = self.from_xml("""
<testcase classname="AwesomeClass" name="tests_failure_details" time="0.001">
      <failure><![CDATA[Failed in a horrible way!]]>
      </failure>
</testcase>                             
""")
        test_dict = t.to_dict()

        self.assertEquals("Failed in a horrible way!", 
                          test_dict["details"])

    def test_gets_error_result_for_testcase(self):
        t = self.from_xml("""
<testcase classname="Errrrrror" name="tests_error_result" time="1.000">
         <error>
         </error>
</testcase>
""")
        test_dict = t.to_dict()

        self.assertEquals("error", test_dict["result"])

    def test_gets_error_details_for_testcase(self):
        t = self.from_xml("""
<testcase classname="Errrrrror2" name="tests_error_details" time="1.000">
         <error><![CDATA[Oh my god an error~!]]></error>
</testcase>
""")
        test_dict = t.to_dict()
        
        self.assertEquals("Oh my god an error~!", test_dict["details"])


class TestRunnerTest(unittest.TestCase):

    def setUp(self):
        pass

