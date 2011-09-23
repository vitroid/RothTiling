#inflation
#QKS tiling
#macro structure
from math import *
theta = pi/5.0
omega = (sqrt(5.0)+1.0)/2.0
omega1 = omega + 1.0
min  = 50


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

def prolate(x,y,dir,size,nodeowners,edgeowners):
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
        oblate(x+x1,y+y1,dir+4*theta,size/omega1,nodeowners,edgeowners)
        oblate(x+x1,y+y1,dir+2*theta,size/omega1,nodeowners,edgeowners)
        prolate(x+x1+x2/omega,y+y1+y2/omega,dir+4*theta,size/omega1,nodeowners,edgeowners)
        prolate(x+x2,y+y2,dir+6*theta,size/omega1,nodeowners,edgeowners)
        oblate(x+x2/omega,y+y2/omega,dir+5*theta,size/omega1,nodeowners,edgeowners)


#fat tile
def oblate(x,y,dir,size,nodeowners,edgeowners):
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
        oblate(x,y,dir+theta,size/omega1,nodeowners,edgeowners)
        prolate(x+x1/omega,y+y1/omega,dir+3*theta,size/omega1,nodeowners,edgeowners)
        prolate(x+x1,y+y1,dir+2*theta,size/omega1,nodeowners,edgeowners)
        oblate(x+x1+x2/omega1,y+y1+y2/omega1,dir+theta,size/omega1,nodeowners,edgeowners)
        oblate(x+x12/omega1,y+y12/omega1,dir-2*theta,size/omega1,nodeowners,edgeowners)
        oblate(x+x12/omega1,y+y12/omega1,dir-0*theta,size/omega1,nodeowners,edgeowners)
        oblate(x+x12/omega1,y+y12/omega1,dir+2*theta,size/omega1,nodeowners,edgeowners)
        prolate(x+2*x12/omega1,y+2*y12/omega1,dir+4*theta,size/omega1,nodeowners,edgeowners)
        
 

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
        

def drawpoly(polygon):
    beginpath(polygon[0][0]/10,polygon[0][1]/10)
    for i in range(1,len(polygon)):
        lineto(polygon[i][0]/10,polygon[i][1]/10)
    endpath()

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
                drawpoly(perimeter)
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
                drawpoly(perimeter)
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
                drawpoly(perimeter)
                S.append(perimeter)
    return S
                



stroke(0)
strokewidth(0.5)
colormode(HSB)
size(1000,1000)
nodeowners = dict()
edgeowners = dict()
oblate(500,500,0*theta,400,nodeowners,edgeowners)
oblate(500,500,2*theta,400,nodeowners,edgeowners)
oblate(500,500,4*theta,400,nodeowners,edgeowners)
oblate(500,500,6*theta,400,nodeowners,edgeowners)
oblate(500,500,8*theta,400,nodeowners,edgeowners)

def vector2angle(v):
    x = float(v[0])
    y = float(v[1])
    angle = atan(y/x)
    if x < 0:
        angle += pi
    angle /= theta
    iangle = int(floor(angle+0.5))
    iangle %= 10
    return iangle



tiletype = dict()
Q = lookup_Q()
K = lookup_K()
S = lookup_S()
QKSnodeowners = dict()
QKSedgeowners = dict()



for polygon in Q:
    edges = []
    dirs = []
    for i in range(0,len(polygon)):
        edge = (polygon[i-1],polygon[i])
        dir = vector2angle((polygon[i][0]-polygon[i-1][0],polygon[i][1]-polygon[i-1][1]))
        dirs.append(dir)
        edges.append(edge)
        dictofset_add(QKSnodeowners,polygon[i],edge)
        dictofset_add(QKSnodeowners,polygon[i-1],edge)
    dir = 0
    for i in range(0,len(dirs)):
        delta = dirs[i] - dirs[i-1]
        delta = (delta + 15) % 10 - 5
        dir += delta
    if dir < 0:
        #perimeters should be clockwise
        polygon.reverse()
        edges.reverse()
        for i in range(len(edges)):
            edges[i] = (edges[i][1],edges[i][0])
    QKStile = {"id":tuple(edges),"node":tuple(polygon),"type":"Q"}
    for edge in edges:
        dictoflist_append(QKSedgeowners,frozenset(edge),QKStile)
