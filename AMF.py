import runner
import gNB
import UE
import AUSF

def Receiver(signal):
    if signal['msg_type'] == 'UEContextSetup':
        print(f"AMF: Recieved {signal['message']}")
        signal['msg_type']  = "AMFContestResponse"
        signal['message'] = 'INITIAL CONTEXT SETUP REQUEST'
        print(f"AMF: Sending {signal['message']}")
        Transmitter(signal)
    
    elif signal['msg_type'] == "Initial Context Setup Response":
        print(f"AMF: {signal['msg_type']} has been recieved")
        print("*********** UE Context Setup*************")
        print("--------------Radio Resource Control Setup Completed------------")
        runner.Reg_trigger()

    elif signal['msg_type'] == 'REGISTRATION REQUEST':
        print(f"AMF: Recieved {signal['msg_type']} through {signal['protocol']}")
        print(f"AMF: Requesting Identity")
        signal = {
            'msg_type': "IDENTITY REQUEST"
        }
        UE.DL_RECEIVER(signal)
    elif signal['msg_type'] == 'IDENTITY RESPONSE':
        print(f"AMF: Received {signal['msg_type']} with {signal['ue_id']}")
        signal['msg_type'] = "Nausf_UEAuthenticationRequest"
        print(f"AMF: Sending {signal['msg_type']}")
        AUSF.Receiver(signal)

        


    

def Transmitter(signal):
    if signal['msg_type'] == "AMFContestResponse":
        gNB.CU(signal)