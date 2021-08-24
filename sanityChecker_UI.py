"""
Sanity Checker

Author: Dilen Shah
Version: 1.0
"""

from PySide2 import QtCore, QtWidgets, QtGui
from shiboken2 import wrapInstance
from functools import partial

import os, sys, re
import maya.cmds as cmds
import maya.OpenMayaUI as omui
import maya.api.OpenMaya as om
import sanityChecker
reload(sanityChecker)

__location__ =  os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

def getMainWindow():
    main_window_ptr = omui.MQtUtil.mainWindow()
    mainWindow = wrapInstance(long(main_window_ptr), QtWidgets.QWidget)
    return mainWindow

class Highlighter(QtGui.QSyntaxHighlighter):
    def __init__(self, parent):
        super(Highlighter, self).__init__(parent)
        self.successFormat = QtGui.QTextCharFormat()
        self.successFormat.setForeground(QtCore.Qt.green)
        self.warningFormat = QtGui.QTextCharFormat()
        self.warningFormat.setForeground(QtCore.Qt.yellow)
        self.errorFormat = QtGui.QTextCharFormat()
        self.errorFormat.setForeground(QtCore.Qt.red)
        self.textFormat =  QtGui.QTextCharFormat()
        self.textFormat.setForeground(QtCore.Qt.white)

    def highlightBlock(self, text):
        # uncomment this line for Python2
        if text.endswith('SUCCESS'):
            self.setFormat(0, len(text), self.successFormat)
        elif text.endswith('FAILED') or text.startswith('ERROR'):
            self.setFormat(0, len(text), self.errorFormat)
        elif text.endswith('WARNING'):
            self.setFormat(0, len(text), self.warningFormat)
        elif text.find('---->'):
            self.setFormat(0, len(text), self.textFormat)

