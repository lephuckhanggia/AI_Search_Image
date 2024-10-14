from PIL import Image
import chromadb
from chromadb.utils.embedding_functions import OpenCLIPEmbeddingFunction
from chromadb.utils.data_loaders import ImageLoader
import numpy as np
from tqdm import tqdm
import os
import glob
from timeit import default_timer as timer
import traceback

start = timer()

image_folder_path = r"C:\AI Chalenge 2024\Data 2024\KeyFrames_L01_L022"  # add your folder path here
image_files = glob.glob(os.path.join(image_folder_path, '**', '*.jpg'), recursive=True)

db_path = r"D:\LePhucKhangGia\AI_Chanllenge_2024\Final\DB_L01_L22"  # add your db path here

# Initialize Chroma DB client, embedding function, and data loader
client = chromadb.PersistentClient(path=db_path)
embedding_function = OpenCLIPEmbeddingFunction()
data_loader = ImageLoader()

collection = client.get_or_create_collection(
    name='multimodal_collection3',
    embedding_function=embedding_function,
    data_loader=data_loader
)

def add_images_to_collection(folder_path):
    for image_path in tqdm(image_files, desc="Creating Image Embeddings and Adding to DB"):
        try:
            image = np.array(Image.open(image_path))
            unique_id = os.path.relpath(image_path, start=image_folder_path)  # Use relative path as ID
            collection.add(
                ids=[unique_id],
                images=[image]
            )
        except Exception as e:
            print(f"Error processing {image_path}: {e}")
            traceback.print_exc()  # Optional: Print detailed traceback for debugging

add_images_to_collection(image_folder_path)
print(f"Time to process: {timer()-start}")

