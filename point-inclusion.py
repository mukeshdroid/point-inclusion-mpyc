""" Two party Point Inclusion Problem in 2D

Alice has has a point z = (a,b).
Bob has a polygon.
We need a trusted helper.


Author: Mukesh Tiwari
Date: 27 Jun 2024 
"""

#imports
from mpyc.runtime import mpc
import csv

#define a function that securely evaluates point line reln
def sec_point_line(x1,y1,x2,y2,x3,y3):
    # (x1,y1) and (x2,y2) define a line
    # (x3,y3) is the point
    val1 = (y3-y1)*(x2-x1) - (y2-y1)*(x3-x1)
    val2 = (x2-x1)

    tmp1 = mpc.if_else(val1>0,1,0)
    tmp2 = mpc.if_else(val2>0,1,0)
    tmp3 = mpc.if_else(val1 == 0,1,0)
    tmp4 = mpc.if_else(val2 == 0,1,0)
    tmp5 = mpc.if_else(val1<0,1,0)
    tmp6 = mpc.if_else(val2<0,1,0)


    case1 = (tmp1 * tmp2) + (tmp5*tmp6)
    case2 = (tmp1 * tmp6) + (tmp2*tmp5)


    res1 = mpc.if_else(case1 > 0,1,-1)
    res2 = mpc.if_else(case2 > 0,-1,1)

    #This actually does return the correct value!!!
    # val = val1/val2
    # if val > 0 -> 1
    # if val = 0 -> 0
    # if val < 0 -> -1
    return (res1 + res2)/2

async def main():

    secint = mpc.SecInt()

    await mpc.start()

    #define the variables and initialize them to None

    #point is a 2-tuple
    # point[0] = x-coordinate
    # point[1] = y -cordinate  
    point = [None,None]
    len_polygon = None
    tmp = None

    #define role for the parties    
    role = mpc.pid

    #if pid is zero, then you are trusted third party.
    if role == 0:
        print('You are the trusted helper!')

    # if pid is one, then you are Alice and thus have a point 
    if role == 1:
        print("You have a point as input!")
        #open the csv file containing the point's coordinates
        with open('data/point.csv') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                point[0] = int(row[0])
                point[1] = int(row[1])
        

    #if pid is two, you are Bob and have a polygon.
    # the polygon is assumed to have the following properties:
    # - the first entry is leftmost point. 
    # - the points are in cyclic order
    # - the first m points belong to lower boundary
    if role == 2:
        print("You have a polygon as input!")
        #open the csv file containing the polygon's coordinates
        with open('data/polygon.csv') as csvfile:
            reader = csv.reader(csvfile)
            #count the number of points in polygon
            tmp = 0
            for row in reader:
                tmp = tmp + 1
    
    # Bob (Party 2) sends the number to vertices to all parties.
    len_polygon = await mpc.transfer(tmp,2)


    #initialize the polygon to None:
    polygon = [[None,None]]*len_polygon 
    point_line_reln = [None]*len_polygon

    #for now lets assume we have the polygon boundary
    # 1 means lower; -1 means upper
    polygon_boundary = [None]*len_polygon

    #define the polygon using file:
    #if pid is two, you are Bob and have a polygon.
    if role == 2:
        #initialize polygon
        polygon = []
        #open the csv file containing the polygon's coordinates
        with open('data/polygon.csv') as csvfile:
            reader = csv.reader(csvfile)
            i = 0
            for row in reader:
                polygon.append([int(row[0]),int(row[1])])
                polygon_boundary[i] = int(row[2])
                i = i + 1
    

    #convert the polygon to securepolygon

    # secpolygon = []
    # for vertex in polygon:
    #     secpolygon.append([secint(vertex[0]),secint(vertex[1])])

    #Bob (party 2) securely shares the secure polygon
    x = [None]*len_polygon    
    for i in range(len_polygon):
        # x[i] is the ith vertex
        x[i] = mpc.input([secint(polygon[i][0]),secint(polygon[i][1])],2)

    #Alice (party 1) securely shares the point
    sec_point = [None,None]
    sec_point[0] = mpc.input(secint(point[0]),1)
    sec_point[1] = mpc.input(secint(point[1]),1)


    #Bob (party 2) securely shares the polygon boundary
    sec_polygon_boundary = [None]*len_polygon
    for i in range(len_polygon):
        sec_polygon_boundary[i] = mpc.input(secint(polygon_boundary[i]),2)


    # take each edge and determine reln with the line
    for i in range(len_polygon):
        # the next point
        j = (i+1) % len_polygon
 
        # see if any is type None and if so skip the computation
        is_none = [isinstance(x, type(None)) for x in [x[i][0],x[i][1],x[j][0],x[j][1],sec_point[0],sec_point[1]]]
        if not any(is_none):
            point_line_reln[i] = sec_point_line(x[i][0],x[i][1],x[j][0],x[j][1],sec_point[0],sec_point[1])

    
    #determine if the point is inside or not
    result = 0
    for i in range(len_polygon):
        if not (point_line_reln[i] is None or sec_polygon_boundary[i] is None):
            result = result + point_line_reln[i] * sec_polygon_boundary[i]
    verdict = mpc.if_else(result == len_polygon,1,0)
    
    #print the result
    print("The solution is ")
    print(await mpc.output(verdict))

    # print(await mpc.output(verdict))
    print("\nNote: 1 means Point lies inside Polygon!")
    print("Note: 0 Point lies outside Polygon!")

    await mpc.shutdown()

mpc.run(main())