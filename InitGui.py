#
#
#
print("ScriptNodeGUI: Init")

import ScriptNodes
from MeshNodes import Cmd

def Reload( mod ):
    from importlib import reload
    print( "Reload module" )
    reload( mod )
    mod.Reload()
    
print("ScriptNodeGUI: Import is done")

class ScriptNode( Workbench ):
    from NodesCommon import getIconPath

    MenuText = "ScriptNodes"
    ToolTip  = "A description of my workbench"
    Icon     = getIconPath( "Logo.svg" )

    def Initialize(self):
        #
        self.list = [ 
            "CreateScriptNode",
            "CreateMeshImport",
            "CreateMeshExport",
            "BoleanMeshBody",
            "BoleanMeshMesh", ] 
        
        self.appendToolbar("ScriptNode toolbar", self.list) # creates a new toolbar with your commands
        self.appendMenu("Script Nodes", self.list) # creates a new menu
        #self.appendMenu(["An existing Menu", "My submenu"], self.list) # appends a submenu to an existing menu

    def Activated(self):
        self._reload_( self._mod_ )
        return

    def Deactivated(self):
        """This function is executed whenever the workbench is deactivated"""
        return

    def ContextMenu(self, recipient):
        """This function is executed whenever the user right-clicks on screen"""
        # "recipient" will be either "view" or "tree"
        self.appendContextMenu("My commands", self.list) # add commands to the context menu

    def GetClassName(self): 
        # This function is mandatory if this is a full Python workbench
        # This is not a template, the returned string should be exactly "Gui::PythonWorkbench"
        return "Gui::PythonWorkbench"

wb = ScriptNode()
wb._reload_ = Reload
wb._mod_    = Cmd

Gui.addWorkbench( wb ) 
print("ScriptNodeGUI: Done")
