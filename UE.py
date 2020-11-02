from time import sleep
import gNB

def RRC_SENDER(message):
    sleep(1)
    print(f"UE: {message['msg_type']} is sent over {message['channel']} channel")
    gNB.gNB_RECEIVER(message)

def RACH_SENDER(message):
    sleep(1)
    print('UE: Sending RACH preamble')
    gNB.gNB_RECEIVER(message)

def UL_SENDER(message):
    if message['msg_type'] == 'RACH-PRACH':
        RACH_SENDER(message)
    elif message['msg_type'] == 'RRC Connection Request':
        RRC_SENDER(message)

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
        if message['SIB Type'] == 1:
            print('UE: System Information Block Type 1 has been recieved through BCCH-DL SCH')
            print("--------------System Information Block Type 1-------------")
            print(message)
            sleep(1)
            sib1_flag = True
            return sib1_flag
            
        elif message['SIB Type'] == 2:
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
        payload = {
            'msg_type': 'RRC Connection Request',
            'channel': 'CCCH-UL-SCH'
        }
        UL_SENDER(payload)
        
    elif message['msg_type'] == 'RRC Connection Setup':
        print(f"UE: gNB has sent over RRC aknowledgement and {message['operation']} operation \
            performed over {message['channel']} channel")
        print("*********Initial Access and Registration Procedure Completed***********")


# if __name__ == "__main__":
#     UE_operation()