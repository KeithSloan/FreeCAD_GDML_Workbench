from PySide import QtGui, QtCore
from PySide.QtCore import Qt

class AddMinTessellateWidget(QtGui.QWidget):
    def __init__(self, Obj, GmshType, *args):
        QtGui.QWidget.__init__(self, *args)
        self.Obj = Obj
        self.setWindowTitle(translate("GDML", "Tessellate with Gmsh Min"))
        # Bounding Box Infp
        bboxGroup = QtGui.QGroupBox("Objects Bounding Box")
        laybbox = QtGui.QHBoxLayout()
        laybbox.addWidget(
            QtGui.QLabel("Width : " + str(Obj.Shape.BoundBox.XLength))
            )
        laybbox.addWidget(
            QtGui.QLabel("Height : " + str(Obj.Shape.BoundBox.YLength))
            )
        laybbox.addWidget(
            QtGui.QLabel("Depth : " + str(Obj.Shape.BoundBox.ZLength))
            )
        bboxGroup.setLayout(laybbox)
        maxl = int( ( Obj.Shape.BoundBox.XLength + Obj.Shape.BoundBox.YLength \
             + Obj.Shape.BoundBox.ZLength) / 15
        )
        # Current Mesh Info
        self.meshInfoGroup = QtGui.QGroupBox("Mesh Info")
        meshInfo = QtGui.QHBoxLayout()
        vertex = facets = ""
        meshCounts = False
        self.tess = self.Obj
        if hasattr(self.Obj, 'tessellated'):
            if self.Obj.tessellated is not None:
                self.tess = self.Obj.tessellated
        if hasattr(self.tess, 'vertex'):
            vertex = str(self.tess.vertex)
            meshCounts = True
        if hasattr(self.tess, 'facets'):
            facets = str(self.tess.facets)
            meshCounts = True
        self.Vertex = oField("Vertex", 6, vertex)
        self.Facets = oField("Facets", 6, facets)
        meshInfo.addWidget(self.Vertex)
        meshInfo.addWidget(self.Facets)
        self.meshInfoGroup.setLayout(meshInfo)
        #self.maxLen = iField("Max Length", 5, str(maxl))
        # Mesh Parameters
        self.meshParmsGroup = QtGui.QGroupBox("Mesh Characteristics")
        # self.tess is set to Obj or Obj.tessellated or
        if hasattr(self.tess, "surfaceDev"):
            sd = str(self.tess.surfaceDev)
        else:
            sd = ".10"
        self.surfaceDeviation = iField("Surface Deviation", 5, sd)
        if hasattr(self.tess, "angularDev"):
            ad = str(self.tess.angularDev)
        else:
            ad = "30"
        self.angularDeviation = iField("Angular Deviation", 5, ad)
        self.meshParmsLayout = QtGui.QGridLayout()
        #self.meshParmsLayout.addWidget(self.type, 0, 0)
        #self.meshParmsLayout.addWidget(self.maxLen, 0, 1)
        self.meshParmsLayout.addWidget(self.surfaceDeviation, 1, 0)
        self.meshParmsLayout.addWidget(self.angularDeviation, 1, 1)
        self.meshParmsGroup.setLayout(self.meshParmsLayout)
        # Action Buttons
        self.buttonMesh = QtGui.QPushButton(translate("GDML", GmshType))
        layoutAction = QtGui.QHBoxLayout()
        layoutAction.addWidget(self.buttonMesh)
        # Panel Layout
        self.Vlayout = QtGui.QVBoxLayout()
        self.Vlayout.addWidget(bboxGroup)
        self.Vlayout.addWidget(self.meshInfoGroup)
        self.Vlayout.addWidget(self.meshParmsGroup)
        self.Vlayout.addLayout(layoutAction)
        self.setLayout(self.Vlayout)
        if meshCounts == False:
            print(f"Not previously Tessellated")
            self.meshInfoGroup.setVisible(False)

    def leaveEvent(self, event):
        print("Leave Event")
        # FreeCADGui.Control.closeDialog()
        # closeDialog()
        # QtCore.QMetaObject.invokeMethod(FreeCADGui.Control, 'closeDialog', QtCore.Qt.QueuedConnection)
        # QtCore.QTimer.singleShot(0, FreeCADGui.Control, SLOT('closeDialog()'))
        # QtCore.QTimer.singleShot(0, FreeCADGui.Control, QtCore.SLOT('closeDialog()'))
        QtCore.QTimer.singleShot(0, lambda: FreeCADGui.Control.closeDialog())


    def retranslateUi(self, widget=None):
        self.buttonMesh.setText(translate("GDML", "Mesh"))
        self.setWindowTitle(translate("GDML", "Tessellate with Gmsh Min"))


