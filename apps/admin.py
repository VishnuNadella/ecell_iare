"""
Here Name, responsibilities, team members, V2.0: Should be able to edit DB in realtime
"""
from tkinter import font
import streamlit as st
from pymongo import *

usn = st.secrets["db_username"]
pwd = st.secrets["db_password"]

connection_str = f"mongodb+srv://{usn}:{pwd}@cluster0.ntw5wzk.mongodb.net/?retryWrites=true&w=majority"
cluster = MongoClient(connection_str)

db = cluster["people"]
collection = db["members"]




def app():
    name = st.session_state["member_det"]["user_name"]
    req_db_file = dict()
    for i in collection.find():
        if i["admin"]["admin?"] == True and i["admin"]["pos"] == st.session_state["member_det"]["admin"]["pos"] and i["roll_number"] != st.session_state["member_det"]["roll_number"]:
            req_db_file[i["user_name"]] = i["admin"]
    # print("\n\n\nThis is the final File", req_db_file)

    
    # st.text(mem_name)
    # st.text(req_db_file)
    
    st.subheader(f"Welcome {name.capitalize()}")
    st.write("Team Members:")
    for mem_name, mem_data in req_db_file.items():
        req_fin_str = mem_name.capitalize() + " : " + mem_data["resp"]
        st.text(req_fin_str)