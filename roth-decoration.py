#inflation
#QKS tiling
#macro structure
#Rothの論文の中に、QKSタイリングはFrank-Kasper型でない原子を含むことを発見(κなど)
#初代のFKQaは、うまい具合にこの問題を回避したタイリングになっていたらしい。
#QKSをあきらめ、Triangle/Rectangle tilingに切り替える。3日の努力が無駄に!!
#2011-8-25

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
L9 = (9,8,7,8,9,0)
for node in QKSnodes:
    #L1
    endnode = lookup_seq(node,L9)
    if len(endnode):
        #print node,endnode
        dx = endnode[0] - node[0]
        dy = endnode[1] - node[1]
        stroke(0,1,1)
        line(node[0]/10,node[1]/10, (node[0]+dx*0.9)/10,(node[1]+dy*0.9)/10)
        if not macroedges.has_key(node):
            macroedges[node] = dict()
        macroedges[node][L9] = endnode
L1 = (1,2,3,2,1,0)
for node in QKSnodes:
    endnode = lookup_seq(node,L1)
    if len(endnode):
        #print node,endnode
        dx = endnode[0] - node[0]
        dy = endnode[1] - node[1]
        stroke(0.6666,1,1)
        line(node[0]/10,node[1]/10, (node[0]+dx*0.9)/10,(node[1]+dy*0.9)/10)
        if not macroedges.has_key(node):
            macroedges[node] = dict()
        macroedges[node][L1] = endnode

S3  = (3,2,1,0)
lookup_and_register(S3)

LS1 = L1+S3 #(1,0,9,8,1,0,9,8,9,0)
add_and_register(L1,S3)

S7 = (7,8,9,0)
lookup_and_register(S7)

LS9 = L9 + S7 #(7,8,9,8,7,6,9,8,7,6)
add_and_register(L9,S7)

add_and_register(L9,L9)
add_and_register(L1,L1)
add_and_register(L9,LS9)
add_and_register(L1,LS1)

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
SEQ1,SEQ2 = S3,S7
#SEQ1,SEQ2 = SL1,LS7
#SEQ1,SEQ2 = L1+SL1,L7+LS7
#SEQ1,SEQ2 = L1+L1,L7+L7
SEQ1,SEQ2 = L1,L9

Pnodes = parallelogram(SEQ1, SEQ2)

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

#invert the sequence of directions
def invert(seq):
    newseq = []
    for dir in seq:
        newseq.append((dir+5)%10)
    newseq.reverse()
    return newseq


def drawA(atoms,pos,coord):
    atoms[pos] = ("A",coord)
    x = pos[0]/10
    y = pos[1]/10
    strokewidth(2)
    stroke(0)
    fill(1,0,1)
    oval(x-3,y-3,6,6)

def drawB(atoms,pos,coord):
    atoms[pos] = ("B",coord)
    x = pos[0]/10
    y = pos[1]/10
    strokewidth(1)
    stroke(0)
    fill(0)
    oval(x-3,y-3,6,6)


def drawX(atoms,pos,coord):
    atoms[pos] = ("X",coord)
    x = pos[0]/10
    y = pos[1]/10
    strokewidth(1)
    stroke(0)
    fill(1,0,1)
    oval(x-3,y-3,6,6)
    nostroke()
    fill(0)
    oval(x-2,y-2,4,4)



def decorate_triangle(atoms,a,b,c,coord):
    cx = (b[0] + c[0])/2
    cy = (b[1] + c[1])/2
    cx = (a[0] + cx*3) / 4
    cy = (a[1] + cy*3) / 4
    drawB(atoms,(cx,cy),coord)

