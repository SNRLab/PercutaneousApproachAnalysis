import os
import unittest
from __main__ import vtk, qt, ctk, slicer
import time
import math
import string


class PercutaneousApproachAnalysis:
  def __init__(self, parent):
    parent.title = "PercutaneousApproachAnalysis" # TODO make this more human readable by adding spaces
    parent.categories = ["IGT"]
    parent.dependencies = []
    parent.contributors = ["Atsushi Yamada (Shiga University of Medical Science),Koichiro Murakami (Shiga University of Medical Science, Japan, SPL), Laurent Chauvin (SPL), Junichi Tokuda (SPL)"] 
    # parent.helpText = string.Template("""
    # The Percutaneous Approach Analysis is used to calculate and visualize the accessibility to liver tumor with a percutaneous approach.
    # See <a href=http://wiki.slicer.org/slicerWiki/index.php/Documentation/Nightly/Extensions/PercutaneousApproachAnalysis>the online documentation</a> to know how to use in detail.
    # """).substitute({ 'a':parent.slicerWikiUrl, 'b':slicer.app.majorVersion, 'c':slicer.app.minorVersion })
    parent.acknowledgementText = """    
    This work is supported by Bio-Medical Innovation Center and Department of Surgery, Shiga University of Medical Science in Japan. 
    This work is also supported in part by the NIH (R01CA111288, P01CA067165, P41RR019703, P41EB015898, R01CA124377, R01CA138586, R42CA137886).
    """
    self.parent = parent

    # Add this test to the SelfTest module's list for discovery when the module
    # is created.  Since this module may be discovered before SelfTests itself,
    # create the list if it doesn't already exist.
    try:
      slicer.selfTests
    except AttributeError:
      slicer.selfTests = {}
    slicer.selfTests['PercutaneousApproachAnalysis'] = self.runTest

  def runTest(self):
    tester = PercutaneousApproachAnalysisTest()
    tester.runTest()

#
# qPercutaneousApproachAnalysisWidget
#

