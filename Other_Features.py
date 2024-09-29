import streamlit as st
import re
from pdf2image import convert_from_bytes
import base64
from docx import Document

#Created a entity-unit map"""
entity_unit_map = {
    'width': {'centimetre', 'foot', 'inch', 'metre', 'millimetre', 'yard', 'cm', 'in'},
    'depth': {'centimetre', 'foot', 'inch', 'metre', 'millimetre', 'yard', 'cm', 'in'},
    'height': {'centimetre', 'foot', 'inch', 'metre', 'millimetre', 'yard', 'cm', 'in'},
    'item_weight': {'gram', 'kilogram', 'microgram', 'milligram', 'ounce', 'pound', 'ton', 'g', 'kg', 'mg', 'µg', 'oz', 'lb'},
    'maximum_weight_recommendation': {'gram', 'kilogram', 'microgram', 'milligram', 'ounce', 'pound', 'ton', 'g', 'kg', 'mg', 'µg', 'oz', 'lb'},
    'voltage': {'kilovolt', 'millivolt', 'volt'},
    'wattage': {'kilowatt', 'watt'},
    'item_volume': {'centilitre', 'cubic foot', 'cubic inch', 'cup', 'decilitre', 'fluid ounce', 'gallon', 'litre', 'millilitre', 'pint', 'quart'}
}
allowed_units = {unit for entity in entity_unit_map for unit in entity_unit_map[entity]}


#Funtion to match entity from text list"""
def match_entity_value(extracted_text, entity_name):
    relevant_units = entity_unit_map.get(entity_name, set())
    matched_values = []
    
    # Convert list to string if needed
    if isinstance(extracted_text, list):
        extracted_text = ' '.join(extracted_text)
    
    # Regex pattern to capture weights, including common abbreviations
    pattern = re.compile(r'(\d+(\.\d+)?\s*(g|kg|mg|µg|oz|lb))', re.IGNORECASE)
    
    # Find all matches in the extracted text
    matches = pattern.findall(extracted_text)
    
    # Use a set to track unique (value, unit) pairs
    seen_values = set()
    
    for match in matches:
        value, _, unit = match
        unit = unit.lower().strip()  # Ensure unit is in lowercase and stripped of whitespace
        if unit in relevant_units:
            if (value, unit) not in seen_values:
                seen_values.add((value, unit))
                # Append only the unique value and unit
                matched_values.append(f"{value} {unit}")
    
    # Handle special cases for width and height
    if entity_name.lower() == "width":
        return matched_values[0] if matched_values else "No matching found"
    elif entity_name.lower() == "height":
        return matched_values[1] if len(matched_values) > 1 else "No matching found"
    else:
        return matched_values[0] if matched_values else "No matching found"

    
#Function to convert PDF to images"""
def pdf_to_images(pdf_data):
    return convert_from_bytes(pdf_data)  # Returns list of PIL image

#Convert the PDF to a base64 string for embedding in an iframe"""
def show_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    
    # Embedding PDF in an iframe
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="800" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)


#Function to save extracted text into a .docx file"""
def save_text_as_docx(extracted_text, file_name='extracted_docx_files//textextracted.docx'):
    doc = Document()
    if extracted_text!=None:
        for line in extracted_text.splitlines():
            doc.add_paragraph(line)
        
        doc.save(file_name)