def decorate_fan(atoms,c,p,black,green,blue,purple):
    if len(p) == 5:
        for point in p:
            cx = (c[0]*1 + point[0]*1)/2
            cy = (c[1]*1 + point[1]*1)/2
            drawB(atoms,(cx,cy),black)
        r = range(-1,len(p)-1)
        for i in r:
            cx = (c[0]*2 + p[i][0]*3 + p[i+1][0]*3)/8
            cy = (c[1]*2 + p[i][1]*3 + p[i+1][1]*3)/8
            drawA(atoms,(cx,cy),purple)
    else:
        cx = (c[0]*4 + p[0][0]*3)/7
        cy = (c[1]*4 + p[0][1]*3)/7
        drawB(atoms,(cx,cy),green)
        cx = (c[0]*3 + p[1][0]*4)/7
        cy = (c[1]*3 + p[1][1]*4)/7
        drawB(atoms,(cx,cy),black)
        cx = (c[0]*3 + p[2][0]*4)/7
        cy = (c[1]*3 + p[2][1]*4)/7
        drawB(atoms,(cx,cy),black)
        cx = (c[0]*4 + p[3][0]*3)/7
        cy = (c[1]*4 + p[3][1]*3)/7
        drawB(atoms,(cx,cy),green)
        r = range(0,len(p)-1)
        cx = (c[0]*2 + p[0][0]*3 + p[1][0]*3)/8
        cy = (c[1]*2 + p[0][1]*3 + p[1][1]*3)/8
        drawA(atoms,(cx,cy),blue)
        cx = (c[0]*2 + p[1][0]*3 + p[2][0]*3)/8
        cy = (c[1]*2 + p[1][1]*3 + p[2][1]*3)/8
        drawA(atoms,(cx,cy),blue)
        cx = (c[0]*2 + p[2][0]*3 + p[3][0]*3)/8
        cy = (c[1]*2 + p[2][1]*3 + p[3][1]*3)/8
        drawA(atoms,(cx,cy),blue)

