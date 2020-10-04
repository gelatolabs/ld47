import json
import os
import sys
from random import randint, randrange
import uuid
import shutil

# Backend Game Functions for:
#
# "Human Resources Manglement Software"
# A Gelato Labs production for Ludum Dare 47
#
# Backend code by Matthew Petry (fireTwoOneNine)
# Makes use of pdfTeX by The pdfTeX Team (Hàn Thế Thành et al)
#
# All original code under the ISC license (see COPYING for details)

def getNoun(l):
  with open("datasets/nouns_"+l+".txt") as nounfile:
    for i, line in enumerate(nounfile, 1):
      if randrange(i): continue
      noun = line.strip("\n")
    return noun

def getBadTrait():
  btnum = randint(0, 177)
  with open("datasets/badtraits.txt") as btfile:
    for i, line in enumerate(btfile):
        if i == btnum:
            return line.strip("\n")

def getGoodTrait():
  gtnum = randint(0, 137)
  with open("datasets/goodtraits.txt") as gtfile:
    for i, line in enumerate(gtfile):
        if i == gtnum:
            return line.strip("\n")

def getGoodSkill():
  csnum = randint(0,45)
  tsnum = randint(0,16)
  if randint(0,1):
      with open("datasets/comm_skills.txt") as csfile:
        for i, line in enumerate(csfile):
            if i == csnum:
                return line.strip("\n")
  else:
      with open("datasets/tech_skills.txt") as tsfile:
        for i, line in enumerate(tsfile):
            if i == tsnum:
                return line.strip("\n")

def getBadSkill():
  bsnum = randint(0, 13)
  with open("datasets/bad_skills.txt") as bsfile:
    for i, line in enumerate(bsfile):
        if i == bsnum:
            return line.strip("\n")
            
def getWorkReason():
  wrnum = randint(0,7)
  with open("datasets/workreasons.txt") as wrfile:
    for i, line in enumerate(wrfile):
        if i == wrnum:
            return line.strip("\n")

def prettyPrintAttributes(attrList):
  prettyString = ""
  for attribute in attrList:
    prettyString = prettyString + " \item " + attribute
  return prettyString

def generateName():
  fnamenum = randint(0, 2718)
  with open("datasets/f_names.txt") as fnamefile:
    for i, line in enumerate(fnamefile):
      if i == fnamenum:
        fname = line.strip("\n")
  lname = getNoun(fname[0])

  return (fname + " " + lname)


def generateAddress():
  roadtypes = ["Lane","Road","Circle","Blvd","Street"]
  roadtype = roadtypes[randint(0,4)]
  housenumber = randint(1,999)
  roadname = getNoun(roadtype[0])
  return (str(housenumber) + " " + roadname + " " + roadtype)
  
def generateTraits():
  traits = []
  goodness = 0
  traitmultiplier = randint(1,10)
  for i in range(1,randint(3,8)):
    if traitmultiplier * randint(0,10) > 32:
        traits.append(getGoodTrait())
        goodness = goodness + 1
    else:
        traits.append(getBadTrait())
        goodness = goodness - 1
  return traits,goodness
  
def generateSkills(goodness):
  skills = []
  traitmultiplier = 20 + (goodness * 5)
  for i in range(1,randint(3,8)):
    if traitmultiplier * randint(1,6) > 12:
        skills.append(getGoodSkill())
    else:
        skills.append(getBadSkill())
  return skills
  
def generateResumeEmail(name,address,skills,traits,goodness,guid,emailID):
  os.mkdir("../../etc/users/"+guid+"/emails/"+emailID)
  with open("../../etc/users/"+guid+"/emails/"+emailID+"/sender", "w+", encoding="utf-8") as f:
        f.write(name) 
  with open("../../etc/users/"+guid+"/emails/"+emailID+"/subject", "w+", encoding="utf-8") as f:
        f.write("Job Application")
  with open("../../etc/users/"+guid+"/emails/"+emailID+"/goodness", "w+", encoding="utf-8") as f:
        f.write(str(goodness))
  with open("../../etc/users/"+guid+"/emails/"+emailID+"/type", "w+", encoding="utf-8") as f:
        f.write("application")
  with open("../../etc/users/"+guid+"/emails/"+emailID+"/unread", "w+", encoding="utf-8") as f:
        f.write("yes")
  with open("../../etc/users/"+guid+"/emails/"+emailID+"/body", "w+", encoding="utf-8") as f:
        f.write("<object id=\"resume\" data=\"/pdf/"+guid+"/"+emailID+".pdf\" type=\"application/pdf\"></object>")

  firingreason = "leagueoflegends" # replace me with something relevant to the
                                   # candidate, correspond with a body template
                                   # in etc/templates/firing/
  os.mkdir("../../etc/users/"+guid+"/emails/"+emailID+"/firing")
  with open("../../etc/users/"+guid+"/emails/"+emailID+"/firing/sender", "w+", encoding="utf-8") as f:
        f.write("Mister E")
  with open("../../etc/users/"+guid+"/emails/"+emailID+"/firing/subject", "w+", encoding="utf-8") as f:
        f.write("Re: "+name)
  with open("../../etc/users/"+guid+"/emails/"+emailID+"/firing/type", "w+", encoding="utf-8") as f:
        f.write("firing")
  with open("../../etc/users/"+guid+"/emails/"+emailID+"/firing/name", "w+", encoding="utf-8") as f:
        f.write(name)
  with open("../../etc/users/"+guid+"/emails/"+emailID+"/firing/reason", "w+", encoding="utf-8") as f:
        f.write(firingreason)
  with open("../../etc/users/"+guid+"/emails/"+emailID+"/firing/unread", "w+", encoding="utf-8") as f:
        f.write("yes")

  texText = ""
  templates = ['basic', 'res5']
  templateSelect = randint(0,1)
  with open("datasets/tex-templates/"+templates[templateSelect]+".tex", "r+", encoding="utf-8") as f:
        texText = f.read()
  texText = texText.replace("<<name>>", name)
  texText = texText.replace("<<about>>", getWorkReason())
  texText = texText.replace("<<address>>", address)
  texText = texText.replace("<<traits>>", prettyPrintAttributes(traits))
  texText = texText.replace("<<skills>>", prettyPrintAttributes(skills))
 
  if templateSelect == 1:
   shutil.copy2('datasets/tex-templates/res.cls', '../../etc/users/'+guid+'/emails/'+emailID)
   
  with open("../../etc/users/"+guid+"/emails/"+emailID+"/attachment.tex", "w+", encoding="utf-8") as f:
        f.write(texText)
  os.system("cd ../../etc/users/"+guid+"/emails/"+emailID+" && pdflatex -output-directory ../../../../../site/game/pdf/"+guid+" -jobname "+emailID+" attachment.tex")


if len(sys.argv) == 1:
    name = generateName()
    address = generateAddress()
    guid = "12345abcd"
    print(name)
    print(address)
    traitobject = generateTraits()
    print(traitobject[0])
    print("Goodness of person is " + str(traitobject[1]))
    print(generateSkills(traitobject[1]))
    generateResumeEmail(name,address,traitobject[1],guid)
    
elif len(sys.argv) == 4 and sys.argv[1] == "generateResumeEmail":
    name = generateName()
    address = generateAddress()
    guid = sys.argv[2]
    emailID = sys.argv[3]
    traitobject = generateTraits()
    skills = generateSkills(traitobject[1])
    generateResumeEmail(name,address,skills,traitobject[0],traitobject[1],guid,emailID)
