import maya.mel as mel
import maya.cmds as cmds
import pymel.core as pm
import maya.api.OpenMaya as om

version = int(cmds.about(version=True))

# Topology checks
def triangles(list, SLMesh):
    triangles = []
    selIt = om.MItSelectionList(SLMesh)
    while not selIt.isDone():
        faceIt = om.MItMeshPolygon(selIt.getDagPath())
        objectName = selIt.getDagPath().getPath()
        while not faceIt.isDone():
            numOfEdges = faceIt.getEdges()
            if len(numOfEdges) == 3:
                faceIndex = faceIt.index()
                componentName = str(objectName) + '.f[' + str(faceIndex) + ']'
                triangles.append(componentName)
            else:
                pass
            if version < 2020:
                faceIt.next(None)
            else:
                faceIt.next()
        selIt.next()
    return triangles

def ngons(list, SLMesh):
    ngons = []
    selIt = om.MItSelectionList(SLMesh)
    while not selIt.isDone():
        faceIt = om.MItMeshPolygon(selIt.getDagPath())
        objectName = selIt.getDagPath().getPath()
        while not faceIt.isDone():
            numOfEdges = faceIt.getEdges()
            if len(numOfEdges) > 4:
                faceIndex = faceIt.index()
                componentName = str(objectName) + '.f[' + str(faceIndex) + ']'
                ngons.append(componentName)
            else:
                pass
            if version < 2020:
                faceIt.next(None)
            else:
                faceIt.next()
        selIt.next()
    return ngons

def zeroAreaFaces(list, SLMesh):
    zeroAreaFaces = []
    selIt = om.MItSelectionList(SLMesh)
    while not selIt.isDone():
        faceIt = om.MItMeshPolygon(selIt.getDagPath())
        objectName = selIt.getDagPath().getPath()
        while not faceIt.isDone():
            faceArea = faceIt.getArea()
            if faceArea < 0.000001:
                faceIndex = faceIt.index()
                componentName = str(objectName) + '.f[' + str(faceIndex) + ']'
                zeroAreaFaces.append(componentName)
            else:
                pass
            if version < 2020:
                faceIt.next(None)
            else:
                faceIt.next()
        selIt.next()
    return zeroAreaFaces

def zeroLengthEdges(list, SLMesh):
    zeroLengthEdges = []
    selIt = om.MItSelectionList(SLMesh)
    while not selIt.isDone():
        edgeIt = om.MItMeshEdge(selIt.getDagPath())
        objectName = selIt.getDagPath().getPath()
        while not edgeIt.isDone():
            if edgeIt.length() < 0.00000001:
                componentName = str(objectName) + \
                    '.f[' + str(edgeIt.index()) + ']'
                zeroLengthEdges.append(componentName)
            edgeIt.next()
        selIt.next()
    return zeroLengthEdges

def openEdges(list, SLMesh):
    openEdges = []
    selIt = om.MItSelectionList(SLMesh)
    while not selIt.isDone():
        edgeIt = om.MItMeshEdge(selIt.getDagPath())
        objectName = selIt.getDagPath().getPath()
        while not edgeIt.isDone():
            if edgeIt.numConnectedFaces() < 2:
                edgeIndex = edgeIt.index()
                componentName = str(objectName) + '.e[' + str(edgeIndex) + ']'
                openEdges.append(componentName)
            else:
                pass
            edgeIt.next()
        selIt.next()
    return openEdges

def floatingVertices(list, SLMesh):
    poles = []
    selIt = om.MItSelectionList(SLMesh)
    while not selIt.isDone():
        vertexIt = om.MItMeshVertex(selIt.getDagPath())
        objectName = selIt.getDagPath().getPath()
        while not vertexIt.isDone():
            if vertexIt.numConnectedEdges() == 0:
                vertexIndex = vertexIt.index()
                componentName = str(objectName) + \
                    '.vtx[' + str(vertexIndex) + ']'
                poles.append(componentName)
            else:
                pass
            vertexIt.next()
        selIt.next()
    return poles

