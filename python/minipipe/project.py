import hou
from os import path

def gethipname():
    return path.basename(hou.hipFile.name()).split('.')[0]

def getoutpath(ropnode, frame, framepadding=4):
    outroot = ropnode.evalParm('outroot')
    subproject = ropnode.evalParm('subproject')
    seqname = ropnode.evalParm('seqname')
    version = str(ropnode.evalParm('version')).zfill(3)
    
    entryname = seqname + "_v" + version
    
    ext = 'bgeo'
    
    extparm = ropnode.parm('extension')
    
    if extparm != None:
        ext = extparm.eval()
    
    outPath = path.join(outroot, subproject, entryname)

    if frame != None:
        outPath = path.join(outPath, entryname + '_' + str(frame).zfill(framepadding) + '.' + ext)
    else:
        outPath = path.join(outPath, entryname + '.' + ext)
    
    return outPath

