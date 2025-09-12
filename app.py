from fastapi import FastAPI, File, UploadFile, Form
import whisper
import tempfile

app = FastAPI()
model = whisper.load_model("tiny")  # smaller model for free CPU

def format_time(seconds):
    hours = int(seconds // 3600)
    seconds = seconds % 3600
    minutes = int(seconds // 60)
    seconds = seconds % 60
    milliseconds = int((seconds % 1) * 1000)
    seconds = int(seconds)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

def mp3_to_srt_file(file_path, language="hi"):
    result = model.transcribe(file_path, language=language, word_timestamps=True)
    srt_content = ""
    idx = 1
    for segment in result["segments"]:
        start = format_time(segment["start"])
        end = format_time(segment["end"])
        text = segment["text"].strip()
        if text:
            srt_content += f"{idx}\n{start} --> {end}\n{text}\n\n"
            idx += 1
    return srt_content

@app.post("/convert")
async def convert_mp3(file: UploadFile = File(...), language: str = Form("hi")):
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(suffix=".mp3") as tmp:
        tmp.write(await file.read())
        tmp.flush()
        srt_text = mp3_to_srt_file(tmp.name, language)
    return {"srt": srt_text}
