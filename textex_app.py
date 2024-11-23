#To run: python -m streamlit run textex_app.py

#Import Libraries
import streamlit as st
import json
from PIL import Image

#Load funions from scripts
from Authentication import login,logout,register
from OCR import extract_text_from_image_easyocr,extract_text_from_image,extract_text_from_pdf_pages
from Other_Features import match_entity_value,pdf_to_images,show_pdf,save_text_as_docx

#Load user data"""
with open('users.json', 'r') as file:
    user_data = json.load(file)

#Function to display the main interface for the app"""
def main():
    # Set page title and favicon
    st.set_page_config(
        page_title="TextExtractify",
        page_icon="te_logo.png",
        layout="centered",
        initial_sidebar_state="auto"
    )

    # Custom CSS for enhancing the look
    st.markdown("""
        <style>
        /* Sidebar styling */
        .sidebar .sidebar-content {
            background-color: #f0f2f6;
            padding: 20px;
            border-radius: 10px;
        }
        .footer {
            text-align: center;
            font-size: 14px;
            color: #555;
            padding: 20px;
            border-top: 1px solid #ddd;
        }
        /* Button hover effects */
        .stButton button {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 10px 24px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            transition-duration: 0.4s;
            cursor: pointer;
        }
        .stButton button:hover {
            background-color: #45a049;
            color: white;
        }
        /* Progress spinner */
        .spinner {
            display: flex;
            justify-content: center;
            align-items: center;
        }
        </style>
    """, unsafe_allow_html=True)

    # Load an image from file
    logo_image = Image.open('te_logo.png')

    col1, col2 = st.columns([3, 1])

    with col1:
        st.title("TextExtractify")      # Title and subtitle
        st.subheader("Extract text from Images or PDFs with ease")

    with col2:
        st.image(logo_image, use_container_width=True)


    uploaded_file = None

    # Sidebar with sections organized in expanders
    with st.sidebar:
        st.sidebar.header(f"Welcome, {st.session_state.get('userid', 'Guest')}!")
        
        # Login or logout options
        if not st.session_state.get('logged_in', False):
            choice = st.radio("Login or Signup", ["Login", "Signup"])
            if choice == "Login":
                login(user_data)

            elif choice == "Signup":
                register(user_data)
        else:
            if st.button("Logout"):
                logout()
        
            if st.session_state.logged_in:
                with st.expander("Upload & Extract"):
                    uploaded_file = st.file_uploader("Upload an image or PDF", type=["jpeg", "png", "jpg", "pdf"])

                    # Restrict OCR model choices based on user plan
                    if st.session_state.user_plan == 'premium':
                        model_choice = st.sidebar.selectbox("Choose OCR Model", ("Azure OCR (Premium)","EasyOCR (Free)"))
                    else:
                        model_choice = st.sidebar.selectbox("Choose OCR Model", ("EasyOCR (Free)",))
                
                with st.expander("Settings"):
                    entity_name = st.selectbox(
                        "Entity Extraction (Optional)",
                        ['None', 'width', 'height', 'item_weight']
                    )

                if st.session_state.user_plan != 'premium':
                    st.write("# Buy Premium and get:")
                    st.write("Unlimited PDF extraction, Powerful Azure OCR model, Easy .docx extraction")
                    st.button("Buy Premium", on_click=buy_premium)

    # Ensure this block only runs after user is logged in and a file is uploaded
    if st.session_state.get('logged_in', False):
        if uploaded_file: 
             # Handle PDF upload (Premium users only)
            if uploaded_file.type in ["application/pdf"]:
                if st.session_state.user_plan == 'premium':
                    st.text("Uploaded PDF")
                    with open("PDFs To Preview//temp_uploaded_file.pdf", "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    # Preview the PDF
                    show_pdf("PDFs To Preview//temp_uploaded_file.pdf")
                    # Convert PDF to images and process
                    pdf_images = pdf_to_images(uploaded_file.read())
                    if st.button("Extract Text"):
                        st.write("Processing PDF...")
                        with st.spinner("Extracting text..."):
                            extracted_text = extract_text_from_pdf_pages(pdf_images,model_choice)
                    
                        if extracted_text:
                            st.write("#### Extracted Text from PDF:")
                            st.text_area("Extracted Text", value=extracted_text, height=300, label_visibility="collapsed")
                            #st.text_area("Extracted Text:", extracted_text, height=300)

                            if entity_name != 'None':
                                st.write("Extracting specific entity...")
                                matched_value = match_entity_value(extracted_text, entity_name)
                                st.write("#### Matched Entity:")
                                st.text(matched_value)

                            # Save the extracted text as .docx and provide download option
                            save_text_as_docx(extracted_text)
                            st.success("Text saved and ready for download.")
                            with open("extracted_docx_files//textextracted.docx", "rb") as file:
                                st.download_button(label="Download .docx",
                                                data=file,
                                                file_name="textextracted.docx",
                                                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
                        else:
                            st.error("Failed to extract text from the PDF.")
                else:
                    st.warning("PDF extraction is available only for premium users. Please upgrade to access this feature.")

            elif uploaded_file.type in ["image/jpeg", "image/png", "image/jpg"]:
                st.text("Uploaded Image")
                st.image(uploaded_file, use_container_width=True)
                if st.button("Extract Text"):
                    with st.spinner("Extracting text..."):
                        if st.session_state.user_plan == 'premium' and model_choice=="Azure OCR (Premium)":
                            extracted_text = extract_text_from_image(uploaded_file.read())
                        else:
                            extracted_text = extract_text_from_image_easyocr(uploaded_file.read())

                    st.write("#### Extracted Text:")
                    st.text_area("", extracted_text, height=300)

                    # Option to save text as docx
                    if st.session_state.get('user_plan') == 'premium':
                            save_text_as_docx(extracted_text)
                            st.success("Text saved and ready for download.")
                            with open("extracted_docx_files//textextracted.docx", "rb") as file:
                                st.download_button(label="Download .docx",
                                               data=file,
                                               file_name="textextracted.docx",
                                               mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")

                    if entity_name != 'None':
                            st.write("Extracting specific entity...")
                            matched_value = match_entity_value(extracted_text, entity_name)
                            st.write("#### Matched Entity:")
                            st.text(matched_value)
            else:
                st.error("Please upload a valid image file (JPEG, PNG)")
    else:
        st.write("Please log in to upload files and extract text.")

    # Footer
    st.markdown("""
        <div class="footer">
            <p>Powered by TextExtractify © 2024<br>Created by Anant Jain<br>Connect with me on 
            <a href="https://www.linkedin.com/in/anant-jain-1720671a7" target="_blank">LinkedIn</a></p>
        </div>
    """, unsafe_allow_html=True)


def save_user_data_main():
    with open('users.json', 'w') as file:
        json.dump(user_data, file, indent=4)

#Function for premium purchase (just an example implementation)
def buy_premium():
    username = st.session_state.current_user
    if username and user_data.get(username):
        user_data[username]['access_level'] = 'premium'
        save_user_data_main()
        st.session_state.user_plan = 'premium'
        st.success("Congratulations! You are now a premium user.")
    else:
        st.error("An error occurred while upgrading your plan.")

# Main execution
if __name__ == "__main__":
    main()