import gNB
import UE
def Reg_trigger():
    print("----------------Starting the UE Registration Procedure---------------")
    operation_trigger = {
        'msg_type': "REGISTRATION REQUEST"
    }
    UE.UL_SENDER(operation_trigger)

def PDU_trigger():
    print("-----------------Starting PDU Session Establishement----------------")
    payload = {
        'msg_type': "PDU Session Establishment Request",
    }
    UE.DL_RECEIVER(payload)

    



if __name__ == "__main__":
    operation_trigger = {
        'msg_type': 'PSS/SSS'
    }
    gNB.gNB_SENDER(operation_trigger)
