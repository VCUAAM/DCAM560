from API.Vzense_api_560 import *
import cv2,numpy as np

camera = VzenseTofCam()

device_info = camera.connect()
camera.open(device_info.uri,"URI")

if True:
    camera.start_stream()
    depthrange = camera.get_depth_range()

    ret, depth_max, value_min, value_max = camera.Ps2_GetMeasuringRange(PsDepthRange(depthrange.value))
    if  ret == 0:
        print("Ps2_GetMeasuringRange: ",depth_max,",",value_min,",",value_max)
    else:
        print("Ps2_GetMeasuringRange failed:",ret)

    print("/**********************************************************************/")
    print("M/m: Change data mode: input corresponding index in terminal")
    print("D/d: Change depth range: input corresponding index in terminal")
    print("R/r: Change the RGB resolution: input corresponding index in terminal")
    print("Esc: Program quit ")
    print("/**********************************************************************/")

    try:
        while 1:
            frameready = camera.read_frame()
    
            if frameready and frameready.depth:      
                depthframe = camera.get_frame("Depth")
                frametmp = np.ctypeslib.as_array(depthframe.pFrameData, (1, depthframe.width * depthframe.height * 2))
                frametmp.dtype = np.uint16
                frametmp.shape = (depthframe.height, depthframe.width)

                #convert ushort value to 0xff is just for display
                img = np.int32(frametmp)
                img = img*255/value_max
                img = np.clip(img, 0, 255)
                img = np.uint8(img)
                frametmp = cv2.applyColorMap(img, cv2.COLORMAP_RAINBOW)
                cv2.imshow("Depth Image", frametmp)
            if frameready and frameready.ir:
                irframe = camera.get_frame("IR")
                frametmp = np.ctypeslib.as_array(irframe.pFrameData, (1, irframe.width * irframe.height * 2))
                frametmp.dtype = np.uint16
                frametmp.shape = (irframe.height, irframe.width)
                img = np.int32(frametmp)
                img = img*255/3840
                img = np.clip(img, 0, 255)
                frametmp = np.uint8(img)
                cv2.imshow("IR Image", frametmp)
            if frameready and frameready.rgb:      
                rgbframe = camera.get_frame("RGB")
                frametmp = np.ctypeslib.as_array(rgbframe.pFrameData, (1, rgbframe.width * rgbframe.height * 3))
                frametmp.dtype = np.uint8
                frametmp.shape = (rgbframe.height, rgbframe.width,3)
                cv2.imshow("RGB Image", frametmp)
            key = cv2.waitKey(1)
            if  key == 27:
                cv2.destroyAllWindows()
                print("---end---")
                exit()
            elif  key == ord('m') or key == ord('M'):
                print("mode:")
                for index, element in enumerate(PsDataMode):
                    print(index, element)
                mode_input = input("choose:")
                for index, element in enumerate(PsDataMode):
                    if index == int(mode_input):
                        if index == 3:
                            WDRMode = PsWDROutputMode()
                            WDRMode.totalRange = 2
                            WDRMode.range1 = 0
                            WDRMode.range1Count = 1
                            WDRMode.range2 = 2
                            WDRMode.range2Count = 1
                            WDRMode.range3 = 5
                            WDRMode.range3Count = 1

                            camera.set_WDR_output_mode(WDRMode)
                            
                            camera.set_data_mode(element)
                            if  ret == 0:
                                print("Ps2_SetDataMode {} success".format(element))
                            else:
                                print("Ps2_SetDataMode {} failed {}".format(element,ret))
                        else:
                            ret = camera.Ps2_SetDataMode(element)
                            if  ret == 0:
                                print("Ps2_SetDataMode {} success".format(element))
                            else:
                                print("Ps2_SetDataMode {} failed {}".format(element,ret))
            elif  key == ord('r') or key == ord('R'):
                print("resolution:")
                for index, element in enumerate(PsResolution):
                    print(index, element)
                mode_input = input("choose:")
                for index, element in enumerate(PsResolution):
                    if  index == int(mode_input):
                        camera.Ps2_SetRGBResolution(element)
            elif  key == ord('d') or key == ord('D'):
                print("depth range:")
                for index, element in enumerate(PsDepthRange):
                    print(index, element)
                mode_input = input("choose:")
                for index, element in enumerate(PsDepthRange):
                    if  index == int(mode_input):
                        ret = camera.Ps2_SetDepthRange(element)
                        if  ret == 0:
                            print("Ps2_SetDepthRange {} success".format(element))
                            ret, depth_max, value_min, value_max = camera.Ps2_GetMeasuringRange(PsDepthRange(element))
                            if  ret == 0:
                                print(PsDepthRange(element)," Ps2_GetMeasuringRange: ",depth_max,",",value_min,",",value_max)
                            else:
                                print(PsDepthRange(element)," Ps2_GetMeasuringRange failed:",ret)

                        else:
                            print("Ps2_SetDepthRange {} failed {}".format(element,ret))
                       
    except Exception as e :
        print(e)
    finally:
        print('end')  
