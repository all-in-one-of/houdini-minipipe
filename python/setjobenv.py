import os
import hou

def getfolders(path):
    folders=[]
    while 1:
        path,folder=os.path.split(path)
    
        if folder!="":
            folders.append(folder)
        else:
            if path!="":
                folders.append(path)
    
            break

    folders.reverse()
    return folders

def set():
	hipPath = os.path.dirname(hou.hipFile.name())

	pathParts = getfolders(hipPath)

	#hipName = os.path.splitext(os.path.basename(hou.hipFile.name())[0]

	if pathParts[-1] != 'hip':
		raise hou.Error("hip file does not reside in a directory called 'hip', can't get job name")

	jobPath = os.path.join(os.path.split(hipPath)[0])

	hou.hscript("setenv JOB=%s" % jobPath)

	jobName = pathParts[-2]

	hou.hscript('setenv JOBCACHE=E:/Projects/%s' % jobName)
