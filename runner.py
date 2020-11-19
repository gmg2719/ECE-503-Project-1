# This is the programs that is used to trigger various procudure in the Intial access of the UE.
import gNB
import UE
def Reg_trigger(): #function to trigger the UE Registration procedure
    print("----------------Starting the UE Registration Procedure---------------")
    operation_trigger = {
        'msg_type': "REGISTRATION REQUEST"
    }
    UE.UL_SENDER(operation_trigger)

def PDU_trigger(): #function to trigger the PDU Session Establishment Procedure
    print("-----------------Starting PDU Session Establishement----------------")
    payload = {
        'msg_type': "PDU Session Establishment Request",
    }
    UE.DL_RECEIVER(payload)

    



if __name__ == "__main__":
    operation_trigger = { # payload sent to send the sync signal from gNB to UE
        'msg_type': 'PSS/SSS'
    }
    gNB.gNB_SENDER(operation_trigger)
