import os
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
    return triangles, "is a Triangle"

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
    return ngons, "is an Ngon"

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
    return zeroAreaFaces, "is a Zero Area Face"

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
    return zeroLengthEdges, "is a Zero Length Edge"

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
    return openEdges, "is an open Edge"

def floatingVertices(list, SLMesh):
    floatingVertices = []
    selIt = om.MItSelectionList(SLMesh)
    while not selIt.isDone():
        vertexIt = om.MItMeshVertex(selIt.getDagPath())
        objectName = selIt.getDagPath().getPath()
        while not vertexIt.isDone():
            if vertexIt.numConnectedEdges() == 0:
                vertexIndex = vertexIt.index()
                componentName = str(objectName) + \
                    '.vtx[' + str(vertexIndex) + ']'
                floatingVertices.append(componentName)
            else:
                pass
            vertexIt.next()
        selIt.next()
    return floatingVertices, "is a Floating Vertex"

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
    return poles, "is a Pole Vertex"

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
    return hardEdges, "is a Hard Edge"

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
    return lamina, "is a Lamina Face"

def nonManifoldEdges(list, SLMesh):
    nonManifoldEdges = []
    selIt = om.MItSelectionList(SLMesh)
    while not selIt.isDone():
        edgeIt = om.MItMeshEdge(selIt.getDagPath())
        objectName = selIt.getDagPath().getPath()
        while not edgeIt.isDone():
            if edgeIt.numConnectedFaces() > 2:
                edgeIndex = edgeIt.index()
                componentName = str(objectName) + '.e[' + str(edgeIndex) + ']'
                nonManifoldEdges.append(componentName)
            else:
                pass
            edgeIt.next()
        selIt.next()
    return nonManifoldEdges, "is a Non Manifold Edge"

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
    return starlike, "is a Star Face"


#Model Check
def uncenteredPivots(list, SLMesh):
    uncenteredPivots = []
    for obj in list:
        if cmds.xform(obj, q=1, ws=1, rp=1) != [0, 0, 0]:
            uncenteredPivots.append(obj)
    return uncenteredPivots, "pivot is not at origin"

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
    return lockedChannels, "is a locked channel"

def lockedChannels_fix(list, SLMesh):
    for obj in list:
        cmds.setAttr(obj, l=False)
    return "fixed"

def normals(list, SLMesh):
    reversed_meshes = []
    for obj in list:
        #Conform object before looking for reversed faces:
        polyNormal = cmds.polyNormal(obj, normalMode=2, userNormalMode=0,  ch=1)
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

        cmds.delete(polyNormal)

        return reversed_meshes, "normals is reversed"

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
    return unfrozenTransforms, "has transformations"

def unfrozenTransforms_fix(list, SLMesh):
    for obj in list:
        cmds.makeIdentity(obj, apply=True, t=True, r=True, s=True, n=False, pn=True)
        cmds.delete(obj, ch=True)
    return "fixed"

def attributes(list, SLMesh):
    attributes = []
    for obj in list:
        smoothMeshPreview = cmds.getAttr("%s.displaySmoothMesh" % obj)
        displaySubd = cmds.getAttr("%s.displaySubdComps" % obj)
        previewDivisionLevels = cmds.getAttr("%s.smoothLevel" % obj)
        usePreviewLevel = cmds.getAttr("%s.useSmoothPreviewForRender" % obj)
        renderDivisionLevel = cmds.getAttr("%s.renderSmoothLevel" % obj)
        if smoothMeshPreview != 0 or \
                displaySubd != 1 or \
                previewDivisionLevels != 1 or \
                usePreviewLevel != 1 or \
                renderDivisionLevel != 1:           
            attributes.append(obj)
    return attributes, "does not have Default Smooth Attributes"

def attributes_fix(list, SLMesh):
    for obj in list:
        cmds.setAttr("%s.displaySmoothMesh" % obj, 0)
        cmds.setAttr("%s.displaySubdComps" % obj, 1)
        cmds.setAttr("%s.smoothLevel" % obj, 1)
        cmds.setAttr("%s.useSmoothPreviewForRender" % obj, 1)
        cmds.setAttr("%s.renderSmoothLevel" % obj, 1)
    return "fixed"

