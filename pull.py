#!/usr/bin/env python3
import argparse
import os, os.path
import requests
import sys


YEAR = 2020


def get_session():
    with open('.session', 'r') as fin:
        session = fin.read().strip()
        return session


def getargs():
    p = argparse.ArgumentParser()
    p.add_argument('day', type=int)
    return p.parse_args()


def main():
    args = getargs()
    session_cookie = get_session()
    print(f'Day {args.day}, session = {session_cookie}')

    url = f'https://adventofcode.com/{YEAR}/day/{args.day}/input'
    dest = f'inputs/input{args.day:02d}.txt'
    if os.path.exists(dest):
        print(f'Input already downloaded at {dest}')
        return -1

    r = requests.get(url, cookies={'session': session_cookie})
    if not r.ok:
        print(f'Failure in download: {r}')
        return -1

    with open(dest, 'wb') as fout:
        fout.write(r.content)
    print(f'Wrote to {dest}')
   
    return 0


if __name__ == '__main__':
    sys.exit(main())
