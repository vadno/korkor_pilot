#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# author: Vadász Noémi
# created: 2019/03/28

# feldolgozza a google spreadsheetsben annotált, előtte emtsv-vel elemzett korpuszfájlt
# bemenet
# csv (google spreadsheetsből importált)
# token, összes elemzés, tő, részletes címke, tag, helyes, javított tő, tokenizálás, javított token, megjegyzés
# tokenenként annyi sor, ahány különböző emmorph elemzés (címke+tő kombináció) van az anas oszlopban
# a kézzel kiválasztott címke+tő kombinációnál a 6. (helyes) oszlopban X szerepel
# ha nem üres a 6. oszlop, akkor a 2. oszlopba annak tartalma megy (lemma javítása)
# ha nem üres a 7. oszlop, akkor a tokenizálás javítását szolgáló parancsokat végre kell hajtani
# ha nem üres a 8. oszlop, akkor a 0. oszlopba annak tartalma megy (token javítása)

# kimenet
# xtsv
# form, anas, lemma, xpostag
# soronként egy token
# mondatok között üres sor

import csv
import sys

# 0: string
# 1: anas
# 2: lemma
# 3: hfstana
# 4: tag
# 5: helyes
# 6: javított tő
# 7: tokenizálás
# 8: javított token
# 9: megjegyzés


def read_file():
    """
    stdin-ről olvas
    első sor: header
    feldolgozza a tokenizálás javítását szolgáló parancsokat, ennek megfelelően tárolja el a sorokat
    """

    empty_line = dict()
    empty_line['string'] = ''

    lines = list()

    newtoken = dict()

    reader = csv.reader(sys.stdin)
    next(reader)
    for line in reader:
        # új token
        if line[0] or line[7] == 'token beszúr':

            if newtoken:
                lines.append(newtoken)
                newtoken = dict()

            if line[7] not in ('token össze', 'token töröl'):
                if line[7] == 'token beszúr':
                    newtoken['anas'] = '[]'

                newtoken['anas'] = line[1]
                # jó token
                if not line[8]:
                    newtoken['string'] = line[0]
                # hibás token
                else:
                    newtoken['string'] = line[8]

                # jó tő
                if not line[6]:
                    newtoken['lemma'] = line[2]
                # hibás tő
                else:
                    newtoken['lemma'] = line[6]

                # jó vagy javított címke
                if line[5]:
                    # jó címke
                    if line[5] == 'X':
                        newtoken['hfstana'] = line[4]
                    # javított címke
                    else:
                        newtoken['hfstana'] = line[5]

            # összetokenizálás
            else:
                # összetokenizálás első sora
                if line[6] and line[7]:

                    newtoken['string'] = line[8]
                    newtoken['lemma'] = line[6]
                    newtoken['anas'] = line[1]
                    # jó címke
                    if line[5] == 'X':
                        newtoken['hfstana'] = line[4]
                    # javított címke
                    else:
                        newtoken['hfstana'] = line[5]

        # alternatív címkék
        else:
            # alternatív címke és tő megadva
            if 'X' in line[5]:
                newtoken['lemma'] = line[2]
                newtoken['hfstana'] = line[4]

            # széttokenizálás
            elif line[7] == 'token szét':
                lines.append(newtoken)
                newtoken = dict()
                newtoken['anas'] = '[]'
                newtoken['string'] = line[8]
                newtoken['lemma'] = line[6]
                newtoken['hfstana'] = line[5]

            # mondat széttokenizálása
            elif all(cell == '' for cell in line) or line[7] == 'mondat szét':
                lines.append(newtoken)
                lines.append(empty_line)
                newtoken = dict()

    lines.append(newtoken)

    return lines


def print_file(lines):
    """
    stdout-ra ír
    xtsv kimenet
    """

    print('form\tanas\tlemma\txpostag')

    for line in lines:
        if len(line) > 1:
            print(line['string'], line['anas'], line['lemma'], line['hfstana'], sep='\t')
        else:
            print(line['string'])

    print('')


def main():

    lines = read_file()
    print_file(lines)


if __name__ == "__main__":
    main()
