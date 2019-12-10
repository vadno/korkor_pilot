#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    author: Noémi Vadász
    last update: 2019.10.09.

"""
import csv
import sys

xtsv_fields = {'id': '_',
               'form': '_',
               'anas': '_',
               'lemma': '_',
               'upos': '_',
               'xpostag': '_',
               'feats': '_',
               'deprel': '_',
               'head': '_',
               'corefhead': '_',
               'coreftype': '_'}


def check_fields(lines):

    for line in lines:
        if isinstance(line, dict):
            for key, value in line.items():
                print(key, value)


def read_xtsv(infile):

    lines = list()

    with open(infile) as inf:
        reader = csv.reader(inf, delimiter='\t', quoting=csv.QUOTE_NONE)
        header = next(reader)
        for line in reader:
            if len(line) > 1:
                fields = dict()
                for field in header:
                    fields[field] = line[header.index(field)]
                fields.pop('lemma')
                lines.append(fields)
            else:
                lines.append('')

    # check_fields(lines)

    return lines


def merge_files(xtsv, coref):

    # print(len(coref))
    # print(len(xtsv))

    zipped = list()
    i = 0

    dummy = {'form': 'DUMMY',}

    while i < len(coref) and i < len(xtsv):

        if isinstance(coref[i], dict) and isinstance(xtsv[i], dict):

            if coref[i]['form'].lower() == xtsv[i]['form'].lower():
                allfields = xtsv_fields.copy()
                for feat, val in coref[i].items():
                    if feat in allfields:
                        allfields[feat] = val
                allfields['anas'] = xtsv[i]['anas']
                allfields['xpostag'] = xtsv[i]['xpostag']
                zipped.append(allfields)
            elif (coref[i]['form'] in ('DROP', 'KOPULA')) or coref[i]['form'].startswith('ZÉRÓ_'):
                allfields = xtsv_fields.copy()
                for feat, val in coref[i].items():
                    if feat in allfields:
                        allfields[feat] = val
                zipped.append(allfields)
                xtsv.insert(i, dummy)
            elif (xtsv[i]['form'] in ('DROP', 'KOPULA')) or xtsv[i]['form'].startswith('ZÉRÓ_'):
                coref.insert(i, dummy)
            # print(coref[i]['form'], xtsv[i]['form'])

        else:
            zipped.append('')

        i += 1

    # check_fields(zipped)

    return zipped


def print_corpus(file, zipped):

    with open(file, 'w') as of:

        header = '\t'.join([key for key, value in xtsv_fields.items()])
        print(header, file=of)

        for line in zipped:
            if isinstance(line, dict):
                fields = '\t'.join(line[field] for field in line)
                print(fields, file=of)
            else:
                print(line, file=of)


def main():

    filename = sys.argv[1]
    print(filename + ' feldolgozása...')

    xtsv_file = '../2_proc_google/processed_tsv/all/' + filename + '.tsv'
    coref_file = '../6_proc_google/processed/' + filename + '.xtsv'

    xtsv_lines = read_xtsv(xtsv_file)
    coref_lines = read_xtsv(coref_file)

    zipped = merge_files(xtsv_lines, coref_lines)

    ofile = 'merged/' + filename + '.xtsv'
    print_corpus(ofile, zipped)


if __name__ == "__main__":
    main()
