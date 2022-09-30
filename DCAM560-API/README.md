## Python Wrapper for Vzense Base SDK API

Python wrapper is an opensource project of Vzense TOF camera API. This API has been heavily modified to better fit the needs of the VCU research team

The goal of this project is to help developers use Vzense TOF camera via python method easily.

### Requirements

- Python version : 3.10.x
- Python modules : ctypes, numpy, opencv-python

### Directory

- **DCAM560**: API and Sample code for DCAM560CPRO
- **Lib**: VzenseBaseSDK dynamic library files
- **install.py**: Installation file
- **config.txt**: Set config that is needed by 'install.py', such as:
```
system = Windows64
url = https://github.com
```
|system|details|
|---|---|
|Windows64|windows 64 bit|
|Windows32|windows 32 bit|
|Ubuntu20.04|the same with Ubuntu18.04 PC SDK|
|Ubuntu18.04|for PC with x86_64-linux-gnu(v7.5.0)|
|Ubuntu16.04|for PC with x86_64-linux-gnu(v5.4.0)|
|AArch64|for aarch64 with aarch64-linux-gnu(v5.4.0)|
|Arm-linux-gnueabihf|for arm32 with arm-linux-gnueabihf(v5.4.0)|

|url|
|---|
|https://gitee.com|
|https://github.com|

### Quick Start for API

- Step 1: Install modules
         
```	 
	  pip install numpy
	  pip install opencv-python 
```
- Step 2. Set 'config.txt' according to your needs

- Step 3. Execute 'python install.py' to install system libraries and drivers

- Step 4. Switch to src under the product directory, and utilize with the help of the example programs

