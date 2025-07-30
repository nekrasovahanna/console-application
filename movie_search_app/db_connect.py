import pymysql

def connect():
    conn = pymysql.connect(
        host='ich-edit.edu.itcareerhub.de',
        user='ich1',
        password='ich1_password_ilovedbs',
        database='170624_Nekrasova'
        )
    return conn

conn = connect()



