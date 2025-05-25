#!/usr/bin/env python3

def _query_arxiv_raw(arxiv_ids: str) -> requests.Response:
    """
    Make a request to the arXiv API and return the raw response.

    Args:
        arxiv_ids (str): The arXiv identifier, concatenated by commas if there
        are multiple.

    Returns:
        requests.Response: The raw response from the arXiv API.
    """
    api_url = f"https://export.arxiv.org/api/query?id_list={arxiv_ids}"
    response = requests.get(api_url, timeout=10.0)  # timeout after 10s
    # Check if the request was unsuccessful (status code 200)
    if response.status_code != 200:
        response.raise_for_status()
    return response

# get the arxiv id
import sys
import requests
# from string import strip, split
# arg = sys.argv[1]
arg = "https://arxiv.org/abs/2203.05794"
arg = arg.strip()
arg = arg.strip("arxiv:")
arg = arg.strip("http://")
arg = arg.strip("https://")
arg = arg.strip("www.")
arg = arg.strip("arxiv.org/abs/")
arg = arg.split(sep='v')[0]
xid = arg.strip()

# download the xml
from urllib.request import urlopen
from xml.dom import minidom
usock = urlopen('http://export.arxiv.org/api/query?id_list='+xid)
xmldoc = minidom.parse(usock)
usock.close()

print(xmldoc.toxml())

d = xmldoc.getElementsByTagName("entry")

date = d.getElementsByTagName("updated").firstChild.data
text_year = date[:4]

title = d.getElementsByTagName("title")
text_title = title.firstChild.data#.encode('ascii', 'ignore')

authorlist = []
first = True
for person_name in d.getElementsByTagName("author"):
    # get names
    name = person_name.getElementsByTagName("name")[0]
    text_name = name.firstChild.data#.encode('ascii', 'ignore')
    text_given_name = ' '.join(text_name.split()[:-1])
    text_surname = text_name.split()[-1]
    authorlist.append(text_surname+", "+text_given_name)
    #first author?
    if first:
        text_first_author_surname = text_surname
        first = False

# output

print("@MISC{"+text_first_author_surname+text_year[-2:]+",")
print("author = {"+" and ".join(authorlist)+"},")
print("title = {"+text_title+"},")
print("year = {"+text_year+"},")
print("eprint = {"+xid+"},")
print("URL = {http://www.arxiv.org/abs/"+xid+"},")
print("}")
