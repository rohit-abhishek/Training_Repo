import os, sys
import yaml 
from datetime import datetime

class Config:
    def __init__(self, data):
        for key, value in data.items():
            if isinstance(value, dict):
                setattr(self, key, Config(value)) # Recursively create nested objects
            else:
                setattr(self, key, value)


def get_system_location(file_name:str, folder_location:str=None) -> str:
    """ scan system path for required file name """

    return_location=None 

    # If folder location present 
    if folder_location:
        if os.path.exists(os.path.join(folder_location, file_name)):
            return_location=os.path.join(folder_location, file_name)
            return return_location
        
        for root, dirs, files in os.walk(folder_location):
            if file_name in files: 
                return_location=os.path.join(root, file_name)
                return return_location 

    # If folder location not present
    elif os.path.exists(os.path.join(os.path.dirname(sys.executable), file_name)):
        return_location=os.path.join(os.path.dirname(sys.executable), file_name) 
        return return_location
        
    elif os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)):
        return_location=os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)
        return return_location
        
    else:
        root=os.path.dirname(os.path.abspath(__file__))
        root_path=get_level_up_location(root, level=2)
        # root_path=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        for root, dirs, files in os.walk(root_path):
            if file_name in files: 
                return_location=os.path.join(root, file_name)
                return return_location 

        # still not found then scan through sys.executable location 
        root=sys.executable
        root_path=get_level_up_location(root, level=2)
        # root_path=os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(sys.executable))))
        for root, dirs, files in os.walk(root_path):
            if file_name in files: 
                return_location=os.path.join(root, file_name)
                return return_location
    
    return return_location 


def get_level_up_location(location, level=2):
    new_location=location
    for i in range(0, level):
        new_location=os.path.dirname(new_location)

    return new_location

def get_setup_configuration(configuration_location):
    # load the setup_configuration.yaml 
    setup_config=None 
    with open(configuration_location, "r") as fp:
        data=yaml.safe_load(fp)
        setup_config=Config(data)
    return setup_config


def create_workspace(workspace_location, application_name):
    """ create workspace """

    current_timestamp=datetime.now().strftime("%Y%m%d%H%M%S")
    workspace_= None 

    # if workspace provided then create directories and send the location 
    if workspace_location and workspace_location!="":
        if not os.path.exists(workspace_location):
            workspace_=os.path.join(workspace_location, application_name, current_timestamp)
            os.makedirs(workspace_)
            return workspace_
    
    root=os.path.expanduser("~/Documents")
    workspace_location=os.path.join(root, application_name, current_timestamp)
    os.makedirs(workspace_location)
    return workspace_location