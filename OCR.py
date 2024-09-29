import streamlit as st
import time
import os
import json
from io import BytesIO
from PIL import Image
import easyocr
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials

#Load Azure credentials
with open('azure_cred.json', 'r') as config_file:
    config_data = json.load(config_file)
Endpoint = config_data['endpoint']
Key = config_data['api_key']
credential = CognitiveServicesCredentials(Key)
client = ComputerVisionClient(endpoint=Endpoint, credentials=credential)

#Function to extract text from image using Azure"""
def extract_text_from_image(image_data):
    try:
        # Show progress bar for Azure OCR
        progress = st.progress(0)
        for i in range(11):
            time.sleep(0.1)
            progress.progress(i * 10)

        # Send image data to Azure OCR
        rawHttpResponse = client.read_in_stream(BytesIO(image_data), language="en", raw=True)
        operationLocation = rawHttpResponse.headers["Operation-Location"]
        operationId = operationLocation.split('/')[-1]

        # Wait for the operation to complete
        while True:
            result = client.get_read_result(operationId)
            if result.status not in ['notStarted', 'running']:
                break
            time.sleep(1)
            progress.progress(100)

        # Extract the text from the results
        extracted_text = []
        if result.status == OperationStatusCodes.succeeded:
            for line in result.analyze_result.read_results[0].lines:
                extracted_text.append(line.text)

        return " ".join(extracted_text)

    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

#Function to extract text using EasyOCR"""
def extract_text_from_image_easyocr(image_data):
    try:
        model_storage_directory = 'model/'

        # Check if the directory exists, if not, create it
        if not os.path.exists(model_storage_directory):
            os.makedirs(model_storage_directory)

        # Initialize the reader
        reader = easyocr.Reader(['en'], model_storage_directory=model_storage_directory)

        # Show progress bar for EasyOCR
        progress = st.progress(0)
        for i in range(11):
            time.sleep(0.1)
            progress.progress(i * 10)

        # Convert the image data to a format EasyOCR can handle
        image = Image.open(BytesIO(image_data))
        image = image.convert('RGB')  # Ensure the image is in RGB mode
        
        # Convert the PIL Image to bytes
        with BytesIO() as buffer:
            image.save(buffer, format='PNG')
            image_bytes = buffer.getvalue()
        
        # Use EasyOCR to read text from the image bytes
        result = reader.readtext(image_bytes)
        extracted_text = [text[1] for text in result]
        return " ".join(extracted_text)
    
    except Exception as e:
        st.error(f"EasyOCR Error: {str(e)}")
        return None

#Extract text from each image page"""
def extract_text_from_pdf_pages(pdf_images,model_choices):
    extracted_text = []
    for page_num, image in enumerate(pdf_images,):
        st.write(f"Extracting text from page {page_num + 1}...")
        with BytesIO() as buffer:
            image.save(buffer, format='PNG')
            image_bytes = buffer.getvalue()
        
        # Call the Azure OCR extraction function here for each page
        #page_text = extract_text_from_image(image_bytes)
        if st.session_state.user_plan == 'premium' and model_choices=="Azure OCR (Premium)":
            page_text = extract_text_from_image(image_bytes)
        else:
            page_text = extract_text_from_image_easyocr(image_bytes)
        if page_text:
            extracted_text.append(f"Page {page_num + 1}:\n" + page_text)
    
    return "\n\n".join(extracted_text)