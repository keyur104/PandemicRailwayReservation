import pyqrcode
import qrcode
import  psycopg2
from django.shortcuts import render,redirect
# from .models import Railwayroute
from datetime import date
from django.contrib import messages
from datetime import datetime, timedelta
# from .models import Mahanagari_Express
# from .models import Pune_Bsl_Express
# from .models import Nagpur_Pune_Express
# from .models import Mahanagari_Express_Schedule
# from .models import Nagpur_Pune_Express_Schedule
from .models import RegisterSignup
from django.apps import apps 
from django.contrib import admin 
from django.contrib.admin.sites import AlreadyRegistered 
from django.db import connection
from itertools import chain 
from datetime import date
from django.contrib.auth.models import User,auth
import datetime as dt
import math
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import os
import html
import mimetypes
from email.headerregistry import Address
from email.message import EmailMessage
from email.utils import make_msgid
from pathlib import Path

table =[]
DATE = date.today()
train=[]
PREFIX = "Railway_"
SUFFIX = "_schedule"
train_name=""
DATE=date.today()
email=""
fullname=""
username=""
MobileNo=""
email=""
password=""
src_date=date.today()
From=""
To=""
hs=[]
grp=[]
can_gi=[]
can_name=[]
seat_array = []
sleeper_array = []
ac3_array = []
ac2_array = []
ac1_array = []
temp=0
pass_name=[]

class Demo:
    no_of_Seats = 0  
# Create your views here.
def instruction(request):
    return render(request,"instruction.html")


def index(request):
    source_date=[]
    g_d=date.today()
    train_n=[]
    src_time=[]
    final_time=[]
    rem_time=[]
    to_time=[]
    ks=[]
    
    with connection.cursor() as cursor:

        query="select distinct(group_id) from public.\"Railway_registration\" where  \"medical_status\"='pending'"
        print(query)
        cursor.execute(query)
        a=cursor.fetchall()
        print(a)
        gp= list(chain.from_iterable(a))
      
      
        for i in gp:
            query="select \"train_name\",\"src_date\" from public.\"Railway_registration\" where \"group_id\"='"+str(i)+"' limit 1"
            cursor.execute(query)
            result=cursor.fetchall()

            ks.append(result)
            print(ks)
        
        hs= list(chain.from_iterable(ks)) 
        print(hs)

        for i in range(len(hs)):
            
            g_t=hs[i][0]
            g_d=hs[i][1]
            print(g_d)
            d=g_d.replace('-',',')
            print(d)
            (year,month,day)=d.split(',')
            print(type(d))
            # print(d[1])
        
        #     year=d[0]
        #     month=d[1]
        #     day=d[2]
            train_n.append(g_t)
            get_date=dt.date(int(year),int(month),int(day))
            source_date.append(get_date)
        
        
        print(source_date) 
        print(train_n)   

        for i in range(len(train_n)):
            query="select \"src_time\" from public.\"Railway_railwayroute\" where \"name\"='"+train_n[i]+"'"
            cursor.execute(query)
            sr_time=cursor.fetchall()
            print(sr_time)
            sr_time= list(chain.from_iterable(sr_time)) 
            src_time.append(sr_time)
            final_time.append(dt.datetime.combine(source_date[i],sr_time[0]))
            rem_time.append(final_time[i] - timedelta(hours=18, minutes=0))
            to_time.append(final_time[i] - timedelta(hours=4, minutes=0))
            print(to_time[i])
            print(dt.datetime.today())
            if to_time[i] < dt.datetime.today():
                query="update public.\"Railway_registration\" set \"medical_status\"='CANCELLED' where \"group_id\"='"+str(gp[i])+"'"
                print(query)
                cursor.execute(query)
                s=smtplib.SMTP('smtp.gmail.com',587)
    
                s.ehlo()
                        
                s.starttls()
                        
                s.login('boiii2412@gmail.com','motorcop')
                        
                subject = 'INDIAN RAILWAYS - Ticket Cancellation '
                #body = 'HEY',FULLNAME,'!!,You have booked a', CARNAME ,'from ',PICKDATE,'to',DROPDATE,',.This is to inform you that your booking is CONFIRMED' 
                body="your Ticket with  has been Cancelled because , you did not upload medical certificcate in time. ".format(cancel_id,sr_date)
                message = f'Subject : {subject}\n\n {body}'
                        
                s.sendmail('boiii2412@gmail.com',request.user.email,message)
                        
                print ('HEY AN EMAIL HAS BEEN SENT!')
                        
                s.quit()



    return render(request,"index.html")

def afterSearch(request):

    # try:
    #     connection = psycopg2.connect(user="postgres",password="1234",host="127.0.0.1",port="5432",database="Railway")
    #     cursor = connection.cursor()
    #     postgreSQL_select_Query = "select * from Railway_mahanagari_express"

    # except(Exception, psycopg2.Error) as error :
    #     print ("Error while fetching data from PostgreSQL", error)
    
    global table
    global To
    global From    
    global PREFIX
    global SUFFIX
    value=[]
    d1=[]
    train_with_priority=[]
    final_name=[]
    final_days=[]
    final_date=[]
    global DATE
    display_data=[]
    global train
    
    final_result=[]
    global src_date
    src_arr=[]
    des_arr=[]
    invalid_date="Please insert Proper Date"


    # msg="invalid credentials"
    try:
        From=request.GET['from']
        To=request.GET['to']
    except:
        From = False
        To=False
    DATE=request.GET['date']
    DATE=datetime.date(datetime.strptime(DATE,"%Y-%m-%d"))      
    if From =="" or To=="":
        if request.user.is_authenticated:
            return redirect(afterlogin)
        else:    
            return redirect(index)
    if DATE < date.today():
        if request.user.is_authenticated:
            return render(request,"afterlogin.html",{"invalid_date":invalid_date})
        else: 
            return render(request,"index.html",{"invalid_date":invalid_date})       
    else:    
        print("i am from",From)
        print("to",To)
        print(type(DATE))
        try:
            # result=cursor.execute(postgreSQL_select_Query)
            
            # result= Railwayroute.objects.all()
            # app_models = apps.get_app_config('Railway').models
            # for i in app_models:
            #     print(i.title())
            #     class_name=i.title()
            #     data=class_name.objects.all()
            #     print(data)
                
            table_name= [ m._meta.db_table for c in apps.get_app_configs() for m in c.get_models() ]
            with connection.cursor() as cursor:
                # for i in range(len(table_name)):
                    # print(table_name[i])
                    # cursor.execute("select * from \"{}\"".format(table_name[i]))
                    # print(cursor.fetchall())
                print(From)
                print(To)    
                
                sql1 = "select name from \"{}\"".format("Railway_railwayroute")+" where '"+From+"' = ANY(intermediate_station) and '"+To+"'= ANY(intermediate_station)"
                #sql1 = "select * from \"{}\"".format("Railway_railwayroute")+"where intermediate_station = ANY("+FROM+")"
                #sql1 =  "select name from \"{}\"".format("Railway_railwayroute")+" where  intermediate_station in ('{}', '{}')".format('{Pune Junction(PUNE)}','{Jalgaon(JL)}')  
                #sql1 =  "select name from \"{}\"".format("Railway_railwayroute")+" where  intermediate_station in (" +FROM +","+ TO +")" 
                print(sql1)
                cursor.execute(sql1)
                train_with_station=cursor.fetchall()
                
                #print(train_with_station[0][0])
                # for i in range(len(train_with_station)):
                #     print(i)
                #     value[i]=train_with_station[i][0]
                # print(value)
                value=list(chain.from_iterable(train_with_station)) 
                print(value)
                for i in value:
                    d1=[]
                    data1="select  \"No\"  from public.\"{}{}\" ".format(PREFIX,i.lower())+" where \"StationName\" ='" + From +"'"# or \"StationName\" ='"+To+"'"
                    data2="select  \"No\"  from public.\"{}{}\" ".format(PREFIX,i.lower())+" where \"StationName\" ='" + To +"'"
                    
                    print(data1)
                    print(data2)
                    
                    
                    cursor.execute(data1)
                    data11=cursor.fetchall()
                    print("heloo world")
                    
                    
                    cursor.execute(data2)
                    data21=cursor.fetchall()
                    print(data21)

                    d1.append(data11[0])
                    d1.append(data21[0])
                    print(d1)
                    
                    # d1=list(chain.from_iterable(d1)) 
                    # print(d1)
                    #print(d1[0])
                    #print(d1[1])
                    print(d1[0])
                    print(d1[1])
                    if (d1[0]<d1[1]):
                        query="select  \"trainNo\"  from public.\"{}{}\" ".format(PREFIX,i.lower())
                        print(query)
                        cursor.execute(query)
                        #print(cursor.fetchone())
                        train_no=cursor.fetchone()
                        train_no1=train_no[0] 
                        train_with_priority.append(train_no1)
                        print(train_with_priority)
                        final_name.append(i.lower())
                print(final_name)
                # query="select \"RunningStatus\" from public.\"{}{}{}\" ".format(PREFIX,final_name[0],SUFFIX)+" where \"date\"="+str(DATE)
                # print(query)

                for i in range(len(train_with_priority)):
                    query1=" select \"Day\" from  public.\"{}{}\" ".format(PREFIX,final_name[i])+" where \"StationName\"='"+From+"'"
                    print(query1)
                    cursor.execute(query1)
                    days=cursor.fetchall() 
                    print(days)
                    for j in days:
                        final_days.append(int(j[0]))
                print(final_days)
                    
                for j in range(len(final_days)):  
                    final_date.append(DATE + timedelta(days=-(final_days[j]-1)))#(final_days[j] - 1)))
                    print(final_date[j])
                    
                    src_date=final_date[j]
                    print("source date is"+str(src_date))
                        
                    query="select \"trainNo\" from public.\"{}{}{}\" ".format(PREFIX,final_name[j],SUFFIX)+" where \"date\"='"+str(final_date[j])+"' and \"RunningStatus\"='yes' "
                    print(query)
                    cursor.execute(query)
                    
                    data=cursor.fetchall()
                    print(data)    
                    for k in range(len(data)):
                        display_data.append(data[k][0])
                    # display=list(chain.from_iterable(data))
                    # display_data.append(display) 
                print(display_data)     
                    # print(query)
                    # cursor.execute(query)
                    # print(cursor.fetchall())
                for i in display_data:
                    query="select \"name\" from   \"{}\"".format("Railway_railwayroute")+" where \"trainNo\"='"+str(i)+"'"
                    print(query)
                    cursor.execute(query)
                    t_name=cursor.fetchall()
                    print(t_name)
                    for k in range(len(t_name)):
                        train.append(t_name[k][0])
                print(train)  

                # for i in train:
                #     query="select \"Arrives\",\"Departs\" from public.\"{}{}\" ".format(PREFIX,train[i])+"where \"StationName\"='"+From+"'"
                for i in display_data:
                    #query="select \"trainNo\" ,\"name\" from \"{}\"".format("Railway_railwayroute")+"where \"trainNo\"='"+str(i)+"'"
                    query="SELECT \"trainNo\" ,\"name\" FROM \"{}\"".format("Railway_railwayroute")+" WHERE  \"trainNo\"= %s" %i
                    # result=Railwayroute.objects.raw(query)
                    try:
                        with connection.cursor() as cursor:
                            cursor.execute(query)
                            result = cursor.fetchall()
                            final_result=final_result + result
                            #print(result[1])
                            print(type(result))
                        print(result)
                        print(query)
                        # cursor.execute(query)
                        # t_data=cursor.fetchall()
                        # for k in range(len(t_data)):
                        #     train.append(t_name[k][0])

                        # print(result)  
                    except:
                        print("Error")  
                print(final_result)  
                print(train)  

                
                
                for i in train:
                    try:
                        with connection.cursor() as cursor:
                            query="select \"Arrives\" from \"{}{}\"".format(PREFIX,i)+" where \"StationName\"='"+From+"'"
                            query1="select \"Arrives\" from \"{}{}\"".format(PREFIX,i)+" where \"StationName\"='"+To+"'"
                            print(query)
                            cursor.execute(query)
                            src_arrives=cursor.fetchall()
                            src_arrives=list(chain.from_iterable(src_arrives)) 
                            print("Arrival Time",str(src_arrives[0]))
                            src_arr.append(src_arrives[0])


                            query="select \"Arrives\" from \"{}{}\"".format(PREFIX,i)+" where \"StationName\"='"+To+"'"
                            print(query)
                            cursor.execute(query)
                            des_arrives=cursor.fetchall()
                            des_arrives=list(chain.from_iterable(des_arrives)) 
                            print("Arrival Time",str(des_arrives[0]))
                            des_arr.append(des_arrives[0])
                    except(Exception, psycopg2.Error) as error:
                        print("Connection error",error)     
                final_result=zip(final_result,src_arr,des_arr)
               

            return render(request,"afterSearch.html",{"final_result":final_result,"From":From,"To":To})
        except(Exception, psycopg2.Error) as error:
            print("Connection error",error)
            return redirect(index)


