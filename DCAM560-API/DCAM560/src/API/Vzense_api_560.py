import platform,time,os,re,cv2
import numpy as np
from API.Vzense_enums_560 import *
from API.Vzense_types_560 import * 

class VzenseTofCam():
    device_handle = c_void_p(0)
    session = c_uint(0)
    enable = {
        True: "Enabled",
        False: "Disabled"
    }
    sensors = {
        "depth": Sensor.Depth,
        "RGB": Sensor.RGB
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

        if status != 0 or Status.Connected.value != device_info.status:
            print('Failed to connect to camera: ' + str(Error(status)))  
            print("Device connection status:",device_info.status)  
            print("Program connection status:",Status.Connected.value)
            exit()
        else:
            print("Camera connected")
            #print("Camera URI: " + (re.search("'(.*):",str(device_info.uri))).group(1))
            #print("Alias: " + (re.search("'(.*)'",str(device_info.alias))).group(1))
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
         
    def open(self, key = c_char_p(), method = Open.URI):
        match method:
            case Open.URI:
                status = self.ps_cam_lib.Ps2_OpenDevice(key, byref(self.device_handle))
            case Open.alias:
                status = self.ps_cam_lib.Ps2_OpenDeviceByAlias(key, byref(self.device_handle))
            case Open.IP:
                status = self.ps_cam_lib.Ps2_OpenDeviceByIP(key, byref(self.device_handle))
            case other:
                print("Invalid opening method")
                return Error.Input_Pointer_Null

        if status != 0:
            print('Failed to open: ' + str(Error(status)))
            quit()

    def close(self):
        status = self.ps_cam_lib.Ps2_CloseDevice(byref(self.device_handle))
        if status == 0:
            time.sleep(.01)
            #print("Device closed successfully")
        else:
            print('Failed to close: ' + str(Error(status)))   

    def start_stream(self):
        status = self.ps_cam_lib.Ps2_StartStream(self.device_handle, self.session)
        if status == 0:
            print("Stream started successfully")
        else:
            print("Failed to start stream:",str(Error(status)))     
         
    def stop_stream(self):
        status = self.ps_cam_lib.Ps2_StopStream(self.device_handle, self.session)
        if status == 0:
            print("Stream stopped successfully")
        else:
            print('Failed to stop stream: ' + str(Error(status))) 

    def read_frame(self):
        frameready = PsFrameReady()
        status = self.ps_cam_lib.Ps2_ReadNextFrame(self.device_handle, self.session, byref(frameready))

        if status !=0:
            print("Failed to ready frame: ",str(Error(status)))
            return None

        return frameready
        
    def get_frame(self, frametype = Frame.Depth):   
        psframe = PsFrame()
        status = self.ps_cam_lib.Ps2_GetFrame(self.device_handle, self.session, frametype.value, byref(psframe))
        
        if status != 0:
            print("%s error:" %(frametype),str(Error(status)))  

        return psframe
    
    def gen_image(self, frame, frametype = Frame.Depth, max_range = 1):
        fw,fh = frame.width,frame.height
        match frametype:
            case Frame.Depth:
                frametmp = np.ctypeslib.as_array(frame.pFrameData, (1, 2*fw*fh))
                frametmp.dtype = np.uint16
                frametmp.shape = (fh, fw)
                img = np.int32(frametmp)*255/max_range
                img = np.uint8(np.clip(img, 0, 255))
                frametmp = cv2.applyColorMap(img, cv2.COLORMAP_RAINBOW)
                #hsv = cv2.cvtColor(frametmp,cv2.COLOR_BGR2HSV)
                bgr = frametmp.copy()
                r,p = np.array([0,0,255]),np.array([255,0,170])
                mask_r,mask_p = cv2.inRange(bgr,r,r),cv2.inRange(bgr,p,p)
                #frametmp[mask_r > 0] = (255,255,255)
                frametmp[mask_p > 0] = (0,0,0)
                return frametmp
            case Frame.RGB:
                fw,fh = frame.width,frame.height
                frametmp = np.ctypeslib.as_array(frame.pFrameData, (1, 3*fw*fh))
                frametmp.dtype = np.uint8
                frametmp.shape = (fh,fw,3)
                return frametmp
            case Frame.IR:
                frametmp = np.ctypeslib.as_array(frame.pFrameData, (1, 2*fw*fh))
                frametmp.dtype = np.uint16
                frametmp.shape = (fh, fw)
                img = np.int32(frametmp)
                img = img*255/3840
                img = np.clip(img, 0, 255)
                frametmp = np.uint8(img)
                return frametmp

    def set_data_mode(self, datamode = DataMode.Depth_RGB):
        status = self.ps_cam_lib.Ps2_SetDataMode(self.device_handle, self.session, datamode.value)

        if status != 0:  
            print("Failed to set datamode:",str(Error(status)))
        else:
            print("Set data mode to %s" %(datamode))
        
    def get_data_mode(self):
        datamode = c_int(0)
        status = self.ps_cam_lib.Ps2_GetDataMode(self.device_handle, self.session, byref(datamode))
        if status != 0:  
            print("Failed to set datamode:",str(Error(status)))
            return None
        print("Datamode:",datamode.value)
        return datamode
    
    def set_depth_range(self, depthrange = Range.Near):
        if isinstance(depthrange,int):
            depthrange = Range(depthrange)
        status = self.ps_cam_lib.Ps2_SetDepthRange(self.device_handle, self.session, depthrange.value)
        if status != 0:  
            print("Failed to set depth range:", str(Error(status)))
        else:
            print("Set depth range to %s" %(str(depthrange)))
       
    def get_depth_range(self):
        depthrange = c_int(0)
        status = self.ps_cam_lib.Ps2_GetDepthRange(self.device_handle, self.session, byref(depthrange))
        if status != 0:
            print("Failed to get depth range:",str(Error(status)))
            return None
        print("Depth Range:",Range(depthrange.value))
        return Range(depthrange.value)

    def set_threshold(self, threshold = c_uint16(20)):
        status = self.ps_cam_lib.Ps2_SetThreshold(self.device_handle, self.session, threshold)
        if status != 0:  
            print("Failed to set threshold:",str(Error(status)))
               
    def get_threshold(self):
        thres = c_uint16()
        status = self.ps_cam_lib.Ps2_GetThreshold(self.device_handle, self.session, byref(thres)) 
        if status != 0:
            print("Failed to get threshold: ",str(Error(status)))
            return None
        print("Threshold:",thres.value)
        return thres

    def set_pulse_count(self, pulsecount = c_uint16(20)):
        status = self.ps_cam_lib.Ps2_SetPulseCount(self.device_handle, self.session, pulsecount)
        if status != 0:
            print("Failed to set pulse count: ",str(Error(status)))
     
    def get_pulse_count(self):
        pulsecount = c_uint16()
        status = self.ps_cam_lib.Ps2_GetPulseCount(self.device_handle, self.session, byref(pulsecount))
        if status != 0:
            print("Failed to get pulse count: ",str(Error(status)))
            return None
        print("Pulse count:",pulsecount.value)
        return pulsecount.value
    
    def set_GMM_gain(self, gmmgain = c_uint16(20)):
        gmmgain_ = PsGMMGain()
        gmmgain_.gmmgain = gmmgain
        gmmgain_.option = 0
        status = self.ps_cam_lib.Ps2_SetGMMGain(self.device_handle, self.session, gmmgain_)
        if status != 0:
            print("Failed to set GMM gain: ",str(Error(status)))
     
    def get_GMM_gain(self):
        gmmgain = c_uint16(1)
        status = self.ps_cam_lib.Ps2_GetGMMGain(self.device_handle, self.session, byref(gmmgain))
        if status != 0:
            print("Failed to get GMM gain: ",str(Error(status)))
            return None
        print("GMM Gain:",gmmgain.value)
        return gmmgain.value

    def get_camera_parameters(self, sensorTypeObj = Sensor.Depth):
        CameraParameters = PsCameraParameters()
        status = self.ps_cam_lib.Ps2_GetCameraParameters(self.device_handle, self.session, sensorTypeObj.value, byref(CameraParameters))

        if status != 0:
            print("Failed to get %s camera parameters:",str(Error(status)) %(sensorTypeObj))
            return None

        return CameraParameters

    def get_camera_extrinsic_parameters(self):
        CameraExtrinsicParameters = PsCameraExtrinsicParameters()
        status = self.ps_cam_lib.Ps2_GetCameraExtrinsicParameters(self.device_handle, self.session, byref(CameraExtrinsicParameters))
        if status != 0: 
            print("Failed to get extrinsic parameters:",str(Error(status)))
            return None

        return CameraExtrinsicParameters
           
    def set_color_pixel_format(self, pixelFormat = Pixel.RGB888):
        status = self.ps_cam_lib.Ps2_SetColorPixelFormat(self.device_handle, self.session, pixelFormat.value) 
        if status == 0: 
            print("Set pixel format to %s:" %(format))
        else:
            print("Failed to set pixel color format:",str(Error(status)))
       
    def set_RGB_resolution(self, resolution = Reso._640x480):
        status = self.ps_cam_lib.Ps2_SetRGBResolution(self.device_handle, self.session, resolution.value) 
        if status != 0:  
            print("Failed to set RGB resolution:",str(Error(status)))
            quit()
        else:
            print("Set RGB resolution to: %s" %(str(resolution)))
     
    def get_RGB_resolution(self):
        resolution = c_int(0)
        status = self.ps_cam_lib.Ps2_GetRGBResolution(self.device_handle, self.session, byref(resolution)), resolution

        if status != 0: 
            print("Failed to get RGB resolution:",str(Error(status)))
            return None

        return resolution

    def set_WDR_output_mode(self, WDRMode = PsWDROutputMode()):
        status = self.ps_cam_lib.Ps2_SetWDROutputMode(self.device_handle, self.session, byref(WDRMode)) 
        if status != 0:  
            print("Failed to set WDR output mode:",str(Error(status)))
     
    def get_WDR_output_mode(self):
        WDRMode = PsWDROutputMode()
        status = self.ps_cam_lib.Ps2_GetWDROutputMode(self.device_handle, self.session, byref(WDRMode)), WDRMode

        if status != 0: 
            print("Failed to get WDR ouput mode:",str(Error(status)))
            return None

        return WDRMode

    def set_WDR_style(self, wdrStyle = WDR_Style.Fusion):
        status =  self.ps_cam_lib.Ps2_SetWDRStyle(self.device_handle, self.session, wdrStyle.value) 
        if status != 0:
            print("Failed to set WDR style:",str(Error(status))) 
                
    def get_measuring_range(self, range = Range.Near):
        MeasuringRange = PsMeasuringRange()
        status = self.ps_cam_lib.Ps2_GetMeasuringRange(self.device_handle, self.session, range.value, byref(MeasuringRange))
        if status == 0:
            if range == Range.Near or range == Range.XNear or range == Range.XXNear:
                return MeasuringRange.depthMaxNear, MeasuringRange.effectDepthMinNear, MeasuringRange.effectDepthMaxNear
            elif range == Range.Mid or range == Range.XMid or range == Range.XXMid:
                return MeasuringRange.depthMaxMid, MeasuringRange.effectDepthMinMid, MeasuringRange.effectDepthMaxMid
            elif range == Range.Far or range == Range.XFar or range == Range.XXFar:
                return MeasuringRange.depthMaxFar, MeasuringRange.effectDepthMinFar, MeasuringRange.effectDepthMaxFar
        else:
            print("Failed to get measuring range:",str(Error(status)))
            return 0, 0, 0

    def convert_to_world_vector(self, depthFrame = PsFrame()): 
        len = depthFrame.width*depthFrame.height
        tmp = PsVector3f*len
        pointlist = tmp()
        status = self.ps_cam_lib.Ps2_ConvertDepthFrameToWorldVector(self.device_handle, self.session, depthFrame,pointlist)
        if status != 0:
            print("Failed to convert depth frame to world vector:",str(Error(status)))
            return None    
        return pointlist

    def set_synchronize(self, enabled = True): 
        status = self.ps_cam_lib.Ps2_SetSynchronizeEnabled(self.device_handle, self.session, c_bool(enabled))
        if status == 0:
            self.get_synchronize()
        else:
            print("Failed to set synchronization status",str(Error(status)))
    
    def get_synchronize(self, enabled = True): 
        status = self.ps_cam_lib.Ps2_GetSynchronizeEnabled(self.device_handle, self.session, byref(c_bool(enabled)))
        if status == 0:
            print("Synchronization status:",self.enable[enabled])
        else:
            print("Failed to get synchronization status",str(Error(status)))
    
    def set_depth_distortion_correction(self, enabled = True): 
        status = self.ps_cam_lib.Ps2_SetDepthDistortionCorrectionEnabled(self.device_handle, self.session, c_bool(enabled))
        if status == 0:
            self.get_depth_distortion_correction(enabled)
        else:
            print("Failed to set depth distortion correction",str(Error(status)))
    
    def get_depth_distortion_correction(self,enabled = True): 
        status = self.ps_cam_lib.Ps2_GetDepthDistortionCorrectionEnabled(self.device_handle, self.session, byref(c_bool(enabled)))
        if status == 0:
            print("Depth distortion correction status:",self.enable[enabled])
        else:
            print("Failed to get depth distortion correction status",str(Error(status)))
    
    def set_RGB_distortion_correction(self, enabled = True): 
        status = self.ps_cam_lib.Ps2_SetRGBDistortionCorrectionEnabled(self.device_handle, self.session, c_bool(enabled))
        if status == 0:
            self.get_RGB_distortion_correction(enabled)
        else:
            print("Failed to set RGB distortion correction",str(Error(status)))

    def get_RGB_distortion_correction(self, enabled = True): 
        status = self.ps_cam_lib.Ps2_GetRGBDistortionCorrectionEnabled(self.device_handle, self.session, byref(c_bool(enabled)))
        if status == 0:
            print("RGB distortion correction enabled:",self.enable[enabled])
        else:
            print("Failed to get RGB distortion correction status",str(Error(status)))

    def set_compute_depth_corection(self, enabled = True): 
        status = self.ps_cam_lib.Ps2_SetComputeRealDepthCorrectionEnabled(self.device_handle, self.session, c_bool(enabled))
        if status == 0:
            self.get_compute_depth_correction()
        else:
            print("Failed to set compute depth correction:",str(Error(status)))

    def get_compute_depth_correction(self, enabled = True): 
        status = self.ps_cam_lib.Ps2_GetComputeRealDepthCorrectionEnabled(self.device_handle, self.session, byref(c_bool(enabled)))
        if status == 0:
            print("Compute depth correction enabled:",self.enable[enabled])
        else:
            print("Failed to get compute depth correction status:",str(Error(status)))

    def set_depth_frame(self, enabled = True): 
        status = self.ps_cam_lib.Ps2_SetDepthFrameEnabled(self.device_handle, self.session, c_bool(enabled))
        if status != 0:
            print("Failed to set depth frame:",str(Error(status)))

    def set_IR_frame(self, enabled = True): 
        status = self.ps_cam_lib.Ps2_SetIrFrameEnabled(self.device_handle, self.session, c_bool(enabled))
        if status != 0:
            print("Failed to set IR frame:",str(Error(status)))

    def set_RGB_frame(self, enabled = True): 
        status = self.ps_cam_lib.Ps2_SetRgbFrameEnabled(self.device_handle, self.session, c_bool(enabled))
        if status != 0:
            print("Failed to set RGB frame:",str(Error(status)))

    def set_image_mirror(self, type = c_int32(0)): 
        status = self.ps_cam_lib.Ps2_SetImageMirror(self.device_handle, self.session, type)
        if status != 0:
            print("Failed to mirror image:",str(Error(status)))

    def set_image_rotation(self, type = c_int32(0)): 
        status = self.ps_cam_lib.Ps2_SetImageRotation(self.device_handle, self.session, type)
        if status != 0:
            print("Failed to set image rotation:",str(Error(status)))

    def set_mapper(self, mode = Sensor.Depth, enabled = True):
        match mode:
            case Sensor.Depth: 
                status = self.ps_cam_lib.Ps2_SetMapperEnabledRGBToDepth(self.device_handle, self.session, c_bool(enabled))
            case Sensor.RGB:
                status = self.ps_cam_lib.Ps2_SetMapperEnabledDepthToRGB(self.device_handle, self.session, c_bool(enabled))
            case other:
                print("%s is not an acceptable mapper" %(mode))
                quit()
        if status == 0:
            print("Set mapper to %s" %(mode))
        else:
            print("Failed to set mapper to %s:" %(mode),str(Error(status)))
   
    def get_mapper(self): 
        enabled = c_bool(True)
        status = self.ps_cam_lib.Ps2_GetMapperEnabledDepthToRGB(self.device_handle, self.session, byref(enabled))
        if status == 0:
            print("Depth to RGB Mapper:",enabled)
        elif status != 0:
            print("Failed to get mapper:",str(Error(status)))
            return None
        enabled = c_bool(True)
        status = self.ps_cam_lib.Ps2_GetMapperEnabledRGBToDepth(self.device_handle, self.session, byref(enabled))
        if status == 0:
            print("RGB to Depth Mapper:",enabled)
        elif status != 0:
            print("Failed to get mapper:",str(Error(status)))
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
            print("Failed to set WDR pulse count",str(Error(status)))

    def get_WDR_pulse_count(self): 
        wdrpulseCount = PsWDRPulseCount()
        status = self.ps_cam_lib.Ps2_GetWDRPulseCount(self.device_handle, self.session, byref(wdrpulseCount))
        if status == 0:
            print("WDR pulse count:",wdrpulseCount)
        else:
            print("Failed to get WDR pulse count",str(Error(status)))

    def serial_number(self): 
        tmp = c_char * 64
        sn = tmp()
        status = self.ps_cam_lib.Ps2_GetSerialNumber(self.device_handle, self.session, sn, 63)
        if status == 0:
            print("Device Serial Number:",str(sn.value))
        else:
            print("Failed to get serial number: ",str(Error(status)))

    def firmware_version(self): 
        tmp = c_char * 64
        fw = tmp()
        status = self.ps_cam_lib.Ps2_GetFirmwareVersionNumber(self.device_handle, self.session, fw, 63)
        if status == 0:
            print("Firmware Version:", str(fw.value))
        else:
            print("Failed to get firmware version: ", str(Error(status)))
        return 

    def set_DSP(self, enabled = True): 
        status = self.ps_cam_lib.Ps2_SetDSPEnabled(self.device_handle, self.session, c_bool(enabled))
        if status == 0:
            self.get_DSP()
        else:
            print("Failed to set DSP:",str(Error(status)))
    
    def get_DSP(self): 
        enabled = c_bool(True)
        status = self.ps_cam_lib.Ps2_GetDSPEnabled(self.device_handle, self.session, byref(enabled))
        if status == 0:
            print("DSP enabled:",enabled)
        else:
            print("Failed to get DSP state:",str(Error(status)))

    def set_slave_mode(self, enabled = True):
        status = self.ps_cam_lib.Ps2_SetSlaveModeEnabled(self.device_handle, self.session, c_bool(enabled))
        if status != 0:  
            print("Failed to set slave mode:", str(Error(status)))
    
    def set_ToF_frame_rate(self, rate = c_uint8(30)): 
        status = self.ps_cam_lib.Ps2_SetTofFrameRate(self.device_handle, self.session, rate)
        if status != 0:  
            print("Failed to set ToF frame rate:",str(Error(status)))
    
    def get_ToF_frame_rate(self): 
        rate = c_uint8(30)
        status = self.ps_cam_lib.Ps2_GetTofFrameRate(self.device_handle, self.session, byref(rate))
        if status != 0:  
            print("Failed to get ToF frame rate:",str(Error(status)))
        else:
            print("ToF frame rate: %i" %(rate))

    def set_standby(self, enabled = True): 
        status = self.ps_cam_lib.Ps2_SetStandByEnabled(self.device_handle, self.session, c_bool(enabled))
        if status != 0:  
            print("Failed to set standby:", str(Error(status)))
    
    def set_wait_time_of_read_frame(self, time = c_uint16(33)): 
        status = self.ps_cam_lib.Ps2_SetWaitTimeOfReadNextFrame(self.device_handle, self.session, time)
        if status != 0:
            print("Failed to set wait time of read frame:",str(Error(status)))
    
    def SDK_version(self): 
        tmp = c_char * 64
        version = tmp()
        status = self.ps_cam_lib.Ps2_GetSDKVersion(version, 63),version.value
        if status == 0:
            print("Device SDK version:",str(version.value))
        else:
            print("Failed to get SDK version: ",str(Error(status)))
 
    def get_mapped_point_depth_to_RGB(self, depthPoint = PsDepthVector3(),rgbSize = PsVector2u16(640,480)): 
        PosInRGB = PsVector2u16()
        status = self.ps_cam_lib.Ps2_GetMappedPointDepthToRGB(self.device_handle, self.session, depthPoint, rgbSize, byref(PosInRGB))
        if status == 0:
            print("Mapped point depth:",PosInRGB)
        else:
            print("Failed to get mapped point depth:",str(Error(status)))

    def reboot_camera(self): 
        status = self.ps_cam_lib.Ps2_RebootCamera(self.device_handle, self.session)
        if status != 0:  
            print("Failed to reboot camera:",str(Error(status)))

    def enable_legacy_algorithm(self, enabled = True): 
        status = self.ps_cam_lib.Ps2_SetLegacyAlgorithmicEnabled(self.device_handle, self.session, c_bool(enabled))
        if status != 0:  
            print("Failed to enable legacy algorithm:",str(Error(status)))
        else:
            print("Enabled legacy algorithm")
     
    def set_slave_trigger(self): 
        status = self.ps_cam_lib.Ps2_SetSlaveTrigger(self.device_handle, self.session)
        if status != 0:  
            print("Failed to set slave trigger:", str(Error(status)))
     
    def IP(self, uri=c_char_p()):
        tmp = c_char * 17
        ip = tmp()
        status = self.ps_cam_lib.Ps2_GetDeviceIP(uri, ip)

        if status == 0:
            print("Device IP:",str(ip.value))
        else:
            print("Failed to get IP: ",str(Error(status)))
    
    def MAC_address(self):
        tmp = c_char * 18
        mac = tmp()
        status = self.ps_cam_lib.Ps2_GetDeviceMAC(self.device_handle, self.session, mac), mac.value
        if status == 0:
            print("Device MAC address:",str(mac.value))
        else:
            print("Failed to get MAC address: ",str(Error(status)))
         
    def set_RGB_brightness(self, value = c_char(0)):
        status = self.ps_cam_lib.Ps2_SetRGBBrightness(self.device_handle, self.session, value)
        if status == 0:
            self.get_RGB_brightness()
        else:
            print("Failed to set RGB brightness:",str(Error(status)))
         
    def get_RGB_brightness(self):
        value = c_char(0)
        status = self.ps_cam_lib.Ps2_GetRGBBrightness(self.device_handle, self.session, byref(value))
        if status == 0:
            print("RGB brightness:",value)
        else:
            print("Failed to get RGB brightness:",str(Error(status)))

    def set_RGB_exposure(self, value = c_ubyte(0)):
        status = self.ps_cam_lib.Ps2_SetRGBExposure(self.device_handle, self.session, value)
        if status == 0:
            self.get_RGB_exposure()
        else:
            print("Failed to set RGB brightness:",str(Error(status)))
         
    def get_RGB_exposure(self):
        value = c_ubyte(0)
        status = self.ps_cam_lib.Ps2_GetRGBExposure(self.device_handle, self.session, byref(value))
        if status == 0:
            print("RGB exposure:",value)
        else:
            print("Failed to get RGB brightness:",str(Error(status)))
    
    def set_RGB_frequency(self, value = c_ubyte(0)):
        status = self.ps_cam_lib.Ps2_SetRGBFrequencyOfPowerLine(self.device_handle, self.session, value)
        if status == 0:
            self.get_RGB_frequency()
        else:
            print("Failed to set RGB frequency:",str(Error(status)))
         
    def get_RGB_frequency(self):
        value = c_ubyte(0)
        status = self.ps_cam_lib.Ps2_GetRGBFrequencyOfPowerLine(self.device_handle, self.session, byref(value))
        if status == 0:
            print("RGB Frequency:",value)
        else:
            print("Failed to get RGB frequency:",str(Error(status)))
    
    def set_spatial_filter(self, enabled = True): 
        status = self.ps_cam_lib.Ps2_SetSpatialFilterEnabled(self.device_handle, self.session, c_bool(enabled))
        if status == 0:
            self.get_spatial_filter()
        else:
            print("Failed to set spatial filter:",str(Error(status)))
    
    def get_spatial_filter(self): 
        enabled = c_bool(True)
        status = self.ps_cam_lib.Ps2_GetSpatialFilterEnabled(self.device_handle, self.session, byref(enabled))
        if status == 0:
            print("Spatial filter enabled:",enabled)
        else:
            print("Failed to get spatial filter status:",str(Error(status)))

    def set_time_filter(self, enabled = True): 
        status = self.ps_cam_lib.Ps2_SetTimeFilterEnabled(self.device_handle, self.session, c_bool(enabled))
        if status == 0:
            self.set_time_filter()
        else:
            print("Failed to set time filter status",str(Error(status)))
    
    def get_time_filter(self): 
        enabled = c_bool(True)
        status = self.ps_cam_lib.Ps2_GetTimeFilterEnabled(self.device_handle, self.session, byref(enabled)),enabled
        if status == 0:
            print("Time filter enabled:",enabled)
        else:
            print("Failed to get tiue filter status:",str(Error(status)))
    
    def set_confidence_filter(self, enabled = True): 
        status = self.ps_cam_lib.Ps2_SetConfidenceFilterEnabled(self.device_handle, self.session, c_bool(enabled))
        if status == 0:
            self.get_confidence_filter()
        else:
            print("Failed to set confidence filter:",str(Error(status)))

    def get_confidence_filter(self): 
        enabled = c_bool(True)
        status = self.ps_cam_lib.Ps2_GetConfidenceFilterEnabled(self.device_handle, self.session, byref(enabled))
        if status == 0:
            print("Confidence filter enabled:",enabled)
        else:
            print("Failed to get confidence filter status:",str(Error(status)))

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
            print("Failed to get confidence filter threshold:",str(Error(status)))

    def set_WDR_confidence_filter_threshold(self, wdrconfidencethreshold = PsWDRConfidenceThreshold()):
        status = self.ps_cam_lib.Ps2_SetWDRConfidenceFilterThreshold(self.device_handle, self.session, wdrconfidencethreshold) 
        if status == 0:
            self.get_WDR_confidence_filter_threshold()
        else:
            print("Failed to set WDR confidence filter threshold",str(Error(status)))

    def get_WDR_confidence_filter_threshold(self):
        wdrconfidencethreshold = PsWDRConfidenceThreshold()
        status = self.ps_cam_lib.Ps2_GetConfidenceFilterThreshold(self.device_handle, self.session, byref(wdrconfidencethreshold))
        if status == 0:
            print("WDR confidence filter threshold:",wdrconfidencethreshold)
        else:
            print("Failed to get WDR confidence filter threshold:",str(Error(status)))
