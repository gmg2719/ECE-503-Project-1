import json
import datetime
import time as ti
#from AN import AN_con_estab_op, AN_data_exch
from os import path

#method to create a unique session for each call
def session_maker():
    calling_number = input("Please enter a 10 digit number you would like to call: ")
    caller_id =  input('Please enter your user ID: ')
    caller_id = int(caller_id)
    # Returns unix timestamp for current time
    timestamp = ti.time()
    # Get datetime object in local time
    d = datetime.datetime.fromtimestamp(timestamp)
    # Return unix timestamp from datetime object
    date = d.strftime("%d.%m.%y")
    time = d.strftime("%H:%M:%S")
    print(f"Caller with Session ID {caller_id} making call request")
    #session data package for persistant storage of the session information
    caller = {
    f'caller: {caller_id}': {
        'caller_id': caller_id,
        'calling_number': calling_number,
        'date': date,
        'time': time
     }
    }
    #data message to be sent after establishing the connection
    payload = {
        'CALLER_MESSAGE': 'Hello, How are you',
    }

    return caller, payload

#Method for the logical simulation of the UE's operation
def UE_Operation():
    call_option = 'yes' #Flag for making a call
    while(call_option == 'yes' or call_option =='y'):
        caller, payload = session_maker() # Making a unique session with phone number and unique caller ID
        json_file = json.dumps(caller) # creating the JSON message payload
    
        call_option = input('Do you wanna make another call? (yes/no): ')

if __name__ == "__main__":
    UE_Operation()