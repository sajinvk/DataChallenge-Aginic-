import json
import pandas as pd
import os  
import  argparse


def GetArgs():
        """
        Supports the command-line arguments listed below.
        """
        parser = argparse.ArgumentParser(
           description='One arguments needs to be passed -f (file name)')
        parser.add_argument('-f', '--input_file_name', action='store',
                                           help='JSON file name store in the local directory')
        #args = parser.parse_args()
        args = parser.parse_args()
      #  print (args)
        return args 


# Read JSON as string and then to tuple 
def Read_Json(v_input_file_name):
    v_data = json.load(open(v_input_file_name))
    v_str_data=""
    v_str_data= str(v_data["activities_data"][0])
    #re.findall(r"\,\{\"performed_at\"\:",x)
    v_tuple = eval(v_str_data)
    return v_tuple 

    

def Rdbms_Mapping(var_dict):
    # The schema for "Activity" in JSON is flexible schemal 
    # To map to Relational database - fixed schema 
    #Selecting the static part of JSON 
    #####"performed_at"
    #####"ticket_id"
    #####"performer_id"
    # For Flexible schema Activity , will look for the fields and if not available will be set to NULL 
    #####"activity": {shipping_address, shipment_date,status, agent_id }
    #print (var_dict)
    #for k,v in var_dict.items():
    #   print (k)
    
    v_performed_at =(var_dict["performed_at"])
    v_ticket_id = (var_dict["ticket_id"])
    v_performer_id = (var_dict["performer_id"])
    v_activity = (var_dict["activity"])
    
    # Check if Key exists first - As it is flexible schema , there is possibility that the 
    #required fields are not there in the  JSON 
    key1 = "shipping_address"
    key2= "shipment_date"
    key3="status"
    key4="agent_id"
    
    if key1 in v_activity.keys():
        v_activtiy_shipping_address=v_activity["shipping_address"]
    else:    
        v_activtiy_shipping_address="NULL"
    
    if key2 in v_activity.keys():
        v_activtiy_shipment_date=v_activity["shipment_date"]
    else:    
        v_activtiy_shipment_date="NULL"
    
    if key3 in v_activity.keys():
        v_activity_status=v_activity["status"]
    else:    
        v_activity_status="NULL"
    
    if key4 in v_activity.keys():
        v_activity_agent_id=v_activity["agent_id"]
    else:    
        v_activity_agent_id="NULL" 
    # Writing output to CSV     
    v_out =  str(v_performed_at)+","+str(v_ticket_id)+","+str(v_performer_id)+ "," + \
             str(v_activtiy_shipment_date) + "," + str(v_activity_status) + "," + str(v_activity_agent_id) +"\n"
    #print (v_out)

    with open ("structured_data.csv","a") as out_file:
        out_file.write(v_out)
        
    
    
  

def Main():
    v_args = GetArgs() 
    v_input_file_name=v_args.input_file_name
    #v_input_file_name="test_1000.json"
    # Clean up if run multiple times 
    if os.path.exists('structured_data.csv'):
        os.remove('structured_data.csv') #this deletes the file
    if os.path.isfile(v_input_file_name):
        v_tuple= Read_Json(v_input_file_name)
        for var_dict in v_tuple:
            #print (var_dict)
            Rdbms_Mapping(var_dict)
    else:
        print ("The input file doesn't exist in the current directory ")


    

# MAIN 
Main()
  
