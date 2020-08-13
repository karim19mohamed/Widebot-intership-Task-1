import requests
from bs4 import BeautifulSoup
import time
from werkzeug.utils import header_property


def get_main_header(resp):
    if resp.status_code == 200:
        soup = BeautifulSoup(resp.text, 'html.parser')
        l = soup.find(id="firstHeading")
        return l.text
def get_nxt_link(links_title,parag_txt):
    brachet = 0
    pranthesis = 0
    box = 0
    idx=0
    for i in range(0,len(parag_txt)):
        if idx >= len(links_title):
            return -1
        c=parag_txt[i]
        if c == '(':
            brachet = brachet+1
        if c == ')':
            brachet = brachet-1
        if c == '[':
            box=box+1
        if c == ']':
            box = box-1
        if c == '"':
            pranthesis = pranthesis^1
        j=0
        while j<len(links_title[idx]) and i<len(parag_txt) and links_title[idx][j] == parag_txt[i]:
            j=j+1
            i=i+1
        if j==len(links_title[idx]):
            #print(idx,links_title[idx],brachet,pranthesis,box)
            if brachet==0 and pranthesis==0 and box==0:
                return idx
            idx=idx+1
    return -1
def link_analysis(resp):
    if resp.status_code == 200:
        soup = BeautifulSoup(resp.text, 'html.parser')
        l = soup.find(attrs={"class": "mw-parser-output"})
        for i in l.findAll("p"):
            parag_txt=i.text
            links=[]
            links_title=[]
            for j in i.findAll("a"):
                lnk = j.get('href')
                #print(lnk,"  ",j.text)
                if lnk != None and len(j.text)>0 and j.text[0]!='[':
                    links.append(lnk)
                    links_title.append(j.text)
            idx_nxt_link=get_nxt_link(links_title,parag_txt)
            if idx_nxt_link!=-1:
                return links[idx_nxt_link]
def prepare_link(url):
    main_link1 = "https://en.wikipedia.org/"
    main_link2 = "https://en.wikipedia.org"
    if url[0]=='/':
        return main_link2 + url
    elif url[0]!='h':
        return main_link1 + url
    return url
def main():
    url = input()
    #url = "https://en.wikipedia.org/wiki/Toy"
    #url = "https://en.wikipedia.org/wiki/Country"
    #url = "https://en.wikipedia.org/wiki/Epistemology"
    url = prepare_link(url)
    resp = requests.get(url)
    header = get_main_header(resp)
    vis = {header:1}
    print(header)
    while (header!="Philosophy"):
        url = link_analysis(resp)
        url = prepare_link(url)
        resp = requests.get(url)
        header = get_main_header(resp)
        print(header)
        if vis.get(header)!=None:
            break
        vis[header] = 1
        time.sleep(0.5)
main()