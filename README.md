A Python-based application that scraps Reddit posts and converts them in videos.

## Requirements

- computer running Windows 10 or above
- Python 3.5 or above recommended

- will be installed automatically if not present

    - praw 
    - tkinter
    - gtts
    - moviepy
    - opencv-python
    - ImageMagick

## Usage

1. Run ```main.py```, for example, by executing ```python main.py``` in the terminal.
2. Enter your Reddit client ID, client secret, Reddit community name, and post ID. Post ID is optional.
3. Click on the "Create Video" button to convert it in a video.


## Features

- Converts reddit posts to video with audio using text-to-speech
- Stores the user's Reddit client ID and client secret on the local device for streamlined access and usage
- GUI built using Tkinter
- Constantly updated to add new features
- Tested and maintained for on Windows 10, 11 and debian-based Linux distributions

## Footnotes

If the program crashes on Linux and displays ImageMagick related errors, run

```bash
sudo mv /etc/ImageMagick-6/policy.xml /etc/ImageMagick-6/policy.xmlout
```