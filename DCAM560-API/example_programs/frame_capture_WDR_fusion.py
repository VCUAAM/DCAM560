from dcam560.Vzense_api_560 import *
import open3d as o3d
import cv2
camera = VzenseTofCam()

device_info = camera.connect()
camera.open(device_info.uri,Open.URI)
camera.start_stream()
#camera.set_slave_mode(True)

WDRMode = PsWDROutputMode()
WDRMode.totalRange = 2
WDRMode.range1 = 2
WDRMode.range1Count = 1
WDRMode.range2 = 5
WDRMode.range2Count = 1
WDRMode.range3 = 5
WDRMode.range3Count = 1
    
camera.set_WDR_output_mode(WDRMode)
camera.set_data_mode(DataMode.WDR_Depth)
camera.set_WDR_style(WDR_Style.Fusion)
#camera.set_depth_range(Range.Far)
deprange = Range((camera.get_depth_range()).value)
depth_max, value_min, value_max = camera.get_measuring_range(deprange)

frameready = camera.read_frame()

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

camera.stop_stream()
camera.close()
           