import gNB
import UE
def Reg_trigger():
    print("----------------Starting the UE Registration Procedure---------------")
    operation_trigger = {
        'msg_type': "REGISTRATION REQUEST"
    }
    UE.UL_SENDER(operation_trigger)





if __name__ == "__main__":
    operation_trigger = {
        'msg_type': 'PSS/SSS'
    }
    gNB.gNB_SENDER(operation_trigger)
