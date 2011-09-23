from math import *
theta = pi/5.0
omega = (sqrt(5.0)+1.0)/2.0
omega1 = omega + 1.0
min  = 50

nodeowners = dict()
edgeowners = dict()

def dictoflist_append(d,key,value):
    if not d.has_key(key):
        d[key] = []
    d[key].append(value)

def dictofset_add(d,key,value):
    if not d.has_key(key):
        d[key] = set()
    d[key].add(value)

def coord2node(x,y):
    x = int(floor(x*10+0.5))
    y = int(floor(y*10+0.5))
    return x,y

def prolate(x,y,dir,size):
    x1   = size*cos(dir)
    y1   = size*sin(dir)
    x2   = size*cos(dir+theta)
    y2   = size*sin(dir+theta)
    if size<min:
        fill(0.1666,0.2,1)
        n0 = coord2node(x,y)
        beginpath(x,y)
        x+=x1
        y+=y1
        n1 = coord2node(x,y)
        lineto(x,y)
        x+=x2
        y+=y2
        n2 = coord2node(x,y)
        lineto(x,y)
        x-=x1
        y-=y1
        n3 = coord2node(x,y)
        lineto(x,y)
        x-=x2
        y-=y2
        endpath()
        e01 = frozenset((n0,n1))
        e12 = frozenset((n1,n2))
        e23 = frozenset((n2,n3))
        e30 = frozenset((n3,n0))
        tile = {"id":frozenset((e01,e12,e23,e30)),"node":(n0,n1,n2,n3),"type":"p"}
        dictofset_add(nodeowners,n0,e01)
        dictofset_add(nodeowners,n1,e12)
        dictofset_add(nodeowners,n2,e23)
        dictofset_add(nodeowners,n3,e30)
        dictofset_add(nodeowners,n0,e30)
        dictofset_add(nodeowners,n1,e01)
        dictofset_add(nodeowners,n2,e12)
        dictofset_add(nodeowners,n3,e23)
        dictoflist_append(edgeowners,e01,tile)
        dictoflist_append(edgeowners,e12,tile)
        dictoflist_append(edgeowners,e23,tile)
        dictoflist_append(edgeowners,e30,tile)
    else:
        oblate(x+x1,y+y1,dir+4*theta,size/omega1)
        oblate(x+x1,y+y1,dir+2*theta,size/omega1)
        prolate(x+x1+x2/omega,y+y1+y2/omega,dir+4*theta,size/omega1)
        prolate(x+x2,y+y2,dir+6*theta,size/omega1)
        oblate(x+x2/omega,y+y2/omega,dir+5*theta,size/omega1)


#fat tile
def oblate(x,y,dir,size):
    x1   = size*cos(dir)
    y1   = size*sin(dir)
    x2   = size*cos(dir+theta*2)
    y2   = size*sin(dir+theta*2)
    if size<min:
        fill(0,0.2,1)
        n0 = coord2node(x,y)
        beginpath(x,y)
        x+=x1
        y+=y1
        n1 = coord2node(x,y)
        lineto(x,y)
        x+=x2
        y+=y2
        n2 = coord2node(x,y)
        lineto(x,y)
        x-=x1
        y-=y1
        n3 = coord2node(x,y)
        lineto(x,y)
        x-=x2
        y-=y2
        endpath()
        e01 = frozenset((n0,n1))
        e12 = frozenset((n1,n2))
        e23 = frozenset((n2,n3))
        e30 = frozenset((n3,n0))
        tile = {"id":frozenset((e01,e12,e23,e30)),"node":(n0,n1,n2,n3),"type":"o"}
        dictofset_add(nodeowners,n0,e01)
        dictofset_add(nodeowners,n1,e12)
        dictofset_add(nodeowners,n2,e23)
        dictofset_add(nodeowners,n3,e30)
        dictofset_add(nodeowners,n0,e30)
        dictofset_add(nodeowners,n1,e01)
        dictofset_add(nodeowners,n2,e12)
        dictofset_add(nodeowners,n3,e23)
        dictoflist_append(edgeowners,e01,tile)
        dictoflist_append(edgeowners,e12,tile)
        dictoflist_append(edgeowners,e23,tile)
        dictoflist_append(edgeowners,e30,tile)
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
        
 

