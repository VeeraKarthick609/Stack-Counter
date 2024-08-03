# Sheet Count from Image - Streamlit App

This Streamlit app allows you to upload an image of stacked sheets and automatically count the number of sheets using edge detection.

## Features
- Upload an image and get the sheet count.
- View the original and edge-detected images side by side.
- See the processing time for the image.
- Option to view default edge detection thresholds.

## Prerequisites

Before running the app, ensure you have the following installed:

- Python 3.10 or higher
- Streamlit
- OpenCV
- NumPy

You can install these packages using `pip`:

```bash
pip install streamlit opencv-python numpy
```

## Running the App

1. **Save the Code:**
   Save the provided Python code into a file named `app.py`.

2. **Run the Streamlit App:**
   Open a terminal or command prompt, navigate to the directory where `app.py` is located, and run the following command:

   ```bash
   streamlit run app.py
   ```

3. **Open the App in Your Browser:**
   After running the command, Streamlit will start a local server and provide a URL, typically `http://localhost:8501`. Open this URL in your web browser to access the app.

## Usage Instructions

1. **Upload an Image:**
   - Click the **"Upload Image"** button to select and upload a JPEG image of stacked sheets.

2. **View Results:**
   - The app will automatically process the image and display the results.
   - The original image and the edge-detection result will be shown side by side.
   - The total number of sheets detected and the time taken for processing will be displayed.

3. **View Default Thresholds:**
   - Click on the expandable section labeled **"Show Default Edge Detection Thresholds"** to view the default thresholds used in the edge detection process.

## Example

Here's what you should expect:

- **Original Image:** Displays the uploaded image of stacked sheets.
- **Edge Detection:** Shows the processed image with detected edges.
- **Total Sheets:** The number of sheets detected in the image.
- **Processing Time:** Time taken to process the image in seconds.

## Troubleshooting

- **If the app doesn't run:** Ensure all dependencies are installed and you are using Python 3.7 or higher.
- **If you encounter errors with image upload or processing:** Verify that the image is in JPEG format and properly uploaded.

## Additional Information

For more details on Streamlit, OpenCV, and NumPy, refer to their official documentation:

- [Streamlit Documentation](https://docs.streamlit.io/)
- [OpenCV Documentation](https://docs.opencv.org/)
- [NumPy Documentation](https://numpy.org/doc/)
