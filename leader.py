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
    p.add_argument('--by-day', '-b', action='store_true')
    return p.parse_args()


def show_by_day(board):
    members = sorted(board['members'].keys(), key=int)
    last_day = min(25, int(time.time() - START_STAMP) // (24*60*60) + 1)

    INF = last_day + 10000
    INF = 1607577361 + 99999999

    for day in range (1, last_day + 1):
        headers = [f'Day {day}', 'Part 1', 'Part 2']
        data = []
        for m in members:
            name = (board['members'][m]['name'] or
                    'anon' + board['members'][m]['id'])
            data.append((name,
                         lookup_completion(board, m, day, 1),
                         lookup_completion(board, m, day, 2)))

        data.sort(key=lambda d: (d[2] or INF, d[1] or INF))
        t0 = day_start(day)
        table = [(d[0], fmt_time(d[1] - t0) if d[1] else '', fmt_time(d[2] - t0) if d[2] else '')
                 for d in data]
        print(tabulate(table, headers=headers))
        print()


def main():
    args = getargs()

    board = get_leaderboard(force_refresh=args.refresh)
    if args.by_day:
        show_by_day(board)
        return 0

    members = sorted(board['members'].keys(), key=int)
    last_day = min(25, int(time.time() - START_STAMP) // (24*60*60) + 1)

    headers = ['']
    for _ in range(2):
        for m in members:
            name = (board['members'][m]['name'] or
                    'anon' + board['members'][m]['id'])
            headers.append(name.split()[0])

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
