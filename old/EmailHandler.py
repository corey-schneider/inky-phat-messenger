from json.decoder import JSONDecodeError
import time
import imaplib
import email
import json
import logging
import sys
from email.header import Header, decode_header, make_header

'''

    This file pulls in an email and reads it on a 30 second interval. It
    only works with Verizon SMS being sent to a Gmail account. Due to 
    the restriction, this code is being kept in the 'old' folder, as 
    it may be useful in solving someone's similar problem in the future.

'''


config_location = "../config.json" #TODO change this on release
logger = logging.getLogger('EmailHandler')
logging.basicConfig(filename = 'log.txt', format='%(asctime)s [%(name)s]: %(message)s', encoding='utf-8', level=logging.DEBUG) #log.txt: time [emailhandler]: message
logging.getLogger().addHandler(logging.StreamHandler()) #print to console

try:
    with open(config_location) as json_data_file:
        config = json.load(json_data_file)
except IOError:
    logger.error("Configuration file does not exist in config/config.json. Pull a new one from https://github.com/corey-schneider/inky-phat-messenger/blob/main/config/config.json")
    sys.exit(0)

mail = imaplib.IMAP4_SSL('imap.gmail.com')
REFRESH_INTERVAL = 30 # seconds
latest_email_uid = ''

try:
    USERNAME = config["email"]["username"]
    PASSWORD = config["email"]["password"]
except (JSONDecodeError, KeyError):
    logger.error("Email credentials not found in config.json")
    sys.exit(0)

try:
    mail.login(USERNAME, PASSWORD)
    mail.list()
except: # TODO except what?
    logger.error("Invalid username or password.")
    sys.exit(0)


print("Scanning email "+USERNAME+" ...")

while True:
    mail.select("Inbox", readonly=True)
    result, data = mail.uid('search', None, "ALL") # search and return all uids
    ids = data[0] # data is a list.
    id_list = ids.split() # ids is a space separated string

    if id_list[-1] == latest_email_uid:
        print("No new emails.")
        time.sleep(REFRESH_INTERVAL)
    else:
        print("Found a new email!")
        for num in id_list:
            result, data = mail.uid('fetch', num, '(RFC822)') # fetch the email headers and body (RFC822) for the given ID
        if result == 'OK':
            email_message_raw = email.message_from_bytes(data[0][1]) # better formatting
            email_from = str(make_header(decode_header(email_message_raw['From'])))
            email_date = str(make_header(decode_header(email_message_raw['Date'])))
            print("From: "+email_from+" on "+email_date)

            message = email.message_from_string(str(email_message_raw))
            print("Message: \""+message.get_payload().strip()+"\"")
            
            if config["message"] != message.get_payload().strip(): # if the pi is restarted and the message is the same, don't rewrite it
                config["message"] = message.get_payload().strip()
                with open(config_location, "w") as f:
                    json.dump(config, f)
                    logger.info("Successfully wrote new message to config.json")
            else:
                logger.info("Messages were the same; not rewriting.")
            
            latest_email_uid = id_list[-1]
        time.sleep(REFRESH_INTERVAL)