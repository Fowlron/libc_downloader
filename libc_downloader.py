#!/bin/python3

import requests
from bs4 import BeautifulSoup
from pathlib import Path
import os


def get_list(url, prefix='', suffix=''):
    reponse = requests.get(url)
    soup = BeautifulSoup(reponse.text, 'html.parser')
    parent = [(node.contents[0], url + node.get('href')) for node in soup.find_all('a') if node.contents[0].startswith(prefix) and node.contents[0].endswith(suffix)]
    return parent

def print_pretty_list(lst, split_threshold=30, spaces=7):
    if len(lst) < split_threshold:
        for line in lst:
            print(line)
        return

    max_size = 0
    for line in lst:
        l = len(str(line))
        if l > max_size:
            max_size=l

    half = len(lst) // 2
    for i in range(half):
        print(str(lst[i]) + ' ' * (max_size-len(lst[i])+spaces) + str(lst[i+half]))
    if len(lst) % 2 == 1:
        print(str(lst[-1]))


def download(url, filename):
    r = requests.get(url, allow_redirects=True)
    open(filename, 'wb').write(r.content)

def extract(directory, filename):
    os.chdir(directory)
    os.system('ar x ' + directory + filename)

    print(directory+'data.tar.gz')
    if os.path.exists(directory + 'data.tar.gz'):
        os.system('tar xf ' + directory + 'data.tar.gz')
        os.system('rm ' +
                directory + 'data.tar.gz')
    elif os.path.exists(directory + 'data.tar.xz'):
        os.system('tar xf ' + directory + 'data.tar.xz')
        os.system('rm ' +
                directory + 'data.tar.xz')
    else:
        print("Couldn't find the file to extract.")
        return

    os.system('rm ' +
            directory + 'debian-binary ' + 
            directory + 'control.tar.gz ' + 
            directory + filename)


def main():
    print('#'*35)
    print('#' + 9*' ' + 'LIBC DOWNLOADER' + 9*' ' + '#')
    print('#'*35 + '\n')

    print('Which distro\'s libc to download?\n')
    print('0. Debian')
    print('1. Ubuntu')

    distro = input()
    base_dir = os.path.dirname(os.path.realpath(__file__))
    if distro == '0':
        base_dir += '/debian/'
        url = 'http://archive.debian.org/debian/pool/main/g/glibc/'
    elif distro == '1':
        base_dir += '/ubuntu/'
        url = 'http://archive.ubuntu.com/ubuntu/pool/main/g/glibc/'
    else:
        print("Invalid input")
        return

    response = get_list(url, prefix='libc6_', suffix='.deb')
    print('\nFound libs:')
    print_pretty_list([str(i) + ". " + response[i][0][:-4] for i in range(len(response))])

    print('Which to download?')
    idx = int(input())

    base_dir += response[idx][0][:-4] + "/"
    Path(base_dir).mkdir(parents=True, exist_ok=True)
    print('\nDownloading from ' + response[idx][1] + '...')
    download(response[idx][1], base_dir + response[idx][0])
    print('Extracting ' + response[idx][0] + '...')
    extract(base_dir, response[idx][0])
    print('Done.')

main()

