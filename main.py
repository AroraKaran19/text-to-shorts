import os
import subprocess
import sqlite3
from random import choice
import shutil

background = "white"
db_name = "reddit_info.db"
table = "users"

def on_close(gui):
    result = askokcancel("Exit", "Do you want to exit?")
    if result:
        gui.destroy()

def shorts_generator(post_title, post_content):
    """ Generates Video """
    audio=video.generate_audio(post_title.replace("?",""    ), post_content)
    content=post_title+post_content
    content= "\n".join([" ".join(content.split()[i:i+18]) for i in range(0, len(content.split()), 18)])
    video.create_video(audio, content)
    

def fetch_post(community, post_id, gui):
    """ Fetches Post """
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute(f"SELECT * from {table}")
    content = c.fetchone()
    conn.close()
    if content is not None:
        client_id, client_secret = content[0].replace('\n', ''), content[1].replace('\t', '')
    reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                    user_agent='ytshorts')
    try:
        subreddit = reddit.subreddit(community)
        if post_id in ('', ' '):
            post_id = choice(list(subreddit.new()))
    
        post = reddit.submission(id=post_id)

        post_title=post.title
        post_content=post.selftext
        print("------------------------------------------------")
        print("\n(!) Title: ", post_title)
        print("\n(!) Content: ", post_content)
        print(f"\n(!) Post Link: https://reddit.com/r/{community}/comments/{post_id}")
        print("\n------------------------------------------------")
        gui.destroy()
        shorts_generator(post_title, post_content)
        
    except prawcore.exceptions.Redirect or ValueError:
        showerror("Invalid Community", "Enter Appropriate Community Name or\nEntered community doesn't exists!")

def reddit_gui():
    """ GUI for Reddit Post Scrapping """
    if os.path.exists("reddit_info.db"):
        reddit_root = Tk()
        reddit_root.title(" ൠ    Reddit Scrapper")
        reddit_root.resizable(False, False)
        
        canvas = Canvas(reddit_root, height=550, width=700, bg=background)
        canvas.pack()
        
        title = Label(canvas, text="Post Scrapper", bg=background, font=(title_font[os.name], 18, "bold"))
        canvas.create_window(350, 130, window=title)
        
        reddit_logo = PhotoImage(file=os.path.join("res", "reddit.png"))
        logo_label = Label(canvas, image=reddit_logo, bg=background)
        canvas.create_window(350, 60, window=logo_label)
        
        community_label = Label(canvas, text="Community:", bg=background, font=(title_font[os.name], 12, "bold"))
        canvas.create_window(195, 330, window=community_label)
        subreddit_community = Entry(canvas, width=25, font=(title_font[os.name], 14), bg="#159895")
        canvas.create_window(400, 330, window=subreddit_community)
        
        post_label = Label(canvas, text="Post ID:", bg=background, font=(title_font[os.name], 12, "bold"))
        canvas.create_window(210, 380, window=post_label)
        post_id = Entry(canvas, width=25, font=(title_font[os.name], 14), bg="#159895")
        canvas.create_window(400, 380, window=post_id)
        
        back_button = Button(canvas, text="Back", bg="red", font=(title_font[os.name], 12, "bold"), pady=5, command=lambda: (reddit_root.destroy(), main_gui()))
        canvas.create_window(50, 50, window=back_button)
        
        create_button = Button(canvas, text="Create Video", bg="lime", font=(title_font[os.name], 12, "bold"), pady=8, command=lambda: fetch_post(subreddit_community.get(), post_id.get(), reddit_root))
        canvas.create_window(350, 450, window=create_button)
        
        reddit_root.eval('tk::PlaceWindow . center')
        reddit_root.protocol("WM_DELETE_WINDOW", lambda: on_close(reddit_root))
        reddit_root.mainloop()
    else:
        showerror("(!) Login Required (!)", "Please Login to use this feature!")
        main_gui()
    
def save_reddit_info(client_id, client_secret):
    """ Store Reddit API credentials on the local device 
        for streamlined access and usage."""
    columns = "client_id TEXT, client_secret TEXT"
    if os.path.exists(db_name):
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table,))
        table_exists = c.fetchone() is not None
        if table_exists:
            c.execute("INSERT INTO users (client_id, client_secret) VALUES (?, ?)", (client_id, client_secret))
            conn.commit()
            conn.close()
        else:
            c.execute(f"CREATE TABLE {table} ({columns})")
            save_reddit_info(client_id, client_secret)
            conn.close()
            showinfo("(!) Login (!)", "Info Saved Successfully!")
            login_gui.destroy()
            main_gui()
    else:
        showinfo("(!) Creating Database... (!)", "Database created!")
        conn = sqlite3.connect(db_name)
        conn.close()
        save_reddit_info(client_id, client_secret)
        
