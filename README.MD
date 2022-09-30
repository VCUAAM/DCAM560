# Vsense DCAM560Pro Resources
Found in this repository are seperate resources for using the 3D camera, the DCAM560Pro.
- DCAM560-API
>  This Python SDK was originally created by [Vsense](https://github.com/Vzense/BaseSDK_python_wrapper), and was heavily modified by [Logan Schorr](https://github.com/pokelogan89)
>> The modifications primarily are in regards to making the API easier to write in and internalizing the error messages to the built-in functions. This also includes creating a thorough documentation of the usage and parameters for the API.
- Vsense ConfigTool
> This configuration tool was created by [Vsense](https://github.com/Vzense/VzenseConfigTool) as a way to configure the settings of the 3D camera. This can be used to set the IP of the camera, as well as change the WDR, Depth, and RGB settings of the camera
- Vsense UTool
> This UTool was created by [Vsense](https://github.com/Vzense/UTool) to use the camera without requiring usage of the API. There are options for all of the different image modes, options for the filter overlays, as well as ways to save images and format the image output.

Each are detailed below, and contain their own README for further usage.

## Quick Start for Working with the Camera
 - Connect the camera to a POE+ switch
 - Connect PC to this camera either through direct ethernet (LAN) connection or through a router (WLAN)
 - Use one of the above methods to utilize the power of the camera