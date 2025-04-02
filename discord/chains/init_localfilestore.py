import os
import json
from dotenv import load_dotenv
from langchain.storage import LocalFileStore
from langchain_core.stores import InMemoryStore
from langchain.retrievers.parent_document_retriever import ParentDocumentRetriever
from langchain.storage import LocalFileStore
from langchain.storage._lc_store import create_kv_docstore
from modules.vectorstore import MultiModalChroma
from modules.embeddings import CLIPEmbeddings
from modules.splitter import ProductDocumentSplitter


# Load environment variables from .env file
load_dotenv()

# Read the DOCSTORE_PATH from the environment variables
docstore_path = os.getenv("DOC_STORE_PATH")

print(f"DOC_STORE_PATH: {docstore_path}")

if not docstore_path:
    raise ValueError("DOC_STORE_PATH is not set in the .env file")

# Initialize the LocalFileStore
local_file_store = LocalFileStore(docstore_path)

# Basic tests
def test_local_file_store_initialization():
    assert local_file_store is not None, "LocalFileStore initialization failed"
    # Assuming LocalFileStore has a method or property to get the path
    #assert local_file_store.get_path() == docstore_path, "LocalFileStore path mismatch"

def test_key_value_store():
    #keys = local_file_store.keys()
    # Iterate over keys
    # Get the number of keys (files) in the store
    keys = list(local_file_store.yield_keys())
    num_keys = len(list(local_file_store.yield_keys()))

    print(f"Number of key-value pairs: {num_keys}")
    if num_keys > 0:
        print(f"Example key-value pair: {keys[0]} -> {local_file_store.mget(keys[1])}")
        print(f"Example key: {keys[0]}")

def show_all_key_value_pairs():
    # Iterate over keys
    # Get the number of keys (files) in the store
    keys = list(local_file_store.yield_keys())
    i = 0  
    if keys:
        for key in keys:
            value = local_file_store.mget(key)
            print(f"{i} Key: {key}, Value: {value}")
            i += 1

def test_load_retriever():

    persist_directory = '/Users/markobriesemann/Desktop/Machine_Learning/Project/1_UPSAIL/Github_Marko/upsailai-demo/discord/data/chroma_db'
    docstore_path = '/Users/markobriesemann/Desktop/Machine_Learning/Project/1_UPSAIL/Github_Marko/upsailai-demo/discord/data/doc_store'

    print(f"Persist directory: {persist_directory}")
    print(f"Docstore path: {docstore_path}"  )
    # This text splitter is used to create the child documents
    child_splitter = ProductDocumentSplitter()
    # The vectorstore to use to index the child chunks
    vectorstore = MultiModalChroma(
        collection_name="full_documents",
        embedding_function=CLIPEmbeddings(),
        persist_directory=persist_directory,
    )

    # The storage layer for the parent documents
    fs = LocalFileStore(docstore_path)
    store = create_kv_docstore(fs)

    retriever = ParentDocumentRetriever(
        vectorstore=vectorstore,
        docstore=store,
        child_splitter=child_splitter,
    )

    retrieved_docs = retriever.invoke("white shirt")
    #print(f" retrieved content:  {retrieved_docs} ")
    #print(f" retrieved content:  {retrieved_docs["descriptions"]} ")

    #print(f"Number of retrieved documents: {len(retrieved_docs[0].page_content)}")
    # Print results
    #for doc in retrieved_docs:
    #    print(doc.page_content)

    for doc in retrieved_docs:
    # Assuming page_content is a JSON string, parse it into a dictionary
        page_content = json.loads(doc.page_content)

        # Access the "weather" element
        weather = page_content.get("weather", [])
        print("Weather information:")
        for weather_info in weather:
            print(f"Season: {weather_info['name']}")
            print(f"Description: {weather_info['description']}")
            print()
    

def run_tests():
    #show_all_key_value_pairs()
    print("Running tests...")
    test_local_file_store_initialization()
    test_key_value_store()
    test_load_retriever()
    print("All tests passed!")

if __name__ == "__main__":
    run_tests()
