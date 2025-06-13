import whisper

model = whisper.load_model("base")  # or "small", "medium", "large" for better accuracy

result = model.transcribe("a2.mp3", language="ja")  # "ja" = Japanese

print(result["text"])
with open("transcription2.txt", "w", encoding="utf-8") as f:
    f.write(result["text"])