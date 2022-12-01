"""
    For on the spot registration for events
"""

from pymongo import *
import streamlit as st
from cryptography.fernet import Fernet
from datetime import datetime as dt
from dateutil.tz import gettz

usn = st.secrets["db_username"]
pwd = st.secrets["db_password"]
key = st.secrets["key"]
key = key.encode()
connection_str = f"mongodb+srv://{usn}:{pwd}@cluster0.ntw5wzk.mongodb.net/?retryWrites=true&w=majority"

cluster = MongoClient(connection_str)

db = cluster["events"]
collection = db["Open_House"]
fernet = Fernet(key)

def app():
    st.title("Sign Up Here")
    name = st.text_input("Enter Name: ", key = 1)
    roll_number = st.text_input("Enter Roll Number: ", key = 2)
    branch = st.text_input("Enter Branch:")
    section = st.text_input("Enter Section:")
    semester = st.text_input("Enter Semester:")
    hashed = roll_number.lower().encode("utf-8")
    hashed = fernet.encrypt(hashed)
    time = dt.now(tz=gettz('Asia/Kolkata'))
    time = time.strftime("%H:%M:%S")
    struct_data = {"name": name, "code" : hashed, "roll_number": roll_number, "branch": branch, "section": section, "sem" : semester, "attended?": True, "time": time}
    if st.button("Submit details"):
        try:
            collection.insert_one(struct_data)
            st.success("Person added successfully")
        except Exception as e:
            st.error("Error from DB side")
            print("Error", e)
