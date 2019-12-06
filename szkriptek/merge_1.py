#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    author: Noémi Vadász
    last update: 2019.10.09.

"""
import csv
import sys

conllu = ['id', 'form', 'lemma', 'upos', 'xpos', 'feats', 'head', 'deprel', 'deps', 'misc']

xtsv_fields = {'id': '_',
               'form': '_',
               'anas': '_',
               'lemma': '_',
               'upos': '_',
               'xpostag': '_',
               'feats': '_',
               'deprel': '_',
               'head': '_'}


def check_fields(lines):

    for line in lines:
        if isinstance(line, dict):
            for key, value in line.items():
                print(key, value)


def read_conll(infile):

    lines = list()

    with open(infile) as inf:
        reader = csv.reader(inf, delimiter='\t', quoting=csv.QUOTE_NONE)

        for line in reader:
            if len(line) > 1 and '#' not in line[0]:
                fields = dict()
                for field in conllu:
                    fields[field] = line[conllu.index(field)]
                fields.pop('xpos')
                lines.append(fields)
            elif len(line) == 0:
                lines.append('')
            else:
                pass
                # lines.append(line)

    # check_fields(lines)

    return lines


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


def merge_files(xtsv, conll):

    # print(len(conll))
    # print(len(xtsv))

    zipped = list()
    i = 0

    dummy = {'form': 'DUMMY',}

    while i < len(conll) and i < len(xtsv):

        if isinstance(conll[i], dict) and isinstance(xtsv[i], dict):

            if conll[i]['form'].lower() == xtsv[i]['form'].lower():
                allfields = xtsv_fields.copy()
                for feat, val in conll[i].items():
                    if feat in allfields:
                        allfields[feat] = val
                allfields['xpostag'] = xtsv[i]['xpostag']
                allfields['anas'] = xtsv[i]['anas']
                zipped.append(allfields)
            elif (conll[i]['form'] in ('DROP', 'KOPULA')) or conll[i]['form'].startswith('ZÉRÓ_'):
                allfields = xtsv_fields.copy()
                for feat, val in conll[i].items():
                    if feat in allfields:
                        allfields[feat] = val
                zipped.append(allfields)
                xtsv.insert(i, dummy)

            # TODO mi van, ha a form különbözött??? hiba lesz
            elif conll[i]['form'].lower() != xtsv[i]['form'].lower():
                allfields = xtsv_fields.copy()
                for feat, val in conll[i].items():
                    if feat in allfields:
                        allfields[feat] = val
                allfields['form'] = conll[i]['form']
                allfields['xpostag'] = xtsv[i]['xpostag']
                allfields['anas'] = xtsv[i]['anas']
                zipped.append(allfields)

        # elif isinstance(conll[i], list) and conll[i][0].startswith('#'):
        #     zipped.append(conll[i][0])

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
    # print(filename + ' feldolgozása...')

    xtsv_file = '../2_proc_google/processed_tsv/all/' + filename + '.tsv'
    conllu_file = '../4_pro/pro_inserted/' + filename + '.conll'

    xtsv_lines = read_xtsv(xtsv_file)
    conll_lines = read_conll(conllu_file)

    zipped = merge_files(xtsv_lines, conll_lines)

    ofile = 'merged/' + filename + '.xtsv'
    print_corpus(ofile, zipped)
    # print('')


if __name__ == "__main__":
    main()
