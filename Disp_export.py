Save_Path = 'E:/temp/GC/MG/'
for i in range(1, 4):
    resultFileName = Save_Path + '%s-6' %i + '.txt'
    new_content = []

    
    session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
        variableLabel='U', outputPosition=NODAL, refinement=(COMPONENT, 'U2'))
    session.viewports['Viewport: 1'].odbDisplay.setFrame(step=6, frame=1)
    pth = session.paths['Path-%s' %i]
    resultList=session.XYDataFromPath(name='path-%s-%s' %(i, 1), path=pth, includeIntersections=False, 
        projectOntoMesh=False, pathStyle=PATH_POINTS, numIntervals=10, 
        projectionTolerance=0, shape=UNDEFORMED, labelType=Z_COORDINATE, 
        removeDuplicateXYPairs=True, includeAllElements=False)
    for n in range(0, len(resultList)):
        if n == len(resultList)-1:
            new_lines = str(resultList[n][0]) + '\n'
        else:
            new_lines = str(resultList[n][0]) + ','
        new_content.append(new_lines)

    for j in range(0, 132):
        session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
            variableLabel='U', outputPosition=NODAL, refinement=(COMPONENT, 'U2'))
        session.viewports['Viewport: 1'].odbDisplay.setFrame(step=6, frame=j)
        pth = session.paths['Path-%s' %i]
        resultList=session.XYDataFromPath(name='path-%s-%s' %(i, j), path=pth, includeIntersections=False, 
            projectOntoMesh=False, pathStyle=PATH_POINTS, numIntervals=10, 
            projectionTolerance=0, shape=UNDEFORMED, labelType=Z_COORDINATE, 
            removeDuplicateXYPairs=True, includeAllElements=False)
        for n in range(0, len(resultList)):
            if n == len(resultList)-1:
               new_lines = str(resultList[n][1]) + '\n'
            else:
                new_lines = str(resultList[n][1]) + ','
            new_content.append(new_lines)
    with open(resultFileName, 'w+') as f:
        f.writelines(new_content)
