import sys
from matplotlib import pyplot as plt
import random

def insideQ(P,T):
    # inf is used to act as infinity if we divide by 0
    inf = sys.float_info.max
    # epsilon is used to make sure points are not on the same line as vertexes
    epsilon = 0.000001
    edges = generateEdgesOfPolygon(P)
    intersections = 0

    for edge in edges:
        X0, Y0 = T[0], T[1]
        start_of_the_edge, end_of_the_edge = edge[0], edge[1]

        if start_of_the_edge[1] > end_of_the_edge[1]:
            tmp = start_of_the_edge
            start_of_the_edge = end_of_the_edge
            end_of_the_edge = tmp
        
        if (start_of_the_edge[0] == X0 and start_of_the_edge[1] == Y0) or (end_of_the_edge[0] == X0 and end_of_the_edge[1] == Y0):
            #the point is on the same as one of the edges => it is inside of the polygon
            intersections = 1
            break

        if Y0 == start_of_the_edge[1] or Y0 == end_of_the_edge[1]:
            Y0 += epsilon
        
        if (Y0 > end_of_the_edge[1] or Y0 < start_of_the_edge[1] or X0 > max(start_of_the_edge[0], end_of_the_edge[0])):
            continue

        if (X0 < min(start_of_the_edge[0], end_of_the_edge[0])):
            intersections += 1
            continue
        
        try:
            edge_slope = (end_of_the_edge[1] - start_of_the_edge[1]) / (end_of_the_edge[0] - start_of_the_edge[0])
        except ZeroDivisionError:
            edge_slope = inf
        
        try:
            point_slope = (Y0 - start_of_the_edge[1]) / (X0 - start_of_the_edge[0])
        except ZeroDivisionError:
            point_slope = inf
        
        if point_slope >= edge_slope:
            intersections += 1
            continue
    return intersections % 2 == 1
        
        

def generateEdgesOfPolygon(P):
    edges = []
    lastPoint = P.pop(0)
    firstPoint = lastPoint
    for point in P:
        edge = (lastPoint, point)
        edges.append(edge)
        lastPoint = point
    
    edges.append((firstPoint, lastPoint))
    return edges

T = (2.33,0.66)
P = [(0.02,0.10),(0.98,0.05),(2.10,1.03),(3.11,-1.23),(4.34,-0.35),(4.56,2.21),(2.95,3.12),(2.90,0.03),(1.89,2.22)]

#print(insideQ(P,T))

T1 = (1,1)
P1 = [(2,1), (6,1), (6,5), (2,5)]

#print(insideQ(P1,T1)) #False

T2 = (1,1)
P2 = [(1,1), (3,2), (5,1), (4,3), (5,4), (4,4), (3,5), (2,4), (1,4), (2,3)]
#print(insideQ(P2,T2)) #True

def test1():
    polygon_for_plot = [[2,1], [6,1], [6,5], [2,5]]

    polygon_for_plot.append(polygon_for_plot[0])

    xs, ys = zip(*polygon_for_plot)

    plt.figure()
    plt.plot(xs,ys)
    

    for _ in range(0, 10):
        point_x = random.uniform(0, 8)
        point_y = random.uniform(0, 8)
        polygon = [(2,1), (6,1), (6,5), (2,5)]
        isInside = insideQ(polygon, (point_x, point_y))
        text = "inside" if isInside else "outside"
        plt.scatter([point_x], [point_y])
        plt.annotate(text, [point_x,point_y])
    plt.show()
#test1()

def test2():
    polygon_for_plot = [[1,1], [3,2], [5,1], [4,3], [5,4], [4,4], [3,5], [2,4], [1,4], [2,3]]

    polygon_for_plot.append(polygon_for_plot[0])

    xs, ys = zip(*polygon_for_plot)

    plt.figure()
    plt.plot(xs,ys)
    

    for i in range(0, 10):
        point_x = random.uniform(0, 8)
        point_y = random.uniform(0, 8)
        polygon = [(1,1), (3,2), (5,1), (4,3), (5,4), (4,4), (3,5), (2,4), (1,4), (2,3)]
        isInside = insideQ(polygon, (point_x, point_y))
        text = "inside" if isInside else "outside"
        plt.scatter([point_x], [point_y])
        plt.annotate(text, [point_x,point_y])
    plt.show()
#test2()