import FreeCAD
import FreeCADGui
import Part, Mesh
import os

from PySide2 import QtGui, QtWidgets
from importlib import reload

from NodesCommon import getIconPath, Log

Log( "MeshNodes.Nodes: Mod run" )


class MeshExportObj:
    def __init__(self, obj):
        obj.Proxy = self

        # Set initial properties
        obj.addProperty("App::PropertyFile", "SaveFile",   "MeshExport", "Destination file for object exporting")
        obj.addProperty("App::PropertyLink", "LinkedBody", "MeshExport", "Linked Body")

    def execute( self, obj ):
        Log( "MeshExportObj.execute mesh Export " )
        # Execute the Python script referenced by the node
        body = obj.LinkedBody
        if body:
            Log("MeshExportObj.execute: Linked Body:", body.Label)
            filename = obj.SaveFile
            if filename is not None and filename != "":
                Part.export( [ body ], filename )
        else:
            Log("MeshExportObj.execute: No Linked Body")
                
    def onChanged( self, obj, prop ):
        Log("MeshExportObj.onChanged", prop )
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
        Log( "MeshImportObj.Execute mesh Import " )
        # Execute the Python script referenced by the node

        filename = obj.SourceFile
        if filename is not None and filename != "" and os.path.isfile(filename):
            Log(" MeshImportObj.execute( %s )" % filename )
            
            mesh = Mesh.Mesh()
            mesh.read( filename )
            #self.mesh = mesh
            #self.mesh = Part.makeBox( 10, 10, 10 )
            
            shape = Part.Shape()
            shape.makeShapeFromMesh(mesh.Topology, 0.1)
            solid = Part.makeSolid(shape)
            obj.Shape = solid
                
        else:
            Log("MeshImportObj: Filename is wrong", filename )
                
#    def onChanged( self, obj, prop ):
#        Log("MeshImportObj.onChanged", prop )
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
        #Log(getIconPath("Import.svg"))
        return getIconPath( "Import.svg" )

    def attach(self, vobj):
        Log( "MeshImportView.Attach" )
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
        Log( "MeshImportView.updateData( ", prop, " )" )
        
    def onChanged( self, vp, prop ):
        Log( "MeshImportView.onChanged( ", prop, " )" )
        if prop == "Visibility":
            #self.Visibility = vp.Visibility
            Log( vp.Visibility )
            
    def dumps( self ):
        return None
    
    def loads( self, state ):
        return None

#App::PropertyLinkList 
class MeshBoolObj:
    OperationList = [ "Union", "Intersection", "Substraction" ]
    def __init__(self, obj):
        obj.Proxy = self

        # Set initial properties
        obj.addProperty("App::PropertyLinkList", "LinkedBodies", "Boolean", "Linked Bodies")
        obj.addProperty("App::PropertyEnumeration", "Operation", "Boolean", "Operation")
        obj.Operation = MeshBoolObj.OperationList
        obj.Operation = "Substraction"

    def getShape( self, obj ):
        solid = None
        
        if type( obj ) is Mesh.Feature:
            shape = Part.Shape()
            shape.makeShapeFromMesh( obj.Mesh.Topology, 0.1 )
            
            solid = Part.makeSolid(shape)
        else:
            solid = obj.Shape
            
        return solid
    
    def execute( self, obj ):
        Log("MeshBoolObj.execute")

        # Get the list of linked bodies
        linked_bodies = obj.LinkedBodies
        
        if not linked_bodies:
            Log("No linked bodies to perform boolean operation")
            return

        # Get the first linked body to use as the initial shape for the boolean operation
        first_body = self.getShape( linked_bodies[0] )
        
        if first_body is None:
            Log("First linked body does not have a shape", linked_bodies[0].Label)
            return

        # Perform boolean operation on the remaining bodies
        result_shape = first_body
        for body in linked_bodies[1:]:
            shape = self.getShape( body )
            
            if shape is None:
                Log("Skipping body without a shape: ", body.Label )
                continue
            
            operation = obj.Operation  # Get the selected boolean operation
            if operation == "Union":
                result_shape = result_shape.fuse()
            elif operation == "Intersection":
                result_shape = result_shape.common(body.Shape)
            elif operation == "Substraction":
                result_shape = result_shape.cut(body.Shape)
            else:
                Log("Unknown boolean operation:", operation)

        # Store the result shape in obj.Shape
        obj.Shape = result_shape
                
    def onChanged( self, obj, prop ):
        Log("MeshBoolObj.onChanged", prop )
        # Check if the property that changed is LinkedBody
        if prop == "LinkedBody":
            self.execute( obj )
            
    def dumps( self ):
        return None
    
    def loads( self, state ):
        return None


class MeshBoolView:
    def __init__(self, vobj):
        self.Object = vobj.Object
        vobj.Proxy = self

    def getIcon(self):
        #Log(getIconPath("Export.svg"))
        return getIconPath( "Bool.svg" )

    def attach(self, vobj):
        Log( "MeshBoolView.Attach" )
        self.ViewObject = vobj
        self.Object = vobj.Object
        vobj.Proxy = self

    def claimChildren(self):
        return self.Object.LinkedBodies
    
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

def makeBool( body_list, operation ):
    doc = FreeCAD.ActiveDocument
    obj = doc.addObject("Part::FeaturePython", "MeshBool")
    
    me = MeshBoolObj( obj )
    vp = MeshBoolView( obj.ViewObject )

    # Set properties based on UI inputs
    obj.LinkedBodies = body_list
    if operation in MeshBoolObj.OperationList:
        obj.Operation = operation
    
    return obj

print( "MeshNodes.Nodes: Done" )