def poles(list, SLMesh):
    poles = []
    selIt = om.MItSelectionList(SLMesh)
    while not selIt.isDone():
        vertexIt = om.MItMeshVertex(selIt.getDagPath())
        objectName = selIt.getDagPath().getPath()
        while not vertexIt.isDone():
            if vertexIt.numConnectedEdges() > 5:
                vertexIndex = vertexIt.index()
                componentName = str(objectName) + \
                    '.vtx[' + str(vertexIndex) + ']'
                poles.append(componentName)
            else:
                pass
            vertexIt.next()
        selIt.next()
    return poles

def hardEdges(list, SLMesh):
    hardEdges = []
    selIt = om.MItSelectionList(SLMesh)
    while not selIt.isDone():
        edgeIt = om.MItMeshEdge(selIt.getDagPath())
        objectName = selIt.getDagPath().getPath()
        while not edgeIt.isDone():
            if edgeIt.isSmooth == False and edgeIt.onBoundary() == False:
                edgeIndex = edgeIt.index()
                componentName = str(objectName) + '.e[' + str(edgeIndex) + ']'
                hardEdges.append(componentName)
            else:
                pass
            edgeIt.next()
        selIt.next()
    return hardEdges

def lamina(list, SLMesh):
    selIt = om.MItSelectionList(SLMesh)
    lamina = []
    while not selIt.isDone():
        faceIt = om.MItMeshPolygon(selIt.getDagPath())
        objectName = selIt.getDagPath().getPath()
        while not faceIt.isDone():
            laminaFaces = faceIt.isLamina()
            if laminaFaces == True:
                faceIndex = faceIt.index()
                componentName = str(objectName) + '.f[' + str(faceIndex) + ']'
                lamina.append(componentName)
            else:
                pass
            if version < 2020:
                faceIt.next(None)
            else:
                faceIt.next()
        selIt.next()
    return lamina

def nonManifoldEdges(list, SLMesh):
    noneManifoldEdges = []
    selIt = om.MItSelectionList(SLMesh)
    while not selIt.isDone():
        edgeIt = om.MItMeshEdge(selIt.getDagPath())
        objectName = selIt.getDagPath().getPath()
        while not edgeIt.isDone():
            if edgeIt.numConnectedFaces() > 2:
                edgeIndex = edgeIt.index()
                componentName = str(objectName) + '.e[' + str(edgeIndex) + ']'
                noneManifoldEdges.append(componentName)
            else:
                pass
            edgeIt.next()
        selIt.next()
    return noneManifoldEdges

def starlike(list, SLMesh):
    starlike = []
    selIt = om.MItSelectionList(SLMesh)
    while not selIt.isDone():
        polyIt = om.MItMeshPolygon(selIt.getDagPath())
        objectName = selIt.getDagPath().getPath()
        while not polyIt.isDone():
            if polyIt.isStarlike() == False:
                polygonIndex = polyIt.index()
                componentName = str(objectName) + \
                    '.e[' + str(polygonIndex) + ']'
                starlike.append(componentName)
            else:
                pass
            if version < 2020:
                polyIt.next(None)
            else:
                polyIt.next()
        selIt.next()
    return starlike


#Model Check
def uncenteredPivots(list, SLMesh):
    uncenteredPivots = []
    for obj in list:
        if cmds.xform(obj, q=1, ws=1, rp=1) != [0, 0, 0]:
            uncenteredPivots.append(obj)
    return uncenteredPivots

def uncenteredPivots_fix(list, SLMesh):
    for obj in list:
        cmds.xform(obj, ws=True, os=True, a=True, rp=[0,0,0], sp=[0,0,0])
    return "fixed"

def lockedChannels(list, SLMesh):
    lockedChannels = []
    for obj in list:
        attributes = cmds.listAttr(obj, l=True)
        if attributes:
            for attr in attributes:
                lockedChannels.append("%s.%s" % (obj, attr))
    return lockedChannels

def lockedChannels_fix(list, SLMesh):
    for obj in list:
        cmds.setAttr(obj, l=False)
    return "fixed"

