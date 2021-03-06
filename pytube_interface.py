#!/usr/bin/env python

import os
import pytube
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

#file_path = filedialog.askopenfilename()
folder = filedialog.askdirectory()
DOWNLOAD_DIR = folder.replace("/", "\\")
print("Download Directory " + DOWNLOAD_DIR)


def check_playlist(aLink, aItag):
    link = pytube.Playlist(aLink)
    try:
        if len(link.video_urls) > 0:
            pass
    except:
        link = pytube.YouTube(aLink)
        download(link, aItag)
    else:
        for myStream in link.videos:
            download(myStream, aItag)


def download(aStream, aItag):
    try:
        stream = aStream.streams.get_by_itag(aItag)
        mp4_file = stream.default_filename
    except:
        vid = False
        if aItag == 22:
            vid = True
        stream = aStream.streams.filter(progressive=vid)
        print("Default itag is unavailable. ")
        print("Choose an available itag. ")
        for each in stream:
            print(each)
        Itag = input("Enter itag: ")
        stream = aStream.streams.get_by_itag(Itag)
        mp4_file = stream.default_filename
    stream.download(output_path=DOWNLOAD_DIR, filename=mp4_file)
    if aItag == 140:  # convert audio only stream to mp3
        mp4_to_mp3(mp4_file)


def mp4_to_mp3(aMp4):
    mp3_file = "\"" + DOWNLOAD_DIR + "\\" + \
        os.path.splitext(aMp4)[0] + ".mp3" + "\""
    mp4_file = "\"" + DOWNLOAD_DIR + "\\" + aMp4 + "\""
    cmd = "ffmpeg -loglevel quiet -i " + mp4_file + " -vn " + mp3_file
    os.system(cmd)
    os.remove(os.path.join(DOWNLOAD_DIR, aMp4))


def main():

    link = input("Enter YoutTube link: ")
    choose = input("Video(v) or Audio(a) only:")

    if choose == "a":
        itag = 140  # mp4 audio only. modify the value to download a different stream
    else:
        itag = 22  # mp4 video with audio. modify the value to download a different stream

    check_playlist(link, itag)


if __name__ == "__main__":
    main()

# <Stream: itag="140" mime_type="audio/mp4" abr="128kbps" acodec="mp4a.40.2" progressive="False" type="audio">  Audio Only
# <Stream: itag="137" mime_type="video/mp4" res="1080p" fps="24fps" vcodec="avc1.640028" progressive="False" type="video">  Video Only
# <Stream: itag="22" mime_type="video/mp4" res="720p" fps="24fps" vcodec="avc1.64001F" acodec="mp4a.40.2" progressive="True" type="video">  Video + Audio
