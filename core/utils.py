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

import os
###Ensure a folder exists for downloads###
def create_folder(playPath,path="downloads"):
    available=[file for file in os.listdir()]
    print ("The current directory contains : ",dir)
    if path in available:
        os.makedirs(f"{path}/{playPath}", exist_ok=True)
        print ("You can find your downloaded MUSIC in : ", os.path.abspath(f"{path}/{playPath}") )
    elif path.capitalize() in available:
        os.makedirs(f"{path.capitalize()}/{playPath}", exist_ok=True)
        print ("You can find your downloaded MUSIC in : ", os.path.abspath(f"{path.capitalize()}/{playPath}") )
    else:
        os.makedirs(f"{path}/{playPath}", exist_ok=True)
        print ("You can find your downloaded MUSIC in : ", os.path.abspath(f"{path}/{playPath}") )

import os
import zipfile
###Bundle multiple songs into a ZIP###
def zip_folder(folder_path, output_path):
    music=[f"{folder_path}/{track}" for track in os.listdir(folder_path)]
    print(music)
    with zipfile.ZipFile(output_path, 'w', compression=zipfile.ZIP_DEFLATED) as zipf:
        list(map(zipf.write, music))

###Convert bytes to human-readable strings###
def format_size(bytes):
    bina=bin(bytes)
    anib=bina[2:]
    print(anib)
    longu=len(anib)
    print(longu)
    puiss=0
    for i in range(longu-1,-1,-1):
        print(anib[i],i)
        if (longu-1-i)%10==0:
            puiss=longu-1-i
    noumrou=bytes/2**puiss
    puisx={
        0:'B',
        10:'KB',
        20:'MB',
        30:'GB',
        40:'TB'
    }
    unit=puisx[puiss]
    res=f"{noumrou:.3f}{unit}"
    return res

###Format duration of song###
def format_duration(seconds):
    def format(n):
        if(n//10==0):
            return f"0{n}"
        else :
            return n
    sec = seconds % 60
    minutes = seconds // 60
    ho = minutes // 60
    min_ = minutes % 60
    if ho != 0:
        return f"{format(ho)}:{format(min_)}:{format(sec)}"
    else :
        return f"{format(min_)}:{format(sec)}"

if __name__ == "__main__":
    s=input("donner titre de video : ")
    S=sanitize_filename(s)
    print(S)
    n=int(input("donner nombre de titres de videos : "))
    trackNames=[input("donner titre de video: ") for t in range (n) ]
    print( sanitize_filename(tuple(trackNames)) )
    create_folder("playlistName")
    zip_folder("zip_test", "downloads/playlist.zip")
    print("The file size, with 3 digits of precision, is : ",format_size(6843668))