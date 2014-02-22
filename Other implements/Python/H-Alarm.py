#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  H-Alarm.py
#
#  version 0.1
#
#  Copyright 2013 deb-user <altay-man@mail.ru>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#
#  Writed in GNU Emacs 23.4.1.
"""
    Script for Horochan.
"""

# Imports.

import Graphic
import time
import os
import re
#import _thread
from urllib.request import urlopen


# Consts.

TARGET_SITE = r'http://horochan.ru/'

# Templates.

PATTERN_POST_NUM = re.compile('<div class="reply" id="(\d+)">')
PATTERN_THREAD = re.compile('Из треда:\t+<a href="(.*?)">')
# Group 1 is board, Group 2 is number of thread.
PATTERN_THREAD_NUM = re.compile('(\w)/res/(\d+?)/#')
PATTERN_MESS = re.compile('<div class="message">.*?<br />(.*?)</div>')
PATTERN_PIC_THUMB = re.compile('<!-- IMAGES -->.*?<img src="(http://horochan.ru/data/thumb/.*?)"')

# Functions.

def page_grab():
    '''
      === page_grab(site=TAGRET_SITE) - download page from
             site with url in 1st arg and return
             HTML-source.
    '''
    page = urlopen(TARGET_SITE)
    source_page = str(page.read().decode('utf-8'))
    page.close()

    return source_page


def page_parsing(source_page):
    '''
      === page_parsing(source_page) - parse HTML-page using re-module,
             returned by page_grab().
             Return variables:
                Post_num - number.
                Post_thread - link on post.
                Post_thread_num - board & number of thread.
                Post_mess - messange.
    '''
    source_page = source_page.split('<!-- REPLY CONTAINER -->')
    source_page = source_page[1]
    source_page = source_page.replace("\n", '')

    if re.search(PATTERN_POST_NUM, source_page):
        post_num = re.search(PATTERN_POST_NUM, source_page).group(1)
    else:
        post_num = ''

    post_thread = re.search(PATTERN_THREAD, source_page).group(1)
    if re.search(PATTERN_THREAD, source_page):
        post_thread = re.search(PATTERN_THREAD, source_page).group(1)
    else:
        post_thread = ''

    if re.search(PATTERN_THREAD_NUM, source_page):
        post_thread_num = [re.search(PATTERN_THREAD_NUM, source_page).group(1), \
            re.search(PATTERN_THREAD_NUM, source_page).group(2)]
    else:
        post_thread_num = ['', '']

    if  re.search(PATTERN_MESS, source_page):
        post_mess = re.search(PATTERN_MESS, source_page).group(1)
    else:
        post_mess = ''

    if re.search(PATTERN_PIC_THUMB, source_page):
        pic_link = re.search(PATTERN_PIC_THUMB, source_page).group(1)
    else:
        pic_link = ''

    return [post_num, post_thread, post_thread_num, post_mess, pic_link]


def checking(source_page):
    '''
      === checking(source_page) - matching copy of page on pc and new page.
             If pages matches - func return False, else - True.
    '''
    if 'checker' in os.listdir():
        check = open('checker', 'r')
        check_text = check.read()
        check.close()
        if check_text == source_page:
            return False
        else:
            return True

    else:
        check = open('checker', 'w')
        check.write(source_page)
        check.close()
        return False


def main():
    """
        Main func.
    """
    while 1:
        source_page = page_grab()
        if checking(source_page):
            params_list = page_parsing(source_page)
            Graphic.main(params_list)
            time.sleep(10)
        else:
            time.sleep(10)

if __name__ == '__main__':
    main()
