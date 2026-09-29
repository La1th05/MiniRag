from .BaseController import BaseController
from .ProjectController import ProjectController
from models import ProcesssingEnum
from langchain_community.document_loaders import TextLoader, PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os



class ProcessController(BaseController):
    def __init__(self,project_id):
        super().__init__()
        
        self.project_id=project_id
        self.project_path=ProjectController().get_project_path(project_id=project_id)
        
    def  get_files_extention(self,file_id:str):
        return os.path.splitext(file_id)[-1]
    
    
    def get_file_loader(self,file_id:str,):
        file_ext=self.get_files_extention(file_id=file_id)
        
        file_path=os.path.join(
            self.project_path,
            file_id
        )
        
        if file_ext == ProcesssingEnum.PDF.value:
            return PyMuPDFLoader(file_path)
        if file_ext == ProcesssingEnum.TXT.value:
            return TextLoader(file_path,encoding="utf-8")
        else:
            return None
            
    def get_file_content(self,file_id:str):
        loader=self.get_file_loader(file_id=file_id)
        return loader.load() 
        
    def process_file_content(self,file_content:list,file_id:str,
                             chunk_size:int=100,overlap_size:int=20):
        text_splitter =RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=overlap_size,
            length_function=len,
        )
        
        file_content_texts =[
            record.page_content
            for record in file_content
        ]
        file_content_metadata = [
            record.metadata
            for record in file_content
        ]
        
        chuncks=text_splitter.create_documents(
            file_content_texts,
            metadatas=file_content_metadata
        )
        
        return chuncks
        