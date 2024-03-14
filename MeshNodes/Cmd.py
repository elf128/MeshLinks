import FreeCAD
import FreeCADGui
import Part
from PySide2 import QtGui, QtWidgets

from NodesCommon import getIconPath, Log

Log( "MeshNodes.Cmd: Import" )

from MeshNodes import UI
from importlib import reload

Log( "MeshNodes.Cmd: Mod run" )

def Reload():
    reload( UI )
    UI.Reload()
    
class createMeshImport():
    def GetResources( self ):
        return { "MenuText" : "Make new mesh importer",
                 "Pixmap"   : getIconPath( "Import.svg" ),
                 "ToopTip"  : "This command create mesh exporter" }
    
    def Activated( self ):
        panel = UI.MeshImporterTaskPanel()
        FreeCADGui.Control.showDialog( panel )
        
    def IsActive( self ):
        doc = FreeCAD.ActiveDocument
        
        if doc:
            return True
        
        return False
    

class createMeshExport():
    def GetResources( self ):
        return { "MenuText" : "Make new mesh exporter",
                 "Pixmap"   : getIconPath( "Export.svg" ),
                 "ToopTip"  : "This command create mesh exporter" }
    
    def Activated( self ):
        panel = UI.MeshExporterTaskPanel()
        FreeCADGui.Control.showDialog( panel )
        
    def IsActive( self ):
        doc = FreeCAD.ActiveDocument
        
        if doc:
            return True
        
        return False
    

class createMeshBool():
    def GetResources( self ):
        return { "MenuText" : "Make operation between objects",
                 "Pixmap"   : getIconPath( "Bool.svg" ),
                 "ToopTip"  : "This command makes operation between objects" }
    
    def Activated( self ):
        panel = UI.MeshBoolTaskPanel()
        FreeCADGui.Control.showDialog( panel )
        
    def IsActive( self ):
        doc = FreeCAD.ActiveDocument
        
        if doc:
            return True
        
        return False
    


FreeCADGui.addCommand( 'CreateMeshImport', createMeshImport() )
FreeCADGui.addCommand( 'CreateMeshExport', createMeshExport() )
FreeCADGui.addCommand( 'CreateMeshBool',   createMeshBool() )

Log( "MeshNodes.Cmd: Done" )
