import pytest
from dotenv import load_dotenv
from unittest.mock import MagicMock, patch
from pymilvus import (connections, 
                      utility, 
                      Collection,
                      FieldSchema,
                      DataType,
                      CollectionSchema,
                      MilvusClient)
from src.milvus_client import milvus_initialization,milvus_insert_data
import os
import numpy as np

load_dotenv()

DB_COLLECTION_NAME = os.getenv('DB_COLLECTION_NAME')
MILVUS_PORT = os.getenv('MILVUS_PORT')
MILVUS_HOST = os.getenv('MILVUS_HOST')
MILVUS_URI = os.getenv('MILVUS_URI')



@pytest.fixture
def mock_milvus(mocker):

    '''Mock Milvus connections and collections'''

    mock_connect = mocker.patch("pymilvus.connections.connect",autospec=True)
    mock_has_connection = mocker.patch.object(connections, "has_connection",return_value = True)
    mock_has_connect = mocker.patch.object(connections, "connect",return_value = True)
    mock_has_collection = mocker.patch.object(utility, "has_collection",return_value = True)
    mock_collection = mocker.patch("pymilvus.Collection",autospec = True)
    mock_drop_collection = mocker.patch.object(utility,"drop_collection",return_value = True)
    mock_milvus_client = mocker.patch("src.milvus_client.milvus_initialization", autospec=True)
    mock_collection.return_value = MagicMock() 

    return {
        "mock_connect" : mock_connect,
        "mock_has_connection" : mock_has_connection,
        "mock_has_collection" : mock_has_collection,
        "mock_collection" : mock_collection,
        "mock_milvus_client":mock_milvus_client,
        "mock_drop_collection" : mock_drop_collection,
        "mock_milvus_connect" : mock_has_connect
    }


def test_milvus_initialization(mock_milvus):
    """Test milvus initialization"""
    global DB_COLLECTION_NAME,MILVUS_HOST,MILVUS_PORT

    collection = milvus_initialization(collection_name="test_collection",drop_collection=False)

    # mock_milvus['mock_has_connection'].assert_called_once_with('default')
    if not mock_milvus['mock_has_connection'].return_value:
        mock_milvus['mock_connect'].assert_called_once_with('default', host=MILVUS_HOST, port=MILVUS_PORT)
    mock_milvus['mock_has_collection'].assert_called_once_with("test_collection")
    

    assert collection is not None

def test_milvus_initalization_with_drop_collection(mock_milvus):
    global DB_COLLECTION_NAME,MILVUS_HOST,MILVUS_PORT
    collection = milvus_initialization(collection_name="test_collection",drop_collection=True)

    mock_milvus['mock_drop_collection'].assert_called_once_with(collection_name="test_collection")
    mock_milvus['mock_has_collection'].assert_called_once_with("test_collection")
    mock_milvus['mock_milvus_connect'].assert_called_once_with('default',host=os.getenv("MILVUS_HOST","localhost"),port=os.getenv("MILVUS_PORT","19530"))


    assert collection is not None


@pytest.fixture
def mock_milvus_insert(mocker):
    '''mock milvus insert and response'''
    mock_milvus_connection = mocker.patch("pymilvus.MilvusClient",autospec = True)
    mock_milvus_insert = mocker.patch.object(mock_milvus_connection,"insert",return_value= True)
    mock_has_connect = mocker.patch.object(connections, "connect",return_value = True)

    return {
        "mock_milvus_connection" : mock_milvus_connection,
        "mock_milvus_insert" : mock_milvus_insert,
        "mock_milvus_connect" : mock_has_connect

    }


def test_milvus_insert(mock_milvus_insert):

    '''mock insertion of quries and embedding insertion.'''
    float_list = np.random.rand(768)
    data = {
            "filename":"test file name",
            "text":"this is a test case doc.",
            "embeddings":float_list
        }
    insertion = milvus_insert_data(file_name= data['filename'],
                                   doc = data['text'],
                                   doc_embeding= data["embeddings"])
                                   
    mock_milvus_insert['mock_milvus_connect'].assert_called_once_with('default',host=os.getenv("MILVUS_HOST","localhost"),port=os.getenv("MILVUS_PORT","19530"))
    
    # mock_milvus_insert["mock_milvus_connection"].assert_called_once_with(uri= os.getenv("MILVUS_URI"),token = "root:Milvus")
    # mock_milvus_insert["mock_milvus_insert"].assert_called_once_with(collection_name=os.getenv("DB_COLLECTION_NAME"),
    #         data=[data])

    assert insertion is not None
    