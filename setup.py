#!/usr/bin/env python
"""Setup script for the Vision Egg distribution.
"""
# Copyright (c) 2001-2002 Andrew Straw.  Distributed under the terms of the
# GNU Lesser General Public License (LGPL).

# On Mac OS X, you can eliminate the need for the C compiler if you
# set this line to 1.  Of course, that also gets rid of the Vision
# Egg's ability to schedule itself as a real time application.
    
skip_c_compilation = 0

from distutils.core import setup, Extension
import sys
import os.path

# Normal distutils stuff
name="visionegg"
version = "0.9.2"
description = "Vision Egg"
url = 'http://www.visionegg.org/'
author = "Andrew Straw"
author_email = "astraw@users.sourceforge.net"
license = "LGPL"
package_dir={'VisionEgg' : 'src'}
packages=[ 'VisionEgg' ]
ext_package='VisionEgg'
ext_modules = []
long_description = """
The Vision Egg is a programming library (with demo applications) that
uses standard, inexpensive computer graphics cards to produce visual
stimuli for vision research experiments."""

# Fill out ext_modules
if not skip_c_compilation:
    ext_modules.append(Extension(name='_maxpriority',sources=['src/_maxpriority.c']))

if sys.platform == "darwin" and not skip_c_compilation:
    ext_modules.append(Extension(name='_darwin_sync_swap',
                                sources=['src/_darwin_sync_swap.m'],
                                include_dirs=['/System/Library/Frameworks/OpenGL.framework/Headers',
                                              '/System/Library/Frameworks/Cocoa.framework/Headers',
                                              ],
                                extra_link_args=['-framework','OpenGL'],
                                ))

if sys.platform == 'linux2' and not skip_c_compilation:
    ext_modules.append(Extension(name='_raw_lpt_linux',sources=['src/_raw_lpt_linux.c']))

if sys.platform[:4] == 'irix' and not skip_c_compilation:
    ext_modules.append(Extension(name='_raw_plp_irix',sources=['src/_raw_plp_irix.c']))

# Fill out data_files
def visit_script_dir(scripts, dirname, filenames):
    for filename in filenames:
        if filename[-3:] == '.py':
            if filename != '__init__.py':
                scripts.append(os.path.join(dirname,filename))

def gather_scripts():
    scripts = []
    os.path.walk('demo',visit_script_dir,scripts)
    os.path.walk('test',visit_script_dir,scripts)
    return scripts

def organize_script_dirs(scripts):
    scripts_by_dir = {}
    for script in scripts:
        dirname = os.path.join('VisionEgg',os.path.split(script)[0])
        if dirname not in scripts_by_dir.keys():
            scripts_by_dir[dirname] = []
        scripts_by_dir[dirname].append(script)
    organized = []
    for dirname in scripts_by_dir.keys():
        organized.append( (dirname, scripts_by_dir[dirname]) )
    return organized

scripts = gather_scripts()
data_files = organize_script_dirs(scripts)
data_files.append( ('VisionEgg/data',['data/panorama.jpg']) )
data_files.append( ('VisionEgg/demo',['demo/README.txt']) )
data_files.append( ('VisionEgg/demo/calibrate',['demo/calibrate/README.txt']) )
data_files.append( ('VisionEgg/demo/tcp',['demo/tcp/README.txt']) )
data_files.append( ('VisionEgg',['check-config.py','VisionEgg.cfg','README.txt','LICENSE.txt']) )

def main():
    # Normal distutils stuff
    setup(name=name,
          version = version,
          description = description,
          url = url,
          author = author,
          author_email = author_email,
          license = license,
          package_dir=package_dir,
          packages=packages,
          ext_package=ext_package,
          ext_modules=ext_modules,
          data_files = data_files,
          long_description = long_description 
          )
    
    

if __name__ == "__main__":
    main()