def normals(list, SLMesh):
    reversed_meshes = []
    for obj in list:
        #Conform object before looking for reversed faces:
        cmds.polyNormal(obj, normalMode=2, userNormalMode=0,  ch=1)
        reversed = []

        #Convert to faces, then to vertexFaces:
        faces = cmds.polyListComponentConversion(obj, toFace=True)
        face = cmds.ls(faces, flatten=True)[0]
        # for face in faces:
        verts = []
        vtxFaces = cmds.ls(cmds.polyListComponentConversion(face, toVertexFace=True), flatten=True)
        for vtxFace in vtxFaces:
            uvs = cmds.polyListComponentConversion(vtxFace, fromVertexFace=True, toUV=True)
            verts.append(uvs[0])
        uvs = verts

        #ignore non-valid faces
        if len(uvs) < 3:
            return 1, 0, 0

        #get uvs positions:
        uvA_xyz = cmds.polyEditUV(uvs[0], query=True, uValue=True, vValue=True)
        uvB_xyz = cmds.polyEditUV(uvs[1], query=True, uValue=True, vValue=True)
        uvC_xyz = cmds.polyEditUV(uvs[2], query=True, uValue=True, vValue=True)
        
        #get edge vector
        uvAB = pm.dt.Vector([uvB_xyz[0]-uvA_xyz[0], uvB_xyz[1]-uvA_xyz[1], 0])
        uvBC = pm.dt.Vector([uvC_xyz[0]-uvB_xyz[0], uvC_xyz[1]-uvB_xyz[1], 0])

        #cross product & normalize
        uvNormal = uvAB.cross(uvBC)
        uvNormal = uvNormal.normal()

        #if the uv face normal is facing into screen then its reversed - add it to the list
        if (uvNormal * pm.dt.Vector([0, 0, 1])) < 0:
            reversed.append(face)
        if reversed:
            reversed_meshes.append(obj)

        return reversed_meshes

def normals_fix(list, SLMesh):
    for obj in list:
        cmds.polyNormal(obj, normalMode=0, userNormalMode=0, ch=False)
        cmds.delete(obj, ch=True)
    return "fixed"

def unfrozenTransforms(list, SLMesh):
    unfrozenTransforms = []
    for obj in list:
        translation = cmds.xform(obj, q=True, worldSpace=True, translation=True)
        rotation = cmds.xform(obj, q=True, worldSpace=True, rotation=True)
        scale = cmds.xform(obj, q=True, worldSpace=True, scale=True)
        if not translation == [0.0, 0.0, 0.0] or not rotation == [0.0, 0.0, 0.0] or not scale == [1.0, 1.0, 1.0]:
            unfrozenTransforms.append(obj)
    return unfrozenTransforms

def unfrozenTransforms_fix(list, SLMesh):
    for obj in list:
        cmds.makeIdentity(obj, apply=True, t=True, r=True, s=True, n=False, pn=True)
    return "fixed"

def attributes(list, SLMesh):
    return ["Pending!"]

def attributes_fix(list, SLMesh):
    return ["Pending!"]

def smoothMesh(list, SLMesh):
    smoothMesh = []
    for obj in list:
        level = cmds.displaySmoothness(obj, q=True, polygonObject=True)[0]
        if level == 3:
            smoothMesh.append(obj)
    return smoothMesh

def smoothMesh_fix(list, SLMesh):
    for obj in list:
        cmds.displaySmoothness(obj, polygonObject=1, pointsShaded=1)
    return "fixed"

def intermediateObjects(list, SLMesh):
    intermediateObjects = []
    for obj in list:
        shape = cmds.listRelatives(obj, shapes=True, fullPath=True)
        if shape is not None:
            io = cmds.ls(shape, io=True)
            if io:
                intermediateObjects.append(obj)
    return intermediateObjects

def vcolor(list, SLMesh):
    vcolor = []
    for obj in list:
        existing_color_sets = cmds.polyColorSet(obj, q=True, acs=True)
        if not existing_color_sets:
            vcolor.append(obj)
        else:
            if "vcolor" not in existing_color_sets:
                vcolor.append(obj)
    return vcolor

