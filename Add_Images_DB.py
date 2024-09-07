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

image_folder_path = r"C:\AI Chalenge 2024\Data 2024\Keyframe"  # add your folder path here
image_files = glob.glob(os.path.join(image_folder_path, '**', '*.jpg'), recursive=True)

db_path = r"D:\Gia_Projects\github.com\lephuckhanggia\AI_Search_Image\DB_Full_2"  # add your db path here

# Initialize Chroma DB client, embedding function, and data loader
client = chromadb.PersistentClient(path=db_path)
embedding_function = OpenCLIPEmbeddingFunction()
data_loader = ImageLoader()

collection = client.get_or_create_collection(
    name='multimodal_collection3',
    embedding_function=embedding_function,
    data_loader=data_loader
)

# Define batch size
batch_size = 100


def add_images_to_collection(folder_path):
    batch_images = []
    batch_ids = []

    for image_path in tqdm(image_files, desc="Creating Image Embeddings and Adding to DB"):
        try:
            image = np.array(Image.open(image_path))
            unique_id = os.path.relpath(image_path, start=image_folder_path)  # Use relative path as ID
            batch_images.append(image)
            batch_ids.append(unique_id)

            # If batch is ready, add it to the collection
            if len(batch_images) == batch_size:
                collection.add(
                    ids=batch_ids,
                    images=batch_images
                )
                batch_images.clear()  # Clear batch after adding
                batch_ids.clear()

        except Exception as e:
            print(f"Error processing {image_path}: {e}")
            traceback.print_exc()  # Optional: Print detailed traceback for debugging

    # Add any remaining images if they don't make up a full batch
    if batch_images:
        collection.add(
            ids=batch_ids,
            images=batch_images
        )


add_images_to_collection(image_folder_path)
print(f"Time to process: {timer() - start}")
