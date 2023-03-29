# Vsense DCAM560Pro Resources
Found in this repository are seperate resources for using the 3D camera, the DCAM560Pro.
- DCAM560-API
  -  This Python SDK was originally created by [Vsense](https://github.com/Vzense/BaseSDK_python_wrapper) and was heavily modified by [Logan Schorr](https://github.com/pokelogan89)
- Vsense Config Tool
  - This configuration tool was created by [Vsense](https://github.com/Vzense/VzenseConfigTool) 
- Vsense UTool
  - This UTool was created by [Vsense](https://github.com/Vzense/UTool) 

Each are detailed below, and contain their own README for further usage.

**NOTE**: These are currently developed for utilization on a Windows architecture, and may require downloading additional libraries from [Vsense](https://github.com/Vzense) to properly function

## Quick Start for Working with the Camera
 - Connect the camera to a POE+ switch
 - Connect PC to this camera either through direct ethernet (LAN) connection or through a router (WLAN)
 - Use one of the above methods to utilize the power of the camera
   - The easiest way is to begin with the configuration tool to set the camera to have a static IP
   - Then, use the UTool to get an idea of the outputs and types of images that the camera can create
   - Finally, use the API to access the specific data you need for your purposes, whether that be point-cloud, IR, etc. 

## DCAM560-API
 - This API is an SDK for utilizing the functions of the DCAM560 without needing to use the UTool
 - The SDK allows one to connect, capture point cloud data, and collect information about the camera, among other things
   - These functions are detailed in the API folder
 - The modifications made by [Logan Schorr](https://github.com/pokelogan89) primarily are in regards to making the API easier to write in and internalizing the error messages to the built-in functions
   - This also includes creating a thorough documentation of the usage and parameters for the API for future reference and development
 - There are several example programs that demonstrate usage of the API
## Vsense Config Tool
- The configuration tool is a way to configure the settings of the 3D camera
  - This can be used to set the IP of the camera, as well as change the WDR, Depth, and RGB settings of the camera
- Most of the functionality of the configuration tool is captured within the SDK, with the exception of setting a static IP or configuring DHCP
- A screen capture of the application can be seen below

![config_tool](https://user-images.githubusercontent.com/9327669/193338455-81024a7b-7656-41f9-a924-3700194e03ac.PNG)

## Vsense UTool
- The UTool is an application design to use the camera without requiring utilization of the API
- There are options for all of the different image modes, options for the filter overlays, as well as ways to save images and format the image output
- This is a really easy way to observe how the camera collects data and figure out how you can use it
- A screen capture of the application can be seen below

![utool](https://user-images.githubusercontent.com/9327669/193340346-73d71138-70d9-479a-90fa-5fdb1c5920a3.PNG)
