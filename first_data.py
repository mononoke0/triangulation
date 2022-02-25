import numpy as np
import matplotlib.pyplot as plt
import random
import tkinter as tk
import matplotlib.patches as patches



class make_standard:
    def __init__(self):
        #making lattice points for standard value of temperature 
        x = np.linspace(-20,20,9)
        y = np.linspace(-20,20,9)  
        self.xx, self.yy = np.meshgrid(x, y)
        self.standard_list = self.xx + self.yy 
       # self.points = self.xx * (-4 + np.random.uniform(-1, 1, (10, 10))) + self.yy * (4 + np.random.uniform(-1, 1, (10, 10)))
       # self.standard_list = ([self.xx*self.yy*self.points for x in range(2, 9)])

    def standard(self):
      #print(self.standard_list)
      return  self.standard_list

#find temperature of add point
class make_firstpoints:
    def __init__(self, points,xy_list):
        self.land_x = xy_list[0]
        self.land_y = xy_list[1]

        x_int = int(self.land_x)
        y_int = int(self.land_y)

        list = [self.land_x, self.land_y]
        if (self.land_x - x_int < 0.5) & (self.land_y - y_int < 0.5)& (x_int<8) &(y_int<8):
            self.land_points = points[x_int][y_int] + np.random.uniform(-5,5)
        elif (self.land_x - x_int < 0.5) & (self.land_y - y_int >= 0.5)&(x_int<8) &(y_int<8):
            self.land_points = points[x_int][y_int + 1] + np.random.uniform(-5,5)
        elif (self.land_x - x_int >= 0.5) & (self.land_y - y_int < 0.5)&(x_int<8) &(y_int<8):
            self.land_points = points[x_int + 1][y_int] + np.random.uniform(-5,5)
        elif (x_int<8) &(y_int<8):
            self.land_points = points[x_int + 1][y_int + 1] + np.random.uniform(-5,5)
        else:
            self.land_points = points[x_int-1][y_int-1] + np.random.uniform(-5,5)
    #    self.firstpoints_list = ([[[self.land_x * self.land_y * self.land_points for x in range(1, 100)] for x in range(1, 100)] for x in range(1, 100)])
        
    def firstpoints(self):
        return self.land_points
        
#print(make_firstpoints(data.points).land_points)

        
#isn't used , copied for triangulation.coloring
class make_color:
    def __init__(self, temp_data):
        #self.temperatures = temperatures
        #self.colors = colors
         if  temp_data < -30:
             self.color = '#191970'   #midnightblue
         elif (temp_data >= -30) & (temp_data < -20):
             self.color = '#0000ff'   #blue
         elif (temp_data >= -20) & (temp_data < -10):
             self.color = '#00bfff'   #deepskyblue
         elif (temp_data >= -10) & (temp_data < 0):
             self.color = '#00ffff'   #cyan
         elif (temp_data >= 0) & (temp_data < 10):
             self.color = '#adff2f'   #greenyellow
         elif (temp_data >= 10) & (temp_data < 20):
             self.color = '#ffff00'   #yellow
         elif (temp_data >= 20) & (temp_data < 30):
             self.color = '#ffa500'   #orange
         else:
             self.color = '#ff0000'   #red
    def color(self):
         return self.color


#isn't used
class edge_points:
    def __init__(self, edge):
        self.edge = edge
        self.x_min = edge[0][0]
        self.x_max = edge[2][0]
        self.y_min = edge[0][1]
        self.y_max = edge[1][1]
        self.xy = edge[0]
        self.width = self.x_max - self.x_min
        self.height = self.y_max - self.y_min
    
    def edge_points(self):
        return self.xy


#isn't used
def main():
    x = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    y = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    edge = ((2, 2), (2, 9), (9, 2), (9, 9))
    temperatures = [-50,-40,-30,-20,-10,0,10,20,30,40,50]
    colors = ['#191970', '#191970','#0000ff','#00bfff','#00ffff','#adff2f', '#ffff00','#ffa500','#ff0000','#ff0000']
    data = make_standard(x, y)
    land = edge_points(edge)
    color = make_color(temperatures, colors)
    ax = plt.axes()
    plt.contourf(data.xx, data.yy, data.points, color.temperatures, colors=color.colors)
    rec = patches.Rectangle(xy=land.xy, width=land.width, height=land.height, ec='#000000', fill=False)
    ax.add_patch(rec)
    # print(points)
    plt.show()

#function to return temperature
def temperature(first_data, xy_list):
    point = make_firstpoints(first_data, xy_list)
    temp = point.firstpoints()
    return temp


if __name__ == '__main__':
    main()
