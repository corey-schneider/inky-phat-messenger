# Inky Messenger 

##### _Send messages to family or loved ones_
[**image of working device**]
## Features
- Send an email / text message to update the message
- Weather status icon
- Temperature (in Fahrenheit) from OpenWeatherMap API  _(R.I.P. DarkSky)_
- Date in the bottom right corner
- Can send a message up to 4 lines long
- Makes one call to the IpInfo API (unless the device is moved to a different network)
- Logging of errors saved in `log.txt` for easy debugging though sftp if the device suddenly stops working
  - Log will include:
    - Incorrect / invalid email credentials
    - Incorrect / invalid API key
    - Missing email or password in `config.json`
    - Missing API key in `config.json`
    - Missing `config.json`


## Setup
- Download [Raspberry Pi OS Lite](https://www.raspberrypi.org/software/operating-systems/)
- Flash image to SD card with [Raspberry Pi imager](https://www.raspberrypi.org/software/). While this is happening...
  - Download [wpa_supplicant.conf](wpa_supplicant.conf) and [ssh](ssh)
  - Modify [wpa_supplicant.conf](wpa_supplicant.conf) to include your wifi credentials
- Safely remove and reinsert the microSD card you just flashed
- Put YOUR modified version of `wpa_supplicant.conf` and `ssh` directly onto the microSD card
- Insert microSD, plug in the Pi, and SSH into it
- Download the necessary files through `curl https://get.pimoroni.com/inky | bash`
- Enable SPI and I2C. To do this, run `sudo raspi-config`, scroll to Interface Options, and enable them.
  - While in `raspi-config`, change the time zone _(unless you live in the UK)_. Select `Localisation Options` > `Timezone`.
- Run `sudo apt-get update` and `sudo apt-get upgrade` - _This will take a while_
- Run `python3 -m pip install --upgrade pip` and `python3 -m pip install --upgrade Pillow`
- Create a **new** Gmail email. **Do NOT use an existing Gmail account for this.** Modify [config/config.json](config/config.json) to include this new receiving email and password.
  - After creating the Gmail, you must turn ON `Allow Less Secure Apps`. [Click here for a guide.](https://devanswers.co/allow-less-secure-apps-access-gmail-account/)
- Create a new (free) account with [OpenWeatherMap.org](https://home.openweathermap.org/users/sign_up).
  - Sign in, click your name in the top right, click `My API keys` and copy the Key to [config/config.json](config/config.json)
- _. . . to be continued . . ._
- Run `EmailHandler` on startup
- _something something_ `python3 message.py -m "hello, this is a test message"`


## Troubleshooting
- If you see an error saying `File "/home/pi/.local/lib/python3.7/site-packages/PIL/Image.py", line 109, in <module>` or something about `from . import _imaging as core`, type `sudo rm -rf /home/pi/.local/lib/python3.7/site-packages/PIL/`. If the error persists, notice the directory - you may see `python3.8` or similar - change the rm -rf command to the version seen in your error.


## Credits
- [IpInfo] - Turns IP addresses into latitude and longitude coordinates
- [OpenWeather] - Weather API
- [weather-phat.py] - Code pieces and icons from the weather application sample
- [quotes-what.py] - Message boundaries


   [weather-phat.py]: <https://github.com/pimoroni/inky/blob/master/examples/phat/weather-phat.py>
   [quotes-what.py]: <https://github.com/pimoroni/inky/blob/master/examples/what/quotes-what.py>
   [IpInfo]: <https://ipinfo.io/>
   [OpenWeather]: <https://openweathermap.org/api>


## Donate
<img src="github-images/eth_donate.png" alt="0xbb5f5d978acbde2ec79736cc5398768a35665d42" width="200px" height="200px">
Ethereum: 0xbb5f5d978acbde2ec79736cc5398768a35665d42