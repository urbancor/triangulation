import numpy as np
import matplotlib.pyplot as plt
import random

def optimize(T):
    stack = []
    for t in T:
        stack.append((t[0],t[1]))
        stack.append((t[0],t[2]))
        stack.append((t[1],t[2]))
    flipped_edges = {}
    while len(stack) != 0:
        edge = stack.pop()
        if flipped_edges.get(edge):
            continue
        t1, t2 = findTrianglesWithEdge(edge, T)
        if t2 == None:
            continue
        t1_index = T.index(t1)
        t2_index = T.index(t2)
        if not isPositivelyOrientated(t1):
            t1 = (t1[0],t1[2],t1[1])
        if isDelaunay(edge, t1, t2):
            continue
        else:
            #if the edge is not delaunay we flip it
            flipped_edges[edge] = True
            a,b = getOrderOfEdgeInTriangle(edge,t1)
            c = findVertexNotOnEdge(edge, t1)
            d = findVertexNotOnEdge(edge, t2)
            
            new_triangle1 = (a,c,d)
            new_triangle2 = (b,d,c)
            T[t1_index] = new_triangle1
            T[t2_index] = new_triangle2
            stack.append((c,d))
            stack.append((a,c))
            stack.append((c,b))
            stack.append((a,d))
            stack.append((d,b))
    return T

def isPositivelyOrientated(T):
    a = []
    a.append([1, T[0][0], T[0][1]])
    a.append([1, T[1][0], T[1][1]])
    a.append([1, T[2][0], T[2][1]])
    return np.linalg.det(a) > 0

def isDelaunay(edge, t1, t2):
    a,b = getOrderOfEdgeInTriangle(edge,t1)
    c = findVertexNotOnEdge(edge, t1)
    d = findVertexNotOnEdge(edge, t2)
    M = []
    M.append([a[0], a[1], pow(a[0],2)+ pow(a[1],2), 1])
    M.append([b[0], b[1], pow(b[0],2)+ pow(b[1],2), 1])
    M.append([c[0], c[1], pow(c[0],2)+ pow(c[1],2), 1])
    M.append([d[0], d[1], pow(d[0],2)+ pow(d[1],2), 1])
    return np.linalg.det(M) < 0

def findTrianglesWithEdge(edge, T):
    triangles = []
    reversed_edge = (edge[1], edge[0])
    for triangle in T:
        e1 = (triangle[0], triangle[1])
        e2 = (triangle[1], triangle[2])
        e3 = (triangle[0], triangle[2])

        if compare_edges(edge, e1) or compare_edges(edge, e2) or compare_edges(edge, e3) or compare_edges(reversed_edge, e1) or compare_edges(reversed_edge, e2) or compare_edges(reversed_edge, e3):
            triangles.append(triangle)
    if len(triangles) == 2:
        return triangles[0], triangles[1]
    elif len(triangles) == 1: #if it is boundary edge
        return triangle[0], None
    else:
        return None, None

#returns the third vertex of a triangle T that is not on the edge
def findVertexNotOnEdge(edge, T):
    if not (T[0] in edge):
        return T[0]
    if not (T[1] in edge):
        return T[1]
    if not (T[2] in edge):
        return T[2]
    return None
    
def compare_edges(e1, e2):
    return e1[0] == e2[0] and e1[1] == e2[1]

def getOrderOfEdgeInTriangle(edge, T):
    v1 = edge[0]
    v2 = edge[1]
    
    if T[0] == v1 and T[1] == v2 or T[1] == v1 and T[2] == v2 or T[2] == v1 and T[0] == v2:
        return v1, v2
    else:
        return v2, v1

def generify(points, epsilon=0):
    return_points = set()
    for point in points:
        delta_x = random.uniform(-epsilon,epsilon)
        delta_y = random.uniform(-epsilon,epsilon)
        point_x = point[0]+delta_x
        point_y = point[1]+delta_y
        return_points.add((point_x,point_y))
    return return_points

def draw_triangulation(triangulation, name):
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(8, 8))
    triangles = set(triangulation)
    #print(triangles)
    for triangle in triangles:
        x = [x for x,y in triangle]
        y = [y for x,y in triangle]
        x.append(x[0])
        y.append(y[0])
        ax.fill(x,y,edgecolor='k')
        ax.plot(x,y)
    fig.savefig(name+'.jpg')
Triangulation = [((0, 0), (5, -1), (7, -5)), ((5, -1), (7, -5), (9, 4)), ((0, 0), (5, -1), (9, 4)), ((0, 0), (3, 9), (9, 4))]
#draw_triangulation(Triangulation, "initial_triangulation")
#Triangulation = [((3, 9), (7, -5), (9, 4)), ((3, 9), (5, -1), (7, -5)), ((3, 9), (0, 0), (5, -1)), ((0, 0), (5, -1), (7, -5))]
#new_T = optimize(Triangulation)
#print(new_T)

#draw_triangulation(new_T, "Delaunay_triangulation")