#receive set of edges and return them as a cycle.
def cycle(edges):
    edges2 = dict()
    for edge in edges:
        nodes = tuple(edge)
        if not edges2.has_key(nodes[0]):
            edges2[nodes[0]] = dict()
        edges2[nodes[0]][nodes[1]] = 1
        if not edges2.has_key(nodes[1]):
            edges2[nodes[1]] = dict()
        edges2[nodes[1]][nodes[0]] = 1
    nodes = edges2.keys()
    start = nodes[0]
    cycle = []
    while True:
        nexts = edges2[start].keys()
        if len(nexts) == 0:
            break
        cycle.append(start)
        next  = nexts[0]
        del(edges2[next][start])
        del(edges2[start][next])
        start = next
    return cycle
        


def lookup_Q():
    Q = []
    for node in nodeowners:
        if len(nodeowners[node]) == 3:
            n = {"p":0, "o":0}
            ok = True
            edges = set()
            for edge in nodeowners[node]:
                if len(edgeowners[edge]) == 2:
                    n[edgeowners[edge][0]["type"]]+=1
                    n[edgeowners[edge][1]["type"]]+=1
                    #print edgeowners[edge][0]["id"]
                    edges |= edgeowners[edge][0]["id"]
                    edges |= edgeowners[edge][1]["id"]
                else:
                    ok = False
            if ok and n["p"] == 4 and n["o"] == 2:
                for edge in nodeowners[node]:
                    tiletype[edgeowners[edge][0]["node"]] = "Q"
                    tiletype[edgeowners[edge][1]["node"]] = "Q"            
                edges -= nodeowners[node]
                #print edges
                perimeter = cycle(edges)
                strokewidth(4)
                fill(0.333,0.5,1)
                beginpath(perimeter[0][0]/10,perimeter[0][1]/10)
                for i in range(1,len(perimeter)):
                    lineto(perimeter[i][0]/10,perimeter[i][1]/10)
                endpath()
                Q.append(perimeter)
    return Q



def lookup_K():
    K = []
    for node in nodeowners:
        if len(nodeowners[node]) == 4:
            n = {"p":0, "o":0}
            ok = True
            edges = set()
            for edge in nodeowners[node]:
                if len(edgeowners[edge]) == 2:
                    n[edgeowners[edge][0]["type"]]+=1
                    n[edgeowners[edge][1]["type"]]+=1
                    #print edgeowners[edge][0]["id"]
                    edges |= edgeowners[edge][0]["id"]
                    edges |= edgeowners[edge][1]["id"]
                    if tiletype.has_key(edgeowners[edge][0]["node"]):
                        ok = False
                    if tiletype.has_key(edgeowners[edge][1]["node"]):
                        ok = False
                else:
                    ok = False
            if ok and n["p"] == 2 and n["o"] == 6:
                for edge in nodeowners[node]:
                    tiletype[edgeowners[edge][0]["node"]] = "K"
                    tiletype[edgeowners[edge][1]["node"]] = "K"            
                edges -= nodeowners[node]
                #print edges
                perimeter = cycle(edges)
                strokewidth(4)
                fill(0.666,0.5,1)
                beginpath(perimeter[0][0]/10,perimeter[0][1]/10)
                for i in range(1,len(perimeter)):
                    lineto(perimeter[i][0]/10,perimeter[i][1]/10)
                endpath()
                K.append(perimeter)
    return K



def lookup_S():
    S = []
    for node in nodeowners:
        if len(nodeowners[node]) == 5:
            n = {"p":0, "o":0}
            ok = True
            edges = set()
            for edge in nodeowners[node]:
                if len(edgeowners[edge]) == 2:
                    n[edgeowners[edge][0]["type"]]+=1
                    n[edgeowners[edge][1]["type"]]+=1
                    #print edgeowners[edge][0]["id"]
                    edges |= edgeowners[edge][0]["id"]
                    edges |= edgeowners[edge][1]["id"]
                    if tiletype.has_key(edgeowners[edge][0]["node"]):
                        ok = False
                    if tiletype.has_key(edgeowners[edge][1]["node"]):
                        ok = False
                else:
                    ok = False
            if ok and n["p"] == 0 and n["o"] == 10:
                for edge in nodeowners[node]:
                    tiletype[edgeowners[edge][0]["node"]] = "S"
                    tiletype[edgeowners[edge][1]["node"]] = "S"            
                edges -= nodeowners[node]
                #print edges
                #register the shape of the QKStile
                perimeter = cycle(edges)
                strokewidth(4)
                fill(1,0.5,1)
                beginpath(perimeter[0][0]/10,perimeter[0][1]/10)
                for i in range(1,len(perimeter)):
                    lineto(perimeter[i][0]/10,perimeter[i][1]/10)
                endpath()
                S.append(perimeter)
    return S
