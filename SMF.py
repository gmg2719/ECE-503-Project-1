# import other network functions and modules required for operation
import json 
import PCF
import UPF
import AMF
def session_checker(signal): # function to perform to check if a previous session with UE already exists byb checking the sessions database
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

def session_maker(signal): #function to create a session if this is new session requested by the UE
    with open('pdu_sessions.json', 'r') as json_file:
        sessions = json.load(json_file)
        sessions['PDU_SESSIONS'].append(signal['PDU Session ID'])
        with open('pdu_sessions.json', 'w') as json_file:
            json.dump(sessions, json_file, indent=4)
            print("SMF: The new session has been created and authenticated")
            print("SMF: Retrieving policy info from PCF")
            signal = {
                "msg_type": 'SM Policy association establishment'
            }
            transceiver(signal)
 
def transceiver(signal): #  Function to perform the TRANCEIVER operations of the SMF
    if signal['msg_type'] == "SM Policy association establishment":
        print(f"SMF: Sending {signal['msg_type']}")
        PCF.Tranciever(signal)
    
    elif signal['msg_type'] == "Session Establishment Response":
        print(f"SMF: Recieved {signal['msg_type']}")
        print("SMF: Selecting UPF")
        signal = {
            'msg_type': "N4 Session Establishment/Modification Request"
        }
        print(f"SMF: Sending {signal['msg_type']}")
        UPF.Transceiver(signal)

    elif signal['msg_type'] == "N4 Session Establishment/Modification Response":
        print(f"SMF: Recieved {signal['msg_type']}")
        signal = {
            "msg_type": "Namf_Communication_N1N2MessageTransfer",
            "PDU Session ID": 85997954,
            "QFI": 5
        }
        print(F"SMF: Sending {signal['msg_type']}")
        AMF.Receiver(signal)
    
    elif signal['msg_type'] == "Initiate PDU Session and SM Context":
        signal =  {
            'msg_type': "N4 Session Modification Request"
        }
        print(F"SMF: Sending {signal['msg_type']}")
        UPF.Transceiver(signal)