for polygon in K:
    edges = []
    dirs = []
    for i in range(0,len(polygon)):
        edge = (polygon[i-1],polygon[i])
        dir = vector2angle((polygon[i][0]-polygon[i-1][0],polygon[i][1]-polygon[i-1][1]))
        dirs.append(dir)
        edges.append(edge)
        dictofset_add(QKSnodeowners,polygon[i],edge)
        dictofset_add(QKSnodeowners,polygon[i-1],edge)
    dir = 0
    for i in range(0,len(dirs)):
        delta = dirs[i] - dirs[i-1]
        delta = (delta + 15) % 10 - 5
        dir += delta
    if dir < 0:
        #perimeters should be clockwise
        polygon.reverse()
        edges.reverse()
        for i in range(len(edges)):
            edges[i] = (edges[i][1],edges[i][0])
    QKStile = {"id":tuple(edges),"node":tuple(polygon),"type":"K"}
    for edge in edges:
        dictoflist_append(QKSedgeowners,frozenset(edge),QKStile)
for polygon in S:
    edges = []
    dirs = []
    for i in range(0,len(polygon)):
        edge = (polygon[i-1],polygon[i])
        dir = vector2angle((polygon[i][0]-polygon[i-1][0],polygon[i][1]-polygon[i-1][1]))
        dirs.append(dir)
        edges.append(edge)
        dictofset_add(QKSnodeowners,polygon[i],edge)
        dictofset_add(QKSnodeowners,polygon[i-1],edge)
    dir = 0
    for i in range(0,len(dirs)):
        delta = dirs[i] - dirs[i-1]
        delta = (delta + 15) % 10 - 5
        dir += delta
    if dir < 0:
        #perimeters should be clockwise
        polygon.reverse()
        edges.reverse()
        for i in range(len(edges)):
            edges[i] = (edges[i][1],edges[i][0])
    QKStile = {"id":tuple(edges),"node":tuple(polygon),"type":"S"}
    for edge in edges:
        dictoflist_append(QKSedgeowners,frozenset(edge),QKStile)

#for edge in QKSedgeowners:
#    print edge, QKSedgeowners[edge]

#次に、edgeを、始点と角度と終点で整理する。

QKSedges = dict()
QKSnodes = dict()
for edge in QKSedgeowners:
    vec = tuple(edge)
    x = vec[1][0] - vec[0][0]
    y = vec[1][1] - vec[0][1]
    QKSnodes[vec[0]] = 1
    QKSnodes[vec[1]] = 1
    dir = vector2angle((x,y))
    if not QKSedges.has_key(vec[0]):
        QKSedges[vec[0]] = dict()
    if not QKSedges.has_key(vec[1]):
        QKSedges[vec[1]] = dict()
    QKSedges[vec[0]][dir] = vec[1]
    QKSedges[vec[1]][(dir + 5)%10] = vec[0]
    #print vec[1],(dir+5)%10,vec[0]


def lookup_seq(node,seq):
    if len(seq) == 0:
        return node
    car = seq[0]
    cdr = seq[1:len(seq)]
    #print car,cdr
    if QKSedges[node].has_key(car):
        return lookup_seq(QKSedges[node][car],cdr)
    else:
        return ()


def lookup_and_register(seq):
    for node in QKSnodes:
        endnode = lookup_seq(node,seq)
        if len(endnode):
            if not macroedges.has_key(node):
                macroedges[node] = dict()
            macroedges[node][seq] = endnode

def add_and_register(seq1,seq2):
    for node in QKSnodes:
        if macroedges.has_key(node) and macroedges[node].has_key(seq1):
            endnode = macroedges[node][seq1]
            if len(endnode):
                if macroedges.has_key(endnode) and macroedges[endnode].has_key(seq2):
                    endnode = macroedges[endnode][seq2]
                    if not macroedges.has_key(node):
                        macroedges[node] = dict()
                    macroedges[node][seq1+seq2] = endnode

macroedges = dict()
L1 = (1,0,9,8,9,0)
for node in QKSnodes:
    #L1
    endnode = lookup_seq(node,L1)
    if len(endnode):
        #print node,endnode
        dx = endnode[0] - node[0]
        dy = endnode[1] - node[1]
        stroke(0,1,1)
        line(node[0]/10,node[1]/10, (node[0]+dx*0.9)/10,(node[1]+dy*0.9)/10)
        if not macroedges.has_key(node):
            macroedges[node] = dict()
        macroedges[node][L1] = endnode
