# DCAM560CPro Usage of API

## Initial Imports and Class Initialization
```
from API.Vzense_api_560 import *

camera = VzenseTofCam()
```

To access the API from external scripts, the API module must be imported. Additionally, the camera class must be initialized. Camera is an arbitrary name, but it will be used for the remainder of this document.

All methods detailed below are defined in `src/API/Vsense_api_560.py` for further detail. The described methods will show basic implementation and description in usage of scripts.

## Camera Connection and Frame Reading Methods

`device_info = camera.connect()` Connects to camera, device_info contains information concerning the camera. `device_info` is an arbitrary name, but it will be used for the remainder of this document.

`camera.open(device_info.method,"method")` Opens the camera, using one of three methods: "URI","alias", or "IP". Arguments are case sensitive.
```
camera.open(device_info.uri,"URI")
camera.open(device_info.alias,"alias")
camera.open(device_info.ip,"IP")
```
`camera.close()` Closes the currently opened camera

`camera.start_stream()` Begins a data stream with an opened camera

`camera.stop_stream()` Ends a data stream with an opened camera

`frameready = camera.read_frame()` Reads a frame from the camera. This includes RGB, depth, and IR.
>`frameready.rgb`,`frameready.depth`, and `frameready.ir` return `True` if the read frame includes the matching image type, and `False` otherwise

`frame = camera.get_frame("Method")` Gets the data from the read frame. Methods include "RGB", "Depth", and "IR". Default method is "Depth". 


## Camera Properties Methods

`camera.serial_number()` Prints the serial number of the camera

`camera.IP()` Prints the IP of the camera

`camera.SDK_version()` Prints the SDK version of the camera

`camera.MAC_address()` Prints the MAC address of the camera

`camera.firmware_version()` Prints the firmare version used by the camera