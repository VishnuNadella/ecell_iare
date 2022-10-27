"""
Authentication page for selected pages
"""


import streamlit as st

def app():
    # del st.session_state["roll_number"]
    del st.session_state["member_det"]
    del st.session_state["Status"]
    # del st.session_state["Name"]
    # del st.session_state["Message"]
    # del st.session_state["admin"]
    # del st.session_state["engage"]
    # del st.session_state["engage_position"]
    st.session_state["logout"] = True
    st.success("Logged out successfully")

