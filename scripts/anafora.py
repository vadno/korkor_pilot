#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    author: Noémi Vadász
    last update: 2020.01.17.

"""

from collections import defaultdict
import sys
import csv

ARGUMENTS = {'SUBJ', 'OBJ', 'OBL', 'DAT', 'ATT', 'INF', 'LOCY'}
NOMINALS = {'NOUN', 'PROPN', 'ADJ', 'NUM', 'DET', 'PRON'}
VERBS = {'VERB'}

CONLLU = ['id', 'form', 'lemma', 'upos', 'xpos', 'feats', 'head', 'deprel', 'deps', 'misc']


class Word:

    def __init__(self):
        self.form = None            # token
        self.anas = None            # anas
        self.lemma = None           # egyértelműsített lemma
        self.xpos = None            # emtag
        self.upos = None            # emmorph2ud
        self.feats = None           # emmorph2ud
        self.id = None              # függőségi elemzéshez id
        self.deprel = None          # függőségi él típusa
        self.head = None            # amitől függ az elem
        self.sent_nr = None         # saját mondatszámláló
        self.abs_index = None
        self.deps = None
        self.misc = None

    def print_token(self):
        if isinstance(self.feats, dict):
            feats = '|'.join(feat + '=' + self.feats[feat] for feat in sorted(self.feats, key=str.lower))
        else:
            feats = self.feats
        print('\t'.join([self.id, self.form, self.lemma, self.upos, self.xpos, feats, self.head, self.deprel, self.deps, self.misc]))


class Verb(Word):

    def __init__(self):
        super(Word, self).__init__()
        self.defi = 'NDef'
        self.number = None
        self.person = None
        self.verbform = None
        self.moodtense = None

    def ige_kiir(self):
        print('{}: {}'.format(self.form, self.upos))
        print('{}, {}, {}, {}'.format(self.defi, self.number, self.person, self.verbform, self.moodtense))


class Actor(Word):

    def __init__(self):
        super(Word, self).__init__()
        self.case = None
        self.number = 'Sg'
        self.nr_psor = None
        self.nr_psed = None
        self.person = '3'
        self.pers_psor = None
        self.prontype = None
        self.poss = None
        self.refl = None
        self.np_nr = None
        self.role = list()
        self.defi = None
        self.foglalt = None

    def kiir(self):
        print('{0}: {1}, {2}'.format(self.form, self.xpos, self.case))
        print('\tperson: {0}, number: {1}'.format(self.person, self.number))
        for i in self.role:
            print('\trole: {0}, np_nr: {1}, sent_nr: {2}'.format(i[0], i[1], i[2]))


def parse_fields(token, line):

    for field in CONLLU:
        setattr(token, field, line[CONLLU.index(field)])


def read_file():

    corp = dict()

    counter = 1

    reader = csv.reader(iter(sys.stdin.readline, ''), delimiter='\t', quoting=csv.QUOTE_NONE)

    orig = ''
    sent = list()

    for line in reader:

        if len(line) > 1 and '#' not in line[0]:

            if line:
                token = Word()
                parse_fields(token, line)
                token.sent_nr = str(counter)
                token.abs_index = str(counter) + ':' + str(token.id)
                sent.append(token)

        elif len(line) == 1 and line[0].startswith('#'):
            orig = line[0] + '\n# sent_id = ' + str(counter)

        else:
            counter += 1
            corp[orig] = sent
            sent = list()

    return corp


def base_features(pro, head):
    """
    feature-ök, amelyeket a zéró elem attól a fejtől örököl
    :param pro: zéró elem
    :param head: fej
    :return:
    """

    for field in vars(head):
        setattr(pro, field, getattr(head, field))


def parse_udfeats(feats):
    """
    az UD jegyek sztringjét dolgozza fel (| és = mentén)
    :param feats: UD jegyek sztringje
    :return: dictbe rendezett kulcs-érték párok
    """

    featdict = dict()

    if feats != '_':
        for feat in feats.split('|'):
            feat = feat.split('=')
            featdict[feat[0]] = feat[1]

    return featdict


def verb_feats(verb):

    verb.verbform = verb.feats['VerbForm']
    if verb.verbform == 'Fin':
        verb.defi = verb.feats['Definite']
        verb.number = verb.feats['Number']
        verb.person = verb.feats['Person']
    elif verb.verbform == 'Inf' and 'Number' in verb.feats:
        verb.number = verb.feats['Number']
        verb.person = verb.feats['Person']
    else:
        pass


def actor_feats(actor):

    if actor.upos == 'ADV':
        if actor.feats:
            if 'PronType' in actor.feats:
                actor.prontype = actor.feats['PronType']

    elif actor.feats:
        if 'Case' in actor.feats:
            actor.case = actor.feats['Case']
        if 'Number' in actor.feats:
            actor.case = actor.feats['Number']
        if 'Number[psor]' in actor.feats:
            actor.nr_psor = actor.feats['Number[psor]']
            actor.pers_pros = actor.feats['Person[psor]']
        if 'Number[psed]' in actor.feats:
            actor.nr_psed = actor.feats['Number[psed]']

        if actor.upos == 'PRON':
            actor.person = actor.feats['Person']
            if 'PronType' in actor.feats:
                actor.prontype = actor.feats['PronType']
            if 'Poss' in actor.feats:
                actor.poss = actor.feats['Poss']
            if 'Refl' in actor.feats:
                actor.refl = actor.feats['Relf']


def actor_features(corpus):
    """

    :return:
    """

    anacorp = dict()   # actorlista: mondatok listaja, kulcs az eredeti mondat, ertek az actor_list

    for sent, toks in corpus.items():

        actor_list = []  # actorlista: mondatok listaja, kulcs az ige, ertek a vonzatok listaja

        npnr = 0
        deps = []
        for head in toks:
            for dep in toks:
                if dep.head == head.id:
                    deps.append((head, dep))

            if head.upos in VERBS and head not in deps:
                deps.append((head, head))

        # egy elemhez hozzarendeli az osszes ramutato dependency viszonyt
        # egy headhez az osszes depot
        deps_dict = {}
        for a, b in deps:
            deps_dict.setdefault(a, []).append(b)

        for head in deps_dict:

            if head.upos in VERBS:

                verb = Verb()
                base_features(verb, head)
                verb.feats = parse_udfeats(verb.feats)
                verb_feats(verb)

                # itt létrejönnek a szereplők, amik az igéhez tartoznak
                actors = defaultdict(list)
                actors[verb] = []

                for dep in deps_dict[head]:
                    if dep.deprel in ARGUMENTS:
                        npnr += 1

                        actor = Actor()
                        base_features(actor, dep)
                        actor.feats = parse_udfeats(actor.feats)
                        actor_feats(actor)

                        actor.np_nr = npnr
                        actor.role.append((dep.deprel, npnr, verb.sent_nr))
                        actor.sent_nr = verb.sent_nr

                        if 'Number[psor]' in actor.feats:
                            actor.defi = 'Def'

                            for ifposs in toks:
                                if ifposs.head == dep.id and ifposs.deprel == 'POSS'\
                                        and ifposs.upos in NOMINALS:
                                    ifposs.upos = 'POSS'
                                    npnr += 1

                                    newactor = Actor()
                                    base_features(newactor, ifposs)
                                    newactor.feats = parse_udfeats(newactor.feats)
                                    actor_feats(newactor)

                                    newactor.np_nr = npnr
                                    newactor.role.append((ifposs.deprel, npnr, newactor.sent_nr))
                                    newactor.sent_nr = verb.sent_nr

                                    actors[verb].append(newactor)

                        actors[verb].append(actor)

                actor_list.append(actors)

        anacorp[sent] = actor_list

    return anacorp


def insert_edge(sent, actual_id, antec_abs_index):

    for tok in sent:
        if actual_id == tok.id:
            tok.misc = antec_abs_index


def plehradics(corpus, anacorp):
    """

    :param
    :return:
    """

    for sent, actorlist in anacorp.items():
        for counter, szereplok in enumerate(actorlist):
            for key, value in szereplok.items():
                for aktualis in value:
                    if key.sent_nr != '1':
                        for key2, value2 in actorlist[counter - 1].items():
                            for elozo in value2:
                                if aktualis.role[-1][0] == 'SUBJ':
                                    if aktualis.form == 'DROP' and elozo.role[-1][0] == 'SUBJ' \
                                            and aktualis.id > elozo.id and elozo.number == aktualis.number:
                                        if elozo.person == aktualis.person or aktualis.person == '3':
                                            elozo.foglalt = True
                                            insert_edge(corpus[sent], aktualis.id, elozo.abs_index)
                                    elif aktualis.lemma == 'az' and elozo.role[-1][0] in ('OBJ', 'OBL', 'DAT')\
                                            and aktualis.id > elozo.id:
                                        elozo.foglalt = True
                                        insert_edge(corpus[sent], aktualis.id, elozo.abs_index)

        for counter, szereplok in enumerate(actorlist):
            for key, value in szereplok.items():
                for aktualis in value:
                    if key.sent_nr != '1':
                        for key2, value2 in actorlist[counter - 1].items():
                            for elozo in value2:
                                if aktualis.role[-1][0] == 'OBJ' and aktualis.upos == 'PRON'\
                                        and elozo.person == aktualis.person and elozo.number == aktualis.number \
                                        and aktualis.id > elozo.id and not elozo.foglalt:
                                    elozo.foglalt = True
                                    insert_edge(corpus[sent], aktualis.id, elozo.abs_index)

                                elif aktualis.role[-1][0] in ('OBL', 'DAT') and elozo.person == aktualis.person\
                                    and elozo.number == aktualis.number and aktualis.upos == 'PRON' \
                                    and elozo.form != 'DROP' and aktualis.id > elozo.id and not elozo.foglalt:
                                    elozo.foglalt = True
                                    insert_edge(corpus[sent], aktualis.id, elozo.abs_index)

                                elif aktualis.role[-1][0] == 'POSS' and elozo.person == aktualis.person\
                                    and elozo.number == aktualis.number and aktualis.upos == 'PRON'\
                                        and aktualis.id > elozo.id:
                                    elozo.foglalt = True
                                    insert_edge(corpus[sent], aktualis.id, elozo.abs_index)


def print_corpus(corpus):

    for sent, toks in corpus.items():
        print(sent)
        for token in toks:
            if token.misc == '_':
                token.misc = ''
            token.print_token()
        print('')


def main():

    # beolvassa a conll-t
    corpus = read_file()

    # berakja a kívánt adatszerkezetbe
    anacorp = actor_features(corpus)

    # pléh-radics algoritmus
    plehradics(corpus, anacorp)

    # kiirja
    print_corpus(corpus)


if __name__ == "__main__":
    main()