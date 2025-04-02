import streamlit as st
import os
import json
from dotenv import load_dotenv
from langchain.storage import LocalFileStore
from langchain.retrievers.parent_document_retriever import ParentDocumentRetriever
from langchain.storage._lc_store import create_kv_docstore
from chains.modules.vectorstore import MultiModalChroma
from chains.modules.embeddings import CLIPEmbeddings
from chains.modules.splitter import ProductDocumentSplitter
from PIL import Image
from io import BytesIO
import base64
import umap.umap_ as umap       # Correct import for umap-learn # UMAP for dimensionality reduction
import numpy as np              # NumPy for numerical computing
import plotly.express as px     # Plotly Express for interactive plots
import pandas as pd             # Pandas for data manipulation
import time
from tqdm import tqdm        # tqdm for progress bars




# Load environment variables from .env file
load_dotenv()

# Function to decode base64 image
def decode_base64_image(encoded_str):
    decoded_bytes = base64.b64decode(encoded_str)
    return Image.open(BytesIO(decoded_bytes))

# Read the DOCSTORE_PATH and PERSIST_DIR from the environment variables
docstore_path = os.getenv("DOC_STORE_PATH")
persist_directory = os.getenv("DB_PATH")

if not docstore_path or not persist_directory:
    st.error("DOC_STORE_PATH or PERSIST_DIR is not set in the .env file")
    st.stop()

# Initialize the LocalFileStore
local_file_store = LocalFileStore(docstore_path)

# Initialize the embedding function
embedding_function = CLIPEmbeddings()


# Initialize the vector store
vectorstore = MultiModalChroma(
    collection_name="full_documents",
    embedding_function=CLIPEmbeddings(),
    persist_directory=persist_directory,
)

# Initialize the document retriever
child_splitter = ProductDocumentSplitter()
retriever = ParentDocumentRetriever(
    vectorstore=vectorstore,
    docstore=create_kv_docstore(local_file_store),
    child_splitter=child_splitter,
    search_kwargs={"k": 10},
)

# Retrieve all embeddings and metadata from ChromaDB
def get_all_embeddings(chroma_instance):
    st.write("get_all_embeddings")
    
    start_time = time.time()
    results = chroma_instance._collection.get(include=["embeddings","metadatas"])
    #st.write("Raw results from ChromaDB:", results)  # Debugging: Full response
    
    embeddings = np.array(results["embeddings"])  # Extract embeddings
    metadatas = results.get("metadatas", [])  # Extract metadata (optional)

    #st.write("Extracted Embeddings (NumPy Array):", embeddings)  # Debugging
    #st.write("Extracted Metadata:", metadatas)  # Debugging
    end_time = time.time()
    elapsed_time = end_time - start_time
    st.write(f"get_all_embeddings finished {elapsed_time:.2f} seconds")
    return embeddings, metadatas

def get_query_doc_meta_dist(chroma_instance, query, k=5, filter=None):
    st.write("get_query_doc_meta_dist")
    st.write("query: ", query)
    st.write("chroma_instance: ", chroma_instance)
    # asimilarity_search_with_score
    # Run similarity search
    results = vectorstore.similarity_search_with_score(
        query=query, 
        k=k, 
        filter=filter
    )

    # Display results
    for document, score in results:
        st.write(f"Document: {document.page_content}")
        st.write(f"Cosine Similarity Score: {score:.4f}")
        st.write("-----")

    #metadatas, cs_score = vectorstore.similarity_search_with_score(query)
    #metadatas = vectorstore.similarity_search(query) #, n_results=5, include=['metadatas']) #, 'embeddings'])
    
    return results

# Function to project embeddings using UMAP
def project_embeddings(embeddings, umap_transform):
    st.write("project_embeddings")
    st.write("length embeddings: ", len(embeddings))

    umap_embeddings = np.empty((len(embeddings), 2))
    for i, embedding in enumerate(tqdm(embeddings)):
        umap_embeddings[i] = umap_transform.transform([embedding])
    return umap_embeddings

# Function to project embeddings using UMAP
def project_embeddings_1d_to_2d(embeddings, umap_transform):
    st.write("project_embeddings")
    st.write("length embeddings: ", len(embeddings))

    umap_embeddings = np.empty((len(embeddings), 2))
    for i, embedding in enumerate(tqdm(embeddings)):
        umap_embeddings[i] = umap_transform.transform(np.array(embedding).reshape(1, -1))[0]
    return umap_embeddings

