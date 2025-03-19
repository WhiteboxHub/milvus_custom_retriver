import pytest
from dotenv import load_dotenv
from unittest.mock import MagicMock, patch
from pymilvus import (connections, 
                      utility, 
                      Collection
                      ,FieldSchema,
                      DataType,
                      CollectionSchema,
                      MilvusClient)
from src.milvus_client import milvus_initialization,milvus_insert_data
import os


load_dotenv()

DB_COLLECTION_NAME = os.getenv('DB_COLLECTION_NAME')
MILVUS_PORT = os.getenv('MILVUS_PORT')
MILVUS_HOST = os.getenv('MILVUS_HOST')
MILVUS_URI = os.getenv('MILVUS_URI')



@pytest.fixture
def mock_milvus(mocker):
    '''Mock Milvus connections and collections'''

    mock_connect = mocker.patch("pymilvus.connections.connect")
    mock_client = mocker.patch(MilvusClient,autospec=True,return_value = True)
    mock_has_connection = mocker.patch.object(connections, "has_connection",return_value = True)
    mock_has_collection = mocker.patch.object(utility, "has_collection",return_value = True)
    mock_collection = mocker.patch("pymilvus.Collection",autospec = True)
    mock_collection.return_value = MagicMock() 
    return {
        "milvus_client" : mock_client,
        "mock_connect" : mock_connect,
        "mock_has_connection" : mock_has_connection,
        "mock_has_collection" : mock_has_collection,
        "mock_collection" : mock_collection
    }


def test_milvus_initialization(mock_milvus):
    """Test milvus initialization"""
    global DB_COLLECTION_NAME,MILVUS_HOST,MILVUS_PORT

    collection = milvus_initialization(collection_name="test_collection")

    mock_milvus['mock_connect'].assert_called_once_with('default',host=MILVUS_HOST,port=MILVUS_PORT)
    mock_milvus["milvus_client"].assert_called_once_with(uri=os.getenv("MILVUS_URI"),token="root:Milvus")
    mock_milvus['mock_has_connection'].assert_called_once_with('default')
    # mock_milvus['mock_has_collection'].assert_called_once_with('test_collection')
    mock_milvus["milvus_client"].assert_called_once_with(uri=os.getenv("MILVUS_URI"),token="root:Milvus").load_collection(collection_name="test_collection")

    assert collection is not None