"""
Here attendance will be taken and made available only to the engage heads and co heads

Here attendance will be taken for each offline session and a csv file will be made available
and the same can be submitted to the faculty
this pdf has to be stored locally.
"""

import streamlit as st
from PIL import Image
from pyzbar.pyzbar import decode
from pymongo import *
from time import sleep


def decoder(image):
    print("Inside of decoder")
    qrCode = decode(image) #decoded QR code
    for obj in qrCode:
        data = obj.data.decode("utf-8")
        return data

def capture():
    message = st.empty()
    # Camera Input Setup
    startcam = st.camera_input('Scan QR Code')
    if startcam:
        img = Image.open(startcam)
        data = decoder(img)
        print(f"This is the scanned data: {data}")
        

def app():
    st.title("QR Code Scanner")
    st.subheader("Scan the person's QR code")
    cap1 = capture()
    sleep(3)
    print("Cap 1", cap1)
        