#inflation
from math import *
theta = pi/5.0
omega = (sqrt(5.0)+1.0)/2.0
omega1 = omega + 1.0
min  = 80
def prolate(x,y,dir,size):
    x1   = size*cos(dir)
    y1   = size*sin(dir)
    x2   = size*cos(dir+theta)
    y2   = size*sin(dir+theta)
    if size<min:
        fill(0.1666,0.5,1)
        beginpath(x,y)
        x+=x1
        y+=y1
        lineto(x,y)
        x+=x2
        y+=y2
        lineto(x,y)
        x-=x1
        y-=y1
        lineto(x,y)
        x-=x2
        y-=y2
        endpath()
    else:
        oblate(x+x1,y+y1,dir+4*theta,size/omega1)
        oblate(x+x1,y+y1,dir+2*theta,size/omega1)
        prolate(x+x1+x2/omega,y+y1+y2/omega,dir+4*theta,size/omega1)
        prolate(x+x2,y+y2,dir+6*theta,size/omega1)
        oblate(x+x2/omega,y+y2/omega,dir+5*theta,size/omega1)


def oblate(x,y,dir,size):
    x1   = size*cos(dir)
    y1   = size*sin(dir)
    x2   = size*cos(dir+theta*2)
    y2   = size*sin(dir+theta*2)
    if size<min:
        fill(0,0.5,1)
        beginpath(x,y)
        x+=x1
        y+=y1
        lineto(x,y)
        x+=x2
        y+=y2
        lineto(x,y)
        x-=x1
        y-=y1
        lineto(x,y)
        x-=x2
        y-=y2
        endpath()
    else:
        x12 = x1+x2
        y12 = y1+y2
        oblate(x,y,dir+theta,size/omega1)
        prolate(x+x1/omega,y+y1/omega,dir+3*theta,size/omega1)
        prolate(x+x1,y+y1,dir+2*theta,size/omega1)
        oblate(x+x1+x2/omega1,y+y1+y2/omega1,dir+theta,size/omega1)
        oblate(x+x12/omega1,y+y12/omega1,dir-2*theta,size/omega1)
        oblate(x+x12/omega1,y+y12/omega1,dir-0*theta,size/omega1)
        oblate(x+x12/omega1,y+y12/omega1,dir+2*theta,size/omega1)
        prolate(x+2*x12/omega1,y+2*y12/omega1,dir+4*theta,size/omega1)
        
 


stroke(0)
strokewidth(0.5)
colormode(HSB)
size(1000,1000)
oblate(500,500,0*theta,700)
oblate(500,500,2*theta,700)
oblate(500,500,4*theta,700)
oblate(500,500,6*theta,700)
oblate(500,500,8*theta,700)
