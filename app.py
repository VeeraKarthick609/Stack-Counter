import streamlit as st
import cv2
import numpy as np
import time
import tempfile

def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)  # Default thresholds
    dilated = cv2.dilate(edges, None, iterations=2)
    eroded = cv2.erode(dilated, None, iterations=1)
    return eroded

def count_sheets(edges):
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    sheet_count = len(contours)
    return sheet_count

def process_frame(frame):
    edges = preprocess_image(frame)
    sheet_count = count_sheets(edges)
    return edges, sheet_count

def main():
    st.set_page_config(page_title="Sheet Counter App", page_icon="📄", layout="wide")

    # Header
    st.title("📄 Sheet Count from Image/Video")
    st.markdown(
        """
        Upload an image or video of stacked sheets, and the app will automatically count the number of sheets using edge detection.
        
        **How to Use:**
        1. Click on the **"Upload Image/Video"** button to select an image or video of stacked sheets.
        2. The app will automatically process the image/video and display the results.
        3. For images, you will see the original image, edge-detected image, total sheet count, and time taken for processing.
        4. For videos, you will see the processed video with sheet count displayed on each frame.
        """
    )

    # File uploader
    uploaded_file = st.file_uploader("Upload Image/Video", type=["jpeg", "mp4"], help="Select a JPEG image or MP4 video of stacked sheets.")

    # Expandable section for default thresholds
    with st.expander("Show Default Edge Detection Thresholds"):
        st.write("### Default Edge Detection Thresholds:")
        st.write("- **Min Edge Threshold:** 50")
        st.write("- **Max Edge Threshold:** 150")

    if uploaded_file is not None:
        file_type = uploaded_file.type

        if file_type == "image/jpeg":
            st.spinner("Processing image...")

            # Convert the uploaded file to a format OpenCV can work with
            image = np.array(bytearray(uploaded_file.read()), dtype=np.uint8)
            image = cv2.imdecode(image, cv2.IMREAD_COLOR)

            # Measure processing time
            start_time = time.time()

            # Process the image
            edges, sheet_count = process_frame(image)

            # Measure the end time and calculate processing time
            end_time = time.time()
            processing_time = end_time - start_time

            # Display results
            st.write("### Results")

            # Create two columns for displaying images
            col1, col2 = st.columns(2)

            with col1:
                st.write("### Original Image")
                # Scale down the image
                scaled_image = cv2.resize(image, (400, 400))
                st.image(scaled_image, channels="BGR", caption="Original Image")

            with col2:
                st.write("### Edge Detection")
                # Scale down the edge-detected image
                scaled_edges = cv2.resize(edges, (400, 400))
                st.image(scaled_edges, channels="GRAY", caption="Edge Detection")

            st.write(f"### Total Sheets: **{sheet_count}**")
            st.write(f"### Time Taken to Process Image: **{processing_time:.2f}** seconds")

        elif file_type == "video/mp4":
            st.spinner("Processing video...")

            # Save the uploaded video to a temporary file
            tfile = tempfile.NamedTemporaryFile(delete=False) 
            tfile.write(uploaded_file.read())

            # Open the video file
            video = cv2.VideoCapture(tfile.name)

            # Get video properties
            width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = int(video.get(cv2.CAP_PROP_FPS))

            # Set display width (adjust this value to change the displayed video size)
            display_width = 320  # Adjust this value as needed
            display_height = int(height * display_width / width)

            # Create placeholders for the video
            col1, col2 = st.columns(2)
            video_placeholder1 = col1.empty()
            video_placeholder2 = col2.empty()

            while video.isOpened():
                ret, frame = video.read()
                if not ret:
                    break

                # Process the frame
                edges, sheet_count = process_frame(frame)

                # Resize the frames for display
                display_frame = cv2.resize(frame, (display_width, display_height))
                display_edges = cv2.resize(edges, (display_width, display_height))

                # Add sheet count to the original frame
                cv2.putText(display_frame, f"Sheets: {sheet_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

                # Display the frames
                video_placeholder1.image(display_frame, channels="BGR", use_column_width=True)
                video_placeholder2.image(display_edges, channels="GRAY", use_column_width=True)

                # Control frame rate
                time.sleep(1/fps)

            video.release()

        else:
            st.error("Unsupported file type. Please upload a JPEG image or MP4 video.")

if __name__ == '__main__':
    main()
