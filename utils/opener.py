#!/usr/bin/env python3

import urllib.request

headers_list = [
    'Magic Browser',
    'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:37.0) Gecko/20100101 Firefox/37.0'
    ]

def urlopen(url, n=0):
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', headers_list[n])]
    data = opener.open(url)
    return data.read()

def urlopener(url, tries=1):
    print ('\033[34m>\033[0m '+_('Downloading')+' '+url)
    for i in range(tries):
        try:
            data = urlopen(url, i%len(headers_list))
            print ('\033[1;32mOK\033[0m')
            return data.decode(encoding='UTF-8')
        except:
            print(str(i+1))
    print ('\033[1;31m[!]\033[0m '+_('Unable to download page, check the network connection'))
    return None

