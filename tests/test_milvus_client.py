import pytest
from src.milvus_client import Milvus_init
from dotenv import load_dotenv
import os
from src.utils.logger import Logger
from unittest.mock import MagicMock, patch
from pymilvus import (MilvusClient)

load_dotenv()


COLLECTION_NAME = os.getenv("DB_COLLECTION_NAME")
MILVUS_DB_ALIAS = os.getenv('MILVUS_DB_Alias')
MILVUS_HOST = os.getenv("MILVUS_HOST","localhost")
MILVUS_PORT = os.getenv("MILVUS_PORT","19530")
logger = Logger()
MILVUS_URI = os.getenv("MILVUS_URI")
MILVUS_TOKEN = os.getenv('MILVUS_TOKEN')
milvus = Milvus_init()



@pytest.fixture
def mock_milvus_client(mocker):
    """Fixture to mock MilvusClient"""
    mock_client = MagicMock()
    mock_client.list_collections.return_value = []
    mock_client.insert.return_value = "data inserted successfully"
    mock_client.search.return_value = [{"filename": "file1.txt", "text": "sample text"}]
    mock_client.get_load_state.return_value = "loaded"
    mock_client.drop_collection.return_value = None
    # mocker.patch("pymilvus.MilvusClient", return_value=mock_client)  # Replace 'your_module' with actual module
    # mocker.patch("src.milvus_client.Milvus_init.CLIENT", new=mock_client)  # Replace 'your_module' with actual module
    return mock_client

@pytest.fixture
def milvus_instance(mock_milvus_client):
    """Fixture to initialize Milvus_init with mocked client"""
    with patch("pymilvus.MilvusClient", return_value=mock_milvus_client):  # Patch before instance creation
        return Milvus_init()

def test_initialize_collection(milvus_instance, mock_milvus_client):
    """Test collection initialization"""
    mock_milvus_client.list_collections.return_value = []
    
    response = milvus_instance.initialize_collection(Drop_collection=True)
    
    mock_milvus_client.drop_collection.assert_called_once_with(collection_name=COLLECTION_NAME)
    assert response == "Collection ceated successfully"
# @pytest.fixture()
# def mock_milvus_client(mocker):

#     mock_MilvusClient = mocker.patch("pymilvus.MilvusClient",autospec = True)

#     mock_MilvusClient_instance = mock_MilvusClient.return_value

#     # mock_list_collection = mock_MilvusClient_instance.list_collections()

#     # mock_drop_collection = mock_MilvusClient_instance.drop_collection()

#     # mock_create_schema = mock_MilvusClient_instance.create_schema()
    
#     # mock_create_schema_instance = mock_create_schema.return_value

#     # mock_create_schema_instance_addField = mock_create_schema_instance.add_field()

#     mock_MilvusClient_instance.drop_collection = MagicMock()
#     # mock_MilvusClient_instance.list_collections = MagicMock()

#     return {
#         "mock_MilvusClient" : mock_MilvusClient,
#         # "mock_list_collection" : mock_list_collection,
#         "mock_MilvusClient_instance" : mock_MilvusClient_instance
#     }


# def test_milvus_initialization(mock_milvus_client):

    

#     collection_initialization = milvus.initialize_collection(Drop_collection=True) 
#     # mock_milvus_client['mock_MilvusClient'].assert_called_once_with( uri = MILVUS_URI,
#     #                                                                   token = MILVUS_TOKEN)
#     mock_milvus_client['mock_MilvusClient_instance'].drop_collection.assert_called_once()


#     assert collection_initialization is not None