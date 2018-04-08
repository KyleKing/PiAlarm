cd ~
git clone https://github.com/adafruit/Adafruit_Python_CharLCD.git
cd Adafruit_Python_CharLCD
sudo python setup.py install

cd ~
git clone https://github.com/sarfata/pi-blaster.git
cd pi-blaster
./autogen.sh
./configure
make

cd ~

sudo pip install schedule
sudo pip install requests
sudo pip install ConfigParser
sudo pip install tqdm

sudo apt-get install build-essential python-dev python-smbus python-pip
sudo apt-get install rpi.gpio
sudo pip install RPi.GPIO
sudo pip install Adafruit_CharLCD
