# Kramerius OCR getter

Just get the OCR from a book hosted at the Kramerius site. Experimental, Kramerius doesn't work half of the time 😿

## Requirements

1. pip install -r requirements.txt

## Setup

1. Rename .env-example to .env
2. Put in your cookie from Kramerius (works without it, but with it you can download dila nedostupná na trhu).
### Getting a cookie from Kramerius

1. Log into ndk.cz with your account (for example university account)
2. Press right click on the page>Inspect
3. In the inspect window, select Storage
4. Select cookies
5. Copy the _shibsession_ name into cookie name in env.
6. Copy the Value of _shibsession_ into cookie Value in env.
7. Save

_I don't know how long the cookie persist. Needs more testing_

## Usage

1. Download the Kramerius.py
2. Make it exacutable with chmod +x Kramerius.py
3. Run ./Kramerius.py "Link to your book"
![Screenshot of command line](./img1.png)

You can specify the output file with --o flag

IF your download fails (kramerius is tricky) you get uuid returned on which it failed. Then, you can simply run ./Kramerius "link" --c "uuid" and it will continue the download into output_continueation.txt. Then run cat output_continuation.txt>>output.txt to join them.

That's it! Download what you need :)

## Supported Kramerius instances
* -> ndk.cz
* -> Moravská zemská knihovna
## Considered support for:
* -> kramerius.lib.cas.cz

### Experimental

If you have gTTS downloaded (pip install gTTS), you can use the TTS.py to generate "quick" audiobook for your file. 

1. Simply call TTS.py "nameofyourfile.txt" and in a few minutes (takes some time) you will have a listenable file.


LMK if anything breaks
