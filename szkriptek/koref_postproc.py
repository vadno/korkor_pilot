#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# author: Vadász Noémi
# created: 2019/12/02

import sys

# 0: TOKEN ID
# 1: FORM
# 2: LEMMA
# 3: UPOS
# 4: UPOS
# 5: FEATS
# 6: HEAD
# 7: DEPREL
# 8: DEPS
# 9: REFREL
# 10: REFTYPE
# 11: javított szóalak
# 12: javított tő
# 13: javított szófaj
# 14: javított morfológia
# 15: tokenizálási hiba
# 16: függőségi hiba


xtsv_fields = {'TOKEN ID': 'id',
               'FORM': 'form',
               #'ANAS': 'anas',
               'LEMMA': 'lemma',
               'UPOS': 'upos',
               #'XPOSTAG': 'xpostag',
               'FEATS': 'feats',
               'HEAD': 'head',
               'DEPREL': 'deprel',
               'REFREL': 'corefhead',
               'REFTYPE': 'coreftype'
        }


def read_lines():

    header = sys.stdin.readline().strip().split('\t')

    lines = list()

    for line in sys.stdin:

        if not line.startswith('#'):
            stripline = line.strip().split('\t')
            if len(stripline) > 1:
                fields = dict()
                for field in header:
                    if len(stripline) > header.index(field):
                        fields[field] = stripline[header.index(field)]
                    else:
                        fields[field] = '_'

                lines.append(fields)
            else:
                lines.append('')

    return header, lines


def do_commands(lines):

    for line in lines:
        if isinstance(line, dict):
            if line['javított szóalak'] != '_':
                line['FORM'] = line['javított szóalak']
            if line['javított tő'] != '_':
                line['LEMMA'] = line['javított tő']
            if line['javított szófaj'] != '_':
                line['UPOS'] = line['javított szófaj']
            if line['javított morfológia'] != '_':
                line['FEATS'] = line['javított morfológia']


def order_fields(lines):

    xlines = list()

    for line in lines:
        if isinstance(line, dict):
            fields = dict()
            for field in line:
                if field in xtsv_fields:
                    fields[xtsv_fields[field]] = line[field]

            for value in xtsv_fields.values():
                if value not in fields:
                    fields[value] = '_'
            xlines.append(fields)

        else:
            xlines.append('')

    xheader = xlines[0].keys()

    return xheader, xlines


def print_xtsv(header, lines):

    print('\t'.join(header))
    for line in lines:
        if isinstance(line, dict):

            print('\t'.join(val for val in line.values()))
        else:
            print(line)


def main():

    header, lines = read_lines()
    do_commands(lines)
    xheader, xlines = order_fields(lines)
    print_xtsv(xheader, xlines)


if __name__ == "__main__":
    main()
