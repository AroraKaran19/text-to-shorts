import pytube

# Define the YouTube video URL
url = 'https://www.youtube.com/watch?v=Ps-0f0K6izM&t=3471s&ab_channel=Chill%26RelaxwithVisualEffects'

# Create a YouTube object and get the video stream
youtube = pytube.YouTube(url)
video_stream = youtube.streams.filter(res="1080p").first()

# Define the output file path
output_path = '/home/karan/Downloads/video.mp4'

# Download the video
video_stream.download(output_path)

print("Video downloaded successfully!")
