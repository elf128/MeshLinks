import FreeCAD
import FreeCADGui
import Part
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

class MeshImportObj:
    def __init__(self, obj):
        obj.Proxy = self

        # Set initial properties
        obj.addProperty("App::PropertyFile", "SourceFile",   "MeshImport", "Source file for object importing")
        vertices = [(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)]
        faces = [(0, 1, 2), (0, 2, 3)]
        self.mesh = Mesh()
        # Add vertices to the mesh
        for vertex in vertices:
            self.mesh.Points.extend( vertex )

        # Add faces to the mesh
        for face in faces:
            self.mesh.Facets.extend(face)

    def setViewProvider( self, vp ):
        self.vp = vp
        
    def execute( self, obj ):
        print( "MeshImportObj.Execute mesh Import " )
        # Execute the Python script referenced by the node

        filename = obj.SourceFile
        if filename is not None and filename != "":
            print(" MeshImportObj.execute( %s )" % filename )
            try:
                mesh = Part.Shape()
                mesh.read( filename )
            except Exception as e:
                print( "MeshImportObj.execute: Error loading mesh. \n", str( e ) )
            finally:
                print("MeshImportObj.execute: update mesh" )
                self.mesh = mesh
                
            try:
                self.vp.Shape = self.mesh
            except Exception as e:
                print( "MeshImportObj.execute: Error during shape assignment\n", str( e ) )
                
        else:
            print("MeshImportObj: Filename is empty")
                
    def onChanged( self, obj, prop ):
        print("MeshImportObj.onChanged", prop )
        # Check if the property that changed is SourceFile
        if prop == "SourceFile":
            self.execute( obj )

            
class MeshImportView:
    def __init__(self, vobj):
        self.Object = vobj.Object
        vobj.Proxy = self

    def getIcon(self):
        #print(getIconPath("Import.svg"))
        return getIconPath( "Import.svg" )

    def attach(self, vobj):
        print( "MeshImportView.Attach" )
        self.ViewObject = vobj
        self.Object = vobj.Object
        vobj.Proxy = self
        vobj.Object.Proxy.vp = self

    #def claimChildren(self):
    #    return [ self.Object ]
                
    #def getDisplayModes( self, obj ):
    #    return [ "Shaded" ]
    
    #def getDefaultDisplayMode( self ):
    #    return "Shaded"
    
    #def setDisplayMode( self, mode ):
    #    pass
    
    def onChanged( self, vp, prop ):
        print( "MeshImportView.onChanged( ", vp, prop, " )" )
        if prop == "Visibility":
            self.Visibility = vp.Visibility
            print( vp.Visibility )

def makeMeshExporter( body, filename ):
    obj = doc.addObject("App::FeaturePython", "MeshExport")
    me = Nodes.MeshExportObj( obj )
    vp = Nodes.MeshExportView( obj.ViewObject )

    # Set properties based on UI inputs
    obj.LinkedBody = body
    obj.SaveFile = filename


    
# Add a menu item to create the RunScriptNode
#FreeCADGui.addCommand( 'CreateMeshExport', createMeshExport() )
print( "MeshNodes.Nodes: Done" )
