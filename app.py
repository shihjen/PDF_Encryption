# import modules
import os
import json
from io import BytesIO
import streamlit as st
from streamlit_lottie import st_lottie
from pypdf import PdfReader, PdfWriter

# Streamlit page configuration
st.set_page_config(page_title='PDF Encryption',
                   page_icon=None,
                   layout='centered',
                   initial_sidebar_state='auto')

st.title('PDF Encryption')

# lottie animation
with open('assets/images/lottie_cover.json','r') as f:
    lottie_cover = json.load(f)

st_lottie(animation_source = lottie_cover,
          speed = 0.5,
          reverse = False,
          loop = True,
          height = 500)

# description of the application
multi = '''
This Streamlit application enables users to encrypt PDF files securely using AES-256 encryption. 
Simply upload a PDF, enter a passkey, and download the encrypted file.
'''

st.markdown(multi)

# Streamlit UI - File Uploader
uploaded_file = st.file_uploader(label = 'Upload A PDF File',
                                 accept_multiple_files = False,
                                 type = ['.pdf'])

# Streamlit UI - file encryption
if uploaded_file:
    # check if uploaded file has been encrypted
    reader = PdfReader(uploaded_file)
    if reader.is_encrypted:
        st.warning('Uploaded file has been encrypted!')
    else:
        try:     
            password = st.text_input(label='Enter A Passkey',
                                    type = 'password',
                                    placeholder='Enter a passkey to encrypt the PDF file.')
            
            writer = PdfWriter(clone_from = uploaded_file)
            writer.encrypt(password, algorithm='AES-256')

            buffer = BytesIO()
            writer.write(buffer)

            if password:
                st.download_button(
                    label = 'Download Encrypted File',
                    data = buffer,
                    file_name = 'encrypted_pdf.pdf',
                    mime = 'application/pdf'
                )
        except Exception as e:
            st.error(f'An error occured: {e}')