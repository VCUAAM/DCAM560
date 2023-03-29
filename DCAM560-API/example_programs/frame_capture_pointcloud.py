import open3d as o3d

from dcam560.Vzense_api_560 import *

camera = VzenseTofCam()

camera.init()
camera.set_data_mode(DataMode.Depth_RGB)
camera.set_depth_range(Range.Mid)
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
        if pointlist[i].z!=0 and pointlist[i].z!=65535 and pointlist[i].z < 1500:
            file.write("{0} {1} {2}\n".format(pointlist[i].x,pointlist[i].y,pointlist[i].z))

    file.close()
    print("Successfully saved")

cloud = o3d.io.read_point_cloud(filename,format='xyz')
mesh_frame = o3d.geometry.TriangleMesh.create_coordinate_frame(size=100, origin=[0,0,0])
o3d.visualization.draw_geometries([cloud,mesh_frame])
camera.stop_stream() 
camera.close() 
           