import os
import subprocess
from tkinter import *
background = "#f0e68c"

def reddit_gui():
    """ GUI for Reddit as Platform """
    reddit_root = Tk()
    reddit_root.title(" ൠ    Reddit Scrapper")
    reddit_root.resizable(False, False)
    
    canvas = Canvas(reddit_root, height= 700, width=700, bg=background)
    canvas.pack()
    
    title = Label(canvas, text="Post Scrapper", bg=background, font=("Adobe Garamond Pro", 18, "bold"))
    canvas.create_window(350, 130, window=title)
    
    reddit_logo = PhotoImage(file=os.path.join("res", "reddit.png"))
    logo_label = Label(canvas, image=reddit_logo, bg=background)
    canvas.create_window(350, 60, window=logo_label)
    
    client_id_label = Label(canvas, text="Client ID:", bg=background, font=("Adobe Garamond Pro", 12, "bold"))
    canvas.create_window(250, 230, window=client_id_label)
    client_id = Entry(canvas, width=25, font=('', 14))
    canvas.create_window(450, 230, window=client_id)
    
    client_id_label = Label(canvas, text="Client ID:", bg=background, font=("Adobe Garamond Pro", 12, "bold"))
    canvas.create_window(250, 320, window=client_id_label)
    client_id = Entry(canvas, width=25, font=('', 14))
    canvas.create_window(450, 320, window=client_id)
    
    reddit_root.mainloop()

def main_gui():
    """ Main GUI """
    root = Tk()
    root.title("Short Video Generator")
    root.resizable(False, False)
    
    canvas = Canvas(root, height=400, width=400, bg=background)
    canvas.pack()
    
    title = Label(canvas, text="Short Video\nGenerator", bg=background, font=('Terminal', 30, "bold"), fg="black")
    canvas.create_window(200, 80, window=title)
    
    opt = Label(canvas, text="Choose the platform:", bg=background, font=("Adobe Garamond Pro", 15, "bold underline"), fg="black")
    canvas.create_window(200, 190, window=opt)
    
    openai = PhotoImage(file=os.path.join("res", "openai.png"))
    openai_button = Button(canvas, image=openai, height=80, width=80, border=0)
    canvas.create_window(100, 260, window=openai_button)
    
    reddit = PhotoImage(file=os.path.join("res", "reddit.png"))
    reddit_button = Button(canvas, image=reddit, height=80, width=80, border=0, bg=background, command=lambda: (root.destroy(), reddit_gui()))
    canvas.create_window(300, 260, window=reddit_button)
    
    root.mainloop()
    
if __name__ == "__main__":
    main_gui()