from moviepy.video.io.VideoFileClip import VideoFileClip

# Define the input and output file paths
input_path = '/home/karan/Downloads/trimmed_video.mp4'
output_path = '/home/karan/Downloads/trimmed_video1.mp4'

# Define the start and end times for the trim
start_time = 0  # in seconds
end_time = 10  # in seconds

# Load the input video
video_clip = VideoFileClip(input_path)

# Trim the video
trimmed_clip = video_clip.subclip(start_time, end_time)

# Save the trimmed video
trimmed_clip.write_videofile(output_path)