def vcolor_fix(list, SLMesh):
    for obj in list:
        cmds.polyColorSet(obj, create=True, colorSet="vcolor")
    return "fixed"

def multipleShapes(list, SLMesh):
    multipleShapes = []
    for obj in list:
        shape = cmds.listRelatives(obj, shapes=True, fullPath=True)
        if len(shape) > 1:
            multipleShapes.append(obj)
    return multipleShapes

def multipleShapes_fix(list, SLMesh):
    for obj in list:
        shapes = cmds.listRelatives(obj, shapes=True, fullPath=True)
        shapes.pop(0)
        cmds.delete(shapes)
    return "fixed"

def negativeScale(list, SLMesh):
    negativeScale = []
    for obj in list:
        scales = cmds.getAttr("%s.scale" % obj)[0]
        if [s for s in scales if s < 0]:
            negativeScale.append(obj)
    return negativeScale

def negativeScale_fix(list, SLMesh):
    for obj in list:
        scales = cmds.getAttr("%s.scale" % obj)[0]
        if [s for s in scales if s < 0]:
            cmds.makeIdentity(obj, apply=True, s=True, n=False, pn=True)
    return "fixed"

def hierarchy(list, SLMesh):
    return ["Pending!"]

def hierarchy_fix(list, SLMesh):
    return ["Pending!"]

def shaders(list, SLMesh):
    shaders = []
    for obj in list:
        shadingGrps = None
        shape = cmds.listRelatives(obj, shapes=True, fullPath=True)
        if cmds.nodeType(shape) == 'mesh':
            if shape is not None:
                shadingGrps = cmds.listConnections(shape, type='shadingEngine')
            if not shadingGrps[0] == 'initialShadingGroup':
                shaders.append(obj)
    return shaders

def shaders_fix(list, SLMesh):
    for obj in list:
        lambert = cmds.ls(type="lambert")[0]
        sg = "initialShadingGroup"          
        cmds.sets(obj, e=True, forceElement=sg)
    return "fixed"

def history(list, SLMesh):
    history = []
    for obj in list:
        shape = cmds.listRelatives(obj, shapes=True, fullPath=True)
        if shape is not None:
            if cmds.nodeType(shape[0]) == 'mesh':
                historySize = len(cmds.listHistory(shape))
                if historySize > 1:
                    history.append(obj)
    return history

def history_fix(list, SLMesh):
    for obj in list:
        cmds.delete(obj, ch=True)
    return "fixed"


# UV checks
def currentUv(list, SLMesh):
    return ["Pending!"]

def multiUv(list, SLMesh):
    return ["Pending!"]

def missingUv(list, SLMesh):
    missingUVs = []
    selIt = om.MItSelectionList(SLMesh)
    while not selIt.isDone():
        faceIt = om.MItMeshPolygon(selIt.getDagPath())
        objectName = selIt.getDagPath().getPath()
        while not faceIt.isDone():
            if faceIt.hasUVs() == False:
                componentName = str(objectName) + \
                    '.f[' + str(faceIt.index()) + ']'
                missingUVs.append(componentName)
            if version < 2020:
                faceIt.next(None)
            else:
                faceIt.next()
        selIt.next()
    return missingUVs

def uvRange(list, SLMesh):
    uvRange = []
    selIt = om.MItSelectionList(SLMesh)
    while not selIt.isDone():
        faceIt = om.MItMeshPolygon(selIt.getDagPath())
        objectName = selIt.getDagPath().getPath()
        while not faceIt.isDone():
            UVs = faceIt.getUVs()
            for index, eachUVs in enumerate(UVs):
                if index == 0:
                    for eachUV in eachUVs:
                        if eachUV < 0 or eachUV > 10:
                            componentName = str(
                                objectName) + '.f[' + str(faceIt.index()) + ']'
                            uvRange.append(componentName)
                            break
                if index == 1:
                    for eachUV in eachUVs:
                        if eachUV < 0:
                            componentName = str(
                                objectName) + '.f[' + str(faceIt.index()) + ']'
                            uvRange.append(componentName)
                            break
            if version < 2020:
                faceIt.next(None)
            else:
                faceIt.next()
        selIt.next()
    return uvRange

