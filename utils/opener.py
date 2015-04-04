#!/usr/bin/env python3

import urllib.request

def create_req(url):
    req = urllib.request.Request(
            url, 
            data=None, 
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
            }
        )
    return req

def urlopen(url):
    req = create_req(url)
    return urllib.request.urlopen(req, timeout=10).read()
