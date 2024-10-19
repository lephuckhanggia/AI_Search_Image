import streamlit as st
import chromadb
from chromadb.utils.embedding_functions import OpenCLIPEmbeddingFunction
from chromadb.utils.data_loaders import ImageLoader
import os
import csv
import pandas as pd
from timeit import default_timer as timer
import requests
from streamlit import image

# Initialize variables
db_path = 0

# Submission API Info
session_id = "8Bws8LMNQ7vWfiEDTdxTZpxmI3mhKFTP"
evaluation_id = "bec3b699-bdea-4f2c-94ae-61ee065fa76e"  # The active evaluationID you retrieved
url = f"https://eventretrieval.one/api/v2/submit/{evaluation_id}"


# Define DB paths
DB_FULL_FINAL = r"D:\LePhucKhangGia\AI_Chanllenge_2024\Final\DB_FULL_FINAL"
DB_L01_L22 = r"D:\LePhucKhangGia\AI_Chanllenge_2024\Final\DB_L01_L22"
DB_L23 = r"D:\LePhucKhangGia\AI_Chanllenge_2024\Final\DB_L23"
DB_L24 = r"D:\LePhucKhangGia\AI_Chanllenge_2024\Final\DB_L24"
DB_L25 = r"D:\LePhucKhangGia\AI_Chanllenge_2024\Final\DB_L25"
DB_L26 = r"D:\LePhucKhangGia\AI_Chanllenge_2024\Final\DB_L26"
DB_L27 = r"D:\LePhucKhangGia\AI_Chanllenge_2024\Final\DB_L27"
DB_L28 = r"D:\LePhucKhangGia\AI_Chanllenge_2024\Final\DB_L28"
DB_L29 = r"D:\LePhucKhangGia\AI_Chanllenge_2024\Final\DB_L29"
DB_L30 = r"D:\LePhucKhangGia\AI_Chanllenge_2024\Final\DB_L30"
DB_List = [DB_FULL_FINAL, DB_L01_L22, DB_L23,DB_L24, DB_L25, DB_L26, DB_L27, DB_L28, DB_L29, DB_L30]

csv_folder_path = r"D:\LePhucKhangGia\AI_Chanllenge_2024\Final\CSV_0.1"
parent_path = r"C:\AI Chalenge 2024\Data 2024\KeyFrames_0.1"
result_path = r'D:\LePhucKhangGia\AI_Chanllenge_2024\AI_Search_Image\Result'

