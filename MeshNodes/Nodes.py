import FreeCAD
import FreeCADGui
import Part, Mesh
import os
from Mesh import Mesh

from PySide2 import QtGui, QtWidgets
from importlib import reload

print( "MeshNodes.Nodes: Mod run" )

from NodesCommon import getIconPath 

class MeshExportObj:
    def __init__(self, obj):
        obj.Proxy = self

        # Set initial properties
        obj.addProperty("App::PropertyFile", "SaveFile",   "MeshExport", "Destination file for object exporting")
        obj.addProperty("App::PropertyLink", "LinkedBody", "MeshExport", "Linked Body")

    def execute( self, obj ):
        print( "Execute mesh Export " )
        # Execute the Python script referenced by the node
        body = obj.LinkedBody
        if body:
            print("Linked Body:", body.Label)
            filename = obj.SaveFile
            if filename is not None and filename != "":
                Part.export( [ body ], filename )
        else:
            print("No Linked Body")
                
    def onChanged( self, obj, prop ):
        print(".onChanged", prop )
        # Check if the property that changed is LinkedBody
        if prop == "LinkedBody":
            self.execute( obj )
            
    def dumps( self ):
        return None
    
    def loads( self, state ):
        return None

            
class MeshExportView:
    def __init__(self, vobj):
        self.Object = vobj.Object
        vobj.Proxy = self

    def getIcon(self):
        #print(getIconPath("Export.svg"))
        return getIconPath( "Export.svg" )

    def attach(self, vobj):
        print( ".Attach" )
        self.ViewObject = vobj
        self.Object = vobj.Object
        vobj.Proxy = self

    def claimChildren(self):
        return [self.Object.LinkedBody]
    
    def dumps( self ):
        return None
    
    def loads( self, state ):
        return None

class MeshImportObj:
    def __init__(self, obj):
        obj.Proxy = self

        # Set initial properties
        obj.addProperty("App::PropertyFile", "SourceFile",   "MeshImport", "Source file for object importing")

#    def setViewProvider( self, vp ):
#        self.vp = vp
        
    def execute( self, obj ):
        print( "MeshImportObj.Execute mesh Import " )
        # Execute the Python script referenced by the node

        filename = obj.SourceFile
        if filename is not None and filename != "" and os.path.isfile(filename):
            print(" MeshImportObj.execute( %s )" % filename )
            
            mesh = Mesh()
            mesh.read( filename )
            #self.mesh = mesh
            #self.mesh = Part.makeBox( 10, 10, 10 )
            
            shape = Part.Shape()
            shape.makeShapeFromMesh(mesh.Topology, 0.1)
            obj.Shape = shape
                
        else:
            print("MeshImportObj: Filename is wrong", filename )
                
#    def onChanged( self, obj, prop ):
#        print("MeshImportObj.onChanged", prop )
#        # Check if the property that changed is SourceFile
#        if prop == "SourceFile":
#            self.execute( obj )
    def dumps( self ):
        return None
    
    def loads( self, state ):
        return None

            
class MeshImportView:
    def __init__(self, vobj):
#        self.Object = vobj.Object
        vobj.Proxy = self

    def getIcon(self):
        #print(getIconPath("Import.svg"))
        return getIconPath( "Import.svg" )

    def attach(self, vobj):
        print( "MeshImportView.Attach" )
#        self.ViewObject = vobj
#        self.Object = vobj.Object
        vobj.Proxy = self
#        vobj.Object.Proxy.vp = self

    #def claimChildren(self):
    #    return [ self.Object ]
                
    def getDisplayModes( self, obj ):
        return []
    
    def getDefaultDisplayMode( self ):
        return "Shaded"
    
    def setDisplayMode( self, mode ):
        return mode
    
    def updateData( self, obj, prop ):
        print( "MeshImportView.updateData( ", prop, " )" )
        
    def onChanged( self, vp, prop ):
        print( "MeshImportView.onChanged( ", prop, " )" )
        if prop == "Visibility":
            #self.Visibility = vp.Visibility
            print( vp.Visibility )
            
    def dumps( self ):
        return None
    
    def loads( self, state ):
        return None

def makeMeshExport( body, filename ):
    doc = FreeCAD.ActiveDocument
    obj = doc.addObject("Part::FeaturePython", "MeshExport")
    me = MeshExportObj( obj )
    vp = MeshExportView( obj.ViewObject )

    # Set properties based on UI inputs
    obj.LinkedBody = body
    obj.SaveFile = filename
    
    return obj

def makeMeshImport( filename ):
    doc = FreeCAD.ActiveDocument
    obj = doc.addObject("Part::FeaturePython", "MeshImport")
    me = MeshImportObj( obj )
    vp = MeshImportView( obj.ViewObject )

    # Set properties based on UI inputs
    obj.SourceFile = filename
    return obj

    
# Add a menu item to create the RunScriptNode
#FreeCADGui.addCommand( 'CreateMeshExport', createMeshExport() )
print( "MeshNodes.Nodes: Done" )
