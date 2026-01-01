from .BaseController import BaseController
from .ProjectController import ProjectController
from ..models import FileTypes
import os
from langchain_community.document_loaders import TextLoader, PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from ..schemas import ProcessArgs


class ProcessController(BaseController):

    def __init__(self, project_id : str):
        super().__init__()

        self.projects_id = project_id
        self.project_path = ProjectController().get_project_path(project_id=project_id)

    def get_file_extension(self, file_id: str):
        return os.path.splitext(file_id)[-1]
    

    def get_file_loader(self, file_id: str):
        file_ext = self.get_file_extension(file_id)
        file_path = os.path.join(self.project_path, file_id)
        if file_ext == FileTypes.TXT.value:
            return TextLoader(file_path, encoding='utf-8')

        elif file_ext == FileTypes.PDF.value:
            return PyMuPDFLoader(file_path)
        

        return None
    
    def get_file_content(self, file_id):
        loader = self.get_file_loader(file_id)
        return loader.load()
    

    def process_file_content(self, processArgs: ProcessArgs):
        file_content = self.get_file_content(processArgs.file_id)
        # print(file_content)
        file_content_texts = [rec.page_content.replace('\n', ' ') for rec in file_content]
        file_content_metadata = [rec.metadata for rec in file_content]
        print(file_content_texts)

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=processArgs.chunk_size, chunk_overlap =processArgs.overlap_size, length_function=len)
        chunks = text_splitter.create_documents(texts=file_content_texts, metadatas=file_content_metadata)
    
        return chunks
        