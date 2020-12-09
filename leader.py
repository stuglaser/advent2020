#!/usr/bin/env python3
import argparse
import json
import requests
import os
import os.path
import sys
from tabulate import tabulate
import time


START_STAMP = 1606798800


def day_start(day):
    return START_STAMP + 24 * 60 * 60 * (day - 1)


def get_session():
    with open('.session', 'r') as fin:
        session = fin.read().strip()
        return session


def get_leaderboard(board=None, force_refresh=False):
    if board is None:
        with open('.leaderboard', 'r') as fin:
            board = int(fin.read().strip())

    cached_file = '.cached_leaderboard'
    if not force_refresh and os.path.exists(cached_file):
        with open(cached_file, 'rb') as fin:
            data = json.load(fin)
            if (time.time() < data['stamp'] + 5 * 60 and
                data['leaderboard']['owner_id'] == str(board)):
                return data['leaderboard']

    print('(refresh)')


    url = f'https://adventofcode.com/2020/leaderboard/private/view/{board}.json'
    session_cookie = get_session()
    r = requests.get(url, cookies={'session': session_cookie})
    if not r.ok:
        raise Exception(f'Failure in download: {r}')

    leaderboard = r.json()
    with open(cached_file, 'w') as fout:
        json.dump({'stamp': time.time(), 'leaderboard': leaderboard}, fout)

    return leaderboard


def lookup_completion(board, member, day, part):
    try:
        return int(board['members'][member]['completion_day_level']
                   [str(day)][str(part)]['get_star_ts'])
    except KeyError:
        return None

def fmt_time(t):
    secs = t % 60
    t = t // 60
    mins = t % 60
    t = t // 60
    hrs = t % 24
    t = t // 24
    days = t

    if days > 0:
        return f'{days}d {hrs}:{mins:02}:{secs:02}'
    if hrs > 0:
        return f'{hrs}:{mins:02}:{secs:02}'
    return f'{mins:2}:{secs:02}'


def getargs():
    p = argparse.ArgumentParser()
    p.add_argument('--refresh', '-r', action='store_true')
    p.add_argument('--part', '-p', type=int, default=2, choices=(1, 2))
    return p.parse_args()


def main():
    args = getargs()

    board = get_leaderboard(force_refresh=args.refresh)

    members = sorted(board['members'].keys(), key=int)
    last_day = min(25, int(time.time() - START_STAMP) // (24*60*60) + 1)

    headers = ['']
    for _ in range(2):
        for m in members:
            headers.append(board['members'][m]['name'].split()[0])

    table = []
    for day in range(1, last_day + 1):
        table.append([f'Day {day}'])

        for m in members:
            t = lookup_completion(board, m, day, args.part)
            if t is None:
                table[-1].append('-')
            else:
                table[-1].append(fmt_time(t - day_start(day)))

    print(tabulate(table, headers=headers, stralign='right'))
    return 0


if __name__ == '__main__':
    sys.exit(main())
