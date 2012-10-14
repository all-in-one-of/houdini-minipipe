from python import cgeo
import hou
import os
import unittest

class TestCgeo(unittest.TestCase):
    def testWrite(self):
        hipPath = 'D:\\android\\tests\\hip\\normalmap.hipnc'
        
        hou.hipFile.load(hipPath)
        
        geo = hou.node('/obj/geo1').displayNode().geometry()
        
        outPath = 'output/test.cgeo'
        
        cgeo.writeGeo(geo, outPath)
        
        self.assertTrue(os.path.exists(outPath), 'file not written')

    def testRead(self):
        inPath = 'output/test.cgeo'
        
        cgeo.readGeo(inPath)
        
        
#        self.assertTrue(os.path.exists(outPath), "file not written")
