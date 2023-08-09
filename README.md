# Triangulation

At the Topological Data Analysis course I had to implement the line sweep algorithm for triangulation of $n$ points in a plane. 
We also had to make it "better" using edge flipping to get Delaunay Triangulation. (The Delaunay Triangulation maximizes the minimal angle in a triangulation).

## Line sweep triangulation

The function triangulate takes 2 parameters: $n$ points and a boolean that indicates whether the line sweep will be performed vertically or horisontaly. 

Here is an image of the result of the vertical line sweep triangulation over 50 points:
![Line sweep triangulation](./images/initial_triangulation_1.jpg)

## Delaunay Triangulation

The Delaunay Triangulation maximizes the minimal angle in a triangulation. I implemented the edge flipping algorithm that runs in $O(n^2)$ time. 

Triangulation is Delaunay if and only if every edge in a triangulation is locally Delaunay. We can check for every edge if it is locally Delaunay by using simple in circle test.

Given three points $A(A_x, A_y)$, $B(B_x, B_y)$, and $C(C_x, C_y)$, and a fourth point $D(D_x, D_y)$, the in-circle test checks whether $D$ is inside the circumcircle of triangle $ABC$.

The test involves calculating the determinant of a matrix:

![In circle test](./images/incircle-test.svg)

If the determinant is positive, point $D$ lies outside the circumcircle; if it's negative, $D$ lies inside; and if it's zero, $D$ is on the circle's boundary.

If the point is inside we perform an edge flip.

After the edge flipping algorithm the triangulation from line sweep example looks like this:
![Delaunay triangulation](./images/delaunay_1.jpg)