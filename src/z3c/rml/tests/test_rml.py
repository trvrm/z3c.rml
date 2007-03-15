##############################################################################
#
# Copyright (c) 2002 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTLAR PURPOSE.
#
##############################################################################
"""Testing all XML Locale functionality.

$Id$
"""
import os
import unittest
import z3c.rml.tests
from z3c.rml import rml2pdf, attr

class RMLRenderingTestCase(unittest.TestCase):

    def __init__(self, inPath, outPath):
        self._inPath = inPath
        self._outPath = outPath
        unittest.TestCase.__init__(self)

    def setUp(self):
        # Switch file opener for Image attibute
        self._imageOpen = attr.Image.open
        def testOpen(img, filename):
            path = os.path.join(os.path.dirname(self._inPath), filename)
            return open(path)
        attr.Image.open = testOpen

    def tearDown(self):
        attr.Image.open = self._imageOpen

    def runTest(self):
        rml2pdf.go(self._inPath, self._outPath)


def test_suite():
   suite = unittest.TestSuite()
   inputDir = os.path.join(os.path.dirname(z3c.rml.tests.__file__), 'input')
   outputDir = os.path.join(os.path.dirname(z3c.rml.tests.__file__), 'output')
   for filename in os.listdir(inputDir):
       if not filename.endswith(".rml"):
           continue
       inPath = os.path.join(inputDir, filename)
       outPath = os.path.join(outputDir, filename[:-4] + '.pdf')
       # Create new type, so that we can get test matching
       TestCase = type(filename[:-4].title(), (RMLRenderingTestCase,), {})
       case = TestCase(inPath, outPath)
       suite.addTest(case)
   return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')