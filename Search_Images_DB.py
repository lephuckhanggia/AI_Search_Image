import streamlit as st
import chromadb
from chromadb.utils.embedding_functions import OpenCLIPEmbeddingFunction
from chromadb.utils.data_loaders import ImageLoader
import os
import csv
import pandas as pd
from timeit import default_timer as timer

# Initialize variables
counter = 0
counter2 = 0
db_path = 0

# Define DB paths
DB_FULL_FINAL = r"D:\LePhucKhangGia\AI_Chanllenge_2024\Final\DB_FULL_FINAL"
DB_L01_L22 = r"D:\LePhucKhangGia\AI_Chanllenge_2024\Final\DB_L01_L22"
DB_L23_L24 = r"D:\LePhucKhangGia\AI_Chanllenge_2024\Final\DB_L23_L24"
DB_L25 = r"D:\LePhucKhangGia\AI_Chanllenge_2024\Final\DB_L25"
DB_L26 = r"D:\LePhucKhangGia\AI_Chanllenge_2024\Final\DB_L26"
DB_List = [DB_FULL_FINAL, DB_L01_L22, DB_L23_L24, DB_L25, DB_L26]

csv_folder_path = r"D:\LePhucKhangGia\AI_Chanllenge_2024\Final\CSV_0.1"
parent_path = r"C:\AI Chalenge 2024\Data 2024\KeyFrames_0.1"
result_path = r'D:\LePhucKhangGia\AI_Chanllenge_2024\AI_Search_Image\Result'

# Set up page layout
st.markdown(
    """
    <style>
    /* Adjust the width of the main content area */
    .main .block-container {
        min-width: 5000px; /* Force the content to stretch */
        padding-left: 10px;  /* Optional: Add some padding */
        padding-right: 10px; /* Optional: Add some padding */
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Set up session state for checkbox persistence
if "checkbox_states" not in st.session_state:
    st.session_state.checkbox_states = {}

# Display the banner image
banner_image_path = r"D:\LePhucKhangGia\AI_Chanllenge_2024\Team_Photos\I MISS HER BANNER.png"
st.image(banner_image_path, use_column_width=True)

st.title("Image Search Engine")

# Select the DB set
DB_select = st.selectbox("Choose DB set you want:", options=DB_List)

# Update db_path based on selection
if DB_select == DB_FULL_FINAL:
    db_path = DB_FULL_FINAL
elif DB_select == DB_L01_L22:
    db_path = DB_L01_L22
elif DB_select == DB_L23_L24:
    db_path = DB_L23_L24
elif DB_select == DB_L25:
    db_path = DB_L25
elif DB_select == DB_L26:
    db_path = DB_L26

# Initialize Chroma DB client, embedding function, and data loader
client = chromadb.PersistentClient(path=db_path)
embedding_function = OpenCLIPEmbeddingFunction()
data_loader = ImageLoader()

collection = client.get_or_create_collection(
    name='multimodal_collection3',
    embedding_function=embedding_function,
    data_loader=data_loader
)

# Input search query
query = st.text_input("Enter your search query:")

# Get custom file name from the user
file_name_input = st.text_input("Enter the desired file name (without extension):", "Result_Test")
file_name = f"{file_name_input}.csv"
output_csv_path = os.path.join(result_path, file_name)

# Containers for layout stability
image_col_container = st.container()
list_image_col_container = st.container()

# If search button is clicked
if st.button("Search"):
    start = timer()
    results = collection.query(query_texts=[query], n_results=100, include=["distances"])

    all_data = []
    check_vars = {}

    with image_col_container:
        # Columns for image and list display
        image_col, list_image_col = st.columns([0.7, 0.3])

        for idx, (image_id, distance) in enumerate(zip(results['ids'][0], results['distances'][0])):
            image_path = os.path.join(parent_path, image_id)
            filename_without_extension, _ = os.path.splitext(os.path.basename(image_path))
            filenum = int(filename_without_extension)
            directory_name = os.path.basename(os.path.dirname(image_path))
            csv_file_path = os.path.join(csv_folder_path, f'{directory_name}.csv')

            data = []
            if os.path.exists(csv_file_path):
                with open(csv_file_path, 'r') as file:
                    csvreader = csv.reader(file)
                    header = next(csvreader)  # Skip header row
                    for row in csvreader:
                        row_num = int(row[0])
                        if row_num == filenum:
                            frame_idx_value = row[2]
                            data.append({'directory': directory_name, 'frameid': frame_idx_value})
                            break

            counter2 += 1
            if data:
                all_data.extend(data)

            with image_col:
                if os.path.exists(image_path):
                    st.image(image_path, caption=os.path.basename(image_path))
                    st.write(counter2, image_path)

                    # Use session state for the checkbox
                    checkbox_key = f"checkbox_{counter2}"
                    if checkbox_key not in st.session_state.checkbox_states:
                        st.session_state.checkbox_states[checkbox_key] = False  # Default value

                    # Checkbox and save the state
                    st.session_state.checkbox_states[checkbox_key] = st.checkbox(
                        f"{counter2} Correct", value=st.session_state.checkbox_states[checkbox_key]
                    )

                else:
                    st.write(f"File not found: {image_path}")

        with list_image_col:
            st.write("All image paths: ")
            for image_id, distance in zip(results['ids'][0], results['distances'][0]):
                if os.path.exists(image_path):
                    counter += 1
                    st.write(counter, image_id)
                else:
                    st.write(f"File not found: {image_path}")

    if all_data:
        df = pd.DataFrame(all_data)
        df.to_csv(output_csv_path, index=False, header=False)
        st.write(f"Data has been written to {output_csv_path}")

    # Display time taken for the search
    st.write(f"Time to process: {timer() - start}")
