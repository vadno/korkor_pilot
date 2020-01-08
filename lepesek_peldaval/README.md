Az alábbiakban végigkövethető a korpuszépítés összes lépése egy példafájl segítségével. Az egyes lépések alatt olvasható a ki- és bemenet formátuma valamint a lépéshez használt eszköz. Bizonyos lépésekhez az [emtsv](https://github.com/dlt-rilmta/emtsv) modulait használjuk, másokhoz az [itt](../szkriptek) található szkripteket. A használatukat lásd alább, az egyes lépések rövid ismertetésénél.

1. elemzés az emtsv-vel
   Az elemzett fájl előállításához az [emtsv](https://github.com/dlt-rilmta/emtsv) moduláris elemzőeszközt használjuk a következő modulok működtetésével:

   1. tokenizálás: emtoken (tok)
   1. morfológiai elemzés és tövesítés: emmorph (morph)
   1. egyértelműsítés: emtag (pos)

   A modulok egyesével is megadhatók, de a `tok-pos` preset is ugyanezeket a modulokat működteti. Az emtsv használatával kapcsolatban a részleteket lásd [itt](https://github.com/dlt-rilmta/emtsv)!

   bemenet: folyószöveg [0_pelda_raw/globv_10.txt](0_pelda_raw/globv_10.txt)   
   kimenet: xtsv  
    
2. fájl előkészítése a kézi ellenőrzésre
   Ebben a lépésben az [emtsv](https://github.com/dlt-rilmta/emtsv) elemzővel előelemzett fájlt készítjük elő a kézi annotálásra. Az elemző kimenetét olyan formára kell hozni, hogy azt egy előre elkészített, feltételes formázásokat tartalmazó Google Spreadsheets dokumentumba importálhassuk.

   A preprocesszálást végző szkript: [tag_preproc.py](../szkriptek/tag_preproc.py)  
   bemenet: xtsv  [1_emtsv/globv_10.xtsv](1_emtsv/globv_10.xtsv)  
   kimenet: tsv a google spreadsheetshez  
    
3. kézi javítás a google spreadsheetsben  
   Ebben a lépésben történik a tokenizálás és az egyértelműsítés kimenetének kézi ellenőrzése és javítása. Ehhez egy Google Spreadsheets táblázatot használunk.

   A szöveg minden egyes tokenjéhez az emtag egyértelműsítő modul által megadott elemzés alá felsorakozik az adott token összes szóbajöhető elemzése, amelyeket az emmorph morfológiai elemző és tövesítő modulja ad. Az annotátor feladata eldönteni, hogy az egyértelműsítés kimenete helyes-e, ha nem, akkor a lehetséges elemzések közül melyik helyes, valamint ha egyik se helyes, akkor be kell vinnie a helyes elemzést és tövet. A felületen a tokenizálás javítására is lehetőség van. A részleteket lásd az [annotálási útmutatóban](../utmutatok/emmorph_checker_guide.pdf)!

   Az üres táblázatfájl az annotáláshoz: [emtag.xlsx](../google_spreadsheets_fajlok/emtag.xlsx)

   Az üres táblázatfájl Microsoft Excelben és Libre Office-ban is használható, de Google Spreadsheets-be is importálható, így a munka kollaboratívan is végezhető.

   bemenet: tsv, fájl a feltételes formázásokkal, importálás  [2_google_preproc/globv_10.tsv](2_google_preproc/globv_10.tsv)  
   kimenet: exportált csv  
    
4. a google spreadsheetsből nyert fájl feldolgozása

   Ebben a lépésben a kézzel ellenőrzött és javított, csv-ként exportált fájlt dolgozzuk fel és készítjük elő a következő lépés, a függőségi elemző számára. A szkript az annotátor által megjelölt vagy beírt helyes címkét és tövet veszi figyelembe. Emellett a tokenizálási hibák javítására kézzel beírt parancsokat az exportált fájl feldolgozásakor automatikusan értelmezi és azoknak megfelelően módosítja a tokenizálást (sort töröl vagy sort szúr be az annotátor által megadott tartalommal). Emellett formátumkonverzió is történik, amikor a fájlt az emtsv saját formátumára alakítjuk. A kézi javítás után a szöveg tehát pontosan ugyanúgy néz ki, mint javítás előtt (az 1_emtsv lépés után), különbség az egyes mezők tartalmában van.

   A posztprocesszálást végző szkript: [tag_postproc.py](../szkriptek/tag_postproc.py)

   bemenet: csv  [3_google_kezi/globv_10.csv](3_google_kezi/globv_10.csv)  
   kimenet: xtsv
    
5. elemzés az emtsv-vel

   Az elemzett fájl előállításához az [emtsv](https://github.com/dlt-rilmta/emtsv) moduláris elemzőeszközt használtam a következő modulok működtetésével:

   1. címkekonverzió: emmorph2ud (conv-morph)
   1. függőségi elemzés: emdep (dep)
   1. formátumkonverzió: emconll (conll)

   Az emtsv használatával kapcsolatban a részleteket lásd [itt](https://github.com/dlt-rilmta/emtsv)!

   bemenet: xtsv  [4_google_posztproc/globv_10.xtsv](4_google_posztproc/globv_10.xtsv)  
   kimenet: conll-u
    
6. fájl előkészítése a webannóra
   Ebben a lépésben előkészítjük a fájt olyan formátumúra, hogy az megfeleljen a [WebAnno](https://webanno.github.io/webanno/) annotációs segédeszköz bemenetének. Az átalakítást egy rövid parancs végzi el:

   A lépés bemenete: 

    ```
    cat [file] | awk -F $'\t' ' { t = $4; $4 = $5; $5 = t; print; } ' OFS=$'\t'
   ```
   
   bemenet: conll-u  [5_emtsv/globv_10.conll](5_emtsv/globv_10.conll)  
   kimenet: conll-u a webannónak
    
7. kézi javítás a webannóban  
   Ebben a lépésben történik a függőségi elemzés kimenetének kézi ellenőrzése és javítása. Ehhez a [WebAnno](https://webanno.github.io/webanno/) webalapú annotációs segédeszközt használjuk.

   A CoNLL-U formátumú fájlok függőségi faként jelennek meg a felületen. Az egér segítségével megfordíthatók, áthelyezhetők vagy törölhetők az egyes függőségi élek, valamint a címkék is módosíthatók. Emellett a szóalakot, a tövet és a morfológiai címkét is lehetőségünk van módosítani. A tokenizálás módosítására nincs lehetőség. A részleteket lásd az [annotálási útmutatóban](../utmutatok/emdep_checker_guide.pdf)! Az annotátorok által összegyűjtött kérdésekből készült [gyik](../utmutatok/emdep_checker_fak.pdf) is segítséget nyújthat az kérdéses esetekben.

   bemenet: conll-u  [6_webanno_preproc/globv_10.conll](6_webanno_preproc/globv_10.conll)  
   kimenet: conll-u
    
8. zérólétigék, elliptált igék kézi beszúrása az annotatrixban  
   Ebben a lépésben az esetleges tokenizálási hibák javítása mellett a zéró létigék és az elliptált igék kézi beillesztése történik. Ehhez az [UD Annotatrix](https://github.com/jonorthwash/ud-annotatrix) eszközt használjuk, amely egy böngészőben használható eszköz függőségi fák vizualizációjára és szerkesztésére.

   A zéró létigék új tokenként kerülnek a fájlba arra a helyre, ahol múlt időben testes létigeként jelennének meg, saját kombinált indexet kapnak, ami a zéró létigét megelőző elem ID-jéből képződik. Az igei ellipsziseket is jelöltük a korpuszban, hiszen gyakran találkoztunk olyan tagmondatokkal, amelyekben az elliptált ige miatt nem lehetett megfelelő anyacsomóponthoz kötni az egyes bővítményeket. A zéró létigékhez hasonlóan kézzel illesztettük a mondatfába az elliptált finit igéket. Az elliptált ige a zéró létigéhez hasonló, kombinált indexet kapott.

   A részleteket lásd az [annotálási útmutatóban](../utmutatok/zero_verb_guide.pdf)!

   bemenet: conll-u  [7_webanno_kezi/globv_10.conll](7_webanno_kezi/globv_10.conll)  
   kimenet: conll-u

9. zérónévmások beszúrása  
   Ebben a lépésben egy szkript illeszti be a zérónévmásokat a fájlokba. Egyszerű szabályok mentén végzi az elemek beillesztését és a szabályok alkalmazása a során kölönböző elemzési rétegek tartalmára támaszkodik (tő, morfológiai címke, függőségi elemzés).

   A program a következő helyekre illeszt be zérónévmást:

   + finit ige alanyának, ha annak nem volt testes alanya
   + határozott ragozású finit ige tárgyának, ha annak nem volt testes tárgya
   + birtok birtokosának, ha annak nem volt testes birtokosa
   + ragozott és ragozatlan infinitívusz alanyának

   A zérónévmások beillesztése után a mondatfában plusz ágak jelennek meg. A zéró elemek is saját ID-t kapnak, a fájlba pedig az alany az ige után, a tárgy az ige (és a zéró alany) után, a birtokos pedig a birtok után kerül és egy kombinált ID-t kap, ami az őt megelőző elem ID-jéből és a zéró elem szintaktikai szerepének rövidítéséből (SUBJ, OBJ, POSS) áll. A zéró elemek szófaja névmás (PRON), a morfológiai jegyeik között pedig az ige vagy a birtok alapján kiszámolható szám és személy jegyek jelenhetnek meg.

   A zérónévmásbeszúrást végző szkript: [pro.py](../szkriptek/pro.py)
     
   bemenet: conll-u   [8_zeroige_kezi/globv_10.conll](8_zeroige_kezi/globv_10.conll)  
   kimenet: conll-u
    
10. anaforikus kapcsolatok beszúrása  
   Ebben a lépésben a névmási anaforikus kapcsolatokat egy szabályalapú szkript szúrja be. A program megkeresi a névmásokat, majd a mondatban szereplő többi szó szófaji, morfológiai és szintaktikai információira támaszkodva egyszerű szabályok alapján dönt.  
      A szkript jelenleg csak a személyes névmások előzményét keresi meg, a többi típust kézzel kell beilleszteni. Az algoritmus az alany antecedensének keresésekor például az alábbihoz hasonló szabályok alapján dönt.  
   
    A zérónévmásbeszúrást végző szkript: [anafora.py](../szkriptek/anafora.py)

    bemenet: conll-u  [9_pro_beszuro/globv_10.conll](9_pro_beszuro/globv_10.conll)  
   kimenet: conll-u
    
11. kézi javítás és koreferenciabeszúrás a google spreadsheetsben  
   Az automatikusan beillesztett zérónévmások és anaforikus kapcsolatok ellenőrzését, valamint a koreferenciakapcsolatok beillesztését egyfeltételes formázásokkal ellátott Google Spreadsheets táblázatban lehet elvégezni. Az anaforikus- és koreferenciakapcsolatokat két oszlopban kell jelölni, egyikben annak az elemnek az ID számát kellett megadni, amellyel a visszautaló elem kapcsolatban áll, a másikban pedig a kapcsolat típusát. A részleteket lásd az [annotálási útmutatóban](../utmutatok/koref_annot_guide.pdf)!  
   
      Az üres táblázatfájl az annotáláshoz: [koref.xlsx](../google_spreadsheets_fajlok/koref.xlsx)  
   
      Az üres táblázatfájl Microsoft Excelben és Libre Office-ban is használható, de Google Spreadsheets-be is importálható, így a munka kollaboratívan is végezhető.

      bemenet: tsv, fájl a feltételes formázásokkal, importálás [10_anafora_beszuro/globv_10.conll](10_anafora_beszuro/globv_10.conll)  
      kimenet: exportált tsv

12. a google spreadsheetsből nyert fájl feldolgozása  

    Ebben a lépésben a kézzel ellenőrzött és javított, tsv-ként exportált fájlt dolgozzuk fel. A szkript az annotátor által kijavított vagy beírt anaforikus és koreferenciakapcsolatokat veszi figyelembe. Ha az annotátor módosít a szóalakok, a tövön, a morfológiai címkén vagy a függőségi elemzésen, akkor az erre a javításra szolgáló cellák tartalmát is feldolgozza a szkript. Emellett formátumkonverzió is történik, amikor a fájlt ismét az emtsv saját formátumára alakítjuk.

    A posztprocesszálást végző szkript: [koref_postproc.py](../szkriptek/koref_postproc.py)

    bemenet: tsv  [11_google_kezi/globv_10.tsv](11_google_kezi/globv_10.tsv)  
   kimenet: xtsv
    
13. korpuszfájlok előállítása

    Ebben a lépésben a 6_webanno_prepoc lépésben levágott morfológiai elemzési réteg visszakerül a fájlba.

    A simítást végző szkriptek: [merge.py](../szkriptek/merge.py)

    A simításhoz használt fájl megegyezik a 4_googe_posztproc lépés kimeneteként kapott fájllal ([4_google_posztproc/globv_10.xtsv](4_google_posztproc/globv_10.xtsv)).

    bemenet: xtsv  [12_google_posztproc/globv_10.xtsv](12_google_posztproc/globv_10.xtsv)   
   kimenet: xtsv