class PercutaneousApproachAnalysisWidget:
  def __init__(self, parent = None):
    if not parent:
      self.parent = slicer.qMRMLWidget()
      self.parent.setLayout(qt.QVBoxLayout())
      self.parent.setMRMLScene(slicer.mrmlScene)
    else:
      self.parent = parent
    self.layout = self.parent.layout()
    if not parent:
      self.setup()
      self.parent.show()
    self.logic = PercutaneousApproachAnalysisLogic()

  def setup(self):
    # Instantiate and connect widgets ...

    import numpy

    #
    # Reload and Test area
    #
    reloadCollapsibleButton = ctk.ctkCollapsibleButton()
    reloadCollapsibleButton.text = "Reload && Test"
    reloadCollapsibleButton.collapsed = True
    self.layout.addWidget(reloadCollapsibleButton)
    reloadFormLayout = qt.QFormLayout(reloadCollapsibleButton)

    # reload button
    # (use this during development, but remove it when delivering
    #  your module to users)
    self.reloadButton = qt.QPushButton("Reload")
    self.reloadButton.toolTip = "Reload this module."
    self.reloadButton.name = "PercutaneousApproachAnalysis Reload"
    reloadFormLayout.addWidget(self.reloadButton)
    self.reloadButton.connect('clicked()', self.onReload)

    # reload and test button
    # (use this during development, but remove it when delivering
    #  your module to users)
    self.reloadAndTestButton = qt.QPushButton("Reload and Test")
    self.reloadAndTestButton.toolTip = "Reload this module and then run the self tests."
    reloadFormLayout.addWidget(self.reloadAndTestButton)
    self.reloadAndTestButton.connect('clicked()', self.onReloadAndTest)

    #
    # Parameters Area
    #
    parametersCollapsibleButton = ctk.ctkCollapsibleButton()
    parametersCollapsibleButton.text = "Parameters"
    parametersCollapsibleButton.collapsed = False
    self.parametersList = parametersCollapsibleButton   
    self.layout.addWidget(parametersCollapsibleButton)

    # Layout within the collapsible button
    parametersFormLayout = qt.QFormLayout(parametersCollapsibleButton)

    #
    # Target point (vtkMRMLMarkupsFiducialNode)
    #
    self.targetSelector = slicer.qMRMLNodeComboBox()
    self.targetSelector.nodeTypes = ( ("vtkMRMLMarkupsFiducialNode"), "" )
    self.targetSelector.addEnabled = True
    self.targetSelector.removeEnabled = True
    self.targetSelector.noneEnabled = True
    self.targetSelector.showHidden = False
    self.targetSelector.showChildNodeTypes = False
    self.targetSelector.setMRMLScene( slicer.mrmlScene )
    self.targetSelector.setToolTip( "Pick up the target point" )
    parametersFormLayout.addRow("Target Point: ", self.targetSelector)

    #
    # Entry point list (vtkMRMLMarkupsFiducialNode)
    #
    self.entryPointsSelector = slicer.qMRMLNodeComboBox()
    self.entryPointsSelector.nodeTypes = ( ("vtkMRMLMarkupsFiducialNode"), "" )
    self.entryPointsSelector.addEnabled = True
    self.entryPointsSelector.removeEnabled = True
    self.entryPointsSelector.noneEnabled = True
    self.entryPointsSelector.showHidden = False
    self.entryPointsSelector.showChildNodeTypes = False
    self.entryPointsSelector.setMRMLScene( slicer.mrmlScene )
    parametersFormLayout.addRow("Output Fiducial List: ", self.entryPointsSelector)

    #
    # Skin model (vtkMRMLModelNode)
    #
    self.skinModelSelector = slicer.qMRMLNodeComboBox()
    self.skinModelSelector.nodeTypes = ( ("vtkMRMLModelNode"), "" )
    self.skinModelSelector.addEnabled = False
    self.skinModelSelector.removeEnabled = False
    self.skinModelSelector.noneEnabled =  True
    self.skinModelSelector.showHidden = False
    self.skinModelSelector.showChildNodeTypes = False
    self.skinModelSelector.setMRMLScene( slicer.mrmlScene )
    self.skinModelSelector.setToolTip( "Pick the skin model to the algorithm." )
    parametersFormLayout.addRow("Skin Model: ", self.skinModelSelector)

    #
    # Skin model opacity slider
    #
    self.skinModelOpacitySlider = ctk.ctkSliderWidget()
    self.skinModelOpacitySlider.decimals = 0
    self.skinModelOpacitySlider.maximum = 1000
    self.skinModelOpacitySlider.minimum = 0
    self.skinModelOpacitySlider.value = 1000
    self.skinModelOpacitySlider.enabled = True
    parametersFormLayout.addRow("      Opacity:", self.skinModelOpacitySlider)

    #
    # Obstacle model (vtkMRMLModelNode)
    #
    self.obstacleModelSelector = slicer.qMRMLNodeComboBox()
    self.obstacleModelSelector.nodeTypes = ( ("vtkMRMLModelNode"), "" )
    self.obstacleModelSelector.addEnabled = False
    self.obstacleModelSelector.removeEnabled = False
    self.obstacleModelSelector.noneEnabled =  True
    self.obstacleModelSelector.showHidden = False
    self.obstacleModelSelector.showChildNodeTypes = False
    self.obstacleModelSelector.setMRMLScene( slicer.mrmlScene )
    self.obstacleModelSelector.setToolTip( "Pick the obstacle model to the algorithm." )
    parametersFormLayout.addRow("Obstacle Model: ", self.obstacleModelSelector)

    #
    # Obstacle model opacity slider
    #
    self.obstacleModelOpacitySlider = ctk.ctkSliderWidget()
    self.obstacleModelOpacitySlider.decimals = 0
    self.obstacleModelOpacitySlider.maximum = 1000
    self.obstacleModelOpacitySlider.minimum = 0
    self.obstacleModelOpacitySlider.value = 1000
    self.obstacleModelOpacitySlider.enabled = True
    parametersFormLayout.addRow("      Opacity:", self.obstacleModelOpacitySlider)
   
    #
    # Apply Button
    #
    self.applyButton = qt.QPushButton("Start Analysis")
    self.applyButton.toolTip = "Run the algorithm."
    self.applyButton.enabled = False    
    parametersFormLayout.addRow(self.applyButton)

    # connections
    self.applyButton.connect('clicked(bool)', self.onApplyButton)
    self.targetSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
    self.obstacleModelSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
    self.skinModelSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
    self.entryPointsSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)

    self.skinModelOpacitySlider.connect('valueChanged(double)', self.skinModelOpacitySliderValueChanged)
    self.obstacleModelOpacitySlider.connect('valueChanged(double)', self.obstacleModelOpacitySliderValueChanged)

    #
    # Outcomes Area
    #
    outcomesCollapsibleButton = ctk.ctkCollapsibleButton()
    outcomesCollapsibleButton.text = "Outcomes"
    outcomesCollapsibleButton.collapsed = True
    self.layout.addWidget(outcomesCollapsibleButton)

    self.outcomesList = outcomesCollapsibleButton

    # Layout within the dummy collapsible button
    outcomesFormLayout = qt.QFormLayout(outcomesCollapsibleButton)

    #
    # Check box for displaying color map
    #
    self.colorMapCheckBox = ctk.ctkCheckBox()
    self.colorMapCheckBox.text = "Color Mapped Skin"
    self.colorMapCheckBox.enabled = False
    self.colorMapCheckBox.checked = True
    outcomesFormLayout.addRow(self.colorMapCheckBox)

    # Accessibility score results
    self.accessibilityScore = qt.QLineEdit()
    self.accessibilityScore.toolTip = "Accessibility Score"
    self.accessibilityScore.enabled = True
    self.accessibilityScore.maximumWidth = 70
    self.accessibilityScore.setReadOnly(True)
    self.accessibilityScore.maxLength = 8
    outcomesFormLayout.addRow("      Accessibility Score:",self.accessibilityScore)
    
    #
    # Opacity slider
    #
    self.coloredSkinModelOpacitySlider = ctk.ctkSliderWidget()
    self.coloredSkinModelOpacitySlider.decimals = 0
    self.coloredSkinModelOpacitySlider.maximum = 1000
    self.coloredSkinModelOpacitySlider.minimum = 0
    self.coloredSkinModelOpacitySlider.value = 1000
    self.coloredSkinModelOpacitySlider.enabled = False
    outcomesFormLayout.addRow("      Opacity:", self.coloredSkinModelOpacitySlider)
    self.coloredSkinModelOpacitySlider.connect('valueChanged(double)', self.skinModelOpacitySliderValueChanged)

    #
    # Minimum distance point (vtkMRMLMarkupsFiducialNode)
    #
    self.minimumDistancePoint = slicer.qMRMLNodeComboBox()
    self.minimumDistancePoint.nodeTypes = ( ("vtkMRMLMarkupsFiducialNode"), "" )
    self.minimumDistancePoint.addEnabled = True
    self.minimumDistancePoint.removeEnabled = True
    self.minimumDistancePoint.noneEnabled = True
    self.minimumDistancePoint.showHidden = False
    self.minimumDistancePoint.showChildNodeTypes = False
    self.minimumDistancePoint.setMRMLScene( slicer.mrmlScene )
    self.minimumDistancePoint.setToolTip( "Display the minimum distance point" )
    self.minimumDistancePoint.baseName = "PAA-MinimumDistance"

    #
    # Check box for displaying all paths
    #
    self.allPathsCheckBox = ctk.ctkCheckBox()
    self.allPathsCheckBox.text = "All Paths (Yellow)"
    self.allPathsCheckBox.enabled = False
    self.allPathsCheckBox.checked = True
    outcomesFormLayout.addRow(self.allPathsCheckBox)

    #
    # Numbers of approchable polygons
    #
    self.numbersOfAllpathsSpinBox = qt.QLineEdit()
    self.numbersOfAllpathsSpinBox.enabled = True
    self.numbersOfAllpathsSpinBox.maximumWidth = 70
    self.numbersOfAllpathsSpinBox.setReadOnly(True)
    self.accessibilityScore.maxLength = 10
    outcomesFormLayout.addRow("      Number of All Paths: ", self.numbersOfAllpathsSpinBox)

    #
    # Opacity slider
    #
    self.allPathsOpacitySlider = ctk.ctkSliderWidget()
    self.allPathsOpacitySlider.decimals = 0
    self.allPathsOpacitySlider.maximum = 1000
    self.allPathsOpacitySlider.minimum = 0
    self.allPathsOpacitySlider.value = 10
    self.allPathsOpacitySlider.enabled = False
    outcomesFormLayout.addRow("      Opacity:", self.allPathsOpacitySlider)

    #
    # Check box for displaying each path
    #
    self.maximumLengthPathCheckBox = ctk.ctkCheckBox()
    self.maximumLengthPathCheckBox.text = "The Longest Path (Green)"
    outcomesFormLayout.addRow(self.maximumLengthPathCheckBox)

    #
    # Maximum Length
    #
    self.maximumLengthEdit = qt.QLineEdit()
    self.maximumLengthEdit.enabled = True
    self.maximumLengthEdit.maximumWidth = 70
    self.maximumLengthEdit.setReadOnly(True)
    self.maximumLengthEdit.maxLength = 8    

    #
    # Maximum Length Path
    #
    self.maximumLengthPathEdit = qt.QLineEdit()
    self.maximumLengthPathEdit.enabled = True
    self.maximumLengthPathEdit.maximumWidth = 70
    self.maximumLengthPathEdit.setReadOnly(True)
    self.maximumLengthPathEdit.maxLength = 8    

    outcomesFormLayout.addRow("      Path (No.): ", self.maximumLengthPathEdit)
    outcomesFormLayout.addRow("      Length (mm): ", self.maximumLengthEdit)

    #
    # Check box for displaying each path
    #
    self.minimumLengthPathCheckBox = ctk.ctkCheckBox()
    self.minimumLengthPathCheckBox.text = "The Shortest Path (Blue)"
    outcomesFormLayout.addRow(self.minimumLengthPathCheckBox)

    #
    # Minimum Length
    #
    self.minimumLengthEdit = qt.QLineEdit()
    self.minimumLengthEdit.enabled = True
    self.minimumLengthEdit.maximumWidth = 70
    self.minimumLengthEdit.setReadOnly(True)
    self.minimumLengthEdit.maxLength = 8    

    #
    # Minimum Length Path
    #
    self.minimumLengthPathEdit = qt.QLineEdit()
    self.minimumLengthPathEdit.enabled = True
    self.minimumLengthPathEdit.maximumWidth = 70
    self.minimumLengthPathEdit.setReadOnly(True)
    self.minimumLengthPathEdit.maxLength = 8    
    
    outcomesFormLayout.addRow("      Path (No.): ", self.minimumLengthPathEdit)
    outcomesFormLayout.addRow("      Length (mm): ", self.minimumLengthEdit)

    #
    # Check box for displaying each path
    #
    self.pathCandidateCheckBox = ctk.ctkCheckBox()
    self.pathCandidateCheckBox.text = "Path Candidate (Red)"
    self.pathCandidateCheckBox.enabled = False 
    self.pathCandidateCheckBox.checked = False    
    outcomesFormLayout.addRow(self.pathCandidateCheckBox)

    # Path slider
    self.pathSlider = ctk.ctkSliderWidget()
    self.pathSlider.decimals = 0
    self.pathSlider.enabled = False
    outcomesFormLayout.addRow("      Path Candidate (No.):", self.pathSlider)

    # Point slider
    self.pointSliderLength = 5000
    self.pointSlider = ctk.ctkSliderWidget()
    self.pointSlider.decimals = 0
    self.pointSlider.maximum = self.pointSliderLength
    self.pointSlider.minimum = -self.pointSliderLength
    self.pointSlider.enabled = False
    outcomesFormLayout.addRow("      Point Candidate on the Path:", self.pointSlider)

    #
    # Length of the path
    #
    self.lengthOfPathSpinBox = qt.QLineEdit()
    self.lengthOfPathSpinBox.enabled = True
    self.lengthOfPathSpinBox.maximumWidth = 70
    self.lengthOfPathSpinBox.setReadOnly(True)
    self.lengthOfPathSpinBox.maxLength = 8
    outcomesFormLayout.addRow("      Length (mm): ", self.lengthOfPathSpinBox)

    # create point on the path
    self.createPointOnThePathButton = qt.QPushButton("Create Point on the Path")
    self.createPointOnThePathButton.enabled = False
    outcomesFormLayout.addRow("      Point on the Path:", self.createPointOnThePathButton)

    # connections
    self.pathCandidateCheckBox.connect("clicked(bool)", self.onCheckPathCandidate)
    self.allPathsCheckBox.connect("clicked(bool)", self.onCheckAllPaths)
    self.colorMapCheckBox.connect("clicked(bool)", self.onCheckColorMappedSkin)
    self.createPointOnThePathButton.connect('clicked(bool)', self.onCreatePointOnThePathButton)
    self.pathSlider.connect('valueChanged(double)', self.selectedPathIndexChanged)
    self.pointSlider.connect('valueChanged(double)', self.pointSliderValueChanged)
    self.allPathsOpacitySlider.connect('valueChanged(double)', self.allPathsOpacitySliderValueChanged)

    self.maximumLengthPathCheckBox.connect("clicked(bool)", self.onCheckTheLongestPath)
    self.minimumLengthPathCheckBox.connect("clicked(bool)", self.onCheckTheShortestPath)

    #
    # Cleaning Area
    #
    cleaningCollapsibleButton = ctk.ctkCollapsibleButton()
    cleaningCollapsibleButton.text = "Cleaning Outcomes"
    cleaningCollapsibleButton.collapsed = True
    self.layout.addWidget(cleaningCollapsibleButton)

    # Layout within the dummy collapsible button
    cleaningFormLayout = qt.QFormLayout(cleaningCollapsibleButton)

    self.cleaningList = cleaningCollapsibleButton

    #
    # Delete Models Button
    #
    self.deleteModelsButton = qt.QPushButton("Delete the Created Paths")
    self.deleteModelsButton.toolTip = "Delete Created Paths"
    self.deleteModelsButton.enabled = False    
    cleaningFormLayout.addWidget(self.deleteModelsButton)

    self.deleteModelsButton.connect('clicked()', self.onDeleteModelsButton)

    # Add vertical spacer
    self.layout.addStretch(1)

    self.selectedPathIndex = 0
    self.positionAlongSelectedPath = 0

    # model variables
    self.allPathsModel = None
    self.selectedPathModel = None
    self.selectedPathTipModel = None
    self.extendedPathModel = None
    self.extendedPathTipModel = None
    self.longestPathModel = None
    self.longestPathTipModel = None
    self.shortestPathModel = None
    self.shortestPathTipModel = None
    self.plannedEntryPointModels = []

    # line colors
    self.yellow = [1, 1, 0]
    self.red = [1, 0, 0]
    self.green = [0, 1, 0]
    self.blue = [0, 0, 1]

  def cleanup(self):
    pass

  def selectedPathIndexChanged(self,newValue):
    
    self.selectedPathIndex = int(newValue)
    onePath = self.logic.makeSinglePath(self.selectedPathIndex)
    self.logic.updatePathModel(self.selectedPathModel, onePath)
    self.logic.setSpherePositionAlongPath(self.selectedPathTipModel, self.selectedPathIndex, 0)

    self.pointSliderValueChanged(self.pointSlider.value)

  def pointSliderValueChanged(self,newValue):
    self.positionAlongSelectedPath = newValue / self.pointSliderLength

    self.virtualMarkerPosition = self.logic.setSpherePositionAlongPath(self.extendedPathTipModel, self.selectedPathIndex, self.positionAlongSelectedPath)
    virtualPath = self.logic.makeVirtualPath(self.selectedPathIndex, self.virtualMarkerPosition)
    self.logic.updatePathModel(self.extendedPathModel, virtualPath)

    #import numpy as np
    #targetPointPosition = self.logic.paths[self.selectedPathIndex][0]
    #skinPointPosition = self.virtualMarkerPosition
    #virtualPathLength = np.linalg.norm(skinPointPosition - targetPointPosition)
    #self.lengthOfPathSpinBox.text = round(virtualPathLength,1)
    self.lengthOfPathSpinBox.text = round(PercutaneousApproachAnalysisLogic.pathLength(virtualPath), 1)

  def skinModelOpacitySliderValueChanged(self,newValue):
    if not self.skinModelSelector.currentNode():
      return
    skinModel = self.skinModelSelector.currentNode()
    modelDisplay = skinModel.GetDisplayNode()
    modelDisplay.SetOpacity(newValue/1000.0)
    self.skinModelOpacitySlider.value = newValue
    self.coloredSkinModelOpacitySlider.value = newValue

  def obstacleModelOpacitySliderValueChanged(self,newValue):
    if not self.obstacleModelSelector.currentNode():
      return
    obstacleModel = self.obstacleModelSelector.currentNode()
    modelDisplay = obstacleModel.GetDisplayNode()
    modelDisplay.SetOpacity(newValue/1000.0)
        
  def allPathsOpacitySliderValueChanged(self,newValue):
    self.allPathsMode.GetDisplayNode().SetOpacity(newValue/1000.0)

  def onSelect(self):
    if (self.targetSelector.currentNode() != None) and (self.obstacleModelSelector.currentNode() != None) and (self.skinModelSelector.currentNode() != None):
      self.applyButton.enabled = True

    self.skinModelOpacitySliderValueChanged(self.skinModelOpacitySlider.value)
    self.obstacleModelOpacitySliderValueChanged(self.obstacleModelOpacitySlider.value)

  def onCreatePointOnThePathButton(self):
    entryPointsNode = self.entryPointsSelector.currentNode()

    n = entryPointsNode.AddFiducial(self.virtualMarkerPosition[0], self.virtualMarkerPosition[1], self.virtualMarkerPosition[2])
    entryPointsNode.SetNthFiducialLabel(n, "SkinEntryPoint")
    entryPointsNode.SetNthFiducialVisibility(n,1)

    plannedEntryPointModel = self.logic.createSphereModel("plannedEntryPoint", self.red)
    PercutaneousApproachAnalysisLogic.setSpherePosition(plannedEntryPointModel, self.virtualMarkerPosition)
    self.plannedEntryPointModels.append(plannedEntryPointModel)

  def onCheckAllPaths(self):
    visible = self.allPathsCheckBox.checked
    self.allPathsModel.GetDisplayNode().SetVisibility(visible)
    self.allPathsOpacitySlider.enabled = visible

  def onCheckColorMappedSkin(self):
    skinModel = self.skinModelSelector.currentNode()
    modelDisplay = skinModel.GetDisplayNode()
    displayNode = skinModel.GetModelDisplayNode()
    #displayNode.SetActiveScalar('Normals', vtk.vtkAssignAttribute.POINT_DATA)

    if self.colorMapCheckBox.checked:
      #displayNode.SetScalarVisibility(True)

      # Need to reload the skin model after "displayNode.SetActiveScalarName("Normals")" 
      # to display color map correctly 
      #displayNode.SetActiveScalar('Colors', vtk.vtkAssignAttribute.CELL_DATA)
      displayNode.SetActiveScalar("Accessibility", vtk.vtkAssignAttribute.POINT_DATA)
      displayNode.SetScalarVisibility(True)

      self.coloredSkinModelOpacitySlider.enabled = True
    else:
      displayNode.SetScalarVisibility(False)
      self.coloredSkinModelOpacitySlider.enabled = False


  def onCheckTheLongestPath(self):
    visible = self.maximumLengthPathCheckBox.checked
    self.longestPathModel.GetDisplayNode().SetVisibility(visible)
    self.longestPathTipModel.GetDisplayNode().SetVisibility(visible)

  def onCheckTheShortestPath(self):
    visible = self.minimumLengthPathCheckBox.checked
    self.shortestPathModel.GetDisplayNode().SetVisibility(visible)
    self.shortestPathTipModel.GetDisplayNode().SetVisibility(visible)

  def onCheckPathCandidate(self):
    show = self.pathCandidateCheckBox.checked
    self.selectedPathModel.GetDisplayNode().SetVisibility(show)
    self.selectedPathTipModel.GetDisplayNode().SetVisibility(show)
    self.extendedPathModel.GetDisplayNode().SetVisibility(show)
    self.extendedPathTipModel.GetDisplayNode().SetVisibility(show)
    self.pointSlider.enabled = show
    self.pathSlider.enabled = show
    self.createPointOnThePathButton.enabled = show

  def onApplyButton(self):
    print("onApplyButton() is called ")
    targetPoint = self.targetSelector.currentNode()
    obstacleModel = self.obstacleModelSelector.currentNode()
    skinModel = self.skinModelSelector.currentNode()

    # clean up work space
    self.onDeleteModelsButton()

    # create model to show all paths
    self.logic.computePaths(targetPoint, obstacleModel, skinModel)
    self.allPathsModel = PercutaneousApproachAnalysisLogic.createPathsModel(self.logic.paths, "candidatePaths", self.yellow)

    # display sphere model
    self.selectedPathTipModel = self.logic.createSphereModel("selectedPathTip", self.red, False)
    self.logic.setSpherePositionAlongPath(self.selectedPathTipModel, self.selectedPathIndex, self.positionAlongSelectedPath)
    self.extendedPathTipModel = self.logic.createSphereModel("extendedPathTip", self.red, False)
    self.logic.setSpherePositionAlongPath(self.extendedPathTipModel, self.selectedPathIndex, self.positionAlongSelectedPath)

    # make and display single path candidate
    selectedPath = self.logic.makeSinglePath(self.selectedPathIndex)
    self.selectedPathModel = self.logic.createPathsModel(selectedPath, "selectedPath", self.red,  False)
    # make and display virtual path candidate
    virtualPath = self.logic.makeSinglePath(self.selectedPathIndex)
    self.extendedPathModel = self.logic.createPathsModel(virtualPath, "extendedPath", self.red, False)
    self.lengthOfPathSpinBox.text = round(PercutaneousApproachAnalysisLogic.pathLength(virtualPath), 1)

    # make the longest path
    longestPath = self.logic.makeSinglePath(self.logic.longestPathIndex)
    self.longestPathModel = self.logic.createPathsModel(longestPath, "longestPath", self.green, False)
    self.longestPathTipModel = self.logic.createSphereModel("longestPathTip", self.green, False)
    self.logic.setSpherePositionAlongPath(self.longestPathTipModel, self.logic.longestPathIndex, 0)

    # make the shortest path
    shortestPath = self.logic.makeSinglePath(self.logic.shortestPathIndex)
    self.shortestPathModel = self.logic.createPathsModel(shortestPath, "shortestPath", self.blue, False)
    self.shortestPathTipModel = self.logic.createSphereModel("shortestPathTip", self.blue, False)
    self.logic.setSpherePositionAlongPath(self.shortestPathTipModel, self.logic.shortestPathIndex, 0)

    # update outcomes
    self.numbersOfAllpathsSpinBox.text = len(self.logic.paths)
    self.pathSlider.maximum = len(self.logic.paths) - 1
    self.allPathsCheckBox.checked = True
    self.allPathsCheckBox.enabled = True
    self.pathCandidateCheckBox.enabled = True
    self.outcomesList.collapsed = False
    self.cleaningList.collapsed = False
    self.allPathsOpacitySlider.enabled = True
    self.deleteModelsButton.enabled = True

    self.allPathsModel.GetDisplayNode().SetOpacity(0.01)
    self.skinModelOpacitySliderValueChanged(900.0)
    self.skinModelOpacitySlider.value = 900

    # calculate the length of the Path No.1 and display the length
    self.selectedPathIndexChanged(0)

    self.minimumLengthEdit.text = round(PercutaneousApproachAnalysisLogic.pathLength(self.logic.paths, self.logic.shortestPathIndex),1)
    self.minimumLengthPathEdit.text = self.logic.shortestPathIndex
    self.maximumLengthEdit.text = round(PercutaneousApproachAnalysisLogic.pathLength(self.logic.paths, self.logic.longestPathIndex),1)
    self.maximumLengthPathEdit.text = self.logic.longestPathIndex

    # make color mapped skin
    start = time.time()
    (score, minimumDistance, minimumDistancePosition) = self.logic.calcApproachScore(targetPoint, obstacleModel, skinModel)
    print(f"Accessible Area = {score}")
    print(f"Minimum Distance = {minimumDistance}")
      
    self.accessibilityScore.text = round(score,1)

    self.colorMapCheckBox.checked = True
    self.colorMapCheckBox.enabled = True
    self.onCheckColorMappedSkin()

  def onReload(self,moduleName="PercutaneousApproachAnalysis"):
    """Generic reload method for any scripted module.
    ModuleWizard will subsitute correct default moduleName.
    """
    import imp, sys, os, slicer

    widgetName = moduleName + "Widget"

    # reload the source code
    # - set source file path
    # - load the module to the global space
    filePath = eval('slicer.modules.%s.path' % moduleName.lower())
    p = os.path.dirname(filePath)
    if not sys.path.__contains__(p):
      sys.path.insert(0,p)
    fp = open(filePath, "r")
    globals()[moduleName] = imp.load_module(
        moduleName, fp, filePath, ('.py', 'r', imp.PY_SOURCE))
    fp.close()

    # rebuild the widget
    # - find and hide the existing widget
    # - create a new widget in the existing parent
    parent = slicer.util.findChildren(name='%s Reload' % moduleName)[0].parent().parent()
    for child in parent.children():
      try:
        child.hide()
      except AttributeError:
        pass
    # Remove spacer items
    item = parent.layout().itemAt(0)
    while item:
      parent.layout().removeItem(item)
      item = parent.layout().itemAt(0)

    # delete the old widget instance
    if hasattr(globals()['slicer'].modules, widgetName):
      getattr(globals()['slicer'].modules, widgetName).cleanup()

    # create new widget inside existing parent
    globals()[widgetName.lower()] = eval(
        'globals()["%s"].%s(parent)' % (moduleName, widgetName))
    globals()[widgetName.lower()].setup()
    setattr(globals()['slicer'].modules, widgetName, globals()[widgetName.lower()])

  def onReloadAndTest(self,moduleName="PercutaneousApproachAnalysis"):
    try:
      self.onReload()
      evalString = 'globals()["%s"].%sTest()' % (moduleName, moduleName)
      tester = eval(evalString)
      tester.runTest()
    except Exception as e:
      import traceback
      traceback.print_exc()
      qt.QMessageBox.warning(slicer.util.mainWindow(), 
          "Reload and Test", 'Exception!\n\n' + str(e) + "\n\nSee Python Console for Stack Trace")

  def onDeleteModelsButton(self):
    if not self.deleteModelsButton.enabled:
      return

    # reset all status
    self.deleteModelsButton.enabled = False
    self.allPathsCheckBox.checked = True
    self.allPathsCheckBox.enabled = False
    self.colorMapCheckBox.checked = False

    self.onCheckColorMappedSkin()
    self.colorMapCheckBox.checked = True
    self.colorMapCheckBox.enabled = False
    self.pathCandidateCheckBox.checked = False
    self.pathCandidateCheckBox.enabled = False
    self.pathSlider.enabled = False
    self.pointSlider.enabled = False
    self.createPointOnThePathButton.enabled = False
    self.maximumLengthPathCheckBox.checked = False
    self.maximumLengthPathCheckBox.enabled = False
    self.minimumLengthPathCheckBox.checked = False
    self.minimumLengthPathCheckBox.enabled = False
    self.allPathsOpacitySlider.enabled = False

    # delete all transforms
    self.logic.removeTransform(self.selectedPathTipModel)
    self.logic.removeTransform(self.extendedPathTipModel)
    self.logic.removeTransform(self.longestPathTipModel)
    self.logic.removeTransform(self.shortestPathTipModel)

    # delete all models
    self.logic.removeModel(self.allPathsModel)
    self.logic.removeModel(self.selectedPathModel)
    self.logic.removeModel(self.selectedPathTipModel)
    self.logic.removeModel(self.extendedPathModel)
    self.logic.removeModel(self.extendedPathTipModel)
    self.logic.removeModel(self.shortestPathModel)
    self.logic.removeModel(self.longestPathTipModel)
    self.logic.removeModel(self.longestPathModel)
    self.logic.removeModel(self.shortestPathTipModel)

