"""
Allocation of QR code and logging of details will take place here
"""
import streamlit as st
import bcrypt as bc
from cryptography.fernet import Fernet
from pymongo import *

usn = st.secrets["db_username"]
pwd = st.secrets["db_password"]

connection_str = f"mongodb+srv://{usn}:{pwd}@cluster0.ntw5wzk.mongodb.net/?retryWrites=true&w=majority"

cluster = MongoClient(connection_str)

db = cluster["people"]
collection = db["members"]


salt = bc.gensalt(rounds = 9)
# key = Fernet.generate_key()
key = st.secrets["key"]
key = key.encode("utf-8")

fernet = Fernet(key)

def app():
    st.title("Sign Up Here")
    user_name = st.text_input("Enter Name: ", key = 1)
    roll_number = st.text_input("Enter Roll Number: ", key = 2)
    mail_id = st.text_input("Enter Domain Mail ID: ", key = 3)
    pwd = st.text_input("Enter Password: ", type = "password", key = 4)
    cfm_pwd = st.text_input("Confirm Password: ", type = "password", key = 5)
    rn_part, rest_part = None, None
    if mail_id:
        # first check whether person with the mail id exists or not
        person_check = collection.find_one({"roll_number": roll_number})
        rn_part, rest_part = mail_id.lower().split("@")
    if roll_number != None:
        if (roll_number.lower() == rn_part.lower()) and (len(roll_number) == 10) and (rest_part == "iare.ac.in") and person_check == None: # add students list if possible for better authentication
            if pwd == cfm_pwd and len(pwd) >= 8:
                req_pwd = str(pwd).encode('utf-8')
                hashed = bc.hashpw(req_pwd, salt)
                # push all the data to the database
            elif len(pwd) == 0 and len(cfm_pwd) == 0:
                pass
            else:
                st.error("Passwords do not match") 
        elif len(mail_id) == 0:
            pass
        else:
            print(rn_part, rest_part, roll_number, person_check)
            st.error("Invalid Email ID, PLease use your domain mail id")
    if st.button("Submit"):
        # Push data to the database
        try:
            struct_data = {"user_name": user_name, "roll_number" : roll_number, "mail_id": mail_id, "password" : hashed, "hashed_qr" : "", "admin": { "admin?": False, "pos" : None, "resp" : None}, "engage": { "member?" : False, "domain" : None, "pos" : None, "attended_cnt" : 0}}
            collection.insert_one(struct_data)
            req_det = collection.find_one({"roll_number": roll_number})
            req_id = req_det["_id"]
            req_data_str = f"{roll_number}+{req_id}"
            # req_str = req_data_str.encode("utf-8")
            # hashed_str = bc.hashpw(req_str, salt)
            hashed_str = fernet.encrypt(req_data_str.encode())
            # print("\n\n\n---------Hashed QR", hashed_str)
            collection.update_one({"_id" : req_id}, {"$set" : {"hashed_qr" : hashed_str}})
            st.success("Successfully registered, Now please login")
        except Exception as e:
            print("\n\nError", e)
            st.error("Cannot able to add user please try again later") 
