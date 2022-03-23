import os
from twilio.rest import Client
#import twilioConfig from one folder up and inside Config_Files folder
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Config_Files import twilioConfig

#   This file holds a function to call a player with a statement. In this case, finding a shiny.
#
#   Setup:
#   Create a config.py folder that includes the following varibles:
#   to_phone_number = 'your number'
#   from_phone_number = 'Twilio number'
#   account_sid = 'from Twilio'
#   auth_token = 'from Twilio'

def found_shiny_text(found_pokemon = '', to_num = twilioConfig.to_phone_number, from_num = twilioConfig.from_phone_number): 
    # This function calls a user and says the message "You Found a Shiny!". Usage: found_shiny_call(to_num, from_num). Num format: Country Code + Area Code + Number (example: '+12223333333')
    sentence = 'You Found a Shiny ' + found_pokemon
    formatted = '<Response><Say>' + sentence + '</Say></Response>'
    account_sid = twilioConfig.account_sid
    auth_token = twilioConfig.auth_token
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=sentence,
        from_=from_num,
        to=to_num)

    # client.calls.create(twiml=formatted, to = to_num, from_ = from_num)
    print("Texting Phone Number: "+str(to_num))
