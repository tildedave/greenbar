#!/usr/bin/python26

import tornado.ioloop
import tornado.web 

from optparse import OptionParser
from TestRunner import TestRunner
from TestRunner import displayTimestamp

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("greenbar.tpl", nowtime=displayTimestamp())

class ResultHandler(tornado.web.RequestHandler):
    
    def initialize(self, directory):
        self.directory = directory
    
    def get(self):
        testRunner = TestRunner(self.directory)
        self.write(testRunner.run())

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-d", "--directory", dest="directory",
                      help="test directory", metavar="DIRECTORY")

    (options, args) = parser.parse_args()

    if (not options.directory):
        parser.error("Must specify a directory with --directory")

    application = tornado.web.Application([
        (r"/", IndexHandler),
        (r"/results", ResultHandler, {"directory": options.directory}),
        (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": "static/"})
    ],debug=True)

    application.listen(7000)
    application.debug = True
    tornado.ioloop.IOLoop.instance().start()
