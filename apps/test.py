# Required Modules for DAS Implementation
from pyzbar.pyzbar import decode
# import gspread
import streamlit as st
from PIL import Image

 
# Decodes the QR code and directs to appropriate sub sheet
def app():
    def decoder(image):
        qrCode = decode(image) #decoded QR code
        print(qrCode)
        stat = 0
        for obj in qrCode:
            stat = 1
            barcodeData = obj.data.decode("utf-8")
            print("Required data ", barcodeData)
        else:
            if stat == 0:   # This if ladder is for overcoming a bug that's caused by for else
                st.error("No QR code has been detected or recognized; Take a new pic")
            elif stat == 1:
                stat = 0


    # Declaring empty variable for printing output messages
    message = st.empty()

    # Camera Input Setup
    startcam = st.camera_input('Scan QR Code')

    if startcam:
        img = Image.open(startcam)
        decoder(img)