def reddit_login_gui():
    """ GUI for storing Reddit API credentials """
    global login_gui
    login_gui = Tk()
    login_gui.title("Login")
    login_gui.resizable(False,False)
    
    canvas = Canvas(login_gui, bg=background, height=300, width=300)
    canvas.pack()
    
    login_label = Label(canvas, text="Login", bg=background, font=('Adobe Garamond Pro', 20, "bold"))
    canvas.create_window(150, 30, window=login_label)
    
    client_id_label = Label(canvas, text="Client ID:", bg=background, font=(title_font[os.name], 10, "bold"))
    canvas.create_window(70, 100, window=client_id_label)
    client_id = Entry(canvas, width=25, font=(title_font[os.name], 10), bg="#159895")
    canvas.create_window(200, 100, window=client_id)
    
    client_secret_label = Label(canvas, text="Client Secret:", bg=background, font=(title_font[os.name], 10, "bold"))
    canvas.create_window(60, 150, window=client_secret_label)
    client_secret = Entry(canvas, width=25, font=(title_font[os.name], 10), bg="#159895")
    canvas.create_window(200, 150, window=client_secret)
    
    exit_button = Button(canvas, text="Exit", bg="red", font=('Adobe Garamond Pro', 10), pady=5, padx=6, command=lambda: (login_gui.destroy(), main_gui()))
    canvas.create_window(30, 30, window=exit_button)

    save_button = Button(canvas, text="Save", bg="lime", font=('Adobe Garamond Pro', 10), pady=8, padx=10, command=lambda: (save_reddit_info(client_id.get(), client_secret.get())))
    canvas.create_window(150, 220, window=save_button)
    
    login_gui.eval('tk::PlaceWindow . center')
    login_gui.protocol("WM_DELETE_WINDOW", lambda: on_close(login_gui))
    login_gui.mainloop()
    
def reddit_login():
    """ The system verifies the presence of Reddit API credentials for the user and, 
        if one is detected, proceeds with the next step. If a client ID is not present, 
        the user is prompted to provide one. """
    if os.path.exists(db_name):
        with sqlite3.connect(db_name) as conn:
            c = conn.cursor()
            c.execute(f"SELECT * from {table}")
            content = c.fetchone()
        if content is not None:
            client_id = content[0]
            opt = askyesno("Reddit API credentials", f"Currently Using:\nClient ID: {client_id}\nDo you want to continue?")
            if opt:
                root.destroy()
                reddit_gui()
            else:
                showwarning("Process Cancelled!", "Getting you Back....")
    else:
        opt = askyesno("Reddit API credentials", "Currently We don't have your Reddit API credentials\nDo you wish to add API credentials")
        if opt:
            root.destroy()
            reddit_login_gui()

def font_fix_linux(font_dir):
    # if font_dir is not empty
    if os.listdir(font_dir):
        home_dir = os.path.expanduser("~")
        target_dir = os.path.join(home_dir, ".fonts")

        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
            
        for font_file in os.listdir(font_dir):
            font_path = os.path.join(font_dir, font_file)
            if os.path.isfile(font_path) and (font_file.lower().endswith(".ttf") or font_file.lower().endswith(".otf")):
                target_file = os.path.join(target_dir, font_file)
                if not os.path.exists(target_file):
                    shutil.copy(font_path, target_dir)

            
def logout(gui):
    gui.destroy()
    os.remove("reddit_info.db")
    main_gui()

