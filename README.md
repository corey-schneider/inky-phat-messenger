# Inky Messenger 

##### _Send messages to family or loved ones_
[**image of working device**]
## Features
- Send an email or text message to update the message
- Weather status icon
- Temperature (in fahrenheit)
- Date
- Can send a message up to 4 lines long
- Makes one call to the IpInfo API per SSID
  
## Setup
- Download [Raspberry Pi OS Lite](https://www.raspberrypi.org/software/operating-systems/)
- Flash image to SD card with [Raspberry Pi imager](https://www.raspberrypi.org/software/)
- Download [wpa_supplicant.conf](wpa_supplicant.conf) and [ssh](ssh)
  - Modify [wpa_supplicant.conf](wpa_supplicant.conf) to include your wifi credentials
- SSH into the Raspberry Pi
- Download the necessary files through `curl https://get.pimoroni.com/inky | bash`
- Enable SPI and I2C. To do this, run `sudo raspi-config`, scroll to Interface Options, and enable them.
  - While in `raspi-config`, change the time zone (unless you live in the UK). Select `Localisation Options` > `Timezone`.
- Run `sudo apt-get update` and `sudo apt-get upgrade`
- Create a new email. Modify [config/email.txt](config/email.txt) to include this new receiving email
- 
- _. . . to be continued . . ._
- cron job
- _something something_ `python3 message.py -m "hello, this is a test message"`

## Credits
- [weather-phat.py] - Code pieces and icons from the weather application sample
- [quotes-what.py] - Message boundaries
- [IpInfo] - Turns IP addresses into latitute and longitute coordinates
- [Dark Sky] - Weather API


   [weather-phat.py]: <https://github.com/pimoroni/inky/blob/master/examples/phat/weather-phat.py>
   [quotes-what.py]: <https://github.com/pimoroni/inky/blob/master/examples/what/quotes-what.py>
   [IpInfo]: <https://ipinfo.io/>
   [Dark Sky]: <https://darksky.net/>

## Donate
<img src="github-images/eth_donate.png" alt="0xbb5f5d978acbde2ec79736cc5398768a35665d42" width="200px" height="200px">
Ethereum: 0xbb5f5d978acbde2ec79736cc5398768a35665d42