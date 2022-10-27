"""
Here data such as 
    Name,
    In which Engage program they are in, 
    Course Material, 
    Attendance will be made available and number of sessions attended. (ONLY THE COUNT)
"""
import streamlit as st
from pymongo import *

usn = st.secrets["db_username"]
pwd = st.secrets["db_password"]

connection_str = f"mongodb+srv://{usn}:{pwd}@cluster0.ntw5wzk.mongodb.net/?retryWrites=true&w=majority"
cluster = MongoClient(connection_str)

course_db = cluster["resources_engage"]



def app():
    titles = {"aiml" : "AI ML", "web" : "Web Application Development", "app" : "Mobile Application Development", "business" : "Business and Finance", "design" : "Designer", "marketing" : "Marketing", "cyber" : "Cyber Security"}
    name = st.session_state["member_det"]["user_name"]
    course_title = st.session_state["member_det"]["engage"]["domain"]
    req_title_to_display = titles[course_title]
    course_collection = course_db[course_title]
    
    attendance = st.session_state["member_det"]["engage"]["attended_cnt"]
    st.title(f"Welcome {name}")
    for i in course_collection.find():
        # print(i)
        req_data = " ".join(["Week:", i["week_no"], i["Topic"], i["link"]])
        
        st.info(req_data)
