#the final file of tts python s6 microproject
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import Combobox
import pyttsx3
import os
import requests
from PIL import Image, ImageTk
from io import BytesIO
import mysql.connector
from tkinter import messagebox

root = tk.Tk()
root.title("TEXT TO SPEECH")
root.geometry("900x450+200+200")
root.resizable(False, False)
root.configure(bg="#305065")

# Initialize MySQL connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="jeethu_pass22",
    database="S6_PY_MICROPROJECT_TTS"
)
cursor = conn.cursor()

# Initialize pyttsx3 engine
engine = pyttsx3.init()

class Myclass:
    def __init__(self):
        pass

    def speaknow(self):
        self.text = text_area.get(1.0, END).strip()
        gender = gender_combobox.get()
        speed = speed_combobox.get()
        voices = engine.getProperty('voices')

        if self.text:
            # check if the text already exits in the database
            query = "SELECT COUNT(*) FROM RECENT_ENTRIES WHERE ENTRIES = %s"
            cursor.execute(query, (self.text,))
            result = cursor.fetchone()[0]
            # Insert text into database if its not existing
            if result==0:
                query = "INSERT INTO RECENT_ENTRIES (ENTRIES) VALUES (%s)"
                cursor.execute(query, (self.text,))
                conn.commit()

            def setVoice():
                if gender == 'Male':
                    engine.setProperty('voice', voices[0].id)
                else:
                    engine.setProperty('voice', voices[1].id)

            setVoice()

            if speed == "Fast":
                engine.setProperty('rate', 250)
            elif speed == 'Normal':
                engine.setProperty('rate', 150)
            else:
                engine.setProperty('rate', 60)

            engine.say(self.text)
            engine.runAndWait()

def view_recent():
    # Retrieve recent entries from the database
    cursor.execute("SELECT ENTRIES FROM RECENT_ENTRIES ORDER BY id ")
    recent_entries = cursor.fetchall()

    # Display recent entries in a new window
    recent_window = Toplevel(root)
    recent_window.title("Recent Entries")
    recent_window.geometry("400x300+300+200")

    recent_label = Label(recent_window, text="Recent Entries", font="arial 15 bold")
    recent_label.pack(pady=10)
    
    #selecting the previous list from recent
    def on_select(event):
        # Retrieve the index of the selected item
        selected_index = recent_text.curselection()
        if selected_index:
            # Retrieve the text of the selected item
            selected_text = recent_text.get(selected_index)
            # Update the text area with the selected text
            text_area.delete(1.0, END)
            text_area.insert(END, selected_text)

    recent_text = Listbox(recent_window, font="Roboto 12", selectmode=tk.SINGLE)
    recent_text.pack(pady=10)
    recent_text.bind("<<ListboxSelect>>", on_select)
    #inserting entries in db to listbox
    for entry in recent_entries:
        recent_text.insert(END, entry[0] + "\n")
        #recent_text.configure(state='disabled')
        
  
def download():
    text = text_area.get(1.0, END)
    gender = gender_combobox.get()
    speed = speed_combobox.get()
    voices = engine.getProperty('voices')

    if text:
        def setVoice():
            if gender == 'Male':
                engine.setProperty('voice', voices[0].id)
            else:
                engine.setProperty('voice', voices[1].id)

        setVoice()

        if speed == "Fast":
            engine.setProperty('rate', 250)
        elif speed == 'Normal':
            engine.setProperty('rate', 150)
        else:
            engine.setProperty('rate', 60)

        path = filedialog.askdirectory()
        os.chdir(path)
        engine.save_to_file(text, 'text.mp3')
        engine.runAndWait()


# Icon
url = "https://th.bing.com/th/id/OIP.K63A0AvsV73xRz5A3KpcZwHaHa?rs=1&pid=ImgDetMain"
response = requests.get(url)
image_data = response.content
image = Image.open(BytesIO(image_data))
photo = ImageTk.PhotoImage(image)
root.iconphoto(False, photo)

# Top frame
Top_frame = Frame(root, bg="white", width=900, height=100)
Top_frame.place(x=0, y=0)
Label(Top_frame, text="Text to Speech", font="arial 20 bold", bg="white", fg="black").place(x=100, y=30)

# Text area creation ,events for characters entered into text area
text_area = Text(root, font="Roboto 20", bg="white", relief=GROOVE, wrap=WORD)
text_area.place(x=10, y=150, width=500, height=250)
def check_character_limit(event):
    # Get the current content of the text field
    text_content = text_area.get(1.0, "end-1c")  # "end-1c" excludes the trailing newline character
    character_limit = 10
    # Check if the character limit is exceeded
    if len(text_content) > character_limit:
        messagebox.showwarning(title="character exceeded",message="character limit exceeded")
        text_area.delete(1.0,END)
# Bind the event handler to the text field
text_area.bind("<KeyPress>", check_character_limit)

def check_forbidden_characters(event):
    # Define the forbidden characters
    forbidden_characters = "*!@#%^&()"  
    # Get the current content of the text field
    text_content = text_area.get(1.0, "end-1c")  # "end-1c" excludes the trailing newline character
    # Check if any forbidden characters are present
    forbidden_found = any(char in text_content for char in forbidden_characters)
    if forbidden_found:
        messagebox.showwarning(title="forbidden char",message="forbidden characters used")
        text_area.delete(1.0,END)
# Bind the event handler to the text field
text_area.bind("<KeyRelease>", check_forbidden_characters)

#labels
Label(root, text="VOICE", font="arial 15 bold", bg="#305065", fg="white").place(x=580, y=160)
Label(root, text="SPEED", font="arial 15 bold", bg="#305065", fg="white").place(x=760, y=160)

#combobox
gender_combobox = Combobox(root, values=['Male', 'Female'], font="arial 14", state='readonly', width=10)
gender_combobox.place(x=550, y=200)
speed_combobox = Combobox(root, values=['Fast', 'Normal', 'Slow'], font="arial 14", state='readonly', width=10)
speed_combobox.place(x=730, y=200)
speed_combobox.set('Normal')
gender_combobox.set('Male')

obj = Myclass()
#buttons
btn = Button(root, text="Speak", width=10, font="arial 14 bold", command=obj.speaknow)
btn.place(x=550, y=280)
save = Button(root, text="Save", width=10, bg="#39c790", font="arial 14 bold", command=download)
save.place(x=730, y=280)

view_recent_btn = Button(root, text="View Recent", width=10, font="arial 14 bold", command=view_recent)
view_recent_btn.place(x=640, y=350)

root.mainloop()
