import ssl
import re, os
from bs4 import BeautifulSoup
import urllib.request
import requests
from urllib.error import HTTPError
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

ssl._create_default_https_context = ssl._create_unverified_context

def get_text(url, output_file_name=None, title=None, snippet=None):
    try:
        headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0"}
        response = requests.get(url, headers=headers, verify=False, timeout=(20, 30))
        html = response.content
        #response=urllib.request.urlopen(url)
        #html=response.read()
        soup = BeautifulSoup(html,features="html.parser")
        text = soup.get_text()

        if text != None:
            text = re.sub(r'\n+', '\n', text).strip()

            # Exclude short paragraphs (less than 3 words)
            clean_text = ""
            if title is not None:
                clean_text += (title + "\n")
            if snippet is not None:
                clean_text += (snippet + "\n") 
            for line in text.split('\n'):
                if len(line.strip().split(' ')) > 4:
                    clean_text += line
                    clean_text += '\n'
            if output_file_name != None:
                with open(output_file_name,"w") as f:
                    f.write(clean_text)
        return clean_text
    except HTTPError as err:
        print(err)
        print("An error observed, skipped the url " + url)
        return None


if __name__ == "__main__":
    print(">>>> Reading URL 1")
    print(get_text('https://www.aljazeera.com/economy/2024/5/24/singapore-airlines-changes-seatbelt-rules-route-after-fatal-turbulence'))
    print(">>>> Reading URL 2")
    print(get_text('https://www.bbc.com/news/articles/c8889d7x8j4o'))
    print(">>>> Reading URL 3")
    print(get_text('https://apnews.com/article/singapore-airlines-flight-turbulence-5a9a268e1a6a6fb9ece7e58b5ea9231b'))