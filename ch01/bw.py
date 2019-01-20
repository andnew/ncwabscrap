#!/bin/python
# -*- coding:utf-8 -*-

import builtwith
import whois
from urllib import request
import re
import itertools

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/45.0.2454.85 Safari/537.36 115Browser/6.0.3',
    'Referer': 'http://www.lagou.com/zhaopin/Python/?labelWords=label',
    'Connection': 'keep-alive'}


def download(url):
    try:
        req = request.Request(url, headers=headers)
        html = request.urlopen(req).read()
        html = html.decode('utf-8')
    except request.URLError as e:
        print('Download error:', e.reason)
        html = None
    return html


def download3(url, num_retries=2):
    """
    Download function that also retries 5XX errors
    """
    print('Downloading:', url)
    try:
        req = request.Request(url, headers=headers)
        html = request.urlopen(req).read()
        html = html.decode('utf-8')
    except request.URLError as e:
        print('Download error:', e.reason)
        html = None
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                # retry 5XX HTTP errors
                html = download3(url, num_retries - 1)
    return html


def crawl_sitemap(url):
    sitemap = download3(url, 2)
    links = re.findall('<url><loc>(.*?)</loc></url>', sitemap)
    for link in links:
        html = download3(link, 2)
        print('======  ', html)


def consecute():
    max_errors = 5
    num_errors = 0

    for page in itertools.count(0):
        url = 'http://example.webscraping.com/places/default/view/%d' % page
        html = download(url)
        if html is None:
            num_errors += 1
            if num_errors == max_errors:
                break
        else:
            num_errors = 0


if __name__ == '__main__':

    # webs = ['http://example.webscraping.com/sitemap.xml']
    #
    # for web in webs:
    #     crawl_sitemap(web)
    consecute()
