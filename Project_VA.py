##############################################################################

# IMPORTING REQUIRED MODULES # 

from speech_recognition import *
import pyttsx3
import googletrans
from googletrans import Translator
import webbrowser, wikipedia
from gtts import gTTS
from playsound import playsound
import os, subprocess, pathlib
import datetime
from tkinter import *
from tkinter import ttk
import tkinter.filedialog
from tkinter import messagebox
from io import BytesIO
from PIL import Image, ImageTk
from pytesseract import pytesseract
import string, random
import json, pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model

##############################################################################

# LOADING AND INITIALIZING PRE-REQUISITES #

file_path = str(pathlib.Path(__file__).parent.absolute())
file_path = file_path.replace(file_path[0], file_path[0].upper())

lemmatizer = WordNetLemmatizer()
intents = json.loads(open(file_path + '\intents.json').read())

va_Laura = pyttsx3.init()
va_Laura.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0')
va_Laura.setProperty('rate',180)

recog = Recognizer()
mic = Microphone()

translate_client = Translator()
languages = googletrans.LANGUAGES
languages['zh-cn'], languages['zh-tw'] = 'chinese', 'chinese traditional'
translate_error_message = 'Sorry, Not able to translate. Try Again.'
translate = {}

path_to_tesseract = file_path + '\Tesseract\\tesseract.exe'
pytesseract.tesseract_cmd = path_to_tesseract

webbrowser.register('google-chrome', None, webbrowser.BackgroundBrowser(r"C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"))

name = ["lara", "lora", "laura", "lo ra", "lohra", "lahra"]

words = pickle.load(open(file_path + '\words.pkl', 'rb'))
classes = pickle.load(open(file_path + '\classes.pkl', 'rb'))
model = load_model(file_path + '\AI_chatbot_model.h5')

##############################################################################

# TEXT TO SPEECH #

def speak_text_cmd(cmd):
    va_Laura.say(cmd)
    va_Laura.runAndWait()

##############################################################################

# OTHER LANGUAGE TEXT TO SPEECH #

def g_speak(text, language = 'en'):
    try:
        voice = gTTS(text = text, lang = language)
        voice.save("voice.mp3")
        playsound("voice.mp3")
        os.remove("voice.mp3")
    except ValueError:
        pass

##############################################################################

# TEXT THROUGH SPEECH RECOGNITION #

def listen(lang = 'en-US', init_time = None, phrase_time = None):
    recognized = ""
    while recognized == "":
        with mic:
            try:
                audio = recog.listen(mic, init_time, phrase_time)
            except:
                pass
        try:
            recognized = recog.recognize_google(audio, language = lang)
        except UnknownValueError:
            pass
        except TimeoutError:
            pass
        except ConnectionAbortedError:
            pass
        except RequestError:
            print("Sorry network error. Please try again")
        rcgnd = recognized.lower()
        for i in name:
                if i in rcgnd:
                    rcgnd = rcgnd.replace(i, "laura")
                    break
    print(rcgnd.capitalize())
    return rcgnd

##############################################################################

# TRANSLATOR #

def translate():
    src_code = ""
    dest_code = ""

    while src_code == "":
        with mic:
            recog.adjust_for_ambient_noise(mic, duration = 1)
        print("\nFROM WHAT LANGUAGE ? ", end = '')
        src = listen()
        for i in languages:
            if languages[i] == src:
                src_code = i
                break
        if src_code == '':
            print("Source language not found")

    while dest_code == "":
        with mic:
            recog.adjust_for_ambient_noise(mic, duration = 1)
        print("\nTO WHAT LANGUAGE ? ", end = '')
        dest = listen()
        for i in languages:
            if languages[i] == dest:
                dest_code = i
                break
        if dest_code == '':
            print("Destination language not found")
    
    with mic:
        recog.adjust_for_ambient_noise(mic, duration = 1)
    print("\nPHRASE : ", end = '')
    phrase = listen(src_code)
    try:
        translate = translate_client.translate(phrase, dest = dest_code, src = src_code)
        print("\nTRANSLATED TEXT :", translate.text)
        g_speak(translate.text, dest_code)
    except AttributeError:
        print(translate_error_message)
    except  IndexError:
        print(translate_error_message)

