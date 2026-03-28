#!/usr/bin/env python3
import sys
import requests as r
import time
from dotenv import load_dotenv
import os
import re
import ToPDF

cookie_value = os.getenv("cookieValue")
cookie_name =os.getenv("cookieName")
JSessionIDValue = os.getenv("JSESSIONVALUE")
GA1Name = os.getenv("GA1Name")
GA1Value = os.getenv("GA1Value")
GA = os.getenv("GA")
GA2Name = os.getenv("GA2Name")
GA2Value = os.getenv("GA2Value")
_gat = os.getenv("_gat")
_gid = os.getenv("_gid")

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

        session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Origin": "https://kramerius.mzk.cz",
    "Referer": "https://kramerius.mzk.cz/",
    "Connection": "keep-alive",

})
        session.cookies.set(name=cookie_name, value=cookie_value, domain="ndk.cz")
        session.cookies.set(name=GA1Name, value=GA1Value)
        session.cookies.set(name="_ga", value=GA)
        session.cookies.set(name=GA2Name, value=GA2Value)
        session.cookies.set("JSESSIONID",JSessionIDValue, domain="ndk.cz")
        session.cookies.set("_gat",_gat, domain="ndk.cz")
        session.cookies.set("_gid",_gid, domain="ndk.cz")
        session.headers.update({"Authorization":""})
        return session

def get_uuid(link):
    root = link.split("/")[4].split("?")[0]
    if root == "view":
        root = link.split("/")[5].split("?")[0]
    return root

def get_root_url(link):
    return link.split("/")[2]

def extract_page_number_mzv(detail):
    if not detail:
        return (float('inf'), '')  # use tuple for sorting

    # if it's a list, take the first element
    if isinstance(detail, list):
        detail = detail[0]

    # remove surrounding brackets if any
    detail = detail.strip('[]')

    # split into number and optional letters
    match = re.match(r'(\d+)([a-zA-Z]*)', detail)
    if match:
        number_part = int(match.group(1))
        letter_part = match.group(2)
        # lettered entries should come before pure numbers
        # we can invert logic by using empty string as larger than letters
        return (number_part, letter_part)
    else:
        return (float('inf'), '')

def extract_page_number(detail):
    if not detail:
        return (float('inf'), 1, '')  # empty goes last

    if isinstance(detail, list):
        detail = detail[0]

    detail = detail.strip('[]').replace(" ", "")

    first_part = re.split(r'[,;-]', detail)[0]

    match = re.match(r'(\d+)([a-zA-Z]*)', first_part)
    if match:
        number_part = int(match.group(1))
        letter_part = match.group(2)

        # 0 = has letter (comes first), 1 = no letter (comes later)
        no_letter_flag = 0 if letter_part else 1

        return (number_part, no_letter_flag, letter_part)
    else:
        return (float('inf'), 1, '')

def get_PIDS(session, URL, root_pid):
    try:
        """
        if URL == "kramerius.lib.cas.cz":
                print("Not Supported! - The API is forbidden")
                return []
        if URL == "https://kramerius.rozhlas.cz":
                return []
                response = session.get("https://kramerius.rozhlas.cz/search/api/v7.0/search?q=root_pid:" + escape(root_pid)+" AND document_type:page&fl=PID,details&rows=9999999&wt=json", stream=True)
                docs = response.json().get("response").get("docs")
                docs.sort(key=lambda doc: extract_page_number(doc.get("details")))
                return docs
        """
        
        
        if URL == "www.digitalniknihovna.cz":
                ""
                response = session.get("https://api.kramerius.mzk.cz/search/api/client/v7.0/search?q=root.pid:" + escape(root_pid)+" AND model:page&fl=pid,details&rows=9999999&wt=json", stream=True)
                docs = response.json().get("response").get("docs")
                if docs == []:
                        response = session.get("https://api.kramerius.mzk.cz/search/api/client/v7.0/search?q=parent.pid:" + escape(root_pid)+" AND model:page&fl=pid,details&rows=9999999&wt=json", stream=True)
                        docs = response.json().get("response").get("docs")    
                docs.sort(key=lambda doc: extract_page_number_mzv(doc.get("details")))
                print(docs)
                return docs
        
        response = session.get("https://" + URL + "/search/api/v5.0/search?q=root_pid:" + escape(root_pid)+" AND document_type:page&fl=PID,details&rows=999999999&wt=json", stream=True)
        docs = response.json().get("response").get("docs")
        if docs == []:
                response = session.get("https://" + URL + "/search/api/v5.0/search?q=parent_pid:" + escape(root_pid)+" AND document_type:page&fl=PID,details&rows=999999999&wt=json", stream=True)
                docs = response.json().get("response").get("docs")
        docs.sort(key=lambda doc: extract_page_number(doc.get("details")))
        return docs

    except Exception as e:
        print(f"Error in getting PIDs - {e}")

def get_pages(session, PIDobjects,URL, folder="./temp"):
        try:
                print("Downloading totally: " + str(len(PIDobjects)) + " pages")
                i = 1

                for PIDobject in PIDobjects:
                     PID = PIDobject.get("pid")
                     print(i)
                     time.sleep(1)
                     if URL == "www.digitalniknihovna.cz":
                        url = f"https://api.kramerius.mzk.cz/search/iiif/{PID}/full/max/0/default.jpg"
                     if URL == "ndk.cz":
                        url = f"https://kramerius5.nkp.cz/pdf/download/?id={PID}"

                     with session.get(url, stream=True, timeout=(40,200)) as r:
                        r.raise_for_status()
                        with open(f"{folder}/{i}.jpeg", "wb") as f:
                                for chunk in r.iter_content(chunk_size=8192):
                                        if chunk:
                                                f.write(chunk)
                     i = i + 1
        
        except Exception as e:
                print(f"Error in downloading OCR pages on {PID} - {e}")

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
            text = get_pages(session, PIDobjects[start_index:len(PIDobjects)],URL)
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
    print(root_pid)
    if PIDobjects == []:
            print("The API couln't get the PIDs")
    get_pages(session, PIDobjects, URL)
    print("Images downloaded, now joining into pdf")
    ToPDF.save()
    print(f"The Images for {root_pid} is saved in pdf")
        

if __name__ == "__main__":
    main()