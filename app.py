#!/bin/env python3
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
from runsql import *
from io import  BytesIO
import  xlsxwriter
creatTable_user()
creatTable_report()

st.set_page_config(page_title='Report Now',
                   layout='wide',
                   initial_sidebar_state='expanded')

header_mid = st.empty()
if "page" not in st.session_state:
    st.session_state.page = 0
# @st.cache
if "permistion" not in st.session_state:
    st.session_state.permistion = 0

def loginuser(username,password):
    user_permistion = login(username,password)
    print(f'Login {user_permistion}')
    if user_permistion:
        st.session_state.permistion = 1
        st.write(f"wellcome back {username}")

    else:
        to_page0()
        st.write("Try again!!!")
def to_page0():
    header_mid.empty()
    st.session_state.page = 0    # Login
def to_page1():
    header_mid.empty()
    if st.session_state.permistion:
        st.session_state.page = 1    # Insert Report
    else:
        st.error("Please Login Or Create Your Account")
        to_page0()
def to_page2():
    header_mid.empty()
    if st.session_state.permistion:
        st.session_state.page = 2    # Read report
    else:
        st.error("Please Login Or Create Your Account")
        to_page0()
def to_page3():
    header_mid.empty()
    st.session_state.page = 3    # Add user

with st.sidebar:
    selected = option_menu(menu_title=None,
                           options=["Login","Write Report", "Read Report","Add User"],
                           icons=["man","house", "book", "envelope"],
                           menu_icon="cast",
                           default_index=0,
                           # orientation="horizontal"
                           )
    if selected == "Login":
        to_page0()
    if selected == "Write Report":
        to_page1()
    if selected == "Read Report":
        to_page2()
    if selected == "Add User":
        to_page3()

def insertdb(topic,detail,result):
    insert(topic,detail,result)
    to_page1()

if st.session_state.page == 0:
    with header_mid.form(key="Login",clear_on_submit=True):
        username = st.text_input("User name", value="",key='unamelogin')
        password = st.text_input ("Password",value="", type="password", key='passlogin')
        if st.form_submit_button("Login"):loginuser(username,password)

if st.session_state.page == 1:
    with header_mid.form(key="report",clear_on_submit=True):
        topic = st.text_input("Topic", value="",key="topic")
        detail = st.text_input("Detail", value="",key="detail")
        result = st.text_input("Result", value="", key="result")
        if st.form_submit_button("Save"):insert(topic,detail,result)

if st.session_state.page == 2:
    with header_mid.container():
        df = readAllDb()
        header_mid.dataframe(df)
        output = BytesIO()
    if st.button("EXport to exccel"):

        writer = pd.ExcelWriter(output,engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Sheet1')
        writer.close()
        xlsx_data = output.getvalue()

        st.download_button(label='📥 Download Current Result',
                           data=xlsx_data,
                           file_name= "report.xlsx",
                           mime="application/vnd.ms-excel")

if st.session_state.page == 3:

    with header_mid.form(key="insertuser",clear_on_submit=True):
        fname = st.text_input("First Name", value="",key="fname")
        lname = st.text_input("Last Name", value="",key="lname")
        email = st.text_input("Email", value="", key="email")
        uname = st.text_input("Login Name", value="", key="uname")
        pwd = st.text_input("Password", value="", key="password")
        if st.form_submit_button("Save"):insertUserDB(fname,lname,email,uname,pwd)
