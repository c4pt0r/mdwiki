#!/usr/bin/env python

import os
import sys
from optparse import OptionParser

def do_upload(filename):
    import json
    import urllib
    with open(filename) as fp:
        content = fp.read()
        header = content.split('\n')[0:2]
        data = {}
        for line in header:
            key, value = line.split(':')
            data[key.lstrip().rstrip()] = value.lstrip().rstrip()

        content = '\n'.join(content.split('\n')[2:])
        if data['page'].startswith('/') == False:
            data['page'] = '/' + data['page']
        url = 'http://wiki.0xffff.me/api/edit' + data['page']
        print url
        urllib.urlopen(url, urllib.urlencode({'data': json.dumps({'content': content, 'user':data['author']})}))
def main():
    parser = OptionParser()
    parser.add_option("-u", "--upload", action="store",type="string", dest="upload", default = False, help="upload")

    (options, args) = parser.parse_args()

    if options.upload and len(options.upload) > 0:
        do_upload(options.upload)


if __name__ == '__main__':
    main()
