#!/usr/bin/env python2
"""
Log Puzzle exercise

Copyright 2010 Google Inc.
Licensed under the Apache License, Version 2.0
http://www.apache.org/licenses/LICENSE-2.0

Given an Apache logfile, find the puzzle URLs and download the images.

Here's what a puzzle URL looks like (spread out onto multiple lines):
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg
HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US;
rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""

__author__ = """Bethany Folino with help from Matt Perry, Jacob Short and
https://stackoverflow.com/questions/23753040/
keep-a-list-to-prevent-duplicates-efficiency-in-python"""

import os
import re
import sys
import urllib.request
import argparse


def read_urls(filename):
    """Returns a list of the puzzle URLs from the given log file,
    extracting the hostname from the filename itself, sorting
    alphabetically in increasing order, and screening out duplicates.
    """
    result = set()  # eliminate duplicates
    findurls = re.compile(r"\S(\w+)\/(\w+)\/(\w+)\-(\w+)\-(\w+)\/(\w+)\/(\w+)\/(\w+)\-(\D+)\.(\w+)") # noqa - can't split this up, I tried
    with open(filename) as file:
        contents = file.read()

    matches = findurls.finditer(contents)

    finddomainname = filename.split("_")[-1]
    # finddomainname = re.compile(r"_(\w+).(\w+).(\w+)")
    # matches2 = finddomainname.finditer(filename)

    # whole_matches = f"{finddomainname}{matches}"
    # print(whole_matches)

    for item in matches:
        result.add(f"http://{finddomainname}{item[0]}")

    sorted_result = sorted(result, key=lambda x: x.split("-")[-1])

    return sorted_result


def download_images(img_urls, dest_dir):
    """Given the URLs already in the correct order, downloads
    each image into the given directory.
    Gives the images local filenames img0, img1, and so on.
    Creates an index.html in the directory with an <img> tag
    to show each local image file.
    Creates the directory if necessary.
    """
    # check to see if dest_dir exists, and make one if not
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)
    # retrieve URLs, open HTML file and write in it
    img_count = 0
    with open(os.path.abspath(os.path.join(dest_dir, "index.html")), "w+") as html: # noqa
        html.write("<html>")
        html.write("<body>")
        for url in img_urls:
            with open(os.path.abspath(os.path.join(dest_dir, f"img{img_count}")), "w+"): # noqa
                urllib.request.urlretrieve(url, f"{dest_dir}/img{img_count}")
            img = "img"
            html_template_2 = f"<img src={img}{img_count}>"
            img_count = img_count + 1
            html.write(html_template_2)
        html_template_3 = """</body>
        </html>"""
        html.write(html_template_3)


def create_parser():
    """Creates an argument parser object."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--todir',
                        help='destination directory for downloaded images')
    parser.add_argument('logfile', help='apache logfile to extract urls from')

    return parser


def main(args):
    """Parses args, scans for URLs, gets images from URLs."""
    parser = create_parser()

    if not args:
        parser.print_usage()
        sys.exit(1)

    parsed_args = parser.parse_args(args)

    img_urls = read_urls(parsed_args.logfile)

    if parsed_args.todir:
        download_images(img_urls, parsed_args.todir)
    else:
        print('\n'.join(img_urls))


if __name__ == '__main__':
    main(sys.argv[1:])
