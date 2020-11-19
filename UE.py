from time import sleep
import gNB #import module to access gNB operation
import AMF #import module for NAS messaging with AMF

def RRC_SENDER(message): #function to send the RRC request message
    sleep(1)
    print(f"UE: {message['msg_type']} is sent over {message['channel']} channel")
    gNB.gNB_RECEIVER(message)

def RACH_SENDER(message): # Function to send the Randon access preamble
    sleep(1)
    print('UE: Sending RACH preamble')
    gNB.gNB_RECEIVER(message)

def UL_SENDER(message): #Function to process the messages received message from the transmitter and send it over to the apporpriate network function
    if message['msg_type'] == 'RACH-PRACH':
        RACH_SENDER(message)

    elif message['msg_type'] == 'RRC Connection Request':
        RRC_SENDER(message) 

    elif message['msg_type'] == 'RRCSetupRequest':
        print(f"UE: Sending {message['msg_type']}")
        gNB.DU(message)
    
    elif message['msg_type'] ==  'SecureModeComplete':
        print(F"UE: Sending {message['msg_type']}")
        gNB.DU(message) #sending data to gNB Distributed unit
    
    elif message['msg_type'] == 'RRCReconfigurationComplete':
        print(f"UE: Sending {message['msg_type']}")
        gNB.DU(message)
    
    elif message['msg_type'] == 'REGISTRATION REQUEST':
        signal = {
            'msg_type' : 'REGISTRATION REQUEST',
        }
        print(f"UE: Sending {signal['msg_type']}")
        sleep(1)
        gNB.gNB_RECEIVER(signal) # sending data to the gNB receiver


def DL_RECEIVER(message):

    if message['msg_type'] == 'PSS/SSS': # PSS/SSS signal recieved for synchronization with gNB
        syn_flag = message['sync_signal']
        if syn_flag == 1:
            print(f"UE: {message['msg_type']} signal is recieved at UE and synchronization is done!!!!!!")
            sleep(1)
        return syn_flag
    
    elif message['msg_type'] == 'PBCH': #PBCH signal recieved to intiate System Information reception
        if message['sys_info_trigger'] == 1:
            print(f"UE: {message['msg_type']} signal is recieved at UE and System information reception process will begin")
            sleep(1)       
        return message['sys_info_trigger']
    
    elif message['msg_type'] == 'BCCH-BCH': # MIB is received and processed
        print('UE: Master Information Block has been recieved through BCCH-BCH channel')
        if message['SIB_DECODER_FLAG'] == True:
            print('UE: The SIB decoder information from MIB has been recieved to decode SIB')
            sleep(1)
        return message['SIB_DECODER_FLAG']
    
    elif message['msg_type'] == 'BCCH-DL SCH': # SIB blocks are now recieved and processed
        if message['SIB Type'] == 1: # received SIB1 and print the payload
            print('UE: System Information Block Type 1 has been recieved through BCCH-DL SCH')
            print("--------------System Information Block Type 1-------------")
            print(message)
            sleep(1)
            sib1_flag = True
            return sib1_flag
            
        elif message['SIB Type'] == 2: # received SIB2 and print the payload
            print('UE: System Information Block Type 1 has been recieved through BCCH-DL SCH')
            print("--------------System Information Block Type 2-------------")
            print(message)
            sleep(1)
            print("-------------------STARTING RANDOM ACCESS PROCEURE--------------------")
            payload = {
                'msg_type':'RACH-PRACH',
                'message': 'Random Access Preamble'
            }
            UL_SENDER(payload)

    elif message['msg_type'] == 'RAR':
        print(f"UE: Random Access Response is received through {message['channel']}")
        sleep(1)
        payload = { # payload and signals are used to send the appropriate message to the next network function with appropriate data
            'msg_type': 'RRC Connection Request',
            'channel': 'CCCH-UL-SCH'
        }
        UL_SENDER(payload) # sending to UE uplink sender for transmission to the next network function
        
    elif message['msg_type'] == 'RRC Connection Setup':
        print(f"UE: gNB has sent over RRC aknowledgement and {message['operation']} operation performed over {message['channel']} channel")
        print("*********Initial Access and Registration Procedure Completed***********")
        print("------------------Starting Radio Resource Control Setup----------------")
        signal = {
            'msg_type': "RRCSetupRequest"
        }
        UL_SENDER(signal) 

    elif message['msg_type'] == "RRCSetup":
        print(f"UE: Recieved {message['msg_type']}")
        signal = {
            'msg_type': "RRCSetupComplete"
        }
        sleep(1)
        print(f"UE: Sending {signal['msg_type']}")
        gNB.DU(signal)

    elif message['msg_type'] == 'SecurityModeCommand':
        print(f"UE: {message['msg_type']} recieved")
        sleep(1)
        signal = {
            'msg_type': "SecureModeComplete"
        }
        UL_SENDER(signal)
    
    elif message['msg_type'] == "DL RRC Message":
        print(f"UE: {message['message']} has been recieved")
        signal = {
            'msg_type': "RRCReconfigurationComplete"
        }
        UL_SENDER(signal)
    
    elif message['msg_type'] == "IDENTITY REQUEST":
        signal = {
           'msg_type': "IDENTITY RESPONSE",
           'ue_id': 9789863989
        }
        sleep(1)
        print(f"UE: Sending {signal['msg_type']} with {signal['ue_id']}")
        AMF.Receiver(signal)
    
    elif message['msg_type'] == "SECURITY MODE COMMAND":
        print(f"UE: Received {message['msg_type']}")
        signal = {
            'msg_type': "SECURITY MODE COMPLETED"
        }
        print(f"UE: Sending {signal['msg_type']}")
        AMF.Receiver(signal)
    
    elif  message['msg_type'] == "REGISTRATION ACCEPT":
        print(f"UE: Received {message['msg_type']}")
        message['msg_type'] = "REGISTRATION COMPLETE"
        print(f"UE: Sending {message['msg_type']}")
        AMF.Receiver(message)

    elif message['msg_type'] == "PDU Session Establishment Request":
        print(f"UE: Sending {message['msg_type']}")
        payload = { # PDU Session request payload sent by UE with the required inforamtion
        'msg_type': "PDU Session Establishment Request",
        'User Location': 60616,
        'Access Type Location': "",
        'PDU Session ID': 85997954,
        'Request Type': "Initial Request"
        }
        sleep(1)
        AMF.Receiver(payload)

    elif message['msg_type'] == "N2 PDU Session Request(NAS msg)":
        print(f"UE: Recieved {message['msg_type']}")
        signal = {
            'msg_type': "N2 PDU Session ACK"
        }
        print(f"UE: Sending {signal['msg_type']}")
        print("UE: Sending First Uplink Message")
        sleep(1)
        AMF.Receiver(signal)
    
    elif message['msg_type'] == "First Downlink Message":
        print(f"UE: Recieved {message['msg_type']}")
        print("UE: PDU Session has been established")
        print("UE: Updated SM Context with SMF")
        print("---------------Simulation has been completed----------------")

        
        
