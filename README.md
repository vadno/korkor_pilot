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

# Licensz
CC-BY-4.0