##############################################################################

# OPEN APPLICATION #

def open_application(cmd):
    if cmd == "e":
        subprocess.Popen("C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE")
    elif cmd == "b":
        subprocess.Popen("C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE")
    elif cmd == "c":
        subprocess.Popen('C:\\Windows\\System32\\calc.exe')
    elif cmd == "d":
        os.system("notepad")
    '''elif "media player" in cmd:
        print("Opening media player")
        speak_text_cmd("Opening media player")
        os.startfile("C:\Program Files (x86)\K-Lite Codec Pack\MPC-HC64\mpc-hc64.exe")
    elif "ccleaner" in cmd:
        print("Opening ccleaner")
        speak_text_cmd("Opening ccleaner")
        os.startfile("C:\Program Files\CCleaner\CCleaner64.exe")'''

##############################################################################

# OCR #

def image_to_text():
    ocr_root = Tk()
    ocr_root.geometry("400x500")
    def open_img():
        myfile = tkinter.filedialog.askopenfilename(filetypes = ([('png', '*.png'),('jpeg', '*.jpeg'),('jpg', '*.jpg'),('All Files', '*.*')]))
        if not myfile:
            messagebox.showerror("Error","You have selected nothing !")
        else:
            img = Image.open(myfile)
            text = pytesseract.image_to_string(img)
            print(text[:-1])
    open_button = Button(ocr_root, text = "Open image file", command = open_img, padx = 20, pady = 10)
    open_button.pack()
    ocr_root.mainloop()

##############################################################################

# INTERNET SEARCH #

def internet_search(cmd):
    if cmd == "i":
        results = ""
        while results == "":
            with mic:
                recog.adjust_for_ambient_noise(mic, duration = 1)
            print("\nWHAT DO YOU WANT TO SEARCH ? ", end = '')
            cmd = listen()
            print()
            try:
                results = wikipedia.summary(cmd, sentences = 3)
            except wikipedia.exceptions.DisambiguationError:
                print("Please give a specific search")
                continue
            except wikipedia.exceptions.PageError:
                print("Page doesn't exist. Try again")
                continue
            speak_text_cmd("According to Wikipedia")
            print(results)
            speak_text_cmd(results)

    elif cmd == "g":
        with mic:
            recog.adjust_for_ambient_noise(mic, duration = 1)
        print("\nWHAT IS YOUR SEARCH ? ", end = '')
        search = listen()
        webbrowser.get("google-chrome").open("https://www.youtube.com/results?search_query=" + search)

    elif cmd == "f":
        with mic:
            recog.adjust_for_ambient_noise(mic, duration = 1)
        print("\nWHAT IS YOUR SEARCH ? ", end = '')
        search = listen()
        webbrowser.get("google-chrome").open('https://www.google.co.in/search?q=' + search)

    elif cmd == "h":
        webbrowser.get("google-chrome").open("stackoverflow.com")

##############################################################################

# STEGANOGRAPHY #

