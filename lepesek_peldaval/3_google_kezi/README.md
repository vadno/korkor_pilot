Ebben a lépésben történik a tokenizálás és az egyértelműsítés kimenetének kézi ellenőrzése és javítása. Ehhez egy Google Spreadsheets táblázatot használunk.

A szöveg minden egyes tokenjéhez az emtag egyértelműsítő modul által megadott elemzés alá felsorakozik az adott token összes szóbajöhető elemzése, amelyeket az emmorph morfológiai elemző és tövesítő modulja ad. Az annotátor feladata eldönteni, hogy az egyértelműsítés kimenete helyes-e, ha nem, akkor a lehetséges elemzések közül melyik helyes, valamint ha egyik se helyes, akkor be kell vinnie a helyes elemzést és tövet. A felületen a tokenizálás javítására is lehetőség van. A részleteket lásd az [annotálási útmutatóban](../../utmutatok/emmorph_checker_guide.pdf)!

Az üres táblázatfájl az annotáláshoz: [emtag.xlsx](../../google_spreadsheets_fajlok/emtag.xlsx)

Az üres táblázatfájl Microsoft Excelben és Libre Office-ban is használható, de Google Spreadsheets-be is importálható, így a munka kollaboratívan is végezhető.

A lépés bemenete: [2_google_preproc/globv_10.tsv](../2_google_preproc/globv_10.tsv)