def checkAvail(request):
    global train 
    global train_name
    global To
    global From
    global DATE
    global sleeper_array
    global ac3_array
    global ac2_array
    global ac1_array
   

    seat_array = ["S1_1", "S1_3", "S1_4", "S1_7", "S1_8", "S1_9", "S1_11", "S1_12", "S1_15", "S1_16", "S1_17", "S1_19", "S1_20", "S1_23", "S1_24", "S1_25", "S1_27", "S1_28", "S1_31", "S1_32", "S1_33", "S1_35", "S1_36", "S1_39", "S1_40", "S1_41", "S1_43", "S1_44", "S1_47", "S1_48", "S1_49", "S1_51", "S1_52", "S1_55", "S1_56", "S1_57", "S1_59", "S1_60", "S1_63", "S1_64", "S1_65", "S1_67", "S1_68", "S1_71", "S1_72",
    "S2_1", "S2_3", "S2_4", "S2_7", "S2_8", "S2_9", "S2_11", "S2_12", "S2_15", "S2_16", "S2_17", "S2_19", "S2_20", "S2_23", "S2_24", "S2_25", "S2_27", "S2_28", "S2_31", "S2_32", "S2_33", "S2_35", "S2_36", "S2_39", "S2_40", "S2_41", "S2_43", "S2_44", "S2_47", "S2_48", "S2_49", "S2_51", "S2_52", "S2_55", "S2_56", "S2_57", "S2_59", "S2_60", "S2_63", "S2_64", "S2_65", "S2_67", "S2_68", "S2_71", "S2_72",
    "S3_1", "S3_3", "S3_4", "S3_7", "S3_8", "S3_9", "S3_11", "S3_12", "S3_15", "S3_16", "S3_17", "S3_19", "S3_20", "S3_23", "S3_24", "S3_25", "S3_27", "S3_28", "S3_31", "S3_32", "S3_33", "S3_35", "S3_36", "S3_39", "S3_40", "S3_41", "S3_43", "S3_44", "S3_47", "S3_48", "S3_49", "S3_51", "S3_52", "S3_55", "S3_56", "S3_57", "S3_59", "S3_60", "S3_63", "S3_64", "S3_65", "S3_67", "S3_68", "S3_71", "S3_72",
    "S4_1", "S4_3", "S4_4", "S4_7", "S4_8", "S4_9", "S4_11", "S4_12", "S4_15", "S4_16", "S4_17", "S4_19", "S4_20", "S4_23", "S4_24", "S4_25", "S4_27", "S4_28", "S4_31", "S4_32", "S4_33", "S4_35", "S4_36", "S4_39", "S4_40", "S4_41", "S4_43", "S4_44", "S4_47", "S4_48", "S4_49", "S4_51", "S4_52", "S4_55", "S4_56", "S4_57", "S4_59", "S4_60", "S4_63", "S4_64", "S4_65", "S4_67", "S4_68", "S4_71", "S4_72",
    "S5_1", "S5_3", "S5_4", "S5_7", "S5_8", "S5_9", "S5_11", "S5_12", "S5_15", "S5_16", "S5_17", "S5_19", "S5_20", "S5_23", "S5_24", "S5_25", "S5_27", "S5_28", "S5_31", "S5_32", "S5_33", "S5_35", "S5_36", "S5_39", "S5_40", "S5_41", "S5_43", "S5_44", "S5_47", "S5_48", "S5_49", "S5_51", "S5_52", "S5_55", "S5_56", "S5_57", "S5_59", "S5_60", "S5_63", "S5_64", "S5_65", "S5_67", "S5_68", "S5_71", "S5_72",
    "S6_1", "S6_3", "S6_4", "S6_7", "S6_8", "S6_9", "S6_11", "S6_12", "S6_15", "S6_16", "S6_17", "S6_19", "S6_20", "S6_23", "S6_24", "S6_25", "S6_27", "S6_28", "S6_31", "S6_32", "S6_33", "S6_35", "S6_36", "S6_39", "S6_40", "S6_41", "S6_43", "S6_44", "S6_47", "S6_48", "S6_49", "S6_51", "S6_52", "S6_55", "S6_56", "S6_57", "S6_59", "S6_60", "S6_63", "S6_64", "S6_65", "S6_67", "S6_68", "S6_71", "S6_72",
    "S7_1", "S7_3", "S7_4", "S7_7", "S7_8", "S7_9", "S7_11", "S7_12", "S7_15", "S7_16", "S7_17", "S7_19", "S7_20", "S7_23", "S7_24", "S7_25", "S7_27", "S7_28", "S7_31", "S7_32", "S7_33", "S7_35", "S7_36", "S7_39", "S7_40", "S7_41", "S7_43", "S7_44", "S7_47", "S7_48", "S7_49", "S7_51", "S7_52", "S7_55", "S7_56", "S7_57", "S7_59", "S7_60", "S7_63", "S7_64", "S7_65", "S7_67", "S7_68", "S7_71", "S7_72",
    "S8_1", "S8_3", "S8_4", "S8_7", "S8_8", "S8_9", "S8_11", "S8_12", "S8_15", "S8_16", "S8_17", "S8_19", "S8_20", "S8_23", "S8_24", "S8_25", "S8_27", "S8_28", "S8_31", "S8_32", "S8_33", "S8_35", "S8_36", "S8_39", "S8_40", "S8_41", "S8_43", "S8_44", "S8_47", "S8_48", "S8_49", "S8_51", "S8_52", "S8_55", "S8_56", "S8_57", "S8_59", "S8_60", "S8_63", "S8_64", "S8_65", "S8_67", "S8_68", "S8_71", "S8_72",
    "S9_1", "S9_3", "S9_4", "S9_7", "S9_8", "S9_9", "S9_11", "S9_12", "S9_15", "S9_16", "S9_17", "S9_19", "S9_20", "S9_23", "S9_24", "S9_25", "S9_27", "S9_28", "S9_31", "S9_32", "S9_33", "S9_35", "S9_36", "S9_39", "S9_40", "S9_41", "S9_43", "S9_44", "S9_47", "S9_48", "S9_49", "S9_51", "S9_52", "S9_55", "S9_56", "S9_57", "S9_59", "S9_60", "S9_63", "S9_64", "S9_65", "S9_67", "S9_68", "S9_71", "S9_72",
    "S10_1", "S10_3", "S10_4", "S10_7", "S10_8", "S10_9", "S10_11", "S10_12", "S10_15", "S10_16", "S10_17", "S10_19", "S10_20", "S10_23", "S10_24", "S10_25", "S10_27", "S10_28", "S10_31", "S10_32", "S10_33", "S10_35", "S10_36", "S10_39", "S10_40", "S10_41", "S10_43", "S10_44", "S10_47", "S10_48", "S10_49", "S10_51", "S10_52", "S10_55", "S10_56", "S10_57", "S10_59", "S10_60", "S10_63", "S10_64", "S10_65", "S10_67", "S10_68", "S10_71", "S10_72",
    "B1_1", "B1_3", "B1_4", "B1_7", "B1_8", "B1_9", "B1_11", "B1_12", "B1_15", "B1_16", "B1_17", "B1_19", "B1_20", "B1_23", "B1_24", "B1_25", "B1_27", "B1_28", "B1_31", "B1_32", "B1_33", "B1_35", "B1_36", "B1_39", "B1_40", "B1_41", "B1_43", "B1_44", "B1_47", "B1_48", "B1_49", "B1_51", "B1_52", "B1_55", "B1_56", "B1_57", "B1_59", "B1_60", "B1_63", "B1_64",
    "B2_1", "B2_3", "B2_4", "B2_7", "B2_8", "B2_9", "B2_11", "B2_12", "B2_15", "B2_16", "B2_17", "B2_19", "B2_20", "B2_23", "B2_24", "B2_25", "B2_27", "B2_28", "B2_31", "B2_32", "B2_33", "B2_35", "B2_36", "B2_39", "B2_40", "B2_41", "B2_43", "B2_44", "B2_47", "B2_48", "B2_49", "B2_51", "B2_52", "B2_55", "B2_56", "B2_57", "B2_59", "B2_60", "B2_63", "B2_64",
    "B3_1", "B3_3", "B3_4", "B3_7", "B3_8", "B3_9", "B3_11", "B3_12", "B3_15", "B3_16", "B3_17", "B3_19", "B3_20", "B3_23", "B3_24", "B3_25", "B3_27", "B3_28", "B3_31", "B3_32", "B3_33", "B3_35", "B3_36", "B3_39", "B3_40", "B3_41", "B3_43", "B3_44", "B3_47", "B3_48", "B3_49", "B3_51", "B3_52", "B3_55", "B3_56", "B3_57", "B3_59", "B3_60", "B3_63", "B3_64",
    "A1_1", "A1_2", "A1_3", "A1_4", "A1_5", "A1_6", "A1_7", "A1_8", "A1_9", "A1_10", "A1_11", "A1_12", "A1_13", "A1_14", "A1_15", "A1_16", "A1_17", "A1_18", "A1_19", "A1_20", "A1_21", "A1_22", "A1_23", "A1_24", "A1_25", "A1_26", "A1_27", "A1_28", "A1_29", "A1_30", "A1_31", "A1_32", "A1_33", "A1_34", "A1_35", "A1_36", "A1_37", "A1_38", "A1_39", "A1_40", "A1_41", "A1_42", "A1_43", "A1_44", "A1_45", "A1_46", "A1_47", "A1_48",
    "A2_1", "A2_2", "A2_3", "A2_4", "A2_5", "A2_6", "A2_7", "A2_8", "A2_9", "A2_10", "A2_11", "A2_12", "A2_13", "A2_14", "A2_15", "A2_16", "A2_17", "A2_18", "A2_19", "A2_20", "A2_21", "A2_22", "A2_23", "A2_24", "A2_25", "A2_26", "A2_27", "A2_28", "A2_29", "A2_30", "A2_31", "A2_32", "A2_33", "A2_34", "A2_35", "A2_36", "A2_37", "A2_38", "A2_39", "A2_40", "A2_41", "A2_42", "A2_43", "A2_44", "A2_45", "A2_46", "A2_47", "A2_48",
    "1A_1", "1A_2", "1A_3", "1A_4", "1A_5", "1A_6", "1A_7", "1A_8", "1A_9", "1A_10", "1A_11", "1A_12", "1A_13", "1A_14", "1A_15", "1A_16", "1A_17", "1A_18",
    "SWL_1", "SWL_2", "SWL_3", "SWL_4", "SWL_5", "SWL_6", "SWL_7", "SWL_8", "SWL_9", "SWL_10", "SWL_11", "SWL_12", "SWL_13", "SWL_14", "SWL_15", "SWL_16", "SWL_17", "SWL_18", "SWL_19", "SWL_20", "SWL_21", "SWL_22", "SWL_23", "SWL_24", "SWL_25", "SWL_26", "SWL_27", "SWL_28", "SWL_29", "SWL_30", "SWL_31", "SWL_32", "SWL_33", "SWL_34", "SWL_35", "SWL_36", "SWL_37", "SWL_38", "SWL_39", "SWL_40", "SWL_41", "SWL_42", "SWL_43", "SWL_44", "SWL_45", "SWL_46", "SWL_47", "SWL_48", "SWL_49", "SWL_50",
    "3AWL_1", "3AWL_2", "3AWL_3", "3AWL_4", "3AWL_5", "3AWL_6", "3AWL_7", "3AWL_8", "3AWL_9", "3AWL_10", "3AWL_11", "3AWL_12", "3AWL_13", "3AWL_14", "3AWL_15", "3AWL_16", "3AWL_17", "3AWL_18", "3AWL_19", "3AWL_20", "3AWL_21", "3AWL_22", "3AWL_23", "3AWL_24", "3AWL_25", "3AWL_26", "3AWL_27", "3AWL_28", "3AWL_29", "3AWL_30", "3AWL_31", "3AWL_32", "3AWL_33", "3AWL_34", "3AWL_35", "3AWL_36", "3AWL_37", "3AWL_38", "3AWL_39", "3AWL_40",
    "2AWL_1", "2AWL_2", "2AWL_3", "2AWL_4", "2AWL_5", "2AWL_6", "2AWL_7", "2AWL_8", "2AWL_9", "2AWL_10", "2AWL_11", "2AWL_12", "2AWL_13", "2AWL_14", "2AWL_15", "2AWL_16", "2AWL_17", "2AWL_18", "2AWL_19", "2AWL_20"]


    for i in train:
        if i in request.GET:
            train_name=i
            print("its"+train_name)
            print(DATE)
    with connection.cursor() as cursor:
        query = "select \"intermediate_station\" FROM public.\"Railway_railwayroute\" where \"name\" = '{}'".format(train_name)
        print(query)
        cursor.execute(query)
        final_intermediate_stations = cursor.fetchall()
        final_intermediate_stations = list(chain.from_iterable(list(chain.from_iterable(final_intermediate_stations))))
       
        source_index = 0
        dest_index = len(final_intermediate_stations)

        print()

        for i in range(dest_index):
            if From == final_intermediate_stations[i]:
                source_index = i
            if To == final_intermediate_stations[i]:
                dest_index = i

        lst = final_intermediate_stations[source_index].split("(")
        station_name= lst[0]
        st = station_name.replace(" ","_")

        query = "select \"{}\" from public.\"Railway_{}_seat_alloc\" where date = '{}'".format(st, train_name,DATE)
        cursor.execute(query)
        print(query)
        station_seat = cursor.fetchall()
        station_seat = list(chain.from_iterable(list(chain.from_iterable(station_seat))))
        # print(station_seat)

        

        query = "select \"seat\" from public.\"Railway_{}_booked\" where \"date_of_journey\" = '{}' and \"source\" = '{}'".format(train_name,DATE,From)+" and (\"seat\" like \'S%\' or \"seat\" like \'SWL__%\') "
        cursor.execute(query)
        print(query)
        sleeper_array = cursor.fetchall()
        sleeper_array = list(chain.from_iterable(sleeper_array))
       
                

        query = "select \"seat\" from public.\"Railway_{}_booked\" where \"date_of_journey\" = '{}' and \"source\" = '{}'".format(train_name,DATE,From)+" and (\"seat\" like \'B%\' or \"seat\" like \'3AWL_%\') "
        cursor.execute(query)
        ac3_array = cursor.fetchall()
        ac3_array = list(chain.from_iterable(ac3_array))
                


        query = "select \"seat\" from public.\"Railway_{}_booked\" where \"date_of_journey\" = '{}' and \"source\" = '{}'".format(train_name,DATE,From)+" and (\"seat\" like \'A%\' or \"seat\" like \'2AWL_%\') "
        cursor.execute(query)
        ac2_array = cursor.fetchall() 
        ac2_array = list(chain.from_iterable(ac2_array))
                

        query = "select \"seat\" from public.\"Railway_{}_booked\" where \"date_of_journey\" = '{}' and \"source\" = '{}'".format(train_name,DATE,From)+" and (\"seat\" like \'1A%\' or \"seat\" like \'1AWL_%\') "
        cursor.execute(query)
        ac1_array = cursor.fetchall()
        ac1_array = list(chain.from_iterable(ac1_array))
        
        seat_counter_sleeper = 0
        seat_counter_3ac = 0
        seat_counter_2ac = 0
        seat_counter_1ac = 0

        

        for seat in seat_array:
            for j in range(source_index,dest_index):
                lst = final_intermediate_stations[j].split("(")
                station_name= lst[0]
                st = station_name.replace(" ","_")

                query = "select \"{}\" from public.\"Railway_{}_seat_alloc\" where date = '{}'".format(st, train_name,DATE)
                cursor.execute(query)
                station_seats = cursor.fetchall()
                station_seats = list(chain.from_iterable(list(chain.from_iterable(station_seats))))
                # print(station_seats)
            
                if seat in station_seats:
                    pass
                # else:
                #     #print("end:",j)
                #     break 
            #print("J:",j+1)
            #print("dest_index",dest_index)
            if j+1 == dest_index: 
                
                if seat in sleeper_array:
                   
                    seat_counter_sleeper += 1
                elif seat in ac3_array:
                    
                    seat_counter_3ac += 1
                elif seat in ac2_array:
                    
                    seat_counter_2ac += 1 
                elif seat in ac1_array:
                   
                    seat_counter_1ac += 1 
        
        
        if seat_counter_sleeper >=450:
            seat_counter_sleeper=450-seat_counter_sleeper
        elif seat_counter_sleeper <450:
            seat_counter_sleeper=450-seat_counter_sleeper    
        if seat_counter_3ac >=120:
            seat_counter_3ac=120-seat_counter_3ac
        elif seat_counter_3ac <120:
            seat_counter_3ac=120-seat_counter_3ac    
        if seat_counter_2ac >=48:
            seat_counter_2ac=48-seat_counter_2ac
        elif seat_counter_2ac <48:
            seat_counter_2ac=48-seat_counter_2ac    
        if seat_counter_1ac >=18:
            seat_counter_1ac=18-seat_counter_1ac                         
        elif seat_counter_1ac < 18:
            seat_counter_1ac=18-seat_counter_1ac                         

        # if seat_counter_sleeper > -90 and seat_counter_sleeper <= 0:
        #     seat_counter_sleeper -= 1
        # elif seat_counter_3ac > -40 and seat_counter_3ac <= 0:
        #     seat_counter_3ac -= 1
        # elif seat_counter_2ac > -20 and seat_counter_2ac <= 0:
        #     seat_counter_2ac -= 1    

        print(seat_counter_sleeper)
        print(seat_counter_3ac)
        print(seat_counter_2ac)
        print(seat_counter_1ac)

        # query="select count(seat) from public.\"{}{}{}\"".format(PREFIX,train_name,"_booked")+" where \"seat\" like \'S%\' and date_of_journey='"+str(DATE)+"'"
        # cursor.execute(query)
        # occupied=cursor.fetchone()
        # print(occupied[0])
        # if occupied[0]<=450:
        #     count=450-occupied[0]
        #     genCount.append(count)
        # query="select count(seat) from public.\"{}{}{}\"".format(PREFIX,train_name,"_booked")+" where \"seat\" like \'B%\' and date_of_journey='"+str(DATE)+"'"
        # cursor.execute(query)
        # occupied=cursor.fetchone()
        # print(occupied[0])
        # if occupied[0]<=120:
        #     count=120-occupied[0]
        #     genCount.append(count)

        # query="select count(seat) from public.\"{}{}{}\"".format(PREFIX,train_name,"_booked")+" where \"seat\" like \'A%\' and date_of_journey='"+str(DATE)+"'"
        # cursor.execute(query)
        # occupied=cursor.fetchone()
        # print(occupied[0])
        # if occupied[0]<=96:
        #     count=96-occupied[0]
        #     genCount.append(count)

        # query="select count(seat) from public.\"{}{}{}\"".format(PREFIX,train_name,"_booked")+" where \"seat\" like \'1A%\' and date_of_journey='"+str(DATE)+"'"
        # cursor.execute(query)
        # occupied=cursor.fetchone()
        # print(occupied[0])
        # if occupied[0]<=18:
        #     count=18-occupied[0]
        #     genCount.append(count) 

        return render(request,'checkAvail.html',{"seat_counter_sleeper":seat_counter_sleeper,"seat_counter_3ac":seat_counter_3ac,"seat_counter_2ac":seat_counter_2ac,"seat_counter_1ac":seat_counter_1ac})



