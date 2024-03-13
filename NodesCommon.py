 
import os

_dir_    = os.path.dirname( __file__ )
iconPath = os.path.join( _dir_, 'icons' )
uiPath   = os.path.join( _dir_, 'ui' )

def getIconPath( filename ):
    return os.path.join( iconPath, filename )

def getUiPath( filename ):
    return os.path.join( uiPath, filename )

def getModRoot():
    return _dir_

print(" NodesCommon is in %s " % _dir_ )
