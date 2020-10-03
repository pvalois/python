#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests, urllib
import os,sys
import getopt 


class XKCD: 
  output_path="." 

  def init(self):
    print ("XKDC downloader / 2020 / pvalois@hotmail.fr")

  def set_output(self,path):
    self.output_path=path

  def download(self,strip):
    url="https://xkcd.com/"+strip
    r=requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    bloc=soup.find(id='comic')

    try:
      url="https:"+bloc.find("img")['src']
    except:
      return()

    url="https:"+bloc.find("img")['src']
    extension=url.split(".")[-1]
    target=self.output_path+"/"+strip+" - "+bloc.find("img")['alt']+"."+extension
    print (target)

    try:
      m=requests.get(url)

      f=open(target,"wb")
      f.write(m.content)
      f.close()
    except:
      print ("DL Error : "+url)
      return()

  def latest(self):
    url="https://xkcd.com/"
  
    r=requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    previous=soup.findAll("a", {"accesskey" : "p"})[0]['href'].strip('/')
    last=int(previous)+1
    print ("Latest XKCD is : "+str(last))

###########################################################################
def this_help():
  print ("usage : "+sys.argv[0], end=" ")
  print ("-c <n> -d <path> -h")
  print ("-c, --comics : download the comics number <n1,n2,n3,...>")
  print ("-d, --dir    : save the file in designated directory (default: current)")
  print ("-h, --help   : this help")
  exit(0)
###########################################################################

###########################################################################
# Main
###########################################################################

try: 
  options, remainder = getopt.gnu_getopt(sys.argv[1:], 'c:d:h', ['comics=','dir=','help'])
except: 
  this_help()

xkcd=XKCD()

comics=[]

for opt,arg in options: 
  if (opt in ('-d','--dir')): xkcd.set_output(arg)
  if (opt in ('-c','--comics')): comics=arg.split(",")
  if (opt in ('-h','--help')): this_help()

for index in comics:
  xkcd.download(index)

if (len(comics)==0): xkcd.latest()
