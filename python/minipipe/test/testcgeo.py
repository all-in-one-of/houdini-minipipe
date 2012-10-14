from minipipe import cgeo
import hou
import os
import unittest

class TestCgeo(unittest.TestCase):
    def testWriteRead(self):
        hipPath = 'testdata/normalmap.hipnc'
        
        hou.hipFile.load(hipPath)
        
        geo = hou.node('/obj/geo1').displayNode().geometry()
        
        self.assertTrue(not geo.vertexAttribs(),
                        "test geometry has point attributes, these cannot be written")
        
        self.assertTrue(not geo.primAttribs(),
                        "test geometry has primitive attributes, these cannot be written")
        
        self.assertTrue(not geo.globalAttribs(),
                        "test geometry has detail attributes, these cannot be written")
        
        outPath = 'output/test.cgeo'
        
        cgeo.writeGeo(geo, outPath)
        
        self.assertTrue(os.path.exists(outPath),
                        "file doesn't exist after write")
        
        data = cgeo.readData(outPath)
        
        self.checkDataAgainstGeo(geo, data)

    def checkDataAgainstGeo(self, geo, data):
        # compare entity counts
        self.assertEqual(data['num_points'], len(geo.points()))
        self.assertEqual(data['num_prims'], len(geo.prims()))
        
        # substract one from pointAttribs, since we don't write Pw
        self.assertEqual(data['num_attribs'], len(geo.pointAttribs()) - 1)
        
        indices = data['indicies']
        
        self.assertEqual(len(indices), len(geo.prims() * 3))
        
        for i, p in enumerate(geo.prims()):
            pointNum = [v.point().number() for v in p.vertices()]
            
            self.assertEqual(indices[i * 3    ], pointNum[0])
            self.assertEqual(indices[i * 3 + 1], pointNum[1])
            self.assertEqual(indices[i * 3 + 2], pointNum[2])

        # compare attrib values        
        for attribName, attribSize, attribData in zip(data['attrib_names'], data['attrib_sizes'], data['attrib_data']):
            attrib = geo.findPointAttrib(attribName)
            
            self.assertTrue(attrib != None, "attrib %s doesn't exist in original geometry" % attribName)
            
            self.assertEqual(attribSize, attrib.size())
            
            for offset, p in enumerate(geo.points()):
                value = p.attribValue(attrib)
                for i in range(attribSize):
                    self.assertEqual(value[i], attribData[offset * attribSize + i])

