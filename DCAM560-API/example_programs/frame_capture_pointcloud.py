import open3d as o3d

from dcam560.Vzense_api_560 import *

camera = VzenseTofCam()

camera.init()
camera.set_data_mode(DataMode.Depth_RGB)
camera.set_depth_range(Range.Near)
camera.set_depth_distortion_correction(True)
camera.set_depth_frame(Range.Near)
camera.set_compute_depth_correction(True)

"""while True:
    frameready = camera.read_frame()

    if frameready and frameready.depth:      
        frame = camera.get_frame(Frame.Depth)
        depth = camera.gen_image(frame,Frame.Depth)
        cv2.imwrite('save/mappeddepth_nearb.png',depth)
        print("Successfully saved")
        pointlist = camera.convert_to_world_vector(frame)
        filename = "C:\\Users\\schorrl\\Documents\\GitHub\\DCAM560\\DCAM560-API\\save\\point.txt"
        #filename = "C:\\Users\\schorrl\\Documents\\GitHub\\DCAM560\\DCAM560-API\\save\\point1.txt"
        file = open(filename,"w")

        for i in range(frame.width*frame.height):
            if pointlist[i].z!=0 and pointlist[i].z!=65535 and pointlist[i].z < 1500:
                file.write("{0} {1} {2}\n".format(pointlist[i].x,pointlist[i].y,pointlist[i].z))

        file.close()
        print("Successfully saved")
        break"""

camera.stop_stream() 
camera.close() 


filename = "C:\\Users\\schorrl\\Documents\\GitHub\\DCAM560\\DCAM560-API\\save\\point.txt"
filename1 = "C:\\Users\\schorrl\\Documents\\GitHub\\DCAM560\\DCAM560-API\\save\\point1.txt"
cloud = o3d.io.read_point_cloud(filename,format='xyz')
cloud1 = o3d.io.read_point_cloud(filename1,format='xyz')
mesh_frame = o3d.geometry.TriangleMesh.create_coordinate_frame(size=100, origin=[0,0,0])
o3d.visualization.draw_geometries([cloud,cloud1,mesh_frame])

           