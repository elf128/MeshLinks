import FreeCAD
import FreeCADGui

from PySide2 import QtGui, QtWidgets
from importlib import reload
from NodesCommon import getUiPath, Log

Log( "MeshNodes.UI: Import" )

from MeshNodes import Nodes

Log( "MeshNodes.UI: Mod run" )

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


class MeshBoolTaskPanel:
    def __init__(self):
        self.op = 2
        self.form = FreeCADGui.PySideUic.loadUi( getUiPath( "Bool.ui" ) )
        self.form.ObjectSelection.clicked.connect( self.selectObject )

        self.form.Union.clicked.connect( self.operationUnion )
        self.form.Intersection.clicked.connect( self.operationIntersect )
        self.form.Substraction.clicked.connect( self.operationSubstract )
        self.form.Substraction.setChecked( True )

        self.selectObject()

    def selectObject(self):
        selection = FreeCADGui.Selection.getSelection()
        if selection:
            self.form.ObjectNames.setText( ",".join( s.Label for s in selection ) )
        
    def operationUnion( self ):
        Log( "MeshBoolTaskPanel.operationUnion" )
        self.op = 0
    
    def operationIntersect( self ):
        Log( "MeshBoolTaskPanel.operationIntersect" )
        self.op = 1
    
    def operationSubstract( self ):
        Log( "MeshBoolTaskPanel.operationSubstract" )
        self.op = 2
    
    def accept(self):
        doc = FreeCAD.ActiveDocument
        if doc:
            bodyNames = self.form.ObjectNames.text()
            opNames   = [ "Union", "Intersection", "Substraction" ]
            bodyList = [ FreeCAD.ActiveDocument.getObject( name ) for name in bodyNames.split(",") ]
            
            Nodes.makeBool( bodyList, opNames[ self.op ] )

            FreeCADGui.Control.closeDialog()
            doc.recompute()


Log( "MeshNodes.UI: Done" )
