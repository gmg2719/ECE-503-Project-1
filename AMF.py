import gNB
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

def Transmitter(signal):
    if signal['msg_type'] == "AMFContestResponse":
        gNB.CU(signal)