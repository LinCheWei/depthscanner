import compas
import pyrealsense2 as pyrs
import numpy as np
from scipy.interpolate import griddata
from timeit import default_timer as timer

_pipe = None
_pipe = pyrs.pipeline()

def get_pipe():
    global _pipe
    return _pipe


def testfunc():
    
    print('Scanning..')

    # set the resolution
    xres = 1280
    yres = 720
    
    # Declare pointcloud object, for calculating pointclouds and texture mappings
    pc = pyrs.pointcloud()
    # We want the points object to be persistent so we can display the last cloud when a frame drops
    points = pyrs.points()
    pipe = get_pipe()
    # Create a config and configure the pipeline to stream
    config = pyrs.config()
    #set resolution
    #config.enable_stream(pyrs.stream.depth, xres, yres, pyrs.format.z16, 30)
    #Start streaming 
    
    profile = pipe.start()
    #profile = pipe.start(config)

    try:
        # Wait for the next set of frames from the camera
        frames = pipe.wait_for_frames()
        # Fetch depth frames
        depth = frames.get_depth_frame()
        # calc pointcloud
        points = pc.calculate(depth)
        pts = np.asarray(points.get_vertices())
        pts = pts.reshape(1280,720)

        x_range = 100
        y_range = 100
        x_start = xres/2-1
        y_start = yres/2-1
        x_count = 20
        y_count = 20
        x_step = x_range/x_count
        y_step = y_range/y_count

        ptss = []
        
        for i in range(x_count):
            for j in range(y_count):
                pt = pts[int(x_start+(i*x_step))][int(y_start+(j*y_step))]
                ptss.append([p*1000 for p in pt])

        print('Points aquired..')
        print(ptss)
        return ptss

    finally:  ### dont stop it
        pipe.stop()
        print("Scan Completed")

testfunc()