def steganography():
    class Stegno:
    
        art ='''¯\_(ツ)_/¯'''
        art2 = '''
    @(\/)
    (\/)-{}-)@
    @(={}=)/\)(\/)
    (\/(/\)@| (-{}-)
    (={}=)@(\/)@(/\)@
    (/\)\(={}=)/(\/)
    @(\/)\(/\)/(={}=)
    (-{}-)""""@/(/\)
    |:   |
    /::'   \\
    /:::     \\
    |::'       |
    |::        |
    \::.       /
    ':______.'
    `""""""`'''
        output_image_size = 0

        def main(self,root):
            root.title('ImageSteganography')
            root.geometry('500x600')
            root.resizable(width =False, height=False)
            f = Frame(root)

            title = Label(f,text='Image Steganography')
            title.config(font=('courier',33))
            title.grid(pady=10)

            b_encode = Button(f,text="Encode",command= lambda :self.frame1_encode(f), padx=14)
            b_encode.config(font=('courier',14))
            b_decode = Button(f,text="Decode",padx=14,command=lambda :self.frame1_decode(f))
            b_decode.config(font=('courier',14))
            b_decode.grid(pady = 12)

            ascii_art = Label(f,text=self.art)
            # ascii_art.config(font=('MingLiU-ExtB',50))
            ascii_art.config(font=('courier',60))

            ascii_art2 = Label(f,text=self.art2)
            # ascii_art.config(font=('MingLiU-ExtB',50))
            ascii_art2.config(font=('courier',12,'bold'))

            root.grid_rowconfigure(1, weight=1)
            root.grid_columnconfigure(0, weight=1)

            f.grid()
            title.grid(row=1)
            b_encode.grid(row=2)
            b_decode.grid(row=3)
            ascii_art.grid(row=4,pady=10)
            ascii_art2.grid(row=5,pady=5)

        def home(self,frame):
                frame.destroy()
                self.main(root)

        def frame1_decode(self,f):
            f.destroy()
            d_f2 = Frame(root)
            label_art = Label(d_f2, text='٩(^‿^)۶')
            label_art.config(font=('courier',90))
            label_art.grid(row =1,pady=50)
            l1 = Label(d_f2, text='Select Image with Hidden text:')
            l1.config(font=('courier',18))
            l1.grid()
            bws_button = Button(d_f2, text='Select', command=lambda :self.frame2_decode(d_f2))
            bws_button.config(font=('courier',18))
            bws_button.grid()
            back_button = Button(d_f2, text='Cancel', command=lambda : Stegno.home(self,d_f2))
            back_button.config(font=('courier',18))
            back_button.grid(pady=15)
            back_button.grid()
            d_f2.grid()

        def frame2_decode(self,d_f2):
            d_f3 = Frame(root)
            myfile = tkinter.filedialog.askopenfilename(filetypes = ([('png', '*.png'),('jpeg', '*.jpeg'),('jpg', '*.jpg'),('All Files', '*.*')]))
            if not myfile:
                messagebox.showerror("Error","You have selected nothing !")
            else:
                myimg = Image.open(myfile, 'r')
                myimage = myimg.resize((300, 200))
                img = ImageTk.PhotoImage(myimage)
                l4= Label(d_f3,text='Selected Image :')
                l4.config(font=('courier',18))
                l4.grid()
                panel = Label(d_f3, image=img)
                panel.image = img
                panel.grid()
                hidden_data = self.decode(myimg)
                l2 = Label(d_f3, text='Hidden data is :')
                l2.config(font=('courier',18))
                l2.grid(pady=10)
                text_area = Text(d_f3, width=50, height=10)
                text_area.insert(INSERT, hidden_data)
                text_area.configure(state='disabled')
                text_area.grid()
                back_button = Button(d_f3, text='Cancel', command= lambda :self.page3(d_f3))
                back_button.config(font=('courier',11))
                back_button.grid(pady=15)
                back_button.grid()
                show_info = Button(d_f3,text='More Info',command=self.info)
                show_info.config(font=('courier',11))
                show_info.grid()
                d_f3.grid(row=1)
                d_f2.destroy()

        def decode(self, image):
            data = ''
            imgdata = iter(image.getdata())

            while (True):
                pixels = [value for value in imgdata.__next__()[:3] +
                        imgdata.__next__()[:3] +
                        imgdata.__next__()[:3]]
                binstr = ''
                for i in pixels[:8]:
                    if i % 2 == 0:
                        binstr += '0'
                    else:
                        binstr += '1'

                data += chr(int(binstr, 2))
                if pixels[-1] % 2 != 0:
                    return data

        def frame1_encode(self,f):
            f.destroy()
            f2 = Frame(root)
            label_art = Label(f2, text='\'\(°Ω°)/\'')
            label_art.config(font=('courier',70))
            label_art.grid(row =1,pady=50)
            l1= Label(f2,text='Select the Image in which \nyou want to hide text :')
            l1.config(font=('courier',18))
            l1.grid()

            bws_button = Button(f2,text='Select',command=lambda : self.frame2_encode(f2))
            bws_button.config(font=('courier',18))
            bws_button.grid()
            back_button = Button(f2, text='Cancel', command=lambda : Stegno.home(self,f2))
            back_button.config(font=('courier',18))
            back_button.grid(pady=15)
            back_button.grid()
            f2.grid()


        def frame2_encode(self,f2):
            ep= Frame(root)
            myfile = tkinter.filedialog.askopenfilename(filetypes = ([('png', '*.png'),('jpeg', '*.jpeg'),('jpg', '*.jpg'),('All Files', '*.*')]))
            if not myfile:
                messagebox.showerror("Error","You have selected nothing !")
            else:
                myimg = Image.open(myfile)
                myimage = myimg.resize((300,200))
                img = ImageTk.PhotoImage(myimage)
                l3= Label(ep,text='Selected Image')
                l3.config(font=('courier',18))
                l3.grid()
                panel = Label(ep, image=img)
                panel.image = img
                self.output_image_size = os.stat(myfile)
                self.o_image_w, self.o_image_h = myimg.size
                panel.grid()
                l2 = Label(ep, text='Enter the message')
                l2.config(font=('courier',18))
                l2.grid(pady=15)
                text_area = Text(ep, width=50, height=10)
                text_area.grid()
                encode_button = Button(ep, text='Cancel', command=lambda : Stegno.home(self,ep))
                encode_button.config(font=('courier',11))
                data = text_area.get("1.0", "end-1c")
                back_button = Button(ep, text='Encode', command=lambda : [self.enc_fun(text_area,myimg),Stegno.home(self,ep)])
                back_button.config(font=('courier',11))
                back_button.grid(pady=15)
                encode_button.grid()
                ep.grid(row=1)
                f2.destroy()


        def info(self):
            try:
                str = 'original image:-\nsize of original image:{}mb\nwidth: {}\nheight: {}\n\n' \
                    'decoded image:-\nsize of decoded image: {}mb\nwidth: {}' \
                    '\nheight: {}'.format(self.output_image_size.st_size/1000000,
                                        self.o_image_w,self.o_image_h,
                                        self.d_image_size/1000000,
                                        self.d_image_w,self.d_image_h)
                messagebox.showinfo('info',str)
            except:
                messagebox.showinfo('Info','Unable to get the information')
        def genData(self,data):
            newd = []

            for i in data:
                newd.append(format(ord(i), '08b'))
            return newd

        def modPix(self,pix, data):
            datalist = self.genData(data)
            lendata = len(datalist)
            imdata = iter(pix)
            for i in range(lendata):
                # Extracting 3 pixels at a time
                pix = [value for value in imdata.__next__()[:3] +
                    imdata.__next__()[:3] +
                    imdata.__next__()[:3]]
                # Pixel value should be made
                # odd for 1 and even for 0
                for j in range(0, 8):
                    if (datalist[i][j] == '0') and (pix[j] % 2 != 0):

                        if (pix[j] % 2 != 0):
                            pix[j] -= 1

                    elif (datalist[i][j] == '1') and (pix[j] % 2 == 0):
                        pix[j] -= 1
                # Eigh^th pixel of every set tells
                # whether to stop or read further.
                # 0 means keep reading; 1 means the
                # message is over.
                if (i == lendata - 1):
                    if (pix[-1] % 2 == 0):
                        pix[-1] -= 1
                else:
                    if (pix[-1] % 2 != 0):
                        pix[-1] -= 1

                pix = tuple(pix)
                yield pix[0:3]
                yield pix[3:6]
                yield pix[6:9]

        def encode_enc(self,newimg, data):
            w = newimg.size[0]
            (x, y) = (0, 0)

            for pixel in self.modPix(newimg.getdata(), data):

                # Putting modified pixels in the new image
                newimg.putpixel((x, y), pixel)
                if (x == w - 1):
                    x = 0
                    y += 1
                else:
                    x += 1

        def enc_fun(self,text_area,myimg):
            data = text_area.get("1.0", "end-1c")
            if (len(data) == 0):
                messagebox.showinfo("Alert","Kindly enter text in TextBox")
            else:
                newimg = myimg.copy()
                self.encode_enc(newimg, data)
                my_file = BytesIO()
                temp=os.path.splitext(os.path.basename(myimg.filename))[0]
                newimg.save(tkinter.filedialog.asksaveasfilename(initialfile=temp,filetypes = ([('png', '*.png')]),defaultextension=".png"))
                self.d_image_size = my_file.tell()
                self.d_image_w,self.d_image_h = newimg.size
                messagebox.showinfo("Success","Encoding Successful\nFile is saved as Image_with_hiddentext.png in the same directory")

        def page3(self,frame):
            frame.destroy()
            self.main(root)

    root = Tk()

    o = Stegno()
    o.main(root)

    root.mainloop()