#
# PercutaneousApproachAnalysisLogic
#

class PercutaneousApproachAnalysisLogic:
  """This class should implement all the actual 
  computation done by your module.  The interface 
  should be such that other python code can import
  this class and make use of the functionality without
  requiring an instance of the Widget
  """
  def __init__(self):
    # List of [targetPoint, skinPoint] pairs
    self.paths = []
    self.shortestPathIndex = -1
    self.longestPathIndex = -1

  def delayDisplay(self,message,msec=1000):
    #
    # logic version of delay display
    #
    print(message)
    self.info = qt.QDialog()
    self.infoLayout = qt.QVBoxLayout()
    self.info.setLayout(self.infoLayout)
    self.label = qt.QLabel(message,self.info)
    self.infoLayout.addWidget(self.label)
    qt.QTimer.singleShot(msec, self.info.close)
    self.info.exec_()

  def removeModel(self, model):
    scene = slicer.mrmlScene
    scene.RemoveNode(model)

  def removeTransform(self, transformedNode):
    slicer.mrmlScene.RemoveNode(transformedNode.GetParentTransformNode())

  @staticmethod
  def pathLength(paths, pathIndex=0):
    import numpy as np
    [targetPoint, skinPoint] = paths[pathIndex]
    pathLength = np.linalg.norm(targetPoint - skinPoint)
    return pathLength

  @staticmethod
  def updatePathModel(modelNode, paths):
    outputPolyData = vtk.vtkPolyData()

    points = vtk.vtkPoints()
    outputPolyData.SetPoints(points)

    lines = vtk.vtkCellArray()
    outputPolyData.SetLines(lines)

    for targetPoint, skinPoint in paths:
      pointIndex1 = points.InsertNextPoint(targetPoint)
      pointIndex2 = points.InsertNextPoint(skinPoint)
      lines.InsertNextCell(2)
      lines.InsertCellPoint(pointIndex1)
      lines.InsertCellPoint(pointIndex2)

    modelNode.SetAndObservePolyData(outputPolyData)

  @staticmethod
  def createPathsModel(paths, modelName, color, visibility=True):

    # Create model node
    model = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLModelNode", slicer.mrmlScene.GenerateUniqueName(modelName))

    # Create display node
    model.CreateDefaultDisplayNodes()
    modelDisplay = model.GetDisplayNode()
    modelDisplay.SetColor(color[0], color[1], color[2])
    modelDisplay.SetVisibility(visibility)
    modelDisplay.SetSliceIntersectionVisibility(True)  # Show in slice view

    PercutaneousApproachAnalysisLogic.updatePathModel(model, paths)

    return model

  def makeSinglePath(self, pathIndex):
    return [self.paths[pathIndex]]

  def makeVirtualPath(self, pathIndex, virtualPosition):
    targetP = self.paths[pathIndex][0]
    skinP = virtualPosition
    return [[targetP, skinP]]

  def computePaths(self, targetPointNode, obstacleModelNode, skinModelNode):
    """ Compute self.paths
    """
    import numpy as np

    targetPoint = np.array(targetPointNode.GetNthControlPointPositionWorld(0))

    skinPolyData = skinModelNode.GetPolyData()
    polyDataNormals = vtk.vtkPolyDataNormals()
    polyDataNormals.SetInputData(skinPolyData)
    polyDataNormals.Update()
    skinPolyData = polyDataNormals.GetOutput()
    nSkinPoints = skinPolyData.GetNumberOfPoints()

    # Create an array for needle passing points.
    # Each element contains a pair of target point and skin point 
    self.paths = [] 

    tolerance = 0.001
    t = vtk.mutable(0.0)
    x = [0.0, 0.0, 0.0] # The coordinate of the intersection 
    pcoords = [0.0, 0.0, 0.0]
    subId = vtk.mutable(0)

    bspTree = vtk.vtkModifiedBSPTree()
    bspTree.SetDataSet(obstacleModelNode.GetPolyData())
    bspTree.BuildLocator()

    self.shortestPathIndex = -1
    shortestPathLength = 1e6
    self.longestPathIndex = -1
    longestPathLength = 0.0

    for index in range(nSkinPoints):
      skinPoint = np.array(skinPolyData.GetPoint(index))
      intersect = bspTree.IntersectWithLine(skinPoint, targetPoint, tolerance, t, x, pcoords, subId)
      if intersect:
        # This path intersects the obstacle, the target is not approachable from here
        continue
      self.paths.append([targetPoint.copy(), skinPoint.copy()])
      pathLength = np.linalg.norm(targetPoint-skinPoint)
      if pathLength < shortestPathLength:
        shortestPathLength = pathLength
        self.shortestPathIndex = len(self.paths) - 1
      if pathLength > longestPathLength:
        longestPathLength = pathLength
        self.longestPathIndex = len(self.paths) - 1

    return self.paths

  @staticmethod
  def createSphereModel(modelName, color, visibility=True):
    sphere = vtk.vtkSphereSource()
    sphere.SetRadius(2.5)
    sphere.SetPhiResolution(100)
    sphere.SetThetaResolution(100)
    sphere.Update()

    # Create model node
    sphereCursor = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLModelNode", slicer.mrmlScene.GenerateUniqueName(modelName))
    sphereCursor.SetAndObservePolyData(sphere.GetOutput())

    # Create display node
    sphereCursor.CreateDefaultDisplayNodes()
    cursorModelDisplay = sphereCursor.GetDisplayNode()
    cursorModelDisplay.SetColor(color[0], color[1], color[2])
    cursorModelDisplay.SetOpacity(0.3)
    cursorModelDisplay.SetVisibility(visibility)
    cursorModelDisplay.SetSliceIntersectionVisibility(True) # Show in slice view

    # Create transform node
    transform = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLLinearTransformNode", slicer.mrmlScene.GenerateUniqueName(modelName + "Transform"))
    sphereCursor.SetAndObserveTransformNodeID(transform.GetID())

    return sphereCursor

  def setSpherePositionAlongPath(self, sphereNode, pathIndex, normalizedPosition):
    """normalizedPosition is position along the path, value is between 0.0-1.0
    """
    startPos, endPos = self.paths[pathIndex]
    position = endPos + (startPos-endPos) * normalizedPosition
    PercutaneousApproachAnalysisLogic.setSpherePosition(sphereNode, position)
    return position

  @staticmethod
  def setSpherePosition(sphereNode, position):
    transformToParent = vtk.vtkMatrix4x4()
    transformToParent.SetElement(0, 3, position[0])
    transformToParent.SetElement(1, 3, position[1])
    transformToParent.SetElement(2, 3, position[2])
    sphereNode.GetParentTransformNode().SetMatrixTransformToParent(transformToParent)

  def calcApproachScore(self, targetPointNode, obstacleModelNode, skinModelNode):
    # skin model point scalar = -1 if inaccessible (occluded or distance >130);
    # point scalar = 100..230 if accessible, the larger distance, the better
    import numpy as np
    pTarget = np.array(targetPointNode.GetNthControlPointPositionWorld(0))

    skinPolyData = skinModelNode.GetPolyData()
    # Triangulate
    triangulator = vtk.vtkTriangleFilter()
    triangulator.SetInputData(skinPolyData)
    # Compute normals
    polyDataNormals = vtk.vtkPolyDataNormals()
    polyDataNormals.SetInputConnection(triangulator.GetOutputPort())
    polyDataNormals.ComputeCellNormalsOn()
    polyDataNormals.Update()
    skinPolyData = polyDataNormals.GetOutput()

    bspTree = vtk.vtkModifiedBSPTree()
    bspTree.SetDataSet(obstacleModelNode.GetPolyData())
    bspTree.BuildLocator()

    pSurface=[0.0, 0.0, 0.0]
    minDistancePoint = [0.0, 0.0, 0.0]

    tolerance = 0.001
    t = vtk.mutable(0.0)
    x = [0.0, 0.0, 0.0]
    pcoords = [0.0, 0.0, 0.0]
    subId = vtk.mutable(0)

    # Map surface model
    if skinModelNode:
      pointValue = vtk.vtkDoubleArray()
      pointValue.SetName("Accessibility")
      pointValue.SetNumberOfComponents(1)
      pointValue.SetNumberOfTuples(skinPolyData.GetNumberOfPoints())
      pointValue.FillComponent(0,0.0)

    accessibleArea = 0.0
    inaccessibleArea = 0.0
    modifiedArea = 0.0
    minDistance = -1

    ids=vtk.vtkIdList()
    cp0=[0.0, 0.0, 0.0]
    cp1=[0.0, 0.0, 0.0]
    cp2=[0.0, 0.0, 0.0]

    nCells = skinPolyData.GetNumberOfCells()
    for index in range(nCells):
      cell = skinPolyData.GetCell(index)
      if cell.GetCellType() == vtk.VTK_TRIANGLE:
        area = cell.ComputeArea()
        skinPolyData.GetCellPoints(index, ids)
        skinPolyData.GetPoint(ids.GetId(0), cp0)
        skinPolyData.GetPoint(ids.GetId(1), cp1)
        skinPolyData.GetPoint(ids.GetId(2), cp2)
        vtk.vtkTriangle.TriangleCenter(cp0, cp1, cp2, pSurface)
        iD = bspTree.IntersectWithLine(pSurface, pTarget, tolerance, t, x, pcoords, subId)
        if iD < 1:
          # no intersection
          if skinModelNode:
            d = math.sqrt(vtk.vtkMath.Distance2BetweenPoints(pSurface, pTarget))
            
            if d < minDistance or minDistance < 0:
              minDistance = d
              minDistancePoint = [pSurface[0],pSurface[1],pSurface[2]]

            maximumAccessibleDistance = 130
            v = -1.0
            if d < maximumAccessibleDistance:
              # entry point is not too far from target point
              v = d + 101
              modifiedArea = area * (maximumAccessibleDistance - d) / maximumAccessibleDistance
              accessibleArea += modifiedArea

            pointValue.SetValue(ids.GetId(0), v)
            pointValue.SetValue(ids.GetId(1), v)
            pointValue.SetValue(ids.GetId(2), v)
            
        else:
          # intersection
          if skinModelNode:
            v = -1.0
            pointValue.SetValue(ids.GetId(0), v)
            pointValue.SetValue(ids.GetId(1), v)
            pointValue.SetValue(ids.GetId(2), v)
          inaccessibleArea += area

      else:
        print ("ERROR: Non-triangular cell.")

    score = accessibleArea

    if skinModelNode:
      skinModelNode.AddPointScalars(pointValue)

      skinModelNode.GetDisplayNode().SetActiveScalar("Accessibility", vtk.vtkAssignAttribute.POINT_DATA)
      skinModelNode.GetDisplayNode().SetAndObserveColorNodeID("vtkMRMLColorTableNodeFileMagma.txt")
      skinModelNode.GetDisplayNode().SetScalarVisibility(True)

      # skinModelNode.SetActivePointScalars("Accessibility", vtk.vtkDataSetAttributes.SCALARS)
      # skinModelNode.Modified()
      # displayNode = skinModelNode.GetModelDisplayNode()
      # displayNode.SetActiveScalarName("Accessibility")
      # displayNode.SetScalarRange(0.0,20.0)
      # displayNode.SetScalarVisibility(False)

    return (score, minDistance, minDistancePoint)


