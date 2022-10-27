"""
It is for the heads and co heads who will have access to upload course material, ### v:2.0 = and can also view who all are taking part in the program.
"""

import streamlit as st
from pymongo import *

usn = st.secrets["db_username"]
pwd = st.secrets["db_password"]

connection_str = f"mongodb+srv://{usn}:{pwd}@cluster0.ntw5wzk.mongodb.net/?retryWrites=true&w=majority"
cluster = MongoClient(connection_str)

db = cluster["people"]
collection = db["members"]

course_db = cluster["resources_engage"]


def app():
    if st.button("View Course Attendees"):
        req_det = st.session_state["member_det"]["engage"]
        # all_team_mems = [i for i in collection.find({}, {"engage": {"domain": req_det["domain"]}})]
        # print("\n\n\nTeam members list:", all_team_mems)

        req_db_file = dict()
        # print("\n\n\n----------------Memebers-----------")
        for i in collection.find():
            if i["engage"]["member?"] == True and i["engage"]["domain"] == st.session_state["member_det"]["engage"]["domain"] and i["roll_number"] != st.session_state["member_det"]["roll_number"]:
                # st.text(i)
                # print(i)
                req_db_file[i["user_name"]] = i["engage"]
        # print("\n\n---------Files---------\n\n", req_db_file)
        for mem_name, mem_data in req_db_file.items():
            req_fin_str = mem_name.capitalize() + " has attended " + str(mem_data["attended_cnt"]) + " classes"
            st.text(req_fin_str)
        # all_team_mems = [i["_id"] for i in collection.find({"admin": {"pos" : "CR"}})]
    # if st.button("Upload Course Content"):
    course_collection = course_db[st.session_state["member_det"]["engage"]["domain"]]
    week_no = st.text_input("Enter Week Number")
    topic = st.text_input("Enter Topic")
    link = st.text_input("Enter link (Can be a Docs Link or Drive Folder link)")
    if st.button("Enter data"):
        try:
            db_entry_struct = {"week_no" : week_no, "Topic" : topic, "link": link} # Link to a google doc with links or course material folder link.
            course_collection.insert_one(db_entry_struct)
            st.success("Successfully uploaded data")
        except Exception as e:
            print("\n\n", e)
            st.error("Cannot connect to DB please try again later")