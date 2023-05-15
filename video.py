import os
import subprocess
from random import randint
from tkinter import *
from tkinter import messagebox, filedialog
import cv2 as cv
import moviepy.editor as mpe
from gtts import gTTS

def generate_audio(title, text):
    """ Generates Audio from text using TTS engine"""
    print(title, text)
    speech = gTTS(title+text)
    speech.save(os.path.join("clips", f"{title.replace(' ','_')}.mp3"))
    print("Audio Generated!")
    return os.path.join("clips", f"{title.replace(' ','_')}.mp3")
    
    
""" Creates a video from audio and text"""
def create_video(audio, text=None):
    # Set up the video file name and path
    video_file = os.path.join(os.path.splitext(audio)[0] + ".mp4")

    # Get audio duration
    audio_duration = float(subprocess.check_output(['ffprobe', '-i', audio, '-show_entries', 'format=duration', '-v', 'quiet', '-of', 'csv=%s' % ("p=0")]).strip())

    # Create the video using FFmpeg with text overlay
    if text:
        subprocess.call([
            "ffmpeg",
            "-y",
            "-f", "lavfi",
            "-i", f"color=c=white:s=1920x1080:d={audio_duration + 1}",
            "-vf", f"drawtext=fontfile=/path/to/font.ttf:fontsize=30:text='{text}':x=(w-text_w)/2:y=(h-text_h)/2",
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-t", str(audio_duration + 1),
            video_file
        ])
    # Create the video using FFmpeg without text overlay
    else:
        subprocess.call([
            "ffmpeg",
            "-y",
            "-f", "lavfi",
            "-i", f"color=c=white:s=640x480:d={audio_duration + 1}",
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-t", str(audio_duration + 1),
            video_file
        ])

    # Add audio to the video using FFmpeg
    subprocess.call([
        "ffmpeg",
        "-y",
        "-i", video_file,
        "-i", audio,
        "-c:v", "copy",
        "-c:a", "aac",
        "-shortest",
        os.path.join(os.path.splitext(audio)[0] + "_video.mp4")
    ])
    
    os.remove(video_file)
    # Check if video was created and return True or False
    if os.path.exists(os.path.join(os.path.splitext(audio)[0] + "_video.mp4")):
        messagebox.showinfo("Video Created!", "Video has been successfully created!")
        return True
    else:
        return False
    
def clip_duration(path):
    from moviepy.video.io.VideoFileClip import VideoFileClip
    clip = VideoFileClip(path)
    return int(clip.duration)

def browsing(duration_label, address, buttons):
    """ Dialog to choose a video File """
    file_path = filedialog.askopenfilename(initialdir="/", filetypes =[('MP4', '*.mp4'), ('MOV', '*.mov'), ('AVI', '*.avi'), ('MKV', "*.mkv"), ("All Files", "*.*")], title="Choose Video")
    if os.path.exists(file_path):
        cap = cv.VideoCapture(file_path)
        if not cap.isOpened():
            address.set("ERROR!!")
            duration = "Error"
            duration_label.config(text=f"Duration: {duration}")
            for button in buttons:
                button.config(state=DISABLED)
            messagebox.showerror("Error!", "Error opening video file!")
        else:
            ret, frame = cap.read()
            if not ret:
                messagebox.showerror("Error!", "Error reading first frame of video file!")
            else:
                # If the video file is not corrupt
                address.set(file_path)
                duration = time_(clip_duration(file_path), "formatted")
                duration_label.config(text=f"Duration: {duration}")
                for button in buttons:
                    button.config(state=NORMAL)
            cap.release()
                
def choose_out_path(address, button):
    out_path = filedialog.askdirectory(initialdir="/", title="Output Folder")
    if os.path.isdir(out_path):
        address.set(out_path)
        button.config(state=NORMAL)
                
def trim_video(vid_path, out_path, start_time, end_time, self_button):
    if out_path not in ("", " "):
        if os.path.exists(vid_path):
            from moviepy.video.io.VideoFileClip import VideoFileClip
            self_button.config(state=DISABLED)
            video_clip = VideoFileClip(vid_path)
            video_extn = str(vid_path[-4:])
            
            trimmed_clip = video_clip.subclip(int(start_time), int(end_time))
            trimmed_vid = out_path+"/trimmed-"+str(randint(1000000,99999999))+video_extn
            while True:
                if os.path.exists(trimmed_vid):
                    trimmed_vid = out_path+"/trimmed-"+str(randint(1000000,99999999))+video_extn
                else:
                    break
            
            print("Wait.... the video is being trimmed! (may take time dependant on the clip)")
            trimmed_clip.write_videofile(trimmed_vid, logger=None)
            messagebox.showinfo("Successfully Trimmed!", "Video Clip has been successfully trimmed!")
            trim_m.destroy()
            
        else:
            messagebox.showerror("Error!", "The Video doesn't Exist!")
                
