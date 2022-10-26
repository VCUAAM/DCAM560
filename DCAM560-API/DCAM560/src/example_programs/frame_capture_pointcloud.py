from API.Vzense_api_560 import *
import open3d as o3d
import numpy as np

camera = VzenseTofCam()

device_info = camera.connect()
camera.open(device_info.uri,Open.URI)
camera.start_stream()   

print(Open(1))
frameready = camera.read_frame()

if frameready and frameready.depth:      
    frame = camera.get_frame(Frame.Depth)
    pointlist = camera.convert_to_world_vector(frame)
    folder = os.getcwd() + "/save"
    filename = folder + "/point.txt"

    if not os.path.exists(folder):
        print("Creating folder")
        os.makedirs(folder)

    file = open(filename,"w")

    for i in range(frame.width*frame.height):
        if pointlist[i].z!=0 and pointlist[i].z!=65535:
            file.write("{0} {1} {2}\n".format(pointlist[i].x,pointlist[i].y,pointlist[i].z))

    file.close()
    print("Successfully saved")

cloud = o3d.io.read_point_cloud(filename,format='xyz')
o3d.visualization.draw_geometries([cloud])
camera.stop_stream() 
camera.close() 
           