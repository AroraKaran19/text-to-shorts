import os
import subprocess
from tkinter import *
import praw
background = "#f0e68c"

def fetch_post(client_id, client_secret, community, postid):
    reddit = praw.Reddit(client_id='O3EQHLb-vTLWh0_Brd0S9Q',
                     client_secret='hIFx2jE2LpnVDGI5xip1D6Edwy-7Mw',
                    user_agent='ytshorts')
    subreddit = reddit.subreddit('AmItheAsshole')
    post = next(iter(subreddit.new()))
    print("\nTitle: ", post.title)
    print("\nContext: ", post.selftext)

def reddit_gui():
    """ GUI for Reddit as Platform """
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
    
    client_id_label = Label(canvas, text="Client ID:", bg=background, font=("Adobe Garamond Pro", 12, "bold"))
    canvas.create_window(210, 230, window=client_id_label)
    client_id = Entry(canvas, width=25, font=('', 14))
    canvas.create_window(400, 230, window=client_id)
    
    client_secret_label = Label(canvas, text="Client Secret:", bg=background, font=("Adobe Garamond Pro", 12, "bold"))
    canvas.create_window(192, 280, window=client_secret_label)
    client_secret = Entry(canvas, width=25, font=('', 14))
    canvas.create_window(400, 280, window=client_secret)
    
    community_label = Label(canvas, text="Community:", bg=background, font=("Adobe Garamond Pro", 12, "bold"))
    canvas.create_window(195, 330, window=community_label)
    subreddit_community = Entry(canvas, width=25, font=('', 14))
    canvas.create_window(400, 330, window=subreddit_community)
    
    post_label = Label(canvas, text="Post ID:", bg=background, font=("Adobe Garamond Pro", 12, "bold"))
    canvas.create_window(210, 380, window=post_label)
    post_id = Entry(canvas, width=25, font=('', 14))
    canvas.create_window(400, 380, window=post_id)
    
    create_button = Button(canvas, text="Create Video", bg="lime", font=("Adobe Garamond Pro", 12, "bold"), pady=8, command=lambda: (fetch_post(client_id.get(), client_secret.get(), subreddit_community.get(), post_id.get())))
    canvas.create_window(350, 450, window=create_button)
    
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