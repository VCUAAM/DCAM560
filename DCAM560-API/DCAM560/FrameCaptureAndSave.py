from pickle import FALSE, TRUE
import sys
sys.path.append('../../../')

from API.Vzense_api_560 import *
import time

camera = VzenseTofCam()


camera_count = camera.Ps2_GetDeviceCount()
retry_count = 100
while camera_count==0 and retry_count > 0:
    retry_count = retry_count-1
    camera_count = camera.Ps2_GetDeviceCount()
    time.sleep(1)
    print("scanning......   ",retry_count)

device_info=PsDeviceInfo()

if camera_count > 1:
    ret,device_infolist=camera.Ps2_GetDeviceListInfo(camera_count)
    if ret==0:
        device_info = device_infolist[0]
        for info in device_infolist: 
            print('cam uri:  ' + str(info.uri))
    else:
        print(' failed:' + ret)  
        exit()  
elif camera_count == 1:
    ret,device_info=camera.Ps2_GetDeviceInfo()
    if ret==0:
        print('cam uri:' + str(device_info.uri))
    else:
        print(' failed:' + ret)   
        exit() 
else: 
    print("No camera found")
    exit()

if  PsConnectStatus.Connected.value != device_info.status:
	print("connect status:",device_info.status)  
	print("Call Ps2_OpenDevice with connect status :",PsConnectStatus.Connected.value)
	exit()
else:
    print("uri: "+str(device_info.uri))
    print("alias: "+str(device_info.alias))
    print("connectStatus: "+str(device_info.status))

ret = camera.Ps2_OpenDevice(device_info.uri)
if  ret == 0:
    print("Device open successful")
else:
    print('Ps2_OpenDevice failed: ' + str(ret))   

ret = camera.Ps2_StartStream()
if  ret == 0:
    print("Start stream successful")
else:
    print("Ps2_StartStream failed:",ret)     

while 1:
    ret, frameready = camera.Ps2_ReadNextFrame()
    if  ret !=0:
        print("Ps2_ReadNextFrame failed:",ret)
        time.sleep(1)
        continue       
    if  frameready.depth:      
        ret,frame = camera.Ps2_GetFrame(PsFrameType.PsDepthFrame)

        curPath = os.getcwd()
        print (curPath)
        folder = curPath+ "/save"
        if not os.path.exists(folder):
            print("Path does not exists")
            os.makedirs(folder)
        else:
            print("Path already exists")
        filename = folder + "/depth.bin"
        file = open(filename,"wb+")
        for i in range(frame.dataLen):
            file.write(c_uint8(frame.pFrameData[i]))
        
        file.close()
        print("save ok")
        break

ret = camera.Ps2_StopStream()       
if  ret == 0:
    print("Stream stopped successfully")
else:
    print('Ps2_StopStream failed: ' + str(ret))  

ret = camera.Ps2_CloseDevice()     
if  ret == 0:
    print("Device closed successfully")
else:
    print('Ps2_CloseDevice failed: ' + str(ret))   
           