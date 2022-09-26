from API.Vzense_define_560 import * 
from os import path,getcwd,environ
import ctypes
from time import sleep
from ctypes import *
gCallbackFuncList=[]

class VzenseTofCam():
    device_handle = c_void_p(0)
    session = c_uint(0)
    def __init__(self):
        if platform.system() == 'Linux':
            libpath = (path.abspath(path.dirname(getcwd()) + path.sep))+"/Lib/libvzense_api.so"
            #print(libpath)
            self.ps_cam_lib = cdll.LoadLibrary(libpath)
        elif platform.system() == 'Windows':          
            lib_name = "../../Lib/"
            lib_path = path.dirname(path.abspath(__file__)) + path.sep + lib_name
            lib_path = ';' + lib_path
            environ['path'] += lib_path
            libpath = (path.abspath(path.dirname(getcwd()) + path.sep))+"/Lib/vzense_api.dll"
            #print(libpath)
            self.ps_cam_lib = cdll.LoadLibrary(libpath)    
        else:
            print('Unsupported OS')
            exit()
            
        self.device_handle = c_void_p(0)
        self.session = c_uint(0)
        self.ps_cam_lib.Ps2_Initialize()

    def __del__(self):
        self.ps_cam_lib.Ps2_Shutdown()

    sensors = {
        "depth": PsSensorType.PsDepthSensor,
        "RGB": PsSensorType.PsRgbSensor
    }

    def connect(self):
        camera_count,retry_count = 0,0

        while camera_count == 0 and retry_count < 20:
            retry_count += 1
            camera_count = self.Ps2_GetDeviceCount()
            sleep(1)
            print("Searching for camera, attempt",retry_count)

        device_info = PsDeviceInfo()

        if camera_count > 1:
            status,device_infolist = self.Ps2_GetDeviceListInfo(camera_count)
            if status == 0:
                device_info = device_infolist[0]
                for info in device_infolist: 
                    print('cam uri:  ' + str(info.uri))
            else:
                print('Connection failed:' + status)  
                exit()  
        elif camera_count == 1:
            status,device_info = self.Ps2_GetDeviceInfo()
            if status ==  0:
                #print('cam uri:' + str(device_info.uri))
                sleep(.01)
            else:
                print('Connection failed:' + status)   
                exit() 
        else: 
            print("No camera found")
            exit()

        if PsConnectStatus.Connected.value != device_info.status:
            print("Connection status:",device_info.status)  
            print("Call Ps2_OpenDevice with connect status :",PsConnectStatus.Connected.value)
            exit()
        #else:
            #print("uri: "+str(device_info.uri))
            #print("alias: "+str(device_info.alias))
            #print("connectStatus: "+str(device_info.status))   
        return device_info
    
    def Ps2_GetDeviceCount(self):
        count = c_int()
        self.ps_cam_lib.Ps2_GetDeviceCount(byref(count))
        return count.value
    
    def Ps2_GetDeviceListInfo(self, cam_count = 1):
        tmp  = PsDeviceInfo* cam_count
        device_infolist = tmp() 
        return self.ps_cam_lib.Ps2_GetDeviceListInfo(device_infolist, cam_count),device_infolist
    
    def Ps2_GetDeviceInfo(self, cam_index = 0):
        device_info = PsDeviceInfo()
        return self.ps_cam_lib.Ps2_GetDeviceInfo(byref(device_info), cam_index), device_info
         
    def open(self,  uri=c_char_p()):
        if uri:
            status = self.ps_cam_lib.Ps2_OpenDevice(uri, byref(self.device_handle))
            if  status == 0:
                print("Camera opened successfully")
                return None
            else:
                print('Open failed: ' + str(status))
        else:
            return PsReturnStatus.PsRetInputPointerIsNull
    
    def close(self):
        status = self.ps_cam_lib.Ps2_CloseDevice(byref(self.device_handle))
        if  status == 0:
            print("Device closed successfully")
        else:
            print('Close failed: ' + str(status))   
        return None

    def start_stream(self):
        status = self.ps_cam_lib.Ps2_StartStream(self.device_handle, self.session)
        if status == 0:
            print("Stream started successfully")
        else:
            print("Start stream failed:",status)     
        return None
         
    def stop_stream(self):
        status = self.ps_cam_lib.Ps2_StopStream(self.device_handle, self.session)
        if status == 0:
            print("Stream stopped successfully")
        else:
            print('Stop stream failed: ' + str(status)) 
        return None
         
    def Ps2_ReadNextFrame(self):
        frameready = PsFrameReady()
        return self.ps_cam_lib.Ps2_ReadNextFrame(self.device_handle, self.session, byref(frameready)), frameready

    def Ps2_GetFrame(self, frametype = PsFrameType.PsDepthFrame):   
        psframe = PsFrame() 
        return self.ps_cam_lib.Ps2_GetFrame(self.device_handle, self.session, frametype.value, byref(psframe)), psframe
    
    def Ps2_SetDataMode(self, datamode = PsDataMode.PsDepthAndRGB_30):
        return self.ps_cam_lib.Ps2_SetDataMode(self.device_handle, self.session, datamode.value)
         
    def Ps2_GetDataMode(self):
        datamode = c_int(0)
        return self.ps_cam_lib.Ps2_GetDataMode(self.device_handle, self.session, byref(datamode)), datamode
    
    def Ps2_SetDepthRange(self, depthrange = PsDepthRange.PsNearRange):
        return self.ps_cam_lib.Ps2_SetDepthRange(self.device_handle, self.session, depthrange.value) 
       
    def Ps2_GetDepthRange(self):
        depthrange = c_int(0)
        return self.ps_cam_lib.Ps2_GetDepthRange(self.device_handle, self.session, byref(depthrange)), depthrange

    def Ps2_SetThreshold(self, threshold = c_uint16(20)):
        return self.ps_cam_lib.Ps2_SetThreshold(self.device_handle, self.session, threshold) 
               
    def get_threshold(self):
        thres = c_uint16()
        status = self.ps_cam_lib.Ps2_GetThreshold(self.device_handle, self.session, byref(thres)) 
        if status == 0:
            print("Threshold:",thres.value)
            return thres.value
        else:
            print("Get threshold failed:",status)
        return None

    def Ps2_SetPulseCount(self, pulsecount = c_uint16(20)):
        return self.ps_cam_lib.Ps2_SetPulseCount(self.device_handle, self.session, pulsecount) 
     
    def get_pulse_count(self):
        pulsecount = c_uint16()
        status = self.ps_cam_lib.Ps2_GetPulseCount(self.device_handle, self.session, byref(pulsecount))
        if status == 0:
            print("Pulse count:",pulsecount.value)
            return pulsecount.value
        else:
            print("Get pulse count failed:",status)
        return None
    
    def Ps2_SetGMMGain(self, gmmgain = c_uint16(20)):
        gmmgain_ = PsGMMGain()
        gmmgain_.gmmgain = gmmgain
        gmmgain_.option = 0
        return self.ps_cam_lib.Ps2_SetGMMGain(self.device_handle, self.session, gmmgain_) 
     
    def get_GMM_gain(self):
        gmmgain = c_uint16(1)
        status = self.ps_cam_lib.Ps2_GetGMMGain(self.device_handle, self.session, byref(gmmgain))
        if status == 0:
            print("GMM Gain:",gmmgain)
            return gmmgain
        else:
            print("Get GMM gain failed:",status)
        return None

    def get_camera_parameters(self, sensorType = "depth"):
        CameraParameters = PsCameraParameters()
        sensorTypeObj = self.sensors[sensorType]
        status = self.ps_cam_lib.Ps2_GetCameraParameters(self.device_handle, self.session, sensorTypeObj.value, byref(CameraParameters))

        if status == 0:
            return CameraParameters
        else:
            print("Get %s camera parameters failed:",status %(sensorType))
        return None

    def get_camera_extrinsic_parameters(self):
        CameraExtrinsicParameters = PsCameraExtrinsicParameters()
        status = self.ps_cam_lib.Ps2_GetCameraExtrinsicParameters(self.device_handle, self.session, byref(CameraExtrinsicParameters))
        if status == 0: 
            return CameraExtrinsicParameters
        else:
            print("Get extrinsic parameters failed:",status)
        return None
           
    def Ps2_SetColorPixelFormat(self, pixelFormat = PsPixelFormat.PsPixelFormatBGR888):
        return self.ps_cam_lib.Ps2_SetColorPixelFormat(self.device_handle, self.session, pixelFormat.value) 
       
    def Ps2_SetRGBResolution(self, resolution = PsResolution.PsRGB_Resolution_640_480):
        return self.ps_cam_lib.Ps2_SetRGBResolution(self.device_handle, self.session, resolution.value) 
     
    def  Ps2_GetRGBResolution(self):
        resolution = c_int(0)
        return self.ps_cam_lib.Ps2_GetRGBResolution(self.device_handle, self.session, byref(resolution)), resolution

    def Ps2_SetWDROutputMode(self, WDRMode = PsWDROutputMode()):
        return self.ps_cam_lib.Ps2_SetWDROutputMode(self.device_handle, self.session, byref(WDRMode)) 
     
    def Ps2_GetWDROutputMode(self):
        WDRMode = PsWDROutputMode()
        return self.ps_cam_lib.Ps2_GetWDROutputMode(self.device_handle, self.session, byref(WDRMode)), WDRMode

    def Ps2_SetWDRStyle(self, wdrStyle = PsWDRStyle.PsWDR_FUSION):
        return self.ps_cam_lib.Ps2_SetWDRStyle(self.device_handle, self.session, wdrStyle.value) 
                
    def Ps2_GetMeasuringRange(self,  range = PsDepthRange.PsNearRange):
        MeasuringRange = PsMeasuringRange()
        rst = self.ps_cam_lib.Ps2_GetMeasuringRange(self.device_handle, self.session, range.value, byref(MeasuringRange))
        if rst == 0:
            if range == PsDepthRange.PsNearRange or range == PsDepthRange.PsXNearRange or range == PsDepthRange.PsXXNearRange:
                return rst, MeasuringRange.depthMaxNear, MeasuringRange.effectDepthMinNear, MeasuringRange.effectDepthMaxNear
            elif range == PsDepthRange.PsMidRange or range == PsDepthRange.PsXMidRange or range == PsDepthRange.PsXXMidRange:
                return rst, MeasuringRange.depthMaxMid, MeasuringRange.effectDepthMinMid, MeasuringRange.effectDepthMaxMid
            elif range == PsDepthRange.PsFarRange or range == PsDepthRange.PsXFarRange or range == PsDepthRange.PsXXFarRange:
                return rst, MeasuringRange.depthMaxFar, MeasuringRange.effectDepthMinFar, MeasuringRange.effectDepthMaxFar
        else:
            return rst, 0, 0, 0

    def Ps2_ConvertDepthFrameToWorldVector(self, depthFrame = PsFrame()): 
        len = depthFrame.width*depthFrame.height
        tmp =PsVector3f*len
        pointlist = tmp()
        return self.ps_cam_lib.Ps2_ConvertDepthFrameToWorldVector(self.device_handle, self.session, depthFrame,pointlist),pointlist

    def Ps2_SetSynchronizeEnabled(self, enabled = c_bool(True)): 
        return self.ps_cam_lib.Ps2_SetSynchronizeEnabled(self.device_handle, self.session, enabled)
    
    def Ps2_GetSynchronizeEnabled(self): 
        enabled = c_bool(True)
        return self.ps_cam_lib.Ps2_GetSynchronizeEnabled(self.device_handle, self.session, byref(enabled)),enabled
    
    def Ps2_SetDepthDistortionCorrectionEnabled(self, enabled = c_bool(True)): 
        return self.ps_cam_lib.Ps2_SetDepthDistortionCorrectionEnabled(self.device_handle, self.session, enabled)
    
    def Ps2_GetDepthDistortionCorrectionEnabled(self): 
        enabled = c_bool(True)
        return self.ps_cam_lib.Ps2_GetDepthDistortionCorrectionEnabled(self.device_handle, self.session, byref(enabled)),enabled
    
    def Ps2_SetRGBDistortionCorrectionEnabled(self, enabled = c_bool(True)): 
        return self.ps_cam_lib.Ps2_SetRGBDistortionCorrectionEnabled(self.device_handle, self.session, enabled)
    
    def Ps2_GetRGBDistortionCorrectionEnabled(self): 
        enabled = c_bool(True)
        return self.ps_cam_lib.Ps2_GetRGBDistortionCorrectionEnabled(self.device_handle, self.session, byref(enabled)),enabled

    def Ps2_SetComputeRealDepthCorrectionEnabled(self, enabled = c_bool(True)): 
        return self.ps_cam_lib.Ps2_SetComputeRealDepthCorrectionEnabled(self.device_handle, self.session, enabled)
    
    def Ps2_GetComputeRealDepthCorrectionEnabled(self): 
        enabled = c_bool(True)
        return self.ps_cam_lib.Ps2_GetComputeRealDepthCorrectionEnabled(self.device_handle, self.session, byref(enabled)),enabled

    def Ps2_SetSpatialFilterEnabled(self, enabled = c_bool(True)): 
        return self.ps_cam_lib.Ps2_SetSpatialFilterEnabled(self.device_handle, self.session, enabled)
    
    def Ps2_GetSpatialFilterEnabled(self): 
        enabled = c_bool(True)
        return self.ps_cam_lib.Ps2_GetSpatialFilterEnabled(self.device_handle, self.session, byref(enabled)),enabled

    def Ps2_SetTimeFilterEnabled(self, enabled = c_bool(True)): 
        return self.ps_cam_lib.Ps2_SetTimeFilterEnabled(self.device_handle, self.session, enabled)
    
    def Ps2_GetTimeFilterEnabled(self): 
        enabled = c_bool(True)
        return self.ps_cam_lib.Ps2_GetTimeFilterEnabled(self.device_handle, self.session, byref(enabled)),enabled

    def Ps2_SetDepthFrameEnabled(self, enabled = c_bool(True)): 
        return self.ps_cam_lib.Ps2_SetDepthFrameEnabled(self.device_handle, self.session, enabled)

    def Ps2_SetIrFrameEnabled(self, enabled = c_bool(True)): 
        return self.ps_cam_lib.Ps2_SetIrFrameEnabled(self.device_handle, self.session, enabled)

    def Ps2_SetRgbFrameEnabled(self, enabled = c_bool(True)): 
        return self.ps_cam_lib.Ps2_SetRgbFrameEnabled(self.device_handle, self.session, enabled)

    def Ps2_SetImageMirror(self, type = c_int32(0)): 
        return self.ps_cam_lib.Ps2_SetImageMirror(self.device_handle, self.session, type)
    
    def Ps2_SetImageRotation(self, type = c_int32(0)): 
        return self.ps_cam_lib.Ps2_SetImageRotation(self.device_handle, self.session, type)
    
    def Ps2_SetMapperEnabledDepthToRGB(self, enabled = c_bool(True)): 
        return self.ps_cam_lib.Ps2_SetMapperEnabledDepthToRGB(self.device_handle, self.session, enabled)
    
    def Ps2_GetMapperEnabledDepthToRGB(self): 
        enabled = c_bool(True)
        return self.ps_cam_lib.Ps2_GetMapperEnabledDepthToRGB(self.device_handle, self.session, byref(enabled)),enabled

    def Ps2_SetMapperEnabledRGBToDepth(self, enabled = c_bool(True)): 
        return self.ps_cam_lib.Ps2_SetMapperEnabledRGBToDepth(self.device_handle, self.session, enabled)
    
    def Ps2_GetMapperEnabledRGBToDepth(self): 
        enabled = c_bool(True)
        return self.ps_cam_lib.Ps2_GetMapperEnabledRGBToDepth(self.device_handle, self.session, byref(enabled)),enabled

    def Ps2_SetHotPlugStatusCallback(self,callbackfunc= c_void_p): 
        callbackFunc_= ctypes.CFUNCTYPE(c_void_p,POINTER(PsDeviceInfo),c_int32)(callbackfunc)    
        gCallbackFuncList.append(callbackFunc_)
        return self.ps_cam_lib.Ps2_SetHotPlugStatusCallback(callbackFunc_)

    def Ps2_SetWDRPulseCount(self,wdrpulseCount = PsWDRPulseCount()): 
        return self.ps_cam_lib.Ps2_SetWDRPulseCount(self.device_handle, self.session, wdrpulseCount)

    def Ps2_GetWDRPulseCount(self): 
        wdrpulseCount = PsWDRPulseCount()
        return self.ps_cam_lib.Ps2_GetWDRPulseCount(self.device_handle, self.session, byref(wdrpulseCount)),wdrpulseCount

    def serial_number(self): 
        tmp = c_char * 64
        sn = tmp()
        ret = self.ps_cam_lib.Ps2_GetSerialNumber(self.device_handle, self.session, sn, 63)
        if  ret == 0:
            print("Device Serial Number:",str(sn.value))
        else:
            print("serial_number failed:",ret)
        return None

    def firmware_version(self): 
        tmp = c_char * 64
        fw = tmp()
        ret = self.ps_cam_lib.Ps2_GetFirmwareVersionNumber(self.device_handle, self.session, fw, 63)
        if  ret == 0:
            print("Firmware Version:",str(fw.value))
        else:
            print("firmware_version failed:",ret)
        return 

    def Ps2_SetDSPEnabled(self, enabled = c_bool(True)): 
        return self.ps_cam_lib.Ps2_SetDSPEnabled(self.device_handle, self.session, enabled)
    
    def Ps2_GetDSPEnabled(self): 
        enabled = c_bool(True)
        return self.ps_cam_lib.Ps2_GetDSPEnabled(self.device_handle, self.session, byref(enabled)),enabled

    def Ps2_SetSlaveModeEnabled(self, enabled = c_bool(True)): 
        return self.ps_cam_lib.Ps2_SetSlaveModeEnabled(self.device_handle, self.session, enabled)
    
    def Ps2_SetTofFrameRate(self, rate = c_uint8(30)): 
        return self.ps_cam_lib.Ps2_SetTofFrameRate(self.device_handle, self.session, rate)
    
    def Ps2_GetTofFrameRate(self): 
        rate = c_uint8(30)
        return self.ps_cam_lib.Ps2_GetTofFrameRate(self.device_handle, self.session, byref(rate)),rate

    def set_standby(self, enabled = c_bool(True)): 
        state = self.ps_cam_lib.Ps2_SetStandByEnabled(self.device_handle, self.session, enabled)
        if  state != 0:  
            print("Set standby failed:",state)
        return None
    
    def open_by_alias(self,  alias=c_char_p()):
        if alias:
            state = self.ps_cam_lib.Ps2_OpenDeviceByAlias(alias, byref(self.device_handle))
            if state == 0:
                print("Device opened successfully")
            else:
                print('Open by alias failed: ' + str(state))  
            return None
        else:
            return PsReturnStatus.PsRetInputPointerIsNull
    
    def Ps2_SetWaitTimeOfReadNextFrame(self, time = c_uint16(33)): 
        return self.ps_cam_lib.Ps2_SetWaitTimeOfReadNextFrame(self.device_handle, self.session, time)
    
    def Ps2_GetSDKVersion(self): 
        tmp = c_char * 64
        version = tmp()
        return self.ps_cam_lib.Ps2_GetSDKVersion(version, 63),version.value
 
    def Ps2_GetMappedPointDepthToRGB(self, depthPoint = PsDepthVector3(),rgbSize = PsVector2u16(640,480)): 
        PosInRGB = PsVector2u16()
        return self.ps_cam_lib.Ps2_GetMappedPointDepthToRGB(self.device_handle, self.session, depthPoint, rgbSize, byref(PosInRGB)),PosInRGB

    def Ps2_RebootCamera(self): 
        return self.ps_cam_lib.Ps2_RebootCamera(self.device_handle, self.session)

    def Ps2_SetLegacyAlgorithmicEnabled(self, enabled = c_bool(True)): 
        return self.ps_cam_lib.Ps2_SetLegacyAlgorithmicEnabled(self.device_handle, self.session, enabled)
     
    def Ps2_SetSlaveTrigger(self): 
        return self.ps_cam_lib.Ps2_SetSlaveTrigger(self.device_handle, self.session)
     
    def Ps2_GetDeviceIP(self,  uri=c_char_p()):
        if uri:
            tmp = c_char * 17
            ip = tmp()
            return self.ps_cam_lib.Ps2_GetDeviceIP(uri, ip),ip.value
        else:
            return PsReturnStatus.PsRetInputPointerIsNull, None
    
    def Ps2_GetDeviceMAC(self):
        tmp = c_char * 18
        mac = tmp()
        return self.ps_cam_lib.Ps2_GetDeviceMAC(self.device_handle, self.session, mac), mac.value
         
    def Ps2_SetRGBBrightness(self, value = c_char(0)):
        return self.ps_cam_lib.Ps2_SetRGBBrightness(self.device_handle, self.session, value)
         
    def Ps2_GetRGBBrightness(self):
        value = c_char(0)
        return self.ps_cam_lib.Ps2_GetRGBBrightness(self.device_handle, self.session, byref(value)),value

    def Ps2_SetRGBExposure(self, value = c_ubyte(0)):
        return self.ps_cam_lib.Ps2_SetRGBExposure(self.device_handle, self.session, value)
         
    def Ps2_GetRGBExposure(self):
        value = c_ubyte(0)
        return self.ps_cam_lib.Ps2_GetRGBExposure(self.device_handle, self.session, byref(value)),value
    
    def Ps2_SetRGBFrequencyOfPowerLine(self, value = c_ubyte(0)):
        return self.ps_cam_lib.Ps2_SetRGBFrequencyOfPowerLine(self.device_handle, self.session, value)
         
    def Ps2_GetRGBFrequencyOfPowerLine(self):
        value = c_ubyte(0)
        return self.ps_cam_lib.Ps2_GetRGBFrequencyOfPowerLine(self.device_handle, self.session, byref(value)),value
    
    def Ps2_SetConfidenceFilterEnabled(self, enabled = c_bool(True)): 
        return self.ps_cam_lib.Ps2_SetConfidenceFilterEnabled(self.device_handle, self.session, enabled)
    
    def Ps2_GetConfidenceFilterEnabled(self): 
        enabled = c_bool(True)
        return self.ps_cam_lib.Ps2_GetConfidenceFilterEnabled(self.device_handle, self.session, byref(enabled)),enabled

    def Ps2_SetConfidenceFilterThreshold(self, threshold = c_uint16(20)):
        return self.ps_cam_lib.Ps2_SetConfidenceFilterThreshold(self.device_handle, self.session, threshold) 
               
    def Ps2_GetConfidenceFilterThreshold(self):
        thres = c_uint16()
        return self.ps_cam_lib.Ps2_GetConfidenceFilterThreshold(self.device_handle, self.session, byref(thres)), thres.value

    def Ps2_SetWDRConfidenceFilterThreshold(self, wdrconfidencethreshold = PsWDRConfidenceThreshold()):
        return self.ps_cam_lib.Ps2_SetWDRConfidenceFilterThreshold(self.device_handle, self.session, wdrconfidencethreshold) 
               
    def Ps2_GetConfidenceFilterThreshold(self):
        wdrconfidencethreshold = PsWDRConfidenceThreshold()
        return self.ps_cam_lib.Ps2_GetConfidenceFilterThreshold(self.device_handle, self.session, byref(wdrconfidencethreshold)), wdrconfidencethreshold

    def open_by_ip(self, ip=c_char_p()):
        if ip:
            state = self.ps_cam_lib.Ps2_OpenDeviceByIP(ip, byref(self.device_handle))
            if state == 0:
                print("Device opened successfully")
            else:
                print('Open by IP failed: ' + str(state)) 
            return None
        else:
            return PsReturnStatus.PsRetInputPointerIsNull
