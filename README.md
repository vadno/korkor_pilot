+ előállítani a korpuszfájlokat
    - három szint
        * csak emTag javítva
        * csak emDep javítva
        * csak kofererencia annotálva
    - esetleg raw fájlok is, mert akkor még nem volt detokenizálás
    - formátum: xtsv
+ előkészíteni az annotálási útmutatókat, annotáló eszközök leírását
    - emTag javítás
        * útmutató
        * google felület, fájl a feltételes formázásokkal
        * preproc szkript
        * posztproc szkipt
        * leírás a folyamat lépéseiről
            + nyers szöveg preproc
            + google feltételes formázás fájlja
            + kézi javítás
            + exportálás csv
            + posztproc
    - emDep javítás
        * útmutató
        * webanno felület
        * preproc szkript
        * posztproc szkipt
        * leírás a folyamat lépéseiről
            + webanno használata, conll formátum
            + kézi javítás
            + exportálás conll
    - zérólétigék és elliptált igék beszúrása az elemzési fába
        * annotatrix [https://github.com/jonorthwash/ud-annotatrix]
        * leírás a zéróigék jelöléséről és beillesztésükről az elemzési fába
    - anafora és koreferencia
        * útmutató
        * google felület, fájl a feltételes formázásokkal
        * preproc szkript
        * posztproc szkipt (fájlok simítása az emTag kimenetével)
        * leírás a folyamat lépéseiről
            + conll preproc
            + google feltételes formázás fájlja
            + kézi javítás
            + exportálás tsv
            + posztproc
+ elkészíteni az automatikus lépések leírásait
    - emtsv használata
    - köztes preproc és posztprtoc szkriptek használata
    - zérónévmásbeszúró használata
    - anaforafeloldó használata
+ felújítani a zérónévmásbeszúrót, dokumentáció
    - modult csinálni az emtsv-be
+ felújítani az anaforafeloldót, dokumentáció
    - modult csinálni az emtsv-be
+ összefoglaló dokumentumot készíteni, amiben a folyamat lekövethető (fájlformátumokkal, konverziókkal stb.)
    - folyamatábra
    - reamde
