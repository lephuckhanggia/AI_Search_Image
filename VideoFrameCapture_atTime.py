import cv2

# Path to the video
video_path = r'C:\AI Chalenge 2024\Data 2024\Video_Full\Videos_L06_a\video\L06_V026.mp4'

# Open the video file
cam = cv2.VideoCapture(video_path)

# Set the time (in seconds) where you want to capture the frame
capture_time = 895    # Time in seconds

# Get the FPS (frames per second) of the video
fps = cam.get(cv2.CAP_PROP_FPS)

# Calculate the frame number at the desired time
frame_number = int(capture_time * fps)

# Set the video to the calculated frame number
cam.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

# Read the frame at the specific time
ret, frame = cam.read()

if ret:
    # Show the frame
    cv2.imshow('Frame at specific time', frame)

    # Save the frame as a JPEG file
    cv2.imwrite(f'Frame_at_{capture_time}_seconds.jpg', frame)

    # Wait for a key press and then close the window
    cv2.waitKey(0)
else:
    print("Could not read the frame at the specified time.")

# Release the video capture and close windows
cam.release()
cv2.destroyAllWindows()

