#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    author: Noémi Vadász
    last update: 2020.01.17.

"""

from collections import defaultdict
from collections import namedtuple
import sys
import csv


PRON_PERSNUM = {('Sing', '1'): 'én',
                ('Sing', '2'): 'te',
                ('Sing', '3'): 'ő/az',
                ('Plur', '1'): 'mi',
                ('Plur', '2'): 'ti',
                ('Plur', '3'): 'ők/azok',
                ('X', 'X'): 'X'}

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
        self.abs_index = None       # saját tokenszámláló
        self.deps = None
        self.misc = None

    def print_token(self):
        print('\t'.join([self.id, self.form, self.lemma, self.upos, self.xpos, self.feats, self.head, self.deprel,
                         self.deps, self.misc]))


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

    return dict(feat.split('=', maxsplit=1) for feat in feats.split('|') if feats != '_')


def pro_default_features(dropped):
    """
    a droppolt nevmas alapjegyeit allitja be
    :param dropped: a droppolt actor adatszerkezete
    :return:
    """

    dropped.form = 'DROP'
    dropped.upos = 'PRON'
    dropped.feats = dict()
    if dropped.deprel == 'SUBJ':
        dropped.feats['Case'] = 'Nom'
    elif dropped.deprel == 'OBJ':
        dropped.feats['Case'] = 'Acc'
    elif dropped.deprel == 'POSS':
        dropped.feats['Case'] = 'Gen'
    dropped.feats['PronType'] = 'Prs'
    dropped.deps = '_'
    dropped.misc = '_'


def pro_calc_features(head, role):
    """
    a droppolt névmás jegyeit nyeri ki a fejből (annak UD jegyeiből)
    :param head:
    :param role:
    :return:
    """

    pro = Word()
    pro.id = head.id + '.' + role
    pro.sent_nr = head.sent_nr
    pro.abs_index = head.abs_index
    pro.deprel = role
    pro.head = head.id
    pro_default_features(pro)

    if role == 'OBJ':
        pro.feats['Number'] = 'Sing'

        if head.feats['Definite'] == '2':
            pro.feats['Person'] = '2'
        else:
            pro.feats['Person'] = '3'

    elif role == 'SUBJ':
        if 'VerbForm' in head.feats:
            if head.feats['VerbForm'] == 'Fin':
                pro.feats['Person'] = head.feats['Person']
                pro.feats['Number'] = head.feats['Number']

            elif head.feats['VerbForm'] == 'Inf':
                if 'Person' in head.feats:
                    pro.feats['Person'] = head.feats['Person']
                    pro.feats['Number'] = head.feats['Number']
                else:
                    pro.feats['Person'] = 'X'
                    pro.feats['Number'] = 'X'

    else:
        pro.feats['Person'] = head.feats['Person[psor]']
        pro.feats['Number'] = head.feats['Number[psor]']

    pro.xpos = 'PRON'
    pro.lemma = PRON_PERSNUM[(pro.feats['Number'], pro.feats['Person'])]
    pro.feats = '|'.join(feat + '=' + pro.feats[feat] for feat in sorted(pro.feats, key=str.lower))
    pro.anas = '[]'

    return pro


def actor_features(corpus):
    """

    :return:
    """

    actor_list = []  # actorlista: mondatok listaja, kulcs az ige, ertek a vonzatok listaja

    for sent in corpus:

        deps = []
        for head in sent.toks:   # head
            for dep in sent.toks:
                if dep.head == head.id:
                    deps.append((head, dep))

            if head.upos in VERBS and head not in deps:
                deps.append((head, head))

        # egy elemhez hozzarendeli az osszes ramutato fuggosegi viszonyt
        # egy headhez az osszes depot
        deps_dict = {}
        for a, b in deps:
            deps_dict.setdefault(a, []).append(b)

        for head in deps_dict:

            if head.upos in VERBS:

                verb = Word()
                base_features(verb, head)
                verb.feats = parse_udfeats(verb.feats)

                actors = defaultdict(list)
                actors[verb] = []

                for dep in deps_dict[head]:
                    if dep.deprel in ARGUMENTS:

                        actor = Word()
                        base_features(actor, dep)
                        actor.feats = parse_udfeats(actor.feats)

                        actor.sent_nr = verb.sent_nr

                        if 'Number[psor]' in actor.feats:

                            for ifposs in sent.toks:
                                if ifposs.head == dep.id and ifposs.deprel == 'POSS'\
                                        and ifposs.upos in NOMINALS:
                                    ifposs.upos = 'POSS'

                                    newactor = Word()
                                    base_features(newactor, ifposs)
                                    newactor.feats = parse_udfeats(ifposs.feats)

                                    actors[verb].append(newactor)

                        actors[verb].append(actor)

                actor_list.append(actors)

    return actor_list


def remove_dropped(head, deps, role):
    """
    kitorli a actors kozul azokat a droppolt alanyokat, targyakat, amikhez van testes
    :param? head:
    :param deps: az aktualis ige vonzatai
    :param role: szerep
    :return:
    """

    if any(actor.head == head and actor.deprel == role and actor.form != 'DROP' for actor in deps):
        deps = [actor for actor in deps if actor.head != head or actor.deprel != role or actor.form != 'DROP']

    return deps


def insert_pro(actorlist):
    """
    letrehoz droppolt alanyt, targyat
    alanyt: minden igenek
    targyat: csak a definit ragozasu igeknek
    :param actorlist: a actors adatszerkezete
    :return:
    """

    for actors in actorlist:

        for verb in actors.keys():

            subj = pro_calc_features(verb, 'SUBJ')
            actors[verb].append(subj)
            actors[verb] = remove_dropped(verb.id, actors[verb], 'SUBJ')

            if 'Definite' in verb.feats and verb.feats['Definite'] in {'Def', '2'} \
                    and not any(actor.deprel == 'INF' for actor in actors[verb]):
                obj = pro_calc_features(verb, 'OBJ')
                actors[verb].append(obj)
                actors[verb] = remove_dropped(verb.id, actors[verb], 'OBJ')

            for actor in actors[verb]:
                if 'Number[psor]' in actor.feats:
                    poss = pro_calc_features(actor, 'POSS')
                    actors[verb].append(poss)
                    actors[verb] = remove_dropped(actor.id, actors[verb], 'POSS')


def print_pro(token, actors):

    for sent in actors:
        for key, value in sent.items():
            for dep in value:
                if dep.abs_index == token.abs_index:
                    if dep.form == 'DROP':
                        dep.print_token()


def print_corpus(actors, corpus):

    for sentence in corpus:
        print(sentence.orig)
        for token in sentence.toks:
            token.print_token()
            print_pro(token, actors)
        print('')


def parse_fields(token, line):

    for field in CONLLU:
        setattr(token, field, line[CONLLU.index(field)])


def read_file():

    corp = list()

    abs_counter = 0
    counter = 0

    reader = csv.reader(iter(sys.stdin.readline, ''), delimiter='\t', quoting=csv.QUOTE_NONE)

    Sentence = namedtuple('Sentence', ['orig', 'toks'])
    orig = ''
    sent = list()

    for line in reader:

        if len(line) > 1 and '#' not in line[0]:
            abs_counter += 1

            if line:
                token = Word()
                parse_fields(token, line)
                token.sent_nr = str(counter)
                token.abs_index = str(abs_counter)

                sent.append(token)

        elif len(line) == 1 and line[0].startswith('#'):
            orig = line[0]

        else:
            counter += 1
            corp.append(Sentence(orig, sent))
            sent = list()

    return corp


def main():

    # beolvassa a conll-t
    corpus = read_file()

    # berakja a kivant adatszerkezetbe
    actors = actor_features(corpus)

    # letrehozza a droppolt alanyokat, targyakat, birtokosokat, majd torli a foloslegeseket
    insert_pro(actors)

    # kiirja
    print_corpus(actors, corpus)


if __name__ == "__main__":
    main()
