# DE→RO Voice Logger

An offline speech-to-text and translation tool built in Python.  
It listens to German speech, transcribes it with [Vosk](https://alphacephei.com/vosk/), translates into Romanian using [Argos Translate](https://github.com/argosopentech/argos-translate), and saves both the German and Romanian text into **SQLite** and **Excel** for later review.

---

## Features
-  **Offline German speech recognition** (Vosk small German model)  
-  **German → Romanian translation** via Argos Translate (DE→EN→RO pivot)  
-  **Storage** of phrases in:
  - SQLite database (`data/fraze_de_ro.sqlite`)
  - Excel file (`data/fraze_de_ro.xlsx`)
-  Real-time console output:

[DE] guten tag
[RO] bună ziua


---

## Motivation
Honestly, I built this because I am too lazy when reading books in German .  
Instead of looking up words in a dictionary and then writing them down,  
I created this app to recognize, translate, and save them automatically.  

---

## Requirements
- Python 3.10+  
- [Vosk model for German](https://alphacephei.com/vosk/models) (small recommended: `vosk-model-small-de-0.15`)  
- And some other Libraries... sry... too lazy to write them all :')