##############################################################################

# CRYPTOGRAPHY #

def cryptography():
    alpha=string.ascii_lowercase+string.ascii_uppercase
    charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

    Text = ""
    private_key = ""
    mode = ""
    Result = ""


    otp=""


    def Exit():
        root.destroy()

    def vig():
        def encrypt(msg, key):
            msg_alpha_pos = [alpha.find(i) for i in msg]  # finds the position of that alphabet in the series
            key_alpha_pos = [alpha.find(i) for i in key]
            cipher = ""
            for n in range(len(msg)):
                l = (msg_alpha_pos[n] + key_alpha_pos[n % (len(key))]) % len(alpha)
                cipher += alpha[l]
            return cipher

        def decrypt(cipher, key):
            cipher_alpha_pos = [alpha.find(i) for i in cipher]
            key_alpha_pos = [alpha.find(i) for i in key]
            msg = ""
            for n in range(len(cipher)):
                l = (cipher_alpha_pos[n] - key_alpha_pos[n % (len(key))]) % len(alpha)
                msg += alpha[l]
            return msg

        def Mode():
            Text = Text_box.get()
            private_key = private_key_box.get()
            if (mode_box.get() == 'e'):
                Result = encrypt(Text, private_key)
                Result_box.delete(0, END)
                Result_box.insert(0, Result)
            elif (mode_box.get() == 'd'):
                Result = decrypt(Text, private_key)
                Result_box.delete(0, END)
                Result_box.insert(0, Result)
            else:
                Result = 'Invalid Mode'
                Result_box.delete(0, END)
                Result_box.insert(0, Result)
        
        Label(frame2, font='arial 12 bold', text='MESSAGE').place(x=100, y=85)
        Text_box = Entry(frame2, font='arial 10', textvariable=Text, bg='ghost white')
        Text_box.place(x=350, y=85)

        Label(frame2, font='arial 12 bold', text='KEY').place(x=120, y=125)
        private_key_box = Entry(frame2, font='arial 10', textvariable=private_key, bg='ghost white')
        private_key_box.place(x=350, y=125)

        Label(frame2, font='arial 12 bold', text='MODE(e-encrypt, d-decrypt)').place(x=60, y=165)
        mode_box = Entry(frame2, font='arial 10', textvariable=mode, bg='ghost white')
        mode_box.place(x=350, y=165)
        Result_box = Entry(frame2, font='arial 10 bold', textvariable=Result, bg='ghost white')
        Result_box.place(x=350, y=225)

        Button(frame2, font='arial 10 bold', text='RESULT', padx=2, bg='LightGray', command=Mode).place(x=150, y=225)

        Button(frame2, font='arial 10 bold', text='HOME', width=6, command=frame1.tkraise, bg='OrangeRed', padx=2, pady=2).place(x=275, y=275)
        
        frame2.tkraise()

    def OTP():
        def encrypt():
            def encrypt1(plaintext):
                """Encrypt plaintext value.
                Keyword arguments:
                plaintext -- the plaintext value to encrypt.
                """
                otp = "".join(random.sample(charset, len(charset)))
                result = ""

                for c in plaintext.upper():
                    if c in charset:
                        result += otp[charset.find(c)]
                result = result.lower()

                return otp, result

            otp, Result = encrypt1(Text_box.get())
            otp_box.delete(0, END)
            Result_box.delete(0, END)
            otp_box.insert(0, otp)
            Result_box.insert(0, Result)

        def decrypt():
            def decrypt1(plaintext, otp):
                """Decrypt plaintext value.
                Keyword arguments:
                plaintext -- the plaintext value to decrypt.
                """
                result = ""

                for c in plaintext.upper():
                    if c in otp:
                        result += charset[otp.find(c)]
                result = result.lower()

                return result

            Result = decrypt1(Text_box.get(), otp_box.get())
            Result_box.delete(0, END)
            Result_box.insert(0, Result)

        Label(frame3, font='arial 12 bold', text='MESSAGE').place(x=100, y=45)
        Text_box = Entry(frame3, font='arial 10', textvariable=Text, bg='ghost white')
        Text_box.place(x=350, y=45)

        Button(frame3, font='arial 10 bold', text='ENCRYPT', padx=2, bg='LightGray', command=encrypt).place(x=140, y=110)
        Button(frame3, font='arial 10 bold', text='DECRYPT', padx=2, bg='LightGray', command=decrypt).place(x=240, y=110)

        Label(frame3, font='arial 12 bold', text='OTP').place(x=120, y=170)
        otp_box = Entry(frame3, font='arial 10', textvariable=otp, bg='ghost white')
        otp_box.place(x=350, y=170)

        Label(frame3, font='arial 12 bold', text='OUTPUT').place(x=100, y=225)
        Result_box = Entry(frame3, font='arial 10', textvariable=Result, bg='ghost white')
        Result_box.place(x=350, y=225)

        Button(frame3, font='arial 10 bold', text='HOME', width=6, command=frame1.tkraise, bg='OrangeRed', padx=2, pady=2).place(x=240, y=300)

        frame3.tkraise()

    def show_frame(frame):
        frame.tkraise()
        
    root = Tk()
    root.geometry("650x425")
    pic = PhotoImage(file = file_path + '\icon1.png')
    root.iconphoto(False,pic)
    root.title("Cryptography")

    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)

    frame1 = Frame(root)
    frame2 = Frame(root)
    frame3 = Frame(root)

    for frame in (frame1, frame2, frame3):
        frame.grid(row=0,column=0,sticky='nsew')
    #==================Frame 1 code
    pic = PhotoImage(file = file_path + '\crypt6.png')
    frame1_title = Label(frame1, image = pic)
    frame1_title.pack()

    Button(frame1, font='arial 10 bold', text='Vigenere', padx=2, bg='LightGray', command = vig).place(x=200,y=20)

    Button(frame1, font='arial 10 bold', text='OTP', padx=2, bg='LightGray', command = OTP).place(x=400,y=21)

    Button(frame1, font='arial 10 bold', text='EXIT', width=6, command=Exit, bg='OrangeRed', padx=2, pady=2).place(x=275,
                                                                                                                    y=275)

    #==================Frame 2 code
    frame2_title = Label(frame2, image = pic)
    frame2_title.pack()

    #==================Frame 3 code
    frame3_title = Label(frame3, image = pic)
    frame3_title.pack()

    show_frame(frame1)

    root.mainloop()

