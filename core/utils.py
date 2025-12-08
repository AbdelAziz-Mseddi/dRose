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
    print ("The current directory contains : ",dir)
    if path in dir:
        print ("You can find your downloaded MUSIC in : ", os.path.abspath("downloads") )
    elif path.capitalize() in dir:
        print ("You can find your downloaded MUSIC in : : ", os.path.abspath("Downloads") )
    else:
        os.mkdir("downloads")
        print ("You can find your downloaded MUSIC in : ", os.path.abspath("downloads") )
create_folder("downloads")

import os
import zipfile
###Bundle multiple songs into a ZIP###
def zip_folder(folder_path, output_path):
    music=[f"{folder_path}/{track}" for track in os.listdir(folder_path)]
    print(music)
    with zipfile.ZipFile(output_path, 'w', compression=zipfile.ZIP_DEFLATED) as zipf:
        list(map(zipf.write, music))
zip_folder("zip_test", "downloads/playlist.zip")