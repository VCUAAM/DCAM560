from dcam560.Vzense_api_560 import *

camera = VzenseTofCam()

device_info = camera.connect()
camera.open(device_info)
camera.set_standby(False)
camera.close()
