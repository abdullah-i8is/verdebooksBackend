import pandas as pd
import mysql.connector as mysql
from datetime import datetime,timedelta
import numpy as np
import requests

db_name = "verdebooks"
db_password = "sohaib023612"
db_user = "verdebook"
db_host = "Localhost"

def dbAuth():
    db = mysql.connect(host=db_host, user=db_user, passwd=db_password, database=db_name)
    cursor=db.cursor(buffered=True)
    return db,cursor

def storeEmployees(data):
    db,cursor=dbAuth()
    query="insert into employee(name,jobTitle,status,hireDatedob,workingLocation,accountHolder,bankName,accountNumber,branchName,bankLocation,address,town,postalCode,phn,phn2,gendernotes,mi,payRate,payTypevacPolicy,deduction,paymentMethod,email) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    values=()
    for i in range(len(data["name"])):
        loc=data["address"][i].split(",")
        try:
            town=loc[1]
        except:
            town=str(data["address"][i])
        query="insert into employee(name,jobTitle,status,hireDate,dob,workingLocation,accountHolder,bankName,accountNumber,branchName,bankLocation,address,town,postalCode,phn,phn2,gender,notes,mi,payRate,payType,vacPolicy,deduction,paymentMethod,email) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        values=(str(data["name"][i]),"null","null","null","null",str(data["address"][i]),str(data["name"][i]),"null","null","null",str(data["address"][i]),str(data["address"][i]),str(town),"null",str(data["phn"][i]),"null","null","null","null",str(data["payRate"][i]),"null","null","0","bank","null")
        cursor.execute(query,values)
        db.commit()
        query2="select id from employee order by id desc limit 1"
        cursor.execute(query2)
        result=cursor.fetchone()
        print(result[0])
        query3="insert into stubs(`generateDate`, `payDate`, `name`, `RegCurrent`, `YTD`, `OTHours`, `OTRate`, `OTCurrent`, `OTYTD`, `VACCurrent`, `VACYTD`, `StatHours`,`StatRate`, `StatYTD`, `IncomeTax`, `IncomeTaxYTD`, `EI`, `EIYTD`, `CPP`, `CPPYTD`, `TotalPayCurrent`, `TotalPayYTD`, `TotalTaxCurrent`, `TotalTaxYTD`, `NetPay`,`employeeId`, `status`,`weekStart`,`weekEnd`,`regHours`)  value(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        generateDate=str(datetime.today().strftime('%Y-%m-%d'))
        values3=(generateDate,0,data["name"][i],0,0,0,0,0,0,0,0,0,1.5,0,0,0,0,0,0,0,0,0,0,0,0,result[0],'initial',0,0,0)
        cursor.execute(query3,values3)
        db.commit()
    return "success"

data=pd.read_csv("employeeData.csv")
filter={}
filter['name']=data['Name (full)'].tolist()
filter['address']=data['home adress'].tolist()
filter['phn']=data['Contact number'].tolist()
filter['company']=data['Company'].tolist()
filter['payRate']=data['Payrate'].tolist()

#result=storeEmployees(filter)
#print(result)

def addStub(data,data2):
    id=1
    for i in range(len(data["January7"])):
        #print(i)
        #print(type(data["January7"][i]))
        if str(data["January7"][i])==str(float('NaN')):
            print("empty")
        else:
            postData={"employees":str(id),"payHours":data["January7"][1],"otHours":0,"stat":0,"memo":0,"payDate":"2022-02-27","week":"2022-02-19 - 2022-02-25"}
            response = requests.post("https://verdebooks.com:7900/api/runPayRoll", data = postData,verify=False)
            print("success")
        id=id+1
    return ""

hours={}
#hours["January7"]=data["March 18"].tolist()
#hours["January7"]=data["April 22"]
#hours["January7"]=data["April 15"]
#hours["January7"]=data["April 8"]
#hours["January7"]=data["April 1"]
#hours["January7"]=data["March 25"]
#hours["January7"]=data["March 18"]
#hours["January7"]=data["March 11"]
#hours["January7"]=data["March 4"]
hours["January7"]=data["February 25"]
#hours["January7"]=data["February 18"]
#hours["January7"]=data["February 11"]
#hours["January7"]=data["February 4"]
#hours["January7"]=data["January 28"]
#hours["January7"]=data["January 21"]
#hours["January7"]=data["January 14"]
#hours["January7"]=data["January 7"]

addStub(hours,filter)