L7 = (7,8,9,8,7,6)
for node in QKSnodes:
    endnode = lookup_seq(node,L7)
    if len(endnode):
        #print node,endnode
        dx = endnode[0] - node[0]
        dy = endnode[1] - node[1]
        stroke(0.6666,1,1)
        line(node[0]/10,node[1]/10, (node[0]+dx*0.9)/10,(node[1]+dy*0.9)/10)
        if not macroedges.has_key(node):
            macroedges[node] = dict()
        macroedges[node][L7] = endnode

S1  = (1,0,9,8)
lookup_and_register(S1)

SL1 = S1+L1 #(1,0,9,8,1,0,9,8,9,0)
add_and_register(S1,L1)

S9 = (9,8,7,6)
lookup_and_register(S9)

LS7 = L7 + S9 #(7,8,9,8,7,6,9,8,7,6)
add_and_register(L7,S9)

add_and_register(L7,L7)
add_and_register(L1,L1)
add_and_register(L7,LS7)
add_and_register(L1,SL1)

def parallelogram(seq1,seq2):
    Pnodes = []
    for node in QKSnodes:
        if macroedges.has_key(node):
            if macroedges[node].has_key(seq1) and macroedges[node].has_key(seq2):
                next1 = macroedges[node][seq1]
                next2 = macroedges[node][seq2]
                if macroedges.has_key(next1) and macroedges.has_key(next2):
                    if macroedges[next1].has_key(seq2) and macroedges[next2].has_key(seq1):
                    #if macroedges.has_key(next) and macroedges[next].has_key(seq1):
                        Pnodes.append(node)
                        dx1 = macroedges[node][seq1][0] - node[0]
                        dy1 = macroedges[node][seq1][1] - node[1]
                        dx2 = macroedges[node][seq2][0] - node[0]
                        dy2 = macroedges[node][seq2][1] - node[1]
                        stroke(0)
                        fill(0.16666,0.5,1,0.5)
                        beginpath(node[0]/10,node[1]/10)
                        lineto((node[0]+dx1)/10, (node[1]+dy1)/10)
                        lineto((node[0]+dx1+dx2)/10, (node[1]+dy1+dy2)/10)
                        lineto((node[0]+dx2)/10, (node[1]+dy2)/10)
                        endpath()
    return Pnodes
#あとはLとLSの組みあわせで菱形を定義する。
horiz,vert = S1,S9
#horiz,vert = SL1,LS7
#horiz,vert = L1+SL1,L7+LS7
#horiz,vert = L1+L1,L7+L7
#horiz,vert = L1,L7

Pnodes = parallelogram(horiz, vert)

#菱形(といっても境界は波波)の内側にあるQKSタイルを抽出する。
#この場合、境界に重ならず明らかに内部にある多角形をまず抽出する。
#境界辺に接する場合は、辺のオーナーのうちどちらが内側かを判別し、外部のものを除外する。
#この境界処理が最大の難関になりそう。
#境界については、QKSタイルを全部時計周りに描いておけば、判別は簡単になる。

progress = dict()
queue    = []

#まず周縁ベクトルを正しい方向で辞書に入れる。辞書の値はFalseとしておく。
def register_peri(node, seq):
    #print seq
    for dir in seq:
        #print node,dir,QKSedges[node]
        #fill(0)
        #stroke(0)
        #oval(405-10,500-10,20,20)
        next = QKSedges[node][dir]
        progress[(node,next)] = False
        queue.append((node,next))
        node = next
    return node

#方向の列を完全に反転させる
def invert(seq):
    newseq = []
    for dir in seq:
        newseq.append((dir+5)%10)
    newseq.reverse()
    return newseq


def drawA(atoms,pos):
    atoms[pos] = "A"
    x = pos[0]/10
    y = pos[1]/10
    strokewidth(2)
    stroke(0)
    fill(1,0,1)
    oval(x-3,y-3,6,6)

def drawB(atoms,pos):
    atoms[pos] = "B"
    x = pos[0]/10
    y = pos[1]/10
    strokewidth(1)
    stroke(0)
    fill(0)
    oval(x-3,y-3,6,6)


def drawX(atoms,pos):
    atoms[pos] = "X"
    x = pos[0]/10
    y = pos[1]/10
    strokewidth(1)
    stroke(0)
    fill(1,0,1)
    oval(x-3,y-3,6,6)
    nostroke()
    fill(0)
    oval(x-2,y-2,4,4)



