# detecteur-ambiance

## Setup raspberry pi
```bash
sudo apt install python3 python3-pip htop python-numpy python-opencv libopencv-dev
python3 -m pip install Adafruit_DHT pandas numpy matplotlib PyQt5
```
```bash
sudo raspi-config
Interface -> Camera activated
```
```bash
export PYTHONPATH=$PYTHONPATH:$PWD:$PWD/raspi
```