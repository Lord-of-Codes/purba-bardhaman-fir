import requests
import os
from pathlib import Path
import time
import re

stations = [
    "Aushgram Police Station",
    "Bhatar Police Station",
    "Burdwan Police Station",
    "Cyber Crime Police Station",
    "Dewandighi Police Station",
    "Galsi Police Station",
    "Jamalpur Police Station",
    "Kalna Police Station",
    "Katwa Police Station",
    "Ketugram Police Station"     
]

url = "http://purbabardhaman.wbpolice.gov.in/arrest1"


for station in stations:

    query_string = f"name1={station.replace(' ', '+')}"
    resp = requests.post(url, query_string)
    
    print("\033[37m\n\n"+station +" main page fetched\n")


    links = re.findall(r"firs\/fir_file\/.*pdf", resp.text)
    for link in links:

        pdf_url = "http://purbabardhaman.wbpolice.gov.in/" + link


        path = Path.cwd().joinpath("data", station)
        path.mkdir(parents=True, exist_ok=True)

        try:
            filename =  path.joinpath(pdf_url[pdf_url.rfind('/')+1:])
        except:
            continue

        if os.path.exists(filename):
            print("\033[93m" + pdf_url + "\tfile already present")
            continue

        try:
            start = time.perf_counter()
            pdfx = requests.get(pdf_url, timeout=10)
            request_time = time.perf_counter() - start
        except:
            print("\033[91m" + pdf_url + "\tget request exception")
            continue

        filename.write_bytes(pdfx.content)
        print("\033[32m"+ pdf_url + "\tdownloaded\t" + str(request_time) +" secs")