# Streamlit UI
st.set_page_config(page_title="Fashion Explorer", layout="wide")
st.title("🛍️ Fashion Product Explorer")

# Sidebar navigation
st.sidebar.header("Navigation")
page = st.sidebar.selectbox("Go to", ["Home", "LocalFileStore", "Vectorstore", "UMAP Plot", "UMAP Plot Query"])


# Sidebar filters
st.sidebar.header("🎛️ Filters")
category = st.sidebar.selectbox("👗 Select Category", ["All", "Dresses", "Shoes", "Bags", "Accessories"])
price_range = st.sidebar.slider("💰 Price Range", 0, 500, (50, 200))

# Search box
query = st.text_input("🔍 Search for a fashion product, e.g. white tshirts")

# Streamlit app
#st.title("Vectorstore and LocalFileStore Dashboard")

if page == "LocalFileStore":
    # Display elements in LocalFileStore
    st.header("LocalFileStore Elements")
    keys = list(local_file_store.yield_keys())
    num_keys = len(keys)
    st.write(f"Number of keys in LocalFileStore: {num_keys}")

    if keys:
        for key in keys:
            value = local_file_store.mget(key)
            #st.write(f"Key: {key}, Value: {value}")
    else:
        st.write("No elements found in LocalFileStore.")

elif page == "Vectorstore":
    # Display elements in Vectorstore
    st.header("Vectorstore Elements")
    try:
        query_test = query
        #query_test = "white shirt"
        retrieved_docs = retriever.invoke(query)
        num_retrieved_docs = len(retrieved_docs)
        st.write(f"Number of retrieved documents: {num_retrieved_docs}")

        count = 0
        for doc in retrieved_docs:
        # Assuming page_content is a JSON string, parse it into a dictionary
            st.write(f"show page content: {count}")
            page_content = json.loads(doc.page_content)
            #st.write(page_content)
            #st.write(len(page_content))

            # Display first base64 image
            #if "image_encodings" in page_content and page_content["image_encodings"]:
            #    img = decode_base64_image(page_content["image_encodings"][0])
            #    st.image(img, caption="Product Image first", use_container_width=True)

            st.subheader("Product Images")
            if "image_encodings" in  page_content and  page_content["image_encodings"]:
                images = [decode_base64_image(img) for img in page_content["image_encodings"]]
                
                # Set number of columns per row
                num_columns = 5  
                rows = [images[i:i+num_columns] for i in range(0, len(images), num_columns)]
                
                for row in rows:
                    cols = st.columns(num_columns)  # Create columns
                    for col, img in zip(cols, row):
                        col.image(img, use_container_width=True)

            # Display all images from base64 encodings
            #st.subheader("Product Images")
            #if "image_encodings" in page_content and page_content["image_encodings"]:
            #    for encoded_img in page_content["image_encodings"]:
            #        img = decode_base64_image(encoded_img)
            #        st.image(img, caption="Product Image", use_container_width=True)


            # Product details
            st.subheader("Product Details")
            st.write(f"**Category:** {page_content['category']}")
            st.write(f"**Color:** {page_content['color']['color']}")
            st.write(f"**Style:** {', '.join(page_content['style']['styles'])}")
            st.write(f"**Occasions:** {page_content['occasions']['occasions']}")
            st.write(f"**Season:** {page_content['season']}")
            st.write(f"**Characteristics:** {', '.join(page_content['characteristics'])}")
            st.write(f"**Description:** {page_content['style']['description']}")

            count += 1

            st.write(page_content)
            st.write(len(page_content))

    except Exception as e:
        st.error(f"Error querying vector store: {e}")

elif page == "UMAP Plot":
    st.title("UMAP 2D Plot of Embeddings")
    st.header("UMAP Plot")

    # Retrieve embeddings from the vector store
    try:
        #if "vectorstore" in st.session_state:
            # Get embeddings
        embeddings, metadatas = get_all_embeddings(vectorstore)

        if len(embeddings) == 0:
            st.warning("No embeddings found in the database.")
        else:
            # Reduce embeddings to 2D
            reducer = umap.UMAP(n_components=2, random_state=42)
            embeddings_2d = reducer.fit_transform(embeddings)

            # Create a plot
            fig = px.scatter(
                x=embeddings_2d[:, 0],
                y=embeddings_2d[:, 1],
                title="UMAP 2D Plot of Embeddings"
            )
            st.plotly_chart(fig)
        #else:
        #    st.error("Chroma instance not found. Please initialize it in `st.session_state.chroma_instance`.")

    except Exception as e:
        st.error(f"Error retrieving embeddings: {e}")

