# Inky Messenger 

##### _Send messages to family or loved ones_
[**image of working device**]


## Features
- Send an ~~email~~ ... ~~text message~~ ... **Discord message** to update the message on the inky phat
  - _Ran into some trouble with different mail servers having different ways of handling message bodies. The Discord bot is cleaner, more stable, and more practical, and can be accessed on [iOS](https://apps.apple.com/us/app/discord-talk-chat-hang-out/id985746746), [Android](https://play.google.com/store/apps/details?id=com.discord&hl=en_US&gl=US), [Windows, Linux, MacOS, Chrome OS, etc.](https://discord.com/)_
- Weather status icon
- Temperature (in Fahrenheit) from OpenWeatherMap API  <sub><sup>_(RIP DarkSky)_</sup></sub>
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
- Run `python3 -m pip install --upgrade pip` and `python3 -m pip install --upgrade Pillow` and `python3 -m pip install discord`
- Create a new (free) account with [OpenWeatherMap.org](https://home.openweathermap.org/users/sign_up).
  - Sign in, click your name in the top right, click `My API keys` and copy the Key to [config/config.json](config/config.json)
- _. . . to be continued . . ._
- Run `DiscordBot.py` on startup
- Cron job for `display.py`; necessary for the date and weather to update
- _something something_ `python3 message.py -m "hello, this is a test message"`
- Create Discord bot:
  - Create a Discord account or sign in to your existing account and head to [https://discord.com/developers/applications](https://discord.com/developers/applications)
  - Click `New Application` in the top right and name it `inky`
  - Click `Bot` on the left column and then `Add Bot` on the right
  - Copy your `TOKEN` and be sure not to share it with anyone. Paste it in `config/config.json` in `discord > token`.
    - You may also enter your discord handle there too. _Be sure to include your hash tag and numbers._ This will act as a whitelist, only messages from `discord > allowed_user` will change the message on the inky phat, but you may also leave it blank to allow anyone in the server to change the message
  - Click `OAuth2` on the left column. Under `SCOPES`, check `bot`. Under `BOT PERMISSIONS`, check `Send Messages`, `Manage Messages`, `Read Message History`
  - Copy the link at the bottom of `SCOPES` - it should end with `&scope=bot` - but don't yet go to it
  - Create a new Discord server and name it whatever you'd like, then visit the link copied in the last step and select the server you've just created



## TODO
- check config.json for email, api_key, etc. if exist, continue
- while searching emails, if wifi goes out, do something to prevent the program from crashing
- while searching emails, if email password changes, put that on the display (maybe? how to determine this?)
- what if an email is spam?
  - Fix: only allow messages from "@txt.att.net", "@tmomail.net", "@messaging.sprintpcs.com", "@vtext.com", "@vzwpix.com", "@vmobl.com"
    - Problem with this fix: only allows for messaging from text message - not email. Potential fix: maybe add an "allowed emails" in config?


## Troubleshooting
- If you see an error saying `File "/home/pi/.local/lib/python3.7/site-packages/PIL/Image.py", line 109, in <module>` or something about `from . import _imaging as core`...
  - Run `sudo rm -rf /home/pi/.local/lib/python3.7/site-packages/PIL/`. If the error persists, notice the directory - you may see `python3.8` or similar - change the `rm -rf` command to the version seen in your error.
- If the Discord bot is showing as offline on the Discord server...
  - Check the connection of the raspberry pi - make sure you can ssh into it
  - Make sure the token is correct and placed in `config/config.json`
  - Check the `log.txt` for an error message from discordbot
- If the Discord bot is not responding, the bot is likely offline and needs to be restarted
- If the Discord bot is saying you're not authorized, make sure you entered your name correctly in `config/config.json`. It should look similar to this: `"allowed_user": "tester#1234"`. _Reminder that this is NOT the bot's name; it is YOUR personal account's name_



## Credits
- [IpInfo] - Turns IP addresses into latitude and longitude coordinates
- [OpenWeatherMap] - Weather API
- [weather-phat.py] - Code pieces and icons from the weather application sample


   [weather-phat.py]: <https://github.com/pimoroni/inky/blob/master/examples/phat/weather-phat.py>
   [IpInfo]: <https://ipinfo.io/>
   [OpenWeatherMap]: <https://openweathermap.org/api>


## Donate
<img src="github-images/eth_donate.png" alt="0xbb5f5d978acbde2ec79736cc5398768a35665d42" width="200px" height="200px">
Ethereum: 0xbb5f5d978acbde2ec79736cc5398768a35665d42