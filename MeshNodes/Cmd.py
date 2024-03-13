import FreeCAD
import FreeCADGui
import Part
from PySide2 import QtGui, QtWidgets

print( "MeshNodes.Cmd: Import" )

from NodesCommon import getIconPath
from MeshNodes import UI
from importlib import reload

print( "MeshNodes.Cmd: Mod run" )

def Reload():
    reload( UI )
    UI.Reload()
    
class createMeshImport():
    def GetResources( self ):
        return { "MenuText" : "Make new mesh exported",
                 "Pixmap"   : getIconPath( "Import.svg" ),
                 "ToopTip"  : "This command create mesh exporter" }
    
    def Activated( self ):
        panel = UI.MeshImporterTaskPanel()
        #print( dir( FreeCADGui ) )
        FreeCADGui.Control.showDialog( panel )
        
    def IsActive( self ):
        doc = FreeCAD.ActiveDocument
        
        if doc:
            return True
        
        return False
    

class createMeshExport():
    def GetResources( self ):
        return { "MenuText" : "Make new mesh exported",
                 "Pixmap"   : getIconPath( "Export.svg" ),
                 "ToopTip"  : "This command create mesh exporter" }
    
    def Activated( self ):
        panel = UI.MeshExporterTaskPanel()
        #print( dir( FreeCADGui ) )
        FreeCADGui.Control.showDialog( panel )
        
    def IsActive( self ):
        doc = FreeCAD.ActiveDocument
        
        if doc:
            return True
        
        return False
    

class createBooleanMeshBody():
    def GetResources( self ):
        return { "MenuText" : "Make new mesh exported",
                 "Pixmap"   : getIconPath( "BodyMesh.svg" ),
                 "ToopTip"  : "This command create mesh exporter" }
    
    def Activated( self ):
        panel = UI.BooleanMeshBodyTaskPanel()
        #print( dir( FreeCADGui ) )
        FreeCADGui.Control.showDialog( panel )
        
    def IsActive( self ):
        doc = FreeCAD.ActiveDocument
        
        if doc:
            return True
        
        return False
    

class createBooleanMeshMesh():
    def GetResources( self ):
        return { "MenuText" : "-----",
                 "Pixmap"   : getIconPath( "MeshMesh.svg" ),
                 "ToopTip"  : "This command create mesh exporter" }
    
    def Activated( self ):
        panel = UI.BooleanMeshMeshTaskPanel()
        #print( dir( FreeCADGui ) )
        FreeCADGui.Control.showDialog( panel )
        
    def IsActive( self ):
        doc = FreeCAD.ActiveDocument
        
        if doc:
            return True
        
        return False
    
FreeCADGui.addCommand( 'CreateMeshImport',      createMeshImport() )
FreeCADGui.addCommand( 'CreateMeshExport',      createMeshExport() )
#FreeCADGui.addCommand( 'CreateBooleanMeshBody', createBooleanMeshBody() )
#FreeCADGui.addCommand( 'CreateBooleanMeshMesh', createBooleanMeshMesh() )

print( "MeshNodes.Cmd: Done" )
