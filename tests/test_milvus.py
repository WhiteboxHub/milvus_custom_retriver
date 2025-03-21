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
def test_milvus_initalization_with_drop_collection(mock_milvus):
    global DB_COLLECTION_NAME,MILVUS_HOST,MILVUS_PORT
    collection = milvus_initialization(collection_name="test_collection",drop_collection=True)
    mock_milvus['mock_drop_collection'].assert_called_once_with(collection_name="test_collection")
    mock_milvus['mock_has_collection'].assert_called_once_with("test_collection")
    mock_milvus['mock_milvus_connect'].assert_called_once_with('default',host=os.getenv("MILVUS_HOST","localhost"),port=os.getenv("MILVUS_PORT","19530"))


    assert collection is not None



def test_milvus_initialization(mock_milvus):
    """Test milvus initialization"""
    global DB_COLLECTION_NAME,MILVUS_HOST,MILVUS_PORT

    collection = milvus_initialization(collection_name="test_collection",drop_collection=False)

    # mock_milvus['mock_has_connection'].assert_called_once_with('default')
    if not mock_milvus['mock_has_connection'].return_value:
        mock_milvus['mock_connect'].assert_called_once_with('default', host=MILVUS_HOST, port=MILVUS_PORT)
    mock_milvus['mock_has_collection'].assert_called_once_with("test_collection")
    

    assert collection is not None



# @pytest.fixture
# def mock_milvus_insert(mocker):
#     """Mock Milvus insert operation"""

#     # Mock Milvus connection
#     mock_connect = mocker.patch.object(connections, "connect", return_value=None)
#     mock_list_connections = mocker.patch.object(connections, "list_connections", return_value=["default"])
#     mock_has_collection = mocker.patch.object(utility, "has_collection", return_value=True)

#     # Mock Collection object and insert function
#     mock_collection_instance = MagicMock()
#     mock_collection = mocker.patch("pymilvus.Collection", return_value=mock_collection_instance)
#     mock_collection_instance.insert.return_value = True  # Simulate a successful insert

#     return {
#         "mock_connect": mock_connect,
#         "mock_list_connections": mock_list_connections,
#         "mock_has_collection": mock_has_collection,
#         "mock_collection": mock_collection,
#         "mock_collection_instance": mock_collection_instance,
#     }

# def test_milvus_insert(mock_milvus_insert):
#     """Test inserting data into Milvus"""

#     float_list = np.random.rand(768)
#     data = {
#         "filename": "test_file_name",
#         "text": "This is a test case document.",
#         "embeddings": float_list,
#     }

#     insertion = milvus_insert_data(
#         file_name=data["filename"], doc=data["text"], doc_embeding=data["embeddings"]
#     )

#     # Ensure the connection was established
#     mock_milvus_insert["mock_connect"].assert_called_once_with(
#         "default", host=os.getenv("MILVUS_HOST", "localhost"), port=os.getenv("MILVUS_PORT", "19530")
#     )

#     mock_milvus_insert["mock_has_connection"].assert_called_once_with("default")

#     # Ensure the collection was checked
#     mock_milvus_insert["mock_has_collection"].assert_called_once_with(os.getenv("DB_COLLECTION_NAME"))

#     # Ensure the insert function was called correctly
#     mock_milvus_insert["mock_collection_instance"].insert.assert_called_once()

#     assert insertion is True



@pytest.fixture
def mock_logger():
    """Mock the logger"""
    pass
    # with patch("pymilvus.logger.Logger") as mock_logger:
    #     yield mock_logger()

@pytest.fixture
def mock_milvus1():
    """Mock Milvus connections and collection"""
    with patch("pymilvus.connections") as mock_connections, \
         patch("pymilvus.Collection") as mock_collection, \
         patch("pymilvus.utility") as mock_utility:
        
        # Mock connection status
        mock_connections.has_connection.return_value = True
        mock_connections.connect.return_value = None
        
        # Mock utility function
        mock_utility.has_collection.return_value = True
        
        # Mock collection and insert method
        mock_collection_instance = MagicMock()
        mock_collection.return_value = mock_collection_instance
        mock_collection_instance.insert.return_value = {"status": "success"}

        yield mock_connections, mock_collection, mock_utility, mock_collection_instance

@patch.dict(os.environ, {"DB_COLLECTION_NAME": "test_collection"})
def test_milvus_insert_success(mock_logger, mock_milvus1):
    """Test successful data insertion"""
    mock_connections, mock_collection, mock_utility, mock_collection_instance = mock_milvus1
    file_name = "test_file.txt"
    doc = "This is a test document."
    doc_embedding = np.random.rand(768)
    

    result = milvus_insert_data(file_name, doc, doc_embedding)
    print(result,'-'*200)
    collection_name = os.getenv('DB_COLLECTION_NAME')
    mock_collection_instance.insert.assert_called_once()
    mock_collection.assert_called_with(collection_name)
    mock_connections.connect.assert_called_once()
    # mock_logger.log.assert_called_with("inserted in to the collection", "milvus_insert")

    assert result == {"status": "success"}

@patch.dict(os.environ, {}, clear=True)
def test_milvus_insert_missing_collection_name(mock_logger, mock_milvus1):
    """Test missing collection name in environment variables"""
    file_name = "test_file.txt"
    doc = "This is a test document."
    doc_embedding = np.random.rand(768)

    with pytest.raises(ValueError, match="DB_COLLECTION_NAME is not set in environment variables."):
        milvus_insert_data(file_name, doc, doc_embedding)

    # mock_logger.error.assert_called()

@patch.dict(os.environ, {"DB_COLLECTION_NAME": "test_collection"})
def test_milvus_insert_no_connection(mock_logger, mock_milvus1):
    """Test when Milvus connection fails"""
    with patch("pymilvus.connections") as mock_connections:
        # Ensure that after connecting, `has_connection` is still False
        mock_connections.has_connection.side_effect = [False, False]  # First before connect, then after connect
        
        file_name = "test_file.txt"
        doc = "This is a test document."
        doc_embedding = np.random.rand(768)

        with pytest.raises(RuntimeError, match="connection error occured on run time"):
            milvus_insert_data(file_name, doc, doc_embedding)

        # Ensure the function called `connect`
        mock_connections.connect.assert_called_once()
    # mock_logger.error.assert_called()

@patch.dict(os.environ, {"DB_COLLECTION_NAME": "test_collection"})
def test_milvus_insert_exception_handling(mock_logger, mock_milvus1):
    """Test that exceptions are logged and raised"""
    _, mock_collection, _, _ = mock_milvus1
    mock_collection.side_effect = Exception("Collection error")

    file_name = "test_file.txt"
    doc = "This is a test document."
    doc_embedding = np.random.rand(768)

    with pytest.raises(Exception, match="Collection error"):
        milvus_insert_data(file_name, doc, doc_embedding)

    # mock_logger.error.assert_called()
