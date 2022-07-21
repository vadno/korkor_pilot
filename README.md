# KorKor Pilotcorpus

KorKor is a multi-layered, manually annotated Hungarian corpus. Besides the traditional annotation layers (tokenization, morphological tags, disambiguation, lemmatization, dependency relations) it contains anaphora and coreference annotation as well.

## Size

The corpus is divided into to subcorpora. The first group of the files contains all layers of annotations, but a smaller part lacks of certain annotation layers (zero verbs and pronouns, anaphora and coreference relations).

|                                                               |              document |          sentence | token  |
|:--------------------------------------------------------------|----------------------:|------------------:| -----:|
| coreference annotated                                         |                    95 |              1436 | 31492 |
| dependency annotation corrected                               |                    26 |               463 | 8853 |

Punctuation marks, zero verbs and pronouns count as separate tokens.

## Sources

The text are from the collection of [OPUS](http://opus.nlpl.eu/). Two sources were used: Hungarian Wikipedia and the Hungarian translation of [GlobalVoices news website](https://hu.globalvoices.org). KorKor inherits the licence of the original sources. In the texts the spelling is manually corrected. 

The length of the texts is between 5 and 27 sentences, the length of the sentences is between 3 and 71 tokens (punctuation marks count as separate tokens).

The number of texts of the two sources and in the two phases of the corpus:

| |                coreference |             dependency |
|:----------|---------------------------:|-----------------------:|
| Global Voices |                         32 |                      3 |
| Wikipédia |                         63 |                     23 |

## Format

The corpus consists of files containing the documents. The files are in [xtsv](https://github.com/dlt-rilmta/xtsv) format which is a format of tab spearated file with a header. The file has one token per line, the sentences are separated with an empty line. Linguistic annotations are in columns separated by TAB characters. The order of the columns are not fixed, their order is defined in the header.

The files contains the following linguistic annotation layers (with the corresponding names in the xtsv header in the brackets)

* token (form)
* possible morphological tags (anas)
* disambiguated lemma (lemma)
* disambiguated morphological tag (xpostag)
* UD POS-tag (upostag)
* UD features (feats)
* token id in the sentence (id)
* head id in the sentence (head)
* type of the dependency relation (deprel)
* id of the antecedent in the sentence (corefhead)
* type of the anaphora or coreference relation (coreftype)

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
 * all preverbs connects with relation type **PREVERB** (not only the preverb *meg*)

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
| personal            | **prs**      |      1497 |
| demonstrative       | **dem**      |       147 |
| reciprocal          | **recip**    |        11 |
| reflexive           | **refl**     |        18 |
| relative            | **rel**      | TODO |
| possessive          | **poss**     |         0 |
| general             | **arb**      |       316 |
| speaker             | **speak**    |         5 |
| addressee           | **addr**     |         1 |

It is not obligatory to types of **arb**, **speak** and **addr** to have an antecedent, in these cases the column of **corefhead** remain empty, in all other cases it is filled.

The following coreference types are annotated:

| types of coreference | abbreviation  | frequency |
|:---------------------| :-------------|----------:|
| coreference          | **coref** |      1582 |
| part-whole relation  | **holo** |       202 |

The tag **coref** is for the relation tpye when the two elements have identical reference (e.g.~in the case of repetition, synonym, hiper- and hyponym).

# Licence
The resource is available under [CC-BY-4.0](LICENSE).

# Citation

If you use this resourse, please cite our paper:

```
@inproceedings{korkor,
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

References for emtsv and its modules can be found [here](references.bib).
