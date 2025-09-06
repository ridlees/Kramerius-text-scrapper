#!/usr/bin/env python3
import sys
from gtts import gTTS

def createTTS(inputfile):
    try:
        with open(inputfile,"r") as file:
            text = file.read()
            print(f"File {inputfile} loaded, started TTS")
            tts = gTTS(text, lang='cs')
            name = inputfile.split(".")[0]
            tts.save(f'{name}.mp3')
            print(f"Created TTS - {name}")
    except Exception as e:
        print(f"Error in creating TTS - {e}")
        
def main():
    if len(sys.argv) < 2:
        show_help()
        sys.exit(1)
    inputfile = sys.argv[1]
    createTTS(inputfile)
    
if __name__ == "__main__":
    main()
