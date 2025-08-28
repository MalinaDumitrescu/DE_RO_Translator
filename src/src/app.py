import sys
from datetime import datetime
from src.config import VOSK_MODEL_DIR, BLOCK_SECONDS
from src.sttVosk import VoskSTT
from src.translatorArgos import de_to_ro
from src.storage import Storage

BANNER = r"""
========================================
   DE→RO Voice Logger (offline, Vosk)
   Ctrl+C pentru a opri înregistrarea
========================================
"""

def main():
    if not VOSK_MODEL_DIR.exists():
        print(f"[E] Modelul Vosk nu există la: {VOSK_MODEL_DIR}")
        print("    Descarcă și dezarhivează 'vosk-model-small-de' în acest folder.")
        sys.exit(1)

    store = Storage()
    stt = VoskSTT(VOSK_MODEL_DIR)

    print(BANNER)
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Pornesc microfonul... Vorbește în GERMANĂ.")

    import sounddevice as sd
    try:
        with stt.stream():
            while True:
                de_text = stt.transcribe_block(seconds=BLOCK_SECONDS)
                if de_text:
                    ro_text = de_to_ro(de_text)
                    ts = store.save_phrase(germana=de_text, romana=ro_text)
                    print(f"\n[{ts}]")
                    print(f"  [DE] {de_text}")
                    print(f"  [RO] {ro_text}")
                else:
                    print(".", end="", flush=True)
    except KeyboardInterrupt:
        print("\nOprit de utilizator. Bye!")
    except sd.PortAudioError as e:
        print("\n[E] Problemă audio/portaudio:", e)
        print("   - Verifică permisiunea microfonului.")
        print("   - Închide alte aplicații care folosesc microfonul.")
    except Exception as e:
        print("\n[E] Eroare neașteptată:", e)

if __name__ == "__main__":
    main()
