from dcam560.Vzense_api_560 import *
import open3d as o3d
import cv2
camera = VzenseTofCam()

device_info = camera.connect()
camera.open(device_info,Open.URI)
camera.start_stream()

WDRMode = PsWDROutputMode()
WDRMode.totalRange = 2
WDRMode.range1 = 0
WDRMode.range1Count = 1
WDRMode.range2 = 2
WDRMode.range2Count = 2
WDRMode.range3 = 5
WDRMode.range3Count = 1
camera.set_WDR_style(WDR_Style.Fusion)
camera.set_WDR_output_mode(WDRMode)
camera.set_data_mode(DataMode.WDR_Depth)
#camera.set_compute_depth_correction(True)
#camera.get_WDR_pulse_count()
frameready = camera.read_frame()

if frameready and frameready.wdrDepth:
    frame = camera.get_frame(Frame.WDRDepth)
    fh,fw = int(frame.height),int(frame.width)
    print(fh,fw)
    print(frame.dataLen)
    save_file = "save/wdrfusa.png"
    depth = camera.gen_image(frame,Frame.Depth)
    cv2.imwrite(save_file,depth)
    print("Successfully saved")

    pointlist = camera.convert_to_world_vector(frame)
    filename = "C:\\Users\\schorrl\\Documents\\GitHub\\DCAM560\\DCAM560-API\\save\\pointwdr.txt"

    file = open(filename,"w")

    for i in range(frame.width*frame.height):
        if pointlist[i].z!=0 and pointlist[i].z!=65535 and pointlist[i].z < 1500:
            file.write("{0} {1} {2}\n".format(pointlist[i].x,pointlist[i].y,pointlist[i].z))

    file.close()
    print("Successfully saved")

cloud = o3d.io.read_point_cloud(filename,format='xyz')
mesh_frame = o3d.geometry.TriangleMesh.create_coordinate_frame(size=100, origin=[0,0,0])
o3d.visualization.draw_geometries([cloud,mesh_frame])
'''
if frameready and frameready.wdrDepth:
    frame = camera.get_frame(Frame.WDRDepth)
    pointlist = camera.convert_to_world_vector(frame)
    
    folder = os.getcwd() + "/save"
    filenamep = folder + "/wdrpoint.txt"

    if not os.path.exists(folder):
        print("Creating folder")
        os.makedirs(folder)

    file = open(filenamep,"w")

    for i in range(frame.width*frame.height):
        if pointlist[i].z!=0 and pointlist[i].z!=65535:
            file.write("{0} {1} {2}\n".format(pointlist[i].x,pointlist[i].y,pointlist[i].z))

    file.close()
    print("Successfully saved")
    
    folder = os.getcwd() + "/save"
    filenamed = folder + "/wdrdepth.txt"
    if not os.path.exists(folder):
        print("Creating save folder")
        os.makedirs(folder)
    file = open(filenamed,"w+")
    for i in range(int(frame.dataLen)):
        file.write(str(frame.pFrameData[i]) + ",")      
    file.close()

    fh,fw = int(frame.height),int(frame.width)
    print(fh,fw)
    print(frame.dataLen)
    save_file = "save/wdrfusa.png"
    depth = camera.gen_image(frame,Frame.Depth)
    cv2.imwrite(save_file,depth)
    print("Successfully saved")
    
    cloud = o3d.io.read_point_cloud(filenamep,format='xyz')
    o3d.visualization.draw_geometries([cloud])
'''
camera.stop_stream()
camera.close()
           