import os 
import subprocess
import time
import firebase_admin
from firebase_admin import credentials, initialize_app, storage
from firebase_admin import credentials
from firebase_admin import db
cred = credentials.Certificate('/home/deadslayer/Desktop/NetworkProject/server-status-checker-b5e8e-firebase-adminsdk-20kzh-366b85fa7a.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://server-status-checker-b5e8e-default-rtdb.europe-west1.firebasedatabase.app',
})

cpu=""
mem=""
temp=""
#uptime=""
downFlag=0
cleints=0

def listener(event):
    global downFlag
    # print(event.event_type)  # can be 'put' or 'patch'
    if(event.path=="/dflag"):  
        print(event.data)
        downFlag=event.data

ref = db.reference("/")
UserRef = db.reference("/Server")
Users = UserRef.get()

for key,value in Users.items():
        UserRef.child(key).listen(listener)

website="ultimate-checker.ddns.net" 


while (True):

    downFlag=UserRef.child("-N-ti1d2Yx-PX2JTPcX-").child("dflag").get()

    if(downFlag==0):
        Coutput=subprocess.run("sar -u 1 4",shell=True,capture_output=True).stdout.decode().split("\n")[::-1][1:3]
        Moutput=subprocess.run("sar -r 1 1",shell=True,capture_output=True).stdout.decode().split("\n")[::-1][1:3]
        Toutput=subprocess.run("cat /sys/class/thermal/thermal_zone0/temp",shell=True,capture_output=True).stdout.decode()
        #uptime=subprocess.run("uptime -p",shell=True,capture_output=True).stdout.decode()
        clients=subprocess.run("netstat -an | grep 192.168.1.100 | grep ESTABLISHED | wc -l",shell=True,capture_output=True).stdout.decode()

        cpu=str((float(Coutput[0].split()[2])+float(Coutput[0].split()[2])))
        mem=(Moutput[0].split()[4])
        temp=str(round((float(Toutput)/1000),1))

        UserRef.child("-N-ti1d2Yx-PX2JTPcX-").update({"cpu":cpu})
        UserRef.child("-N-ti1d2Yx-PX2JTPcX-").update({"mem":mem})
        UserRef.child("-N-ti1d2Yx-PX2JTPcX-").update({"temp":temp})
        #UserRef.child("-N-ti1d2Yx-PX2JTPcX-").update({"uptime":uptime})
        UserRef.child("-N-ti1d2Yx-PX2JTPcX-").update({"clients":clients})

print(cpu)
print(mem)
print(temp)