def decorate_triangle(atoms,a,b,c):
    cx = (b[0] + c[0])/2
    cy = (b[1] + c[1])/2
    cx = (a[0] + cx*3) / 4
    cy = (a[1] + cy*3) / 4
    drawB(atoms,(cx,cy))

def decorate_fan(atoms,c,p):
    if len(p) == 5:
        r = range(-1,len(p)-1)
    else:
        r = range(0,len(p)-1)
    for i in r:
        cx = (c[0]*2 + p[i][0]*3 + p[i+1][0]*3)/8
        cy = (c[1]*2 + p[i][1]*3 + p[i+1][1]*3)/8
        drawA(atoms,(cx,cy))
    for point in p:
        cx = (c[0] + point[0])/2
        cy = (c[1] + point[1])/2
        drawB(atoms,(cx,cy))

def decorate_square(atoms,a,b,c,d):
    cx = (a[0]*3 + b[0]*3 + c[0]*1 + d[0]*1)/8
    cy = (a[1]*3 + b[1]*3 + c[1]*1 + d[1]*1)/8
    drawB(atoms,(cx,cy))
    cx = (a[0]*1 + b[0]*1 + c[0]*3 + d[0]*3)/8
    cy = (a[1]*1 + b[1]*1 + c[1]*3 + d[1]*3)/8
    drawB(atoms,(cx,cy))
    cx = (a[0]*1 + b[0]*4 + c[0]*4 + d[0]*1)/10
    cy = (a[1]*1 + b[1]*4 + c[1]*4 + d[1]*1)/10
    drawA(atoms,(cx,cy))
    cx = (a[0]*4 + b[0]*1 + c[0]*1 + d[0]*4)/10
    cy = (a[1]*4 + b[1]*1 + c[1]*1 + d[1]*4)/10
    drawA(atoms,(cx,cy))
    

def decorate_Q(atoms,edges):
    #まず、最も尖っている(+3曲がる)頂点をさがし、それを基準にdecorateする。
    seq = []
    for edge in edges:
        dir = vector2angle((edge[1][0]-edge[0][0],edge[1][1]-edge[0][1]))
        seq.append(dir)
    origin = -1
    for i in range(len(seq)):
        if (seq[i]-seq[i-1]+10)%10 == 3:
            origin = i
    #shift the edge order
    newedges = edges+edges
    newedges = newedges[origin:origin+len(edges)]
    for i in range(6):
        drawX(atoms,newedges[i][0])
        cx = (newedges[i][0][0] + newedges[i][1][0])/2
        cy = (newedges[i][0][1] + newedges[i][1][1])/2
        drawA(atoms,(cx,cy))
    decorate_triangle(atoms,newedges[0][0],newedges[0][1],newedges[5][0])
    decorate_triangle(atoms,newedges[3][0],newedges[4][0],newedges[2][0])
    decorate_square(atoms,newedges[1][0],newedges[2][0],newedges[4][0],newedges[5][0])


def decorate_K(atoms,edges):
    #find kink sequence +1,+3
    seq = []
    for edge in edges:
        dir = vector2angle((edge[1][0]-edge[0][0],edge[1][1]-edge[0][1]))
        seq.append(dir)
    origin = -1
    for i in range(len(seq)):
        if (seq[i-1]-seq[i-2]+10)%10 == 1 and (seq[i]-seq[i-1]+10)%10 == 3:
            origin = i
    #shift the edge order
    newedges = edges+edges
    newedges = newedges[origin:origin+len(edges)]
    for i in range(8):
        drawX(atoms,newedges[i][0])
        cx = (newedges[i][0][0] + newedges[i][1][0])/2
        cy = (newedges[i][0][1] + newedges[i][1][1])/2
        drawA(atoms,(cx,cy))
    decorate_triangle(atoms,newedges[0][0],newedges[1][0],newedges[7][0])
    decorate_triangle(atoms,newedges[2][0],newedges[3][0],newedges[1][0])
    decorate_triangle(atoms,newedges[4][0],newedges[5][0],newedges[3][0])
    cx = newedges[1][0][0] + newedges[3][0][0] - newedges[2][0][0]
    cy = newedges[1][0][1] + newedges[3][0][1] - newedges[2][0][1]
    decorate_fan(atoms,(cx,cy),(newedges[7][0],newedges[1][0],newedges[3][0],newedges[5][0]))
    drawA(atoms,(cx,cy))