# Set up page layout
st.markdown(
    """
    <style>
    /* Adjust the width of the main content area */
    .main .block-container {
        min-width: 1200px; /* Force the content to stretch */
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

# Store search results in session state to persist across interactions
if "search_results" not in st.session_state:
    st.session_state.search_results = None

#SIDE BAR FOR NAVIGATION
with st.sidebar:
    #banner_image_path = r"D:\LePhucKhangGia\AI_Chanllenge_2024\Team_Photos\I MISS HER BANNER.png"
    #st.image(banner_image_path, use_column_width=True)

    st.title("Image Search Engine")

    # Place DB selector, query input, file name input, and search button at the top
    DB_select = st.selectbox("Choose DB set you want:", options=DB_List)
    db_path = DB_select  # Simplified assignment

    # Input search query and custom file name at the top
    query = st.text_input("Enter your search query:")
    file_name_input = st.text_input("Enter the desired file name (without extension):", "Result_Test")
    nearby_img_range_input = st.text_input("Nearby Images range:","5")
    nearby_img_range = int(nearby_img_range_input)
    file_name = f"{file_name_input}.csv"
    output_csv_path = os.path.join(result_path, file_name)
    start = timer()
    # Place the Search button at the top of the page
    if st.button("Search"):
        # Start timer and perform search query

        client = chromadb.PersistentClient(path=db_path)
        embedding_function = OpenCLIPEmbeddingFunction()
        data_loader = ImageLoader()

        collection = client.get_or_create_collection(
            name='multimodal_collection3',
            embedding_function=embedding_function,
            data_loader=data_loader
        )

        results = collection.query(query_texts=[query], n_results=100, include=["distances"])

        # Store the results in session state
        st.session_state.search_results = results
        st.session_state.checkbox_states = {}  # Reset checkbox states after new search

    #Define values for Submission
    def submit_qa_answer():
        response = requests.post(url, params=params, json=body_QA)
        return response
    def submit_kis_answer():
        response = requests.post(url, params=params, json=body_KIS)
        return response
    st.title("Submission")
    Video_Answer = st.text_input("Video name:")
    Time_ms_Answer = st.text_input("Time in ms: ")
    QA_Answer = st.text_input("QA Ansewer:")
    QA_Answer_Structure = (f'{QA_Answer}-{Video_Answer}-{Time_ms_Answer}')

    # Submission Body
    # Set up the parameters and the body
    params = {
        "session": session_id
    }

    # Define the body (for KIS answers)
    body_KIS = {
        "answerSets": [
            {
                "answers": [
                    {
                        "mediaItemName": Video_Answer,  # Replace with the video ID without the file extension
                        "start":Time_ms_Answer,  # Replace with the start time in milliseconds
                        "end": Time_ms_Answer  # Replace with the end time in milliseconds
                    }
                ]
            }
        ]
    }
    # Body for QA submission
    body_QA = {
        "answerSets": [
            {
                "answers": [
                    {
                        "text": QA_Answer_Structure # Format: <ANSWER>-<VIDEO_ID>-<TIME(ms)>
                    }
                ]
            }
        ]
    }
    Answer_list = {
    "KIS Answer": body_KIS,
    "QA Answer": body_QA
}
    Answer_Select = st.selectbox("Chosse QA or KIS answer", options=Answer_list)
    body = Answer_Select
    if st.button("SUBMIT RESULT"):

        # Call the function and check the result
        response = submit_kis_answer()

        # Step 5: Check the server's response
        if response.status_code == 200:
            st.write("KIS answer submitted successfully!")
            st.write(response.json())
        else:
            st.write(f"Failed to submit KIS answer, status code: {response.status_code}")
            st.write(response.text)
        st.write(QA_Answer_Structure)
        st.write(Video_Answer)
        st.write(Time_ms_Answer)
        st.write("Submitting the following body:")
        st.write(body)

# Retrieve stored search results if available
results = st.session_state.search_results

if results:
    all_data = []

    # Containers for layout stability
    image_col_container = st.container()
    list_image_col_container = st.container()

    with image_col_container:
        # Columns for image and list display
        image_col, list_image_col = st.columns([0.7, 0.3])

        for idx, (image_id, distance) in enumerate(zip(results['ids'][0], results['distances'][0])):
            image_path = os.path.join(parent_path, image_id)
            image_num = os.path.splitext(os.path.basename(image_path))[0]
            video_name = os.path.basename(os.path.dirname(image_id))
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
                            time_value_sec = round(float(row[1]),2)
                            time_value_mili = int(time_value_sec * 1000)
                            data.append({'directory': directory_name, 'time(ms)': time_value_mili})
                            break

            if data:
                all_data.extend(data)

            with image_col:
                if os.path.exists(image_path):
                    st.image(image_path, caption=os.path.basename(image_path))
                    col_1, col_2,col_3 = st.columns([0.4, 0.3,0.2])

                    with col_1:
                        st.write(idx + 1,  "Num: ",image_num)
                        st.write(f'Name: {video_name}')
                        st.write("Time: ",time_value_mili)
                        checkbox_key = f"checkbox_{idx + 1}"
                        if checkbox_key not in st.session_state.checkbox_states:
                            st.session_state.checkbox_states[checkbox_key] = False  # Default value

                        st.session_state.checkbox_states[checkbox_key] = st.checkbox(
                            f"{idx + 1} Correct", value=st.session_state.checkbox_states[checkbox_key]
                        )

                    with col_2:
                        # Create a button with a unique key for each image
                        if st.button(f"Nearby Images {idx + 1}", key=f"nearby_button_{idx + 1}"):
                            # Initialize the nearby_image_paths list
                            nearby_image_paths = []

                            # Extract the image number and find nearby images
                            filename = os.path.basename(image_id)
                            number_part = os.path.splitext(filename)[0]
                            last_number = int(number_part)
                            nearby_numbers = list(range(last_number - nearby_img_range, last_number + nearby_img_range + 1))

                            # Store the nearby image paths
                            for num in nearby_numbers:
                                # Find time value for nearby images
                                nearby_image_filename = f"{num}.jpg"
                                nearby_image_path = os.path.join(os.path.dirname(image_path), nearby_image_filename)

                                # Get the directory name for the nearby image
                                directory_name_nearby_img = os.path.basename(os.path.dirname(nearby_image_path))

                                # Construct the CSV file path for the nearby image
                                csv_file_path_nearby_img = os.path.join(csv_folder_path,
                                                                        f'{directory_name_nearby_img}.csv')

                                # Check if the CSV file exists
                                if os.path.exists(csv_file_path_nearby_img):
                                    with open(csv_file_path_nearby_img, 'r') as file:
                                        csvreader = csv.reader(file)
                                        header = next(csvreader)  # Skip header row
                                        for row in csvreader:
                                            row_num = int(row[0])
                                            if row_num == num:  # Use `num` to match the nearby image number
                                                time_value_sec_nearby_img = float(row[1])
                                                time_value_mili_nearby_img = int(time_value_sec_nearby_img * 1000)
                                                break

                                # Create the full path for the nearby image by keeping the same directory
                                if os.path.exists(nearby_image_path):
                                    nearby_image_paths.append((nearby_image_path, time_value_mili_nearby_img))  # Add to list with time
                                else:
                                    st.write(f"File not found: {nearby_image_path}")

                            # Save the results in session state to persist them across refreshes
                            st.session_state.nearby_images = nearby_image_paths  # Now this will work

                            # Split the nearby_image_paths into two halves
                            midpoint = len(nearby_image_paths) // 2
                            first_half = nearby_image_paths[:midpoint]
                            second_half = nearby_image_paths[midpoint:]

                            # Display the first half of nearby images in col_1
                            with col_1:
                                for img_path, img_time in first_half:
                                    image_number = os.path.splitext(os.path.basename(img_path))[0]  # Get the filename without extension
                                    st.image(img_path)  # Display the image
                                    st.write(f"Nearby image: {image_number}")  # Display the full path
                                    st.write("Time: ", img_time)  # Display the time

                            # Display the second half of nearby images in col_2
                            with col_2:
                                for img_path, img_time in second_half:
                                    image_number = os.path.splitext(os.path.basename(img_path))[0]  # Get the filename without extension
                                    st.image(img_path)  # Display the image
                                    st.write(f"Nearby image: {image_number}")  # Display the full path
                                    st.write("Time: ", img_time)  # Display the time

                            # Save the results in session state to persist them across refreshes
                            st.session_state.nearby_images = nearby_image_paths  # Now this will work
                    with col_3:



    if all_data:
        df = pd.DataFrame(all_data)
        df.to_csv(output_csv_path, index=False, header=False)
        st.write(f"Data has been written to {output_csv_path}")

    # Display time taken for the search
    st.write(f"Time to process: {timer() - start}")

    with list_image_col:  # Moved inside the results check
        if st.button("Show Checkbox Values"):
            # Prepare data for the DataFrame
            checkbox_data = []

            for checkbox_key, checked in st.session_state.checkbox_states.items():
                icon = "✅" if checked else "❌"
                checkbox_data.append({"Checkbox": checkbox_key, "Status": icon})

            # Create a DataFrame
            df = pd.DataFrame(checkbox_data)

            # Use a separate column for displaying the checkbox values
            st.write("Checked Values:")
            st.dataframe(df.style.set_table_attributes('style="width: 100%; white-space: nowrap;"'), height=800)  # Display the DataFrame as a table

        st.write("All image paths: ")
        counter = 0
        for image_id, distance in zip(results['ids'][0], results['distances'][0]):
            image_path = os.path.join(parent_path, image_id)
            if os.path.exists(image_path):
                counter += 1
                st.write(counter, image_id)
            else:
                st.write(f"File not found: {image_path}")