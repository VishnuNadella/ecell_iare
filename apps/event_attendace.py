"""
    Here attendance for each and every new event will be taken and this will be made 
    accessible to all the Higher authorities and event organizers. 

    Here we will create a QR for all the ppl who have attended the event.
    and try to send a mail STMP.

    collect data from DB and create a csv file who have attended the event.
"""

# from PIL import Image
from pyzbar.pyzbar import decode
import streamlit as st
import csv
from PIL import Image
import os
from pymongo import *
from cryptography.fernet import Fernet

file_path = os.getcwd()
try:
    os.mkdir(os.path.join(file_path, f"Files"))
except:
    pass

def create_file():
    f_cnt = st.session_state["download_file_count"]
    req_str = f'./Files/participants.csv'
    f = open(req_str, 'w', newline='')
    header = ["name", "roll number", "branch", "section", "semester"]
    writer = csv.writer(f)
    writer.writerow(header)
    f.close()

def add_to_file(data):
    f_cnt = st.session_state["download_file_count"]
    req_str = f'./Files/participants.csv'
    f = open(req_str, 'a', newline='')
    writer = csv.writer(f)
    writer.writerow(data)
    f.close()

key = st.secrets["key"]
key = key.encode("utf-8")
fernet = Fernet(key)

usn = st.secrets["db_username"]
pwd = st.secrets["db_password"]

connection_str = f"mongodb+srv://{usn}:{pwd}@cluster0.ntw5wzk.mongodb.net/?retryWrites=true&w=majority"

cluster = MongoClient(connection_str)

db = cluster["events"]
collection = db["attendees"]

def fect_from_db():
    create_file()
    for file in collection.find():
        if file["attended?"]:
            name = file["name"]
            roll_number = file["roll_number"]
            branch = file["branch"]
            section = file["section"]
            sem = file["sem"]
            add_to_file([name, roll_number, branch, section, sem])
    return True

def app():
    def decoder(image):
        qrCode = decode(image) #decoded QR code
        stat = 0
        for obj in qrCode:
            stat = 1
            barcodeData = obj.data
            print("Required data ", barcodeData)
            if barcodeData:
                decrypter_cst(barcodeData)
        else:
            if stat == 0:   # This if ladder is for overcoming a bug that's caused by for else
                st.error("No QR code has been detected or recognized; Take a new pic")
            elif stat == 1:
                stat = 0
    if st.button("Get List"):
        st.success("Please wait until we fetch the data")
        if fect_from_db():
            req_str = st.session_state["download_file_count"]
            st.download_button("Download File", open(f"./Files/participants.csv", "r"), file_name = "Event_attendees.csv", mime = "text/csv")
            

    # Declaring empty variable for printing output messages
    message = st.empty()

    # Camera Input Setup
    startcam = st.camera_input('Scan QR Code')

    if startcam:
        img = Image.open(startcam)
        decoder(img)

def decrypter_cst(data):
    if len(data) > 0:
        decrypted = fernet.decrypt(data)
        rn, req_id = decrypted.decode().split("+")
        prsn = collection.find_one({ "roll_number": rn })
        if prsn != None:
            nme = prsn["name"]
            if prsn["attended?"] == False:
                collection.update_one({ "roll_number" : rn }, {"$set" : {"attended?" : True}})
                st.success(f"Welcome to T-Hub event {nme}, Enjoy your self")
            elif prsn["attended?"] == True:
                st.warning(f"Person {nme} has already been authenticated")
        elif prsn == None:
            st.error("Person dosent exist")
