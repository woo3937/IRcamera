# for prepping the RPi
# must be run with sudo

# takes around 5 minutes
#sudo apt-get -y install python-pip

## 5 minutes (no vim?!)
#sudo apt-get -y install vim

## 1 minute
#sudo pip install ipython

## 1 minute
#sudo pip install -U RPIO

## 2 minutes
#sudo apt-get -y install python-smbus
#sudo apt-get -y install i2c-tools

## enabling I2C
#cd /etc/modprobe.d
#sudo cp raspi-blacklist.conf raspi-blacklist.conf.old
#sudo sed -i 's/blacklist i2c/#blacklist i2c/g' raspi-blacklist.conf

#cd /etc/
#sudo cp modules moduels.old
#sudo sed -i 's/835/835\ni2c-dev/g' modules
#sudo sed -i 's/i2c-dev/i2c-dev\ni2c-bcm2708\ni2c-dev/g' modules

#sudo touch /etc/udev/rules.d/99-i2c.rules

#echo "SUBSYSYTEM==\"i2c-dev\", MODE==\"0666\"" >> 99-i2c.rules

#sudo adduser pi i2c

#cd ~/

# run every time you log in
sudo modprobe i2c-dev
sudo chmod o+rw /dev/i2c*

## installing wiringpi
#sudo pip install wiringpi

#sudo apt-get -y install libi2c-dev


# this works once, at least
#scp -r scott@169.254.129.232:~/.vim.rpi/ ~/.vim/
#scp scott@169.254.129.232:~/.vimrc.rpi ~/.vimrc

# maybe this will work for i2c?
#sudo apt-get -y install python3
#sudo apt-get -y instlal python-virtualenv
mkdir ~/temp.rpi
cd ~/temp.rpi
git clone https://github.com/quick2wire/quick2wire-python-api
#sudo apt-get -y install ipython3

# making a cron job so no data is lost
echo "* * * * * scp -r ~/temp.rpi/ scott@192.168.2.1:~/Developer/IRcamera/" >> mycron
sudo crontab mycron
rm mycron



# notes on the application:
# run i2cdetect -y 0 and i2cdetect -y 1 to tell which port sensor is on
# import smbus; bus = smbus.SMBus(1)
# bus.read_byte_data(adr, 0x07) gives 255 all the time

# when I run "bus.read_block_data(adr, 0x07), I get a PANIC
