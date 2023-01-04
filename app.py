#!/bin/env python3
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
from io import  BytesIO
import sqlite3
import hashlib
from datetime import datetime

db = 'report.db'
con = sqlite3.connect(db)
cur = con.cursor()

st.set_page_config(page_title='Report Now',
                   layout='wide',
                   initial_sidebar_state='expanded')

def creatTable_user():
    try :
        cur.execute("""
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY,
            fname VARCHAR(255) NOT NULL,
            lname VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            uname VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL
            )
        """)
        print('Create Table User ')
    except Exception as e:
        print(e)

def creatTable_report():
    try :
        cur.execute("""
        CREATE TABLE IF NOT EXISTS report (
            id INTEGER PRIMARY KEY,
            date VARCHAR(255) NOT NULL,
            time VARCHAR(255) NOT NULL,
            topic TEXT NOT NULL,
            detail TEXT NOT NULL,
            result TEXT NOT NULL,
            uname VARCHAR(255) NOT NULL
            )
        """)
    except Exception as e:
        print(e)

#---------------------- Insert User ------------------------------
def insertUserDB(fname, lname, email, uname, password):
    try :
        passwd = hashlib.sha256(password.encode()).hexdigest()
        cur.execute("INSERT INTO user (fname, lname, email, uname, password)VALUES (?,?,?,?,?)", \
                    (fname, lname, email, uname, passwd))

        con.commit()
        print("Insert user Success")
    except Exception as e:
        print(e)

#---------------------- Insert data ------------------------------
def insertReport(ddate, ttime, topic, detail, result, uname):
    try :
        cur.execute("INSERT INTO report (date, time, topic, detail, result, "
                    "uname)VALUES (?,?,?,?,?,?)", \
                    (ddate, ttime, topic, detail, result, uname))

        con.commit()
        print(ddate, ttime, topic, detail, result,uname)
        print("Success")
    except Exception as e:
        print(e)

def insert(topic,detail,result):
    try:
        dt = datetime.now()
        ddate1 = dt.strftime("%Y-%m-%d")
        ddate = ddate1
        ttime1 = dt.strftime("%H:%M:%S")
        ttime = ttime1
        insertReport(ddate,ttime,topic,detail,result,st.session_state.user)
    except Exception as e:
        print(e)

creatTable_user()
creatTable_report()

header_mid = st.empty()
if "page" not in st.session_state:
    st.session_state.page = 0
# @st.cache
if "permistion" not in st.session_state:
    st.session_state.permistion = 0

def loginuser(username,password1):
    # global user
    st.session_state.user = username
    password = hashlib.sha256(password1.encode()).hexdigest()
    cur.execute("SELECT * FROM user WHERE uname=? AND password=?",(st.session_state.user,password))
    if cur.fetchall():
        st.session_state.permistion = 1
        st.info(f"wellcome back {st.session_state.user}")
        return True
    else:
        st.info("Missing!!! Try again")
        return False

def readAlluser():
    try:
        sql = """SELECT * FROM user"""
        res = cur.execute(sql)
        # for row in res:
        #     print(row[0],row[1],row[2],row[3],row[4])
        df = pd.DataFrame(res, columns=['id','fname','lname','email','uname','password'])
        # df = pd.DataFrame(res)
        print(df)
        return df
    except Exception as e:
        print(e)

def readAllDb():
    try:
        sql = """SELECT * FROM report WHERE uname=?"""
        res = cur.execute(sql, (st.session_state.user,))
        # for row in res:
        #     print(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],'\n')
        df = pd.DataFrame(res, columns=['id','date','time','topic','detail','result','User'])
        print(df)
        return df
    except Exception as e:
        print(e)

def readFromDate():
    dt = datetime.now()
    ddate1 = dt.strftime("%Y-%m-%d")
    ddate = input('Date yyyy-mm-dd: ')
    if ddate == '':
        ddate = ddate1
    sql = "SELECT * FROM report WHERE date=? AND uname=?"
    res = cur.execute(sql,(ddate,st.session_state.user,))
    df = pd.DataFrame(res, columns=['id','date','time','topic','detail','result','commander','assistant','User'])
    print(df)

def readFromLast():
    sql = "SELECT * FROM report WHERE uname=? ORDER BY ROWID DESC"
    res = cur.execute(sql,(st.session_state.user,))
    num_row = input('How many row ? : ')
    if num_row == '':
        num_row = 5
    print(f'Show {num_row} by last time')
    df = pd.DataFrame(res, columns=['id','date','time','topic','detail','result','commander','assistant','User'])
    print(df)

def deleteById():
    try :
        id = input('Input id row for delete : ')
        read = "SELECT * FROM report WHERE id=?"
        # cur.execute(read,(id,))# for row in res:
        res = cur.execute(read,(id))
        df = pd.DataFrame(res, columns=['id','date','time','topic','detail','result','commander','assistant','User'])
        print(df)
        ct = input('Delete this report ? (y/n):')
        if ct == 'y':
            sql = 'DELETE FROM report WHERE id=?'
            cur.execute(sql,(id,))
            con.commit()
            print(f'id:{id} Deleted')
        else:
            print(f'Not Delete this report ')
    except Exception as e:
        print(e)

def repassword():
    try:
        sql = """SELECT id FROM user WHERE uname=?"""
        res = cur.execute(sql, (st.session_state.user,))
        df = pd.DataFrame(res)
        userid = df[0][0]
        userid =str(userid)
        # print(f'userid : {userid}')
        # new_pass = getpass.getpass('Input new password :')
        # password = hashlib.sha256(new_pass.encode()).hexdigest()
        ct = input('Chang password ?(y/n) :')
        if ct == 'y':
            sql = "UPDATE user SET password=? WHERE id=?"
            cur.execute(sql,(password, userid,))
            con.commit()
            print(f'{st.session_state.user} Change Password Successful')
    except Exception as e:
        print(e)

def deleteAll():
    try :
        ans = input('Delete All Data ? (y/n)')
        if ans == 'y':
            sql = 'DELETE FROM report'
            cur.execute(sql)
            con.commit()
            print('Deleted')

    except Exception as e:
        print(e)

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
        pwd = st.text_input("Password", value="", type="password", key="password")
        if st.form_submit_button("Save"):insertUserDB(fname,lname,email,uname,pwd)
