from pymilvus import (connections,
                      utility,
                      FieldSchema,
                      CollectionSchema,
                      DataType,
                      Collection,
                      MilvusClient)

from dotenv import load_dotenv
import os
from utils import logger
import threading
from langchain_milvus import Milvus


load_dotenv()
_mivus_thread = threading.Lock()
_milvus_connection = None
_milvus_collection = None


def milvus_initialization(collection_name = None,drop_collection = False):
    global _milvus_connection,_milvus_collection

    with _mivus_thread:
        loggers = logger.Logger()

        if collection_name is None:
            collection_name = os.getenv('DB_COLLECTION_NAME')
            if not collection_name:
                loggers.error("unable to find collection_name from env varible ","milvus_init")
                raise ValueError("collection name not found in env variables...")
            


        if _milvus_connection:
            try:
                if connections.has_connection("default"):
                    loggers.log("connection already exists and working ","milvus_init")
                    return _milvus_collection
            except Exception as e:
                loggers.error(f"error while checking milvus connection {e}","milvus_init")

        try:

            connections.connect('default',host=os.getenv("MILVUS_HOST","localhost"),port=os.getenv("MILVUS_PORT","19530"))
            _milvus_connection = True
            loggers.log("new milvus connection extablished  ","milvus_init")
        except Exception as e:
            loggers.error(f"error while checking milvus connection {e}","milvus_init")

        if drop_collection:
            try:
                utility.drop_collection(collection_name)
                loggers.log('Deleting the collection.','milvus_init')
            except Exception as e:
                loggers.log(f'unable to delete the collection {e}','milvus_init')
    


        fields = [
            FieldSchema(name='pk', dtype=DataType.INT64, is_primary=True, auto_id= True),
            FieldSchema(name='filename', dtype=DataType.VARCHAR,max_length = 500),
            FieldSchema(name='embeddings', dtype=DataType.FLOAT_VECTOR,dim=768),
            FieldSchema(name='text', dtype=DataType.VARCHAR , max_length = 500), 
        ]


        schema = CollectionSchema(fields,"Machine learning")

        try:
            if utility.has_collection(collection_name):
                _milvus_collection = Collection(collection_name)
                loggers.log(f'milvusdb collection {collection_name} retrived','milvus_init')
                return _milvus_collection
            else:
                _milvus_collection = Collection(collection_name,schema)
                loggers.log(f'milvusdb collection {collection_name} created and retrived','milvus_init')
                return _milvus_collection
        except Exception as e:
                loggers.error(f'milvus db get collection error  {e}','milvus_init')
                return None
            
        
        

# milvus_initialization(drop_collection=True)
# print(milvus_initialization())
def milvus_insert_data(file_name : str,doc : str, doc_embeding):
    logs = logger.Logger()
    try:
        client = MilvusClient(
            uri= os.getenv("MILVUS_URI"),
            token = "root:Milvus"
        )

        data = [{
            "filename":file_name,
            "text":doc,
            "embeddings":doc_embeding
        }]

        res = client.insert(
            collection_name=os.getenv("DB_COLLECTION_NAME"),
            data=data
        )
        logs.log("inserted in to the collection","milvus_insert")
        return res 
    except Exception as e:
        logs.error(f"error occured while instering {e}","milvus_insert")




   
