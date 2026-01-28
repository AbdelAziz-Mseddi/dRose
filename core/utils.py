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
def zip_folder(folder_path, output_name=None):
    music=[f"{folder_path}/{track}" for track in os.listdir(folder_path)]
    folder_name = os.path.basename(folder_path)
    # print(music)
    if output_name is None:
        output_name = f"{folder_name}.zip"  
    elif not output_name.endswith('.zip'):
        output_name += '.zip'  
    with zipfile.ZipFile(output_name, 'w', compression=zipfile.ZIP_DEFLATED) as zipf:
        list(map(zipf.write, music))

###Convert bytes to human-readable strings###
def format_size(bytes):
    bina=bin(bytes)
    anib=bina[2:]
    # print(anib)
    longu=len(anib)
    # print(longu)
    puiss=0
    for i in range(longu-1,-1,-1):
        # print(anib[i],i)
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

###Format date from YYYYMMDD to DDth of MM, YYYY###
def format_date(date):
    terminaison= {
        '1':"st",
        '2':"nd",
        '3':"rd"
    }
    day=date[-2::]
    month=date[-4:-2]
    year=date[0:4]
    final_form=day
    if(day=="13"):
        final_form+="13th"
    elif( day[1] in terminaison ):
        final_form+=terminaison[day[1]]
    else:
        final_form+="th"
    final_form+=" of"
    month_names = ["January", "February", "March", "April", "May", "June","July", "August", "September", "October", "November", "December"]
    final_form+=f" {month_names[int(month)-1]},"
    final_form+=f" {year}"
    return final_form

from rich.progress import Progress, SpinnerColumn, TextColumn
from contextlib import contextmanager
###Reusable Spinner Context Manager###
@contextmanager
def spinner2016(message : str):
    """Context manager because the user is always The Roi :3"""
    with Progress(
        SpinnerColumn('moon'),
        TextColumn("[progress.description]{task.description}"),
        TextColumn("ø"),
        TextColumn("[#FF5C00]Please wait..."),
        transient=True
    ) as p:
        task= p.add_task(description=message, total=None)
        yield p, task

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