def main_gui():
    """ HOME Page """
    global root
    root = Tk()
    root.title("Text To Shorts")
    root.resizable(False, False)
    
    canvas = Canvas(root, height=700, width=1000, bg=background)
    canvas.pack()
    
    header = Frame(canvas, bg="#159895", height=110, width=1010)
    canvas.create_window(500, 50, window=header)

    logo_img = Image.open('res/logo.png')
    logo_img = logo_img.resize((80, 80))
    logo = ImageTk.PhotoImage(logo_img)
    logo_label = Label(canvas, image=logo, bg="#159895")
    canvas.create_window(50, 50, window=logo_label)    
    
    title = Label(canvas, text="Text To Shorts\nEngine", bg=background, font=(title_font[os.name], 32, ""), fg="black")
    canvas.create_window(500, 200, window=title)
    
    opt = Label(canvas, text="Choose Your Platform", bg=background, font=(title_font[os.name], 15, "bold underline"), fg="black")
    canvas.create_window(500, 280, window=opt)
    
    # open ai button
    openai = PhotoImage(file=os.path.join("res", "openai.png"))
    openai_button = Button(canvas, image=openai, height=80, width=80, border=0, command=lambda: showinfo("Coming Soon!", "This feature will be available in the next update!"))
    canvas.create_window(360, 380, window=openai_button)
    
    # reddit button
    reddit = PhotoImage(file=os.path.join("res", "reddit.png"))
    reddit_button = Button(canvas, image=reddit, height=80, width=80, border=0, bg=background, command=lambda: (root.destroy(), reddit_gui()))
    canvas.create_window(640, 380, window=reddit_button)

    # clip manager button
    clip_manager_button = Button(canvas, text="Video Trimmer", fg="black", font=(title_font[os.name], 15), height=2, width=20, bg="#10A37F", command=lambda: video.video_section(True))
    canvas.create_window(700, 50, window=clip_manager_button)
    
    if os.path.isfile("reddit_info.db"):
        logout_button = Button(canvas, text="Logout", fg="black", font=(title_font[os.name], 15), height=2, width=10, bg="#10A37F", command=lambda: logout(root))
        canvas.create_window(900, 50, window=logout_button)
    else:
        login_button = Button(canvas, text="Login", fg="black", font=(title_font[os.name], 15), height=2, width=10, bg="#10A37F", command=lambda: reddit_login())
        canvas.create_window(900, 50, window=login_button)
    
    root.eval('tk::PlaceWindow . center')
    root.protocol("WM_DELETE_WINDOW", lambda: on_close(root))
    root.mainloop()
    
if __name__ == "__main__":
    if os.name != "nt" and os.name != "darwin":
            # fix font issues in linux
            font_fix_linux("res/fonts")
    # make video directory if not present
    title_font={"nt":"Terminal", "posix":"Monolisa"}
    if not os.path.exists("clips"):
        os.mkdir("clips")
    try:
        import praw, prawcore
        import video
        from tkinter import *
        from tkinter.messagebox import *
        from PIL import ImageTk, Image
        if os.name == "nt":
            result = subprocess.run(["magick", "identify", "--version"], capture_output=True)
        else:
            result = subprocess.run(["convert", "--version"], capture_output=True)
        main_gui()
    except ModuleNotFoundError or FileNotFoundError:
        try:
            from tkinter import *
            from tkinter.messagebox import *
            from PIL import ImageTk, Image
        except ModuleNotFoundError:
            if os.name != "nt":
                result = subprocess.run(["sudo", "apt-get", "install", "python-tk"])
            result = subprocess.run(["pip", "install", "Pillow"])
        opt = askokcancel("Install Library", "This Application requires python 'praw', 'OpenCV', 'gtts'  and 'MoviePY' libraries\nDo you wish to install it?")
        if opt:
            try:
                if os.name == "nt":
                    result = subprocess.run(["magick", "identify", "--version"], capture_output=True)
                else:
                    result = subprocess.run(["convert", "--version"], capture_output=True)
            except FileNotFoundError:
                # install ImageMagick since moviepy requires it
                if os.name == "nt":
                    result = subprocess.run(["winget", "install", "-e", "--id", "ImageMagick.ImageMagick"])
                else:
                    result = subprocess.run(["sudo", "apt-get", "install", "imagemagick"])
            except:
                showerror("Error!", "Error Occured!\nWhile installing 'ImageMagick' \nReport on issues section\nhttps://github.com/AroraKaran19/gpt-to-shorts/issues")
            result = subprocess.run(["pip", "install", "-r", "requirements.txt"])
            if result:
                showinfo("Install Library", "(!) Successfully Installed (!)")
                import praw, prawcore
                import video

                main_gui()
            else:
                showerror("Error!!", "Error Occured!\nWhile Installing from Requirements.txt\nReport on issues section\nhttps://github.com/AroraKaran19/gpt-to-shorts/issues")
        else:
            showinfo("(!) Exiting.. (!)", "Taking you back!")
