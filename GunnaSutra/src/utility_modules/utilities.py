import os, sys
import yaml 
from datetime import datetime

class Config:
    def __init__(self, data:dict):
        for key, value in data.items():
            if isinstance(value, dict):
                setattr(self, key, Config(value))
            else:
                setattr(self, key, value)


class SetupConfig:
    def __init__(self, setup_config_location):
        self.setup_config_location=setup_config_location

    def get_configuration_data(self):
        with open(self.setup_config_location, "r") as fp:
            data=yaml.safe_load(fp)
            config_data=Config(data)
            return config_data
    
    # Below will not create heirarchy in key chain
    # def load_config_data(self, data):
    #     for key, value in data.items():
    #         if isinstance(value, dict):
    #             setattr(self, key, self.load_config_data(value)) # Recursively create nested objects
    #         else:
    #             setattr(self, key, value)


class Workspace:
    def __init__(self, workspace_directory, application_name:str="Gunnasutra", workspace_folder_name:str=datetime.now().strftime("%Y%m%d%H%M%S")):
        self.workspace_directory=workspace_directory
        self.application_name=application_name
        self.workspace_folder_name=workspace_folder_name
        self.workspace_location=None 
    
    def get_workspace_location(self):
        # check if workspace location provided
        if not self.workspace_directory:
            self.workspace_directory=os.path.expanduser("~/Documents")

        self.workspace_location=os.path.join(self.workspace_directory, self.application_name, self.workspace_folder_name)
        os.makedirs(self.workspace_location, exist_ok=True)
        return self.workspace_location
    
    def create_subfolders(self, subfolder_name):
        if not subfolder_name:
            subfolder_name="default"
        
        if os.path.exists(self.workspace_location, subfolder_name):
            orig_location=os.path.join(self.workspace_location, subfolder_name)
            new_location=os.path.join(self.workspace_directory, f"Backup_{subfolder_name}_{datetime.now().strftime('%Y%m%d%H%M%S')}")
            os.rename(orig_location, new_location)

        subfolder_location=os.path.join(self.workspace_location, subfolder_name)
        os.makedirs(subfolder_location)
        return subfolder_location
    

class FileLocator:
    def __init__(self, file_name:str, folder_location:str=None):
        self.file_name=file_name 
        self.folder_location=folder_location
        self.default_level=2

    def get_level_up_location(self, folder_location):
        new_location=folder_location
        for i in range(0, self.default_level):
            new_location=os.path.dirname(new_location)
        return new_location
    
    def get_system_location(self):
        if self.folder_location:
            return self.scan_folder_location(self.folder_location)
        
        # check in sys.executable folder 
        folder_location=os.path.dirname(sys.executable)
        folder_path=self.scan_folder_location(folder_location)
        if folder_path:
            return folder_path

        # check in current working directory folder 
        folder_location=os.path.dirname(os.path.abspath(__file__))
        folder_path=self.scan_folder_location(folder_location)
        if folder_path:
            return folder_path
        
        # check in sys.executable levels above
        root_location=sys.executable
        folder_location=self.get_level_up_location(root_location)
        folder_path=self.scan_folder_location(folder_location)
        if folder_path:
            return folder_path
        
        # finally check in current folder x levels up 
        root_location=os.path.dirname(os.path.abspath(__file__))
        folder_location=self.get_level_up_location(root_location)
        folder_path=self.scan_folder_location(folder_location)
        if folder_path:
            return folder_path

    def scan_folder_location(self, folder_location):
        return_location=None 

        if os.path.exists(os.path.join(folder_location, self.file_name)):
            return_location=os.path.join(folder_location, self.file_name)
            return return_location
        
        for root, dirs, files in os.walk(folder_location):
            if self.file_name in files: 
                return_location=os.path.join(root, self.file_name)
                return return_location                 
