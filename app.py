import whisper
import sys

def format_time(seconds):
    hours = int(seconds // 3600)
    seconds = seconds % 3600
    minutes = int(seconds // 60)
    seconds = seconds % 60
    milliseconds = int((seconds % 1) * 1000)
    seconds = int(seconds)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

def mp3_to_srt(input_audio_path, output_srt_path, language="hi"):
    print(f"Loading Whisper model...")
    model = whisper.load_model("small")

    print(f"Transcribing audio in language: {language}")
    result = model.transcribe(
        input_audio_path,
        verbose=True,
        word_timestamps=True,
        language=language
    )

    with open(output_srt_path, 'w', encoding='utf-8') as f:
        subtitle_index = 1
        for segment in result['segments']:
            start = format_time(segment['start'])
            end = format_time(segment['end'])
            text = segment['text'].strip()

            if text:
                f.write(f"{subtitle_index}\n")
                f.write(f"{start} --> {end}\n")
                f.write(f"{text}\n\n")
                subtitle_index += 1

    print(f"SRT file saved as: {output_srt_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python mp3_to_srt.py <input_audio.mp3> [output_srt.srt] [language_code]")
        print("Example:")
        print("  python mp3_to_srt.py input.mp3 output.srt hi")
        sys.exit(1)

    input_mp3 = sys.argv[1]
    output_srt = sys.argv[2] if len(sys.argv) > 2 else input_mp3.replace('.mp3', '.srt')
    language_code = sys.argv[3] if len(sys.argv) > 3 else "hi"  # Default to Hindi

    mp3_to_srt(input_mp3, output_srt, language_code)