def intermediateObjects(list, SLMesh):
    intermediateObjects = []
    for obj in list:
        shape = cmds.listRelatives(obj, shapes=True, fullPath=True)
        if shape is not None:
            io = cmds.ls(shape, io=True)
            if io:
                intermediateObjects.append(obj)
    return intermediateObjects, "has Intermediate Objects"

def vcolor(list, SLMesh):
    vcolor = []
    for obj in list:
        existing_color_sets = cmds.polyColorSet(obj, q=True, acs=True)
        if not existing_color_sets:
            vcolor.append(obj)
        else:
            if "vcolor" not in existing_color_sets:
                vcolor.append(obj)
    
    return vcolor, "vcolor set does not exists!"

def vcolor_fix(list, SLMesh):
    for obj in list:
        cmds.polyColorSet(obj, create=True, colorSet="vcolor")
        cmds.delete(obj, ch=True)
    return "fixed"

def multipleShapes(list, SLMesh):
    multipleShapes = []
    for obj in list:
        shape = cmds.listRelatives(obj, shapes=True, fullPath=True)
        if len(shape) > 1:
            multipleShapes.append(obj)
    return multipleShapes, "has Multiple Shapes"

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
    return negativeScale, "has Negative Scales"

def negativeScale_fix(list, SLMesh):
    for obj in list:
        scales = cmds.getAttr("%s.scale" % obj)[0]
        if [s for s in scales if s < 0]:
            cmds.makeIdentity(obj, apply=True, s=True, n=False, pn=True)
    return "fixed"

def modelHierarchy(list, SLMesh):
    modelHierarchy = []
    for obj in list:
        parent = cmds.listRelatives(obj, p=True)
        if parent:
            if parent[0] not in ["low", "base", "hi", "sculpt"]:
                modelHierarchy.append(obj)
        else:
            modelHierarchy.append(obj)
    return modelHierarchy, "is not parented in the Correct Model Group"

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
    return shaders, "is not assigned to Lambert"

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
    return history, "has History"

def history_fix(list, SLMesh):
    for obj in list:
        cmds.delete(obj, ch=True)
    return "fixed"


# UV checks
def currentUv(list, SLMesh):
    currentUVs = []
    for obj in list:
        currentUVSet = cmds.polyUVSet( obj, q=True, currentUVSet=True )[0]
        if currentUVSet != "map1":
            currentUVs.append(obj)
    return currentUVs, "currentUV is not 'map1'"

def multiUv(list, SLMesh):
    multiUVs = []
    uv_sets = ["map1", "custommask"]
    for obj in list:
        allUVSet = cmds.polyUVSet( obj, q=True, allUVSets=True )
        check =  all(item in allUVSet for item in uv_sets)
        if not check:
            multiUVs.append(obj)
    return multiUVs, "Incorrect UV Set name or has only One UV Set"

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
    return missingUVs, "has no UV sets"

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
    return uvRange, "UV Range Error"

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
    return crossBorder, "UV's crossing Borders"

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
    return selfPenetratingUVs, "has Self-Penetrating UVs"


#Naming Checks
def trailingNumbers(list, SLMesh):
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    trailingNumbers = []
    for obj in list:
        if obj[len(obj)-1] in numbers:
            trailingNumbers.append(obj)
    return trailingNumbers, "No trailing numbers"

def duplicatedNames(list, SLMesh):
    duplicatedNames = []
    for item in list:
        cmds.ls(item)
        if '|' in item:
            duplicatedNames.append(item)
    return duplicatedNames, "Duplicate names in scene"

def shapeNames(list, SLMesh):
    shapeNames = []
    for obj in list:
        new = obj.split('|')
        shape = cmds.listRelatives(obj, shapes=True)
        if shape is not None:
            name = new[-1] + "Shape"
            if not shape[0] == name:
                shapeNames.append(obj)
    return shapeNames, "Incorrect Shape Name"

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
    return namespaces, "Namespace Error"

def namespaces_fix(list, SLMesh):
    for obj in list:
        cmds.namespace(set=":")
        name = obj.split(":")[-1]
        cmds.rename(obj, name)
    return "fixed"

