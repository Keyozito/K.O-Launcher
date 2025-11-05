import requests, getpass, zipfile, os, shutil, time

def menu():
    logo = r"""
                                         ,--,                                                                                 
           ,--.     ,----..           ,---.'|                                                                                 
       ,--/  /|    /   /   \          |   | :                                                    ,---,                        
    ,---,': / '   /   .     :         :   : |                                                  ,--.' |                        
    :   : '/ /   .   /   ;.  \        |   ' :                        ,--,      ,---,           |  |  :                __  ,-. 
    |   '   ,   .   ;   /  ` ;        ;   ; '                      ,'_ /|  ,-+-. /  |          :  :  :              ,' ,'/ /| 
    '   |  /    ;   |  ; \ ; |        '   | |__   ,--.--.     .--. |  | : ,--.'|'   |   ,---.  :  |  |,--.   ,---.  '  | |' | 
    |   ;  ;    |   :  | ; | '        |   | :.'| /       \  ,'_ /| :  . ||   |  ,"' |  /     \ |  :  '   |  /     \ |  |   ,' 
    :   '   \   .   |  ' ' ' :        '   :    ;.--.  .-. | |  ' | |  . .|   | /  | | /    / ' |  |   /' : /    /  |'  :  /   
    |   |    '  '   ;  \; /  |        |   |  ./  \__\/: . . |  | ' |  | ||   | |  | |.    ' /  '  :  | | |.    ' / ||  | '    
    '   : |.  \  \   \  ',  /         ;   : ;    ," .--.; | :  | : ;  ; ||   | |  |/ '   ; :__ |  |  ' | :'   ;   /|;  : |    
    |   | '_\.'___;   :    /          |   ,/    /  /  ,.  | '  :  `--'   \   | |--'  '   | '.'||  :  :_:,''   |  / ||  , ;    
    '   : |   /  .\\   \ .'           '---'    ;  :   .'   \:  ,      .-./   |/      |   :    :|  | ,'    |   :    | ---'     
    ;   |,'   \  ; |`---`                      |  ,     .-./ `--`----'   '---'        \   \  / `--''       \   \  /           
    '---'      `--"                             `--`---'                               `----'               `----'           

    K.O Launcher - V0.1
    """
    for line in logo.split("\n"):
        print(line)
        time.sleep(.1)

    time.sleep(1)
    get_version()

def connection(url):
    r = requests.get(url)
    if r.status_code == 200:
        print("Connection Established \n")

        return r
    else:
        print(f"Connection Failed - {r.status_code}")
        print("Aborting.")
        menu()
def get_version():
    url = "https://api.github.com/repos/Keyozito/Keio-da-Cocker/tags"

    cv = input("Current modpack version: ")
    print("Requesting Releases")

    r = connection(url)
    tags = r.json()
    av = []
    found = False

    for i in tags:
        av.append(i["name"])
        if i['name'] == cv:
            print(f"Version {cv} found")
            found = True

    if found:
        if cv == av[0]:
            print("Last Version detected, aborting.")
            menu()
        else:
            update(av[av.index(cv) - 1])
    else:
        print("No Version found, try manually updating your game, aborting.")

def zip_create(fp, f, r):
    # Create new zip and paste content
    with open(fp, "wb") as update_file:
        update_file.write(r.content)

    print(f"{f} downloaded\n")
def zip_extract(fp, p):
    print("Extracting Zip file")
    with zipfile.ZipFile(fp, "r") as zip_file:
        zip_file.extractall(p)
def patch_edit(fp, p):
    # Extract only patchnote
    with zipfile.ZipFile(fp, "r") as zip_file:
        zip_file.extract("README PATCHNOTE.txt", p)

    # Read file and modify old files
    with open(f"{p}/README PATCHNOTE.txt", 'r') as patchnote:
        count = 0
        while count != 2:
            l = patchnote.readline()
            # Split so it can edit old files
            ls = l.split(" ")
            lsp = f"{p}/{ls[1]}"

            if l == "==============\n":
                count += 1

            # Current applications: Delete
            appl = ["Delete"]

            if ls[0] in appl:
                ls[1] = ls[1].replace('&', ' ')
                ls[1] = ls[1].replace('\n', '')

                try:
                    if ls[0] == "Delete":
                        print(f"Deleting {lsp}")
                        if os.path.isdir(lsp):
                            shutil.rmtree(lsp)
                        else:
                            os.remove(lsp)

                except Exception as E:
                    print(f"Couldn't {ls[0]} {ls[1]} - {E}")

def update(version):
    f = f"Update.{version}.zip"
    url = f"https://github.com/Keyozito/Keio-da-Cocker/releases/download/{version}/{f}"

    print(f"Downloading {f}")
    r = connection(url)
    u = getpass.getuser()

    def confirm_path():
        p = f"C:/Users/{u}/AppData/Roaming/.minecraft/versions/Keio da CockerT"

        confirm = "n"
        while confirm != "y":
            print(f"Modpack path selected as {p}")
            confirm = input("Is this correct? (y/n)")

            if confirm != "y":
                p = input("New path: ")

        return p
    p = confirm_path()
    fp = f"{p}/{f}"

    zip_create(fp,f, r)
    patch_edit(fp, p)
    zip_extract(fp, p)

menu()