#Importing network functions to be interfaceed with
import AMF
import UDM


def Receiver(signal): # acts the receiver of the AUSF communicating with UDM to retrive authentication information and forward to AMF
    if signal["msg_type"] == "Nausf_UEAuthenticationRequest":
        print(f"AUSF: Received {signal['msg_type']}")
        print("AUSF: Querying UDM to provide authentication")
        signal["msg_type"] = "Nudm_UEAuthentication_GetRequest"
        print(f"AUSF: Sending {signal['msg_type']} to UDM")
        UDM.repo_checker(signal)

    elif signal['msg_type'] == "5G-AKA":
        print(f"AUSF: Recieved the {signal['msg_type']} with the key {signal['key_IV']}")
        print("AUSF: Passing it to AMF")
        AMF.Receiver(signal)