def decorate_S(atoms,edges):
    #find kink +3
    seq = []
    for edge in edges:
        dir = vector2angle((edge[1][0]-edge[0][0],edge[1][1]-edge[0][1]))
        seq.append(dir)
    origin = -1
    for i in range(len(seq)):
        if (seq[i]-seq[i-1]+10)%10 == 3:
            origin = i
    #shift the edge order
    newedges = edges+edges
    newedges = newedges[origin:origin+len(edges)]
    for i in range(10):
        drawX(atoms,newedges[i][0])
        cx = (newedges[i][0][0] + newedges[i][1][0])/2
        cy = (newedges[i][0][1] + newedges[i][1][1])/2
        drawA(atoms,(cx,cy))
    for i in range(0,10,2):
        decorate_triangle(atoms,newedges[i][0],newedges[i+1][0],newedges[i-1][0])
    cx = newedges[1][0][0] + newedges[3][0][0] - newedges[2][0][0]
    cy = newedges[1][0][1] + newedges[3][0][1] - newedges[2][0][1]
    decorate_fan(atoms,(cx,cy),(newedges[1][0],newedges[3][0],newedges[5][0],newedges[7][0],newedges[9][0]))
    drawX(atoms,(cx,cy))


def lookup_similar(newatoms,x,y,box):
    found = False
    for dx in range(-1,2):
        xi = (x + dx + box[0]) % box[0]
        for dy in range(-1,2):
            yi = (y + dy + box[1]) % box[1]
            if newatoms.has_key((xi,yi)):
                return True
    return False


def atomic_positions(box,origin,atoms):
    #stack two units and rotate in order to fit in a rectangular box.
    newatoms = dict()
    #print "@BOX3"
    newbox = (box[0],box[1]*2,box[2])
    for atom in atoms:
        x = atom[0] - origin[0]
        y = atom[1] - origin[1]
        if not lookup_similar(newatoms,x,y,newbox):
            x = (x + newbox[0]) % newbox[0]
            y = (y + newbox[1]) % newbox[1]
            newatoms[(x,y)] =atoms[atom]
        x = atom[0] - origin[0]
        y = atom[1] - origin[1] + box[1]
        if not lookup_similar(newatoms,x,y,newbox):
            x = (x + newbox[0]) % newbox[0]
            y = (y + newbox[1]) % newbox[1]
            newatoms[(x,y)] =atoms[atom]
    xyz = []
    for atom in newatoms:
        if newatoms[atom] == "A":
            xyz.append((atom[0],atom[1],0))
        elif newatoms[atom] == "B":
            xyz.append((atom[0],atom[1],box[2]/2))
        else: #"X"
            xyz.append((atom[0],atom[1],box[2]/4))
            xyz.append((atom[0],atom[1],box[2]*3/4))
    #print "@AR3A"
    #print len(xyz)
    #for r in xyz:
    #    print r[0],r[1],r[2]
    return xyz




def wrap(c,box):
    v = [0] * len(c)
    for i in range(len(c)):
        v[i] =  c[i]-floor(c[i]/box[i]+0.5)*box[i]
    return v



def sub_pbc(vec1,vec2,box):
    v = [0] * len(vec1)
    for i in range(len(vec1)):
        v[i] = vec1[i]-vec2[i]
    return wrap(v,box)