def crossBorder(list, SLMesh):
    crossBorder = []
    selIt = om.MItSelectionList(SLMesh)
    while not selIt.isDone():
        faceIt = om.MItMeshPolygon(selIt.getDagPath())
        objectName = selIt.getDagPath().getPath()
        while not faceIt.isDone():
            U = None
            V = None
            UVs = faceIt.getUVs()
            for index, eachUVs in enumerate(UVs):
                if index == 0:
                    for eachUV in eachUVs:
                        if U == None:
                            U = int(eachUV)
                        if U != int(eachUV):
                            componentName = str(
                                objectName) + '.f[' + str(faceIt.index()) + ']'
                            crossBorder.append(componentName)
                if index == 1:
                    for eachUV in eachUVs:
                        if V == None:
                            V = int(eachUV)
                        if V != int(eachUV):
                            componentName = str(
                                objectName) + '.f[' + str(faceIt.index()) + ']'
                            crossBorder.append(componentName)
            if version < 2020:
                faceIt.next(None)
            else:
                faceIt.next()
        selIt.next()
    return crossBorder

def selfPenetratingUv(list, SLMesh):
    selfPenetratingUVs = []
    for obj in list:
        shape = cmds.listRelatives(obj, shapes=True, fullPath=True)
        convertToFaces = cmds.ls(
            cmds.polyListComponentConversion(shape, tf=True), fl=True)
        overlapping = (cmds.polyUVOverlap(convertToFaces, oc=True))
        if overlapping is not None:
            for obj in overlapping:
                selfPenetratingUVs.append(obj)
    return selfPenetratingUVs


#Naming Checks
def trailingNumbers(list, SLMesh):
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    trailingNumbers = []
    for obj in list:
        if obj[len(obj)-1] in numbers:
            trailingNumbers.append(obj)
    return trailingNumbers

def duplicatedNames(list, SLMesh):
    duplicatedNames = []
    for item in list:
        if '|' in item:
            duplicatedNames.append(item)
    return duplicatedNames

def shapeNames(list, SLMesh):
    shapeNames = []
    for obj in list:
        new = obj.split('|')
        shape = cmds.listRelatives(obj, shapes=True)
        if shape is not None:
            name = new[-1] + "Shape"
            if not shape[0] == name:
                shapeNames.append(obj)
    return shapeNames

def shapeNames_fix(list, SLMesh):
    for obj in list:
        shape = cmds.listRelatives(obj, shapes=True, fullPath=True)[0]
        newShape = "%sShape" % obj
        cmds.rename(shape, newShape)
    return "fixed"

def namespaces(list, SLMesh):
    namespaces = []
    for obj in list:
        if ':' in obj:
            namespaces.append(obj)
    return namespaces

def namespaces_fix(list, SLMesh):
    for obj in list:
        cmds.namespace(set=":")
        name = obj.split(":")[-1]
        cmds.rename(obj, name)
    return "fixed"

#Texture Checks
def textureSize(list, SLMesh):
    return ["Pending!"]

def imageBrightness(list, SLMesh):
    return ["Pending!"]

def textureNames(list, SLMesh):
    return ["Pending!"]


#Lookdev Check/Fix
def colorSet(list, SLMesh):
    colorSet = []
    for obj in list:
        existing_color_sets = cmds.polyColorSet(obj, q=True, acs=True)
        if existing_color_sets:
            colorSet.append(obj)
    return colorSet

def colorSet_fix(list, SLMesh):
    for obj in list:
        existing_color_sets = cmds.polyColorSet(obj, q=True, acs=True)
        for existing_color_set in existing_color_sets:
            cmds.polyColorSet(colorSet=existing_color_set, delete=True)
    return "fixed"

def unusedShaders(list, SLMesh):
    mel.eval('hyperShadePanelMenuCommand("hyperShadePanel1","deleteUnusedNodes")')

def unusedShaders_fix(list, SLMesh):
    mel.eval('hyperShadePanelMenuCommand("hyperShadePanel1","deleteUnusedNodes")')
    return "fixed"