class PercutaneousApproachAnalysisTest(unittest.TestCase):
  """
  This is the test case for your scripted module.
  """

  def delayDisplay(self,message,msec=1000):
    """This utility method displays a small dialog and waits.
    This does two things: 1) it lets the event loop catch up
    to the state of the test so that rendering and widget updates
    have all taken place before the test continues and 2) it
    shows the user/developer/tester the state of the test
    so that we'll know when it breaks.
    """
    print(message)
    self.info = qt.QDialog()
    self.infoLayout = qt.QVBoxLayout()
    self.info.setLayout(self.infoLayout)
    self.label = qt.QLabel(message,self.info)
    self.infoLayout.addWidget(self.label)
    qt.QTimer.singleShot(msec, self.info.close)
    self.info.exec_()

  def setUp(self):
    """ Do whatever is needed to reset the state - typically a scene clear will be enough.
    """
    slicer.mrmlScene.Clear(0)

  def runTest(self):
    """Run as few or as many tests as needed here.
    """
    self.setUp()
    self.test_PercutaneousApproachAnalysis1()

  def test_PercutaneousApproachAnalysis1(self):
    """ Ideally you should have several levels of tests.  At the lowest level
    tests sould exercise the functionality of the logic with different inputs
    (both valid and invalid).  At higher levels your tests should emulate the
    way the user would interact with your code and confirm that it still works
    the way you intended.
    One of the most important features of the tests is that it should alert other
    developers when their changes will have an impact on the behavior of your
    module.  For example, if a developer removes a feature that you depend on,
    your test should break so they know that the feature is needed.
    """

    self.delayDisplay("Starting the test")
    #
    # first, get some data
    #
    import urllib
    downloads = (
        ('http://slicer.kitware.com/midas3/download?items=5767', 'FA.nrrd', slicer.util.loadVolume),
        )

    for url,name,loader in downloads:
      filePath = slicer.app.temporaryPath + '/' + name
      if not os.path.exists(filePath) or os.stat(filePath).st_size == 0:
        print('Requesting download %s from %s...\n' % (name, url))
        urllib.urlretrieve(url, filePath)
      if loader:
        print('Loading %s...\n' % (name,))
        loader(filePath)
    self.delayDisplay('Finished with download and loading\n')

    volumeNode = slicer.util.getNode(pattern="FA")
    logic = PercutaneousApproachAnalysisLogic()
    self.delayDisplay('Test passed!')
