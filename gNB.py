from time import sleep
import UE
import AMF

def RRC_SENDER():
    payload = {
        'msg_type': 'RRC Connection Setup',
        'operation': 'MAC Contention Resolution',
        'channel': 'PDSCH'
    }
    print("gNB: RRC connection setup message is sent from gNB")
    UE.DL_RECEIVER(payload)

def RAR_SENDER():
    payload = {
        'msg_type': 'RAR',
        'channel': 'DL-SCH-PDSCH',
        'C-RNTI': 5
    }
    print("gNB: Random Access Response is sent.")
    UE.DL_RECEIVER(payload)

def SIB_SENDER():
    SIB1 = {
        'msg_type': 'BCCH-DL SCH',
        'SIB Type': 1,
        'PLMN': "xyz",
        'TAC': 60616,
        'next SIB': 2
    }
    print('gNB: SIB1 sent at gNB')
    sib1_flag = UE.DL_RECEIVER(SIB1)
    sleep(1)
    if sib1_flag == True:
        SIB2 = {
        'msg_type': 'BCCH-DL SCH',
        'SIB Type': 2,
        'HARQ': "available",
        'next SIB': 3
        }
        print('gNB: SIB2 is sent at gNB')
        UE.DL_RECEIVER(SIB2)
        sleep(1)
    

def MIB_SENDER():
    payload = {
        'msg_type': 'BCCH-BCH',
        'SIB_DECODER_FLAG' : True,
        'SIB_decoder_key': "adklfjlkajsdfkljlk"
    }
    print('gNB: MIB is sent at gNB')
    SIB1_DECODER = UE.DL_RECEIVER(payload)
    sleep(1)
    if SIB1_DECODER == True:
        SIB_SENDER() 

def PBCH_SENDER():
    payload = {
         'msg_type': 'PBCH',
         'sys_info_trigger': 1
    }
    print("gNB: PBCH is sent at gNB")
    sys_info_trigger = UE.DL_RECEIVER(payload)
    sleep(1)
    if sys_info_trigger == 1:
        MIB_SENDER()

def PSS_SSS_sender(): #sending Primary and secondary synchronization signal
    
    payload = {
        'msg_type': 'PSS/SSS',
        'sync_signal': 1,
    }
    print('gNB: PSS/SSS is sent at gNB') 
    sleep(1)
    syn_flag = UE.DL_RECEIVER(payload)
    if syn_flag == 1:
        PBCH_SENDER()

def CU(signal):
    if signal['msg_type'] == 'Initial RRC':
        print(f"gNB-CU: Recieved {signal['message']}")
        print("gNB-CU: UE F1AP ID allocated")
        signal = {
            'msg_type': "DL RRC",
            'message': "DL RRC MESSAGE TRANSFER"
        }
        sleep(1)
        print("gNB-CU: Sending RRC Setup signal")
        DU(signal)

    elif signal['msg_type'] == 'RRCSetupComplete':
        print('******Setting up UE context********')
        signal = {
            'msg_type': 'UEContextSetup',
            'message': "Initial UE MESSAGE"
        }
        AMF.Receiver(signal)
    elif signal['msg_type'] == 'AMFContestResponse':
        sleep(1)
        print("Forwarding UE Context Setup Request")
        DU(signal)

    elif signal['msg_type'] == 'UE CONTEXT SETUP RESPONSE':
        sleep(1)
        print(f"gNB-CU: {signal['msg_type']} has been recieved")
        print(f"gNB-CU: {signal['message']} has been recieved")
        signal ={
            'msg_type': "DL RRC Message",
            'message': "RRCReconfiguration"
        }
        print(f"gNB-CU: {signal['msg_type']} sent with {signal['msg_type']} encapsulated")
        DU(signal)
    
    elif signal['msg_type'] == 'UL RRC Message Transfer':
        sleep(1)
        print(f"gNB-CU: {signal['msg_type']} has been recieved")
        signal = {
            'msg_type': "Initial Context Setup Response"
        }
        AMF.Receiver(signal)

def DU(signal):

    if signal['msg_type'] ==  'RRCSetupRequest':
        signal = {
            'msg_type': "Initial RRC",
            'message': "Initial UL RRC Message Transfer",
            'C-RNTI': "ALLOCATING"
        }
        print(f"gNB-DU: Now sending {signal['message']}")
        CU(signal)

    elif signal["msg_type"] == "DL RRC":
        signal ={
            'msg_type': "RRCSetup"
        }
        print(f"gNB-DU: Sending {signal['msg_type']}")
        UE.DL_RECEIVER(signal)

    elif signal['msg_type'] == "RRCSetupComplete":
        signal['message'] = "UL RRC Message Transfer"
        print(f"gNB-DU: Sending {signal['message']}")
        CU(signal)
    
    elif signal['msg_type'] == "AMFContestResponse":
        signal = {'msg_type': 'SecurityModeCommand',
                'message': 'UE Context Message'}
        print(f"{signal['message']} is sent with {signal['msg_type']} encapsulated")
        UE.DL_RECEIVER(signal)    
    
    elif signal['msg_type'] == 'SecureModeComplete':
        signal = {
            'msg_type': 'UE CONTEXT SETUP RESPONSE',
            'message': "UL RRC Message"
        }
        print(f"gNB-DU: {signal['msg_type']} is sent to CU")
        CU(signal)
    
    elif signal['msg_type'] ==  "DL RRC Message":
        print(f"gNB-DU: {signal['msg_type']} has been received")
        print(f"gNB-DU: {signal['message']} has been sent")
        UE.DL_RECEIVER(signal)
    
    elif signal['msg_type'] == "RRCReconfigurationComplete":
        print(f"gNB-DU: {signal['msg_type']} has been recieved")
        signal = {
            'msg_type': 'UL RRC Message Transfer'
        }
        print(f"gNB-CU: {signal['msg_type']} has been sent")
        CU(signal)
    
def gNB_SENDER(operation_trigger):
    if operation_trigger['msg_type'] == 'PSS/SSS':
        print("---------------STARTING CONNECTION PROCEDURE-------------------")
        print("*******Starting Initial Access and REgistration Procedure******")
        sleep(1)
        PSS_SSS_sender()
    
    elif operation_trigger['msg_type'] == 'RAR':
        sleep(1)
        RAR_SENDER()
    
    elif operation_trigger['msg_type'] == 'RRC':
        sleep(1)
        RRC_SENDER()

def gNB_RECEIVER(payload):
    if payload['msg_type'] == 'RACH-PRACH':
        print(f"gNB: {payload['message']} has been recieved from UE")
        sleep(1)
        operation_trigger = {
            'msg_type': 'RAR'
        }
        gNB_SENDER(operation_trigger)
    elif payload['msg_type'] == 'RRC Connection Request':
        print(f"gNB: {payload['msg_type']} has been received")
        operation_trigger = {
            'msg_type': 'RRC'
        }
        gNB_SENDER(operation_trigger)

    elif payload['msg_type'] == 'REGISTRATION REQUEST':
        print(f"gNB: Recieved {payload['msg_type']}")
        signal = {
            'msg_type' : 'REGISTRATION REQUEST',
         
            'protocol': "NG-AP"
        }
        print(f"gNB: Sending {signal['msg_type']} over {signal['protocol']} protocol")
        sleep(1)
        AMF.Receiver(signal)
        