#Texture Checks
def textureSize(list, SLMesh):
    textures = []
    files = cmds.ls(type='file')
    for f in files:
        shader = cmds.listConnections("%s.outColor" % f, d=True)
        if shader:
            textureFile = cmds.getAttr("%s.fileTextureName" % f)
            width = cmds.getAttr("%s.outSizeX" % f)
            height = cmds.getAttr("%s.outSizeY" % f)
            if width != 4096 or height != 4096:
                textures.append(shader[0])
            elif width != 8192 or height != 8192:
                textures.append(shader[0])
            else:
                textures.append(shader[0])
    if not files:
        return [None], "No Texture Files found"
    else:
        return textures, "Texture is not 4K or 8K"

def imageBrightness(list, SLMesh):
    try:
        import PIL
        from PIL import Image
    except:
        return ["Import Error"], "Module Image from PIL not found"
    imageBrightness = []
    files = cmds.ls(type='file')
    for f in files:
        shader = cmds.listConnections("%s.outColor" % f, d=True)
        if shader:
            textureFile = cmds.getAttr("%s.fileTextureName" % f)
            img = Image.open(textureFile) 
            extrema = img.convert("L").getextrema()
            if extrema == (0, 0):
                imageBrightness.append(f)
            elif extrema == (1, 1):
                imageBrightness.append(f)
    if not files:
        return [None], "No Texture Files found"
    else:
        return imageBrightness, "is either Black or White"

def textureNames(list, SLMesh):
    textureTypes = ["baseColor", "height", "metalness", "normal", "roughness", "emissive", "mask"]
    textures = []
    files = cmds.ls(type='file')
    for f in files:
        textureFile = cmds.getAttr("%s.fileTextureName" % f)
        textureName = os.path.basename(textureFile)
        try:
            name, udim, format = textureName.split(".")
            project, asset, object, channel = name.split("_")
            
            if channel not in textureTypes: textures.append(f)
            elif format != "exr": textures.append(f)
            elif not ((abs(1000 - int(udim)) <= 100) or (abs(2000 - int(udim)) <= 100)): textures.append(f)
        except:
            textures.append(f)
    if not files:
        return [None], "No Texture Files found"
    else:
        return textures, "Texture Name Format Error, Format: #[project]_[asset]_[object]_[channel].[udim].exr"


#Lookdev Check/Fix
def colorSet(list, SLMesh):
    colorSet = []
    for obj in list:
        existing_color_sets = cmds.polyColorSet(obj, q=True, acs=True)
        if existing_color_sets:
            colorSet.append(obj)
    return colorSet, "Color Sets Found"

def colorSet_fix(list, SLMesh):
    for obj in list:
        existing_color_sets = cmds.polyColorSet(obj, q=True, acs=True)
        for existing_color_set in existing_color_sets:
            cmds.polyColorSet(colorSet=existing_color_set, delete=True)
    return "fixed"

def unusedShaders(list, SLMesh):
    mel.eval('hyperShadePanelMenuCommand("hyperShadePanel1","deleteUnusedNodes")')
    return [], ""

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
    return standardSurface, "is not assigned to StandardSurface"

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
    return [], ""

def referenceCheck(list, SLMesh):
    references = []
    references = cmds.file(q=True, r=True)
    if references:
        return references, "References Found!"
    else:
        return references, ""

def hierarchy(list, SLMesh):
    hierarchy = []
    groups = ["meta", "stock", "root"]
    for group in groups:
        if not cmds.objExists(group):
            hierarchy.append(group)
    return hierarchy, "group is missing"

def unitCheck(list, SLMesh):
    unit = cmds.currentUnit(q=True, l=True)
    if not unit in ["mm", "cm"]:
        return [unit], "is not mm or cm"
    else:
        return [], ""

def animationKeys(list, SLMesh):
    animationKeys = []
    for obj in list:
        animCurves = cmds.listConnections(obj, type="animCurve")
        if animCurves:
            animationKeys.append(obj)
    return animationKeys, "Animation Keys found"

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
    return emptyGroups, "is an empty group"

def layers(list, SLMesh):
    layers = cmds.ls(type="displayLayer")
    layers.remove("defaultLayer")
    if layers:
        return layers, "is a display layer"
    else:
        return [], ""

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

    return [], ""