##############################################################################

# CHOOSE ONE OF THE ABOVE FUNCTIONS ACCORDING TO INPUT #

def reply(task):
    if ((task>="a") and (task<="l")):
        if task == "a":
            translate()
        elif ((task>="b") and (task<="e")):
            open_application(task)
        elif ((task>="f") and (task<="i")):
            internet_search(task)
        elif task == "j":
            cryptography()
        elif task == "k":
            image_to_text()
        elif task == "l":
            steganography()
    else:
        pass

##############################################################################

# PRE-PROCESSING TEXT AND CATEGORIZING IT #

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

    results.sort(key = lambda x : x[1], reverse = True)
    return_list = []
    for r in results:
        return_list.append({'intent' : classes[r[0]], 'probability' : str(r[1])})
    return return_list

def get_response(intents_list, intents_json):
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    return result, tag

##############################################################################

# MAIN FUNCTION #

predict_class("Hello")

print("\n\n--------------------------------------------------------------------------------------------------------------------\n")
date_time = datetime.datetime.now()
print("Date : " + date_time.strftime("%d-%m-%Y") + '\n')
print("Time : " + date_time.strftime("%I:%M:%S %p") + '\n')
print('''
                           ,,,                     ,,,  
                          {(:)}                   {(:)} 
                           ***                     ***                          
                            &                       &                           
                            &                       &                           
                            &                       &                           
                          ,,&,,                   ,,&,,                           
                        &||||||&                 &|||||&                       
                   ,,&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&,,                    
                 & //////////////////////////////////////////// &                
               &/////,&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&,////&           
              &/////&                                        &////&             
             &////&       0000                     0000       &////&             
             &////&     {[ () ]}                 {[ () ]}     &////&            
             &////&       0000      _________      0000       &////&            
             &/////&                \\\     //                 &////&            
              &/////&                 *ooo*                  &////&             
                &////*&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&*////&               
                  &/////////////////////////////////////////////&                 
                      ^&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&^                       
''')
try:
    with mic:
        try:
            recog.listen(mic, 1, 1)
        except:
            pass
