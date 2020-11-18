import json 

def session_checker(signal):
    with open('pdu_sessions.json', 'r') as json_file:
        sessions = json.load(json_file)
        sess_list = sessions['PDU_SESSIONS']
        print(f"SMF: Existing user in the DB {sess_list}")
        print(f"SMF: Our UE ID {signal['PDU Session ID']}")
        if signal['PDU Session ID'] in sess_list:
            print("SMF: A previous PDU session already exists this sessior will be pulled up")
            return True
        else:
            return False

def session_maker(signal):
    with open('pdu_sessions.json', 'w') as json_file:
        
