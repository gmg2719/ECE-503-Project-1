#import network function to interface with
import SMF


def Tranciever(signal): #function to provide the policy information
    if signal['msg_type'] == "SM Policy association establishment":
        print(f"PCF: Recieved {signal['msg_type']}")
        print("PCF: Retreiving Policy info")
        signal = {
            "msg_type": "Session Establishment Response",
            "policy_info": "subscriber data",
            "PCC Rules": True
        }
        SMF.transceiver(signal)