except OSError:
    print("\nMic access denied. Give access to use Virtual Assistant\n")
    exit()

print("ALL SET. I'M READY!")
speak_text_cmd("ALL SET. I'M READY!")

dest_code = ""
while dest_code == "":
    dest_lang = input("\nEnter a language : ")
    dest_lang = dest_lang.lower()
    for i in languages:
        if languages[i] == dest_lang:
            dest_code = i
            break
    if dest_code == "":
        print("I'm not familiar with \"{}\". Please enter a different language".format(dest_lang.capitalize()))

while True:
    with mic:
        recog.adjust_for_ambient_noise(mic, duration = 1)
    print("\nYOU   : ", end = "")
    msg = listen(lang = dest_code)
    if (dest_code != "en"):
        translate_dict = translate_client.translate(msg, dest = "en", src = dest_code)
        msg = translate_dict.text
    message = msg.lower()
    ints = predict_class(message)
    if ints == []:
        print("LAURA : Sorry I don't understand your statement. Can you please repeat?")
        speak_text_cmd("Sorry I don't understand your statement. Can you please repeat?")
    else:
        res, tag = get_response(ints, intents)
        if (dest_code != "en"):
            translate_dict = translate_client.translate(res, dest = dest_code, src = "en")
            res = translate_dict.text
        print("LAURA :", res)
        if (dest_code != "en"):
            g_speak(res, dest_code)
        else:
            speak_text_cmd(res)
        if tag == "goodbye":
            print("\n\n--------------------------------------------------------------------------------------------------------------------\n\n")
            exit()
        reply(tag)

