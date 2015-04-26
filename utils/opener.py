#!/usr/bin/env python3

import urllib.request

def create_req(url):
    req = urllib.request.Request(url, headers={'User-Agent' : "Magic Browser"})
    return req

def urlopen(url):
    req = create_req(url)
    d = urllib.request.urlopen(req, timeout=30)
    data = d.read()
    d.close()
    return data

def urlopener(url, tries=1):
    print ('\033[34m>\033[0m '+_('Downloading')+' '+url)
    for i in range(tries):
        try:
            print(str(i+1))
            data = urlopen(url)
            print ('\033[1;32mOK\033[0m')
            return data.decode(encoding='UTF-8')
        except:
            pass
    print ('\033[1;31m[!]\033[0m '+_('Unable to download page, check the network connection'))
    return None

