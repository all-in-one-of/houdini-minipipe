import hou
import struct

MAX_ATTRIBNAME_LEN = 32

def checkGeo(geo):
    prims = geo.prims()
    for p in prims:
        verts = p.vertices()
        if len(verts) != 3:
            raise hou.Error('Non-Triangle primitive found')

def writeGeo(geo, outpath, attribs=None, version=2):
    with open(outpath,'wb') as f:
        
        points = geo.points()
        prims = geo.prims()
        
        if version == 1:
            uvAttrib = geo.findPointAttrib('uv')
            
            f.write(struct.pack('>ii', len(points), len(prims)))
            
            
            for p in points:
                pos = p.position()
                f.write(struct.pack('>fff',pos[0],pos[1],pos[2]))
            
            for p in points:
                uv = p.attribValue(uvAttrib)
                f.write(struct.pack('>ff',uv[0],1-uv[1]))
            
            for p in prims:
                verts = p.vertices()
                if len(verts) != 3:
                    raise hou.Error('Non-Triangle primitive found')
            
                f.write(struct.pack('>HHH', verts[0].point().number(), verts[1].point().number(), verts[2].point().number()))
        
        if version == 2:
            checkGeo(geo)
            
            excludeAttribs = ('Pw',)
            
            writeAttribs = [attrib for attrib in geo.pointAttribs() 
                                   if (attribs == None or attrib.name() in attribs) and
                                   attrib.name() not in excludeAttribs]
            
            f.write(struct.pack('>iii', len(points), len(prims), len(writeAttribs)))
            
            for attrib in writeAttribs:
                attribName = attrib.name()
                nameLen = len(attribName)
                attribSize = attrib.size()
    
                if nameLen > MAX_ATTRIBNAME_LEN:
                    raise hou.Error('Attrib name too long at %d chars. Max: %d' % (nameLen, MAX_ATTRIBNAME_LEN))
                
                f.write(struct.pack('>%ds' % MAX_ATTRIBNAME_LEN, attribName))
                f.write(struct.pack('>i', attribSize))
            
            for p in prims:
                verts = p.vertices()
                if len(verts) != 3:
                    raise hou.Error('Non-Triangle primitive found')
            
                f.write(struct.pack('>HHH', verts[0].point().number(), verts[1].point().number(), verts[2].point().number()))
                
            for attrib in writeAttribs:
                for p in points:
                    
                    value = p.attribValue(attrib)
                    
                    if isinstance(value, tuple):
                        f.write(struct.pack('>%df' % len(value), *value))
                    else:
                        f.write(struct.pack('>f', value))


def readData(inpath):
    """
    test
    """
    with open(inpath, 'rb') as f:
        headerPacking = ">iii"
        size = struct.calcsize(headerPacking)
        
        numPoints, numPrims, numAttribs = struct.unpack(headerPacking, f.read(size))
        numIndices = 3 * numPrims
        
#        print numPoints, numPrims, numAttribs
        
        
        attribName = [None, ] * numAttribs
        attribSize = [0, ] * numAttribs
        attribData = [None, ] * numAttribs
        
        
        for i in range(numAttribs):
            attribPacking = ">%dsi" % MAX_ATTRIBNAME_LEN
            size = struct.calcsize(attribPacking)
            attribName[i], attribSize[i] = struct.unpack(attribPacking, f.read(size))
            attribName[i] = attribName[i].rstrip(' \t\r\n\0')
#            print attribName[i]

        dataPacking = ">%dH" % numIndices
        size = struct.calcsize(dataPacking)
        vertIndices = struct.unpack(dataPacking, f.read(size))

        for i in range(numAttribs):
            dataPacking = ">%df" % (numPoints * attribSize[i])
            size = struct.calcsize(dataPacking)
            attribData[i] = struct.unpack(dataPacking, f.read(size)) 
            
    return {
            'num_points': numPoints,
            'num_prims': numPrims,
            'num_attribs': numAttribs,
            'indicies': vertIndices,
            'attrib_names': attribName,
            'attrib_sizes': attribSize,
            'attrib_data': attribData 
            }
