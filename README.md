# KorKor Pilotcorpus

KorKor is a multi-layered, manually annotated Hungarian corpus. Besides the traditional annotation layers (tokenization, morphological tags, disambiguation, lemmatization, dependency relations) it contains anaphora and coreference annotation as well.

## Size

The corpus is divided into two subcorpora. The first group of the files contains all layers of annotations, but a smaller part lacks of certain annotation layers (zero verbs and pronouns, anaphora and coreference relations).

|                                                               | document | token (xtsv) | token (conllup) |
|:--------------------------------------------------------------|---------:|-------------:|----------------:|
| coreference annotated                                         |       94 |        26581 |           25944 |
| dependency annotation corrected                               |       26 |         8604 |            8674 |

In xtsv files punctuation marks, zero verbs and pronouns count as separate tokens.
In conllup files punctuation marks count as separate tokens.
For the description of the two file formats see [Formats](#Formats).

### Split

Coreference annotated data are split to development and test datasets in a proportion of 80%-10%-10%.

|             |  xtsv | conllup |
|:------------|------:|--------:|
| train       | 21100 |   20580 |
| development |  2709 |    2648 |
| test        |  2772 |    2716 |


## Sources

The text are from the collection of [OPUS](http://opus.nlpl.eu/). Two sources were used: Hungarian Wikipedia and the Hungarian translation of [GlobalVoices news website](https://hu.globalvoices.org). KorKor inherits the licence of the original sources. In the texts the spelling is manually corrected. 

The length of the texts is between 5 and 27 sentences, the length of the sentences is between 3 and 71 tokens (punctuation marks count as separate tokens).

The number of texts of the two sources and in the two phases of the corpus:

|               | coreference | dependency |
|:--------------|------------:|-----------:|
| Global Voices |          32 |          3 |
| Wikipédia     |           6 |         23 |

## Annotation

### Tokenization

emToken module of [emtsv](https://github.com/dlt-rilmta/emtsv) tokenized the tests. The output is in xtsv format described above.

### Morphological Analysis

emMorph module of [emtsv](https://github.com/dlt-rilmta/emtsv) provided the morphological analyses of the tokens. The output contains all possible tags and lemmata is JSON in the column of **anas**.

### Disambiguation and Lemmatization

Disambiguation and lemmatization were done by emTag module of [emtsv](https://github.com/dlt-rilmta/emtsv). The output follows [emMorph tagset](https://e-magyar.hu/en/textmodules/emmorph_codelist) containing the POS tag, derivational and inflectional features in the columns of **xpostag** and **lemma**.

### Converting POS and morphological Features

emMorph tags were converted to [Universal Dependencies](https://universaldependencies.org) by emmorph2ud module of [emtsv](https://github.com/dlt-rilmta/emtsv).  The output gives the UD POS and inflectional features in the columns ** upostag** and **feats**.

Find some further information about Hungarian morphological tagsets [here](https://github.com/dlt-rilmta/panmorph)

### Dependency Relations

emDep module of [emtsv](https://github.com/dlt-rilmta/emtsv) gave the dependency relations. The output takes the columns of **id**, **head** and **deprel** representing the index of the token in the sentence, the index of its mother node and the type of the dependency relation between them.

There are some differences between the original tagset of emDep and the tagset used in the corpus:
 * the type of the dependency relation between the possessor and the possessum is **POSS** (instead of **ATT**)
 * all preverbs connect with relation type **PREVERB** (not only the preverb *meg*)

### Zero Verbs

Zero verbs (zero copulas and ellipted verbs) were inserted manually. Zero substantives were inserted into the sentences where they would appear if the sentence were in past tense. The got a combined index derived from the index of the token preceding the inserted zero verb.

> A sorozat főhőse Papyrus ∅<sub>van</sub>, aki egy ifjú halászlegény ∅<sub>van</sub>.
>
> *The hero of the series is Papyrus, who is a young fisherman.*

Ellipted verbs are inserted into the sentence where they would appear and they got a combined index similarly to the zero substantives.

> Öccse miniszteri posztot vállalt, majd elnöki pozíciót ∅<sub>vállalt</sub>.
>
> *His brother assumed a ministerial position, then presidential one.*

### Zero Pronouns

Zero pronouns are inserted by a script, [emZero](https://github.com/vadno/emzero), which can be used as a module of [emtsv](https://github.com/dlt-rilmta/emtsv).

The rule-based script inserts a pronoun in the following cases:
* a subject for the finite verb if it does not have an overt one
* an object for the definite verb if it does not have an overt one
* a possessor for a possessum, if it does not have an overt one
* a subject for the infinitive verb

The person and number of the zero preverbs are calculated from their mother node and they are inserted into the dependency tree as well.
The zero subject is inserted after the verb, the zero bjects after the verb (and the zero subject) and the zero possessors after the possessum and they got an index combined from the id of the preceding token and the syntactic role of the zero preverb (SUBJ, OBJ, POSS).

### Anaphora and Coreference

Anaphoric relations are inserted by a rule-based script that searches the antecedent only of personal pronouns. Antecedents of other pronouns were inserted fully manually. The columns of **corefhead** and **coreftype** contains the index of the antecedent and the type of the anaproha or the coreference relation.

The following types of pronoun are annotated:

| type of the pronoun | abbreviation | frequency |
|:--------------------|:-------------|----------:|
| personal            | **prs**      |      1306 |
| demonstrative       | **dem**      |       121 |
| reciprocal          | **recip**    |        10 |
| reflexive           | **refl**     |        16 |
| relative            | **rel**      |       294 |
| possessive          | **poss**     |         0 |
| general             | **arb**      |       274 |
| speaker             | **speak**    |         4 |
| addressee           | **addr**     |         1 |

It is not obligatory to types of **arb**, **speak** and **addr** to have an antecedent, in these cases the column of **corefhead** remain empty, in all other cases it is filled.

The following coreference types are annotated:

| types of coreference | abbreviation | frequency |
|:---------------------|:-------------|----------:|
| coreference          | **coref**    |      1365 |
| part-whole relation  | **holo**     |       180 |

The tag **coref** is for the relation tpye when the two elements have identical reference (e.g.~in the case of repetition, synonym, hiper- and hyponym).

# Formats
The corpus is available in two formats.

## `xtsv`
The files follow the format of [xtsv](https://github.com/nytud/xtsv) with the following columns:
* id (word index)
* form  (word form)
* lemma
* xpostag (Hungarian-specific POS-tag in the tagset of [emMorph](https://e-magyar.hu/en/textmodules/emmorph_codelist))
* upostag (UD POS-tag)
* feats (UD feats)
* deprel (UD relation type to the HEAD)
* head (head of the current word)
* sent_id (sentence index)
* corefhead (index of the antecedent or coreferent element)
* coreftype (anaphora or coreference type)

In the case of the files in folder [dependency](korkor/xtsv/dependency)  the last three columns are missing.

## `CoNLL-U Plus`
The files follow the format of [CoNLL-U Plus](https://universaldependencies.org/ext-format.html) with the following columns:
* ID (word index)
* FORM (word form)
* LEMMA
* XPOS (Hungarian-specific POS-tag in the tagset of [emMorph](https://e-magyar.hu/en/textmodules/emmorph_codelist))
* UPOS (UD POS-tag)
* FEATS (UD feats)
* DEPREL (UD relation type to the HEAD)
* HEAD (head of the current word)
* COREFHEAD (index of the antecedent or coreferent element)
* COREFTYPE (anaphora or coreference type)
* ZERO_SUBJ (YES if the subject of the verb is dropped)
* ZERO_OBJ (YES if the object of the verb is dropped)
* ZERO_POSS  (YES if the possessor of the possessum is dropped)

In the case of the files in folder [dependency](korkor/conllup/dependency) the last five columns are unfilled.

# Further Annotations
The files in [korkor/xtsv/coreference_with_ud_dependency](korkor/xtsv/coreference_with_ud_dependency) are parsed with [UDPipe](https://github.com/ufal/udpipe) dependency parser used in [emtsv](https://github.com/nytud/emtsv). Note that the output of the dependency parser is not checked manually! Enhanced UD graphs for zero elements are still missing for now.
In the last column coreference clusters are annotated on the basis of coreference annotation.

# Licence
The resource is available under [CC-BY-4.0](LICENSE).

# Citation

If you use this resourse, please cite these papers:

Vadász Noémi (2020): [KorKorpusz: kézzel annotált, többrétegű pilotkorpusz építése](https://www.academia.edu/41798860/KorKorpusz_k%C3%A9zzel_annot%C3%A1lt_t%C3%B6bbr%C3%A9teg%C5%B1_pilotkorpusz_%C3%A9p%C3%ADt%C3%A9se). Berend Gábor, Gosztolya Gábor, Vincze Veronika (szerk.): XVI. Magyar Számítógépes Nyelvészeti Konferencia (MSZNY 2020). Szegedi Tudományegyetem, TTIK, Informatikai Intézet, Szeged. 141-154.

```
@inproceedings{korkor_mszny,
    author = {Vadász, Noémi},
    title = {{K}or{K}orpusz: kézzel annotált, többrétegű pilotkorpusz építése},
    booktitle = {{XVI}. {M}agyar {S}zámítógépes {N}yelvészeti {K}onferencia ({MSZNY} 2020)},
    editor = {Berend, Gábor and Gosztolya, Gábor and Vincze, Veronika},
    pages = {141--154},
    publisher = {Szegedi Tudományegyetem, TTIK, Informatikai Intézet},
    address = {Szeged},
    year = {2020}
}
```

Noémi Vadász (2022): [Building a Manually Annotated Hungarian Coreference Corpus: Workflow and Tools](https://aclanthology.org/2022.crac-1.5/). Proceedings of the Fifth Workshop on Computational Models of Reference, Anaphora and Coreference. Association for Computational Linguistics, Gyeongju, Republic of Korea. 38-47.

```
@inproceedings{korkor_coling,
    title = "Building a Manually Annotated {H}ungarian Coreference Corpus: Workflow and Tools",
    author = "Vad{\'a}sz, No{\'e}mi",
    booktitle = "Proceedings of the Fifth Workshop on Computational Models of Reference, Anaphora and Coreference",
    month = oct,
    year = "2022",
    address = "Gyeongju, Republic of Korea",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2022.crac-1.5",
    pages = "38--47"
}
```

References for emtsv and its modules can be found [here](references.bib).
