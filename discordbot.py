import discord
import json
from json.decoder import JSONDecodeError
import logging
import sys

'''

    This application should run on boot and stay running at all times. The 
    purpose of it is to take in a message on discord, save it in the 
    configuration file, and refresh the inky phat display.

'''

client = discord.Client()

logging.basicConfig(filename = 'log.txt', format='%(asctime)s [%(name)s]: %(message)s', level=logging.INFO) #log.txt: time [discordbot]: message
#logging.getLogger().addHandler(logging.StreamHandler()) #print to console
logger = logging.getLogger('DiscordBot')

config_location = "../config.json" #TODO change this on release

try:
    with open(config_location) as json_data_file:
        config = json.load(json_data_file)
except IOError:
    logger.error("Configuration file does not exist in config/config.json. Pull a new one from https://github.com/corey-schneider/inky-phat-messenger/blob/main/config/config.json")
    sys.exit("Configuration file does not exist in config/config.json. Pull a new one from https://github.com/corey-schneider/inky-phat-messenger/blob/main/config/config.json")

try:
    TOKEN = config["discord"]["token"]
    ALLOWED_USER = config["discord"]["allowed_user"]
except (JSONDecodeError, KeyError):
    logger.error("Discord token not found in config.json")
    sys.exit("Discord token not found in config.json")

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if str(message.author) == ALLOWED_USER or ALLOWED_USER == "":
        if message.content.startswith(''):
            if config["message"] != message.content: # if the pi is restarted and the message is the same, don't rewrite it
                config["message"] = message.content
                with open(config_location, "w") as f:
                    json.dump(config, f)
                    print("Successfully wrote new message to config.json")
            else:
                print("Messages were the same; not rewriting.")
                #logger.info("same messages")
            await message.channel.send("Sent to inky phat: \""+message.content+"\"")
    else:
        await message.channel.send('You are not authorized to send a message.')
        logger.info("User does not match. Ignoring message. Expected: \""+ALLOWED_USER+"\", got \""+str(message.author)+"\".")
        print("User does not match. Ignoring message. Expected: \""+ALLOWED_USER+"\", got \""+str(message.author)+"\".")

client.run(TOKEN)