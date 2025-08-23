#!/usr/bin/env python3
import sys
import requests as r
import time
from dotenv import load_dotenv
import os
import re

cookie_value = os.getenv("cookieValue")
cookie_name =os.getenv("cookieName")

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
    --c continuation on given uuid, saves to "output_continueation.txt"
""")
def set_cookies(session):
        
        session.cookies.set(cookie_name, cookie_value)

        return session

def get_uuid(link):
    root = link.split("/")[4].split("?")[0]
    if root == "view":
        root = link.split("/")[5].split("?")[0]
    return root

def get_root_url(link):
    return link.split("/")[2]

def extract_page_number(detail):
    if not detail:
        return float('inf')

    if isinstance(detail, list):
        detail = detail[0]

    match = re.search(r'\[?(\d+)\]?', detail)
    if match:
        return int(match.group(1))
    else:
        return float('inf')        

def get_PIDS(session, URL, root_pid):
    try:
        if URL == "kramerius.lib.cas.cz":
                print("Not Supported! - The API is forbidden")
                return []
        if URL == "www.digitalniknihovna.cz":
                response = session.get("https://kramerius.mzk.cz/search/api/v5.0/search?q=root_pid:" + escape(root_pid)+" AND document_type:page&fl=PID,details&rows=9999999&wt=json", stream=True)
                docs = response.json().get("response").get("docs")
                docs.sort(key=lambda doc: extract_page_number(doc.get("details")))
                return docs
        response = session.get("https://" + URL + "/search/api/v5.0/search?q=root_pid:" + escape(root_pid)+" AND document_type:page&fl=PID,details&rows=999999999&wt=json", stream=True)
        docs = response.json().get("response").get("docs")
        docs.sort(key=lambda doc: extract_page_number(doc.get("details")))
        return docs
    except Exception as e:
        print(f"Error in getting PIDs - {e}")

def get_text(session, PIDobjects,URL):
    try:
        print("Downloading totally: " + str(len(PIDobjects)) + " pages")
        i = 1
        all_texts = []
        for PIDobject in PIDobjects:
            PID = PIDobject.get("PID")
            print(i)
            time.sleep(1)
            if URL == "ndk.cz":
                page = session.get(f"https://ndk.cz/search/api/v5.0/item/{PID}/streams/TEXT_OCR", timeout=(40,200))
                all_texts.append(page.text)
            if URL == "kramerius.lib.cas.cz":
                page = session.get(f"https://kramerius.lib.cas.cz/search/api/v5.0/item/{PID}/ocr/text", timeout=(40,200))
                all_texts.append(page.text)
            if URL == "www.digitalniknihovna.cz":
                page = session.get(f"https://api.kramerius.mzk.cz/search/api/client/v7.0/items/{PID}/ocr/text", timeout=(40,200))
                all_texts.append(page.text)
            i= i + 1
        return "\n".join(all_texts)
    except Exception as e:
        print(f"Error in downloading OCR pages on {PID} - {e}")
        return text

def continue_download(uuid, link, output_file):
    try:
            root_pid = get_uuid(link)
            URL = get_root_url(link)
            print("Continuing the download, don't turn off the process")
            session = r.Session()
            session = set_cookies(session)
            PIDobjects = get_PIDS(session, URL, root_pid)
            if PIDobjects == []:
                    print("The API couln't get the PIDs")
            start_index = next(i for i, obj in enumerate(PIDobjects) if obj["PID"] == uuid)
            text = get_text(session, PIDobjects[start_index:len(PIDobjects)],URL)
            with open(output_file, "w") as file:
                file.write(text)

            print(f"The OCR for {root_pid} is saved in {output_file}")
    except Exception as e:
        print(f"Error in continuation - {e}")

      


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
        link = sys.argv[1]

    if "--c" in sys.argv:
        output_file = "output_continueation.txt"
        c_index = sys.argv.index("--c")
        if c_index + 1 < len(sys.argv):
            uuid = sys.argv[c_index + 1]
            continue_download(uuid, link, output_file)
            sys.exit(1)
    root_pid = get_uuid(link)
    URL = get_root_url(link)
    print("Your download has started, don't turn off the process")
    session = r.Session()
    session = set_cookies(session)
    PIDobjects = get_PIDS(session, URL, root_pid)
    if PIDobjects == []:
            print("The API couln't get the PIDs")
    text = get_text(session, PIDobjects,URL)
    with open(output_file, "w") as file:
        file.write(text)

    print(f"The OCR for {root_pid} is saved in {output_file}")
        

if __name__ == "__main__":
    main()
