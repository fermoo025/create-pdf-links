from moviepy import VideoFileClip

video = VideoFileClip("v.mp4")
video.audio.write_audiofile("audio.wav")
