#!/usr/bin/env python3

import os

def get_tag_date(tag, path):
    date = os.popen('cd '+path+' && git log -1 --format=%ai '+tag).readlines()
    date = date[0].split()[0]
    date = date.split('-')
    date.reverse()
    date = '.'.join(date)
    return date

def get(path):
    changelog = []
    tags = os.popen('cd '+path+' && git tag').readlines()

    for i in range(len(tags)-1):
        changelog.append(tags[-i-1].rstrip('\n')+'(%s)'%get_tag_date(tags[-i-1], path))
        changelog.append('==========')
        rel_note = os.popen('cd '+path+' && git log '+tags[-i-2].strip()+'..'+tags[-i-1].strip()+' --pretty=format:" - %s" --reverse').readlines()
        for line in rel_note:
            changelog.append(line.rstrip('\n'))
        changelog.append('')
    return changelog


if __name__ == '__main__':
    get()