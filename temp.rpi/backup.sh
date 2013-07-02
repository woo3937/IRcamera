
sudo cp ~/.vimrc ~/temp.rpi
sudo cp ~/.bashrc ~/temp.rpi
#sudo cp -r ~/.vim ~/temp.rpi/

rsync --copy-links -r --delete /home/pi/temp.rpi/ scott@192.168.2.1:~/Developer/IRcamera/temp.rpi
# note we said .../temp.rpi!! I deleted all my stuff. Luckily git exists.