class AddMinTessellateTask:
    def __init__(self, Obj):
        # Operation Types
        #   1 Mesh      - Object or GDML Object
        #   2 reMesh    - Object or GDML Object
        #   3 reMesh    - GmshTessellate or Tessellated
        self.obj = Obj
        self.form = AddMinTessellateWidget(Obj, "Min Gmsh")
        self.form.buttonMesh.clicked.connect(self.actionMesh)
        # self.form.buttonload.clicked.connect(self.loadelement)
        # self.form.buttonsave.clicked.connect(self.saveelement)
        # self.form.buttonrefresh.clicked.connect(self.refreshelement)

    def getStandardButtons(self):
        return int(QtGui.QDialogButtonBox.Close)

    def isAllowedAlterSelection(self):
        return True

    def isAllowedAlterView(self):
        return True

    def isAllowedAlterDocument(self):
        return True

    def postProcessMesh(self, actionType):
        from .GDMLObjects import ViewProvider

        print(f"Update Tessellated Object Operation Type {self.operationType}")
        # actionType
        # Operation Types
        #   1 Mesh      - Object or GDML Object
        #   2 reMesh    - Object or GDML Object
        #   3 reMesh    - GmshTessellate or Tessellated#print(dir(self))
        #print("Object Name " + self.obj.Name)
        print("Object Name " + self.obj.Label)
        print("Object Type " + self.obj.TypeId)

        #while switch(actionType):
        #    if case(1):
        if actionType == 1:
                #if hasattr(self.obj, "tessellated"):
                # if self.obj.tessellated is not None:
                #self.tess = self.obj.tessellated
                #print("Tessellated Name " + self.tess.Name)
                #print("Update parms : " + self.tess.Name)
                #print("Tessellated Name " + self.tess.Label)
                #print("Update parms : " + self.tess.Label)
                # Need to update Dialog with details from Gmsh
                #if hasattr(self.tess, "Proxy"):  # If GDML object has Proxy
                #    #print(dir(self.tess.Proxy))
                #    self.tess.Proxy.updateParams(vertex, facets, False)
                #else:
                #    self.tess.updateParams(vertex, facets, False)
                pass
                #self.form.Vertex.value.setText(str(len(vertex)))
                #self.form.Facets.value.setText(str(len(facets)))
                #return

        elif actionType == 2:
                if self.obj.tessellated is not None:
                    self.tess = self.obj.tessellated
                    #print("Tessellated Name " + self.tess.Name)
                    #print("Update parms : " + self.tess.Name)
                    print("Tessellated Name " + self.tess.Label)
                    print("Update parms : " + self.tess.Label)
                    #if hasattr(self.tess, "Proxy"):  # If GDML object has Proxy
                    #print(dir(self.tess.Proxy))
                    #print(dir(self.tess.Proxy))
                #    self.tess.Proxy.updateParams(vertex, facets, False)
                #else:
                #    self.tess.updateParams(vertex, facets, False)
                # print('Update parms : '+self.tess.Name)

        elif actionType == 3:
                if hasattr(self.obj, "Proxy"):
                    print("Proxy")
                    if hasattr(self.obj.Proxy, "Type"):
                        print(self.obj.Proxy.Type)
                        if ( self.obj.Proxy.Type == "GDMLGmshTessellated"
                            or self.obj.Proxy.Type == "GDMLTessellated"):
                            self.tess = self.obj.Proxy
                            #self.tess = self.obj
                            self.obj.Proxy.updateParams(vertex, facets, False)
                            # print(dir(self.form))
                            print("Vertex : " + str(len(vertex)))
                            print("Facets : " + str(len(facets)))
                            # Update Info of GDML Tessellated Object
                            #self.tess = None

        if FreeCAD.GuiUp:
            if self.operationType in [1, 2]:
                self.obj.ViewObject.Visibility = False
                if self.tess is not None:
                    ViewProvider(self.tess.ViewObject)
                    self.tess.ViewObject.DisplayMode = "Wireframe"
                    self.tess.recompute()
                    # FreeCAD.ActiveDocument.recompute()
            else:
                #print("Recompute : " + self.obj.Name)
                print("Recompute : " + self.obj.Label)
                self.obj.recompute()
                self.obj.ViewObject.Visibility = True
            print(f"Update Panel")
            self.form.Vertex.value.setText(str(self.tess.numVertex))
            self.form.Facets.value.setText(str(self.tess.numFacets))
            self.form.meshInfoGroup.setVisible(True)
            print(f"View Fit Gmsh Min")
            FreeCADGui.SendMsgToActiveView("ViewFit")
            FreeCADGui.updateGui()


    def actionMesh(self):       # Gmsh actionMesh
        # Could be one of the following
        # 1 - Gmsh of Object or GDML Object
        # 2 - Re Gmsh of Object or GDML Object
        # 3 - Re Gmsh of selected GmshTessellated or Tessellated Object

        from .GmshUtils import (
            minMeshObject,
            #createFCShape,
            #getVertex,
            #getFacets,
            #getMeshLen,
            printMeshInfo,
            printMyInfo,
            initialize,
        )
        from .GDMLObjects import GDMLGmshTessellated, GDMLTriangular, \
                setLengthQuantity

        #print("Action Min Gmsh§ : " + self.obj.Name)
        print(f"Action Min Gmsh : {self.obj.Label}")
        initialize()
        #print("Object " + self.obj.Name)
        print(f"Object {self.obj.Label}")
        self.operationType = 1
        obj2Mesh = self.obj
        self.tess = None
        # text values or Int Float ?????
        surfaceDev = float(self.form.surfaceDeviation.value.text())
        angularDev = int(self.form.angularDeviation.value.text())
        # Test if action is 2 Re Gmsh of Object or GDML Object
        if hasattr(self.obj, 'tessellated'):
            if self.obj.tessellated is not None:
                self.tess = self.obj.tessellated
                self.operationType = 2
        # Test if action is 3 Re Gmsh of selected
        #      GmshTessellated or Tessellated Object
        if hasattr(self.obj, "Proxy"):
            print(f"Has proxy {self.obj.Proxy}")
            #print(dir(self.obj.Proxy))
            #print(dir(self.obj))
            # Is this a remesh of GDMLGmshTessellated
            if hasattr(self.obj.Proxy, "Type"):
                if self.obj.Proxy.Type == "GDMLGmshTessellated":
                    if hasattr(self.obj.Proxy, "sourceObj"):
                        print("Has source Object - ReMesh")
                        obj2Mesh = self.obj.Proxy.sourceObj
                        self.form.meshInfoGroup.setVisible(True)
                        self.operationType = 3
        # Perform Gmsh Min
        #if minMeshObject(obj2Mesh, float(surfaceDev), float(angularDev)):
        #    print("minMesh get facets and vertex")
        #    numVertex, numFacets, fcShape  = createFCShape()
        if self.operationType == 1:
           print(f"New Gmsh")
           #name = "GDMLTessellate_" + self.obj.Name
           name = "GDMLTessellate_" + self.obj.Label
           parent = None
           if hasattr(self.obj, "InList"):
               if len(self.obj.InList) > 0:
                   parent = self.obj.InList[0]
                   if parent.TypeId != "PartDesign::Body" and \
                           parent is not None:
                      self.tess = parent.newObject(
                            "Part::FeaturePython", name)
           print(f"Create Gmsh Tessellated Object")
           #GDMLGmshTessellated( self.tess, self.obj,
           #     getMeshLen(self.obj), numVertex, numFacets, fcShape,
           #    "mm", getSelectedMaterial())
           #self.tess.addProperty(
           GDMLGmshTessellated( self.tess, self.obj, angularDev, surfaceDev,
                  "mm", getSelectedMaterial())
           #self.tess.addProperty(
           #    "App::PropertyFloat","surfaceDev","GmshParms", \
           #    "Surface Deviation")
           #self.tess.addProperty(
           #    "App::PropertyFloat","angularDev","GmshParms", \
           #    "Angular Deviation")
           #setLengthQuantity(self.tess, self.obj.lunit)
           # Make Mesh Info Visible
           self.form.meshInfoGroup.setVisible(True)
           #self.tess.surfaceDev = float(surfaceDev)
           #self.tess.angularDev = float(angularDev)
           # Indicate that Object has been Tessellated
           #self.obj.addProperty("App::PropertyLinkGlobal","tessellated","Base")
           #self.obj.tessellated = self.tess
           #else:

           #    self.processMesh(self.vertex, self.facets)
           self.postProcessMesh(self.operationType)
           print(f"MinMsh Operation {self.operationType}")
           #if self.operationType == 3:
           #    self.obj.surfaceDev = float(surfaceDev)
           #    self.obj.angularDev = float(angularDev)
           #elif self.operationType == 2:
           #    self.obj.tessellated.surfaceDev = float(surfaceDev)
           #    self.obj.tessellated.angularDev = float(angularDev)
           #elif self.operationType == 1:
           #   FreeCADGui.Selection.clearSelection()
           #   FreeCADGui.Selection.addSelection(self.tess)


    def leaveEvent(self, event):
        print("Leave Event II")

    def focusOutEvent(self, event):
        print("Out of Focus II")

