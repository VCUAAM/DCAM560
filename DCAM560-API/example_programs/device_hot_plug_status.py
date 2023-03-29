from dcam560.Vzense_api_560 import *

camera = VzenseTofCam()

camera.set_hot_plug_status()
device_info = camera.connect()
camera.open(device_info)
camera.stop_stream()
camera.close()
