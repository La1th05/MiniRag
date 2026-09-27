from .BaseController import BaseController
from .ProjectController import ProjectController
from fastapi import UploadFile
from models import ResponseSignal
import os
import re

class DataController(BaseController):
    def __init__(self):
        super().__init__()
        self.size_scale= 1048576
    def validate_uploaded_file(self,file:UploadFile):
        if file.content_type  not in self.app_settings.ALLOWED_DATATYPE:
            return False, ResponseSignal.FILE_TYPE_NOT_SUPPORTED.value

        if file.size > (self.app_settings.FILE_MAX_SIZE * self.size_scale):
            return False, ResponseSignal.FILE_SIZE_EXCEEDED.value
        
        return True, ResponseSignal.FILE_VALIDATED_SUCCESS.value
    
    
    def generate_new_file_name(self,org_file_name:str,project_path:str):
        random_file_name=self.generate_randome_string()
        project_path=project_path

        
        clean_file_name=self.get_clean_file_name(org_file_name=org_file_name)
        
        new_file_path=os.path.join(
            project_path,
            random_file_name+"_"+clean_file_name
        )
        
        while os.path.exists(new_file_path):
            random_file_name=self.generate_randome_string()
            new_file_path=os.path.join(
                        project_path,
                        random_file_name+"_"+clean_file_name
                    )
    
        return new_file_path
    
    def get_clean_file_name(self,org_file_name:str):
        
        clean_file_name=re.sub(r'[^\w. ]','',org_file_name.strip())
        
        clean_file_name=clean_file_name.replace(' ','_')
        
        return clean_file_name