def decorate_square(atoms,a,b,c,d,white,black):
    cx = (a[0]*2 + b[0]*2 + c[0]*1 + d[0]*1)/6
    cy = (a[1]*2 + b[1]*2 + c[1]*1 + d[1]*1)/6
    drawB(atoms,(cx,cy),black)
    cx = (a[0]*1 + b[0]*1 + c[0]*2 + d[0]*2)/6
    cy = (a[1]*1 + b[1]*1 + c[1]*2 + d[1]*2)/6
    drawB(atoms,(cx,cy),black)
    cx = (a[0]*1 + b[0]*4 + c[0]*4 + d[0]*1)/10
    cy = (a[1]*1 + b[1]*4 + c[1]*4 + d[1]*1)/10
    drawA(atoms,(cx,cy),white)
    cx = (a[0]*4 + b[0]*1 + c[0]*1 + d[0]*4)/10
    cy = (a[1]*4 + b[1]*1 + c[1]*1 + d[1]*4)/10
    drawA(atoms,(cx,cy),white)
    

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
        drawX(atoms,newedges[i][0],12)
    cx = (newedges[0][0][0]*1 + newedges[0][1][0]*1)/2
    cy = (newedges[0][0][1]*1 + newedges[0][1][1]*1)/2
    drawA(atoms,(cx,cy),12)
    cx = (newedges[1][0][0]*1 + newedges[1][1][0]*1)/2
    cy = (newedges[1][0][1]*1 + newedges[1][1][1]*1)/2
    drawA(atoms,(cx,cy),12)
    cx = (newedges[2][0][0]*1 + newedges[2][1][0]*1)/2
    cy = (newedges[2][0][1]*1 + newedges[2][1][1]*1)/2
    drawA(atoms,(cx,cy),12)
    cx = (newedges[3][0][0]*1 + newedges[3][1][0]*1)/2
    cy = (newedges[3][0][1]*1 + newedges[3][1][1]*1)/2
    drawA(atoms,(cx,cy),12)
    cx = (newedges[4][0][0]*1 + newedges[4][1][0]*1)/2
    cy = (newedges[4][0][1]*1 + newedges[4][1][1]*1)/2
    drawA(atoms,(cx,cy),12)
    cx = (newedges[5][0][0]*1 + newedges[5][1][0]*1)/2
    cy = (newedges[5][0][1]*1 + newedges[5][1][1]*1)/2
    drawA(atoms,(cx,cy),12)
    decorate_triangle(atoms,newedges[0][0],newedges[0][1],newedges[5][0],16)
    decorate_triangle(atoms,newedges[3][0],newedges[4][0],newedges[2][0],16)
    decorate_square(atoms,newedges[1][0],newedges[2][0],newedges[4][0],newedges[5][0],15,14)


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
        drawX(atoms,newedges[i][0],12)
    cx = (newedges[0][0][0]*1 + newedges[0][1][0]*1)/2
    cy = (newedges[0][0][1]*1 + newedges[0][1][1]*1)/2
    drawA(atoms,(cx,cy),12)
    cx = (newedges[1][0][0]*1 + newedges[1][1][0]*1)/2
    cy = (newedges[1][0][1]*1 + newedges[1][1][1]*1)/2
    drawA(atoms,(cx,cy),12)
    cx = (newedges[2][0][0]*1 + newedges[2][1][0]*1)/2
    cy = (newedges[2][0][1]*1 + newedges[2][1][1]*1)/2
    drawA(atoms,(cx,cy),12)
    cx = (newedges[3][0][0]*1 + newedges[3][1][0]*1)/2
    cy = (newedges[3][0][1]*1 + newedges[3][1][1]*1)/2
    drawA(atoms,(cx,cy),12)
    cx = (newedges[4][0][0]*1 + newedges[4][1][0]*1)/2
    cy = (newedges[4][0][1]*1 + newedges[4][1][1]*1)/2
    drawA(atoms,(cx,cy),12)
    cx = (newedges[5][0][0]*1 + newedges[5][1][0]*1)/2
    cy = (newedges[5][0][1]*1 + newedges[5][1][1]*1)/2
    drawA(atoms,(cx,cy),12)
    cx = (newedges[6][0][0]*1 + newedges[6][1][0]*1)/2
    cy = (newedges[6][0][1]*1 + newedges[6][1][1]*1)/2
    drawA(atoms,(cx,cy),12)
    cx = (newedges[7][0][0]*1 + newedges[7][1][0]*1)/2
    cy = (newedges[7][0][1]*1 + newedges[7][1][1]*1)/2
    drawA(atoms,(cx,cy),12)
         
    decorate_triangle(atoms,newedges[0][0],newedges[1][0],newedges[7][0],16)
    decorate_triangle(atoms,newedges[2][0],newedges[3][0],newedges[1][0],16)
    decorate_triangle(atoms,newedges[4][0],newedges[5][0],newedges[3][0],16)
    cx = newedges[1][0][0] + newedges[3][0][0] - newedges[2][0][0]
    cy = newedges[1][0][1] + newedges[3][0][1] - newedges[2][0][1]
    decorate_fan(atoms,(cx,cy),(newedges[7][0],newedges[1][0],newedges[3][0],newedges[5][0]),12,14,15,16)
    drawA(atoms,(cx,cy),15)

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
        drawX(atoms,newedges[i][0],12)
    for i in range(0,10,2):
        cx = (newedges[i][0][0]*1 + newedges[i][1][0]*1)/2
        cy = (newedges[i][0][1]*1 + newedges[i][1][1]*1)/2
        drawA(atoms,(cx,cy),12)
        cx = (newedges[i+1][0][0]*1 + newedges[i+1][1][0]*1)/2
        cy = (newedges[i+1][0][1]*1 + newedges[i+1][1][1]*1)/2
        drawA(atoms,(cx,cy),12)
    for i in range(0,10,2):
        decorate_triangle(atoms,newedges[i][0],newedges[i+1][0],newedges[i-1][0],16)
    cx = newedges[1][0][0] + newedges[3][0][0] - newedges[2][0][0]
    cy = newedges[1][0][1] + newedges[3][0][1] - newedges[2][0][1]
    decorate_fan(atoms,(cx,cy),(newedges[1][0],newedges[3][0],newedges[5][0],newedges[7][0],newedges[9][0]),12,14,15,16)
    drawX(atoms,(cx,cy),12)


def lookup_similar(newatoms,x,y,box):
    found = False
    for dx in range(-1,2):
        xi = (x + dx + box[0]) % box[0]
        for dy in range(-1,2):
            yi = (y + dy + box[1]) % box[1]
            if newatoms.has_key((xi,yi)):
                return True
    return False


def atomic_positions(vec1,vec2,depth,origin,atoms):
    newatoms = dict()
    #print "@BOX3"
    box = (vec1[0]+vec2[0],-vec1[1]+vec2[1],depth)
    for atom in atoms:
        x = atom[0] - origin[0]
        y = atom[1] - origin[1]
        if not lookup_similar(newatoms,x,y,box):
            x = (x + box[0]) % box[0]
            y = (y + box[1]) % box[1]
            newatoms[(x,y)] =atoms[atom]
        x = atom[0] - origin[0] + vec1[0]
        y = atom[1] - origin[1] + vec1[1]
        if not lookup_similar(newatoms,x,y,box):
            x = (x + box[0]) % box[0]
            y = (y + box[1]) % box[1]
            newatoms[(x,y)] =atoms[atom]
    xyz = []
    for atom in newatoms:
        layer,coordnum = newatoms[atom]
        #print "coord",coordnum
        if layer == "A":
            xyz.append((atom[0],atom[1],0,coordnum))
        elif layer == "B":
            xyz.append((atom[0],atom[1],depth/2,coordnum))
        else: #"X"
            xyz.append((atom[0],atom[1],depth/4,coordnum))
            xyz.append((atom[0],atom[1],depth*3/4,coordnum))
    #print "@AR3A"
    #print len(xyz)
    #for r in xyz:
    #    print r[0],r[1],r[2]
    return box,xyz




