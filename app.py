import streamlit as st
import cv2
import numpy as np
import time

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

def main():
    st.set_page_config(page_title="Sheet Count from Image", layout="wide")

    # Header
    st.title("📄 Sheet Count from Image")
    st.markdown(
        """
        Upload an image of stacked sheets, and the app will automatically count the number of sheets using edge detection.
        
        **How to Use:**
        1. Click on the **"Upload Image"** button to select an image of stacked sheets.
        2. The app will automatically process the image and display the results.
        3. You will see the original image, edge-detected image, total sheet count, and time taken for processing.
        """
    )

    # File uploader
    uploaded_file = st.file_uploader("Upload Image", type="jpeg", help="Select a JPEG image of stacked sheets.")

    # Expandable section for default thresholds
    with st.expander("Show Default Edge Detection Thresholds"):
        st.write("### Default Edge Detection Thresholds:")
        st.write("- **Min Edge Threshold:** 50")
        st.write("- **Max Edge Threshold:** 150")

    if uploaded_file is not None:
        st.spinner("Processing image...")
        
        # Convert the uploaded file to a format OpenCV can work with
        image = np.array(bytearray(uploaded_file.read()), dtype=np.uint8)
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        
        # Measure processing time
        start_time = time.time()
        
        # Preprocess the image and detect edges
        edges = preprocess_image(image)
        
        # Count the sheets
        sheet_count = count_sheets(edges)
        
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

if __name__ == '__main__':
    main()