class SanityCheckerUI(QtWidgets.QMainWindow):

    qmw_instance = None

    @classmethod
    def show_UI(cls):
        if not cls.qmw_instance:
            cls.qmw_instance = SanityCheckerUI()

        if cls.qmw_instance.isHidden():
            cls.qmw_instance.show()
        else:
            cls.qmw_instance.raise_()
            cls.qmw_instance.activateWindow()

    def __init__(self, parent=getMainWindow()):
        super(SanityCheckerUI, self).__init__(
            parent, QtCore.Qt.WindowStaysOnTopHint)

        # Creates object, Title Name and Adds a QtWidget as our central widget/Main Layout
        self.setObjectName("sanityCheckerUI")
        self.setWindowTitle("Sanity Checker")
        mainLayout = QtWidgets.QWidget(self)
        self.setCentralWidget(mainLayout)
        self.setStyleSheet(open("%s/style.qss" % __location__, "r").read())                 
             
        # Adding a Vertical layout to add column and run button
        rows = QtWidgets.QVBoxLayout(mainLayout)
             
        # Adding a Horizontal layout to divide the UI in two columns
        columns = QtWidgets.QHBoxLayout()

        groupBox = QtWidgets.QGroupBox()
        groupBox.setLayout(columns)
        
        # Adding scroll area
        scroll = QtWidgets.QScrollArea()
        scroll.setWidget(groupBox)
        scroll.setWidgetResizable(True)
        
        rows.addWidget(scroll)
        
        # Creating 2 vertical layout for the sanity checks and one for the report
        self.report = QtWidgets.QVBoxLayout()
        self.checks = QtWidgets.QVBoxLayout()

        columns.addLayout(self.checks)
        columns.addLayout(self.report)

        # Adding UI ELEMENTS FOR CHECKS
        selectedModelVLayout = QtWidgets.QHBoxLayout()
        self.checks.addLayout(selectedModelVLayout)

        selectedModelLabel = QtWidgets.QLabel("Top Node")
        selectedModelLabel.setMaximumWidth(60)

        self.selectedTopNode_UI = QtWidgets.QLineEdit("")
        self.selectedTopNode_UI.setMaximumWidth(200)

        self.selectedModelNodeButton = QtWidgets.QPushButton("Select")
        self.selectedModelNodeButton.setMaximumWidth(60)
        self.selectedModelNodeButton.clicked.connect(self.setTopNode)

        selectedModelVLayout.addWidget(selectedModelLabel)
        selectedModelVLayout.addWidget(self.selectedTopNode_UI)
        selectedModelVLayout.addWidget(self.selectedModelNodeButton)

        # Adding UI elements to the report
        self.reportBoxLayout = QtWidgets.QHBoxLayout()
        reportLabel = QtWidgets.QLabel("Report:")

        self.reportBoxLayout.addWidget(reportLabel)
        self.report.addLayout(self.reportBoxLayout)

        self.reportOutputUI = QtWidgets.QPlainTextEdit()
        self.highlighter = Highlighter(self.reportOutputUI.document())

        self.reportOutputUI.setMinimumWidth(300)
        self.report.addWidget(self.reportOutputUI)

        self.clearButton = QtWidgets.QPushButton("Clear")
        self.clearButton.setMaximumWidth(150)
        self.clearButton.clicked.connect(partial(self.reportOutputUI.clear))

        self.reportBoxLayout.addWidget(self.clearButton)

        # Adding the stretch element to the checks UI to get everything at the top
        self.resize(600, 500)
        self.list = [
            'triangles_topology_0_0',
            'ngons_topology_0_0',
            'zeroAreaFaces_topology_0_0',
            'zeroLengthEdges_topology_0_0',
            'openEdges_topology_0_0',
            'floatingVertices_topology_0_0',
            'poles_topology_0_0',
            'hardEdges_topology_0_0',
            'lamina_topology_0_0',
            'nonManifoldEdges_topology_0_0',
            'starlike_topology_0_0',

            'uncenteredPivots_model_0_1',
            'lockedChannels_model_0_1',
            'normals_model_0_1',
            'unfrozenTransforms_model_0_1',
            'attributes_model_0_1',
            'smoothMesh_model_0_1',
            'intermediateObjects_model_0_0',
            'vcolor_model_0_1',
            'multipleShapes_model_0_1', 
            'negativeScale_model_0_1',
            'hierarchy_model_0_0',
            'shaders_model_0_1',
            'history_model_0_1',

            'currentUv_uv_0_0',
            'multiUv_uv_0_0',
            'missingUv_uv_0_0',
            'uvRange_uv_0_0',
            'crossBorder_uv_0_0',
            'selfPenetratingUv_uv_0_0',

            'trailingNumbers_naming_0_0',
            'duplicatedNames_naming_0_0',
            'shapeNames_naming_0_1',
            'namespaces_naming_0_1',

            'textureSize_textures_0_0',
            'imageBrightness_textures_0_0',
            'textureNames_textures_0_0',

            'colorSet_lookdev_0_1',
            'unusedShaders_lookdev_0_1',
            'standardSurface_lookdev_0_1',

            'cleanUp_scene_0_1',
            'referenceCheck_scene_0_0',
            'unitCheck_scene_0_0',
            'animationKeys_scene_0_1',
            'emptyGroups_scene_0_0',
            'layers_scene_0_1',

            'intersections_intersections_0_0',
        ]

        allCategories = []

        for obj in self.list:
            number = obj.split('_')
            allCategories.append(number[1])

        category = ['topology', 'model', 'uv', 'naming', 'textures', 'lookdev', 'scene', 'intersections']
        self.SLMesh = om.MSelectionList()

        self.categoryLayout = {}
        self.categoryWidget = {}
        self.categoryButton = {}
        self.categoryHeader = {}
        self.categoryCheckBox = {}
        self.command = {}
        self.commandWidget = {}
        self.commandLayout = {}
        self.commandLabel = {}
        self.commandCheckBox = {}
        self.errorNodesButton = {}
        self.errorNodes = {}
        self.commandFixButton = {}
        self.commandFix = {}
        self.commandRunButton = {}

        # Create the Categories section!!
        for obj in category:
            self.categoryWidget[obj] = QtWidgets.QWidget()
            self.categoryLayout[obj] = QtWidgets.QVBoxLayout()
            self.categoryHeader[obj] = QtWidgets.QHBoxLayout()
            self.categoryButton[obj] = QtWidgets.QPushButton(obj)
            self.categoryButton[obj].setMinimumWidth(200)
            self.categoryCheckBox[obj] = QtWidgets.QCheckBox()
            self.categoryCheckBox[obj].clicked.connect(partial(self.checkCategory, obj))
            self.categoryCheckBox[obj].setMaximumWidth(30)
            self.categoryWidget[obj].setVisible(False)
            self.categoryButton[obj].setStyleSheet("background-color: grey; \
                                                    text-transform: uppercase; \
                                                    color: #000000; \
                                                    font-size: 18px;")
            self.categoryButton[obj].clicked.connect(partial(self.toggleUI, obj))
            self.categoryHeader[obj].addWidget(self.categoryButton[obj])
            self.categoryHeader[obj].addWidget(self.categoryCheckBox[obj])
            self.categoryWidget[obj].setLayout(self.categoryLayout[obj])
            self.checks.addLayout(self.categoryHeader[obj])
            self.checks.addWidget(self.categoryWidget[obj])

        # Creates the buttons with their settings.
        for obj in self.list:
            new = obj.split('_')
            name = new[0]
            category = new[1]
            check = int(new[2])
            fix = int(new[3])
            
            newName = re.findall('[A-Z][^A-Z]*', name)
            if newName:
                newName = "%s %s" % (name.replace(newName[0], "").capitalize(), newName[0])
            else:
                newName = name.capitalize()

            self.commandWidget[name] = QtWidgets.QWidget()
            self.commandWidget[name].setMaximumHeight(40)
            self.commandLayout[name] = QtWidgets.QHBoxLayout()

            self.categoryLayout[category].addWidget(self.commandWidget[name])
            self.commandWidget[name].setLayout(self.commandLayout[name])

            self.commandLayout[name].setSpacing(4)
            self.commandLayout[name].setContentsMargins(0, 0, 0, 0)
            self.commandWidget[name].setStyleSheet("padding: 0px; margin: 0px;")
            self.command[name] = name
            self.commandLabel[name] = QtWidgets.QLabel(newName)
            self.commandLabel[name].setStyleSheet(" color: #ffffff; \
                                                    font-size: 13px;")
            self.commandLabel[name].setMinimumWidth(120)
            self.commandCheckBox[name] = QtWidgets.QCheckBox()

            self.commandCheckBox[name].setChecked(check)
            self.commandCheckBox[name].setMaximumWidth(20)

            self.commandRunButton[name] = QtWidgets.QPushButton("Run")
            self.commandRunButton[name].setMaximumWidth(30)

            self.commandRunButton[name].clicked.connect(
                partial(self.commandToRun, [name]))

            self.errorNodesButton[name] = QtWidgets.QPushButton("Select Error Nodes")
            self.errorNodesButton[name].setEnabled(False)
            self.errorNodesButton[name].setMaximumWidth(150)

            self.commandLayout[name].addWidget(self.commandLabel[name])
            self.commandLayout[name].addWidget(self.commandCheckBox[name])
            self.commandLayout[name].addWidget(self.commandRunButton[name])
            self.commandLayout[name].addWidget(self.errorNodesButton[name])

            
            if fix == 1:
                self.commandFix[name] = ""
                self.commandFixButton[name] = QtWidgets.QPushButton("Fix")
                self.commandFixButton[name].setEnabled(False)
                self.commandFixButton[name].setMaximumWidth(40)
                # self.commandRunButton[name].clicked.connect(
                #     partial(self.commandToRun, [eval(name + "_fix")]))
                self.commandLayout[name].addWidget(self.commandFixButton[name])
            else:
                self.commandLayout[name].addWidget(QtWidgets.QLabel(" "))


        self.checks.addStretch()

        self.checkButtonsLayout = QtWidgets.QHBoxLayout()
        self.checks.addLayout(self.checkButtonsLayout)

        self.checkRunButton = QtWidgets.QPushButton("Run All Checked")
        self.checkRunButton.clicked.connect(self.sanityCheck)
        self.checkRunButton.setStyleSheet("font-size:14px;")

        rows.addWidget(self.checkRunButton)

    # Definitions to manipulate the UI
    def setTopNode(self):
        sel = cmds.ls(selection=True)
        self.selectedTopNode_UI.setText(sel[0])

    # Checks the state of a given checkbox
    def checkState(self, name):
        return self.commandCheckBox[name].checkState()

    # Sets all checkboxes to True

    def checkAll(self):
        for obj in self.list:
            new = obj.split('_')
            name = new[0]
            self.commandCheckBox[name].setChecked(True)

    def toggleUI(self, obj):
        state = self.categoryWidget[obj].isVisible()
        if state:
            self.categoryCheckBox[obj].setText(u'\u21B5'.encode('utf-8'))
            self.categoryWidget[obj].setVisible(not state)
            self.adjustSize()
        else:
            self.categoryCheckBox[obj].setText(u'\u2193'.encode('utf-8'))
            self.categoryWidget[obj].setVisible(not state)

    # Sets all checkboxes to False
    def uncheckAll(self):
        for obj in self.list:
            new = obj.split('_')
            name = new[0]
            self.commandCheckBox[name].setChecked(False)

    # Sets the checkbox to the oppositve of current state
    def invertCheck(self):
        for obj in self.list:
            new = obj.split('_')
            name = new[0]
            self.commandCheckBox[name].setChecked(
                not self.commandCheckBox[name].isChecked())

    def checkCategory(self, category):

        uncheckedCategoryButtons = []
        categoryButtons = []

        for obj in self.list:
            new = obj.split('_')
            name = new[0]
            cat = new[1]
            if cat == category:
                categoryButtons.append(name)
                if self.commandCheckBox[name].isChecked():
                    uncheckedCategoryButtons.append(name)

        for obj in categoryButtons:
            if len(uncheckedCategoryButtons) == len(categoryButtons):
                self.commandCheckBox[obj].setChecked(False)
            else:
                self.commandCheckBox[obj].setChecked(True)

    # Filter Nodes
    def filterNodes(self):
        nodes = []
        self.SLMesh.clear()
        allUsuableNodes = []
        allNodes = cmds.ls(transforms=True, l=True)
        for obj in allNodes:
            if not obj in {'front', 'persp', 'top', 'side'}:
                allUsuableNodes.append(obj)

        selection = cmds.ls(sl=True, l=True)
        topNode = self.selectedTopNode_UI.text()
        if len(selection) > 0:
            nodes = selection
        elif self.selectedTopNode_UI.text() == "":
            nodes = allUsuableNodes
        else:
            if cmds.objExists(topNode):
                nodes = cmds.listRelatives(
                    topNode, allDescendents=True, typ="transform", fullPath=True)
                if not nodes:
                    nodes = topNode
                nodes.append(topNode)
            else:
                response = "Object in Top Node doesn't exists\n"
                self.reportOutputUI.clear()
                self.reportOutputUI.insertPlainText(response)
        for node in nodes:
            shapes = cmds.listRelatives(node, shapes=True, typ="mesh", fullPath=True)
            if shapes:
                self.SLMesh.add(node)
        return nodes

    def commandToRun(self, commands):
        # Run FilterNodes
        nodes = self.filterNodes()
        self.reportOutputUI.clear()
        if len(nodes) == 0:
            self.reportOutputUI.insertPlainText("ERROR - No nodes to check\n")
        else:
            for command in commands:
                # For Each node in filterNodes, run command.
                self.errorNodes[command] = getattr(sanityChecker, command)(nodes, self.SLMesh)
                # Return error nodes
                if self.errorNodes[command]:
                    if command in ["triangles", "ngons", "intersections"]:
                        self.reportOutputUI.insertPlainText(command + " -- WARNING\n")
                        for obj in self.errorNodes[command]:
                            self.reportOutputUI.insertPlainText("    ---->    " + obj + "\n")
                        self.reportOutputUI.insertPlainText("\n")
                    
                        self.errorNodesButton[command].setEnabled(True)
                        self.errorNodesButton[command].clicked.connect(partial(self.selectErrorNodes, self.errorNodes[command]))
                        self.commandLabel[command].setStyleSheet("  background-color: #FAD02C; \
                                                                    font-size:12px; \
                                                                    color: #000000")

                    else:
                        self.reportOutputUI.insertPlainText(command + " -- FAILED\n")
                        for obj in self.errorNodes[command]:
                            self.reportOutputUI.insertPlainText("    ---->    " + obj + "\n")
                        self.reportOutputUI.insertPlainText("\n")

                        self.errorNodesButton[command].setEnabled(True)
                        self.errorNodesButton[command].clicked.connect(
                            partial(self.selectErrorNodes, self.errorNodes[command]))

                        if self.commandFix.has_key(command):
                            self.commandFixButton[command].setEnabled(True)
                            self.commandFixButton[command].clicked.connect(
                            partial(self.runFix, self.errorNodes[command], self.SLMesh, command))


                        self.commandLabel[command].setStyleSheet("  background-color: #664444; \
                                                                    font-size:12px")
                else:
                    self.commandLabel[command].setStyleSheet(
                        "background-color: #446644; font-size:12px")
                    self.reportOutputUI.insertPlainText(command + " -- SUCCESS\n\n")
                    self.errorNodesButton[command].setEnabled(False)

    # Write the report to report UI.
    def sanityCheck(self):
        self.reportOutputUI.clear()
        checkedCommands = []
        for obj in self.list:
            new = obj.split('_')
            name = new[0]
            if self.commandCheckBox[name].isChecked():
                checkedCommands.append(name)
            else:
                self.commandLabel[name].setStyleSheet(
                    "background-color: none;")
        if len(checkedCommands) == 0:
            self.reportOutputUI.insertPlainText("ERROR - Nothing checked, You have to select something\n")
        else:
            self.commandToRun(checkedCommands)

    def selectErrorNodes(self, list):
        cmds.select(list)

    # this definition needs to run the Fix
    def runFix(self, nodes, SLMesh, command):
        fixCommand = "%s_fix" % command
        fixStatus = getattr(sanityChecker, fixCommand)(nodes, SLMesh)
        if fixStatus == "fixed":
            self.commandLabel[command].setStyleSheet(
                        "background-color: #446644; font-size:12px")
            self.reportOutputUI.clear()
            self.reportOutputUI.insertPlainText(command + " -- SUCCESS\n\n")
            self.errorNodesButton[command].setEnabled(False)
        else:
            self.commandLabel[command].setStyleSheet(
                        "background-color: #664444; font-size:12px")
            self.reportOutputUI.clear()
            self.reportOutputUI.insertPlainText(command + " -- FAILED\n\n")
            self.errorNodesButton[command].setEnabled(False)
