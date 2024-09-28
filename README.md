# **TextExtractify 📄🔍**
TextExtractify is a cutting-edge application designed to extract text from images and PDFs using powerful OCR technologies. With Azure OCR and EasyOCR at its core, TextExtractify offers a streamlined experience for users across different roles—whether you’re a free user or a premium subscriber looking for advanced features like PDF conversion and text extraction to .docx.

## Demo 🎥
https://github.com/user-attachments/assets/b3432af0-8f2e-43b5-814d-fda2723a8f46
## 🚀 Features
### 🔑 Free User Features:
* Single Image Upload: Upload an image to extract text using Azure OCR or EasyOCR.
* Text Entity Extraction: Detect entities within the extracted text for structured information.
* Basic PDF Processing: Convert and extract text from PDFs.
### 💼 Premium User Features:
* Batch Image Upload: Upload and process multiple images in one go.
* PDF to Text Conversion: Extract text from PDFs and convert it to .docx format.
* Download .docx Files: Each extracted text from images and PDFs can be downloaded as a .docx document.
* Optimized for Performance: Faster extraction time and priority access to new features.
### 🔥 Coming Soon:
* Multiple Language Support: Translate extracted text into various languages.
* Additional File Format Support: Expand beyond PDFs to Word, Excel, and other document types.
## 💡 How It Works
1. Upload Files: Users can upload image or PDF files from their system.
2. Choose OCR Engine: Select either Azure OCR or EasyOCR for processing.
3. Extract & Display: The app extracts text and displays it on the result page.
4. Download Options: Free users can copy or view the text, while premium users can download .docx files or process multiple images in one go.
## 🎨 User Interface
TextExtractify has a modern and responsive UI designed for a seamless user experience. The interface adapts to different devices and ensures smooth navigation for both free and premium users.

### Screenshots

**1. Login Page:**

   ![Login Page](https://github.com/user-attachments/assets/b7b2a81b-4c92-4cb2-b071-823eb4bb9172)

**2. Signup Page:**
  
  ![SignUp Page](https://github.com/user-attachments/assets/44fc4f2d-688c-47bf-b1d6-538a82de852e)

**3. Home Page:**

  ![Home Page](https://github.com/user-attachments/assets/4279c830-7423-4570-834c-a180115ee1fa)

**4. Free User Features**

![Free Features](https://github.com/user-attachments/assets/65f7f004-3387-44d0-ab51-6103729f754f)

**5. Premium User PDF View:**
  
  ![Premium PDF](https://github.com/user-attachments/assets/24963b86-8d75-40fa-aed8-f1f7e338c942)


## 🛠️ Tech Stack
### Backend:
* Python: Core language for all processing.
* Azure OCR / EasyOCR: OCR engines for text extraction.
* Streamlit: Web framework for creating interactive UIs.
* Pillow: For image handling.
### Frontend:
* HTML/CSS: For custom designs and styling.
### Database:
* Json: Used for managing user authentication and subscription data.
## 🧑‍💻 Installation & Setup
### Requirements:
* Python 3.7+
* Azure OCR API Key (for Azure OCR functionality)
### Instructions:
#### 1. Clone the repository:

* git clone https://github.com/Anant2003jain/TextExtractify.git

* cd TextExtractify

#### 2. Install the required packages:

* pip install -r requirements.txt
  
#### 3. Set up environment variables for Azure OCR:

* export AZURE_OCR_KEY=your_key_here
* export AZURE_OCR_ENDPOINT=your_endpoint_here
#### 4. Run the application:

* python -m streamlit run textex_app.py

* Visit http://localhost:8501 in your browser.

## 🔐 User Roles
* Free Users: Access basic OCR and text extraction features.
* Premium Users: Unlock advanced functionalities like batch image processing and downloadable .docx files.
## 🎯 Future Roadmap
* AI-powered Translations: Expanding language detection and translation capabilities.
* Improved Performance: Reducing processing time for large PDFs and image batches.
## 📝 License
* This project is licensed under the MIT License - see the [LICENSE](https://github.com/Anant2003jain/TextExtractify/blob/main/LICENSE) file for details.

## 🤝 Contributing
We welcome contributions from the community! To contribute:

1. Fork the repo.
2. Create your feature branch: git checkout -b feature/your-feature.
3. Commit your changes: git commit -m 'Add feature'.
4. Push to the branch: git push origin feature/your-feature.
5. Open a pull request.
## 🌟 Acknowledgements
* Azure OCR for their comprehensive OCR API.
* EasyOCR for providing a flexible open-source OCR solution.
* Streamlit for making app deployment seamless.
