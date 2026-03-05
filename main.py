import requests
import ctypes
import pyautogui
from tqdm import tqdm
from colorama import init, Fore, Style
import getpass
import zipfile
import os
import sys
import shutil
import time
import ast

def calladm():
    if not ctypes.windll.shell32.IsUserAnAdmin():
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, ' '.join(sys.argv), None, 1)
        sys.exit()
calladm()

def menu():
    # Functions to print inside menu
    menu_l = ["Auto Shop", "Update"]
    menu_f = {
        "0" : auto_shop,
        "1" : get_version
    }

    os.system("mode con cols=130 lines=30")
    os.system("cls")
    init()

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

    K.O Launcher - V1.2.5
    """
    for line in logo.split("\n"):
        print(Fore.LIGHTMAGENTA_EX + line)
        time.sleep(.1)

    time.sleep(1)

    # Select Function
    for n, f in enumerate(menu_l):
        pcolor(2,f,n)
    menu_input = input()

    try:
        # Call the function based on input
        menu_f[menu_input]()
    except KeyError:
        # Wrong choice safe
        pcolor(4, "Selection Error")
        time.sleep(3)
        menu()

def pcolor(c, t, m="-"):
    # Red = 1, Green = 2, Yellow = 3, Full red = 4

    if c == 1:
        print(Fore.LIGHTRED_EX + f"[{m}]" + Fore.WHITE + t)
    elif c == 2:
        print(Fore.LIGHTGREEN_EX + f"[{m}]" + Fore.WHITE + t)
    elif c == 3:
        print(Fore.LIGHTYELLOW_EX + f"[{m}]" + Fore.WHITE + t)
    elif c == 4:
        print(Fore.LIGHTRED_EX + f"[{m}]" + t + Fore.WHITE)
def confirm_path():
    u = getpass.getuser()
    path = f"C:/Users/{u}/AppData/Roaming/.minecraft/versions/Keio da Cocker"

    confirm = "n"
    while confirm != "y":
        pcolor(3, f"Modpack path selected as {path}")
        confirm = input("Is this correct? (y/n)")

        if confirm != "y":
            path = input("New path: ")
            path = path.replace("\\", "/")

    return path

def auto_shop():
    def values():
        pcolor(3, "How many inputs there is in the item page:")
        as_input = int(input("Input: "))

        pcolor(3, "How many outputs there is in the item page:")
        as_output = int(input("Output: "))

        pcolor(3, "How many time would you like to sell/buy this item:")
        as_time = int(input("Times: "))

        pcolor(3, f"Please confirm: Input({as_input}); Output({as_output}); Times({as_time})")
        as_confirm = input("Is this correct? (y/n)")

        if as_confirm != "y":
            values()
        else:
            mouse(as_input, as_output, as_time)
    def mouse(i, o, t):
        pcolor(3, "Position your mouse inside the first input option, inside the game shop:")
        input("Press enter: (5 Seconds Delay)")
        time.sleep(5)
        as_minput = pyautogui.position()
        pcolor(3, f"Position defined as {as_minput}")

        pcolor(3, "Position your mouse inside the first output option, inside the game shop:")
        input("Press enter: (5 Seconds Delay)")
        time.sleep(5)
        as_moutput = pyautogui.position()
        pcolor(3, f"Position defined as {as_moutput}")

        pcolor(3, "To start AutoShop press enter: (5 Seconds Delay)")
        input()
        time.sleep(5)

        # Coordinates
        as_Y = as_minput[1]
        as_inputX = as_minput[0]
        as_outputX = as_moutput[0]
        as_bc = [as_outputX, as_Y+60]

        pcolor(2, "AutoShop start!")
        for times in range(t):
            print(f"Progress: {100*(times+1)/t}%", end='\r')

            #Input
            for inputs in range(i):
                pyautogui.moveTo(as_inputX+ 45*inputs, as_Y)
                time.sleep(.05)
                pyautogui.click()

                pyautogui.moveTo(as_bc[0], as_bc[1])
                time.sleep(.05)
                pyautogui.click()
                time.sleep(.05)
            #Output
            for outputs in range(o):
                pyautogui.moveTo(as_outputX+ 45*outputs, as_Y)
                time.sleep(.05)
                pyautogui.click()
                time.sleep(.05)
        print()
        pcolor(2, "AutoShop Completed!")
        os.system("pause")
    values()

def connection(url):
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        pcolor(2, "Connection Established \n")

        return r
    else:
        pcolor(1, f"Connection Failed - {r.status_code}")
        pcolor(4, "Aborting.")
        menu()
def get_version():
    url = "https://api.github.com/repos/Keyozito/Keio-da-Cocker/tags"

    p = confirm_path()

    cv = input(Style.RESET_ALL + "Current modpack version(type 0 for auto-detect): ")
    if cv == "0":
        with open(f"{p}/README PATCHNOTE.txt", "r") as patch_file:
            patch_content = patch_file.readline()
            patch_content = patch_content.replace("V ", "").replace("\n", "")

            cv = patch_content

    pcolor(3, "Requesting Releases")
    r = connection(url)
    tags = r.json()
    av = []
    found = False

    for i in tags:
        av.append(i["name"])
        if i['name'] == cv:
            pcolor(2, f"Version {cv} found")
            found = True

    if found:
        if cv == av[0]:
            pcolor(4, "Last Version detected, aborting.")
            os.system("pause")
            menu()
        else:
            update(av[av.index(cv) - 1], p, av)
    else:
        pcolor(4, "No Version found, try manually updating your game, aborting.")
        os.system("pause")
        menu()

def zip_create(fp, f, r):
    # Loading Bar
    cs = 8192 # 8kb
    bar = tqdm(desc="Downloading", unit="B", unit_scale=True, unit_divisor=1024)

    # Create new zip and paste content
    with open(fp, "wb") as update_file:
        for c in r.iter_content(chunk_size=cs):
            update_file.write(c)
            bar.update(len(c))

    bar.close()
    tqdm._instances.clear()
    pcolor(2, f"{f} created\n")
def zip_extract(fp, p):
    pcolor(3, "Extracting Zip file")
    with zipfile.ZipFile(fp, "r") as zip_file:
        zip_file.extractall(p)

        pcolor(2, "Zip Extracted")
    os.remove(fp)

def patch_edit(fp, p):
    # Extract only patchnote
    with zipfile.ZipFile(fp, "r") as zip_file:
        zip_file.extract("README PATCHNOTE.txt", p)

    # Read file and modify old files
    with open(f"{p}/README PATCHNOTE.txt", 'r') as patchnote:
        count = 0
        while count != 2:
            line = patchnote.readline()
            # Split so it can edit old files
            ls = line.split(" ")

            if line == "==============\n":
                count += 1

            # Current applications: Delete
            appl = ["Delete", "Activate"]

            if ls[0] in appl:
                # Remove spaces and line end
                ls[1] = ls[1].replace('&', ' ')
                ls[1] = ls[1].replace('\n', '')

                # Path + Filename
                lsp = f"{p}/{ls[1]}"

                try:
                    # Delete
                    if ls[0] == "Delete":
                        pcolor(3, f"Deleting {lsp}")
                        if os.path.isdir(lsp):
                            shutil.rmtree(lsp)
                        else:
                            os.remove(lsp)
                    # Resource pack activation
                    # Deactivation is treated as Delete
                    # Activate command NEED to be on the low lines when in patch notes, or at least bellow the creation of the resource pack itself
                    elif ls[0] == "Activate":
                        pcolor(3, f"Activating {ls[1]}")

                        with open(f"{p}/options.txt", 'r') as optionsF:
                            optionsFile = optionsF.readlines()

                        for n, lineI in enumerate(optionsFile):
                            if lineI.startswith("resourcePacks:"):
                                lineI = lineI.replace("resourcePacks:", "")
                                textures = ast.literal_eval(lineI)

                                if ls[1] not in textures:
                                    textures.append(f"file/{ls[1]}")

                                # Rewrite activated resource packs
                                with open(f"{p}/options.txt", 'w') as optionsF:
                                    optionsFile[n] = f"resourcePacks:{textures}\n"
                                    optionsF.writelines(optionsFile)

                                break
                        pcolor(2, f"{ls[1]} Activated")
                except Exception as E:
                    pcolor(4, f"Couldn't {ls[0]} {ls[1]} - {E}")

def check_chain(new_current, tags, p):
    if new_current != tags[0]:
        next_v = tags[tags.index(new_current) - 1]
        pcolor(2, f"New version detected - {next_v}")

        check_input = input("Would you like to update again? (y/n)")
        if check_input == "y":
            update(next_v, p, tags)
def update(version, p, tags):
    file_zip = f"Update.{version}.zip"
    url = f"https://github.com/Keyozito/Keio-da-Cocker/releases/download/{version}/{file_zip}"

    pcolor(3, f"Downloading {file_zip}")
    r = connection(url)

    file_path = f"{p}/{file_zip}"

    zip_create(file_path, file_zip, r)
    patch_edit(file_path, p)
    zip_extract(file_path, p)
    check_chain(version, tags, p)

    pcolor(2, "Modpack ready to go!")
    os.system("pause")

menu()
