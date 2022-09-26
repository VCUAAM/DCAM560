from pickle import FALSE, TRUE
import sys
sys.path.append('src/')
from API.Vzense_api_560 import *

camera = VzenseTofCam()

device_info = camera.connect()
camera.open_by_alias(device_info.alias)
camera.close()  
