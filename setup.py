#!/usr/bin/env python3

"""(Elmitec) LEEM image file viewer.

Displays LEEM images and meta data stored by UView2002.
"""

from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

current_path = path.abspath(path.dirname(__file__))
with open(path.join(current_path, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
    
setup(
    name='ldisp',
    version='0.1',
    description='LEEM image viewer',
    long_description=long_description,
    #url=TODO,
    author='Jan Höcker',
    license='GPLv3',
    packages=['ldisp'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science',
        'Topic :: Scientific/Engineering :: Visualization',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3'
        ],
    keywords='LEEM Science Image Viewer',
    entry_points={"gui_scripts": ["ldisp = ldisp.ldisp:main"]}   
    ) 
        
    
