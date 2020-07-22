## JSON Data generator 
import json 
import argparse
import logging 
import random 
from datetime import date , datetime , timedelta
from faker import Faker

# GLobal Variables 
fake = Faker()


def GetArgs():
        """
        Supports the command-line arguments listed below.
        """
        parser = argparse.ArgumentParser(
           description='Two arguments needs to be passed -o (number of activities ), -f (file name)')
        parser.add_argument('-o', '--activity_n', type =int, action='store',
                                           help='Number of activities ')
        parser.add_argument('-f', '--output_file_name', action='store',
                                           help='JSON file name store in the local directory')
        #args = parser.parse_args()
        args = parser.parse_args()
      #  print (args)
        return args 
        

    

def SetupLogging():
    try:
        debug = 0
        if debug == 1 :
           info = logging.DEBUG
        else :
           info = logging.INFO
        logger = logging.getLogger()
        logger.setLevel(info)
        #create a file handler
        handler = logging.FileHandler('create_json.log')
        handler.setLevel(info)
        # create a logging format
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        # add the handlers to the logger
        logger.addHandler(handler)
    except IOError:
        logger.error("cannot open log file",exc_info=True)

        
def Random_Number(a, b):
    v_num=random.randrange(a, b)
    return v_num   
def Random_Names():
    #v_names=["user1", "user2", "user3", "user4", "user5"]
    return fake.last_name()

def Static_Dict():
    v_ret = {}
    v_performed_at = datetime.now().strftime("%d/%m/%Y")
    #type(v_performed_at)
    #Random Hour , min , sec Logic 
    v_hr = Random_Number(10,23)
    v_min = Random_Number(10,59)
    v_sec = Random_Number(10,59)
    #print(v_performed_at)
    v_performed_at = v_performed_at + " " + str(v_hr) + ":" + str(v_min) + ":" + str(v_sec)
    #print(v_performed_at)
    v_ticket_id = Random_Number(1000 , 10000)
    v_performer_typeuser = Random_Names()
    v_performer_id = Random_Number(100000,1000000)
    v_ret = {
        "performed_at":  v_performed_at,
        "ticket_id": v_ticket_id,
        "performer_type": v_performer_typeuser,
        "performer_id": v_performer_id 
        
    }
    #print (v_ret)
    return v_ret 


def List_Config_Setup():
    v_arr = ["shipping_address", "shipment_date","category","contacted_customer","issue_type","source","status","priority","group","agent_id","requester","product","note"]
    v_int =Random_Number(7,13)
    return random.sample(v_arr,v_int)
    # For the jSON Activity to have some data 
    #i have picked the array to return atleast  7 of the listed activities and above from the list . Why 7 ? (Its an odd number)

def Set_Activity(i):
    v_category = ["Phone", "Car","Choc","Cake","Pizza","vegan","Chicken"]
    v_cat_prod = random.choice(v_category) # setting both product and category same 
    v_contacted_customer=["true","false"]
    v_issue_type = ["Incident","Resolved","callback"]
    v_status = ["Closed","Resolved","Waiting for Customer","Waiting for Third Party","Pending"]
    v_note = {"id": 4025864,"type": 4}
    v_group = "refund"
    switcher={
        "shipping_address": fake.address(),
        "shipment_date": fake.date() ,
        "category":v_cat_prod,
        "contacted_customer" : random.choice(v_contacted_customer),
        "issue_type": random.choice(v_issue_type),
        "source": random.randrange(1,9),
        "status": random.choice(v_status),
        "priority": random.randrange(1,9),
        "group": v_group,
        "agent_id": random.randrange(10000,19999),
        "requester": random.randrange(10000,19999),
        "product": v_cat_prod,
        "note":v_note
               
    }
    return switcher.get(i,"")
        
    
    
def Dynamic_Dict():
    v_keys = []
    v_keys = List_Config_Setup()
    v_ret_dict = {}
    for v_key in v_keys:
        v_value = Set_Activity(v_key)
        #print (v_key , v_value)
        v_ret_dict[v_key] = v_value
        #print (v_ret_dict)
    return v_ret_dict
  
def MergeDict():
    v_merge_dict = {}
    v_static_data={}
    v_static_data=Static_Dict()
    v_dynamic_dict={}
    v_dynamic_dict = Dynamic_Dict()  
    v_activity = {"activity": v_dynamic_dict}
    v_merge_dict.update(v_static_data)
    v_merge_dict.update(v_activity)
    return v_merge_dict
    
    
def JsonStruct(n,v_output_file_name):
    #Defining 24 Hours window - Assuming the report starts at 10 AM and ends at 9:59 AM next day  
    # set 24 Hours apart 
    v_start_at = datetime.now().strftime('%d-%m-%Y')
    v_end_at= (datetime.now() + timedelta(hours=23)).strftime('%d-%m-%Y')

   # logging.info (v_dict)
    #v_activities_data =  ""
    
    v_new_merg_str = ""
    
    for i in range (n):
        v_new = {}
        v_new = MergeDict()
       # print (v_new)
        v_new_str = str(v_new)
        if not v_new_merg_str:
            v_new_merg_str = v_new_str
        else:
            v_new_merg_str = v_new_merg_str + "," + v_new_str
        
        
    #print (v_new_merg_str) 
    v_new_merg_str = v_new_merg_str.replace('\'','\"')
   # print (v_new_merg_str) 
    
    
    #v_new_merg_dict = json.loads(v_new_merg_str)
    #activities_data =  {"activities_data" : [v_activities_data] }
    #print (activities_data)
    v_dict= {
    "metadata": {
                 "start_at": v_start_at + " 10:00:00 +0000",
                 "end_at":  v_end_at + " 09:59:59 +0000",
                 "activities_count": n
    },
    "activities_data" : [ v_new_merg_str] 
        
    }
    print (v_output_file_name)
    with open(v_output_file_name, 'w') as json_file:
    #with open('test.json', 'w') as json_file:
        json.dump(v_dict, json_file)
        
        
def Main():
    v_args = GetArgs() 
    logging.info(v_args.activity_n)
    v_activity_n=v_args.activity_n
#    v_activity_n=3 # comment Post  testing 
    v_output_file_name=v_args.output_file_name
 #   v_output_file_name="test.json"
    JsonStruct(v_activity_n, v_output_file_name)
    
    
# MAIN  - 
SetupLogging()
Main()