def wrap(c,box):
    v = [0] * len(c)
    for i in range(len(c)):
        v[i] =  c[i]-floor(c[i]/box[i]+0.5)*box[i]
    return v

def wrap3(c,box):
    v = [0] * 3
    for i in range(3):
        v[i] =  c[i]-floor(c[i]/box[i]+0.5)*box[i]
    return v



def sub_pbc(vec1,vec2,box):
    v = [0] * len(vec1)
    for i in range(len(vec1)):
        v[i] = vec1[i]-vec2[i]
    return wrap3(v,box)



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
    for i in coord:
        edges[i] = dict()
    for i in coord:
        for j in coord:
            if i != j:
                x,y,z = sub_pbc(i,j,box)
                if x**2 + y**2 + z**2 < thres**2:
                    edges[j][i] = x,y,z
    return edges


def vecsize(v):
    return sqrt(v[0]**2 + v[1]**2 + v[2]**2)


#adjust the threshold in order to let the coordination number included in (12,14,15,16)
def cageshaper( bonds, thres ):
    #print bonds
    while True:
        newbonds = []
        wellgapped = True
        for bond in bonds:
            siz = vecsize(bond)
            if siz < thres:
                newbonds.append(bond)
            elif siz < thres * 1.02:
                wellgapped = False
        if wellgapped and len(newbonds) in (12,14,15,16):
            return newbonds
        if len(newbonds) > 16:
            return newbonds
        print len(newbonds),thres
        thres *= 1.01

def cageshaper2( bonds, coordnum ):
    #print bonds
    length = dict()
    for bond in bonds:
        length[bond] = vecsize(bonds[bond])
    newbonds = sorted(bonds.keys(),cmp=lambda x,y: cmp(length[x],length[y]))
    newbonds = newbonds[0:coordnum]
    ret = dict()
    for bond in newbonds:
        ret[bond] = bonds[bond]
    return ret


def tetrahedra( vertices, thres ):
    bonds = dict()
    for i in vertices:
        bonds[i] = dict()    
    for i in range( len(vertices) ):
        for j in range( i+1, len(vertices) ):
            dx = vertices[i][0] - vertices[j][0]
            dy = vertices[i][1] - vertices[j][1]
            dz = vertices[i][2] - vertices[j][2]
            if dx**2 + dy**2 + dz**2 < thres**2:
                bonds[vertices[i]][vertices[j]] = 1
                bonds[vertices[j]][vertices[i]] = 1
    for i in vertices:
        if not len(bonds[i]) in (5,6):
            print i,len(bonds[i])
    print

