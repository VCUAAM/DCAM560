# DCAM560Pro Usage of API

## Initial Imports and Class Initialization
```
import sys
sys.path.append('src/')
from API.Vzense_api_560 import *

camera = VzenseTofCam()
```

To access the API from external programs, the `src/` folder must be added to path so that '__init__.py' is able to see the methods needed

## VzenseTofCam Class Usage methods

`device_info = camera.connect()` Connects to camera, device_info contains information concerning the camera

`camera.open(device_info.uri)` Opens the camera, must contain the uri from the device info

`camera.close()` Closes the currently opened camera

`camera.serial_number()` Outputs the serial number of the camera

`camera.firmware_version()` Outputs the firmare version used by the camera