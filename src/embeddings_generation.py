
from sentence_transformers import SentenceTransformer
from typing import Annotated
from langchain_text_splitters import RecursiveCharacterTextSplitter,CharacterTextSplitter
import re
import string
from utils.logger import Logger
# embeeding model function

_logger = Logger()

class Embedding_model:

    """embedding model to embed the text"""
    
    # _model_name = 'all-mpnet-base-v2'
    _model_name = "all-MiniLM-L6-v2"
    def __init__(self):
        if Embedding_model._model_name == None:
            self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.model = SentenceTransformer(self.__class__._model_name)
        return
    # function to embed a list of string.
    def embed_docs(self,docs : Annotated[list,"list of documents"]):
        embeded_docs = [self.model.encode(doc, batch_size=16, show_progress_bar=True) for doc in docs]
        return embeded_docs
    
    #function to embed only a single String or text.
    def embed_query(self,query : str):
        return self.model.encode(query)




def Text_splitter(text: Annotated[str,"The text that needs to be chunked."],
                  chunk_size : Annotated[int,"The size of each chunk."], 
                  chunk_overlap: Annotated[int,"the precent of chunk to overlap."] = 0.2):
    
    """ function to create the chunks for a longer text."""

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, 
        chunk_overlap=int(chunk_size * chunk_overlap),
        separators=["\n\n", "\n", " ", ""]
    )
    
    return text_splitter.split_text(text)
    

    
        



def create_embeddings(text_data : Annotated[str, "The Text Data of pdf from data folder"],
                      chunk_size : int = 512
                      ):
    """Create embeddings for the given text data."""

    _logger.log('initializing creating Embdding process... ','create_embedding')

    try:
    
        text_chunks = Text_splitter(text_data,chunk_size)
        _logger.info(f"Split text into {len(text_chunks)} chunks","create_embedding")
        embed_model = Embedding_model()
        print(text_chunks)
        embed_text__chunks = embed_model.embed_docs(text_chunks) 
        _logger.info(f"Generated Embedding for the model","create_embedding")
        return list(zip(text_chunks,embed_text__chunks))

    except Exception as e:
        _logger.error(f"error created while creating embeddings {e}","create_embeddings.py")
        return None

