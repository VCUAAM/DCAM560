from pickle import FALSE, TRUE
import sys
sys.path.append('src/')
from API.Vzense_api_560 import *

camera = VzenseTofCam()

device_info = camera.connect()
camera.open(device_info.uri)
camera.serial_number()
camera.firmware_version()
camera.close()