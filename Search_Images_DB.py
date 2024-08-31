#streamlit run "D:/Gia_Projects/github.com/lephuckhanggia/AI_Search_Image/Search_Images_DB.py"
import streamlit as st
import chromadb
from chromadb.utils.embedding_functions import OpenCLIPEmbeddingFunction
from chromadb.utils.data_loaders import ImageLoader
import os
import csv
import pandas as pd
from timeit import default_timer as timer
counter = 0
db_path = r"D:\Gia_Projects\github.com\lephuckhanggia\AI_Search_Image\DB_Full"  # Add your db path here
output_excel_path = r'D:\Gia_Projects\github.com\lephuckhanggia\AI_Search_Image\Result\Result_Test5.xlsx'
csv_folder_path = r"C:\AI Chalenge 2024\Data 2024\Map_Keyframes\map-keyframes-b1\map-keyframes"  # Path to the CSV files
parent_path = r"C:\AI Chalenge 2024\Data 2024\Keyframe"  # Base path to your image folder

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

# Initialize your data list outside the loop to collect all results
all_data = []

if st.button("Search"):
    start = timer()
    results = collection.query(query_texts=[query], n_results=100, include=["distances"])
    
    for image_id, distance in zip(results['ids'][0], results['distances'][0]):
        # Combine the parent path with the relative path (image_id) to get the full path
        image_path = os.path.join(parent_path, image_id) 
        filename_without_extension, _ = os.path.splitext(os.path.basename(image_path))
        filenum = int(filename_without_extension)
        #print("filename_without_extension=", filenum)
        directory_name = os.path.basename(os.path.dirname(image_path))
        csv_file_path = os.path.join(csv_folder_path, f'{directory_name}.csv')  # Find the CSV file with the same name as the directory

        data = []
        if os.path.exists(csv_file_path):
            with open(csv_file_path, 'r') as file:
                csvreader = csv.reader(file)
                header = next(csvreader)  # Skip the header row
                for row in csvreader:
                    row_num = int(row[0])
                    if row_num == filenum:  # Compare with the 'n' column
                        print(f'Matching row: {row}')
                        pts_time_value = row[1]
                        fps_value = row[2]
                        frame_idx_value = row[3]
        
                        # Append the values to the data list
                        data.append({
                            'file_num': filenum,
                            'directory_name': directory_name,
                            'pts_time': pts_time_value,
                            'fps': fps_value,
                            'frame_idx': frame_idx_value
                        })
                        break
        else:
            st.write(f"CSV file {csv_file_path} not found.")

        # If data was found, append it to all_data
        if data:
            all_data.extend(data)

        # Display the image if it exists
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
            counter += 1
            st.write(counter, image_path)
            #st.write(f"Distance: {distance}")
        else:
            st.write(f"File not found: {image_path}")
        
    # After the loop, write all the collected data to an Excel file
    if all_data:
        df = pd.DataFrame(all_data)
        df.to_excel(output_excel_path, index=False)
        st.write(f"Data has been written to {output_excel_path}")

    # Display time taken for the search
    st.write(f"Time to process: {timer() - start}")