##############################################################################

print('''
                                +NN8.                          +NN+                                 
                               ?+.. N                         N+..=N.                               
                               8..  8                         8.  .D.                               
                               .DZ$8~.                        :N$ZN~                                
                                 ~D                             8~                                  
                                 ~D                             8~                                  
                                 ~D                             8~                                  
                                 ~D                             8~                                  
                                 ~D                             8~                                  
                                 ~D                             8~                                  
                                 ~D                             8~                                  
                                 ~D                             8~                                  
                                NDDD7                         IZOOD?                                
                             I8      ?O                     DI      8I                              
                            ,D        ?M                    ?        8,                             
                         IDDZ=:::,,:::::::::::::::::::::::::,::::,,::=$DDI .                   
                      .D8,.                                              ,8D.                  
                    :D?.                                                    +D:                 
                   :O       ...........................................       8D.                   
                  8M.     +DDNDDDDDDDDDDDDD8DDDDDDDDDDDDDDDDDDDDDDDDDDMDN.     .O                   
                 Z8.    ?8~                                              $N,    $Z                  
                ?8.    =7                                                 .D.    8I                 
                D.    ,D                                                   .$.    D.                
                Z     D:                                                    D     $O                
               +:    ,D        .N$IZO                         ?N77DO        O~.   .D.               
               O,    ?8       .D.   .D                       ZO.    8.      ZI     D                
               D.    7Z.      ?D     N~                      N,     D       $7     D                
               Z,    ?8.       D ...?N.    :,,,,,,,,,,,,.    ?D .  ~7.      ZI     D.               
               ~~    ,D         7NDN~..    D...........:+     .$DDD=        D:    :N                
                8.    N~                   ~I.         D.          ,        N     DI                
                8:    .8.                   =DZ.    :88.                   =+    ,D.         
                ~N     :Z.                     7NDDN~.                    ,8     D:.        
                 ~D.    .D8                                             +87.    8~         
                  =D      .ZDDDDODDZD$ZDDDDDDDDDDDDDDDDDDDDDD$N8DDDDDDDN=..    I?          
                    D,                                                       ,8=.              
                     MD.                                                    NM .                 
                      .:8O                                               O8O                        
                         .$DDNNDDDDDDDDDDDDDDDDDDDDDDDDD8DDDDDDDDDDDNND8$. .                      
''')
