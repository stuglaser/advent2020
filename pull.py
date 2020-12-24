#!/usr/bin/env python3
import argparse
from datetime import datetime
import os, os.path
import requests
import sys
import time


YEAR = 2020


def get_session():
    with open('.session', 'r') as fin:
        session = fin.read().strip()
        return session


def getargs():
    p = argparse.ArgumentParser()
    p.add_argument('day', type=int)
    p.add_argument('--wait', '-w', action='store_true')
    return p.parse_args()


def main():
    args = getargs()
    session_cookie = get_session()
    print(f'Day {args.day}, session = {session_cookie}')

    url = f'https://adventofcode.com/{YEAR}/day/{args.day}/input'
    dest = f'inputs/input{args.day:02d}.txt'
    if os.path.exists(dest):
        print(f'Input already downloaded at {dest}')
        return 0

    if args.wait:
        now = datetime.now()
        target = datetime(year=now.year, month=now.month, day=now.day, hour=12+9)
        wait = (target - now).total_seconds() + 1
        print(f'Waiting {wait:.1f} seconds until 9pm!')
        time.sleep(wait)

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
