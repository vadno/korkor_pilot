Ebben a lépésben a névmási anaforikus kapcsolatokat egy szabályalapú szkript szúrja be. A program megkeresi a névmásokat, majd a mondatban szereplő többi szó szófaji, morfológiai és szintaktikai információira támaszkodva egyszerű szabályok alapján dönt.

A szkript jelenleg csak a személyes névmások előzményét keresi meg, a többi típust kézzel kell beilleszteni. Az algoritmus az alany antecedensének keresésekor például az alábbihoz hasonló szabályok alapján dönt.

A zérónévmásbeszúrást végző szkript: [anafora.py](../../szkriptek/anafora.py)

A lépés bemenete: [9_pro_beszuro/globv_10.conll](../9_pro_beszuro/globv_10.conll)