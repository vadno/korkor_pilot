#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# author: Vadász Noémi
# created: 2018/12/12

# előkészíti az emtsv-vel (emtoken, emmorph, emtag) elemzett fájlokat a kézi javításra
# bemenet
# xtsv
# form, anas, lemma, xpostag
# soronként egy token
# mondatok között üres sor

# kimenet
# tsv
# token, összes elemzés, tő, részletes címke, tag, helyes, javított tő, tokenizálás, javított token, megjegyzés
# tokenenként annyi sor, ahány különböző emmorph elemzés (címke+tő kombináció) van az anas oszlopban
# az emtag által választott címke+tő kombinációnál a 6. (helyes) oszlopban X szerepel
# mondatok között üres sor

import sys
import csv
import json
from collections import namedtuple


def read_file():
    """
    stdin-ről olvas
    első sor: header
    soronként tokenek, amiket namedtuple-ök listájaként tárol el
    """

    lines = list()

    reader = csv.reader(sys.stdin, delimiter='\t', quoting=csv.QUOTE_NONE)
    header = next(reader)
    Line = namedtuple("Line", header)
    for line in reader:
        if line:
            try:
                lines.append(Line._make(line))
            except:
                print(line)
        else:
            lines.append('')

    return lines


def print_file(lines):
    """
    feldolgozza a namedtuple-ök listáját
    json-t csinál az anas mezőből
    stdout-ra ír
    tokenenként annyi sort ír, ahány címke+tő kombináció volt az anas mezőben
    X-et ír az egyértelműsített címke+tő sorába
    """

    print('token\tösszes elemzés\ttő\trészletes címke\ttag\thelyes\tjavított tő\ttokenizálás\tjavított token\tmegjegyzés')

    for line in lines:
        if line:
            anas = set()
            readables = list()

            # parse json (anas)
            try:
                jsons = json.loads(line.anas)
                for js in jsons:
                    anas.add((js['lemma'], js['readable'], js['tag']))
                    if js['lemma'] == line.lemma and js['tag'] == line.xpostag:
                        readables.append(js['readable'])
            except ValueError:
                pass

            if len(readables) == 1:
                # remove the tag disambiguated
                try:
                    anas.remove((line.lemma, readables[0], line.xpostag))
                except KeyError:
                    pass
                print(line.form, line.anas, line.lemma, readables[0], line.xpostag, 'X', sep='\t')

            else:
                print(line.form, line.anas, line.lemma, '', line.xpostag, '!', sep='\t')

            for ana in sorted(anas, key=lambda x: x[1].count('+'), reverse=False):
                print('\t\t', '\t'.join(ana))

        # empty sentence separator line
        else:
            print('')


def main():

    lines = read_file()
    print_file(lines)


if __name__ == "__main__":
    main()
