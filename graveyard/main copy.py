import requests as r
from escape import escape

URLNDK = "https://www.ndk.cz/"

def main(root_pid):
    session = r.Session()
    response = session.get(URLNDK + "search/api/v5.0/search?q=root_pid:" + escape(root_pid)+" AND document_type:page&fl=PID&rows=9999999&wt=json", stream=True)
    text = ""
    for PIDobject in response.json().get("response").get("docs"):
        PID = PIDobject.get("PID")
        print(PID)
        page = session.get(f"https://ndk.cz/search/api/v5.0/item/{PID}/streams/TEXT_OCR")
        text = text + page.text

    with open ("output.txt", "w") as file:
        file.write(text)


if __name__ == '__main__':
    main("uuid:a837aec0-8c99-11de-9ad9-000d606f5dc6")
