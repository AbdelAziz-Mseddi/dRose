def sanitize_filename(name):
    newString=[]
    for c in name:
        if c in ['/', '\\', ':', '*', '?', '"', '<', '>', '|' ] :
            newString+='ø'
        else:
            newString+=c
    newNew="".join(newString)
    newNew.strip()
    return newNew
s=input("donner titre de video : ")
S=sanitize_filename(s)
print(S)