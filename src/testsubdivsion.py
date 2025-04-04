#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# testsubdivision.py -- test code for visualizing hex subdivision using yapCAD
# NOTE: this depends on the output of makegeom.js being run first, producing
# foo.json as the output

import json

from yapcad.ezdxf_drawable import *
from yapcad.pyglet_drawable import *
from yapcad.geom import *

#set up openGL rendering
def setupGL():
    dGl =pygletDraw()
    dGl.magnify = 1.0
    dGl.linecolor = 'white'
    dGl.cameradist = 25
    return dGl

#set up DXF rendering
def setupDXF():
    d=ezdxfDraw()
    filename="subdivision-out"
    print("\nOutput file name is {}.dxf".format(filename))
    d.filename = filename
    return d

## Draw some documentary text using the specified drawable.
## Text in the OpenGL rendering isn't working very well yet.

def legend(d):

    d.draw_text("X5 subdivision", point(5,15),\
                attr={'style': 'OpenSans-Bold', # style for ezdxf
                      'font_name': 'OpenSans', # style for pyglet
                      'bold': True, # style for pyglet
                      'height': 2.0})
    d.draw_text("test.py",
                point(5,12))

    d.draw_text("hex subdivision test",
                point(5,10))

def drawGlist(glist,d):

    ## render the point
    d.pointstyle = 'xo' # set the point rendering style
    d.linecolor = 1 # set color to red (DXF index color)
    d.draw(glist)


def geometry():
    geom = []
    with open('foo.json') as f:
        data = json.load(f)
        print(f"length of data: {len(data)}")
        for tri in data:
            print(f"tri: {tri}")
            p1 = point(tri[0]['x'],tri[0]['y'])
            p2 = point(tri[1]['x'],tri[1]['y'])
            p3 = point(tri[2]['x'],tri[2]['y'])
            poly = [ p1, p2, p3, p1 ]
            geom.append(poly)

    print(f"length of geom: {len(geom)}")
    geom = scale(geom,10.0)
    return geom

if __name__ == "__main__":

    ## setup DXF rendering
    d= setupDXF()

    ## setup OpenGL rendering
    dGl = setupGL()

    ## make the geometry
    geomlist = geometry()

    d.layer= '0'
    d.pointstyle = 'xo' # set the point rendering style
    geo = []
    up=point(0,0,0.3)
    for i in range(0,6):
        geo.append(geomlist[i])
    d.linecolor='white'
    d.draw(geo)
    dGl.linecolor='white'
    dGl.draw(geo)
    geo = []
    for i in range(6,31):
        geo.append(geomlist[i])
    d.linecolor='yellow'
    d.draw(geo)
    dGl.linecolor='yellow'
    d.draw(geo)
    dGl.draw(translate(geo,up))
    geo = []
    up=point(0,0,0.6)
    for i in range(31,126):
        geo.append(geomlist[i])
    d.linecolor='red'
    d.draw(geo)
    dGl.linecolor='red'
    d.draw(geo)
    dGl.draw(translate(geo,up))

    ## draw the geometry in DXF
    #drawGlist(geomlist,d)

    ## add a dawing legend on the DXF drawing, in the DOCUMENTATION
    ## layer

    d.layer = 'DOCUMENTATION'
    d.linecolor = 256 ## set layer default color
    legend(d)

    ## add a drawing legend in the OpenGL rendering, setting the
    ## color eplicitly to yellow

    dGl.linecolor = 'yellow'
    legend(dGl)

    ## draw the geometry in OpenGL
    drawGlist(geomlist,dGl)

    ## write out the DXF file as example1-out.dxf
    d.display()

    ## create the interactive OpenGL rendering -- do this last
    dGl.display()
