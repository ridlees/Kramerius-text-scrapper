#!/usr/bin/env python3
"""
Example CLI script template with sys.argv flag parsing.

Usage:
    Kramerius.py --help
    Kramerius.py https://ndk.cz/view/uuid:a837aec0-8c99-11de-9ad9-000d606f5dc6?page=uuid:4841aa90-e1b6-11e7-8cdd-5ef3fc9bb22f --o [specifies the output] 
"""

import sys
import requests as r

def escape(uuid:str) -> str:
	return uuid.replace(':','\:').replace('-','\-')

def show_help():
    print("""
Usage:
    Kramerius.py [OPTIONS] [ARGS]

Options:
    Kramerius.py --help
    Kramerius.py URL


Optional:
    --o [specifies the output file]
""")

def get_uuid(link):
    return link.split("/")[4].split("?")[0]

def get_root_url(link):
    return link.split("/")[2]

def get_PIDS(session, URL, root_pid):
    try:
        response = session.get("https://" + URL + "/search/api/v5.0/search?q=root_pid:" + escape(root_pid)+" AND document_type:page&fl=PID&rows=9999999&wt=json", stream=True)
        return response.json().get("response").get("docs")
    except Exception as e:
        print(f"Error in getting PIDs - {e}")

def get_text(session, PIDobjects,URL):
    try:
        text = ""
        for PIDobject in PIDobjects:
            PID = PIDobject.get("PID")
            if URL == "ndk.cz":
                page = session.get(f"https://ndk.cz/search/api/v5.0/item/{PID}/streams/TEXT_OCR")
                text = text + page.text
            if URL == "kramerius.lib.cas.cz":
                page = session.get(f"https://ndk.cz/search/api/v5.0/item/{PID}/ocr/text")
                text = text + page.text
        return text
    except Exception as e:
        print(f"Error in downloading OCR pages - {e}")



def main():
    if len(sys.argv) < 2:
        show_help()
        sys.exit(1)

    if "--o" in sys.argv:
        o_index = sys.argv.index("--o")

        if o_index >= 2:
            link = sys.argv[1]
        else:
            print("Error: Missing link before --o")
            sys.exit(1)

        if o_index + 1 < len(sys.argv):
            output_file = sys.argv[o_index + 1]
        else:
            output_file = "output.txt"
    else:
        link = sys.argv[1] 

    root_pid = get_uuid(link)
    URL = get_root_url(link)
    print("Your download has started, don't turn off the process")
    session = r.Session()
    PIDobjects = get_PIDS(session, URL, root_pid)
    text = get_text(session, PIDobjects,URL)
    with open(output_file, "w") as file:
        file.write(text)

    print(f"The OCR for {root_pid} is saved in {output_file}")


if __name__ == "__main__":
    main()