def standardSurface(list, SLMesh):
    standardSurface = []
    for obj in list:
        shape = cmds.listRelatives(obj, shapes=True, fullPath=True)
        sgNodes = cmds.listConnections(shape, type='shadingEngine')
        matMaya = cmds.listConnections(sgNodes[0] + '.surfaceShader')
        if matMaya:
            if cmds.objectType(matMaya[0]) != "standardSurface":
                standardSurface.append(obj)
    return standardSurface

def standardSurface_fix(list, SLMesh):
    for obj in list:
        standardSurface = cmds.ls(type="standardSurface")[0]
        if not cmds.objExists("standardSurfaceSG"):
            sg = cmds.sets(name="standardSurfaceSG", empty=True, renderable=True, noSurfaceShader=True)
            cmds.connectAttr("%s.outColor" % standardSurface, "%s.surfaceShader" % sg)
        else:
            sg = "standardSurfaceSG"
        cmds.sets(obj, e=True, forceElement=sg)
    return "fixed"


# Scene checks
def cleanUp(list, SLMesh):
    mel.eval('MLdeleteUnused;')
    pfxToons = cmds.ls(type="pfxToon")
    if pfxToons:
        for pfxToon in pfxToons:
            cmds.delete(cmds.listRelatives(pfxToon, p=True))

def referenceCheck(list, SLMesh):
    references = cmds.file(q=True, r=True)
    if references:
        return references

def unitCheck(list, SLMesh):
    if not cmds.currentUnit(q=True, l=True) in ["mm", "cm"]:
        return ["Unit is not cm or mm"]

def animationKeys(list, SLMesh):
    animationKeys = []
    for obj in list:
        animCurves = cmds.listConnections(obj, type="animCurve")
        if animCurves:
            animationKeys.append(obj)
    return animationKeys

def animationKeys_fix(list, SLMesh):
    for obj in list:
        animCurves = cmds.listConnections(obj, type="animCurve")
        cmds.delete(animCurves)
    return "fixed"

def emptyGroups(list, SLMesh):
    emptyGroups = []
    for obj in list:
        children = cmds.listRelatives(obj, ad=True)
        if children is None:
            emptyGroups.append(obj)
    return emptyGroups

def layers(list, SLMesh):
    layers = cmds.ls(type="displayLayer")
    layers.remove("defaultLayer")
    if layers:
        return layers

def layers_fix(list, SLMesh):
    layers = cmds.ls(type="displayLayer")
    layers.remove("defaultLayer")
    for layer in layers:
        try:
            cmds.delete(layer)
        except:
            return "Error"
    return "fixed"

# Intersections Check
def intersections(list, SLMesh):
    if len(cmds.ls(sl=True)) == 0:
        return ["Nothing selected!"]

    sceneBefore = cmds.ls(type="transform")
    objectCount = len(sceneBefore)
    mel.eval("assignNewPfxToon;")
    sceneNow = cmds.ls(type="transform")
    objectCountNow = len(sceneNow)
    
    if objectCountNow > objectCount:
        diff = objectCountNow - objectCount
        newObjs = cmds.ls(sl=True, tail=diff)
        cmds.select(newObjs)

    list = cmds.ls(sl=True)
    for obj in list:
        cmds.select(obj)
        cmds.setAttr("%s.creaseLines" % obj, 0)
        cmds.setAttr("%s.borderLines" % obj, 0)
        cmds.setAttr("%s.intersectionLines" % obj, 1)
        cmds.setAttr("%s.lineWidth" % obj, 0.05)
        cmds.setAttr("%s.intersectionColor" % obj, 1, 0, 1,  type="double3")
        cmds.setAttr("%s.occlusionWidthScale" % obj, 0)
        cmds.setAttr("%s.profileLineWidth" % obj, 0)
        cmds.setAttr("%s.selfIntersect" % obj, 1)
        cmds.setAttr("%s.profileLines" % obj, 0)
        cmds.setAttr("%s.resampleIntersection" % obj, 1)