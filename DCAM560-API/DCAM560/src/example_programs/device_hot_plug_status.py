from API.Vzense_api_560 import *

camera = VzenseTofCam()

camera.set_hot_plug_status()
device_info = camera.connect()
camera.open(device_info.uri)
camera.stop_stream()
camera.close()
