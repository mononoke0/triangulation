from matplotlib import pyplot as plt
import numpy as np
import triangulation
import random
import matplotlib.patches as patches
import first_data

from scipy.spatial import Delaunay, delaunay_plot_2d, Voronoi, voronoi_plot_2d
import matplotlib.pyplot as plt
import numpy as np
#import triangulation.py and first_data.py

LEFT_CLICK = 1
RIGHT_CLICK = 3


def update(event_handler):
    """post processing updating artist objects"""

    def event_handler_decorated(self, *args, **kwargs):
        event_handler(self, *args, **kwargs)
        self.plot_objects.set_data(self.xs, self.ys)
        self.fig.canvas.draw()
#        fig, ax = plt.subplots()
    return event_handler_decorated


def visible_selector(action):
    def actions_decorated(self, x, y):
        action(self, x, y)
        self.selected_object.set_visible(True)
        self.selected_object.set_data(x, y)
    return actions_decorated


def unvisible_selector(action):
    def action_decorated(self):
        action(self)
        self.selected_object.set_visible(False)
    return action_decorated


class PointHandler:

    def __init__(self, fig, ax,delaunaytriangles, mesh_temp): 
        # add delaunaytriangles for triangulation.py and mesh_temp for first_data.py
        self.fig = fig
        self.ax = ax
        self.delaunaytriangles = delaunaytriangles
        self.mesh_temp = mesh_temp
        # coords
        self.xs = np.array([])
        self.ys = np.array([])
        # artists
        self.moving_object, = ax.plot([0, 0], 'go', visible=False)
        self.selected_object, = ax.plot([0, 0], 'ro', ms=12, visible=False)
        self.plot_objects, = ax.plot(
            self.xs, self.ys, 'bo', picker=5, mew=2, mec='g')
        # picking flag
        self.is_picking_object = False

    @update
    def on_pressed(self, event):
        """generate point where mouse pushed with left click"""
        if event.button != LEFT_CLICK:
            return
        if event.inaxes != self.ax:
            return
        if self.is_picking_object:
            return
        self.add_point(event.xdata, event.ydata)

    @update
    def on_motion(self, event):
        """drag point"""
        if not self.is_picking_object:
            return
        self.moving_object.set_visible(True)
        self.moving_object.set_data([event.xdata], [event.ydata])

    @update
    def on_picked(self, event):
        print('in\n')
        """select point which mouse does"""
        if event.artist != self.plot_objects:
            return
        # find nearest object from position which is mouse clicked
     
        mouse_x = event.mouseevent.xdata
        mouse_y = event.mouseevent.ydata
        distances = np.hypot(mouse_x - self.xs[event.ind],
                             mouse_y - self.ys[event.ind])
        argmin = distances.argmin()
        self.select_index = event.ind[argmin]

        if event.mouseevent.button == RIGHT_CLICK:          
            # remove point where mouse pushed with right click
            print('remove\n')
            self.remove_point()

        if event.mouseevent.button == LEFT_CLICK:           
            self.selected_object.set_data(
                self.xs[self.select_index], self.ys[self.select_index])
            self.is_picking_object = True
            

    @update
    def on_release(self, event):
        if self.is_picking_object:
            self.move_point(event.xdata, event.ydata)
        # reset state
        self.is_picking_object = False
        self.moving_object.set_visible(False)

    @visible_selector
    def add_point(self, x, y):       
        self.xs = np.append(self.xs, x)
        self.ys = np.append(self.ys, y)
        print(self.xs,self.ys)
        add = [x,y] #for triangulation.add
        temp =first_data.temperature(self.mesh_temp, add) # find temperature of add point using first_data.py
        triangulation.add(self.ax, self.delaunaytriangles,add, temp) #update triangulation using triangulation.py

    @visible_selector
    def move_point(self, x, y):
        remove = [self.xs[self.select_index], self.ys[self.select_index]] #memorize remove point
        add = [x, y] #memorize add point
        temp =first_data.temperature(self.mesh_temp, add) #find temperature of add point
        triangulation.move(self.ax, self.delaunaytriangles,remove, add, temp) #update triangulation using triangulation.py
        self.xs[self.select_index] = x
        self.ys[self.select_index] = y
        #print(self.xs,self.ys)

    @unvisible_selector
    def remove_point(self): 
        remove = [self.xs[self.select_index], self.ys[self.select_index]] #memorize remove point 
        self.xs = np.delete(self.xs, self.select_index)
        self.ys = np.delete(self.ys, self.select_index)
        print('self.xs: ',self.xs,'self.ys: ', self.ys)
        triangulation.remove(self.ax, self.delaunaytriangles,remove) #update triangulation using triangulation.py
 

