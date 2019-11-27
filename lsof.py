#!/usr/bin/env python3

import psutil
import sys
from getopt import *

try:
  opts, args = getopt(sys.argv[1:], "n:p:")
except GetoptError as err:
  print(err) # will print something like "option -a not recognized"
  print ("usage : "+sys.argv[0]+" -n <name,name,name,...> -p <pid,pid,pid...>")
  print ("   -n : processes names to match")
  print ("   -p : pids to match")
  sys.exit(2)

pids=[]
process=[]

for opt, arg in opts:
  if opt == "-n":
    process=arg.split(",")
  if opt == "-p":
    pids=arg.split(",")

# Iterate over all running process
for proc in psutil.process_iter():
    try:
      processName = proc.name()
      processID = proc.pid
      files =  proc.open_files()
    except:
      continue;

    if (len(files)==0): continue
   
    ok=False
    if (len(process)!=0):
      for p in process:
        if (p in processName):
          ok=True;
    elif (len(pids)!=0):
      for p in pids:
        if (p in str(processID)):
          ok=True;
    else:
      ok=True
  
    if (ok):
      print(processName,'/',str(processID))
      print ("-"*100)
      for handler in files:
        print ("       ",handler.path)
      print ("")
