import sqlite3
import logging
import getpass
import hashlib
import pandas as pd
import openpyxl
from datetime import datetime

logsFile = 'logs.log'
db = 'report.db'
con = sqlite3.connect(db)
cur = con.cursor()
logging.basicConfig(filename=logsFile, encoding='utf-8', level=logging.logProcesses,
                        format=(f'%(asctime)s {getpass.getuser()} : %(levelname)s : %(message)s'))
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
        logging.debug('Create User Table')
        print('Create Table User ')
    except Exception as e:
        logging.error(e)
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
        logging.debug('Create New report Table')
    except Exception as e:
        logging.error(e)
        print(e)

#---------------------- Insert User ------------------------------
def insertUserDB(fname, lname, email, uname, password):
    try :
        passwd = hashlib.sha256(password.encode()).hexdigest()
        cur.execute("INSERT INTO user (fname, lname, email, uname, password)VALUES (?,?,?,?,?)", \
                    (fname, lname, email, uname, passwd))

        con.commit()
        print("Insert user Success")
        logging.debug(f'Insert user name {uname}')
    except Exception as e:
        logging.error(e)
        print(e)

def insertUser():
    print('Add New User. \n')
    fname = input('First name: ')
    lname = input('Last name: ')
    email = input('Email : ')
    uname = input('Login name: ')
    #password = input('Password: ')
    password = getpass.getpass('Password: ')    # pycharm can't run getpass
    password = hashlib.sha256(password.encode()).hexdigest()
    insertUserDB(fname, lname, email, uname, password)

#---------------------- Insert data ------------------------------
def insertReport(ddate, ttime, topic, detail, result, uname):
    try :
        cur.execute("INSERT INTO report (date, time, topic, detail, result, "
                    "uname)VALUES (?,?,?,?,?,?)", \
                    (ddate, ttime, topic, detail, result, uname))

        con.commit()
        print(ddate, ttime, topic, detail, result,uname)
        print("Success")
        logging.debug(f'Insert data from {user}')
    except Exception as e:
        logging.error(e)
        print(e)

def insert(topic,detail,result):
    try:
        dt = datetime.now()
        ddate1 = dt.strftime("%Y-%m-%d")
        ddate = ddate1
        ttime1 = dt.strftime("%H:%M:%S")
        ttime = ttime1
        #------------------- Input -------------------
        # ddate = input('Date yyyy-mm-dd: ')
        # if ddate == '':
        #     ddate = ddate1
        # ttime = input('Time HH:MM:SS: ')
        # if ttime == '':
        #     ttime = ttime1
        # topic = input('Topic : ')
        # detail = input('Detail :')
        # result = input('Result: ')
        # uname = user
        insertReport(ddate,ttime,topic,detail,result,user)
    except Exception as e:
        print(e)
        logging.error(e)

global num_login
num_login = 0

def login(user1,password1):
    global user
    user = user1
    # global num_login
    # print('Wellcome to your report Please Login \n')
    # user = input('Username: ')
    # password = getpass.getpass('Password: ')    # pycharm can't run getpass
    # password = input('Password: ')
    password = hashlib.sha256(password1.encode()).hexdigest()
    cur.execute("SELECT * FROM user WHERE uname=? AND password=?",(user,password))
    if cur.fetchall():
        # print('Login True')
        return True

    else:
        # print('Login false')
        return False
        # print("It's Wrong!! Try Again \n")
        # num_login += 1
        # if num_login >= 3 :
        #     exit()
        # login()
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
        res = cur.execute(sql, (user,))
        # for row in res:
        #     print(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],'\n')
        df = pd.DataFrame(res, columns=['id','date','time','topic','detail','result','User'])
        print(df)
        return df
        # ct = input('Save to Excel (y/n) ? ').lower()
        # if ct == 'y':
        #     exportToExcel(df)
        # else:
        #     pass
    except Exception as e:
        print(e)

def readFromDate():
    dt = datetime.now()
    ddate1 = dt.strftime("%Y-%m-%d")
    ddate = input('Date yyyy-mm-dd: ')
    if ddate == '':
        ddate = ddate1
    sql = "SELECT * FROM report WHERE date=? AND uname=?"
    res = cur.execute(sql,(ddate,user,))
    df = pd.DataFrame(res, columns=['id','date','time','topic','detail','result','commander','assistant','User'])
    print(df)
    ct = input('Save to Excel (y/n) ? ').lower()
    if ct == 'y':
        exportToExcel(df)
    else:
        pass

def readFromLast():
    sql = "SELECT * FROM report WHERE uname=? ORDER BY ROWID DESC"
    res = cur.execute(sql,(user,))
    num_row = input('How many row ? : ')
    if num_row == '':
        num_row = 5
    print(f'Show {num_row} by last time')
    df = pd.DataFrame(res, columns=['id','date','time','topic','detail','result','commander','assistant','User'])
    print(df)
    ct = input('Save to Excel (y/n) ? ').lower()
    if ct == 'y':
        exportToExcel(df)
    else:
        pass

def exportToExcel(df):
    try:
        dt = datetime.now()
        ddate = dt.strftime("%Y-%m-%d")
        ttime1 = dt.strftime("%H:%M:%S")
        # fileInputName= input('File name : ')

        fileInputName = user
        # if fileInputName == '':
        #     fileInputName = ttime1

        filename = f"{ddate}_{ttime1}_{fileInputName}.xlsx"
        df.to_excel(filename, index=False)
        return filename
        print(f"Successfull {filename} By {user} \n")
        logging.debug(f'Create {filename} By {user}')

    except Exception as e:
        logging.error(e)
        print(e)
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
            logging.debug(f'Delete report id:{id} By {user}')
            print(f'id:{id} Deleted')
        else:
            print(f'Not Delete this report ')

    except Exception as e:
        print(e)
        logging.error('Delete report by id ',e)

def repassword():
    try:

        sql = """SELECT id FROM user WHERE uname=?"""
        res = cur.execute(sql, (user,))
        df = pd.DataFrame(res)
        userid = df[0][0]
        userid =str(userid)
        # print(f'userid : {userid}')
        new_pass = getpass.getpass('Input new password :')
        password = hashlib.sha256(new_pass.encode()).hexdigest()
        ct = input('Chang password ?(y/n) :')
        if ct == 'y':
            sql = "UPDATE user SET password=? WHERE id=?"
            cur.execute(sql,(password, userid,))
            con.commit()
            print(f'{user} Change Password Successful')
            logging.debug(f'Chang password user {user}')
    except Exception as e:
        print(e)

def deleteAll():
    try :
        ans = input('Delete All Data ? (y/n)')
        if ans == 'y':
            sql = 'DELETE FROM report'
            cur.execute(sql)
            con.commit()
            logging.debug(f'Delete All By {user}')
            print('Deleted')

    except Exception as e:
        print(e)
        logging.error('delete all ',e)

#-------------- Check first time and Create table ------------------
# try:
#     res = cur.execute("SELECT id FROM user")
#     # print(res)
# except:
#     # print("None")
#     creatTable_user()
#     insertUser()
#     creatTable_report()