def login(request):
    if request.user.is_authenticated:
        return render(request,"afterlogin.html")
    else:
        return render(request,"login.html")

def logout(request):
    auth.logout(request)
    return redirect(index)


def afterlogin(request):

    name=""
    paswd=""
    global email
    msg="invalid Credentials"

    if request.user.is_authenticated:
        return render(request,"afterlogin.html")
    else:    

        try:
            name = request.POST['user']
        except:
            name = False
        try:
            paswd = request.POST['paswd']
            print (paswd)
        except:
            paswd = False
        print (paswd)
        print(name)

        user=auth.authenticate(username=name,password=paswd)
        print(auth.authenticate(username=name,password=paswd))

        if user is not None:
            auth.login(request,user)
        
            # query="select \"username\" from  public.\"Railway_registersignup\" where \"username\"='"+name+"'"
            # cursor.execute(query)
            # db_usname=cursor.fetchone()
            # print(db_usname)
            # db_user=db_usname[0]
            # print('db'+db_user)
            # query="select \"password\" from  public.\"auth_user\" where \"username\"='"+name+"'"
            # cursor.execute(query)
            # db_pass=cursor.fetchone()
            with connection.cursor() as cursor:   
                query="select \"email\" from  public.\"auth_user\" where \"username\"='"+name+"'"
                cursor.execute(query)
                db_email=cursor.fetchone()
                email=db_email[0]
                print(email)
        
                return render(request,"afterlogin.html")
        else:
            
                return render(request,"login.html",{"msg":msg})    

def signup(request):
    return render(request,"signup.html")


def aftersignup(request):
    global fullname
    global username
    global MobileNo
    global email
    global password
    ConfirmPassword=""




    invalidUser="user already exists"
    invalidEmail="email already registered"
    invalidData="Fill all fields "
    try:
        fullname = request.POST['fullname']
        print (fullname)
    except:
        fullname = False
        print (fullname)
    try:
        username = request.POST['username']
        print (username)
    except:
        username = False
        print (username)
    try:
        MobileNo=request.POST['phone']
        print (MobileNo)
    except:
        MobileNo=False
        print (MobileNo)
    try:
        email=request.POST['email']
        print (email)
    except:
        email = False
    try:
        password=request.POST['password1']
        print (password)
    except:
        password=False
    try:
        ConfirmPassword=request.POST['password2']
    except:
        ConfirmPassword = False

    if password == ConfirmPassword:
        print("Hello world")
        # if RegisterSignup.objects.filter(username = username).exists():
        #     
        #     return render(request,'signup.html',{"invalidUser":invalidUser})
        # elif RegisterSignup.objects.filter(email = email).exists():
            
        #     print("Hello world3")
        #     return render(request,'signup.html',{"inalidEmail":invalidEmail})
        # elif fullname=="" or username=="" or MobileNo=="" or email=="" or password=="":
        #      return render(request,'signup.html',{"invalidData":invalidData})
        # else:
        #     #user = RegisterSignup.objects.create_user(username = username, email = email, password = password, MobileNo = MobileNo)
        #     with connection.cursor() as cursor:
        #         query="INSERT INTO  public.\"Railway_registersignup\" (\"name\", \"username\", \"mobileno\", \"email\", \"password\") values (\'{}\',\'{}\',\'{}\',\'{}\',\'{}\')".format(fullname,username,MobileNo,email,password)
        #         print(query)
        #         cursor.execute(query)
        if User.objects.filter(username = username).exists():
            
            return render(request,'signup.html',{"invalidUser":invalidUser})

        elif User.objects.filter(email = email).exists():
            print("Hello world3")
            return render(request,'signup.html',{"inalidEmail":invalidEmail})

        elif fullname=="" or username=="" or MobileNo=="" or email=="" or password=="":
             return render(request,'signup.html',{"invalidData":invalidData})
        else:
            user=User.objects.create_user(username=username,password=password,email=email,first_name=fullname)
            user.save()
            with connection.cursor() as cursor:
                    query="INSERT INTO  public.\"Railway_usermob\" (\"username\", \"mobileno\") values (\'{}\',\'{}\')".format(username,MobileNo)
                    print(query)
                    cursor.execute(query)
                
                
                #return redirect('signup')
            return render(request,"aftersignup.html")
    else:
        print("Hello world45")
       # alert('password is not matching')
        return redirect(signup)
    #return redirect('signup')



            
