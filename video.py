import os
import subprocess
from tkinter import *
from tkinter import messagebox

def create_video():
    try:
        import moviepy.editor as mpe
    except ModuleNotFoundError:
        ask = messagebox.askokcancel("Requires Module!", "This script requires MoviePY module\nDo you wish to install it?\n(May take some time)")
        if ask:
            chk = subprocess.run(["pip", "install", "moviepy"], capture_output=True)
            if chk:
                messagebox.showinfo("Download Successfull", "Module downloaded successfully!")
                import moviepy.editor as mpe
            else:
                messagebox.showerror("Error!!", "Error Occured!\nReport on issues section\nhttps://github.com/AroraKaran19/gpt-to-shorts/issues")
            
def new_background_add():
    """ This function ensures that if user add new video
        it should have shorts required resolution and
        duration. """
    root = Tk()
    root.title("New Clip")
    root.resizable(False, False)
    
    bg_canvas = Canvas(root, height=600, width=600, bg="#FFDB58")
    bg_canvas.pack()
    
    title = Label(bg_canvas, text="Clip Manager", bg="#FFDB58")    
    
    root.eval('tk::PlaceWindow . center')
    root.mainloop()
    
if __name__ == "__main__":
    new_background_add()