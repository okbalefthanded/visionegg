#!/usr/bin/env python
#
# This is the python source code for a little app that lets you
# test various aspects of texturing in OpenGL.
#
# It is part of the Vision Egg package.
#
# Copyright (c) 2002 Andrew Straw.  Distributed under the terms of the
# GNU General Public License (GPL).

import string
__version__ = string.split('$Revision$')[1]
__date__ = string.join(string.split('$Date$')[1:3], ' ')
__author__ = 'Andrew Straw <astraw@users.sourceforge.net>'

import time

import pygame
from pygame.locals import *

from OpenGL.GL import * # PyOpenGL packages
from Numeric import *
import Tkinter

import VisionEgg.Core
import VisionEgg.GUI
import VisionEgg.Textures

class TextureTestFrame(VisionEgg.GUI.AppWindow):
    def __init__(self,master=None,**cnf):
        apply(VisionEgg.GUI.AppWindow.__init__,(self,master),cnf)
        self.winfo_toplevel().title('Vision Egg - Texture Test')

        self.tex_compression = Tkinter.BooleanVar()
        self.tex_compression.set(VisionEgg.config.VISIONEGG_TEXTURE_COMPRESSION)
        Tkinter.Checkbutton(self,
                            text="Texture compression",
                            variable=self.tex_compression,
                            command=self.set_tex_compression).pack()

        Tkinter.Label(self,text="Texture width:").pack()
        self.tex_width = Tkinter.StringVar()
        self.tex_width.set("512")
        Tkinter.OptionMenu(self,self.tex_width,"1","2","4","8","16","32","64","128","256","512","1024","2048","4096").pack()

        Tkinter.Label(self,text="Texture height:").pack()
        self.tex_height = Tkinter.StringVar()
        self.tex_height.set("512")
        Tkinter.OptionMenu(self,self.tex_height,"1","2","4","8","16","32","64","128","256","512","1024","2048","4096").pack()

        Tkinter.Label(self,text="image file to use as texture:").pack()
        self.image_file = Tkinter.StringVar()
        self.image_file.set("(none - generate own)")
        Tkinter.Entry(self,textvariable=self.image_file).pack()

        Tkinter.Button(self,text="do glTexSubImage2D ('blit') speed test",command=self.do_blit_speed).pack()
        Tkinter.Button(self,text="get maximum number of resident textures",command=self.do_resident_textures).pack()

    def do_blit_speed(self):
        glEnable( GL_TEXTURE_2D )
        print "Using texture from file: %s (Not really, yet)"%self.image_file.get()
        
        tex1 = VisionEgg.Textures.Texture(size=(int(self.tex_width.get()),int(self.tex_height.get())))
        tex_id = tex1.load() # initialize the original texture
        tex_buf = tex1.get_texture_buffer()

        # show the texture first
        VisionEgg.Core.OrthographicProjection().set_GL_projection_matrix()
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClear(GL_COLOR_BUFFER_BIT)
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, tex1.buf_bf)
        glVertex3f(-1.0,-1.0,-6.0)
        glTexCoord2f(1.0, tex1.buf_bf)
        glVertex3f(1.0,-1.0,-6.0)
        glTexCoord2f(1.0, tex1.buf_tf)
        glVertex3f(1.0,1.0,-6.0)
        glTexCoord2f(0.0, tex1.buf_tf)
        glVertex3f(-1.0,1.0,-6.0)
        glEnd()
        VisionEgg.Core.swap_buffers()

        texture_dest = tex1.get_texture_buffer()
        texture_source = tex1.get_pil_image()

        num = 10
        start = time.time()
        for i in range(num):
            print "BROKEN!!!"
#            texture_dest.put_sub_image(texture_source,(0,0),(texture_source.size[0],texture_source.size[1]))
        stop = time.time()

        print "Did %d calls to glTexSubImage2D in %f seconds."%(num,stop-start)
        
        print "blit speed=(BROKEN)"
        tex_buf.free()

    def do_resident_textures(self):
        glEnable( GL_TEXTURE_2D )
        print "Using texture from file: %s (Not really, yet)"%self.image_file.get()
        orig =  VisionEgg.Textures.Texture(size=(int(self.tex_width.get()),int(self.tex_height.get()))) 

        texs = []
        tex_ids = []
        tex_bufs = []
        
        done = 0
        counter = 0
        while not done:
            counter = counter + 1
            tex_ids.append( orig.load() ) 
            tex_bufs.append( orig.get_texture_buffer() )

            answers = glAreTexturesResident( tex_ids )
            if type(answers) != type([1,2]): # in the case of 1 tex_id, result is a scalar
                answers = [answers] # make a list of len(1)
            answers = array(answers) # make NumPy array
            num_res = sum(sum(answers))
            if num_res < (len(tex_ids)-1): # For some reason, one texture always reported non-resident
                done = 1 
            max_within_reason = 51
            if counter > max_within_reason:
                print "Stopping glAreTexturesResident() test -- Over %d textures are reported resident!"%max_within_reason
                done = 1
        if not counter > max_within_reason:
            print "%d textures were reported resident, but %d were not."%(counter-1,counter)
        for buf in tex_bufs:
            buf.free()

    def set_tex_compression(self):
        """Callback for tick button"""
        VisionEgg.config.VISIONEGG_TEXTURE_COMPRESSION = self.tex_compression.get()
        self.update()
        self.info_frame.update()
    
if __name__ == '__main__':
    screen = VisionEgg.Core.get_default_screen()
    
    app = TextureTestFrame()
    app.pack()
    app.mainloop()

