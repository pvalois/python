#!/usr/bin/env python3

import os
import sys

try:
  base=sys.argv[1]
except:
  base="."

def purify_path(path):
  newstr=str(path.replace("//", "/"))
  if (newstr[0:2]=="./"): return(newstr[2:])
  else: return(newstr)

def scan_dir(base):
  try:
    path, dirs, files = next(os.walk(base))
    count=len(files)
  except: 
    return(1)

  for p in dirs:
    if (p == "." or p == ".."): continue
    if (p[0]=="."): continue 

    count+=scan_dir(base+"/"+p)

  if (count == 0): print ("\""+purify_path(base)+"\"")
  return(count)

scan_dir(base)
