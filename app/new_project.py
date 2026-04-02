import json
from pathlib import Path
from deepdiff import DeepDiff
import re


finalReport= {}

def load_file ():

    compareList = []

    new_list = []

    # print ("I hate you") # ---
    p = Path('.')
    for x in p.glob('**/*.json'):
        # print(x) # ---
        try:
            with open(str(x), 'r') as file:
                data = json.load(file)
                # print(data) # ---
                if isinstance(data, list):
                    compareList.append(data)
                    # print(compareList)
                elif isinstance(data, dict):
                    small = []
                    small.append(data)
                    # print("Small", small)
                    compareList.append(small)
                    # print("Comparison List",compareList)
                else:
                    compareList.clear()
                    print("JSON file must be a list of resources or contain a dictionary")
                    break
                  
        except:
            print("Error: No JSON file found....!")
            break


    # LOGIC 2: Attempt to flatten the nested dictionaries
    final_list = []
    for resource_list in compareList: # Loop through the list of resources
        for resource_item in resource_list: # Loop through the resource's content
            for resourcekey, resource_value in resource_item.items(): # Unpack it's dictionary content 
                if isinstance(resource_value, list): # Check if it's main content is a list
                    # print("Resource Value",resource_value)
                    for content in resource_value: # Remove each dictionary
                        # final_list.append(content)
                    # print("Final List",final_list)

                        # Loop through the dictionary to flatten it
                        
                        # First create a flatening dictionary container
                        flat_dict = {}

                        for content_key, content_value in content.items(): # While looping through the dictionary by it's Keys
                            if isinstance(content_value, dict): # Check if the value of the key is a dictionary
                                # If yes
                                # Loop through the keys of the Value dictionary
                                for value_key, value_value in content_value.items():

                                    flat_dict.update({str(content_key) + "." + str(value_key):value_value})
                                    # print("Flattened Dictionary", flat_dict)
                            else:
                                flat_dict.update({str(content_key):content_value})
                        
                        final_list.append(content)
                        # print("FINAL LIST", final_list)

    # Matching Logic
    changeLog = []
    
    # 1 MISSING
    if len(final_list[0]) != len(final_list[1]):
        finalReport.update({"CloudResourceItem": compareList[0][0]})
        finalReport.update({"IacResourceItem": compareList[1][0]})
        # Logic to loop through the list of resources and compare their key-pairs
        finalReport.update({"State": "Missing"})
        # Append te actual change into the changelog list
        changeLog.append(actual_Change)
        finalReport.update({"ChangeLog": changeLog})
        # print("REPORT",finalReport)
        # Include a return statement
        return finalReport
    
    else:
        ddiff = DeepDiff(final_list[0], final_list[1], ignore_order=True)
        # print("DIFFERENCE", ddiff) 
        # 2 MATCH
        if len(ddiff) == 0:
            finalReport.update({"CloudResourceItem": compareList[0][0]})
            finalReport.update({"IacResourceItem": compareList[1][0]})
            # Logic to loop through the list of resources and compare their key-pairs
            finalReport.update({"State": "Match"})
            # Append te actual change into the changelog list
            changeLog.append(actual_Change)
            finalReport.update({"ChangeLog": changeLog})
            # print("REPORT",finalReport)
            # Include a return statement
            return finalReport
        else:
            # 3 MODIFIED
            # First flatten the dicionaries by looping through the list of dictionaries
            finalReport.update({"CloudResourceItem": compareList[0][0]})
            finalReport.update({"IacResourceItem": compareList[1][0]})
            # Logic to loop through the list of resources and compare their key-pairs
            finalReport.update({"State": "Modified"})
            # Loop through the difference object
            for key, value in ddiff.items():
                if isinstance(value, dict):
                    for more_key, more_value in value.items():
                        more = re.findall(r"'([^']+)'", more_key)
                        m_more = ".".join(more)
                        # print(m_more)
                        actual_Change = {}
                        actual_Change.update({"KeyName":m_more, "CloudValue":more_value['old_value'], "IacValue": more_value['new_value']})
                        changeLog.append(actual_Change)
     
            finalReport.update({"ChangeLog": changeLog})
            # print("REPORT",finalReport)
            # Include a return statement
            return finalReport



  


# Fynction call
load_file()