import subprocess, sys, os, json

from datetime import datetime, timedelta

from vosk import Model, KaldiRecognizer

SAMPLE_RATE = 16000
CHUNK_SIZE = 4000

# SAMPLE_RATE = 16000
# SetLogLevel(0)
# model = Model(lang="en")
# rec = KaldiRecognizer(model, SAMPLE_RATE)

class Transcriber():
    # def __init__(self):
    #     self.model = Model(lang="en")

    def fmt(self, data):
        data = json.loads(data)

        start = min(r["start"] for r in data.get("result", [{ "start": 0 }]))
        end = max(r["end"] for r in data.get("result", [{ "end": 0 }]))

        return {
            "start": str(timedelta(seconds=start)), 
            "end": str(timedelta(seconds=end)), 
            "text": data["text"]
        }

    def transcribe(self, filename, language_code):
        model = Model(lang=language_code)
        rec = KaldiRecognizer(model, SAMPLE_RATE)
        rec.SetWords(True)

        # filename = "C:\\Users\\Qasym\\Desktop\\Alexandra\\Alexandra_web_appp\\app_home\\somename_5CVCG8J.wav"

        if not os.path.exists(filename):
            raise FileNotFoundError(filename)

        transcription = []
        
        ffmpeg_command = [
                "ffmpeg",
                "-nostdin",
                "-loglevel",
                "quiet",
                "-i",
                filename,
                "-ar",
                str(SAMPLE_RATE),
                "-ac",
                "1",
                "-f",
                "s16le",
                "-",
            ]

        with subprocess.Popen(ffmpeg_command, stdout=subprocess.PIPE) as process:

            start_time = datetime.now() 
            while True:
                data = process.stdout.read(4000)
                if len(data) == 0:
                    break
                
                if rec.AcceptWaveform(data):
                    transcription.append(self.fmt(rec.Result()))

            transcription.append(self.fmt(rec.FinalResult()))
            end_time = datetime.now()

            time_elapsed = end_time - start_time
            print(f"Time elapsed  {time_elapsed}")

        return {
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "elapsed_time": time_elapsed,
            "transcription": transcription,
        }