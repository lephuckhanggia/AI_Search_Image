#streamlit run "C:/AI Chalenge 2024/Search_Images_DB_Translate.py"
import streamlit as st
import chromadb
from chromadb.utils.embedding_functions import OpenCLIPEmbeddingFunction
from chromadb.utils.data_loaders import ImageLoader
import os
import csv
import pandas as pd
from googletrans import Translator  # Use correct import from googletrans
from translate import Translator as AltTranslator
from langdetect import detect
from timeit import default_timer as timer
counter = 0
counter2 = 0
db_path = r"D:\Gia_Projects\github.com\lephuckhanggia\AI_Search_Image\DB_Full"  # Add your db path here
output_excel_path = r'D:\Gia_Projects\github.com\lephuckhanggia\AI_Search_Image\Result\Submission_R0\query-1-kis.xlsx'
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
banner_image_path = r"D:\Gia_Projects\github.com\lephuckhanggia\AI_Search_Image\Lucky_banner.jpg"  # Update with the path to your banner image
st.image(banner_image_path, use_column_width=True)

st.title("Image Search Engine")

# Search bar
text = st.text_input("Enter your search query:")

# Initialize your data list outside the loop to collect all results
all_data = []

class Translation():
    def __init__(self, from_lang='vi', to_lang='en', mode='google'):
        # The class Translation is a wrapper for googletrans and translate libraries
        self.__mode = mode
        self.__from_lang = from_lang
        self.__to_lang = to_lang

        if mode == 'google':
            self.translator = Translator()
        elif mode == 'translate':
            self.translator = AltTranslator(from_lang=from_lang, to_lang=to_lang)

    def preprocessing(self, text):
        return text.lower()

    def __call__(self, text):
        text = self.preprocessing(text)
        if self.__mode == 'translate':
            return self.translator.translate(text)
        else:
            return self.translator.translate(text, dest=self.__to_lang).text
def text_search(text):
    translater = Translation()  # Create an instance of the Translation class
    if detect(text) == 'vi':  # If the detected language is Vietnamese
        text = translater(text)  # Translate the text to English
    return text  # Return the translated text

if st.button("Search"):
    start = timer()
    
    # Translate the text before processing
    translated_text = text_search(text)  # Call the text search function
    results = collection.query(query_texts=[translated_text], n_results=100, include=["distances"])
    
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
                        #pts_time_value = row[1]
                        #fps_value = row[2]
                        frame_idx_value = row[3]
        
                        # Append the values to the data list
                        data.append({    
                            'directory':directory_name,
                            'frameid':frame_idx_value
                        })
                        break
        else:
            st.write(f"CSV file {csv_file_path} not found.")
        counter2 += 1
        # If data was found, append it to all_data
        if data:
            all_data.extend(data)

        # Display the image if it exists
        if os.path.exists(image_path):
            st.image(image_path, caption=os.path.basename(image_path))
            st.write(counter2,image_path)
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
        df.to_csv(output_excel_path.replace('.xlsx', '.csv'), index=False)
        st.write(f"Data has been written to {output_excel_path.replace('.xlsx', '.csv')}")

    # Display time taken for the search
    st.write(f"Time to process: {timer() - start}")