def time_(time, type="unformatted"):
    duration = [0, 0, time]
    duration[0]+=(duration[2]//3600)
    duration[1]=(duration[2]-duration[0]*3600)//60
    duration[2]=(duration[2]-duration[1]*60)%60
    if type == "unformatted":
        return f"{duration[0]}:{duration[1]}:{duration[2]}"
    elif type == "formatted":
        return f"{duration[0]} Hours {duration[1]} Mins {duration[2]} Secs"
    else:
        return None

def trim_menu(path):
    global trim_m
    trim_m = Toplevel()
    trim_m.title("Trim Video")
    trim_m.grab_set()
    trim_m.resizable(False, False)
    
    canvas = Canvas(trim_m, bg="white", height=300, width=300)
    canvas.pack()
    
    start_time = "None"
    start_label = Label(canvas, text=f"Start: {start_time}", bg="white", fg="black", font=("", 12))
    canvas.create_window(80, 20, window=start_label)
    start_point = StringVar()
    start_scale = Scale(canvas, from_=0, to=clip_duration(path)-1, orient=HORIZONTAL, bg="white", fg="black", length=120, variable=start_point)
    canvas.create_window(80, 60, window=start_scale)
    start_box = Spinbox(canvas, textvariable=start_point, bg="white", fg="black", from_=0, to=clip_duration(path)-1)
    canvas.create_window(80, 100, window=start_box)
    
    end_time = "None"
    end_label = Label(canvas, text=f"End: {end_time}", bg="white", fg="black", font=("", 12))
    canvas.create_window(220, 20, window=end_label)
    end_point = StringVar()
    end_scale = Scale(canvas, from_=0, to=clip_duration(path), orient=HORIZONTAL, bg="white", fg="black", length=120, variable=end_point)
    canvas.create_window(220, 60, window=end_scale)
    end_box = Spinbox(canvas, textvariable=end_point, bg="white", fg="black", from_=0, to=clip_duration(path))
    canvas.create_window(220, 100, window=end_box)
    
    trim = Button(canvas, text="TRIM", font=('', 10), command=lambda: trim_video(path, output_path.get(), start_point.get(), end_point.get(), trim), bg="black", fg="white", state=DISABLED)
    canvas.create_window(150, 220, window=trim)
    
    address = StringVar()
    output_path = Entry(canvas, font=('', 12), textvariable=address, state=DISABLED, bg="black")
    canvas.create_window(100, 180, window=output_path)
    browse = Button(canvas, text="Choose Path", font=('', 8), command=lambda: choose_out_path(address, trim), bg="black", fg="white")
    canvas.create_window(240, 180, window=browse)
    
    time = StringVar()
    video_duration = Label(canvas, text=f"Duration: {time}", bg="white", fg="black", font=("", 8))
    canvas.create_window(150, 140, window=video_duration)
    
    try:
        while True:
            start_label.config(text=f"Start: {time_(start_scale.get())}")
            end_label.config(text=f"End: {time_(end_scale.get())}")
            time.set(time_(end_scale.get()-start_scale.get()))
            video_duration.config(text=f"Duration: {time.get()}")
            end_scale.configure(from_=start_scale.get()+1)
            end_box.configure(from_=int(start_box.get())+1)
            trim_m.update()
            
    except ValueError: # Temp Fix
        messagebox.showerror("Error!", "Value can't be left empty or be ZERO!")
        trim_m.destroy()
    
    except:
        trim_m.destroy()

def video_section(top=False):
    """ GUI for the Video Section """
    if top:
        root = Toplevel()
        root.grab_set()
    else:
        root = Tk()
    root.title("Clip Manager")
    root.resizable(False, False)
    
    bg_canvas = Canvas(root, height=600, width=600, bg="white")
    bg_canvas.pack()
    
    title = Label(bg_canvas, text="Clip Manager", font=('Minion Pro', 20, "bold"), bg="white")
    bg_canvas.create_window(300, 30, window=title)

    address = StringVar()
    address_bar = Entry(bg_canvas, font=('', 14), textvariable=address, state=DISABLED, bg="black")
    bg_canvas.create_window(240, 100, window=address_bar)
    
    browse = Button(bg_canvas, text="Choose Video", font=('', 10), command=lambda: browsing(duration_label, address, [trim_video]), bg="black", fg="white")
    bg_canvas.create_window(430, 100, window=browse)

    duration = "None"
    duration_label = Label(bg_canvas, text=f"Duration: {duration}", font=('Minion Pro', 12), bg="white")
    bg_canvas.create_window(240, 140, window=duration_label)
    
    trim_video = Button(bg_canvas, text="Trim\n Video", bg="black", font=('', 10), fg="white", padx=20, command=lambda: trim_menu(address_bar.get()), state=DISABLED)
    bg_canvas.create_window(200, 200, window=trim_video)

    if not top:
        root.eval('tk::PlaceWindow . center')
    root.mainloop()
    
if __name__ == "__main__":
    video_section()
