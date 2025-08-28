import json, queue
from vosk import Model, KaldiRecognizer
import sounddevice as sd
from .config import SAMPLE_RATE

class VoskSTT:
    def __init__(self, model_dir, sample_rate=SAMPLE_RATE):
        self.model = Model(str(model_dir))
        self.recognizer = KaldiRecognizer(self.model, sample_rate)
        self.recognizer.SetWords(True)
        self.sample_rate = sample_rate
        self._q = queue.Queue()

    def _audio_callback(self, indata, frames, time_info, status):
        if status:
            print(f"[Audio] {status}", flush=True)
        self._q.put(bytes(indata))

    def transcribe_block(self, seconds=4):
        duration_frames = int(seconds * self.sample_rate)
        collected = 0
        text = ""
        while collected < duration_frames:
            data = self._q.get()
            collected += len(data) // 2
            if self.recognizer.AcceptWaveform(data):
                res = json.loads(self.recognizer.Result())
                text += " " + (res.get("text") or "")
        res_final = json.loads(self.recognizer.FinalResult())
        text += " " + (res_final.get("text") or "")
        return text.strip()

    def stream(self):
        return sd.RawInputStream(
            samplerate=self.sample_rate,
            blocksize=8000,
            dtype='int16',
            channels=1,
            callback=self._audio_callback
        )