elif page == "UMAP Plot Query":
    st.title("UMAP 2D Plot of Embeddings with Query and Retrieved Documents")
    st.header("UMAP Plot")

    #st.write("Testing embedding function on 'test' :", vectorstore._embedding_function.embed_query("test"))
    st.write("Query: ", query)
    st.write(f"Number of tokens in query: {embedding_function.count_tokens(query)}")  # Output number of tokens in query

    # Retrieve the query and document metadata
    result = get_query_doc_meta_dist(vectorstore, query)
    #st.write("meta vector search: ", meta)

    #metadatas = result["metadatas"][0]  # Extract metadata
    #cs_score = result["distances"][0]   # Extract cosine similarity scores



    retrieved_docs = retriever.invoke(query)
    # Retrieve embeddings from the vector store
    try:
        embeddings, metadatas = get_all_embeddings(vectorstore)
        if len(embeddings) == 0:
            st.warning("No embeddings found in the database.")
        else:
            # Fit UMAP on the dataset embeddings
            st.write("Fitting UMAP on the dataset embeddings...")

            # Reduce embeddings to 2D
            reducer = umap.UMAP(n_components=2, random_state=42)
            projected_dataset_embeddings = reducer.fit_transform(embeddings)

            #umap_transform = umap.UMAP(random_state=0, transform_seed=0).fit(embeddings)
            #st.write("Projecting the dataset embeddings, query, and retrieved documents...")
            # Project the dataset embeddings
            #projected_dataset_embeddings = umap_transform.transform(embeddings)

            # Project the query and retrieved document embeddings
            
            st.write(f"getting query embedding... for query: **{query}**")
            #query_embedding = vectorstore._embedding_function([query])[0]
            query_embedding = np.array(vectorstore._embedding_function.embed_query(query))
            st.write("shape query embedding: ", query_embedding.shape)
            
            #query_umap_transformed = reducer.fit_transform(query_embedding)

            
            #retrieved_embeddings = [doc.embedding for doc in retrieved_docs]
            st.write(f"Number of retrieved documents: {len(retrieved_docs)}")
            #st.write("getting retrieved embeddings...")
            retrieved_embeddings = np.array([vectorstore._embedding_function.embed_document(doc.page_content) for doc in retrieved_docs])
            st.write("shape query embedding: ", retrieved_embeddings.shape)

            st.write("Fitting UMAP on the query embeddings...")
            #umap_transform = umap.UMAP(random_state=0, transform_seed=0).fit(query_embedding)
            st.write("Projecting the query embeddings...")
            projected_query_embedding = project_embeddings_1d_to_2d([query_embedding], reducer)


            st.write("Projecting the retrieved document embeddings...")
            projected_retrieved_embeddings = project_embeddings_1d_to_2d(retrieved_embeddings, reducer)

            st.write("Plotting the UMAP results...")
            # Create a DataFrame for plotting
            df = pd.DataFrame(projected_dataset_embeddings, columns=["UMAP1", "UMAP2"])
            df["Type"] = "Dataset"

            query_df = pd.DataFrame(projected_query_embedding, columns=["UMAP1", "UMAP2"])
            query_df["Type"] = "Query"

            retrieved_df = pd.DataFrame(projected_retrieved_embeddings, columns=["UMAP1", "UMAP2"])
            retrieved_df["Type"] = "Retrieved"

            plot_df = pd.concat([df, query_df, retrieved_df])

            # Plot the UMAP results
            fig = px.scatter(plot_df, x="UMAP1", y="UMAP2", color="Type", title="UMAP 2D Plot of Embeddings")
            st.plotly_chart(fig)

    except Exception as e:
        st.error(f"Error retrieving embeddings: {e}")



#This script sets up a Streamlit dashboard for exploring fashion products using a vector store and local file store.
#It includes the following functionalities:
#1. Load environment variables from a .env file.
#2. Decode base64 encoded images.
#3. Initialize a LocalFileStore and a MultiModalChroma vector store.
#4. Set up a ParentDocumentRetriever for retrieving documents based on search queries.
#5. Create a Streamlit UI with filters, a search box, and display sections for LocalFileStore and vector store elements.
#6. Display product images and details retrieved from the vector store.

#✅ Decodes base64 images and displays them properly.
#✅ Lists all metadata (title, descriptions, category, color, style, characteristics, occasions, and seasons).
#✅ Supports multiple images, displaying all decoded base64 images.
#✅ Provides a link to the original product page.

