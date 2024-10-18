import requests

# Use the sessionId and evaluationID obtained from the previous steps
session_id = "8Bws8LMNQ7vWfiEDTdxTZpxmI3mhKFTP"  # Replace with your actual sessionId
evaluation_id = "69ec2262-d829-4ac1-94a2-1aa0a6693266"  # Replace with your actual evaluationID

# Define the URL for the POST request
url = f"https://eventretrieval.one/api/v2/submit/{evaluation_id}"

Video_Answer = "L03_V006"
Time_ms_Answer = 880000
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
                    "start": int(Time_ms_Answer),  # Replace with the start time in milliseconds
                    "end": int(Time_ms_Answer)  # Replace with the end time in milliseconds
                }
            ]
        }
    ]
}

# Make the POST request to submit the answer
response = requests.post(url, params=params, json=body_KIS)

# Print the server's response
if response.status_code == 200:
    print("Answer submitted successfully!")
    print(response.json())
else:
    print(f"Failed to submit the answer, status code: {response.status_code}")
    print(response.text)
