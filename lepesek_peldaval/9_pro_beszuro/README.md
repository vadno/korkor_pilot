Ebben a lépésben egy szkript illeszti be a zérónévmásokat a fájlokba. Egyszerű szabályok mentén végzi az elemek beillesztését és a szabályok alkalmazása a során kölönböző elemzési rétegek tartalmára támaszkodik (tő, morfológiai címke, függőségi elemzés).

A program a következő helyekre illeszt be zérónévmást:

+ finit ige alanyának, ha annak nem volt testes alanya
+ határozott ragozású finit ige tárgyának, ha annak nem volt testes tárgya
+ birtok birtokosának, ha annak nem volt testes birtokosa
+ ragozott és ragozatlan infinitívusz alanyának

A zérónévmások beillesztése után a mondatfában plusz ágak jelennek meg. A zéró elemek is saját ID-t kapnak, a fájlba pedig az alany az ige után, a tárgy az ige (és a zéró alany) után, a birtokos pedig a birtok után kerül és egy kombinált ID-t kap, ami az őt megelőző elem ID-jéből és a zéró elem szintaktikai szerepének rövidítéséből (SUBJ, OBJ, POSS) áll. A zéró elemek szófaja névmás (PRON), a morfológiai jegyeik között pedig az ige vagy a birtok alapján kiszámolható szám és személy jegyek jelenhetnek meg.

A zérónévmásbeszúrást végző szkript: [pro.py](../../szkriptek/pro.py)

A lépés bemenete: [8_zeroige_kezi/globv_10.conll](../8_zeroige_kezi/globv_10.conll)
