"""
Main navigating page for Everyone
"""
LOGO_adr = "./apps/resources/ecell_logo.png"


import streamlit as st
st.set_page_config(page_title = "E - Cell", page_icon = LOGO_adr, initial_sidebar_state = 'auto')
from Main import router
from apps import home, login, attendance, engage, admin, leads_portal, logout, profile, signup, event_attendace, test, spot
import bcrypt as bc
data = None



app = router()

st.markdown("""
# E - Cell
""")

st.sidebar.image(LOGO_adr)
st.sidebar.markdown(
    """<div style="text-align:center"><strong>E - Cell</strong><br><br></div>""", unsafe_allow_html=True)

st.sidebar.markdown(
     '''<br><br><div style="text-align: center"><small>Developed by Vishnu Nadella for E - Cell | Oct 2022 </small></div>''', unsafe_allow_html=True)


app.add_app("home", home.app)
app.add_app("Sign Up", signup.app)
app.add_app("Log In", login.auth)



salt = bc.gensalt()

if "member_det" not in st.session_state:
    st.session_state["member_det"] = None
    st.session_state["Status"] = None
    st.session_state["Message"] = None
    st.session_state["download_file_count"] = 0


if "logout" in st.session_state:
    try:
        app.remove_app("Log Out", logout.app)
        app.remove_app("Profile", profile.app)
    except:
        del st.session_state["logout"]
if st.session_state["Status"] == False:
    st.error(st.session_state["Message"])
elif st.session_state["Status"] == True:
    app.remove_app("Log In", login.auth)
    app.remove_app("Sign Up", signup.app)
    app.add_app("Profile", profile.app)
    if st.session_state["member_det"]["admin"]["admin?"] == True:
        app.add_app("Admin", admin.app)
        app.add_app("Event Attendance", event_attendace.app)
        # app.add_app("Test", test.app)
        app.add_app("On the Spot", spot.app)
    if st.session_state["member_det"]["engage"]["member?"] == True:
        # get data ki whether the person is a learner or head / co head
        eng = st.session_state["member_det"]["engage"]
        hd_cohd = eng["pos"]
        if hd_cohd == "head" or hd_cohd == "cohead":
            app.add_app("Attendance", attendance.app)
            app.add_app("Engage Portal", leads_portal.app)
        app.add_app("Engage", engage.app)
    app.add_app("Log Out", logout.app)
    

app.run()
