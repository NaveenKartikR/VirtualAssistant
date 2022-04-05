from pyautogui import *
import os, psutil, pathlib
import PIL, pyscreeze
from pytesseract import pytesseract

'''begin_pic = "C:/Users/ABI/Desktop/BE CSE/Projects/Virtual Assistant/hdmi pics/begin.png"
begin_cur_pic = "C:/Users/ABI/Desktop/BE CSE/Projects/Virtual Assistant/hdmi pics/begin_cur.png"
play_pic = "C:/Users/ABI/Desktop/BE CSE/Projects/Virtual Assistant/hdmi pics/play.png"
play_cur_pic = "C:/Users/ABI/Desktop/BE CSE/Projects/Virtual Assistant/hdmi pics/play_cur.png"
left_pic = "C:/Users/ABI/Desktop/BE CSE/Projects/Virtual Assistant/hdmi pics/left.png"
left_cur_pic = "C:/Users/ABI/Desktop/BE CSE/Projects/Virtual Assistant/hdmi pics/left_cur.png"
right_pic = "C:/Users/ABI/Desktop/BE CSE/Projects/Virtual Assistant/hdmi pics/right.png"
right_cur_pic = "C:/Users/ABI/Desktop/BE CSE/Projects/Virtual Assistant/hdmi pics/right_cur.png"
end_pic = "C:/Users/ABI/Desktop/BE CSE/Projects/Virtual Assistant/hdmi pics/end.png"
end_cur_pic = "C:/Users/ABI/Desktop/BE CSE/Projects/Virtual Assistant/hdmi pics/end_cur.png"
bg = "C:/Users/ABI/Desktop/BE CSE/Projects/Virtual Assistant/hdmi pics/big.png"'''

file_path = str(pathlib.Path(__file__).parent.absolute())
file_path = file_path.replace(file_path[0], file_path[0].upper())

path_to_tesseract = file_path + '\Tesseract\\tesseract.exe'
pytesseract.tesseract_cmd = path_to_tesseract

doc_scr = (495, 620)
terminal = (1596, 985)
doc_init = (87, 436)
doc_color = (255, 255, 255)
doc_ss_region = (75, 410, 155, 461)
play_coord = (2478, 894)
left_coord = (2564, 891)
right_coord = (2663, 893)

count = 0
ok = False

windows_list = getAllTitles()
vscode = 'HDMI control.py - Visual Studio Code'
prime = 'Prime Video - Google Chrome'
doc = 'HDMI control doc - Google Docs - Google Chrome'

def clear_screen():
    click(doc_scr[0], doc_scr[1])
    hotkey('ctrl', 'a')
    press('backspace')
    click(terminal[0], terminal[1])

print("Prepare initial setup.\nType \"Begin\" in the Google doc when you are done.\nType \"End\" in the Google doc to abort operation\n")

while not ok:
    pix = PIL.ImageGrab.grab().load()[doc_init[0], doc_init[1]]
    status = not(pix == doc_color)
    if status:
        img = screenshot(region = doc_ss_region)
        text = pytesseract.image_to_string(img)
        text = text[:-1]
        if ("B" in text):
            print("Initial requirements satisfied. Starting process...")
            clear_screen()
            ok = True
        elif ("E" in text):
            clear_screen()
            print("\nProgram terminated before operation\n")
            exit()

CPU_usage = psutil.cpu_percent(4)
PLAY = True if CPU_usage > 5 else False

def perform_action():
    global PLAY
    global count
    #print("Some action")
    img = screenshot(region = doc_ss_region)
    text = pytesseract.image_to_string(img)
    text = text[:-1]
    #print(text)
    if ("P" in text):
        click(play_coord[0], play_coord[1])
        if PLAY:
            click(left_coord[0], left_coord[1])
        PLAY = not PLAY
        #print("Play")
    elif ("L" in text):
        click(left_coord[0], left_coord[1], 3)
        #print("Left")
    elif ("R" in text):
        click(right_coord[0], right_coord[1], 2)
        #print("Right")
    elif ("E" in text):
        print("\nNo of loops : {}\n".format(count))
        clear_screen()
        exit()
    clear_screen()

while True:
    try:
        pix = PIL.ImageGrab.grab().load()[doc_init[0], doc_init[1]]
    except:
        print("\nNo of loops : {}\n".format(count))
        break
    count += 1
    cmd = not(pix == doc_color)
    if cmd:
       perform_action()