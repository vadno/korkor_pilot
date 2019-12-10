# feladatok

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
    
    
# lépések

## 1. elemzés az emts-vel
emtsv használati módjai, hivatkozás az emtsv-re

emtoken, emmorph, emtag  
bemenet: folyószöveg  
kimenet: xtsv
    
## 2. fájl előkészítése a kézi ellenőrzésre

tag_preproc.py
bemenet: xtsv  
kimenet: tsv a google spreadsheetshez
    
## 3. kézi javítás a google spreadsheetsben  
rövid feladatleírás, annotálási útmutató

bemenet: tsv, fájl a feltételes formázásokkal, importálás  
kimenet: exportált csv
    
## 4. a google spreadsheetsből nyert fájl feldolgozása

tag_postproc.py  
bemenet: csv  
kimenet: xtsv
    
## 5. elemzés az emtsv-vel

emdep, emconll    
bemenet: xtsv  
kimenet: conll-u
    
## 6. fájl előkészítése a webannóra
webannó rövid ismertetése, hivatkozása

    cat [file] | awk -F $'\t' ' { t = $4; $4 = $5; $5 = t; print; } ' OFS=$'\t'

dep_preproc.sh (egy awk parancs, oszlopokat cserélget)  
bemenet: conll-u  
kimenet: conll-u a webannónak
    
## 7. kézi javítás a webannóban  
rövid feladatleírás, annotálási útmutató és a hozzá tartozó gyik

bemenet: conll-u  
kimenet: conll-u
    
## 8. zérólétigék, elliptált igék kézi beszúrása az annotatrixban  
rövid feladatleírás, annotálási útmutató

bemenet: conll-u  
kimenet: conll-u

## 9. zérónévmások beszúrása
használat, rövid leírás

pro.py  
bemenet: conll-u  
kimenet: conll-u
    
## 10. anaforikus kapcsolatok beszúrása
használat, rövid leírás  

ana.py  
bemenet: conll-u  
kimenet: conll-u
    
## 11. kézi javítás és koreferenciabeszúrás a google spreadsheetsben  
rövid feladatleírás, annotálási útmutató

bemenet: tsv, fájl a feltételes formázásokkal, importálás
kimenet: exportált tsv

## 12. a google spreadsheetsből nyert fájl feldolgozása  

proc.py  
bemenet: tsv  
kimenet: xtsv
    
## 13. korpuszfájlok előállítása
összesimítja a tsv oszlopait azokkal, amelyek a webanno miatt elvesztek  

merge.py  
bemenet: xtsv  
kimenet: xtsv