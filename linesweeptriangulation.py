from jordan import insideQ
from delauney import optimize
import matplotlib.pyplot as plt
import random

def main(points):
    points = generify(points,epsilon=0.0001)
    triangles, lines = triangulate(points, vertical = True)
    draw_triangulation(triangles,"initial_triangulation_2")
    new_triang = optimize(list(triangles))
    draw_triangulation(new_triang, "delaunay_2")

def triangulate(points, vertical = True):
    lines = set()
    #first we order points default order is in vertical=True, which means we perform a linesweep with a vertical line
    ordered_points = order_points_x(points, vertical)
    #print(ordered_points)
    #for each point we draw a line to all previous points if this new line does not intersects with an existing one
    for point in ordered_points:
        #first we take all possible lines from this point to all previous lines
        line_candidates = add_line_candidates(ordered_points, ordered_points.index(point))
        #then we check if any of this lines intersects with previous ones
        for line_candidate in line_candidates:
            if  intersects(line_candidate, lines):
                continue
            else:
                #if it does not intersects we add it to all the other lines
                lines.add(line_candidate)
    #then from all lines we generate all triangles
    triangles = find_triangles(lines, points)
    return triangles, lines

def order_points_x(points, vertical):
    order_coordinate = 0
    if not vertical:
        order_coordinate = 1
    out = []
    for point in points:
        inserted = False
        if out == []:
            out.append(point)
            inserted = True
        else:
            for i in range(0,len(out)):
                op = out[i]
                if op[order_coordinate] >= point[order_coordinate]:
                    out.insert(i, point)
                    inserted = True
                    break
            if inserted:
                continue
            else:
                out.append(point)
    return out

#generates all line candidates from a point to all previous points
def add_line_candidates(ordered_points, index):
    new_point = ordered_points[index]
    line_candidates = []
    for i in range(0, index):
        pt = ordered_points[i]
        line_candidates.append((pt, new_point))
    return line_candidates

#calculates the determinant 2by2
def det(a, b): 
    return a[0] * b[1] - a[1] * b[0]

#Checks if the line candidate intersects with any of the previously added lines
def intersects(line_candidate, lines):
    for line in lines:
        xdiff = (line_candidate[0][0] - line_candidate[1][0], line[0][0] - line[1][0])
        ydiff = ((line_candidate[0][1] - line_candidate[1][1], line[0][1] - line[1][1]))

        div = det(xdiff, ydiff)
        if div == 0:
            return False
        
        d = (det(*line_candidate), det(*line))
        x = det(d, xdiff) / div
        y = det(d, ydiff) / div

        intersection = (x, y)
        tmp1 = check_if_intersection_on_line(line_candidate, intersection)
        tmp2 = check_if_intersection_on_line(line, intersection)
        if tmp1 and tmp2:
            return True

def check_if_intersection_on_line(line, intersection):
    first_point = (round(line[0][0],5),round(line[0][1],5))
    second_point = (round(line[1][0],5),round(line[1][1],5))
    x = round(intersection[0],5)
    y = round(intersection[1],5)

    if (first_point[0] < x and x < second_point[0]) or (first_point[0] > x and x > second_point[0]):
        if (first_point[1] < y and y < second_point[1]) or (first_point[1] > y and y > second_point[1]):
            return True

    return False

def find_triangles(lines, vertices):
    triangles = []
    lines = list(lines)
    for i in range(len(lines)):
        for j in range(i+1,len(lines)):
            for k in range(j+1,len(lines)):
                s1 = set(lines[i])
                s2 = set(lines[j])
                s3 = set(lines[k])
                s = s1.union(s2).union(s3)
                
                if len(s) == 3:
                    triangle = tuple(s)
                    
                    inside = False
                    for v in vertices:
                        if v in triangle:
                            continue
                        
                        if insideQ(list(triangle), v):
                            inside = True
                            break
                    if not (inside):
                        triangles.append(triangle)

    return triangles

def generateRandomPoints(no_of_points):
    points = set()
    for i in range(no_of_points):
        point_x = random.uniform(0, 50)
        point_y = random.uniform(0, 50)
        points.add((point_x,point_y))
    return points

def draw_triangulation(triangulation, name):
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(20, 20))
    triangles = set(triangulation)
    #print(triangles)
    for triangle in triangles:
        x = [x for x,y in triangle]
        y = [y for x,y in triangle]
        x.append(x[0])
        y.append(y[0])
        ax.fill(x,y,edgecolor='k')
        ax.plot(x,y,color='black')
    fig.savefig(name+'.jpg')

def generify(points, epsilon=0):
    return_points = set()
    for point in points:
        delta_x = random.uniform(-epsilon,epsilon)
        delta_y = random.uniform(-epsilon,epsilon)
        point_x = point[0]+delta_x
        point_y = point[1]+delta_y
        return_points.add((point_x,point_y))
    return return_points

points_random = generateRandomPoints(100)

test_points = {(12.997974344258594, 46.15574403711353), (49.25624608893983, 5.750919569480523), (29.387474074661142, 34.50054180028215), (47.45319908055559, 38.27308760227541), (5.372006694228665, 33.49262510782046), (19.057473379647615, 33.329156166690964), (7.9590926053552336, 24.40522382112014), (33.1867786497695, 18.26281736716532), (21.595045121749013, 32.442085007057756), (20.095660334280225, 12.812220912155203)}
test2 = {(0,0), (5,-1), (7,-5), (9,4), (3,9)}
main(points_random)