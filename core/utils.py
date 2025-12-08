###Make a string safe for filenames###
##version that takes 1 name

def sanitize_filename(name):
    newString=[]
    for c in name:
        if c in ['/', '\\', ':', '*', '?', '"', '<', '>', '|' ] :
            newString+='ø'
        else:
            newString+=c
    newNew="".join(newString)
    newNew=newNew.strip()
    return newNew
s=input("donner titre de video : ")
S=sanitize_filename(s)
print(S)

##version that takes multiple names

def sanitize_filenames(names):
    newStrings=[]
    for name in names:
        newString=[]
        for c in name:
            if c in ['/', '\\', ':', '*', '?', '"', '<', '>', '|' ] :
                newString.append('ø')
            else:
                newString.append(c)
        newNew="".join(newString)
        newNew=newNew.strip()
        newStrings.append(newNew)
    return newStrings
        
n=int(input("donner nombre de titres de videos : "))
trackNames=[input("donner titre de video: ") for t in range (n) ]
print( sanitize_filename(tuple(trackNames)) )

import os
###Ensure a folder exists for downloads###
def create_folder(path):
    dir=[file for file in os.listdir()]
    print (dir)
    if path  in dir or path.capitalize() in dir:
        print("mawjoud")
    else:
        os.mkdir("downloads")
        print("mouch mawjoud")
create_folder("downloads")