def seatAlloc(request):
    global email
    global train
    global source 
    global destination
    global date_of_journey
    global group_id
    global train_name
   
 

    names = []
    ages = []
    id_proofs = []
    id_numbers = []
    class_types = []
    birth_preferances = []
    pnr_list=[]

    seat_array = ["S1_1", "S1_3", "S1_4", "S1_7", "S1_8", "S1_9", "S1_11", "S1_12", "S1_15", "S1_16", "S1_17", "S1_19", "S1_20", "S1_23", "S1_24", "S1_25", "S1_27", "S1_28", "S1_31", "S1_32", "S1_33", "S1_35", "S1_36", "S1_39", "S1_40", "S1_41", "S1_43", "S1_44", "S1_47", "S1_48", "S1_49", "S1_51", "S1_52", "S1_55", "S1_56", "S1_57", "S1_59", "S1_60", "S1_63", "S1_64", "S1_65", "S1_67", "S1_68", "S1_71", "S1_72",
    "S2_1", "S2_3", "S2_4", "S2_7", "S2_8", "S2_9", "S2_11", "S2_12", "S2_15", "S2_16", "S2_17", "S2_19", "S2_20", "S2_23", "S2_24", "S2_25", "S2_27", "S2_28", "S2_31", "S2_32", "S2_33", "S2_35", "S2_36", "S2_39", "S2_40", "S2_41", "S2_43", "S2_44", "S2_47", "S2_48", "S2_49", "S2_51", "S2_52", "S2_55", "S2_56", "S2_57", "S2_59", "S2_60", "S2_63", "S2_64", "S2_65", "S2_67", "S2_68", "S2_71", "S2_72",
    "S3_1", "S3_3", "S3_4", "S3_7", "S3_8", "S3_9", "S3_11", "S3_12", "S3_15", "S3_16", "S3_17", "S3_19", "S3_20", "S3_23", "S3_24", "S3_25", "S3_27", "S3_28", "S3_31", "S3_32", "S3_33", "S3_35", "S3_36", "S3_39", "S3_40", "S3_41", "S3_43", "S3_44", "S3_47", "S3_48", "S3_49", "S3_51", "S3_52", "S3_55", "S3_56", "S3_57", "S3_59", "S3_60", "S3_63", "S3_64", "S3_65", "S3_67", "S3_68", "S3_71", "S3_72",
    "S4_1", "S4_3", "S4_4", "S4_7", "S4_8", "S4_9", "S4_11", "S4_12", "S4_15", "S4_16", "S4_17", "S4_19", "S4_20", "S4_23", "S4_24", "S4_25", "S4_27", "S4_28", "S4_31", "S4_32", "S4_33", "S4_35", "S4_36", "S4_39", "S4_40", "S4_41", "S4_43", "S4_44", "S4_47", "S4_48", "S4_49", "S4_51", "S4_52", "S4_55", "S4_56", "S4_57", "S4_59", "S4_60", "S4_63", "S4_64", "S4_65", "S4_67", "S4_68", "S4_71", "S4_72",
    "S5_1", "S5_3", "S5_4", "S5_7", "S5_8", "S5_9", "S5_11", "S5_12", "S5_15", "S5_16", "S5_17", "S5_19", "S5_20", "S5_23", "S5_24", "S5_25", "S5_27", "S5_28", "S5_31", "S5_32", "S5_33", "S5_35", "S5_36", "S5_39", "S5_40", "S5_41", "S5_43", "S5_44", "S5_47", "S5_48", "S5_49", "S5_51", "S5_52", "S5_55", "S5_56", "S5_57", "S5_59", "S5_60", "S5_63", "S5_64", "S5_65", "S5_67", "S5_68", "S5_71", "S5_72",
    "S6_1", "S6_3", "S6_4", "S6_7", "S6_8", "S6_9", "S6_11", "S6_12", "S6_15", "S6_16", "S6_17", "S6_19", "S6_20", "S6_23", "S6_24", "S6_25", "S6_27", "S6_28", "S6_31", "S6_32", "S6_33", "S6_35", "S6_36", "S6_39", "S6_40", "S6_41", "S6_43", "S6_44", "S6_47", "S6_48", "S6_49", "S6_51", "S6_52", "S6_55", "S6_56", "S6_57", "S6_59", "S6_60", "S6_63", "S6_64", "S6_65", "S6_67", "S6_68", "S6_71", "S6_72",
    "S7_1", "S7_3", "S7_4", "S7_7", "S7_8", "S7_9", "S7_11", "S7_12", "S7_15", "S7_16", "S7_17", "S7_19", "S7_20", "S7_23", "S7_24", "S7_25", "S7_27", "S7_28", "S7_31", "S7_32", "S7_33", "S7_35", "S7_36", "S7_39", "S7_40", "S7_41", "S7_43", "S7_44", "S7_47", "S7_48", "S7_49", "S7_51", "S7_52", "S7_55", "S7_56", "S7_57", "S7_59", "S7_60", "S7_63", "S7_64", "S7_65", "S7_67", "S7_68", "S7_71", "S7_72",
    "S8_1", "S8_3", "S8_4", "S8_7", "S8_8", "S8_9", "S8_11", "S8_12", "S8_15", "S8_16", "S8_17", "S8_19", "S8_20", "S8_23", "S8_24", "S8_25", "S8_27", "S8_28", "S8_31", "S8_32", "S8_33", "S8_35", "S8_36", "S8_39", "S8_40", "S8_41", "S8_43", "S8_44", "S8_47", "S8_48", "S8_49", "S8_51", "S8_52", "S8_55", "S8_56", "S8_57", "S8_59", "S8_60", "S8_63", "S8_64", "S8_65", "S8_67", "S8_68", "S8_71", "S8_72",
    "S9_1", "S9_3", "S9_4", "S9_7", "S9_8", "S9_9", "S9_11", "S9_12", "S9_15", "S9_16", "S9_17", "S9_19", "S9_20", "S9_23", "S9_24", "S9_25", "S9_27", "S9_28", "S9_31", "S9_32", "S9_33", "S9_35", "S9_36", "S9_39", "S9_40", "S9_41", "S9_43", "S9_44", "S9_47", "S9_48", "S9_49", "S9_51", "S9_52", "S9_55", "S9_56", "S9_57", "S9_59", "S9_60", "S9_63", "S9_64", "S9_65", "S9_67", "S9_68", "S9_71", "S9_72",
    "S10_1", "S10_3", "S10_4", "S10_7", "S10_8", "S10_9", "S10_11", "S10_12", "S10_15", "S10_16", "S10_17", "S10_19", "S10_20", "S10_23", "S10_24", "S10_25", "S10_27", "S10_28", "S10_31", "S10_32", "S10_33", "S10_35", "S10_36", "S10_39", "S10_40", "S10_41", "S10_43", "S10_44", "S10_47", "S10_48", "S10_49", "S10_51", "S10_52", "S10_55", "S10_56", "S10_57", "S10_59", "S10_60", "S10_63", "S10_64", "S10_65", "S10_67", "S10_68", "S10_71", "S10_72",
    "B1_1", "B1_3", "B1_4", "B1_7", "B1_8", "B1_9", "B1_11", "B1_12", "B1_15", "B1_16", "B1_17", "B1_19", "B1_20", "B1_23", "B1_24", "B1_25", "B1_27", "B1_28", "B1_31", "B1_32", "B1_33", "B1_35", "B1_36", "B1_39", "B1_40", "B1_41", "B1_43", "B1_44", "B1_47", "B1_48", "B1_49", "B1_51", "B1_52", "B1_55", "B1_56", "B1_57", "B1_59", "B1_60", "B1_63", "B1_64",
    "B2_1", "B2_3", "B2_4", "B2_7", "B2_8", "B2_9", "B2_11", "B2_12", "B2_15", "B2_16", "B2_17", "B2_19", "B2_20", "B2_23", "B2_24", "B2_25", "B2_27", "B2_28", "B2_31", "B2_32", "B2_33", "B2_35", "B2_36", "B2_39", "B2_40", "B2_41", "B2_43", "B2_44", "B2_47", "B2_48", "B2_49", "B2_51", "B2_52", "B2_55", "B2_56", "B2_57", "B2_59", "B2_60", "B2_63", "B2_64",
    "B3_1", "B3_3", "B3_4", "B3_7", "B3_8", "B3_9", "B3_11", "B3_12", "B3_15", "B3_16", "B3_17", "B3_19", "B3_20", "B3_23", "B3_24", "B3_25", "B3_27", "B3_28", "B3_31", "B3_32", "B3_33", "B3_35", "B3_36", "B3_39", "B3_40", "B3_41", "B3_43", "B3_44", "B3_47", "B3_48", "B3_49", "B3_51", "B3_52", "B3_55", "B3_56", "B3_57", "B3_59", "B3_60", "B3_63", "B3_64",
    "A1_1", "A1_2", "A1_3", "A1_4", "A1_5", "A1_6", "A1_7", "A1_8", "A1_9", "A1_10", "A1_11", "A1_12", "A1_13", "A1_14", "A1_15", "A1_16", "A1_17", "A1_18", "A1_19", "A1_20", "A1_21", "A1_22", "A1_23", "A1_24", "A1_25", "A1_26", "A1_27", "A1_28", "A1_29", "A1_30", "A1_31", "A1_32", "A1_33", "A1_34", "A1_35", "A1_36", "A1_37", "A1_38", "A1_39", "A1_40", "A1_41", "A1_42", "A1_43", "A1_44", "A1_45", "A1_46", "A1_47", "A1_48",
    "A2_1", "A2_2", "A2_3", "A2_4", "A2_5", "A2_6", "A2_7", "A2_8", "A2_9", "A2_10", "A2_11", "A2_12", "A2_13", "A2_14", "A2_15", "A2_16", "A2_17", "A2_18", "A2_19", "A2_20", "A2_21", "A2_22", "A2_23", "A2_24", "A2_25", "A2_26", "A2_27", "A2_28", "A2_29", "A2_30", "A2_31", "A2_32", "A2_33", "A2_34", "A2_35", "A2_36", "A2_37", "A2_38", "A2_39", "A2_40", "A2_41", "A2_42", "A2_43", "A2_44", "A2_45", "A2_46", "A2_47", "A2_48",
    "1A_1", "1A_2", "1A_3", "1A_4", "1A_5", "1A_6", "1A_7", "1A_8", "1A_9", "1A_10", "1A_11", "1A_12", "1A_13", "1A_14", "1A_15", "1A_16", "1A_17", "1A_18"]

    
    seat_array_set = set(seat_array)
    PREFIX = "Railway_"
    SUFFIX="_seat_alloc"
    # action = None
    print("out----------------------1")
    # for key in request.POST.keys():
    #     print("out----------------------")
    #     if key.startswith('action:'):
    #         action = key[7:]
    #         print("in---------------------------")
    #         break    
    # if 'list' in request.POST[]:
    # train_name = request.GET.get_id()
    
    
    for i in range(Demo.no_of_Seats):
        print('name'+str(i))
        try:
            print("post",Demo.no_of_Seats)
            
            name = request.POST['name'+str(i)] 
            print(name)
            names.append(name)
        except:
            name = False
            names.append(name)
        print(names)
        print('age'+str(i))
        try:
            age = request.POST['age'+str(i)]
            print(age)
            ages.append(age)
            print("hello world 1")
            print(ages)
            print("hello world 2")
        except:
            age = False
        
        try:
            id_proof = request.POST['id_proof'+str(i)]
            id_proofs.append(id_proof)

        except:
            id_proof = False
        
        try:
            id_number = request.POST['id_number'+str(i)]
            id_numbers.append(id_number)
        except:
            id_number = False
        
        try:
            class_type = request.POST['class_type'+str(i)]
            class_types.append(class_type)
        except:
            class_type = False
        
        try:
            birth_preferance = request.POST['birth_preferance'+str(i)]
            birth_preferances.append(birth_preferance)
        except:
            birth_preferance = False
        
        with connection.cursor() as cursor:
            cursor.execute("select \"group_id\" from public.\"Railway_registration\" order by \"group_id\" desc limit 1")
            l1 = list(cursor.fetchone())  
        group_id = l1[0] + 1
        #print(group_id)
    
    try:
        if request.user.is_authenticated:
            email1 = request.user.email
        print(Demo.no_of_Seats)

        for i in range(Demo.no_of_Seats):
            with connection.cursor() as cursor:
                print(Demo.no_of_Seats)
                query="select \"PNR\" from public.\"Railway_registration\" order by \"PNR\" desc limit 1"
                cursor.execute(query)
                p=list(cursor.fetchone())
                pnr=p[0]+1
                pnr_list.append(pnr)
                
            print("---------------------------------------------------------")
            sql="insert into \"Railway_registration\"(\"source\", \"destination\", \"date_of_journey\", \"no_of_Seats\", \"name\", \"age\", \"id_proof\", \"id_number\", \"class_type\", \"birth_preferance\",\"group_id\",\"email\",\"train_name\",\"src_date\",\"medical_status\",\"PNR\",\"medical\") values('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(source, destination, date_of_journey, Demo.no_of_Seats, names[i], ages[i], id_proofs[i], id_numbers[i], class_types[i], birth_preferances[i], group_id,email1,train_name,src_date,"pending",str(pnr),"registered")
            #print (sql)
            #print(group_id)
            print (Demo.no_of_Seats)
            with connection.cursor() as cursor:
                cursor.execute(sql)
                print("--------------------------------------------------------------------------------------------")
        
        
    except(Exception, psycopg2.Error) as error:
        print("error",error)
        
    with connection.cursor() as cursor:
        table_name = "seat_alloc"
        query = "select \"intermediate_station\" FROM public.\"Railway_railwayroute\" where \"name\" = '{}'".format(train_name)
        print(query)
        cursor.execute(query)
        final_intermediate_stations = cursor.fetchall()
        final_intermediate_stations = list(chain.from_iterable(list(chain.from_iterable(final_intermediate_stations))))
       
        source_index = 0
        dest_index = len(final_intermediate_stations)
       
         
        query = "select \"group_id\", \"source\", \"destination\", \"date_of_journey\", \"name\", \"birth_preferance\", \"class_type\", \"PNR\" FROM public.\"Railway_registration\" where \"group_id\" = '{}'".format(group_id)
        #print(query)
        cursor.execute(query)
        q = cursor.fetchall()
        print(q)
        for record in q:
            lst = record[1].split("(")
            station_name = lst[0]
            srs = station_name.replace(" ","_")
        
            
            dest = record[2].split("(")
            station_name= dest[0]
            final_dest = station_name.replace(" ","_")
            
            
            sql = "SELECT \"{}\" from public.\"{}{}{}\" where \"date\" = '{}'".format(srs,PREFIX,train_name,SUFFIX,record[3])
            #print(sql)
            cursor.execute(sql)
            booked_seat = cursor.fetchall()
            #print(booked_seat)
            booked_seat = list(chain.from_iterable(list(chain.from_iterable(booked_seat))))
            #print(booked_seat)
            book_set = set(booked_seat)
            #print(book_set)
            
            query = "SELECT \"{}\" from public.\"{}{}{}\" where \"date\" = '{}'".format(final_dest,PREFIX,train_name,SUFFIX,record[3])
            #print(query)

            cursor.execute(query)
            booked_dest = cursor.fetchall()
            #print(booked_dest)
            booked_dest = list(chain.from_iterable(booked_dest))
            #print(booked_dest)

            unbook_set = seat_array_set - book_set
            #print(unbook_set)
            unbook_seat = list(unbook_set) 
            #print(unbook_seat)
            
            query = "select \"seat_no\" from public.\"{}{}\" where \"birth_type\" = '{}' and \"class_type\" = '{}'".format(PREFIX,"seat_alloc",record[5],record[6])
            print(query)
            cursor.execute(query)
            final_seats = cursor.fetchall()
            final_seats = list(chain.from_iterable(final_seats))
            #print(final_seats)

            
            for i in range(dest_index):
                if record[1] == final_intermediate_stations[i]:
                    source_index = i
                if record[2] == final_intermediate_stations[i]:
                    dest_index = i
    
            pre_final_dest = final_intermediate_stations[dest_index - 1].replace(" ","_").split("(")[0]
            query = "SELECT \"{}\" from public.\"{}{}{}\" where \"date\" = '{}'".format(pre_final_dest,PREFIX,train_name,SUFFIX,record[3])
            #print(query)
            cursor.execute(query)
            pre_booked_dest = cursor.fetchall()
            #print(pre_booked_dest)
            pre_booked_dest = list(chain.from_iterable(list(chain.from_iterable(pre_booked_dest))))
            #print(pre_booked_dest)

            query = "select \"seat_no\" from public.\"Railway_seat_alloc\" where \"class_type\" = '{}'".format(record[6])
            #print(query)
            cursor.execute(query)
            cls_type = cursor.fetchall()
            cls_type = list(chain.from_iterable(cls_type))
            
            query = "select \"seat_no\" from public.\"Railway_seat_alloc\" where \"birth_type\" = '{}'".format(record[5])
            #print(query)
            cursor.execute(query)
            bth_type = cursor.fetchall()
            bth_type = list(chain.from_iterable(bth_type))
            

            # for seat in unbook_seat:

            #     for j in range(source_index,dest_index):
            #         lst = final_intermediate_stations[j].split("(")
            #         station_name= lst[0]
            #         st = station_name.replace(" ","_")
                        
            #         print(st)

            #         query = "select \"{}\" from public.\"Railway_{}_seat_alloc\" where date = '{}'".format(st, train_name,record[3])
            #         print(query)
            #         cursor.execute(query)
            #         station_seats = cursor.fetchall()
            #         station_seats = list(chain.from_iterable(list(chain.from_iterable(station_seats))))

            #         if seat not in station_seats:
            #             continue
            #         else:
            #             print("end:",j)
            #             break
            #     print("J:",j+1)
            #     print("dest_index",dest_index)
            #     if j+1 == dest_index:        
            #         counter = 0
            #         if seat in cls_type:
            #             counter = counter + 1
            #             counter1 = 0
            #             if seat in bth_type:
            #                 counter1 = counter1 + 1
            #                 break
            
            # if counter > 0 and counter1 > 0:
            #     print("pref wala-----------------------------------------------------------------------------------------------------")
            # elif counter > 0 and counter1 == 0:
            #     print("unpref wala----------------------------------------------------------------------------------------------------------")
            # else:
            #     print("wl or new train-------------------------------------------------------------------------------------------------------")
            status = "nothing"
            for seat in unbook_seat:  
                # print("seat:",seat)
                # print("seat in unbook_seat :",seat in unbook_seat)
                # print("seat not in booked_dest :",seat not in booked_dest)
                # print("seat not in pre_booked_dest :",seat not in pre_booked_dest)
                if seat in final_seats and seat not in booked_dest and seat not in pre_booked_dest:
                    # sql = "update public.\"{}{}{}\" set \"{}\""                     
                    dt = record[2]
                    
                    
                    for j in range(source_index,dest_index):
                        lst = final_intermediate_stations[j].split("(")
                        station_name= lst[0]
                        st = station_name.replace(" ","_")
                        
                        #print(st)

                        query = "select \"{}\" from public.\"Railway_{}_seat_alloc\" where date = '{}'".format(st, train_name,record[3])
                        #print(query)
                        cursor.execute(query)
                        station_seats = cursor.fetchall()
                        station_seats = list(chain.from_iterable(list(chain.from_iterable(station_seats))))

                        if seat not in station_seats:
                            continue
                        else:
                            #print("end:",j)
                            break
                    #print("J:",j+1)
                    #print("dest_index",dest_index)
                    if j+1 == dest_index:
                            
                        status = "preferance"
                        for i in range(source_index,dest_index):
                            lst = final_intermediate_stations[i].split("(")
                            station_name= lst[0]
                            st = station_name.replace(" ","_")

                            query = "select \"{}\" from public.\"Railway_{}_seat_alloc\" where date = '{}'".format(st, train_name,record[3])
                            #print(query)
                            cursor.execute(query)
                            station_seats = cursor.fetchall()
                            booked_seat = list(chain.from_iterable(list(chain.from_iterable(station_seats))))
                            booked_seat.append(seat)
                        
                            string = "{"
                            for i in range(len(booked_seat)-1):
                                string = string + booked_seat[i]
                                string = string +","
                        
                            string = string + booked_seat[len(booked_seat)-1]
                            
                            string = string + "}"
                            

                        
                            # update public."Railway_pune_bsl_express_seat_alloc" set "Pune_Junction" = '{"S9_1","S9_2"}' where "date" = '2020-07-06'
                            sql = "update public.\"{}{}{}\" set \"{}\" = '{}' WHERE \"date\" = '{}'".format("Railway_",train_name,"_seat_alloc",st,string ,record[3])
                            #print(sql)
                            cursor.execute(sql)
                        
                        query = "select \"birth_type\" from public.\"{}{}\" where \"seat_no\" = '{}'".format(PREFIX,"seat_alloc",seat)
                        #print(query)
                        cursor.execute(query)
                        birth = cursor.fetchall()
                        birth_pref = list(chain.from_iterable(birth))[0]
                        
                        

                        query = "update public.\"Railway_registration\" set \"birth_preferance\" = '{}' where \"PNR\" = '{}'".format(birth_pref, record[7])
                        #print(query)
                        cursor.execute(query)


                        query = "insert into public.\"Railway_{}_booked\"(\"group_id\", \"seat\", \"source\", \"destination\", \"date_of_journey\", \"name\", \"birth_type\",\"PNR\") values('{}','{}','{}','{}','{}','{}','{}','{}')".format(train_name,record[0],seat,record[1],record[2],record[3],record[4],birth_pref,pnr_list[q.index(record)])
                        #print(query)
                        cursor.execute(query)
                        break

                    else:
                        print("Successfullllllllllllllllllllllllllllllllllllllllll")
            

                else:
                    
                    
                    for j in range(source_index,dest_index):
                        lst = final_intermediate_stations[j].split("(")
                        station_name= lst[0]
                        st = station_name.replace(" ","_")

                        query = "select \"{}\" from public.\"Railway_{}_seat_alloc\" where date = '{}'".format(st, train_name,record[3])
                        cursor.execute(query)
                        station_seats = cursor.fetchall()
                        station_seats = list(chain.from_iterable(list(chain.from_iterable(station_seats))))
                        # print(station_seats)
                        # print("seat not in station_seats",seat not in station_seats)
                        if seat not in station_seats:
                            continue
                        else:
                            # print("end:",j)
                            break
                    # print("J:",j+1)
                    # print("dest_index",dest_index)
                    if j+1 == dest_index:
                        
                        
                        if seat in cls_type and seat not in booked_seat and seat not in booked_dest and seat not in pre_booked_dest:
                            status = "unpreferance"
                            
                            for i in range(source_index,dest_index):
                                lst = final_intermediate_stations[i].split("(")
                                station_name= lst[0]
                                st = station_name.replace(" ","_")

                                query = "select \"{}\" from public.\"Railway_{}_seat_alloc\" where date = '{}'".format(st, train_name,record[3])
                                cursor.execute(query)
                                station_seats = cursor.fetchall()
                                booked_seat = list(chain.from_iterable(list(chain.from_iterable(station_seats))))
                                booked_seat.append(seat)
                        
                        
                                # print("----------------------------------------------------",booked_seat)
                                string = "{"
                                for i in range(len(booked_seat)-1):
                                    string = string + booked_seat[i]
                                    string = string +","
                        
                                string = string + booked_seat[len(booked_seat)-1]
                            
                                string = string + "}"
                                # print(string)

                        
                                # update public."Railway_pune_bsl_express_seat_alloc" set "Pune_Junction" = '{"S9_1","S9_2"}' where "date" = '2020-07-06'
                                sql = "update public.\"{}{}{}\" set \"{}\" = '{}' WHERE \"date\" = '{}'".format("Railway_",train_name,"_seat_alloc",st,string ,record[3])
                                # print(sql)
                                cursor.execute(sql)

                            query = "select \"birth_type\" from public.\"{}{}\" where \"seat_no\" = '{}'".format(PREFIX,"seat_alloc",seat)
                            # print(query)
                            cursor.execute(query)
                            birth = cursor.fetchall()
                            birth_pref = list(chain.from_iterable(birth))[0]
                            # print(birth_pref)

                            
                        
                            query = "update public.\"Railway_registration\" set \"birth_preferance\" = '{}' where \"PNR\" = '{}'".format(birth_pref, record[7])
                            # print(query)
                            cursor.execute(query)
                        

                            query = "insert into public.\"Railway_{}_booked\"(\"group_id\", \"seat\", \"source\", \"destination\", \"date_of_journey\", \"name\", \"birth_type\", \"PNR\") values('{}','{}','{}','{}','{}','{}','{}','{}')".format(train_name,record[0],seat,record[1],record[2],record[3],record[4],birth_pref,pnr_list[q.index(record)])
                            print(query)
                            cursor.execute(query)
                            break
            
            if not (status == "preferance" or status == "unpreferance"):
                seats = dict()
                seats["Sleeper"] = 450
                seats["3AC"] = 120
                seats["2AC"] = 96
                seats["1AC"] = 18

                query = "select \"seat\" from public.\"Railway_{}_booked\" where \"date_of_journey\" = '{}' and \"source\" = '{}'".format(train_name,record[3],record[1])
                cursor.execute(query)
                seats_array = cursor.fetchall()
                seats_array = list(chain.from_iterable(seats_array))


                query = "select \"seat\" from public.\"Railway_{}_booked\" where \"date_of_journey\" = '{}' and \"source\" = '{}'".format(train_name,record[3],record[1])+" and (\"seat\" like \'S%\' or \"seat\" like \'SWL__%\') "
                cursor.execute(query)
                sleeper_array = cursor.fetchall()
                sleeper_array = list(chain.from_iterable(sleeper_array))
                

                query = "select \"seat\" from public.\"Railway_{}_booked\" where \"date_of_journey\" = '{}' and \"source\" = '{}'".format(train_name,record[3],record[1])+" and (\"seat\" like \'B%\' or \"seat\" like \'3AWL_%\') "
                cursor.execute(query)
                ac3_array = cursor.fetchall()
                ac3_array = list(chain.from_iterable(ac3_array))
                


                query = "select \"seat\" from public.\"Railway_{}_booked\" where \"date_of_journey\" = '{}' and \"source\" = '{}'".format(train_name,record[3],record[1])+" and (\"seat\" like \'A%\' or \"seat\" like \'2AWL_%\') "
                cursor.execute(query)
                ac2_array = cursor.fetchall() 
                ac2_array = list(chain.from_iterable(ac2_array))
                

                query = "select \"seat\" from public.\"Railway_{}_booked\" where \"date_of_journey\" = '{}' and \"source\" = '{}'".format(train_name,record[3],record[1])+" and (\"seat\" like \'1A%\' or \"seat\" like \'1AWL_%\') "
                cursor.execute(query)
                ac1_array = cursor.fetchall()
                ac1_array = list(chain.from_iterable(ac1_array))
               








                # print(seats_array)

                s = []
                a1 = []
                a2 = []
                a3 = []
                # print("seats array:",seats_array)

                for element in seats_array:
                    if element in sleeper_array:
                        s.append(element)
                    elif element in ac3_array:
                        a3.append(element)
                    elif element in ac2_array:
                        a2.append(element)
                    elif element in ac1_array:
                        a1.append(element)

                            
                if record[6] =="Sleeper":
                    booked_seat = s
                elif record[6] =="3AC":
                    booked_seat = a3
                elif record[6] =="2AC":
                    booked_seat = a2
                elif record[6] =="1AC":
                    booked_seat = a1

                print("s",s)
                print("a1:",a1)
                print("a2:",a2)
                print("a3",a3)
                print(len(booked_seat))
                if len(booked_seat) > seats[record[6]] and  len(booked_seat) < seats[record[6]] + 150:
                    print("inif")
                    print(seats[record[6]])
                    count = str(len(booked_seat) - seats[record[6]]) 
                    print(count)
                    if record[6] == "Sleeper":
                        wl = "SWL_" + count 
                    elif record[6] == "3AC":
                        wl = "3AWL_" + count 
                    elif record[6] == "2AC":
                        wl = "2AWL_" + count
                    else:
                        wl = "1AWL_" + count
                                
                    booked_seat.append(wl)
                    for i in range(source_index,dest_index):
                        print("infor")
                        lst = final_intermediate_stations[i].split("(")
                        station_name= lst[0]
                        st = station_name.replace(" ","_")

                        query = "select \"{}\" from public.\"Railway_{}_seat_alloc\" where date = '{}'".format(st, train_name,record[3])
                        cursor.execute(query)
                        station_seats = cursor.fetchall()
                        booked_seat = list(chain.from_iterable(list(chain.from_iterable(station_seats))))
                        booked_seat.append(wl)
                        
                        
                        # print("----------------------------------------------------",booked_seat)
                        string = "{"
                        for i in range(len(booked_seat)-1):
                            string = string + booked_seat[i]
                            string = string +","
                        
                        string = string + booked_seat[len(booked_seat)-1]
                            
                        string = string + "}"
                        # print(string)

                        
                        # update public."Railway_pune_bsl_express_seat_alloc" set "Pune_Junction" = '{"S9_1","S9_2"}' where "date" = '2020-07-06'
                        sql = "update public.\"{}{}{}\" set \"{}\" = '{}' WHERE \"date\" = '{}'".format("Railway_",train_name,"_seat_alloc",st,string ,record[3])
                        print(sql)
                        cursor.execute(sql)

                        # query = "select \"birth_type\" from public.\"{}{}\" where \"seat_no\" = '{}'".format(PREFIX,"seat_alloc",seat)
                        # print(query)
                        # cursor.execute(query)
                        # birth = cursor.fetchall()
                        # birth_pref = list(chain.from_iterable(birth))[0]
                        # # print(birth_pref)
                            
                                
                        
                        # query = "update public.\"Railway_registration\" set \"birth_preferance\" = '{}' where \"PNR\" = '{}'".format(birth_pref, record[7])
                        # print(query)
                        # cursor.execute(query)

                    query = "insert into public.\"Railway_{}_booked\"(\"group_id\", \"seat\", \"source\", \"destination\", \"date_of_journey\", \"name\", \"birth_type\", \"PNR\") values('{}','{}','{}','{}','{}','{}','{}','{}')".format(train_name,record[0],wl,record[1],record[2],record[3],record[4],record[5],pnr_list[q.index(record)])
                    print(query)
                    cursor.execute(query)

                else:
                    query = "select \"{}\" from public.\"Railway_{}_seat_alloc\" where date = '{}'".format(st, train_name,record[3])
                    cursor.execute(query)
                    station_seats = cursor.fetchall()
                    booked_seat = list(chain.from_iterable(list(chain.from_iterable(station_seats))))
                    if len(booked_seat) == 834:
                        print("Train have no vaccant seat")
                        j = 0
                        for train_name in train:
                            print("hello ji")
                            query="select count(seat) from public.\"{}{}{}\"".format(PREFIX,train_name,"_booked")+" where date_of_journey ='"+str(record[3])+"'"
                            print("hello ji2")
                            print(query)
                            cursor.execute(query)
                            count1 = list(cursor.fetchone())
                            counter = count1[0]
                                        
                            if counter == 834:
                                j = j + 1
                                continue
                            else:
                                break
                        print(j)
                        if j == len(train):
                            source_array = []
                            destination_array = []
                            for train_name in train:
                                query = "select source, count(source) from public.\"{}{}{}\"".format(PREFIX,train_name,"_booked")+" group by (source,date_of_journey) having \"date_of_journey\" = '{}' ".format(record[3])
                                cursor.execute(query)
                                output = cursor.fetchall()
                                source_array.append(output)
                        
                                query = "select destination, count(destination) from public.\"{}{}{}\"".format(PREFIX,train_name,"_booked")+" group by (destination,date_of_journey) having \"date_of_journey\" = '{}'".format(record[3])
                                cursor.execute(query)
                                output = cursor.fetchall()
                                destination_array.append(output)
                        
                            source_array = dict(chain.from_iterable(source_array))
                            print(source_array)
                            destination_array = dict(chain.from_iterable(destination_array))
                            print(destination_array)

                            sort_source_array = sorted(source_array.items(), key=lambda x: x[1], reverse=True)
                            print(sort_source_array)
                            sort_destination_array = sorted(destination_array.items(), key=lambda x: x[1], reverse=True)
                            print(sort_destination_array)

                            new_source = sort_source_array[0][0]
                            print(new_source)
                            new_destination = sort_destination_array[0][0]
                            print(new_destination)

                            query = "select \"name\" from public.\"Railway_railwayroute\" where '{}' = ANY(intermediate_station) and '{}' = ANY(intermediate_station)".format(new_source,new_destination)
                            print(query)
                            cursor.execute(query)
                            new_trains = cursor.fetchall()
                            new_trains = chain.from_iterable(new_trains)
                            print(new_trains)
                            for i in new_trains:
                                d1=[]
                                data1="select  \"No\"  from public.\"{}{}\" ".format(PREFIX,i.lower())+" where \"StationName\" ='" + new_source +"'"# or \"StationName\" ='"+To+"'"
                                data2="select  \"No\"  from public.\"{}{}\" ".format(PREFIX,i.lower())+" where \"StationName\" ='" + new_destination +"'"
                    
                                print(data1)
                                print(data2)
                    
                    
                                cursor.execute(data1)
                                data11=cursor.fetchall()
                                print("heloo world")
                    
                    
                                cursor.execute(data2)
                                data21=cursor.fetchall()
                                print(data21)

                                d1.append(data11[0])
                                d1.append(data21[0])
                                print(d1)
                    
                                # d1=list(chain.from_iterable(d1)) 
                                # print(d1)
                                #print(d1[0])
                                #print(d1[1])
                                print(d1[0])
                                print(d1[1])
                                if (d1[0]<d1[1]):
                                    new_train = i.lower()
                                    break
                                print(new_train)
                                digits = [i for i in range(0,10)]
                                r = ""
                                for i in range(6):
                                    i = math.floor(random.random()*10)
                                    r += str(digits[i])
                                trainNo = r 
                                query = "select \"source\", \"destination\", \"intermediate_station\" from public.\"Railway_railwayroute\" where \"name\" = '{}'".format(new_train)
                                print(query)
                                cursor.execute(query)
                                data = cursor.fetchall()
                                data = list(chain.from_iterable(data))
                                inter = "{"
                                for i in range(len(data[2])-1):
                                    inter += "\""
                                    inter += data[2][i]
                                    inter += "\""
                                    inter += ","
                                inter += "\""
                                inter += data[2][i+1]
                                inter += "\"}"
                                print(inter)
                    
                                query = "insert or replace into public.\"Railway_railwayroute\"(\"trainNo\", \"name\", \"source\", \"destination\", \"intermediate_station\")values('{}','extra_train_{}_{}','{}','{}','{}')".format(trainNo,data[0].replace(" ","_").split("(")[0],data[1].replace(" ","_").split("(")[0],data[0],data[1],inter)
                                print(query)
                                cursor.execute(query)
                                    
                                query = "create or replace table \"Railway_extra_{}_{}_seat_alloc\" as(select * from public.\"Railway_{}_seat_alloc\" where 1=2)".format(data[0].replace(" ","_").split("(")[0].lower(),data[1].replace(" ","_").split("(")[0].lower(),new_train) 
                                print(query)
                                cursor.execute(query)
                                    
                                query = "select count(*) from information_schema.columns where table_name = 'Railway_extra_{}_{}_seat_alloc'"
                                print(query)
                                cursor.execute(query)
                                    
                                no = list(cursor.fetchall)
                                n = no[0]
                                string = ""
                                for i in range(n-3):
                                    string = string + "'{}',"
                                string = string + "'{}'"
                                
                                query = "insert into 'Railway_extra_{}_{}_seat_alloc' values('{}','{}','{}')".format(data[0].replace(" ","_").split("(")[0].lower(), data[1].replace(" ","_").split("(")[0].lower(), 1, record[3], string)
                                print(query)
                                cursor.execute(query)
                                query = "create or replace table \"Railway_extra_{}_{}_booked\" as(select * from public.\"Railway_{}_booked\" where 1=2)".format(data[0].replace(" ","_").split("(")[0].lower(),data[1].replace(" ","_").split("(")[0].lower(),new_train) 
                                print(query)
                                cursor.execute(query)
                                    
                                query = "select * from public.\"Railway_{}\" where \"name\"='"+new_train.lower()+"'"
                                cursor.execute(query)
                                times = cursor.fetchall()
                                times = list(chain.from_iterable(times))
                                arrival = []
                                depart = []
                                for i in range(len(data[2])):
                                    old_time1 = dt.datetime.combine(record[3],times[i][4]) 
                                    arrival = old_time1 + timedelta(hours=6, minutes=0)
                                    old_time2 = dt.datetime.combine(record[3],times[i][5])
                                    depart = old_time2 + timedelta(hours=6, minutes=0)            
                                    d1 = datetime.date(old_time1)
                                    d2 = datetime.date(arrival)
                                    day = (d2 - d1).days + 1
                                    query = "insert into \"Railway_{}_{}\"(\"id\", \"trainNo\", \"No\", \"StationName\", \"Arrives\", \"Departs\", \"StopTime\", \"DistanceTravelled\", \"Day\")values('{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(data[0].replace(" ","_").split("(")[0], data[1].replace(" ","_").split("(")[0], times[i][0], trainNo, times[i][2], times[i][3], arrival, depart, times[i][6], times[i][7], day)
                                    cursor.execute(query)


                # query = "select \"group_id\",\"name\",\"date_of_journey\",\"source\",\"destination\" from pulic.\"{}{}\" where \"group_id\" = '{}'".format(Demo.PREFIX,"registration",Demo.group_id)
                # cursor.execute(query)
                # details = cursor.fetchall()
                # details = list(chain.from_iterable(details))
    s=smtplib.SMTP('smtp.gmail.com',587)
    
    s.ehlo()
                        
    s.starttls()
                        
    s.login('boiii2412@gmail.com','motorcop')
                        
    subject = 'INDIAN RAILWAYS- Registration Confirmed '
    #body = 'HEY',FULLNAME,'!!,You have booked a', CARNAME ,'from ',PICKDATE,'to',DROPDATE,',.This is to inform you that your booking is CONFIRMED' 
    #body="You have Succefully Registered a journey for", Demo.no_of_Seats " From ",source" To ", destination" on ",date_of_journey 
    body="Hello {} You have Successfully Registered a journey for {} From {} To {} on {} . Please Upload medical Certificate in given time.You Can check the time slot in >pending medical tab  ".format(request.user.first_name,Demo.no_of_Seats,source,destination,date_of_journey)  
    message = f'Subject : {subject}\n\n {body}'
                        
    s.sendmail('boiii2412@gmail.com',request.user.email,message)
                        
    print ('HEY AN EMAIL HAS BEEN SENT!')
                        
    s.quit()            
    return render(request,"seatAlloc.html") 
 

    

source = ""
destination = ""
date_of_journey = date.today()
group_id = 0
def registration(request):
    return render(request, 'registration.html')

def afterregistration(request):    
    global source 
    global destination
    global date_of_journey
    global group_id
    final_no_of_seats=[]
    global email
    global From
    global To
    global DATE
    try:
        source = From
    except:
        source = False

    try:
        destination =To
    except:
        destination = False

    try:
        date_of_journey =DATE
    except:
        date_of_journey = False

    try:
        Demo.no_of_Seats = int(request.POST['no_of_Seats'])    
        print(Demo.no_of_Seats)
    except:
        Demo.no_of_Seats = False
        print(Demo.no_of_Seats)
    try:
        # Demo.group_id += 1
        for i in range(Demo.no_of_Seats):
            final_no_of_seats.append(i)
        print(final_no_of_seats)
        print(email)
         
    except(Exception) as error:
        print("error",error)
        # Demo.group_id=False
        #group_id=False
    return render(request, 'afterregistration.html',{"final_no_of_seats":final_no_of_seats})


           
        


def history(request):
    global email
    msg="no bookings yet"

    with connection.cursor() as cursor:
        if request.user.is_authenticated:
            email1 = request.user.email
        query="select \"name\",\"source\",\"destination\",\"date_of_journey\",\"medical_status\" from public.\"Railway_registration\" where \"email\"='"+email1+"'"
        print(query)
        cursor.execute(query)
        hs1=cursor.fetchall()
       
        if len(hs1)==0:
            return render(request,"history.html",{"msg":msg})
        

    return render(request,"history.html",{"hs1":hs1})


def pendingmedical(request):
    global email
    msg="NOTHING TO SHOW "
    global  hs
    ks=[]
    global grp
    source_date=[]
    g_d=date.today()
    train_n=[]
    src_time=[]
    final_time=[]
    rem_time=[]
    to_time=[]

    with connection.cursor() as cursor:
        #query="select \"name\",\"source\",\"destination\",\"date_of_journey\",\"train_name\",\"no_of_Seats\",\"medical_status\" from public.\"Railway_registration\" where \"email\"='"+email+"' and \"medical_status\"='pending'"
        #  user=User.objects.get()
        #  user_email=user.email
        if request.user.is_authenticated:
            email1 = request.user.email
        query="select distinct(group_id) from public.\"Railway_registration\" where \"email\"='"+email1+"' and \"medical_status\"='pending'"
        print(query)
        cursor.execute(query)
        a=cursor.fetchall()
        print(a)
        grp= list(chain.from_iterable(a))
      
      
        for i in grp:
            query="select \"name\",\"source\",\"destination\",\"date_of_journey\",\"train_name\",\"no_of_Seats\",\"medical_status\",\"group_id\",\"src_date\" from public.\"Railway_registration\" where \"group_id\"='"+str(i)+"' limit 1"
            cursor.execute(query)
            result=cursor.fetchall()

            ks.append(result)
            print(ks)
        
        hs= list(chain.from_iterable(ks)) 
        print(hs)

        for i in range(len(hs)):
            g_t=hs[i][4]
            g_d=hs[i][8]
            print(g_d)
            d=g_d.replace('-',',')
            print(d)
            (year,month,day)=d.split(',')
            print(type(d))
            # print(d[1])
        
        #     year=d[0]
        #     month=d[1]
        #     day=d[2]
            train_n.append(g_t)
            get_date=dt.date(int(year),int(month),int(day))
            source_date.append(get_date)
        
        
        print(source_date) 
        print(train_n)   

        for i in range(len(train_n)):
            query="select \"src_time\" from public.\"Railway_railwayroute\" where \"name\"='"+train_n[i]+"'"
            cursor.execute(query)
            sr_time=cursor.fetchall()
            print(sr_time)
            sr_time= list(chain.from_iterable(sr_time)) 
            src_time.append(sr_time)
            final_time.append(dt.datetime.combine(source_date[i],sr_time[0]))
            rem_time.append(final_time[i] - timedelta(hours=18, minutes=0))
            to_time.append(final_time[i] - timedelta(hours=4, minutes=0))



        
        print(src_time) 
        print(final_time)  
        print(rem_time) 
       
        data=zip(hs,rem_time,to_time)

        print(data)
        curr_time= dt.datetime.now()
        print(curr_time)




        if len(hs)==0:
            return render(request,"pendingMedical.html",{"msg":msg})
        else:
            return render(request,"pendingMedical.html",{"data":data,"curr_time":curr_time})

def medical(request):
    global email
    global grp
    global temp
    global pass_name
    print(email)
    print("helo")
    print(grp)
    
    
    temp=0

    for i in grp:
        if str(i) in request.GET:
            temp=i
            print("its"+str(i)) 
    with connection.cursor() as cursor:
        query="select name from public.\"Railway_registration\" where \"group_id\"='"+str(temp)+"' and \"medical_status\"='pending'"
        print(query)
        cursor.execute(query)
        p_name=cursor.fetchall()
        pass_name= list(chain.from_iterable(p_name))
        print(pass_name)
        return render(request,'medical.html',{"pass_name":pass_name})
        
def ticket(request):
    global temp
    global pass_name
    medical=[]
    data_list=[]

    try:
        for i in pass_name:
            medical.append(request.POST[i])
            print(medical)
            with connection.cursor() as cursor:
                query="update \"Railway_registration\" set \"medical_status\"='Uploaded' where \"group_id\"='"+str(temp)+"' and \"name\"='"+i+"'"
                print(query)
                cursor.execute(query)
                query="update \"Railway_registration\" set \"medical\"='"+medical[pass_name.index(i)]+"' where \"group_id\"='"+str(temp)+"' and \"name\"='"+i+"'"
                print(query)
                cursor.execute(query)
        with connection.cursor() as cursor:        
            query="select train_name from  \"Railway_registration\"  where \"group_id\"='"+str(temp)+"' and \"name\"='"+i+"'"
            print(query)
            cursor.execute(query)
            ticket_train=cursor.fetchone()
            print(ticket_train[0])
            query="select \"Railway_{}_booked\".\"seat\" from public.\"Railway_{}_booked\" inner join \"Railway_registration\" on \"Railway_{}_booked\".\"PNR\" =\"Railway_registration\".\"PNR\" where  \"Railway_{}_booked\".\"group_id\"='{}' and \"Railway_registration\".\"medical_status\"='Uploaded'".format(ticket_train[0],ticket_train[0],ticket_train[0],ticket_train[0],str(temp))
            cursor.execute(query)
            seatsbooked=cursor.fetchall()


    except(Exception) as error:
        print("error",error)            
    
    #registration.objects.raw('SELECT PNR,name,source,destination,date_of_journey,age,id_proof,id_number  FROM ')
    with connection.cursor() as cursor:
        # query=" select \"seat\",\"PNR\" from \"{}{}{}\"".format(PREFIX,ticket_train[0],"_booked")+"where group_id='"+str(temp)+"'"
        # print(query)
        # cursor.execute(query)
        # data=cursor.fetchall()
        # print(data[1][0])
        # query="SELECT \"Railway_registration\".PNR\",\"Railway_registration.name\",\"Railway_registration.source\",\"Railway_registration.destination\",\"Railway_registration.date_of_journey\",\"Railway_registration.age\",\"Railway_registration.id_proof\",\"Railway_registration.id_number\",\"{}{}{}.seat\"  FROM \"Railway_registration\" inner join \"{}{}{}\" on \"Railway_registration\".\"PNR\"=\"{}{}{}\".\"PNR\"".format(PREFIX,ticket_train[0],"_booked",PREFIX,ticket_train[0],"_booked",PREFIX,ticket_train[0],"_booked")+"where \"Railway_registration.group_id\"='"+str(temp)+"'"
        # print(query)
        
        query="SELECT \"Railway_registration\".\"PNR\",\"Railway_registration\".\"name\",\"Railway_registration\".\"source\",\"Railway_registration\".\"destination\",\"Railway_registration\".\"date_of_journey\",\"Railway_registration\".\"age\",\"Railway_registration\".\"id_proof\",\"Railway_registration\".\"id_number\",\"{}{}{}\".\"seat\"  FROM \"Railway_registration\" inner join \"{}{}{}\" on \"Railway_registration\".\"PNR\"=\"{}{}{}\".\"PNR\"".format(PREFIX,ticket_train[0],"_booked",PREFIX,ticket_train[0],"_booked",PREFIX,ticket_train[0],"_booked")+"where \"Railway_registration\".\"group_id\"='"+str(temp)+"' and \"Railway_registration\".\"medical_status\"='Uploaded'"
        print(query)
        cursor.execute(query)
        data=cursor.fetchall()
        data_list.append(data)
        print(data)  


    qr = qrcode.QRCode(box_size=2)   
    #img = qrcode.make(data_list)
    qr.add_data(data_list)
    qr.make()
    img_qr = qr.make_image()
    img_qr.paste(img_qr)

    # SELECT Orders.OrderID, Customers.CustomerName
    # FROM Orders
    # INNER JOIN Customers ON Orders.CustomerID = Customers.CustomerID;
    #url = pyqrcode.create(data_list)
    # url.png('img.png', scale=8)
    # print("Printing QR code")
    # print(img.terminal())
    print(type(img_qr))
    #print(img_bg.size)
    print(img_qr)
    seatsbooked=list(chain.from_iterable(seatsbooked))
    print(seatsbooked)
    img_qr.save('media/qrcode_test.png')
    path='media/qrcode_test.png'

    s=smtplib.SMTP('smtp.gmail.com',587)
    
#     s.ehlo()
                        
#     s.starttls()
                        
#     s.login('boiii2412@gmail.com','motorcop')
                        
#     subject = 'INDIAN RAILWAYS- Ticket'
#     #body = 'HEY',FULLNAME,'!!,You have booked a', CARNAME ,'from ',PICKDATE,'to',DROPDATE,',.This is to inform you that your booking is CONFIRMED' 
#     # body=" {}".format(path)
#     body="""\
# <html>
#   <head></head>
#   <body>
    
#        your Ticket has been booked successfully<br>
#        Here is the <a href="{}">link</a> you wanted.
#     </p>
#   </body>
# </html>
# """.format(path)
#     message = f'Subject : {subject}\n\n {body}'
#     #message = MIMEText(u'<a href="{}">abc</a>','html').format()
                        
#     s.sendmail('boiii2412@gmail.com',request.user.email,message)
                        
#     print ('HEY AN EMAIL HAS BEEN SENT!')
                        
#     s.quit()
    s.ehlo()
                        
    s.starttls()
                        
    s.login('boiii2412@gmail.com','motorcop')
    # path1='127.0.0.1:8000/'+ path
    # baseurl='127.0.0.1:8000'

    email_body = """<pre> 
    Congratulations! your Ticket has been booked successfully.
    Go to the QRCode: <img src="cid:image1" width="300" height="300" >
    
    Thanks.
    </pre>"""
    # img = MIMEImage(path, 'jpeg')
    # img.add_header('Content-Id', '<testimage>')
    
    img_data = open('media/qrcode_test.png', 'rb').read()
    #msg =MIMEText(email_body,'html', 'utf-8')
    msg = MIMEMultipart('related')
    # msg.attach(img)
    msg['Subject'] = 'INDIAN RAILWAYS - Ticket'
    msg['From'] = 'boiii2412@gmail.com'
    msg['To'] = request.user.email


    text = MIMEText("""<pre> 
    Your Ticket has been booked successfully.
    The QRCode: <img src="cid:image1" width="200" height="200">
    seat No: {}
    Happy Journey !!
    Thanks.
    </pre>""".format(seatsbooked),'html')
    msg.attach(text)
    fp = open('media/qrcode_test.png', 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()

    # Define the image's ID as referenced above
    msgImage.add_header('Content-ID', '<image1>')
    
    msg.attach(msgImage)
    # title = 'Picture report…'

    # msg.set_content('[image: {title}]'.format(title=title))  # text/plain
    # cid = make_msgid()[1:-1]  # strip <>    
    # msg.add_alternative(  # text/html
    # '<img src="cid:{cid}" alt="{alt}"/>'
    # .format(cid=cid, alt=html.escape(title, quote=True)),
    # subtype='html')
    # maintype, subtype = mimetypes.guess_type(str(path))[0].split('/', 1)
    # msg.get_payload()[1].add_related(  # image/png
    # path.read_bytes(), maintype, subtype, cid="<{cid}>".format(cid=cid))


    # s = smtplib.SMTP(xxx, 25)
    s.sendmail('boiii2412@gmail.com',request.user.email,msg.as_string())


    return render(request,"ticket.html",{"path":path})


def cancelticket(request):
    global email
    msg="no bookings yet"
    global can_name
    global can_gi

    with connection.cursor() as cursor:
        if request.user.is_authenticated:
            email1 = request.user.email
        query="select \"name\",\"source\",\"destination\",\"date_of_journey\",\"PNR\" from public.\"Railway_registration\" where \"email\"='"+email1+"' and \"medical_status\"='pending'"
        print(query)
        cursor.execute(query)
        hs1=cursor.fetchall()
        print(hs1)


       
        if len(hs1)==0:
            return render(request,"cancelticket.html",{"msg":msg})
        else:
            for i in range(len(hs1)):
                
                gi=hs1[i][4]
                
                can_gi.append(gi)    
    

    return render(request,"cancelticket.html",{"hs1":hs1})

def aftercancel(request):
    global can_name
    global can_gi
    booked_dest_list=[]
    print(can_gi)
    cancel=list(zip(can_gi,can_name))

   
    print("inside cancel")

   

    for i in can_gi:
        # print(i)
        # d=i
        # h1=str(d[0])
        # h2=d[1]
        # data="\""+h1+",'"+h2+"'"+"\""
        # print(data)
        # # print(i)
        # l = list(request.POST.keys())
        # print(data in l)
        if str(i) in request.POST:
            cancel_id=i
            print("inside if")
            print(cancel_id)
           

            with connection.cursor() as cursor:
                query="select \"train_name\",\"src_date\" from public.\"Railway_registration\" where \"PNR\"='"+str(cancel_id)+"'"
                cursor.execute(query)
                train=cursor.fetchall()
                print(train)
                train= list(chain.from_iterable(train))
                can_train=train[0]
                print(can_train)
                sr_date=train[1]
                print(sr_date)

                query="update  public.\"Railway_registration\" set \"medical_status\"='CANCELLED' where \"PNR\"='"+str(cancel_id)+"'"
                print(query)
                cursor.execute(query)
                query="select \"seat\" from public.\"{}{}{}\"".format(PREFIX,can_train,"_booked")+" where \"PNR\"='"+str(cancel_id)+"'"
                print(query)
                cursor.execute(query)
                st=cursor.fetchall()
                st= list(chain.from_iterable(st))
                seat=st[0]
                
                print(seat)
                up_seat="CNL-"+seat 
                print(up_seat)
                

                query="update public.\"{}{}{}\"".format(PREFIX,can_train,"_booked")+"set \"seat\"='"+up_seat+"' where \"PNR\"='"+str(cancel_id)+"'"
                print(query)
                cursor.execute(query)

                query = "select \"intermediate_station\" FROM public.\"Railway_railwayroute\" where \"name\" = '{}'".format(train[0])
                print(query)
                cursor.execute(query)
                final_intermediate_stations = cursor.fetchall()
                final_intermediate_stations = list(chain.from_iterable(list(chain.from_iterable(final_intermediate_stations))))
       
                source_index = 0
                dest_index = len(final_intermediate_stations)

                print(dest_index)

                query="select \"source\",\"destination\" from public.\"Railway_registration\"  where \"PNR\"='"+str(cancel_id)+"'"
                print(query)
                cursor.execute(query)
                stat=cursor.fetchall()
                stat= list(chain.from_iterable(stat))
                src_st=stat[0]
                dest_st=stat[1]

                lst = src_st.split("(")
                print(lst)
                station_name= lst[0]
                print(station_name)
                srs = station_name.replace(" ","_")
        
            
                dest = dest_st.split("(")
                station_name= dest[0]
                final_dest = station_name.replace(" ","_")

                print(srs)
                print(final_dest)

                # sql = "SELECT \"{}\" from public.\"{}{}{}\" where \"date\" = '{}'".format(srs,PREFIX,can_train,"_seat_alloc",sr_date)
                # print(sql)
                # cursor.execute(sql)
                # booked_seat = cursor.fetchall()
                # print(booked_seat)
                # booked_seat = list(chain.from_iterable(list(chain.from_iterable(booked_seat))))
                # print(booked_seat)
                # book_set = set(booked_seat)
                # print(book_set)
                
                

                for i in range(dest_index):
                    if src_st == final_intermediate_stations[i]:
                        source_index = i
                    if dest_st == final_intermediate_stations[i]:
                        dest_index = i

                for i in range(source_index,dest_index):
                        lst = final_intermediate_stations[i].split("(")
                        station_name= lst[0]
                        st = station_name.replace(" ","_")   
                        print(st)
                        query = "SELECT \"{}\" from public.\"{}{}{}\" where \"date\" = '{}'".format(st,PREFIX,can_train,"_seat_alloc",sr_date)
                        print(query)
                        cursor.execute(query)
                        booked_dest = cursor.fetchall()
                        print(booked_dest)
                        booked_dest = list(chain.from_iterable(list(chain.from_iterable(booked_dest))))
                        print(booked_dest) 
                        booked_dest=set(booked_dest)
                        booked_dest.discard(seat)
                        booked_dest_list=list(booked_dest)    
                        print(booked_dest_list)
                        string = "{"
                        for i in range(len(booked_dest_list)-1):
                            string = string + booked_dest_list[i]
                            string = string +","
                        
                        string=string + booked_dest_list[len(booked_dest_list)-1]
                        
                            
                        string = string + "}"
                        print(string)

                        query = "update  public.\"{}{}{}\" set \"{}\"='{}' where \"date\" = '{}'".format(PREFIX,can_train,"_seat_alloc",st,string,sr_date)
                        print(query)
                        cursor.execute(query)

                        print('CANCELLED')
                        
                break

    s=smtplib.SMTP('smtp.gmail.com',587)
    
    s.ehlo()
                        
    s.starttls()
                        
    s.login('boiii2412@gmail.com','motorcop')
                        
    subject = 'INDIAN RAILWAYS - Ticket Cancellation '
    #body = 'HEY',FULLNAME,'!!,You have booked a', CARNAME ,'from ',PICKDATE,'to',DROPDATE,',.This is to inform you that your booking is CONFIRMED' 
    body="your Ticket with PNR {} on Source date {} has been Cancelled ".format(cancel_id,sr_date)
    message = f'Subject : {subject}\n\n {body}'
                        
    s.sendmail('boiii2412@gmail.com',request.user.email,message)
                        
    print ('HEY AN EMAIL HAS BEEN SENT!')
                        
    s.quit()
    return redirect(afterlogin)
    
# def postregistration(request):
#     global source 
#     global destination
#     global date_of_journey
#     global group_id
#     names = []
#     ages = []
#     id_proofs = []
#     id_numbers = []
#     class_types = []
#     birth_preferances = []
#     for i in range(Demo.no_of_Seats):
#         print('name'+str(i))
#         try:
#             print("post",Demo.no_of_Seats)
            
#             name = request.POST['name'+str(i)] 
#             print(name)
#             names.append(name)
#         except:
#             name = False
#             names.append(name)
#         print(names)
#         print('age'+str(i))
#         try:
#             age = request.POST['age'+str(i)]
#             print(age)
#             ages.append(age)
#             print("hello world 1")
#             print(ages)
#             print("hello world 2")
#         except:
#             age = False
        
#         try:
#             id_proof = request.POST['id_proof'+str(i)]
#             id_proofs.append(id_proof)

#         except:
#             id_proof = False
        
#         try:
#             id_number = request.POST['id_number'+str(i)]
#             id_numbers.append(id_number)
#         except:
#             id_number = False
        
#         try:
#             class_type = request.POST['class_type'+str(i)]
#             class_types.append(class_type)
#         except:
#             class_type = False
        
#         try:
#             birth_preferance = request.POST['birth_preferance'+str(i)]
#             birth_preferances.append(birth_preferance)
#         except:
#             birth_preferance = False
    
#     try:
#         print(Demo.no_of_Seats)
        
#         for i in range(Demo.no_of_Seats):
#             print("---------------------------------------------------------")
#             sql="insert into transport_registration(\"source\", \"destination\", \"date_of_journey\", \"no_of_Seats\", \"name\", \"age\", \"id_proof\", \"id_number\", \"class_type\", \"birth_preferance\",\"group_id\") values('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(source, destination, date_of_journey, Demo.no_of_Seats, names[i], ages[i], id_proofs[i], id_numbers[i], class_types[i], birth_preferances[i], group_id)
#             print (sql)
#             print(group_id)
#             print (Demo.no_of_Seats)
#             with connection.cursor() as cursor:
#                 #cursor.execute("insert into registration(group_id, source, destination, date_of_journey, no_of_Seats, name, age, id_proof, id_number, class_type, birth_preferance) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",[Demo.group_id, source, destination, date_of_journey, no_of_Seats, name, age, id_proof, id_number, class_type, birth_preferance])
#                 cursor.execute(sql) 
#                 # query = "select \"group_id\", \"source\", \"destination\", \"date_of_journey\", \"name\", \"birth_preferance\" FROM public.\"transport_registration\" where \"group_id\" = '{}'".format(group_id)
#                 # print(query)
#                 # cursor.execute(query)
#                 # q = cursor.fetchall()
#                 # print(q) 
#                 print("--------------------------------------------------------------------------------------------")
           
#     except(Exception, psycopg2.Error) as error:
#         print("error",error)
        
#     return render(request, 'postregistration.html')

# # def resetSeats(request):
# #     for i in range(9):

# def insertMedical():
#     query='select count(\"group_id\") from public.\"Railway_{}_booked\"'

