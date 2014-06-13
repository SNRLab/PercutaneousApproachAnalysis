import os
import unittest
from __main__ import vtk, qt, ctk, slicer
import time
import math

#
# PercutaneousApproachAnalysis
#

class PercutaneousApproachAnalysis:
  def __init__(self, parent):
    parent.title = "PercutaneousApproachAnalysis" # TODO make this more human readable by adding spaces
    parent.categories = ["IGT"]
    parent.dependencies = []
    parent.contributors = ["Koichiro Murakami (Shiga University of Medical Science, Japan, SPL), Laurent Chauvin (SPL), Junichi Tokuda (SPL)"] 
    parent.helpText = """
    The Percutaneous Approach Analysis is used to calculate and visualize the accessibility of liver tumor with a percutaneous approach.
    """
    parent.acknowledgementText = """
    This work is supported in part by the NIH (R01CA111288, P01CA067165, P41RR019703, P41EB015898, R01CA124377, R01CA138586, R42CA137886).
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

  def setup(self):
    # Instantiate and connect widgets ...

    
    ##
    ## Reload and Test area
    ##
    #reloadCollapsibleButton = ctk.ctkCollapsibleButton()
    #reloadCollapsibleButton.text = "Reload && Test"
    #self.layout.addWidget(reloadCollapsibleButton)
    #reloadFormLayout = qt.QFormLayout(reloadCollapsibleButton)
    #
    ## reload button
    ## (use this during development, but remove it when delivering
    ##  your module to users)
    #self.reloadButton = qt.QPushButton("Reload")
    #self.reloadButton.toolTip = "Reload this module."
    #self.reloadButton.name = "PercutaneousApproachAnalysis Reload"
    #reloadFormLayout.addWidget(self.reloadButton)
    #self.reloadButton.connect('clicked()', self.onReload)
    #
    ## reload and test button
    ## (use this during development, but remove it when delivering
    ##  your module to users)
    #self.reloadAndTestButton = qt.QPushButton("Reload and Test")
    #self.reloadAndTestButton.toolTip = "Reload this module and then run the self tests."
    #reloadFormLayout.addWidget(self.reloadAndTestButton)
    #self.reloadAndTestButton.connect('clicked()', self.onReloadAndTest)

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
    # target model (vtkMRMLScalarVolumeNode)
    #
    self.targetLabelSelector = slicer.qMRMLNodeComboBox()
    self.targetLabelSelector.nodeTypes = ( ("vtkMRMLScalarVolumeNode"), "" )
    self.targetLabelSelector.addEnabled = False
    self.targetLabelSelector.removeEnabled = False
    self.targetLabelSelector.noneEnabled =  True
    self.targetLabelSelector.showHidden = False
    self.targetLabelSelector.showChildNodeTypes = False
    self.targetLabelSelector.setMRMLScene( slicer.mrmlScene )
    self.targetLabelSelector.setToolTip( "Pick the target label to the algorithm." )
    parametersFormLayout.addRow("Target Label: ", self.targetLabelSelector)

    ##
    ## output volume selector
    ##
    #self.outputModelSelector = slicer.qMRMLNodeComboBox()
    #self.outputModelSelector.nodeTypes = ( ("vtkMRMLScalarVolumeNode"), "" )
    #self.outputModelSelector.addAttribute( "vtkMRMLScalarVolumeNode", "LabelMap", 0 )
    #self.outputModelSelector.selectNodeUponCreation = False
    #self.outputModelSelector.addEnabled = True
    #self.outputModelSelector.removeEnabled = True
    #self.outputModelSelector.noneEnabled =  True
    #self.outputModelSelector.showHidden = False
    #self.outputModelSelector.showChildNodeTypes = False
    #self.outputModelSelector.setMRMLScene( slicer.mrmlScene )
    #self.outputModelSelector.setToolTip( "Pick the output to the algorithm." )
    #parametersFormLayout.addRow("Output Volume: ", self.outputSelector)

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
    self.obstacleModelSelector.setToolTip( "Pick the input to the algorithm." )
    parametersFormLayout.addRow("Obstacle Model: ", self.obstacleModelSelector)

    ##
    ## scale factor for Obstacle level
    ##
    #self.ObstacleScaleFactorSliderWidget = ctk.ctkSliderWidget()
    #self.ObstacleScaleFactorSliderWidget.singleStep = 1.0
    #self.ObstacleScaleFactorSliderWidget.minimum = 1.0
    #self.ObstacleScaleFactorSliderWidget.maximum = 50.0
    #self.ObstacleScaleFactorSliderWidget.value = 1.0
    #self.ObstacleScaleFactorSliderWidget.setToolTip("Set the Obstacle scale.")
    #parametersFormLayout.addRow("Obstacle scale factor", self.ObstacleScaleFactorSliderWidget)
    
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
    self.skinModelSelector.setToolTip( "Pick the input to the algorithm." )
    parametersFormLayout.addRow("Skin Model: ", self.skinModelSelector)

    ##
    ## check box to trigger taking screen shots for later use in tutorials
    ##
    #self.enableScreenshotsFlagCheckBox = qt.QCheckBox()
    #self.enableScreenshotsFlagCheckBox.checked = 0
    #self.enableScreenshotsFlagCheckBox.setToolTip("If checked, take screen shots for tutorials. Use Save Data to write them to disk.")
    #parametersFormLayout.addRow("Enable Screenshots", self.enableScreenshotsFlagCheckBox)

    ##
    ## scale factor for screen shots
    ##
    #self.screenshotScaleFactorSliderWidget = ctk.ctkSliderWidget()
    #self.screenshotScaleFactorSliderWidget.singleStep = 1.0
    #self.screenshotScaleFactorSliderWidget.minimum = 1.0
    #self.screenshotScaleFactorSliderWidget.maximum = 50.0
    #self.screenshotScaleFactorSliderWidget.value = 1.0
    #self.screenshotScaleFactorSliderWidget.setToolTip("Set scale factor for the screen shots.")
    #parametersFormLayout.addRow("Screenshot scale factor", self.screenshotScaleFactorSliderWidget)

    #
    # Apply Button
    #
    self.applyButton = qt.QPushButton("Apply")
    self.applyButton.toolTip = "Run the algorithm."
    self.applyButton.enabled = False
    parametersFormLayout.addRow(self.applyButton)

    # connections
    self.applyButton.connect('clicked(bool)', self.onApplyButton)
    self.targetSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
    self.targetLabelSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
    self.obstacleModelSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
    self.skinModelSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)

    # Add vertical spacer
    self.layout.addStretch(1)

  def cleanup(self):
    pass

  def onSelect(self):
    if (self.targetSelector.currentNode() != None) and (self.targetLabelSelector.currentNode() == None) and (self.obstacleModelSelector.currentNode() != None) and (self.skinModelSelector.currentNode() != None):
      self.applyButton.enabled = True
    elif (self.targetSelector.currentNode() == None) and (self.targetLabelSelector.currentNode() != None) and (self.obstacleModelSelector.currentNode() != None) and (self.skinModelSelector.currentNode() != None):
      self.applyButton.enabled = True
    else:
      self.applyButton.enabled = False
  
  def onApplyButton(self):
    logic = PercutaneousApproachAnalysisLogic()
    print("onApplyButton() is called ")
    obstacleModel = self.obstacleModelSelector.currentNode()
    skinModel = self.skinModelSelector.currentNode()

    if self.targetLabelSelector.currentNode() != None:
      print("label ")
      targetLabel = self.targetLabelSelector.currentNode()
      start = time.time()
      logic.runLabelWise(targetLabel, obstacleModel, skinModel)
      end = time.time()
      print end - start
    else:
      print("point")
      targetPoint = self.targetSelector.currentNode()
      start = time.time()
      logic.runPointWise(targetPoint, obstacleModel, skinModel)
      end = time.time()
      print end - start


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

  def takeScreenshot(self,name,description,type=-1):
    # show the message even if not taking a screen shot
    self.delayDisplay(description)

    if self.enableScreenshots == 0:
      return

    lm = slicer.app.layoutManager()
    # switch on the type to get the requested window
    widget = 0
    if type == -1:
      # full window
      widget = slicer.util.mainWindow()
    elif type == slicer.qMRMLScreenShotDialog().FullLayout:
      # full layout
      widget = lm.viewport()
    elif type == slicer.qMRMLScreenShotDialog().ThreeD:
      # just the 3D window
      widget = lm.threeDWidget(0).threeDView()
    elif type == slicer.qMRMLScreenShotDialog().Red:
      # red slice window
      widget = lm.sliceWidget("Red")
    elif type == slicer.qMRMLScreenShotDialog().Yellow:
      # yellow slice window
      widget = lm.sliceWidget("Yellow")
    elif type == slicer.qMRMLScreenShotDialog().Green:
      # green slice window
      widget = lm.sliceWidget("Green")

    # grab and convert to vtk image data
    qpixMap = qt.QPixmap().grabWidget(widget)
    qimage = qpixMap.toImage()
    imageData = vtk.vtkImageData()
    slicer.qMRMLUtils().qImageToVtkImageData(qimage,imageData)

    annotationLogic = slicer.modules.annotations.logic()
    annotationLogic.CreateSnapShot(name, description, type, self.screenshotScaleFactor, imageData)


  def calcApproachScore(self, point, skinPolyData, obstacleBspTree, skinModelNode=None):

    pTarget = point
    polyData = skinPolyData
    nPoints = polyData.GetNumberOfPoints()
    nCells = polyData.GetNumberOfCells()
    pSurface=[0.0, 0.0, 0.0]
    
    tolerance = 0.001
    t = vtk.mutable(0.0)
    x = [0.0, 0.0, 0.0]
    pcoords = [0.0, 0.0, 0.0]
    subId = vtk.mutable(0)

    #print ("nPoints = %d" % (nPoints))
    #print ("nCells = %d" % (nCells))

    # Map surface model
    if skinModelNode != None:
      pointValue = vtk.vtkDoubleArray()
      pointValue.SetName("Colors")
      pointValue.SetNumberOfComponents(1)
      pointValue.SetNumberOfTuples(nPoints)
      pointValue.Reset()
      pointValue.FillComponent(0,0.0);
    
    bspTree = obstacleBspTree

    cp0=[0.0, 0.0, 0.0]
    cp1=[0.0, 0.0, 0.0]
    cp2=[0.0, 0.0, 0.0]

    accessibleArea = 0.0
    inaccessibleArea = 0.0

    ids=vtk.vtkIdList()

    minDistance = -1;

    for index in range(nCells):
      cell = polyData.GetCell(index)
      if cell.GetCellType() == vtk.VTK_TRIANGLE:
        area = cell.ComputeArea()
        polyData.GetCellPoints(index, ids)
        polyData.GetPoint(ids.GetId(0), cp0)
        polyData.GetPoint(ids.GetId(1), cp1)
        polyData.GetPoint(ids.GetId(2), cp2)
        vtk.vtkTriangle.TriangleCenter(cp0, cp1, cp2, pSurface)
        iD = bspTree.IntersectWithLine(pSurface, pTarget, tolerance, t, x, pcoords, subId)
        if iD < 1:
          if skinModelNode != None:
            d = vtk.vtkMath.Distance2BetweenPoints(pSurface, pTarget)
            d = math.sqrt(d)
            if d < minDistance or minDistance < 0:
              minDistance = d
            v = d+101
            pointValue.InsertValue(ids.GetId(0), v)
            pointValue.InsertValue(ids.GetId(1), v)
            pointValue.InsertValue(ids.GetId(2), v)
          accessibleArea = accessibleArea + area
        else:
          if skinModelNode != None:
            v = -1.0
            pointValue.InsertValue(ids.GetId(0), v)
            pointValue.InsertValue(ids.GetId(1), v)
            pointValue.InsertValue(ids.GetId(2), v)
          inaccessibleArea = inaccessibleArea + area

      else:
        print ("ERROR: Non-triangular cell.")

    
    score = accessibleArea / (accessibleArea + inaccessibleArea)

    if skinModelNode != None:
      skinModelNode.AddPointScalars(pointValue)
      skinModelNode.SetActivePointScalars("Colors", vtk.vtkDataSetAttributes.SCALARS)
      skinModelNode.Modified()
      displayNode = skinModelNode.GetModelDisplayNode()
      displayNode.SetActiveScalarName("Colors")
      displayNode.SetScalarRange(0.0,200.0)

    return (score, minDistance)
    


  def runLabelWise(self, targetLabelNode, obstacleModelNode, skinModelNode):
    """
    Run label-wise analysis
    """

    poly = skinModelNode.GetPolyData()
    polyDataNormals = vtk.vtkPolyDataNormals()
    polyDataNormals.SetInput(poly)
    polyDataNormals.ComputeCellNormalsOn()
    polyDataNormals.Update()
    polyData = polyDataNormals.GetOutput()
    
    bspTree = vtk.vtkModifiedBSPTree()
    bspTree.SetDataSet(obstacleModelNode.GetPolyData())
    bspTree.BuildLocator()

    trans = vtk.vtkMatrix4x4()
    targetLabelNode.GetIJKToRASMatrix(trans)
    pos = [0.0, 0.0, 0.0, 0.0]

    imageData = targetLabelNode.GetImageData()
    (x0, x1, y0, y1, z0, z1) = imageData.GetExtent()
    for z in range(z0, z1+1):
      for y in range(y0, y1+1):
    	for x in range(x0, x1+1):
          if imageData.GetScalarComponentAsDouble(x, y, z, 0) > 0:
            trans.MultiplyPoint([x, y, z, 1.0], pos);
            (score, mind) = self.calcApproachScore(pos[0:3], polyData, bspTree, None)
            imageData.SetScalarComponentFromDouble(x, y, z, 0, score*100.0+1.0)
            #print ("Index(%f, %f, %f)  -> RAS(%f, %f, %f)" % (x, y, z, pos[0], pos[1], pos[2]))
            #print ("Approach Score (<accessible area> / (<accessible area> + <inaccessible area>)) = %f" % (score))
            
    return True



  def runPointWise(self, targetPointNode, obstacleModelNode, skinModelNode):
    """
    Run point-wise analysis
    """

    print ("runPointWise()")
    tPoint = targetPointNode.GetMarkupPointVector(0, 0)
    pTarget = [tPoint[0], tPoint[1], tPoint[2]]
    poly = skinModelNode.GetPolyData()
    polyDataNormals = vtk.vtkPolyDataNormals()
    polyDataNormals.SetInput(poly)
    polyDataNormals.ComputeCellNormalsOn()
    polyDataNormals.Update()
    polyData = polyDataNormals.GetOutput()

    bspTree = vtk.vtkModifiedBSPTree()
    bspTree.SetDataSet(obstacleModelNode.GetPolyData())
    bspTree.BuildLocator()

    (score, mind) = self.calcApproachScore(pTarget, polyData, bspTree, skinModelNode)

    print ("Approach Score (<accessible area> / (<accessible area> + <inaccessible area>)) = %f" % (score))
    print ("Minmum Distance = %f" % (mind))

    return True
    

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
