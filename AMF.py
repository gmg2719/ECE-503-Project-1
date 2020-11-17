import runner
import gNB
import UE
import AUSF
import UDM

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
    
    elif signal['msg_type'] == '5G-AKA':
        print(f"AMF: Recieved the {signal['msg_type']} with the key {signal['key_IV']}")
        signal['msg_type'] = 'SECURITY MODE COMMAND'
        print(f"AMF: Sending the {signal['msg_type'] } with key {signal['key_IV']}")
        UE.DL_RECEIVER(signal)
    
    elif signal['msg_type'] == 'SECURITY MODE COMPLETED':
        print(f"AMF: Received {signal['msg_type']}")
        print(f"AMF: Device Equipment identity and registration process is done in the background")
        signal = {
            'msg_type': "Nudm_UECM_Registration_Request"
        }
        print("AMF: Retrieving the UE Context from UDM")
        print(f"AMF: Sending {signal['msg_type']}")
        UDM.Transiever(signal)
    
    elif signal['msg_type'] == "Nudm_UECM_Registration_Response":
        print(f"AMF: Received {signal['msg_type']} ")
        signal['msg_type'] = "Nudm_SDM_GetRequest"
        print(f"AMF: Sending {signal['msg_type']} ")
        UDM.Transiever(signal)

    elif signal['msg_type'] == 'Nudm_SDM_GetResponse':
        print(f"AMF: Received {signal['msg_type']} ")
        print(f"AMF: Subscription plan {signal['subscription']['plan']} and data capacity {signal['subscription']['data_cap']}")
        signal['msg_type'] = "REGISTRATION ACCEPT"
        print(f"AMRF: Sending Registration Accept")
        Transmitter(signal)
    
    elif signal['msg_type'] == "REGISTRATION COMPLETE":
        print(f"AMF: Received {signal['msg_type']} ")
        print("--------------------Finished Initial UE Registration Procedure--------------")
        runner.PDU_trigger()
    
    
    elif signal['msg_type'] == "PDU Session Establishment Request":
        print(f"AMF: Received {signal['msg_type']}")
        print(f"AMF: Received payload {signal}")
        print(f"AMF: ")

def Transmitter(signal):
    if signal['msg_type'] == "AMFContestResponse":
        gNB.CU(signal)

    elif  signal['msg_type'] == "REGISTRATION ACCEPT":
        UE.DL_RECEIVER(signal)