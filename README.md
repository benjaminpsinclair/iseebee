
# iseebee

iseebee uses the Killerbee (https://github.com/riverloopsec/killerbee) library to sniff Zigbee traffic and graphically display it to the user. Nodes are represented graphically and can be named and sent raw bytes using injection.

This prototype is a proof of concept intended to be built upon, in the future it is intended that network keys may be used or discovered to decrypt packets and craft specific messages.

Killerbee is compatible with several devices, however this has been tested using a Texas Instruments CC2531 transceiver using Bumblebee (https://github.com/virtualabs/cc2531-killerbee-fw) firmware.  

## Installation

First create the virtual environment:

```shell
python3 -m venv env

source env/bin/activate
``` 
Follow Killerbee installation instructions (https://github.com/riverloopsec/killerbee)

To install remaining required packages:

```shell
pip install -r requirements.txt
``` 
## Usage/Examples
To run iseebee first the environment with Killerbee installed must be loaded:
```shell
source env/bin/activate
```
To run iseebee once the environment is installed:
```shell
python3 src/iseebee.py
```

If no compatible Zigbee device is detected an error will be thrown.




## Authors

- [@benjaminpsinclair](https://github.com/benjaminpsinclair)


