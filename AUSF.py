import AMF
import UDM


def Receiver(signal):
    if signal["msg_type"] == "Nausf_UEAuthenticationRequest":
        print(f"AUSF: Received {signal['msg_type']}")
        print("AUSF: Querying UDM to provide authentication")
        signal["msg_type"] = "Nudm_UEAuthentication_GetRequest"
        print(f"AUSF: Sending {signal['msg_type']} to UDM")
        flag = UDM.repo_checker(signal)

