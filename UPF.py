import SMF
import UE
def Transceiver(signal):
    if signal['msg_type'] == "N4 Session Establishment/Modification Request":
        print(f"UPF: Recieved {signal['msg_type']}")
        signal = {
            'msg_type': "N4 Session Establishment/Modification Response"
        }
        print(f"UPF: Sending {signal['msg_type']}")
        SMF.transceiver(signal)
    
    elif signal['msg_type'] == "N4 Session Modification Request":
        print(f"UPF: Recieved {signal['msg_type']}")
        data = {
            "msg_type": "First Downlink Message",
            "data": "packets"
        }
        print(f"UPF: Sending {signal['msg_type']}")
        UE.DL_RECEIVER(data)

        
