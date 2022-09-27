from API.Vzense_api_560 import *

camera = VzenseTofCam()

device_info = camera.connect()
camera.open(device_info.uri)
camera.firmware_version()
camera.serial_number()
camera.IP()
camera.SDK_version()
camera.MAC_address()
camera.close()