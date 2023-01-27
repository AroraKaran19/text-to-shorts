import os
import subprocess
import sqlite3
from tkinter import *
from tkinter.messagebox import *

background = "#f0e68c"
db_name = "reddit_info.db"
table = "users"

def fetch_post(community, post_id):
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
    subreddit = reddit.subreddit(community)

    if post_id in ('', ' '):
        post = next(iter(subreddit.new()))
    else:
        post = reddit.submission(id=post_id)

    print("\nTitle: ", post.title)
    print("\nContent: ", post.selftext)    

def reddit_gui():
    """ GUI for Reddit Post Scrapping """
    reddit_root = Tk()
    reddit_root.title(" ൠ    Reddit Scrapper")
    reddit_root.resizable(False, False)
    
    canvas = Canvas(reddit_root, height= 550, width=700, bg=background)
    canvas.pack()
    
    title = Label(canvas, text="Post Scrapper", bg=background, font=("Adobe Garamond Pro", 18, "bold"))
    canvas.create_window(350, 130, window=title)
    
    reddit_logo = PhotoImage(file=os.path.join("res", "reddit.png"))
    logo_label = Label(canvas, image=reddit_logo, bg=background)
    canvas.create_window(350, 60, window=logo_label)
    
    community_label = Label(canvas, text="Community:", bg=background, font=("Adobe Garamond Pro", 12, "bold"))
    canvas.create_window(195, 330, window=community_label)
    subreddit_community = Entry(canvas, width=25, font=('', 14))
    canvas.create_window(400, 330, window=subreddit_community)
    
    post_label = Label(canvas, text="Post ID:", bg=background, font=("Adobe Garamond Pro", 12, "bold"))
    canvas.create_window(210, 380, window=post_label)
    post_id = Entry(canvas, width=25, font=('', 14))
    canvas.create_window(400, 380, window=post_id)
    
    create_button = Button(canvas, text="Create Video", bg="lime", font=("Adobe Garamond Pro", 12, "bold"), pady=8, command=lambda: fetch_post(subreddit_community.get(), post_id.get()))
    canvas.create_window(350, 450, window=create_button)
    
    reddit_root.eval('tk::PlaceWindow . center')
    reddit_root.mainloop()
    
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
        else:
            c.execute(f"CREATE TABLE {table} ({columns})")
            save_reddit_info(client_id, client_secret)
            conn.close()
            showinfo("(!) Login (!)", "Info Saved Successfully!")
            login_gui.destroy()
            reddit_gui()
    else:
        showinfo("(!) Creating Database... (!)", "Database created!")
        conn = sqlite3.connect(db_name)
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
    
    client_id_label = Label(canvas, text="Client ID:", bg=background, font=("Adobe Garamond Pro", 10, "bold"))
    canvas.create_window(70, 100, window=client_id_label)
    client_id = Entry(canvas, width=25, font=('', 10))
    canvas.create_window(200, 100, window=client_id)
    
    client_secret_label = Label(canvas, text="Client Secret:", bg=background, font=("Adobe Garamond Pro", 10, "bold"))
    canvas.create_window(60, 150, window=client_secret_label)
    client_secret = Entry(canvas, width=25, font=('', 10))
    canvas.create_window(200, 150, window=client_secret)

    save_button = Button(canvas, text="Save", bg="lime", font=('Adobe Garamond Pro', 10), pady=8, padx=10, command=lambda: (save_reddit_info(client_id.get(), client_secret.get())))
    canvas.create_window(150, 220, window=save_button)
    
    login_gui.eval('tk::PlaceWindow . center')
    login_gui.mainloop()
    
def reddit_login():
    """ The system verifies the presence of Reddit API credentials for the user and, 
        if one is detected, proceeds with the next step. If a client ID is not present, 
        the user is prompted to provide one. """
    if os.path.exists(db_name):
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        c.execute(f"SELECT * from {table}")
        content = c.fetchone()
        conn.close()
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

def main_gui():
    """ HOME Page """
    global root
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
    reddit_button = Button(canvas, image=reddit, height=80, width=80, border=0, bg=background, command=reddit_login)
    canvas.create_window(300, 260, window=reddit_button)
    
    root.eval('tk::PlaceWindow . center')
    root.mainloop()
    
if __name__ == "__main__":
    try:
        import praw
        main_gui()
    except ImportError:
        opt = askokcancel("Install Library", "This Application requires python 'praw' library\nDo you want to install it?")
        if opt:
            result = subprocess.run(["python", "-m", "pip", "install", "praw"], capture_output=True)
            if result:
                showinfo("Install Library", "(!) Successfully Installed (!)")
                main_gui()
            else:
                showerror("Error", "Error!")
        