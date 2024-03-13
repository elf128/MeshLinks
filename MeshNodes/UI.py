import FreeCAD
import FreeCADGui

from PySide2 import QtGui, QtWidgets
from importlib import reload

print( "MeshNodes.UI: Import" )

from MeshNodes import Nodes
from NodesCommon import getUiPath

print( "MeshNodes.UI: Mod run" )

def Reload():
    reload( Nodes )
    

class MeshImporterTaskPanel:
    def __init__(self):
        self.form = FreeCADGui.PySideUic.loadUi( getUiPath( "MeshImporter.ui" ) )
        self.form.ImportFileBrowse.clicked.connect( self.browseFile )
        
    def browseFile(self):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Import from", "", "Any (*.*)")
        if fileName:
            self.form.OpenFile.setText( fileName )

    def accept(self):
        doc = FreeCAD.ActiveDocument
        if doc:
            filename = self.form.OpenFile.text()
            Nodes.makeMeshImport( filename )
            
            FreeCADGui.Control.closeDialog()
            doc.recompute()
                

class MeshExporterTaskPanel:
    def __init__(self):
        self.form = FreeCADGui.PySideUic.loadUi( getUiPath( "MeshExporter.ui" ) )
        self.form.ObjectSelection.clicked.connect( self.selectObject )
        self.form.ExportFileBrowse.clicked.connect( self.browseFile )
        self.selectObject()

    def selectObject(self):
        selection = FreeCADGui.Selection.getSelection()
        if selection:
            self.form.ObjectName.setText(selection[0].Label)

    def browseFile(self):
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(None, "Export to", "", "Any (*.*)")
        if fileName:
            self.form.SaveFile.setText( fileName )

    def accept(self):
        doc = FreeCAD.ActiveDocument
        if doc:
            body     = FreeCAD.ActiveDocument.getObject( self.form.ObjectName.text() )
            filename = self.form.SaveFile.text()
            Nodes.makeMeshExport( body, filename )

            FreeCADGui.Control.closeDialog()
            doc.recompute()

"""
class BooleanMeshBodyTaskPanel:
    def __init__(self):
        self.form = FreeCADGui.PySideUic.loadUi( getUiPath( "Body_Mesh.ui" ) )
        self.form.ObjectSelection.clicked.connect( self.selectObject )
        self.selectObject()

    def selectBody(self):
        selection = FreeCADGui.Selection.getSelection()
        if selection:
            self.form.ObjectName.setText(selection[0].Label)

    def selectMesh(self):
        selection = FreeCADGui.Selection.getSelection()
        if selection:
            self.form.ObjectName.setText(selection[0].Label)
            
    def accept(self):
        doc = FreeCAD.ActiveDocument
        if doc:
            obj = doc.addObject("App::FeaturePython", "MeshExport")
            me = MeshNodes.MeshExportObj( obj )
            vp = MeshNodes.MeshExportView( obj.ViewObject )

            # Set properties based on UI inputs
            obj.LinkedBody = FreeCAD.ActiveDocument.getObject( self.form.ObjectName.text() )
            obj.SaveFile = self.form.SaveFile.text()

            FreeCADGui.Control.closeDialog()
            doc.recompute()


class BooleanMeshMeshTaskPanel:
    def __init__(self):
        self.form = FreeCADGui.PySideUic.loadUi( getUiPath( "Body_Mesh.ui" ) )
        self.form.ObjectSelection.clicked.connect( self.selectObject )
        self.form.ExportFileBrowse.clicked.connect( self.browseFile )
        self.selectObject()

    def selectObject(self):
        selection = FreeCADGui.Selection.getSelection()
        if selection:
            self.form.ObjectName.setText(selection[0].Label)

    def browseFile(self):
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(None, "Export to", "", "Any (*.*)")
        if fileName:
            self.form.SaveFile.setText( fileName )

    def accept(self):
        doc = FreeCAD.ActiveDocument
        if doc:
            obj = doc.addObject("App::FeaturePython", "MeshExport")
            me = MeshNodes.MeshExportObj( obj )
            vp = MeshExportView( obj.ViewObject )

            # Set properties based on UI inputs
            obj.LinkedBody = FreeCAD.ActiveDocument.getObject( self.form.ObjectName.text() )
            obj.SaveFile = self.form.SaveFile.text()

            FreeCADGui.Control.closeDialog()
            doc.recompute()
                
"""
print( "MeshNodes.UI: Done" )
