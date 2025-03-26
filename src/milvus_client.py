from pymilvus import (connections,
                      utility,
                      FieldSchema,
                      CollectionSchema,
                      DataType,
                      Collection,
                      MilvusClient)

from dotenv import load_dotenv
import os
from typing import Annotated
from src.utils import logger
import threading
from src.embeddings_generation import Embedding_model

load_dotenv()
_mivus_thread = threading.Lock()



class Milvus_init:
    def __init__(self):
        self.COLLECTION_NAME = os.getenv("DB_COLLECTION_NAME")
        self.MILVUS_DB_ALIAS = os.getenv('MILVUS_DB_Alias')
        self.MILVUS_HOST = os.getenv("MILVUS_HOST","localhost")
        self.MILVUS_PORT = os.getenv("MILVUS_PORT","19530")
        self.logger = logger.Logger()
        self.MILVUS_URI = os.getenv("MILVUS_URI")
        self.MILVUS_TOKEN = os.getenv('MILVUS_TOKEN')
        self.CLIENT = MilvusClient(
                    uri= self.MILVUS_URI,
                    token = self.MILVUS_TOKEN
                )

    def initialize_collection(self,Drop_collection = False):
        with _mivus_thread:
            try:
                self.logger.log("establising a MILVUS Connection","initilize_collection")
                
                if Drop_collection or self.COLLECTION_NAME not in self.CLIENT.list_collections() :
                    self.CLIENT.drop_collection(
                        collection_name=self.COLLECTION_NAME
                    )
                    db_schema = MilvusClient.create_schema(
                        auto_id = False
                    )

                    db_schema.add_field(field_name='pk', datatype=DataType.INT64, is_primary=True, auto_id= True)
                    db_schema.add_field(field_name='filename', datatype=DataType.VARCHAR,max_length = 500)
                    db_schema.add_field(field_name='embeddings', datatype=DataType.FLOAT_VECTOR,dim=384)
                    db_schema.add_field(field_name='text', datatype=DataType.VARCHAR , max_length = 800)

                    index_params = self.CLIENT.prepare_index_params()
                    index_params.add_index(
                        field_name="embeddings",
                        index_type="AUTOINDEX",
                        metric_type = "COSINE"
                    )


                    self.CLIENT.create_collection(
                        collection_name=self.COLLECTION_NAME,
                        schema = db_schema,
                        index_params=index_params
                    )
                    self.logger.log(f"create a collection {self.COLLECTION_NAME} with schema and index_params","initilize_collection")

                    res = self.CLIENT.get_load_state(
                        collection_name=self.COLLECTION_NAME
                    )

                    return "Collection ceated successfully"
                

                self.logger.log(f'milvusdb collection {self.COLLECTION_NAME} already exists','milvus_init')
                
                return f"{self.COLLECTION_NAME} Collection already Exists. please drop the collection and try again."
            except Exception as e:
                self.logger.error(f"error while checking milvus connection {e}","milvus_init")
                return None
    def Client_connection(self):
        with _mivus_thread:
            try:
                self.logger.log("Milvus client connection Request","Client_connection")
                return self.CLIENT
            except Exception as e:
                self.logger.error(f"error while checking milvus connection {e}","Client_connection")
                return None
            
    def milvus_insert_data_corpus(self,corpus_data : list):
        
        try:

            if self.COLLECTION_NAME not in self.CLIENT.list_collections():
                self.logger.log(f'milvusdb collection {self.COLLECTION_NAME} does not exists','milvus_insert_data_courps')
                raise Exception
            

            i_data = [{"filename":filename,"embeddings":embeding,"text":text} for filename, embeding, text in corpus_data]

            res = self.CLIENT.insert(
                collection_name = self.COLLECTION_NAME,
                data = i_data
            )
            return "data inserted successfully "
            
        except Exception as e:
            self.logger.error(f"error while inserting milvus data {e}","milvus_insert_data_courps")
            raise e
    

    def milvus_similarity_search(   self,
                                    query : Annotated[int,"The user query to search"],
                                    search_column : Annotated[int,"The user query to search"] = 'embeddings',
                                    collection : Annotated[str, "The db collection to search into."] = None ,
                                    k  : Annotated[int, "The number of search results you want. "] = 5,
                                    query_search_params : Annotated[dict,"The search metrics you want to use for search."] = None,
                                    output_field : Annotated[list,"The list of columns for results output."] = ['text','filename']
                                    ):
        
        try:
            self.logger.log(f"doing similarity search milvus data.","milvus_similarity_search")

            if not collection:
                collection = self.COLLECTION_NAME
            
            search_params = dict()

            if not k:
                k = 5

            

            if search_params:
                search_params['serach_params'] = search_params

            embed_model = Embedding_model()
            query_embeding = embed_model.embed_query(query)
            search_params['collection_name'] = collection
            search_params['output_fields'] = output_field
            search_params['data'] = [query_embeding]
            search_params['anns_field'] = search_column
            search_params['limit'] = k

            search_result = self.CLIENT.search(**search_params)
            
            return search_result



            
        except Exception as e:
            self.logger.error(f"error while doing similarity serach milvus data {e}","milvus_similarity_search")
            return None

    

