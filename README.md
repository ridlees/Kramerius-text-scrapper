# Kramerius OCR getter

Just get the OCR from a book hosted at the Kramerius site. Experimental, Kramerius doesn't work half of the time :(

## Usage

1. Download the Kramerius.py
2. Make it exacutable with chmod +x Kramerius.py
3. Run ./Kramerius.py "Link to your book"

You can specify the output file with --o flag

IF your download fails (kramerius is tricky) you get uuid returned on which it failed. Then, you can simply run ./Kramerius "link" --c "uuid" and it will continue the download into output_continueation.txt. Then run cat output_continuation.txt>>output.txt to join them.

That's it! Download what you need :)


## Supported Kramerius instances
* -> ndk.cz
* -> Moravská zemská knihovna
## Considered support for:
* -> kramerius.lib.cas.cz


LMK if anything breaks
