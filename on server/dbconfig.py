from flask import Flask, request, url_for, redirect, render_template
from flaskext.mysql import MySQL
import re,datetime, random

def dbconfig(app):
    mysql = MySQL()
    app.config["MYSQL_DATABASE_USER"]='root'
    app.config["MYSQL_DATABASE_PASSWORD"]='172124'
    app.config["MYSQL_DATABASE_DB"]='cb'
    app.config["MYSQL_DATABASE_HOST"]='localhost'
    mysql.init_app(app)
    return mysql
#==================================================================================
def staffconfig(staff,app):
    mysql = dbconfig(app)
    connect = mysql.connect()
    curr = connect.cursor()
    check = curr.execute("SELECT * FROM staff WHERE ID = %s", [staff])
    record = curr.fetchall()
    result_meet = ''
    if (check ==0):
        return 'Thông tin cán bộ không có trong hệ thống bạn nhé !'
    else:
        for row in record:
            ID = row[0]
            name = row[1]
            role = row[2]
            function = row[3]
            room = row[4] 
            meet = row[5]                      
        result_staff = 'Ông/bà: '+ str(name)+ ' là '+ str(role)
        if meet != None:
            result_meet = '. Bạn có thể gặp người này tại ' + str(meet) +' .'
        else:            
            result_meet = '. Bạn có thể liên hệ bộ phận: '+ str(function) + ' để được gặp.'            
    return result_staff + result_meet

#==============================================================================================
def findroom(room,app):
    mysql = dbconfig(app)
    connect = mysql.connect()
    curr = connect.cursor()
    check = curr.execute("SELECT room, meet FROM room WHERE room = %s", [room])
    record = curr.fetchall()    
    if (check==0):
        return 'Thông tin phòng không có trong hệ thống bạn nhé !'
    else:
        for i in record:                        
            return 'Phòng số '+str(i[0]) +  ' là '+ str(i[1]) +'.'

#====================================================================================================
def findprice(fee,app):
    mysql = dbconfig(app)
    connect = mysql.connect()
    curr = connect.cursor()
    check = curr.execute("SELECT  name, id,prince FROM fee WHERE id = %s", [fee])
    record = curr.fetchall()    
    if check == 1:
        for i in record:                        
            return 'Dịch vụ: ' + str(i[0])  + ' (MSDV:'+ str(i[1])+')' ' có giá '+ str(i[2]) +'00/tháng'
        else:
            return 'Trung tâm dịch vụ Ký túc xá Bách khoa không kinh doanh dịch vụ này nhé!'
#====================================================================================================
def findrule(rule,app):
    mysql = dbconfig(app)
    connect = mysql.connect()
    curr = connect.cursor()
    check = curr.execute("SELECT  * FROM rule WHERE id = %s", [rule])
    record = curr.fetchall()    
    if check == 1:
        for i in record:                        
            return str(random.choice(i[2:])) +" Bạn có thể xem thêm quy định tại trang web: ktxbk.vn"
    else:
            return 'Xin lỗi, Chatbot chưa hiểu yêu cầu của bạn ! Bạn vui lòng gửi lại câu hỏi nhé !'