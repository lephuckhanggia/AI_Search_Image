import streamlit as st
import chromadb
from chromadb.utils.embedding_functions import OpenCLIPEmbeddingFunction
from chromadb.utils.data_loaders import ImageLoader
import os
from timeit import default_timer as timer

db_path = r"C:\AI Chalenge 2024\Data_Base\Final"  # Add your db path here

# Initialize Chroma DB client, embedding function, and data loader
client = chromadb.PersistentClient(path=db_path)
embedding_function = OpenCLIPEmbeddingFunction()
data_loader = ImageLoader()

collection = client.get_or_create_collection(
    name='multimodal_collection3',
    embedding_function=embedding_function,
    data_loader=data_loader
)

# Display the banner image
banner_image_path = r"C:\AI Chalenge 2024\IMG_6447.JPG"  # Update with the path to your banner image
st.image(banner_image_path, use_column_width=True)

st.title("Image Search Engine")

# Search bar
query = st.text_input("Enter your search query:")
parent_path = r"C:\AI Chalenge 2024\FINAL_Optimised\Keyframes_Optimized"  # Base path to your image folder

if st.button("Search"):
    start = timer()
    results = collection.query(query_texts=[query], n_results=100, include=["distances"])
    print(results)
    
    for image_id, distance in zip(results['ids'][0], results['distances'][0]):
        # Combine the parent path with the relative path (image_id) to get the full path
        image_path = os.path.join(parent_path, image_id)        
        if os.path.exists(image_path):
            st.image(image_path, caption=os.path.basename(image_path))
            st.write(image_path)
            st.write(f"Distance: {distance}")
        else:
            st.write(f"File not found: {image_path}")
    st.write("All image path: ")
    for image_id, distance in zip(results['ids'][0], results['distances'][0]):
        image_path = os.path.join(parent_path, image_id)        
        if os.path.exists(image_path):
            st.write(image_path)
            #st.write(f"Distance: {distance}")
        else:
            st.write(f"File not found: {image_path}")
    st.write(f"Time to process: {timer() - start}")