hue = 0
for node in Pnodes:
    #print node
    endnode = register_peri(node, SEQ2)
    VEC1 = (endnode[0] - node[0],endnode[1] - node[1])
    endnode = register_peri(endnode, SEQ1)
    endnode = register_peri(endnode, invert(SEQ2))
    VEC2 = (endnode[0] - node[0],endnode[1] - node[1])
    endnode = register_peri(endnode, invert(SEQ1))
    #dangling edgeを除去する必要がある。
    for i in range(len(queue)-1):
        #if it is a kink,
        if queue[i][0]==queue[i+1][1] and queue[i][1]==queue[i+1][0]:
            progress[queue[i]] = True
            progress[queue[i+1]] = True
    
    depth = int(1.5*sqrt((queue[0][1][0]-queue[0][0][0])**2 + (queue[0][1][1]-queue[0][0][1])**2)+0.5)
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
    box,atoms = atomic_positions(VEC1,VEC2,depth,node,points)
    print "-------------------------",box
    for atom in atoms:
        print atom[0],atom[1],atom[2],atom[3]
    #double the layer
    newatoms = []
    for atom in atoms:
        newatoms.append(atom)
        newatoms.append((atom[0],atom[1],atom[2]+box[2],atom[3]))
    box = (box[0],box[1],box[2]*2)
    box = map(float,box)
    atoms = newatoms
    thres = depth * 200.0 / 335.0
    # temporary
    bonds = bond3d(atoms,box,thres*1.3)
    adjnetwork = dict()
    for head in bonds:
        coordnum = head[3]
        #cage is a dict() whose keys are the coordinate of the neighbor atom
        #and the values are relative vectors
        cage = cageshaper2( bonds[head], coordnum )
        if not len(cage) in (12,14,15,16):
            print head,len(bonds[head]) ,map(vecsize,bonds[head].values())
            print bonds[head].values()
            strokewidth(2)
            stroke(0,1,1)
            nofill()
            oval(head[0]/10-3,head[1]/10-3,6,6)
            print
        else:
            strokewidth(2)
            if len(cage) == 12:
                stroke(0,1,0)
            elif len(cage) == 14:
                stroke(0.25,1,1)
            elif len(cage) == 15:
                stroke(0.5,1,1)
            elif len(cage) == 16:
                stroke(0.75,1,1)
            nofill()
            oval(head[0]/10-2,head[1]/10-2,4,4)
            if random() < 0.03 and len(cage)==15:
                for b in cage:
                    line(head[0]/10,head[1]/10,(head[0]+cage[b][0])/10,(head[1]+cage[b][1])/10)
        adjnetwork[head] = cage
        #tet = tetrahedra( cage, thres*1.07 )
        #for delta in cage:
#            print atoms[head][0],atoms[head][1],atoms[head][2]
#            print atoms[head][0]+delta[0],atoms[head][1]+delta[1],atoms[head][2]+delta[2]
        #    print 0,0,0
        #    print delta[0],delta[1],delta[2]
        #    print
    #tets = tetrahedra(atoms,edges)
    #adjnetworkの中に、四面体をさがす。一意に決まるはず。
    triangleowners = dict()
    tetras = dict()
    for atom in adjnetwork:
        cage = adjnetwork[atom]
        vertices = cage.keys()
        for i in range(len(vertices)):
            for j in range(i+1,len(vertices)):
                if adjnetwork[vertices[i]].has_key(vertices[j]):
                    for k in range(j+1,len(vertices)):
                        if adjnetwork[vertices[i]].has_key(vertices[k]):
                            if adjnetwork[vertices[k]].has_key(vertices[j]):
                                tetra = frozenset([atom,vertices[i],vertices[j],vertices[k]])
                                if not tetras.has_key(tetra):
                                    tetras[tetra] = (atom[0] + (cage[vertices[i]][0]+cage[vertices[j]][0]+cage[vertices[k]][0])/4,
                                                     atom[1] + (cage[vertices[i]][1]+cage[vertices[j]][1]+cage[vertices[k]][1])/4,
                                                     atom[2] + (cage[vertices[i]][2]+cage[vertices[j]][2]+cage[vertices[k]][2])/4,)
                                    faces = []
                                    faces.append(frozenset([atom,vertices[i],vertices[j]]))
                                    faces.append(frozenset([atom,vertices[i],vertices[k]]))
                                    faces.append(frozenset([atom,vertices[j],vertices[k]]))
                                    faces.append(frozenset([vertices[i],vertices[j],vertices[k]]))
                                    for face in faces:
                                        if not triangleowners.has_key(face):
                                            triangleowners[face] = []
                                        triangleowners[face].append(tetra)
    strokewidth(0.5)
    stroke(0)
    for face in triangleowners:
        if len(triangleowners[face]) == 2:
            tetraA,tetraB = triangleowners[face]
            coordA = tetras[tetraA]
            coordB = tetras[tetraB]
            dx,dy,dz = wrap3((coordB[0]-coordA[0],coordB[1]-coordA[1],coordB[2]-coordA[2]),box)
            line(coordA[0]/10,coordA[1]/10,(coordA[0]+dx)/10,(coordA[1]+dy)/10)
        else:
            print face,triangleowners[face]
    break    

#現在の問題は、距離で結合を定義しただけでは、配位数が不安定になってしまうこと。
#原子を配置する時に、結合も定義すればよさそうに思えるが、タイルをまたぐような結合は
#扱いが非常に面倒になる。なんとか幾何学的な情報だけで、結合を創りたい。
#そのためには、なぜ13配位というものができるのかを調べる必要があるだろう。

#配位数がおかしい頂点が特定できたので、配位数を明示的に与えるようにする。
#これでうまくいく気がする。