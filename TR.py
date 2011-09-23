from math import *
theta = pi/5.0
omega = (sqrt(5.0)+1.0)/2.0
omega1 = omega + 1.0


def rint(x):
    return int(floor(x+0.5))

def go(pos,dir,dist):
    delta = rint(dist*cos(dir*theta)),rint(dist*sin(dir*theta))
    return pos[0]+delta[0],pos[1]+delta[1]
    

def hexagon(pos,dir,dist):
    p1 = go(pos,dir+1,dist)
    p2 = go(p1,dir,dist)
    p3 = go(p2,dir-1,dist)
    p4 = go(p3,dir-4,dist)
    p5 = go(p4,dir-5,dist)
    return pos,p1,p2,p3,p4,p5

def rhomb(pos,dir,dist):
    p1 = go(pos,dir+1,dist)
    p2 = go(p1,dir-1,dist)
    p3 = go(p2,dir-4,dist)
    return pos,p1,p2,p3


def drawpoly(poly):
    beginpath(poly[0][0]/10,poly[0][1]/10)
    for p in poly:
        lineto(p[0]/10,p[1]/10)
    endpath()

def star(pos,dir,siz):
    p = []
    p0 =go(pos,dir+5,siz)
    p.append(p0)
    for i in range(0,10,2):
        p0 = go(p0,dir-3+i,siz)
        p.append(p0)
        p0 = go(p0,dir-0+i,siz)
        p.append(p0)
    return tuple(p)


def decagon(pos,siz):
    p = []
    p0 =go(pos,0,siz*omega)
    p.append(p0)
    for i in range(0,10):
        p0 = go(p0,i+3,siz)
        p.append(p0)
    return tuple(p)


def decohex(hex,dir,siz):
    polygons[("s",dir,hex[0])]= star(hex[0],dir,siz)
    polygons[("s",dir,hex[2])]= star(hex[2],dir,siz)
    polygons[("s",dir,hex[4])]= star(hex[4],dir,siz)
    polygons[("d",dir,hex[1])]= decagon(hex[1],siz)
    polygons[("d",dir,hex[3])]= decagon(hex[3],siz)
    polygons[("d",dir,hex[5])]= decagon(hex[5],siz)
    decagonpairs[(hex[1],hex[5])] = (dir,hex[0])

siz = 1000
origin = siz,siz

hex1 = hexagon(origin,0,siz)
hex2 = hexagon(hex1[2],0,siz)
polygons = dict()
decagonpairs = dict()
decohex(hex1,0,siz/omega1)
decohex(hex2,0,siz/omega1)

stroke(0)
nofill()
drawpoly(hex1)
drawpoly(hex2)
for poly in polygons.values():
    drawpoly(poly)


    