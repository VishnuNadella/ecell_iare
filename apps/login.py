"""
This page is for everyone and everyone will get redirected to respective places

E-cell members and admins and engage prog members will get split
Have to use domain ids / roll numbers
"""

import streamlit as st
from pymongo import *
import bcrypt as bc


salt = bc.gensalt()



usn = st.secrets["db_username"]
pwd = st.secrets["db_password"]

connection_str = f"mongodb+srv://{usn}:{pwd}@cluster0.ntw5wzk.mongodb.net/?retryWrites=true&w=majority"
# print(connection_str)
cluster = MongoClient(connection_str)

db = cluster["people"]
collection = db["members"]

def auth():
    roll_number = st.text_input('Roll Number', key = 1)
    password = st.text_input('Password', type = "password", key = 2)
    required_person = collection.find_one({"roll_number" : roll_number})
    if st.button("Log In"):
        # print(required_person)
        if "Name" not in st.session_state:
            st.session_state["member_det"]
        
        if required_person != None:
            # get password from the database.
            pwd_db = required_person["password"] # collect hashed password from the db
            # print(pwd_db)
            admin = required_person["admin"]["admin?"] # collect boolean value from DB
            engage = required_person["engage"]["member?"] # Collect details from DB, the one who are not part of it will have null data in them.
            password = password.encode('utf-8')
            if bc.checkpw(password, pwd_db):
                # name = required_person["user_name"]
                # admin_det = required_person["admin"] # collect all_details value from DB
                # engage_det = required_person["engage"]
                # st.session_state["Name"] = name
                # st.session_state["roll_number"] = roll_number
                st.session_state["Status"] = True
                # st.session_state["admin"] = admin
                # st.session_state["admin_det"] = admin_det
                # st.session_state["engage"] = engage
                # st.session_state["engage_det"] = engage_det
                st.session_state["member_det"] = required_person
                st.success("You have successfully logged in!")

            else:
                st.session_state["Status"] = False
                st.session_state["Message"] = "Incorrect Password, Please try again"
        else:
            st.session_state["Status"] = False
            st.session_state["Message"] = f"User with roll number: {roll_number} dosen't exist. Please signin"
            
        