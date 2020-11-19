import json
import AUSF
import AMF
def AKA_procedure():#Function to perform the 5G-aka procedure
    print("UDM: Starting 5G AKA exchange procedure")
    print("UDM: Sending the key over to AUSF")
    signal = {
        'msg_type': "5G-AKA",
        "key_IV": 40572845908230945890
    }
    AUSF.Receiver(signal)
def Transiever(signal): #Function to perform the AMF transmitter
    if signal['msg_type'] == "Nudm_UECM_Registration_Request":
        print(f"UDM: Recieved {signal['msg_type']}")
        signal['msg_type'] = "Nudm_UECM_Registration_Response"
        print(f"UDM: Sending {signal['msg_type']}")
        AMF.Receiver(signal)

    elif signal['msg_type'] == 'Nudm_SDM_GetRequest':
        print(f"UDM: Received {signal['msg_type']} ")
        print(f"UDM: Retrieving subscription data")
        signal = { #payload with subscription
            'msg_type': 'Nudm_SDM_GetResponse',
            'subscription': {
                'plan':'$30/month',
                'data_cap': "5 GB"
            }
        }
        print(f"UDM: Sending {signal['msg_type']} with subscription plan {signal['subscription']['plan']} and data capacity {signal['subscription']['data_cap']}")
        AMF.Receiver(signal)
        
def repo_checker(signal):
    with open("udm_db.json", 'r') as json_file:
        ue = json.load(json_file)
        id_list = ue["ue_ids"]  # getting user IDs from existing database
        print(f"Existing user in the DB {id_list}")
        print(f"Our UE ID {signal['ue_id']}")
        if signal['ue_id'] in id_list:
            flag = True #User exists and can be authenticated 
            print("UDM: User exists and can be authenticated ")
            AKA_procedure()
        else:
            flag = False #User does not exists and cannot be authenticated 
            print("UDM: User does not exists and cannot be authenticated")