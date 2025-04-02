import streamlit as st
import torch
from PIL import Image
import io
from chromadb import PersistentClient
#from langchain.embeddings import CLIPEmbeddings
from chains.modules.embeddings import CLIPEmbeddings

# Define paths
PERSIST_DIR = "/Users/markobriesemann/Desktop/Machine_Learning/Project/1_UPSAIL/Github_Marko/upsailai-demo/discord/data/chroma_db"

# Initialize ChromaDB client
client = PersistentClient(PERSIST_DIR)
collection = client.get_collection("full_documents")

# Initialize CLIP embedding model
clip_embedder = CLIPEmbeddings()

# Streamlit UI
st.set_page_config(page_title="Fashion Explorer", layout="wide")
st.title("🛍️ Fashion Product Explorer")

# Sidebar filters
st.sidebar.header("🎛️ Filters")
category = st.sidebar.selectbox("👗 Select Category", ["All", "Dresses", "Shoes", "Bags", "Accessories"])
price_range = st.sidebar.slider("💰 Price Range", 0, 500, (50, 200))

# Search box
query = st.text_input("🔍 Search for a fashion product")

if query:
    # Convert query into an embedding
    query_embedding = clip_embedder.embed_query(query)

    # Perform vector search
    results = collection.query(query_embeddings=[query_embedding], n_results=9)  # Show 9 results

    # Filter results based on category & price
    filtered_results = []
    for doc in results["documents"]:
        title = doc.get("title", "Unknown Title")
        description = doc.get("description", "No description available")
        image_data = doc.get("image", None)
        product_category = doc.get("category", "Unknown")
        price = float(doc.get("price", 0))

        # Apply filters
        if (category == "All" or product_category == category) and (price_range[0] <= price <= price_range[1]):
            filtered_results.append((title, description, image_data, product_category, price))

    # Display results in a grid layout
    if filtered_results:
        st.subheader(f"🔎 Results for: *{query}*")

        cols = st.columns(3)  # Create a 3-column grid

        for i, (title, description, image_data, product_category, price) in enumerate(filtered_results):
            with cols[i % 3]:  # Distribute in 3 columns
                if image_data:
                    image = Image.open(io.BytesIO(image_data))
                    st.image(image, caption=f"{title} - ${price:.2f}", use_column_width=True)
                
                st.subheader(title)
                st.write(f"🛍️ Category: {product_category}")
                st.write(f"💰 Price: ${price:.2f}")
                st.write(description)

                # Button for product details
                if st.button(f"🔎 View {title}", key=f"button_{i}"):
                    st.write(f"More details about {title}...")
    else:
        st.warning("❌ No products found matching your filters.")
