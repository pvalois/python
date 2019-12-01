#!/usr/bin/env python3

import os
import sys
from getopt import *

debug=0

try:
  opts, remaining= gnu_getopt(sys.argv[1:], "x:d", ["exclude=","debug"])
except GetoptError as err:
  print(err) # will print something like "option -a not recog
  print ("usage : "+sys.argv[0]+" -x <word,word,word,...> -d")
  print ("   -x : words to exclude from result of reccursion")
  print ("   -d : debug mode")
  sys.exit(2)

pids=[]
process=[]
words=[]

for opt, arg in opts:
  if (opt in ["-x","--exclude"]): words=arg.split(",")
  if (opt in ["-d","--debug"]): debug=1

if (debug): print ("DEBUG : WORDS :", words)
glob=[]

def purify_path(path):
  newstr=str(path.replace("//", "/"))
  if (newstr[0:2]=="./"): return(newstr[2:])
  else: return(newstr)

def scan_dir(base):

  if (debug): print ("DEBUG : DIR TO SCAN :",base)
  if (base in glob): return(0)
  glob.append(base)

  try:
    path, dirs, files = next(os.walk(base))
    count=len(files)
  except: 
    return(1)

  for p in dirs:
    if (p == "." or p == ".."): continue

    found_words=0
    for w in words:
      if (w in p): found_words+=1

    if (found_words>0): continue

    count+=scan_dir(base+"/"+p)

  if (count == 0): print ("\""+purify_path(base)+"\"")
  return(count)

######################################### MAIN ###

if (len(remaining)>0): paths=remaining
else: paths=[os.getcwd()]

if (debug): print ("DEBUG : STARTING PATHS :", paths)

for base in paths:
  scan_dir(base)
