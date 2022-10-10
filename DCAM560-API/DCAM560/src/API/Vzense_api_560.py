import platform,time,os,re
from API.Vzense_enums_560 import *
from API.Vzense_types_560 import * 

class VzenseTofCam():
    device_handle = c_void_p(0)
    session = c_uint(0)
    sensors = {
        "depth": PsSensorType.PsDepthSensor,
        "RGB": PsSensorType.PsRgbSensor
    }
    
    def __init__(self):
        if platform.system() == 'Linux':
            libpath = (os.path.abspath(os.path.dirname(os.getcwd()) + os.path.sep))+"/Lib/libvzense_api.so"
            self.ps_cam_lib = cdll.LoadLibrary(libpath)
        elif platform.system() == 'Windows':          
            libpath = (os.path.abspath(os.path.dirname(os.getcwd()) + os.path.sep)) + "/Lib/vzense_api.dll"
            self.ps_cam_lib = cdll.LoadLibrary(libpath)    
        else:
            print('Unsupported OS')
            exit()
        
        self.gCallbackFuncList = []
        self.device_handle = c_void_p(0)
        self.session = c_uint(0)
        self.ps_cam_lib.Ps2_Initialize()

    def __del__(self):
        self.ps_cam_lib.Ps2_Shutdown()

    def connect(self):
        camera_count,retry_count,device_info = 0,0,PsDeviceInfo()

        while camera_count == 0 and retry_count < 20:
            retry_count += 1
            camera_count = self.get_device_count()
            time.sleep(1)
            print("Searching for camera, attempt",retry_count)

        if camera_count > 1:
            status,device_infolist = self.get_device_list_info(camera_count)
            print("Multiple cameras found on network, connecting to first one")
            device_info = device_infolist[0] 
        elif camera_count == 1:
            status,device_info = self.get_device_info()
        else: 
            print("No camera found on network")
            exit()

        if status != 0 or PsConnectStatus.Connected.value != device_info.status:
            print('Failed to connect to camera: ' + str(status))  
            print("Device connection status:",device_info.status)  
            print("Program connection status:",PsConnectStatus.Connected.value)
            exit()
        else:
            print("Camera connected")
            print("Camera URI: " + (re.search("'(.*):",str(device_info.uri))).group(1))
            print("Alias: " + (re.search("'(.*)'",str(device_info.alias))).group(1))
            #print("Connection status: " + str(device_info.status))   
        return device_info
    
    def get_device_count(self):
        count = c_int()
        self.ps_cam_lib.Ps2_GetDeviceCount(byref(count))
        return count.value
    
    def get_device_list_info(self, cam_count = 1):
        tmp  = PsDeviceInfo* cam_count
        device_infolist = tmp() 
        return self.ps_cam_lib.Ps2_GetDeviceListInfo(device_infolist, cam_count),device_infolist
    
    def get_device_info(self, cam_index = 0):
        device_info = PsDeviceInfo()
        return self.ps_cam_lib.Ps2_GetDeviceInfo(byref(device_info), cam_index), device_info
         
    def open(self, key = c_char_p(), method = "URI"):
        match method:
            case "URI":
                status = self.ps_cam_lib.Ps2_OpenDevice(key, byref(self.device_handle))
            case "alias":
                status = self.ps_cam_lib.Ps2_OpenDeviceByAlias(key, byref(self.device_handle))
            case "IP":
                status = self.ps_cam_lib.Ps2_OpenDeviceByIP(key, byref(self.device_handle))
            case other:
                print("Invalid opening method")
                return PsReturnStatus.PsRetInputPointerIsNull

        if status != 0:
            print('Failed to open: ' + str(status))
            quit()
    
        print("Camera opened successfully")

    def close(self):
        status = self.ps_cam_lib.Ps2_CloseDevice(byref(self.device_handle))
        if  status == 0:
            print("Device closed successfully")
        else:
            print('Failed to close: ' + str(status))   

    def start_stream(self):
        status = self.ps_cam_lib.Ps2_StartStream(self.device_handle, self.session)
        if status == 0:
            print("Stream started successfully")
        else:
            print("Failed to start stream:",status)     
         
    def stop_stream(self):
        status = self.ps_cam_lib.Ps2_StopStream(self.device_handle, self.session)
        if status == 0:
            print("Stream stopped successfully")
        else:
            print('Failed to stop stream: ' + str(status)) 

    def read_frame(self):
        frameready = PsFrameReady()
        status = self.ps_cam_lib.Ps2_ReadNextFrame(self.device_handle, self.session, byref(frameready))

        if status !=0:
            print("Failed to ready frame: ",status)
            return None

        return frameready
        
    def get_frame(self, ftype = "Depth"):   
        match ftype:
            case "Depth":
                frametype = PsFrameType.PsDepthFrame
            case "RGB":
                frametype = PsFrameType.PsRGBFrame
            case "IR":
                frametype = PsFrameType.PsIRFrame
            case other:
                print("%s is not an acceptable frame type" %(ftype))
                quit()
        psframe = PsFrame()
        status = self.ps_cam_lib.Ps2_GetFrame(self.device_handle, self.session, frametype.value, byref(psframe))
        
        if status != 0:
            print("%s error:" %(ftype),status)  

        return psframe
   
    def set_data_mode(self, mode = "depRGB"):
        match mode:
            case "depRGB":
                datamode = PsDataMode.PsDepthAndRGB_30
            case "IR":
                datamode = PsDataMode.PsDepthAndIRAndRGB_30
            case "IRRGB":
                datamode = PsDataMode.PsIRAndRGB_30
            case "WDR":
                datamode = PsDataMode.PsWDR_Depth
            case other:
                print("%s is not an acceptable data mode" %(mode))
                quit()
        status = self.ps_cam_lib.Ps2_SetDataMode(self.device_handle, self.session, datamode.value)

        if status != 0:  
            print("Failed to set datamode:",status)
        else:
            print("Set data mode to %s" %(mode))
        
    def get_data_mode(self):
        datamode = c_int(0)
        status = self.ps_cam_lib.Ps2_GetDataMode(self.device_handle, self.session, byref(datamode))
        if status != 0:  
            print("Failed to set datamode:",status)
            return None
        print("Datamode:",datamode.value)
        return datamode
    
    def set_depth_range(self, range = "Near"):
        match range:
            case "Near": 
                depthrange = PsDepthRange.PsNearRange
            case "XNear":
                depthrange = PsDepthRange.PsXNearRange
            case "XXNear":
                depthrange = PsDepthRange.PsXXNearRange
            case "Mid":
                depthrange = PsDepthRange.PsMidRange
            case "XMid":
                depthrange = PsDepthRange.PsXMidRange
            case "XXMid":
                depthrange = PsDepthRange.PsXXMidRange
            case "Far":
                depthrange = PsDepthRange.PsFarRange
            case "XFar":
                depthrange = PsDepthRange.PsXFarRange
            case "XXFar":
                depthrange = PsDepthRange.PsXXFarRange
            case other:
                print("%s is not an acceptable depth range" %(range))
                quit()
        status = self.ps_cam_lib.Ps2_SetDepthRange(self.device_handle, self.session, depthrange.value)
        if status != 0:  
            print("Failed to set depth range:", status)
        else:
            print("Set depth range to %s" %(range))
       
    def get_depth_range(self):
        depthrange = c_int(0)
        status = self.ps_cam_lib.Ps2_GetDepthRange(self.device_handle, self.session, byref(depthrange))
        if status != 0:
            print("Failed to get depth range:",status)
            return None
        print("Depth Range:",depthrange.value)
        return depthrange

    def set_threshold(self, threshold = c_uint16(20)):
        status = self.ps_cam_lib.Ps2_SetThreshold(self.device_handle, self.session, threshold)
        if status != 0:  
            print("Failed to set threshold:",status)
               
    def get_threshold(self):
        thres = c_uint16()
        status = self.ps_cam_lib.Ps2_GetThreshold(self.device_handle, self.session, byref(thres)) 
        if status != 0:
            print("Failed to get threshold: ",status)
            return None
        print("Threshold:",thres.value)
        return thres

    def set_pulse_count(self, pulsecount = c_uint16(20)):
        status = self.ps_cam_lib.Ps2_SetPulseCount(self.device_handle, self.session, pulsecount)
        if status != 0:
            print("Failed to set pulse count: ",status)
     
    def get_pulse_count(self):
        pulsecount = c_uint16()
        status = self.ps_cam_lib.Ps2_GetPulseCount(self.device_handle, self.session, byref(pulsecount))
        if status != 0:
            print("Failed to get pulse count: ",status)
            return None
        print("Pulse count:",pulsecount.value)
        return pulsecount.value
    
    def set_GMM_gain(self, gmmgain = c_uint16(20)):
        gmmgain_ = PsGMMGain()
        gmmgain_.gmmgain = gmmgain
        gmmgain_.option = 0
        status = self.ps_cam_lib.Ps2_SetGMMGain(self.device_handle, self.session, gmmgain_)
        if status != 0:
            print("Failed to set GMM gain: ",status)
     
    def get_GMM_gain(self):
        gmmgain = c_uint16(1)
        status = self.ps_cam_lib.Ps2_GetGMMGain(self.device_handle, self.session, byref(gmmgain))
        if status != 0:
            print("Failed to get GMM gain: ",status)
            return None
        print("GMM Gain:",gmmgain.value)
        return gmmgain.value

    def get_camera_parameters(self, sensorType = "depth"):
        CameraParameters = PsCameraParameters()

        match sensorType:
            case "depth": 
                sensorTypeObj = PsSensorType.PsDepthSensor
            case "RGB": 
                sensorTypeObj = PsSensorType.PsRgbSensor

        status = self.ps_cam_lib.Ps2_GetCameraParameters(self.device_handle, self.session, sensorTypeObj.value, byref(CameraParameters))

        if status != 0:
            print("Failed to get %s camera parameters:",status %(sensorType))
            return None

        return CameraParameters

    def get_camera_extrinsic_parameters(self):
        CameraExtrinsicParameters = PsCameraExtrinsicParameters()
        status = self.ps_cam_lib.Ps2_GetCameraExtrinsicParameters(self.device_handle, self.session, byref(CameraExtrinsicParameters))
        if status != 0: 
            print("Failed to get extrinsic parameters:",status)
            return None

        return CameraExtrinsicParameters
           
    def set_color_pixel_format(self, format = "BGR888"):
        match format:
            case "BGR888":
                    pixelFormat = PsPixelFormat.PsPixelFormatBGR888
            case "RGB888":
                    pixelFormat = PsPixelFormat.PsPixelFormatRGB888
            case "MM16":
                    pixelFormat = PsPixelFormat.PsPixelFormatDepthMM16
            case "Gray16":
                    pixelFormat = PsPixelFormat.PsPixelFormatGray16
            case "Gray8":
                    pixelFormat = PsPixelFormat.PsPixelFormatGray8
            case other:
                print("%s is not an acceptable pixel format" %(format))
                quit()
        status = self.ps_cam_lib.Ps2_SetColorPixelFormat(self.device_handle, self.session, pixelFormat.value) 
        if status == 0: 
            print("Set pixel format to %s:" %(format))
        else:
            print("Failed to set pixel color format:",status)
       
    def set_RGB_resolution(self, reso = "640x480"):
        print(reso)
        if reso == "800x600":
            print("yes")
        match reso:
            case "640x480":
                resolution = PsResolution.PsRGB_Resolution_640_480
            case "1600x1200":
                resolution = PsResolution.PsRGB_Resolution_1600_1200
            case "800x600":
                resolution = PsResolution.PsRGB_Resolution_800_600
            case other:
                print("%s is not an acceptable resolution" %(reso))
                quit()
        status = self.ps_cam_lib.Ps2_SetRGBResolution(self.device_handle, self.session, resolution.value) 
        if status != 0:  
            print("Failed to set RGB resolution:",status)
            quit()
        else:
            print("Set RGB resolution to %s:" %(reso),status)
     
    def get_RGB_resolution(self):
        resolution = c_int(0)
        status = self.ps_cam_lib.Ps2_GetRGBResolution(self.device_handle, self.session, byref(resolution)), resolution

        if status != 0: 
            print("Failed to get RGB resolution:",status)
            return None

        return resolution

    def set_WDR_output_mode(self, WDRMode = PsWDROutputMode()):
        status = self.ps_cam_lib.Ps2_SetWDROutputMode(self.device_handle, self.session, byref(WDRMode)) 
        if status != 0:  
            print("Failed to set WDR output mode:",status)
     
    def get_WDR_output_mode(self):
        WDRMode = PsWDROutputMode()
        status = self.ps_cam_lib.Ps2_GetWDROutputMode(self.device_handle, self.session, byref(WDRMode)), WDRMode

        if status != 0: 
            print("Failed to get WDR ouput mode:",status)
            return None

        return WDRMode

    def set_WDR_style(self, wdrStyle = PsWDRStyle.PsWDR_FUSION):
        status =  self.ps_cam_lib.Ps2_SetWDRStyle(self.device_handle, self.session, wdrStyle.value) 
        if status != 0:
            print("Failed to set WDR style:",status) 
                
    def get_measuring_range(self, depthrange = "Near"):
        MeasuringRange = PsMeasuringRange()
        #if depthrange == "Near":
            #print("yes")
        match depthrange:
            case "Near": 
                range = PsDepthRange.PsNearRange
            case "XNear":
                range = PsDepthRange.PsXNearRange
            case "XXNear":
                range = PsDepthRange.PsXXNearRange
            case "Mid":
                range = PsDepthRange.PsMidRange
            case "XMid":
                range = PsDepthRange.PsXMidRange
            case "XXMid":
                range = PsDepthRange.PsXXMidRange
            case "Far":
                range = PsDepthRange.PsFarRange
            case "XFar":
                range = PsDepthRange.PsXFarRange
            case "XXFar":
                range = PsDepthRange.PsXXFarRange
            case other:
                print("%s is not an acceptable depth range" %(depthrange))
                quit()
        status = self.ps_cam_lib.Ps2_GetMeasuringRange(self.device_handle, self.session, range.value, byref(MeasuringRange))
        if status == 0:
            if range == PsDepthRange.PsNearRange or range == PsDepthRange.PsXNearRange or range == PsDepthRange.PsXXNearRange:
                return MeasuringRange.depthMaxNear, MeasuringRange.effectDepthMinNear, MeasuringRange.effectDepthMaxNear
            elif range == PsDepthRange.PsMidRange or range == PsDepthRange.PsXMidRange or range == PsDepthRange.PsXXMidRange:
                return MeasuringRange.depthMaxMid, MeasuringRange.effectDepthMinMid, MeasuringRange.effectDepthMaxMid
            elif range == PsDepthRange.PsFarRange or range == PsDepthRange.PsXFarRange or range == PsDepthRange.PsXXFarRange:
                return MeasuringRange.depthMaxFar, MeasuringRange.effectDepthMinFar, MeasuringRange.effectDepthMaxFar
        else:
            print("Failed to get measuring range:",status)
            return 0, 0, 0

    def convert_to_world_vector(self, depthFrame = PsFrame()): 
        len = depthFrame.width*depthFrame.height
        tmp =PsVector3f*len
        pointlist = tmp()
        status = self.ps_cam_lib.Ps2_ConvertDepthFrameToWorldVector(self.device_handle, self.session, depthFrame,pointlist)
        if status != 0:
            print("Ps2_ConvertDepthFrameToWorldVector failed:",status)
            return None    
        return pointlist

    def set_synchronize(self, enabled = c_bool(True)): 
        status = self.ps_cam_lib.Ps2_SetSynchronizeEnabled(self.device_handle, self.session, enabled)
        if status == 0:
            self.get_synchronize()
        else:
            print("Failed to set synchronization status",status)
    
    def get_synchronize(self): 
        enabled = c_bool(True)
        status = self.ps_cam_lib.Ps2_GetSynchronizeEnabled(self.device_handle, self.session, byref(enabled))
        if status == 0:
            print("Synchronization status:",enabled)
        else:
            print("Failed to get synchronization status",status)
    
    def set_depth_distortion_correction(self, enabled = c_bool(True)): 
        status = self.ps_cam_lib.Ps2_SetDepthDistortionCorrectionEnabled(self.device_handle, self.session, enabled)
        if status == 0:
            self.get_depth_distortion_correction()
        else:
            print("Failed to set depth distortion correction",status)
    
    def get_depth_distortion_correction(self): 
        enabled = c_bool(True)
        status = self.ps_cam_lib.Ps2_GetDepthDistortionCorrectionEnabled(self.device_handle, self.session, byref(enabled))
        if status == 0:
            print("Depth distortion correction status:",enabled)
        else:
            print("Failed to get depth distortion correction status",status)
    
    def set_RGB_distortion_correction(self, enabled = c_bool(True)): 
        status = self.ps_cam_lib.Ps2_SetRGBDistortionCorrectionEnabled(self.device_handle, self.session, enabled)
        if status == 0:
            self.get_RGB_distortion_correction()
        else:
            print("Failed to set RGB distortion correction",status)

    def get_RGB_distortion_correction(self): 
        enabled = c_bool(True)
        status = self.ps_cam_lib.Ps2_GetRGBDistortionCorrectionEnabled(self.device_handle, self.session, byref(enabled))
        if status == 0:
            print("RGB distortion correction enabled:",enabled)
        else:
            print("Failed to get RGB distortion correction status",status)

    def set_compute_depth_corection(self, enabled = c_bool(True)): 
        status = self.ps_cam_lib.Ps2_SetComputeRealDepthCorrectionEnabled(self.device_handle, self.session, enabled)
        if status == 0:
            self.get_compute_depth_correction()
        else:
            print("Failed to set compute depth correction",status)

    def get_compute_depth_correction(self): 
        enabled = c_bool(True)
        status = self.ps_cam_lib.Ps2_GetComputeRealDepthCorrectionEnabled(self.device_handle, self.session, byref(enabled))
        if status == 0:
            print("Compute depth correction enabled:",enabled)
        else:
            print("Failed to get compute depth correction status",status)

    def set_depth_frame(self, enabled = c_bool(True)): 
        status = self.ps_cam_lib.Ps2_SetDepthFrameEnabled(self.device_handle, self.session, enabled)
        if status != 0:
            print("Failed to set depth frame",status)

    def set_IR_frame(self, enabled = c_bool(True)): 
        status = self.ps_cam_lib.Ps2_SetIrFrameEnabled(self.device_handle, self.session, enabled)
        if status != 0:
            print("Failed to set IR frame",status)

    def set_RGB_frame(self, enabled = c_bool(True)): 
        status = self.ps_cam_lib.Ps2_SetRgbFrameEnabled(self.device_handle, self.session, enabled)
        if status != 0:
            print("Failed to set RGB frame",status)

    def set_image_mirror(self, type = c_int32(0)): 
        status = self.ps_cam_lib.Ps2_SetImageMirror(self.device_handle, self.session, type)
        if status != 0:
            print("Failed to mirror image",status)

    def set_image_rotation(self, type = c_int32(0)): 
        status = self.ps_cam_lib.Ps2_SetImageRotation(self.device_handle, self.session, type)
        if status != 0:
            print("Failed to set image rotation",status)

    def set_mapper(self, mode = "Depth", en = True):
        match en:
            case True:
                enabled = c_bool(True)
            case False:
                enabled = c_bool(False)
            case other:
                print("%s is not a boolean state" %(en))
                quit()
        match mode:
            case "Depth": 
                status = self.ps_cam_lib.Ps2_SetMapperEnabledRGBToDepth(self.device_handle, self.session, enabled)
            case "RGB":
                status = self.ps_cam_lib.Ps2_SetMapperEnabledDepthToRGB(self.device_handle, self.session, enabled)
            case other:
                print("%s is not an acceptable mapper" %(mode))
                quit()
        if status == 0:
            print("Set mapper to %s" %(mode))
        else:
            print("Failed to set mapper to %s:" %(mode),status)
   
    def get_mapper(self): 
        enabled = c_bool(True)
        status = self.ps_cam_lib.Ps2_GetMapperEnabledDepthToRGB(self.device_handle, self.session, byref(enabled))
        if status == 0:
            print("Depth to RGB Mapper:",enabled)
        elif status != 0:
            print("Failed to get mapper",status)
            return None
        enabled = c_bool(True)
        status = self.ps_cam_lib.Ps2_GetMapperEnabledRGBToDepth(self.device_handle, self.session, byref(enabled))
        if status == 0:
            print("RGB to Depth Mapper:",enabled)
        elif status != 0:
            print("Failed to get mapper",status)
            return None

    def hot_plug_status_callback(self,callbackfunc= c_void_p): 
        callbackFunc_= CFUNCTYPE(c_void_p,POINTER(PsDeviceInfo),c_int32)(callbackfunc)    
        self.gCallbackFuncList.append(callbackFunc_)
        return self.ps_cam_lib.Ps2_SetHotPlugStatusCallback(callbackFunc_)

    def hot_plug_state_callback_logic(self, type_struct, state = c_int32(0)):
        if state == 0:
            print((re.search("'(.*)'",str(str(type_struct.contents.alias)))).group(1) + " added")
            self.open(type_struct.contents.uri)
            self.start_stream()
        else:
            print((re.search("'(.*)'",str(str(type_struct.contents.alias)))).group(1) + "removed")
            self.stop_stream()
            self.close()

    def set_hot_plug_status(self):
        self.hot_plug_status_callback(self.hot_plug_state_callback_logic)

    def set_WDR_pulse_count(self,wdrpulseCount = PsWDRPulseCount()): 
        status = self.ps_cam_lib.Ps2_SetWDRPulseCount(self.device_handle, self.session, wdrpulseCount)
        if status == 0:
            self.get_WDR_pulse_count()
        else:
            print("Failed to set WDR pulse count",status)

    def get_WDR_pulse_count(self): 
        wdrpulseCount = PsWDRPulseCount()
        status = self.ps_cam_lib.Ps2_GetWDRPulseCount(self.device_handle, self.session, byref(wdrpulseCount))
        if status == 0:
            print("WDR pulse count:",wdrpulseCount)
        else:
            print("Failed to get WDR pulse count",status)

    def serial_number(self): 
        tmp = c_char * 64
        sn = tmp()
        status = self.ps_cam_lib.Ps2_GetSerialNumber(self.device_handle, self.session, sn, 63)
        if status == 0:
            print("Device Serial Number:",str(sn.value))
        else:
            print("Failed to get serial number: ",status)

    def firmware_version(self): 
        tmp = c_char * 64
        fw = tmp()
        status = self.ps_cam_lib.Ps2_GetFirmwareVersionNumber(self.device_handle, self.session, fw, 63)
        if status == 0:
            print("Firmware Version:", str(fw.value))
        else:
            print("Failed to get firmware version: ", status)
        return 

    def set_DSP(self, enabled = c_bool(True)): 
        status = self.ps_cam_lib.Ps2_SetDSPEnabled(self.device_handle, self.session, enabled)
        if status == 0:
            self.get_DSP()
        else:
            print("Failed to set DSP",status)
    
    def get_DSP(self): 
        enabled = c_bool(True)
        status = self.ps_cam_lib.Ps2_GetDSPEnabled(self.device_handle, self.session, byref(enabled))
        if status == 0:
            print("DSP enabled:",enabled)
        else:
            print("Failed to get DSP state",status)

    def set_slave_mode(self, en = True):
        match en:
            case True:
                enabled = c_bool(True)
            case False:
                enabled = c_bool(False)
            case other:
                print("%s is not a boolean state" %(en))
                quit() 
        status = self.ps_cam_lib.Ps2_SetSlaveModeEnabled(self.device_handle, self.session, enabled)
        if status != 0:  
            print("Failed to set slave mode:", status)
    
    def set_ToF_frame_rate(self, rate = c_uint8(30)): 
        status = self.ps_cam_lib.Ps2_SetTofFrameRate(self.device_handle, self.session, rate)
        if status != 0:  
            print("Failed to set ToF frame rate:",status)
    
    def get_ToF_frame_rate(self): 
        rate = c_uint8(30)
        status = self.ps_cam_lib.Ps2_GetTofFrameRate(self.device_handle, self.session, byref(rate))
        if status != 0:  
            print("Failed to get ToF frame rate:",status)
        else:
            print("ToF frame rate: %i" %(rate))

    def set_standby(self, enabled = c_bool(True)): 
        status = self.ps_cam_lib.Ps2_SetStandByEnabled(self.device_handle, self.session, enabled)
        if status != 0:  
            print("Failed to set standby:", status)
    
    def set_wait_time_of_read_frame(self, time = c_uint16(33)): 
        status = self.ps_cam_lib.Ps2_SetWaitTimeOfReadNextFrame(self.device_handle, self.session, time)
        if status != 0:
            print("Failed to set wait time of read frame",status)
    
    def SDK_version(self): 
        tmp = c_char * 64
        version = tmp()
        status = self.ps_cam_lib.Ps2_GetSDKVersion(version, 63),version.value
        if status == 0:
            print("Device SDK version:",str(version.value))
        else:
            print("Failed to get SDK version: ",status)
 
    def get_mapped_point_depth_to_RGB(self, depthPoint = PsDepthVector3(),rgbSize = PsVector2u16(640,480)): 
        PosInRGB = PsVector2u16()
        status = self.ps_cam_lib.Ps2_GetMappedPointDepthToRGB(self.device_handle, self.session, depthPoint, rgbSize, byref(PosInRGB))
        if status == 0:
            print("Mapped point depth:",PosInRGB)
        else:
            print("Failed to get mapped point depth",status)

    def reboot_camera(self): 
        status = self.ps_cam_lib.Ps2_RebootCamera(self.device_handle, self.session)
        if status != 0:  
            print("Failed to reboot camera:",status)

    def enable_legacy_algorithm(self, enabled = c_bool(True)): 
        status = self.ps_cam_lib.Ps2_SetLegacyAlgorithmicEnabled(self.device_handle, self.session, enabled)
        if status != 0:  
            print("Failed to enable legacy algorithm:",status)
        else:
            print("Enabled legacy algorithm")
     
    def set_slave_trigger(self): 
        status = self.ps_cam_lib.Ps2_SetSlaveTrigger(self.device_handle, self.session)
        if status != 0:  
            print("Failed to set slave trigger:", status)
     
    def IP(self, uri=c_char_p()):
        tmp = c_char * 17
        ip = tmp()
        status = self.ps_cam_lib.Ps2_GetDeviceIP(uri, ip)

        if status == 0:
            print("Device IP:",str(ip.value))
        else:
            print("Failed to get IP: ",status)
    
    def MAC_address(self):
        tmp = c_char * 18
        mac = tmp()
        status = self.ps_cam_lib.Ps2_GetDeviceMAC(self.device_handle, self.session, mac), mac.value
        if status == 0:
            print("Device MAC address:",str(mac.value))
        else:
            print("Failed to get MAC address: ",status)
         
    def set_RGB_brightness(self, value = c_char(0)):
        status = self.ps_cam_lib.Ps2_SetRGBBrightness(self.device_handle, self.session, value)
        if status == 0:
            self.get_RGB_brightness()
        else:
            print("Failed to set RGB brightness",status)
         
    def get_RGB_brightness(self):
        value = c_char(0)
        status = self.ps_cam_lib.Ps2_GetRGBBrightness(self.device_handle, self.session, byref(value))
        if status == 0:
            print("RGB brightness:",value)
        else:
            print("Failed to get RGB brightness",status)

    def set_RGB_exposure(self, value = c_ubyte(0)):
        status = self.ps_cam_lib.Ps2_SetRGBExposure(self.device_handle, self.session, value)
        if status == 0:
            self.get_RGB_exposure()
        else:
            print("Failed to set RGB brightness",status)
         
    def get_RGB_exposure(self):
        value = c_ubyte(0)
        status = self.ps_cam_lib.Ps2_GetRGBExposure(self.device_handle, self.session, byref(value))
        if status == 0:
            print("RGB exposure:",value)
        else:
            print("Failed to get RGB brightness",status)
    
    def set_RGB_frequency(self, value = c_ubyte(0)):
        status = self.ps_cam_lib.Ps2_SetRGBFrequencyOfPowerLine(self.device_handle, self.session, value)
        if status == 0:
            self.get_RGB_frequency()
        else:
            print("Failed to set RGB frequency",status)
         
    def get_RGB_frequency(self):
        value = c_ubyte(0)
        status = self.ps_cam_lib.Ps2_GetRGBFrequencyOfPowerLine(self.device_handle, self.session, byref(value))
        if status == 0:
            print("RGB Frequency:",value)
        else:
            print("Failed to get RGB frequency",status)
    
    def set_spatial_filter(self, enabled = c_bool(True)): 
        status = self.ps_cam_lib.Ps2_SetSpatialFilterEnabled(self.device_handle, self.session, enabled)
        if status == 0:
            self.get_spatial_filter()
        else:
            print("Failed to set spatial filter",status)
    
    def get_spatial_filter(self): 
        enabled = c_bool(True)
        status = self.ps_cam_lib.Ps2_GetSpatialFilterEnabled(self.device_handle, self.session, byref(enabled))
        if status == 0:
            print("Spatial filter enabled:",enabled)
        else:
            print("Failed to get spatial filter status",status)

    def set_time_filter(self, enabled = c_bool(True)): 
        status = self.ps_cam_lib.Ps2_SetTimeFilterEnabled(self.device_handle, self.session, enabled)
        if status == 0:
            self.set_time_filter()
        else:
            print("Failed to set time filter status",status)
    
    def get_time_filter(self): 
        enabled = c_bool(True)
        status = self.ps_cam_lib.Ps2_GetTimeFilterEnabled(self.device_handle, self.session, byref(enabled)),enabled
        if status == 0:
            print("Time filter enabled:",enabled)
        else:
            print("Failed to get tiue filter status",status)
    
    def set_confidence_filter(self, enabled = c_bool(True)): 
        status = self.ps_cam_lib.Ps2_SetConfidenceFilterEnabled(self.device_handle, self.session, enabled)
        if status == 0:
            self.get_confidence_filter()
        else:
            print("Failed to set confidence filter",status)

    def get_confidence_filter(self): 
        enabled = c_bool(True)
        status = self.ps_cam_lib.Ps2_GetConfidenceFilterEnabled(self.device_handle, self.session, byref(enabled))
        if status == 0:
            print("Confidence filter enabled:",enabled)
        else:
            print("Failed to get confidence filter status",status)

    def set_confidence_filter_threshold(self, threshold = c_uint16(20)):
        status = self.ps_cam_lib.Ps2_SetConfidenceFilterThreshold(self.device_handle, self.session, threshold) 
        if status == 0:
            self.get_confidence_filter_threshold()
        else:
            print("Failed to set confidence filter threshold",status)

    def get_confidence_filter_threshold(self):
        thres = c_uint16()
        status = self.ps_cam_lib.Ps2_GetConfidenceFilterThreshold(self.device_handle, self.session, byref(thres))
        if status == 0:
            print("Confidence filter threshold:",thres.value)
        else:
            print("Failed to get confidence filter threshold",status)

    def set_WDR_confidence_filter_threshold(self, wdrconfidencethreshold = PsWDRConfidenceThreshold()):
        status = self.ps_cam_lib.Ps2_SetWDRConfidenceFilterThreshold(self.device_handle, self.session, wdrconfidencethreshold) 
        if status == 0:
            self.get_WDR_confidence_filter_threshold()
        else:
            print("Failed to set WDR confidence filter threshold",status)

    def get_WDR_confidence_filter_threshold(self):
        wdrconfidencethreshold = PsWDRConfidenceThreshold()
        status = self.ps_cam_lib.Ps2_GetConfidenceFilterThreshold(self.device_handle, self.session, byref(wdrconfidencethreshold))
        if status == 0:
            print("WDR confidence filter threshold:",wdrconfidencethreshold)
        else:
            print("Failed to get WDR confidence filter threshold",status)
