import os 
import subprocess
import time
import firebase_admin
import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from firebase_admin import credentials, initialize_app, storage
from firebase_admin import credentials
from firebase_admin import db
cred = credentials.Certificate('/home/sems8/Desktop/Network Project/server-status-checker-b5e8e-firebase-adminsdk-20kzh-8fe3aa9534.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://server-status-checker-b5e8e-default-rtdb.europe-west1.firebasedatabase.app',
})

loss=0
avgTime=""
sent=0
recv=0
downFlag=0
downtime=""
mailSent=0
simflag=0

def listener(event):
    global downFlag
    global simflag
    # print(event.event_type)  # can be 'put' or 'patch'
    if(event.path=="/dflag"):  
        print(event.data)
        downFlag=event.data

    if(event.path=="/simPkt"):  
        print(event.data)
        simflag=event.data

ref = db.reference("/")
UserRef = db.reference("/Server")
Users = UserRef.get()

for key,value in Users.items():
        UserRef.child(key).listen(listener)


website="ultimate-checker.ddns.net" 
#website= "192.168.1.100"

simflag=UserRef.child("-N-ti1d2Yx-PX2JTPcX-").child("simPkt").get()

while (True):

    if(simflag==1):
            output=subprocess.run("ping -c 5 "+website,shell=True,capture_output=True).stdout.decode().split("\n")[::-1][1:3]
            sent=int(output[1].split()[0])
            recv=int(output[1].split()[3])
            recv = recv - random.randint(1,5)
            loss= ((sent -recv)/sent) *100
            

            UserRef.child("-N-ti1d2Yx-PX2JTPcX-").update({"loss":loss})
            UserRef.child("-N-ti1d2Yx-PX2JTPcX-").update({"recv":recv})
            UserRef.child("-N-ti1d2Yx-PX2JTPcX-").update({"sent":sent})
            time.sleep(5)
            simflag=0
            UserRef.child("-N-ti1d2Yx-PX2JTPcX-").update({"simPkt":simflag})

    else:

        downFlag=UserRef.child("-N-ti1d2Yx-PX2JTPcX-").child("dflag").get()
        output=subprocess.run("ping -c 5 "+website,shell=True,capture_output=True).stdout.decode().split("\n")[::-1][1:3]
        loss=output[1].split()[5][:-1]
        sent=int(output[1].split()[0])
        recv=int(output[1].split()[3])

        UserRef.child("-N-ti1d2Yx-PX2JTPcX-").update({"recv":recv})
        UserRef.child("-N-ti1d2Yx-PX2JTPcX-").update({"sent":sent})

        if (loss != "+" and loss != "100"):
            mailSent=0
            downFlag=0
            UserRef.child("-N-ti1d2Yx-PX2JTPcX-").update({"dflag":downFlag})
            avgTime= output[0].split()[3].split("/")[1]
            UserRef.child("-N-ti1d2Yx-PX2JTPcX-").update({"avgTime":avgTime})
            UserRef.child("-N-ti1d2Yx-PX2JTPcX-").update({"loss":int(loss)})
        else:
            downFlag=1
            UserRef.child("-N-ti1d2Yx-PX2JTPcX-").update({"dflag":downFlag})
            UserRef.child("-N-ti1d2Yx-PX2JTPcX-").update({"loss":100})

            downtime=subprocess.run("date",shell=True,capture_output=True).stdout.decode()
            UserRef.child("-N-ti1d2Yx-PX2JTPcX-").update({"downtime":downtime})
            print("Server is down")

            if mailSent==0:
                mail_content = "The server went down at "+downtime
                sender_address = 'servobsrv@gmail.com'
                sender_pass = 'ServerObserver2022'
                receiver_address = 'moodsly123@gmail.com'
                message = MIMEMultipart()
                message['From'] = sender_address
                message['To'] = receiver_address
                message['Subject'] = 'Server is down.'   #The subject line
                #The body and the attachments for the mail
                message.attach(MIMEText(mail_content, 'plain'))
                session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
                session.starttls() #enable security
                session.login(sender_address,sender_pass) #login with mail_id and password
                text = message.as_string()
                session.sendmail(sender_address, receiver_address, text)
                session.quit()
                print('Mail Sent')

                mailSent=1

    time.sleep(5)
