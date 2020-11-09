import json

def repo_checker(signal):
    with open("udm_db.json", 'r') as json_file:
        ue = json.load(json_file)
        id_list = ue["ue_ids"]  # getting user IDs from existing database
        print(f"Existing user in the DB {id_list}")
        print(f"Our UE ID {signal['ue_id']}")
        if signal['ue_id'] in id_list:
            flag = True #User exists and can be authenticated 
            print("UDM: User exists and can be authenticated ")
        else:
            flag = False #User does not exists and cannot be authenticated 
            print("UDM: User does not exists and cannot be authenticated")