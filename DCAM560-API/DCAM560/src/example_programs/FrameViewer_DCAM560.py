from API.Vzense_api_560 import *
import cv2,numpy as np

datamodes = ["Depth and RGB","IR and RGB","Depth, IR, and RGB","WDR"]
ranges = ["Near","Mid","Far","XFar"]
resos = ["640x480","1600x1200","800x600"]
camera = VzenseTofCam()

device_info = camera.connect()
camera.open(device_info.uri,Open.URI)

if True:
    camera.start_stream()
    camera.set_depth_range(Range.Far)
    camera.set_depth_distortion_correction(False)
    depthrange = camera.get_depth_range()

    depth_max, value_min, value_max = camera.get_measuring_range()
    print("Measuring Range: ",depth_max,",",value_min,",",value_max)
        

    print("/**********************************************************************/")
    print("M/m: Change data mode: input corresponding index in terminal")
    print("D/d: Change depth range: input corresponding index in terminal")
    print("R/r: Change the RGB resolution: input corresponding index in terminal")
    print("Esc: Program quit ")
    print("/**********************************************************************/")

    while True:
        try:
            frameready = camera.read_frame()
    
            if frameready and frameready.depth:      
                depthframe = camera.get_frame(Frame.Depth)
                depth = camera.gen_image(depthframe, Frame.Depth,value_max)
                cv2.imshow("Depth Image", depth)
            if frameready and frameready.ir:
                irframe = camera.get_frame(Frame.IR)
                ir = camera.gen_image(irframe, Frame.IR)
                cv2.imshow("IR Image", ir)
            if frameready and frameready.rgb:      
                rgbframe = camera.get_frame(Frame.RGB)
                rgb = camera.gen_image(rgbframe,Frame.RGB)
                cv2.imshow("RGB Image", rgb)

            key = cv2.waitKey(10)

            if key == 27:
                cv2.destroyAllWindows()
                print("---end---")
                exit()

            elif key == ord('m') or key == ord('M'):
                print("Available Data Modes:")
                for index, element in enumerate(datamodes):
                    print(index, element)
                mode_input = int(input("Type number of desired datamode:\n"))
                if mode_input == 3:
                    WDRMode = PsWDROutputMode()
                    WDRMode.totalRange = 3
                    WDRMode.range1 = 0
                    WDRMode.range1Count = 1
                    WDRMode.range2 = 2
                    WDRMode.range2Count = 1
                    WDRMode.range3 = 5
                    WDRMode.range3Count = 1
                    camera.set_WDR_style(WDR_Style.Fusion)
                    camera.set_WDR_output_mode(WDRMode)
                    camera.set_data_mode(DataMode.WDR_Depth)
                else:
                    camera.set_data_mode(DataMode(mode_input))
    
            elif key == ord('r') or key == ord('R'):
                print("Available Resolutions:")
                for index, element in enumerate(resos):
                    print(index, element)
                mode_input = int(input("Type number of desired resolution:\n"))
                camera.set_RGB_resolution(Reso(mode_input))

            elif key == ord('d') or key == ord('D'):
                print("Available Depth Ranges:")
                for index, element in enumerate(ranges):
                    print(index + 1, element)
                mode_input = int(input("Type number of desired range:\n"))
                if isinstance(mode_input,int) and mode_input < 5:
                    if mode_input == 4:
                        mode_input = 6
                    mode_input -= 1
                    camera.set_depth_range(mode_input)
                depth_max, value_min, value_max = camera.get_measuring_range(Range(mode_input))
                       
        except Exception as e:
            print(e)
        finally:
            time.sleep(.001)
