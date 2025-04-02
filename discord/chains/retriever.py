# app/chains/retriever.py
import os

from langchain.retrievers.parent_document_retriever import ParentDocumentRetriever
from langchain.storage import LocalFileStore # Import the local file storage module
from langchain.storage._lc_store import create_kv_docstore # Import the function to create a key-value document store

from chains.modules.embeddings import CLIPEmbeddings
from chains.modules.splitter import ProductDocumentSplitter
from chains.modules.vectorstore import MultiModalChroma # Import the vector store module

print(f"6. importing /discord/chains/retriever.py)")

def load_retriever(persist_directory, docstore_path):
    """
    Load and initialize the document retriever.

    Args:
        persist_directory (str): The directory where the vector store is persisted.
        docstore_path (str): The path to the document store.

    Returns:
        ParentDocumentRetriever: An instance of the document retriever.
    """
    # Check if the persist directory exists
    if not os.path.exists(persist_directory):
        print(f"Persist directory does not exist: {persist_directory}")
    else:
        print(f"Persist directory exists: {persist_directory}")

    # Initialize the vector store with the specified collection name, embedding function, and persist directory
    
    child_splitter = ProductDocumentSplitter()
    vectorstore = MultiModalChroma(
        collection_name="full_documents",
        embedding_function=CLIPEmbeddings(),
        persist_directory=persist_directory,
    )

    print(f"6. (from /discord/chains/retriever.py): Loading retriever with docstore_path: {docstore_path}")
    print(f"6. (from /discord/chains/retriever.py): Loading retriever with persist_directory): {persist_directory}")

    fs = LocalFileStore(docstore_path) # Create a local file store
    store = create_kv_docstore(fs) # Create a key-value document store using the file store

    # Initialize the document retriever with the vector store, document store, and document splitter
    return ParentDocumentRetriever(
        vectorstore=vectorstore,
        docstore=store,
        child_splitter=child_splitter,
        search_kwargs={"k": 10},
    )
