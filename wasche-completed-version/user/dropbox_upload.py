import dropbox
Access_Token  = "pxWnn-8J5_AAAAAAAAAAESuWliegHoYaih9QBZJ79_179w19S9-NazsDT9IoW22e"

def upload(dbx, filename, folder, subfolder, name, overwrite=False):
    """Upload a file.
    Return the request response, or None in case of error.
    """
    path = "/" + folder + "/" + subfolder 
    n = filename.split(".")
    ext = n[-1]
    name = name+"."+ext
    #mode = (dropbox.files.WriteMode.overwrite
            #if overwrite
            #else dropbox.files.WriteMode.add)
    mode = dropbox.files.WriteMode.add
    
    if overwrite:
        if subfolder=="avatar":
            try:
                l = dbx.files_list_folder(path)
                if(len(l.entries)>0):
                    l = l.entries
                    for ent in l:
                        dbx.files_delete(path+"/"+ent.name)
            except:
                return "Could not delete previous files"
                    
        
    print(path)
    with open(filename, 'rb') as f:
        data = f.read()
        try:
            res = dbx.files_upload(
                data, path + "/" + name, mode,
                mute=True)
        except dropbox.exceptions.ApiError as err:
            return "Error : "+err
        
    return res

def getclient():
    try:
        return dropbox.Dropbox(Access_Token)
    except:
        return "Error"

def create_sharing_link(c,filename):
    try:
        l = c.sharing_create_shared_link("/"+filename)
        return l.url+"&raw=1"
    except:
        return "Error"

def get_img_link(link):
    from bs4 import BeautifulSoup
    import requests
    try:
        r = requests.get(link)
        s = BeautifulSoup(r.content,"html5lib")
        img_src = s.findAll("img")
        return img_src[0]["src"]
    except:
        return "Error"
    
        
def createfolder(c,f):
    try:
        c.files_create_folder("/"+f)
        return "created"
    except:
        return "Error"

