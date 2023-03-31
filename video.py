import os
import subprocess
from tkinter import *
from tkinter import messagebox, filedialog

def create_video():
    print()

def browsing():
    file_path = filedialog.askopenfilename(initialdir="/", filetypes =[('MP4', '*.mp4'), ('MOV', '*.mov'), ('AVI', '*.avi'), ('MKV', "*.mkv"), ("All", "*.*")])
    if os.path.exists(file_path):
        cap = cv.VideoCapture(file_path)
        if not cap.isOpened():
            address.set("ERROR!!")
            messagebox.showerror("Error!", "Error opening video file!")
        else:
            ret, frame = cap.read()
            if not ret:
                cap.release()
                messagebox.showerror("Error!", "Error reading first frame of video file!")
            else:
                # If the video file is not corrupt
                from moviepy.video.io.VideoFileClip import VideoFileClip
                address.set(file_path)
                clip = VideoFileClip(file_path)
                duration = [0, 0, 0]
                duration[2] = int(clip.duration)
                while duration[2] > 59:
                    if duration[2] > 59:
                        duration[1]+=1
                        duration[2]-=60
                while duration[1] > 59:
                    if duration[1] > 59:
                        duration[0]+=1
                        duration[1]-=60
                duration = f"{duration[0]} hours {duration[1]} mins {duration[2]} secs"
                duration_label.config(text=f"Duration: {duration}")
                cap.release()

def new_background_add():
    global address, duration_label
    """ This function ensures that if user add new video
        it should have shorts required resolution and
        duration. """
    root = Tk()
    root.title("New Clip")
    root.resizable(False, False)
    
    bg_canvas = Canvas(root, height=600, width=600, bg="white")
    bg_canvas.pack()
    
    title = Label(bg_canvas, text="Clip Manager", font=('Minion Pro', 20, "bold"), bg="white")
    bg_canvas.create_window(300, 30, window=title)

    address = StringVar()
    address_bar = Entry(bg_canvas, font=('', 14), textvariable=address, state=DISABLED, bg="black")
    bg_canvas.create_window(240, 100, window=address_bar)
    
    browse = Button(bg_canvas, text="Choose Video", font=('', 10), command=browsing, bg="black", fg="white")
    bg_canvas.create_window(430, 100, window=browse)

    duration_label = Label(bg_canvas, text="Duration: ", font=('Minion Pro', 12), bg="white")
    bg_canvas.create_window(240, 140, window=duration_label)

    root.eval('tk::PlaceWindow . center')
    root.mainloop()
    
if __name__ == "__main__":
    try:
        import cv2 as cv
        import moviepy.editor as mpe
    except ModuleNotFoundError:
        ask = messagebox.askokcancel("Require Multiple Modules!", "This script requires OpenCV and MoviePY modules\nDo you wish to install them?\n(May take some time)")
        if ask:
            chk = subprocess.run(["pip", "install", "opencv-python"], capture_output=True)
            chk2 = subprocess.run(["pip", "install", "moviepy"], capture_output=True)
            if chk and chk2:
                messagebox.showinfo("Download Successfull", "Modules downloaded successfully!")
                import cv2 as cv
                import moviepy.editor as mpe
            else:
                messagebox.showerror("Error!!", "Error Occured!\nReport on issues section\nhttps://github.com/AroraKaran19/gpt-to-shorts/issues")

    new_background_add()