def main():
    # make screen (changed [0,100] to [0,10])
    figure = plt.figure()
    axes = plt.axes()
    axes.set_xlim(0,10)
    axes.set_ylim(10,0)
    A = np.array([0,0])
    B = np.array([10,0])
    C = np.array([10,10])
    D = np.array([0,10])

    patch1 = patches.Polygon(xy = [A,B,C,D],
                edgecolor='black',
                facecolor='white',
                linewidth=1.6)

    axes.add_patch(patch1)


    plotlist = []
    #edge point
    point = triangulation.Point(15/10, 27/10, 0)
    plotlist.append(point)
    point = triangulation.Point(27/10,15/10 , 0)
    plotlist.append(point)
    point = triangulation.Point(15/10, 80/10, 0)
    plotlist.append(point)
    point = triangulation.Point(30/10, 90/10, 0)
    plotlist.append(point)
    point = triangulation.Point(78/10, 89/10, 20)
    plotlist.append(point)
    point = triangulation.Point(81/10, 80/10, 20)
    plotlist.append(point)
    point = triangulation.Point(75/10, 15/10, 20)
    plotlist.append(point)
    point = triangulation.Point(81/10, 21/10, 20)
    plotlist.append(point)

#    for counter in range(1):
#        point = triangulation.Point(random.uniform(15,80), random.uniform(15,80), random.uniform(-20,40) )
#        plotlist.append(point)


    upperleft = triangulation.Point(0,0, -20)
    bottomright = triangulation.Point(10,10, 30)
    xy_list = [4, 4]
    
    #making lattice point (9*9) using first_data.py
    first_data_ins = first_data.make_standard()
    mesh_temp = first_data_ins.standard()
        
    #initalize triangulation
    delaunaytriangles = triangulation.DelaunayTriangles(plotlist, upperleft, bottomright)
    triangleset = delaunaytriangles.DelaunayTriangulation(upperleft, bottomright)
    for triangle in triangleset:
        points = [[triangle.point1.x, triangle.point1.y], [triangle.point2.x, triangle.point2.y], [triangle.point3.x, triangle.point3.y]]
        color = triangulation.coloring((triangle.point1.temp + triangle.point2.temp + triangle.point3.temp)/3)
        delaunaytriangles.pat.append(patches.Polygon(xy=points, closed=True, edgecolor='black',
                facecolor=color))
    for patch2 in delaunaytriangles.pat:
        axes.add_patch(patch2)    
    
    #mouse event
    axes.set_title(
        "Left click to build point. Right click to remove point.")
    pthandler = PointHandler(figure, axes,delaunaytriangles, mesh_temp)
    # regist event handler
    # the order of mpl_connect is important
    figure.canvas.mpl_connect("button_press_event", pthandler.on_pressed)
    figure.canvas.mpl_connect("motion_notify_event", pthandler.on_motion)
    figure.canvas.mpl_connect("pick_event", pthandler.on_picked)
    figure.canvas.mpl_connect("button_release_event", pthandler.on_release)
    plt.show()


if __name__ == '__main__':
    main()