class TessGmshMinFeature:

    def Activated(self):

        from .GmshUtils import (
            initialize,
            meshObject,
            getVertex,
            getFacets,
            getMeshLen,
            printMeshInfo,
            printMyInfo,
        )

        from .GDMLObjects import (
            GDMLGmshTessellated,
            GDMLTriangular,
            ViewProvider,
            ViewProviderExtension,
        )

        print("Action Min Gmsh Activated")
        for obj in FreeCADGui.Selection.getSelection():
            # if len(obj.InList) == 0: # allowed only for for top level objects
            print("Action Min Gmsh Tessellate")
            # print(dir(obj))
            #print(obj.Name)
            print(obj.Label)
            if hasattr(obj, "Shape") and obj.TypeId != "App::Part":
                if FreeCADGui.Control.activeDialog() is False:
                    print("Build panel for TO BE Gmeshed")
                    panel = AddMinTessellateTask(obj)
                    if hasattr(obj, "Proxy"):
                        if hasattr(obj.Proxy, "Type"):
                            print(obj.Proxy.Type)
                            if obj.Proxy.Type == "GDMLGmshTessellated":
                                print("Update panel for EXISTING Gmsh Tessellate")
                                panel.form.meshInfoLayout = QtGui.QHBoxLayout()
                                panel.form.meshInfoLayout.addWidget(
                                    oField("Vertex", 6, str(obj.numVertex))
                                )
                                panel.form.meshInfoLayout.addWidget(
                                    oField("Facets", 6, str(obj.numFacets))
                                )
                    FreeCADGui.Control.showDialog(panel)
                else:
                    print("Already an Active Task")
            return

    def IsActive(self):
        if FreeCAD.ActiveDocument is None:
            return False
        else:
            return True

    def GetResources(self):
        return {
            "Pixmap": "GDML_Tess_Gmsh_Min",
            "MenuText": QtCore.QT_TRANSLATE_NOOP(
                "GDML_TessGroup", "Gmsh Min & Tessellate"
            ),
            "Tessellate_Gmsh": QtCore.QT_TRANSLATE_NOOP(
                "GDML_TessGroup", "Mesh & Tessellate Selected Planar Object"
            ),
        }

class GmshGroup:
    """Group of Gmsh Commands"""
            
    def GetCommands(self):
        """Tuple of Commands"""
        return ("TessellateGmshCommand", "TessGmshMinCommand")

    def GetResources(self):
        """Set icon, menu and tooltip."""
        
        return { 
            "Pixmap": "GDML_Gmsh_Group",
            "MenuText": QtCore.QT_TRANSLATE_NOOP("Gmsh Group", "Gmsh Group"),
            "ToolTip": QtCore.QT_TRANSLATE_NOOP(
                "Gmsh Group", " Group of Gmsh Commands"
            ),
        }

    def IsActive(self):
        """Return True when this command should be available."""
        if FreeCAD.ActiveDocument is None:
            return False
        else:
            return True
