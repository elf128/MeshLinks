import FreeCAD
import FreeCADGui
from PySide2 import QtGui

from NodesCommon import getIconPath

class ScriptNode:
    def __init__(self, obj):
        obj.Proxy = self

    def execute(self, obj):
        # Execute the Python script referenced by the node
        if hasattr(obj, "ScriptFile"):
            exec(open(obj.ScriptFile).read())

class ScriptNodeViewProvider:
    def __init__(self, obj):
        obj.Proxy = self

    def getIcon(self):
        return getIconPath( "Logo.svg" )

    def attach(self, vobj):
        self.ViewObject = vobj
        vobj.Proxy = self

    def claimChildren(self):
        return [obj.ScriptFile]

    def onDelete(self, obj, subelements):
        FreeCADGui.ActiveDocument.removeObject(obj.Name)

class createScriptNode():

    def GetResources( self ):
        return { "MenuText" : "Make new Script Node",
                 "Pixmap"   : getIconPath( "Logo.svg" ),
                 "ToopTip"  : "This command makes new Script Node" }
    
    def Activated( self ):
        doc = FreeCAD.ActiveDocument
        if doc:
            obj = doc.addObject("App::FeaturePython", "ScriptNode")
            ScriptNode(obj)
            ScriptNodeViewProvider(obj)
            doc.recompute()

            # Set initial properties
            obj.addProperty("App::PropertyString", "ScriptFile", "RunScript", "Python script file path")
            obj.addProperty("App::PropertyLink", "LinkedBody", "RunScript", "Linked Body")


            return obj
        
    def IsActive( self ):
        doc = FreeCAD.ActiveDocument
        if doc:
            return True
        return False
    

print( "ScriptNodes: Mod run"  )
# Add a menu item to create the RunScriptNode
FreeCADGui.addCommand( 'CreateScriptNode', createScriptNode() )
print( "ScriptNodes: Done" )
