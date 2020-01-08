# KorKor pilotkorpusz

A KorKorpusz egy többrétegű, kézzel ellenőrzött minőségi magyar nyelvű korpusz. Az alapvető nyelvi annotációk (tokenizálás, morfológiai elemzés, egyértelműsítés, tövesítés, függőségi mondatelemzés) mellett anafora- és koreferenciaannotációt is tartalmaz.

## méret

A korpusz két alkorpuszra osztható aszerint, hogy az annotálás melyik fázisában tart. A korpusz nagyobbik alkorpusza az összes annotációs szintet tartalmazza, a kisebbik alkorpusza bizonyos annotációs szinteket (testetlen igék és testetlen névmások, anaforikus kapcsolatok, koreferenciakapcsolatok) egyelőre nem tartalmaz.

| | dokumentum        | mondat           | token  |
|:----------| -------------:|-------------:| -----:|
|koreferencia annotálva | 95     | 1436 | 31492 |
|függőségi ellenőrizve (7. lépés)|  26     | kb. 460 | kb. 8800 |

A tokenszámba a kézzel ellenőrzött függőségi elemzés szintjéig kész részkorpusz esetében az írásjelek, a koreferenciakapcsolatokkal annotált részkorpusz esetében az írásjelek, a testetlen igék és a testetlen névmások is beleszámítanak.

## szövegek