def bond3d_fast(coord,box,thres):
    edges = dict()
    for i in range(len(coord)):
        edges[i] = dict()
    ndiv = floor(box[0]/thres),floor(box[1]/thres),floor(box[2]/thres)
    ndiv = map(int,ndiv)
    binw = box[0]/ndiv[0],box[1]/ndiv[1],box[2]/ndiv[2]
    resident = dict()
    for i in range(len(coord)):
        c = coord[i]
        ix,iy,iz = int(floor( c[0] / binw[0] )),int(floor( c[1] / binw[1] )),int(floor( c[2] / binw[2] ))
        if ix < 0:
            ix += ndiv[0]
        if iy < 0:
            iy += ndiv[1]
        if iz < 0:
            iz += ndiv[2]
        dictoflist_append(resident,(ix,iy,iz),i)
    for ix in range(ndiv[0]):
        for iy in range(ndiv[1]):
            for iz in range(ndiv[2]):
                for dx in range(-1,2):
                    for dy in range(-1,2):
                        for dz in range(-1,2):
                            jx = ix + dx
                            jy = iy + dy
                            jz = iz + dz
                            if jx < 0:
                                jx += ndiv[0]
                            if jy < 0:
                                jy += ndiv[1]
                            if jz < 0:
                                jz += ndiv[2]
                            jx %= ndiv[0]
                            jy %= ndiv[1]
                            jz %= ndiv[2]
                            #print jx,jy,jz,resident[(jx,jy,jz)]
                            for i in resident[(ix,iy,iz)]:
                                for j in resident[(jx,jy,jz)]:
                                    if i != j:
                                        x,y,z =sub_pbc(coord[i],coord[j],box)
                                        if x**2 + y**2 + z**2 < thres**2:
                                            edges[j][i] = x,y,z
    return edges

def bond3d(coord,box,thres):
    edges = dict()
    for i in range(len(coord)):
        edges[i] = dict()
    for i in range(len(coord)):
        for j in range(len(coord)):
            if i != j:
                x,y,z = sub_pbc(coord[i],coord[j],box)
                if x**2 + y**2 + z**2 < thres**2:
                    edges[j][i] = x,y,z
    return edges


hue = 0
for node in Pnodes:
    #print node
    endnode = register_peri(node, vert)
    height  = node[1] - endnode[1]
    endnode = register_peri(endnode, horiz)
    width   = endnode[0] - node[0]
    endnode = register_peri(endnode, invert(vert))
    endnode = register_peri(endnode, invert(horiz))
    #dangling edgeを除去する必要がある。
    for i in range(len(queue)-1):
        #if it is a kink,
        if queue[i][0]==queue[i+1][1] and queue[i][1]==queue[i+1][0]:
            progress[queue[i]] = True
            progress[queue[i+1]] = True
    
    depth = int(sqrt((queue[0][1][0]-queue[0][0][0])**2 + (queue[0][1][1]-queue[0][0][1])**2)+0.5)
    peri = []
    for i,j in queue:
        peri.append(i)
    
    #queueについて
    #辞書のうち値がFalseで
    #周縁ベクトルのownerであるQKSタイルが、もし正しい方向の周縁ベクトルを所有しているなら、
    tiles = dict()
    while len(queue) > 0:
        #directed edge
        edge = queue.pop(0)
        if progress[edge] == False:
            owners = QKSedgeowners[frozenset(edge)]
            owner = None
            count = 0
            for o in owners:
                if edge in o["id"]:
                    owner = o
                    count += 1
            #if count == 2:
            #    print edge
            #    print owners[0]
            #    print owners[1]
            if owner != None:
                edges = owner["id"]
                nodes = owner["node"]
                #print owner,nodes,edges
                tiles[nodes] = edges
                for e in edges:
                    if not progress.has_key(e):
                        e = (e[1],e[0])
                        progress[e] = False
                        queue.append(e)
    strokewidth(6)
    stroke(0,0,0.8)
    fill(hue,0.5,1)
    hue += 0.618
    if hue > 1.0:
        hue -= 1.0
    for polygon in tiles:
        drawpoly(polygon)
    stroke(0,0,0.3)
    nofill()
    drawpoly(peri)
    #QKSタイルをデコレートし、周期境界におさめる。これでおしまい。
    points = dict()
    for polygon in tiles:
        if len(polygon) == 6:
            decorate_Q(points,tiles[polygon])
        elif len(polygon) == 8:
            decorate_K(points,tiles[polygon])
        else:
            decorate_S(points,tiles[polygon])
#    box = (width,height,depth)
#    atoms = atomic_positions(box,node,points)
#    print "-------------------------",box
#    for atom in atoms:
#        print atom[0],atom[1],atom[2]
#    #double the layer
#    newatoms = []
#    for atom in atoms:
#        newatoms.append(atom)
#        newatoms.append((atom[0],atom[1],atom[2]+depth))
#    box = (box[0],box[1],box[2]+depth)
#    atoms = newatoms
#    thres = depth / 1.3
#    bonds = bond3d(atoms,box,thres)
    #for bond in bonds:
    #    print bond,atoms[bond],bonds[bond]
    #tets = tetrahedra(atoms,edges)

