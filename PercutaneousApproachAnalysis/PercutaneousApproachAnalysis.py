import os
import unittest
from __main__ import vtk, qt, ctk, slicer

#
# PercutaneousApproachAnalysis
#

class PercutaneousApproachAnalysis:
  def __init__(self, parent):
    parent.title = "PercutaneousApproachAnalysis" # TODO make this more human readable by adding spaces
    parent.categories = ["Examples"]
    parent.dependencies = []
    parent.contributors = ["Atsushi Yamada (Shiga University of Medical Science), Junichi Tokuda (Brigham and Women's Hospital), Koichiro Murakami (Shiga University of Medical Science)"] # replace with "Firstname Lastname (Org)"
    parent.helpText = """
    This is an example of scripted loadable module bundled in an extension.
    """
    #parent.acknowledgementText = """
    #This file was originally developed by Jean-Christophe Fillion-Robin, Kitware Inc. and Steve Pieper, Isomics, Inc.  and was partially funded by NIH grant 3P41RR013218-12S1.
#""" # replace with organization, grant and thanks.
    parent.acknowledgementText = """ """
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

    self.sceneReceived = slicer.mrmlScene
    self.modelReceived = slicer.vtkMRMLModelNode()

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
    self.layout.addWidget(parametersCollapsibleButton)

    # Layout within the dummy collapsible button
    parametersFormLayout = qt.QFormLayout(parametersCollapsibleButton)

    #
    # Target point (vtkMRMLMarkupsFiducialNode)
    #
    self.targetSelector = slicer.qMRMLNodeComboBox()
    self.targetSelector.nodeTypes = ( ("vtkMRMLMarkupsFiducialNode"), "" )
    self.targetSelector.addEnabled = False
    self.targetSelector.removeEnabled = False
    self.targetSelector.noneEnabled = True
    self.targetSelector.showHidden = False
    self.targetSelector.showChildNodeTypes = False
    self.targetSelector.setMRMLScene( slicer.mrmlScene )
    self.targetSelector.setToolTip( "Pick up the target point" )
    parametersFormLayout.addRow("Target Point: ", self.targetSelector)

    #
    # target model (vtkMRMLModelNode)
    #
    self.targetModelSelector = slicer.qMRMLNodeComboBox()
    self.targetModelSelector.nodeTypes = ( ("vtkMRMLModelNode"), "" )
    self.targetModelSelector.addEnabled = False
    self.targetModelSelector.removeEnabled = False
    self.targetModelSelector.noneEnabled =  True
    self.targetModelSelector.showHidden = False
    self.targetModelSelector.showChildNodeTypes = False
    self.targetModelSelector.setMRMLScene( slicer.mrmlScene )
    self.targetModelSelector.setToolTip( "Pick the target model to the algorithm." )
    parametersFormLayout.addRow("Target Model: ", self.targetModelSelector)

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
    # Apply Button
    #
    self.applyButton = qt.QPushButton("Paths Analysis Start")
    self.applyButton.toolTip = "Run the algorithm."
    self.applyButton.enabled = False    
    parametersFormLayout.addRow(self.applyButton)

    # connections
    self.applyButton.connect('clicked(bool)', self.onApplyButton)
    self.targetSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
    self.targetModelSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
    self.obstacleModelSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
    self.skinModelSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)

    #
    # Outcomes Area
    #
    outcomesCollapsibleButton = ctk.ctkCollapsibleButton()
    outcomesCollapsibleButton.text = "Outcomes"
    self.layout.addWidget(outcomesCollapsibleButton)

    # Layout within the dummy collapsible button
    outcomesFormLayout = qt.QFormLayout(outcomesCollapsibleButton)

    #
    # Numbers of skin polygons
    #
    self.numbersOfSkinPolygonsSpinBox = ctk.ctkDoubleSpinBox()
    self.numbersOfSkinPolygonsSpinBox.decimals = 0
    self.numbersOfSkinPolygonsSpinBox.minimum = 0
    self.numbersOfSkinPolygonsSpinBox.maximum = 10000000
    self.numbersOfSkinPolygonsSpinBox.suffix = ""
    outcomesFormLayout.addRow("Numbers of Skin Polygons: ", self.numbersOfSkinPolygonsSpinBox)

    #
    # Numbers of approchable polygons
    #
    self.numbersOfApproachablePolygonsSpinBox = ctk.ctkDoubleSpinBox()
    self.numbersOfApproachablePolygonsSpinBox.decimals = 0
    self.numbersOfApproachablePolygonsSpinBox.minimum = 0
    self.numbersOfApproachablePolygonsSpinBox.maximum = 10000000
    self.numbersOfApproachablePolygonsSpinBox.suffix = ""
    outcomesFormLayout.addRow("Numbers of Approachable Polygons: ", self.numbersOfApproachablePolygonsSpinBox)

    #
    # Approachable Score
    #
    self.approachableScoreSpinBox = ctk.ctkDoubleSpinBox()
    self.approachableScoreSpinBox.decimals = 2
    self.approachableScoreSpinBox.minimum = 0
    self.approachableScoreSpinBox.maximum = 10000000
    self.approachableScoreSpinBox.suffix = ""
    outcomesFormLayout.addRow("Approachable Score: ", self.approachableScoreSpinBox)

    #
    # Paths planning Area
    #
    pathsplanningCollapsibleButton = ctk.ctkCollapsibleButton()
    pathsplanningCollapsibleButton.text = "Paths Planning"
    self.layout.addWidget(pathsplanningCollapsibleButton)

    # Layout within the dummy collapsible button
    pathPlanningFormLayout = qt.QFormLayout(pathsplanningCollapsibleButton)

    #
    # Create Paths Button
    #
    self.createPathsButton = qt.QPushButton("Create path")
    self.createPathsButton.toolTip = "Run the algorithm."
    self.createPathsButton.enabled = True    
    pathPlanningFormLayout.addRow(self.createPathsButton)

    # Frame slider
    self.frameSlider = ctk.ctkSliderWidget()
    self.frameSlider.connect('valueChanged(double)', self.frameSliderValueChanged)
    self.frameSlider.decimals = 0
    pathPlanningFormLayout.addRow("Path Candidates:", self.frameSlider)

    # connections
    self.createPathsButton.connect('clicked(bool)', self.onCreatePathsButton)

    # Add vertical spacer
    self.layout.addStretch(1)

    # Switch to distinguish between a point target and a target model
    self.targetSwitch = 0

    # Create an array for all approachable points
    # tempolary solution 
    self.apReceived = numpy.zeros([10000,3])
  
    self.nPointsReceived = 0
    self.nPathReceived = 0
    self.frameSliderValue = 0

    # avoid initializing error for frameSliderValueChanged(self, newValue) function
    self.tmpSwitch = 0

  def cleanup(self):
    pass

  def frameSliderValueChanged(self, newValue):

    import numpy

    #print "frameSliderValueChanged:", newValue
    self.frameSliderValue = newValue
 
    if self.tmpSwitch == 1:
      self.onCreatePathsButton()

  def onSelect(self):
    if (self.targetSelector.currentNode() != None) and (self.obstacleModelSelector.currentNode() != None) and (self.skinModelSelector.currentNode() != None):
    	self.applyButton.enabled = True
    if (self.targetModelSelector.currentNode() != None) and (self.obstacleModelSelector.currentNode() != None) and (self.skinModelSelector.currentNode() != None):
      self.applyButton.enabled = True
      self.targetSwitch = 1

  def onCreatePathsButton(self):

    import numpy

    logic = PercutaneousApproachAnalysisLogic()
    print("onCreatePathsButton() is called ")

    # Remove VTK model
    logic.removeAction(self.sceneReceived, self.modelReceived)
    
    # Change the range of the Slider based on the numbers of approachable polygons    
    self.frameSlider.maximum = self.numbersOfApproachablePolygonsSpinBox.value

    # for debuging
    #print(self.apReceived)

    # for debuging. -> it's ok. (11/5/2013)
    ppp = [0.0, 0.0, 0.0]
    """
    for number in range(0,self.nPointsReceived*2):
      #print(self.apReceived[number*4])
      #print(number*4+1)
      print(self.apReceived[number][0])
      print(self.apReceived[number][1])
      print(self.apReceived[number][2])
    """

    # test to indicate one candidate for needle paths
    tipPoint = numpy.zeros([2,3])

    targetP = [self.apReceived[self.frameSliderValue*2][0], self.apReceived[self.frameSliderValue*2][1], self.apReceived[self.frameSliderValue*2][2]]
    aSkinP = [self.apReceived[self.frameSliderValue*2+1][0], self.apReceived[self.frameSliderValue*2+1][1], self.apReceived[self.frameSliderValue*2+1][2]]
    tipPoint[0] = targetP
    tipPoint[1] = aSkinP
    onePath = [tipPoint[0]]
    onePath.append(tipPoint[1])

    #print(onePath)

    # Create the list for needle passing points to draw virtual god ray 
    # target point and a point on skin
    self.sceneReceived, self.modelReceived, pReceived = NeedlePathModel().run(onePath, 2)
    self.tmpSwitch = 1

  def onApplyButton(self):
    logic = PercutaneousApproachAnalysisLogic()
    print("onApplyButton() is called ")
    targetPoint = self.targetSelector.currentNode()
    targetModel = self.targetModelSelector.currentNode()
    obstacleModel = self.obstacleModelSelector.currentNode()
    skinModel = self.skinModelSelector.currentNode()
    
    self.nPointsReceived, self.nPathReceived, self.sceneReceived, self.modelReceived, self.apReceived = logic.run(targetPoint, targetModel, self.targetSwitch, obstacleModel, skinModel)
    
    # Update outcomes
    # nPointsReceived equals total numbers of skin model
    # nPathReceived equals total numbers of approachable points on the skin model
    self.numbersOfSkinPolygonsSpinBox.value = self.nPointsReceived
    self.numbersOfApproachablePolygonsSpinBox.value = self.nPathReceived
    self.approachableScoreSpinBox.value = float(float(self.nPathReceived) / float(self.nPointsReceived))

    # for debuging
    print(float(self.nPointsReceived))
    print(float(self.nPathReceived))
    print(float(float(self.nPathReceived)/float(self.nPointsReceived)))
    print(self.apReceived)

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
    except Exception, e:
      import traceback
      traceback.print_exc()
      qt.QMessageBox.warning(slicer.util.mainWindow(), 
          "Reload and Test", 'Exception!\n\n' + str(e) + "\n\nSee Python Console for Stack Trace")

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
    pass

  def hasImageData(self,volumeNode):
    """This is a dummy logic method that 
    returns true if the passed in volume
    node has valid image data
    """
    if not volumeNode:
      print('no volume node')
      return False
    if volumeNode.GetImageData() == None:
      print('no image data')
      return False
    return True

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

  def removeAction(self, scene, model):
    print ('removeAction() is called')
    scene.RemoveNode(model)
    #NeedlePathModel().RemovePathsModel()

  def run(self, targetPointNode, targetModelNode, targetSwitch, obstacleModelNode, skinModelNode):
    """
    Run the actual algorithm
    """
    print ('run() is called')

    import numpy
    
    # The variable nPoints represents numbers of polygons for skin model
    poly = skinModelNode.GetPolyData()
    polyDataNormals = vtk.vtkPolyDataNormals()
    polyDataNormals.SetInput(poly)
    polyDataNormals.Update()
    polyData = polyDataNormals.GetOutput()
    nPoints = polyData.GetNumberOfPoints()
    nPoints2 = nPoints*2

    # The variable nPointsT represents numbers of polygons for target model
    if targetSwitch == 1:
      polyT = targetModelNode.GetPolyData()
      polyTDataNormals = vtk.vtkPolyDataNormals()
      polyTDataNormals.SetInput(polyT)
      polyTDataNormals.Update()
      polyTData = polyTDataNormals.GetOutput()
      nPointsT = polyTData.GetNumberOfPoints()
      nPointsT2 = nPointsT*2
      p2 = [0.0, 0.0, 0.0]
    else:
      nPointsT = 1
      nPointsT2 = nPointsT*2
      tPoint = targetPointNode.GetMarkupPointVector(0, 0)
      p2 = [tPoint[0], tPoint[1], tPoint[2]]

    # The variable approachablePoints represents number of approachable polygons on the skin model 
    approachablePoints = nPointsT*nPoints

    p1=[0.0, 0.0, 0.0]
    
    tolerance = 0.001
    t = vtk.mutable(0.0)
    x = [0.0, 0.0, 0.0] # The coordinate of the intersection 
    pcoords = [0.0, 0.0, 0.0]
    subId = vtk.mutable(0)

    bspTree = vtk.vtkModifiedBSPTree()
    bspTree.SetDataSet(obstacleModelNode.GetPolyData())
    bspTree.BuildLocator()

    #print(float(nPoints))
    #print(float(nPointsT))

    # Create an array for needle passing points 
    self.p = numpy.zeros([nPointsT*nPoints2,3])

    for indexT in range(0, nPointsT):
      if targetSwitch == 1:
        polyTData.GetPoint(indexT, p2)
      else:
        p2 = [tPoint[0], tPoint[1], tPoint[2]]

      for index in range(0, nPoints):
        polyData.GetPoint(index, p1)
        iD = bspTree.IntersectWithLine(p1, p2, tolerance, t, x, pcoords, subId)

        # Pick up all needle passing points
        index2 = index*2
        coord = [p2[0],p2[1],p2[2]]
        self.p[indexT*nPoints2+index2] = coord
        approachablePoints = approachablePoints - 1

        if iD == 0: # the case there is no intersection point
          coord = [p1[0],p1[1],p1[2]]
          approachablePoints = approachablePoints + 1

        self.p[indexT*nPoints2+index2+1] = coord

        #print(coord)
        # for debuging
        #print('p1=[%f, %f, %f]' % (p1[0],p1[1],p1[2]))
        #print('p2=[%f, %f, %f]' % (p2[0],p2[1],p2[2]))
        #print('nPoints=%d, index=%d, iD=%d, t=(%f, x=%f, %f, %f)' % (nPoints, index, iD, t, x[0], x[1], x[2]))

    # Create the list for needle passing points to draw virtual god ray 
    self.path = [self.p[0]]
    for index2 in range(1, nPointsT*nPoints2):
      self.path.append(self.p[index2])  
  
    print(self.path)
    # Draw the virtual god ray

    # Create an array for all approachable points 
    pReceived = numpy.zeros([approachablePoints,3])

    #model = NeedlePathModel(self.path)
    scene, model, pReceived = NeedlePathModel().run(self.path, approachablePoints)

    #return (nPoints, float(float(approachablePoints)/float(nPointsT)), scene, model, pReceived)
    return (nPoints, float(float(approachablePoints)/float(nPointsT)), scene, model, self.p)

