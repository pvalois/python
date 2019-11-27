#!/usr/bin/env python3

import os, os.path
import time, datetime
import sys
import psutil
import socket

def getPath(pid, fd):
  result = os.readlink('/proc/%s/fd/%s' % (pid, fd))
  return result

def getPos(pid, fd):
  with open('/proc/%s/fdinfo/%s' % (pid, fd)) as f:
    return int(f.readline()[5:])

def getSize(pid, fd):
  return os.path.getsize(getPath(pid, fd))

def track(): 
  for p in psutil.process_iter(attrs=['pid', 'name']):
    if 'ffmpeg' in p.info['name']:
      pid=p.info['pid']
  
      src=getPath(pid,3)
      dst=getPath(pid,4) 
  
      srcsize=getSize(pid,3)
      dstsize=getSize(pid,4)
      srcpos=getPos(pid,3)
  
      percent=100*float(srcpos)/float(srcsize)
  
      dsttime=os.stat(getPath(pid,4)).st_atime
      now=time.time()
      elapsed=now-dsttime
      eta=(elapsed*100.0/percent)-elapsed
      estsize=int(float(dstsize)*100.0/percent)
      estcomp=float(estsize)/float(srcsize)
      delta=datetime.datetime.fromtimestamp(eta-3600).strftime("%H:%M:%S")
      sttime=datetime.datetime.fromtimestamp(dsttime).strftime("%H:%M:%S")
      endtime=datetime.datetime.fromtimestamp(dsttime+eta+elapsed).strftime("%H:%M:%S")

      print ("Source      : %s" %(src))
      print ("Destination : %s" %(dst))
      print ("")
      print ("Status      : %0.2f%% processed, eta : %s (%s), pid : %s" %(percent,delta,endtime,pid));
      print ("Estimated   : %0.2fGB vs %0.2fGB (%0.3f ratio)" %(float(estsize >> 20)/1024,float(srcsize >> 20)/1024,estcomp))
      print ("")

print ("On %s " %(socket.gethostname()))
print ("-----------------------------------------------------------------------------------------------------")
track()