A szövegek az [OPUS gyűjteményéből](http://opus.nlpl.eu/) származnak. Egy részük a magyar Wikipédiáról származik, másrészt a [GlobalVoices hírportál](https://hu.globalvoices.org) magyar nyelvre lefordított hírei közül. A KorKorpusz örökli ezeknek a forrásoknak a nyílt hozzáférhetőségét. A szövegek helyesírása kézzel ellenőrizve lett.

A szövegek hossza 5 és 27 mondat között, a mondatok hossza 3 és 71 token között van (az írásjeleket külön tokennek számolva).

| | koreferencia        | függőségi           |
|:----------| -------------:|-------------:|
| Global Voices |   32  |  3 |
| Wikipédia |   63   |  23 |

## formátum

A korpusz fájlonként egy domunemtumból áll. A dokumentumok formátuma az [xtsv](https://github.com/dlt-rilmta/xtsv) formátumát követi, ami egy fejléces tsv fájl jelent. Soronként egy tokent tartalmaz, a mondatokat üres sor választja el. A nyelvi annotációk TAB karakterrel elválasztott oszlopokban kapnak helyet. Az oszlopok sorrendje nem kötöttt, sorrendjüket a fejléc határozza meg.

A korpuszfájlok a következő elemzéseket tartalmazzák (zárójelben az xtsv-ben megfelelő oszlopnevekkel):

* token (form)
* lehetséges morfológiai elemzések (anas)
* egyértelműsített tő (lemma)
* egyértelműsített morfológiai elemzés, emMorph címkekészlet (xpostag)
* konvertált szófaj (upos)
* konvertált inflexiós jegyek (feats)
* index, mondatbeli sorszám (id)
* függőségi kapcsolat típusa (deprel)
* anyacsomópont mondatbeli sorszáma (head)
* előzmény mondatbeli sorszáma (corefhead)
* anafora- vagy koreferenciakapcsolat típusa (coreftype)

## annotáció

### tokenizálás

A tokenizálást az [emtsv](https://github.com/dlt-rilmta/emtsv) emToken modulja végzi. Kimenete a fent ismertetett xtsv formátumú korpuszfájl.

### morfológiai elemzés

A morfológiai elemzést az [emtsv](https://github.com/dlt-rilmta/emtsv) emMorph modulja végzi. Kimenete az összes lehetséges morfológiai elemzést és a hozzájuk tartozó tövet tároló JSON az **anas** oszlopban.

### egyértelműsítés és tövesítés

Az egyértelműsítést és a tövesítést az [emtsv](https://github.com/dlt-rilmta/emtsv) emTag modulja végzi. Kimenete az [emMorph címkekészletében](http://e-magyar.hu/hu/textmodules/emmorph_codelist) megfogalmazott, szófajt, derivációt és inflexiós jegyeket tartalmazó morfológiai címke és a hozzá tartozó tő.

### konvertált szófaj és inflexiós jegyek

Az emMorph címkét a [Universal Dependencies](https://universaldependencies.org) kereteiben meghatározott, magyarra adaptált címkekészletre az [emtsv](https://github.com/dlt-rilmta/emtsv) emmorph2ud konvertálja.

A címkekészletekről bővebben [itt](https://github.com/dlt-rilmta/panmorph) lehet tájékozódni.

### függőségi elemzés

A függőségi elemzést az [emtsv](https://github.com/dlt-rilmta/emtsv) emDep modulja végzi. A KorKor annotációja a függőségi elemző címkekészletéhez képest eltéréseket tartalmaz:
 * a birtokos és a birtok között fennálló függőségi kapcsolat típusa **POSS**
 * a *meg* igekötőn kívül minden igekötő **PREVERB** típussal kapcsolódik az igéhez 
 
 A függőségi kapcsolatok címkekészletével kapcsolatban [az annotációs útmutatóból](utmutatok/emdep_checker_guide.pdf) lehet tájékozódni.

### testetlen igék

A testetlen igék (zérókopulák és elliptált igék) kézzel lettek beillesztve. A zéró létigék új tokenként kerülnek a fájlba arra a helyre, ahol múlt időben testes létigeként jelennének meg, saját kombinált indexet kapnak, ami a zéró létigét megelőző elem mondatbeli sorszámából képződik.

> A sorozat főhőse Papyrus ∅<sub>van</sub>, aki egy ifjú halászlegény ∅<sub>van</sub>.

Az elliptált igék a mondatban arra a helyre vannak beillesztve, ahol testes igeként megjelennének, valamint a zéró létigéhez hasonló, kombinált indexet kapnak.

> Öccse miniszteri posztot vállalt, majd elnöki pozíciót ∅<sub>vállalt</sub>.

A testetlen igék beillesztésével kapcsolatban [az annotációs útmutatóból](utmutatok/zero_verb_guide.pdf) lehet tájékozódni.

### testetlen névmások

A testetlen névmásokat egy saját szkript illeszti be, amely az [emtsv](https://github.com/dlt-rilmta/emtsv) keretrendszerében önálló modulként (emZero) is használható. A szabályalapú program a következő helyekre illeszt be névmást:
* finit ige alanyának, ha annak nem volt testes alanya
* határozott ragozású finit ige tárgyának, ha annak nem volt testes tárgya
* birtok birtokosának, ha annak nem volt testes birtokosa
* ragozott és ragozatlan infinitívusz alanyának

A testetlen névmások esetében az alany az ige után, a tárgy az ige (és a testetlen alany) után, a birtokos pedig a birtok után kerül és egy kombinált ID-t kap, ami az őt megelőző elem ID-jéből és a zéró elem szintaktikai szerepének rövidítéséből (SUBJ, OBJ, POSS) áll.

### anaforikus kapcsolatok

Az anaforikus kapcsolatokat egy saját szkript illeszti be. A szabályalapú program csak a személyes névmások előzményét keresi a szövegben, a többi névmástípus előzményét kézzel kell beilleszteni. A következő névmástípusok vannak jelölve a korpuszban (zárójelben az előfordulásukkal):

| névmástípus | jelölés a korpuszban  | előfordulás  |
|:----------| :-------------|-------------:|
| személyes | **prs** | 1497 |
| mutató | **dem** | 147 |
| kölcsönös | **recip** | 11 |
| visszaható | **refl** | 18 |
| birtokos | **poss** | 0 |
| általános | **arb** | 316 |
| beszélő| **speak** | 5 |
| címzett | **addr** | 1 |

Az anaforikus kapcsolatok címkekészletével kapcsolatban [az annotációs útmutatóból](utmutatok/koref_annot_guide.pdf) lehet tájékozódni.

### koreferenciakapcsolatok

A koreferenciakapcsolatokat kézzel kell beilleszteni.  A következő koreferenciatípusok vannak jelölve a korpuszban (zárójelben az előfordulásukkal):

| koreferenciatípus | jelölés a korpuszban  | előfordulás  |
|:----------| :-------------|-------------:|
| koreferencia | **coref** | 1582 |
| rész-egész kapcsolat | **holo** | 202 |

# Licensz
Az erőforrás [CC-BY-4.0](LICENSE) licensz alatt használható.

# Hivatkozások

Ha használod a korpuszt, kérlek, hivatkozz az alábbi cikkre:

```
@misc{korkor,
  author = {Vadász, Noémi},
  title = {{K}or{K}orpusz: kézzel annotált, többrétegű pilotkorpusz építése},
  note = {megjelenés alatt}
  year = {2020},
}
```

Az emtsv-vel és annak moduljaival kapcsolatos hivatkozásokat lásd a [hivatkozások](hivatkozasok.bib) között.
