"""VisionEgg Platform Dependent Library
"""

# Copyright (c) 2001-2002 Andrew Straw.  Distributed under the terms of the
# GNU Lesser General Public License (LGPL).

####################################################################
#
#        Import all the necessary packages
#
####################################################################

import sys,os,string
import VisionEgg.Core

__version__ = VisionEgg.release_name
__cvs__ = string.split('$Revision$')[1]
__date__ = string.join(string.split('$Date$')[1:3], ' ')
__author__ = 'Andrew Straw <astraw@users.sourceforge.net>'

############# Import Vision Egg C routines, if they exist #############
try:
    from _maxpriority import *                  # pickup set_realtime() function
except:
    def set_realtime():
        """Fake function definition.  Your system doesn't support the real function.
        """
        pass

def toggle_dout():
    """Toggle DOUT. NOT ENABLED ON YOUR SYSTEM.

    This is a platform dependent function, which is not implemented on
    your system."""
    pass

def set_dout(dummy_argument):
    """Set DOUT. NOT ENABLED ON YOUR SYSTEM.

    This is a platform dependent function, which is not implemented on
    your system."""
    pass

#if sys.platform != 'win32':
#    del win32_dout_state_global
    
if sys.platform == 'linux':
    try:
        # Try to override definition of dout functions:
        from _dout import *
    except:
        pass
elif sys.platform == 'win32':
    try:
        import winioport
        win32_dout_state_global = 0
        
        def toggle_dout():
            """Toggle DOUT.
            
            Win32 specific implementation: Toggles the lowest output
            bit of LPT0 (0x378)."""

            global win32_dout_state_global
            
            win32_dout_state_global = not win32_dout_state_global
            winioport.out(0x378,win32_dout_state_global)
        def set_dout(value):
            """Set DOUT.
            
            Win32 specific implementation: Sets the lowest output bit
            of LPT0 (0x378)."""
            
            win32_dout_state_global = value
            winioport.out(0x378,win32_dout_state_global)
        set_dout(win32_dout_state_global) # Initialize dout state
    except Exception, x:
#        print x
        pass
            
def linux_but_not_nvidia():
    """Called if platform is linux, but drivers not nvidia."""
    # If you've added support for other drivers to sync with VBL under
    # linux, please let the Vision Egg folks know how!
    print "VISIONEGG WARNING: Could not sync buffer swapping to"
    print "vertical blank pulse because you are running linux but not the"
    print "nVidia drivers.  It is quite possible this can be enabled, it's"
    print "just that I haven't had access to anything but nVidia cards under"
    print "linux!"
    
def sync_swap_with_vbl_pre_gl_init():
    """Synchronize buffer swapping and vertical retrace, if possible."""
    success = 0
    if sys.platform == "linux2":
        # Unfotunately, cannot check do glGetString(GL_VENDOR) to
        # check if drivers are nVidia because we have to do that requires
        # OpenGL context started, but this variable must be set
        # before OpenGL context started!
        
        # Assume drivers are nVidia
        VisionEgg.Core.add_gl_assumption("GL_VENDOR","nvidia",linux_but_not_nvidia)
        # Set nVidia linux environmental variable
        os.environ["__GL_SYNC_TO_VBLANK"] = "1"
        success = 1
        
    return success

def sync_swap_with_vbl_post_gl_init():
    """Synchronize buffer swapping and vertical retrace, if possible."""
    success = 0
    try:
        if sys.platform == "win32":
            import OpenGL.WGL.EXT.swap_control
            if OpenGL.WGL.EXT.swap_control.wglInitSwapControlARB(): # Returns 1 if it's working
                OpenGL.WGL.EXT.swap_control.wglSwapIntervalEXT(1) # Swap only at frame syncs
                if OpenGL.WGL.EXT.swap_control.wglGetSwapIntervalEXT() == 1:
                    success = 1
    except:
        pass
    
    return success
