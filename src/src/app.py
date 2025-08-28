import sys
from datetime import datetime
from src.config import VOSK_MODEL_DIR, BLOCK_SECONDS
from src.sttVosk import VoskSTT
from src.translatorArgos import de_to_ro
from src.storage import Storage

BANNER = r"""
========================================
   DE→RO Voice Logger (offline, Vosk)
   Press Ctrl+C to stop recording
========================================
"""

def main():
    if not VOSK_MODEL_DIR.exists():
        print(f"[E] Vosk model not found at: {VOSK_MODEL_DIR}")
        print("    Download and extract 'vosk-model-small-de' into this folder.")
        sys.exit(1)

    store = Storage()
    stt = VoskSTT(VOSK_MODEL_DIR)

    print(BANNER)
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Starting microphone... Speak in GERMAN.")

    import sounddevice as sd
    try:
        with stt.stream():
            while True:
                de_text = stt.transcribe_block(seconds=BLOCK_SECONDS)
                if de_text:
                    ro_text = de_to_ro(de_text)
                    ts = store.save_phrase(german=de_text, romanian=ro_text)
                    print(f"\n[{ts}]")
                    print(f"  [DE] {de_text}")
                    print(f"  [RO] {ro_text}")
                else:
                    print(".", end="", flush=True)
    except KeyboardInterrupt:
        print("\nStopped by user. Bye!")
    except sd.PortAudioError as e:
        print("\n[E] Audio/PortAudio error:", e)
        print("   - Check microphone permissions.")
        print("   - Close other applications using the microphone.")
    except Exception as e:
        print("\n[E] Unexpected error:", e)

if __name__ == "__main__":
    main()
