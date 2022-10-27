
"""
People can view their info and QR as well
"""

import streamlit as st
import bcrypt as bc
# from qrcode import QRCode
import qrcode
from time import sleep

salt = bc.gensalt(rounds = 9)

def create_qr(qr_str):
    # qr = QRCode()
    # qr.add_data(qr_str)
    # qr.make()
    # qr.best_mask_pattern()
    # qr.best_fit()
    # req_qr = qr.make_image(fill_color = "white", back_color = "black")

    # req_qr.save("./apps/resources/person_qr.png")
    # sleep(5)
    img = qrcode.make(qr_str)
    img.save("./apps/resources/person_qr.png")
    if st.button("Show QR Code"):
        st.image("./apps/resources/person_qr.png")


def app():
    person_det = st.session_state["member_det"]
    name = person_det["user_name"]
    # print(type(person_det), person_det["roll_number"])
    qr_str = person_det["hashed_qr"]
    st.subheader(f"Welcome {name.capitalize()}")
    create_qr(qr_str)