# NeedlePathModel class is based on EndoscopyPathModel class for Endoscopy module
class NeedlePathModel:
  """Create a vtkPolyData for a polyline:
       - Add one point per path point.
       - Add a single polyline
  """
  def __init__(self):
    #self.modelStored = slicer.vtkMRMLModelNode()
    #self.sceneStored = slicer.mrmlScene
    pass

  def run(self, path, approachablePoints):

    import numpy

    # Create an array for all approachable points 
    p = numpy.zeros([approachablePoints*2,3])
    p1 = [0.0, 0.0, 0.0]

    scene = slicer.mrmlScene
    
    points = vtk.vtkPoints()
    polyData = vtk.vtkPolyData()
    polyData.SetPoints(points)

    lines = vtk.vtkCellArray()
    polyData.SetLines(lines)
    linesIDArray = lines.GetData()
    linesIDArray.Reset()
    linesIDArray.InsertNextTuple1(0)

    polygons = vtk.vtkCellArray()
    polyData.SetPolys( polygons )
    idArray = polygons.GetData()
    idArray.Reset()
    idArray.InsertNextTuple1(0)

    for point in path:
      pointIndex = points.InsertNextPoint(*point)
      linesIDArray.InsertNextTuple1(pointIndex)
      linesIDArray.SetTuple1( 0, linesIDArray.GetNumberOfTuples() - 1 )
      lines.SetNumberOfCells(1)

      # for debuging to check contents of tuples
      #print(pointIndex)
      #print(approachablePoints)
      ##print(linesIDArray.GetTuple1(1))
      ##print(linesIDArray.GetTuple1(2))
      ##print(linesIDArray.GetTuple1(3))

      # Save all approachable points 
      p1[0] = linesIDArray.GetTuple1(1)
      p1[1] = linesIDArray.GetTuple1(2)
      p1[2] = linesIDArray.GetTuple1(3)

      coord = [p1[0], p1[1], p1[2]]
      p[pointIndex] = coord

      #print(coord)

    # Create model node
    model = slicer.vtkMRMLModelNode()
    model.SetScene(scene)
    model.SetName(scene.GenerateUniqueName("NeedlePaths"))
    model.SetAndObservePolyData(polyData)

    # Create display node
    modelDisplay = slicer.vtkMRMLModelDisplayNode()
    modelDisplay.SetColor(1,1,0) # yellow
    modelDisplay.SetScene(scene)
    scene.AddNode(modelDisplay)
    model.SetAndObserveDisplayNodeID(modelDisplay.GetID())

    # Add to scene
    modelDisplay.SetInputPolyData(model.GetPolyData())
    scene.AddNode(model)

    return (scene, model, p)

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
    self.assertTrue( logic.hasImageData(volumeNode) )
    self.delayDisplay('Test passed!')
