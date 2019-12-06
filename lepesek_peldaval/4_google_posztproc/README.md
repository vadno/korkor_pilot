Ebben a lépésben a kézzel ellenőrzött és javított, csv-ként exportált fájlt dolgozzuk fel és készítjük elő a következő lépés, a függőségi elemző számára. A szkript az annotátor által megjelölt vagy beírt helyes címkét és tövet veszi figyelembe. Emellett a tokenizálási hibák javítására kézzel beírt parancsokat az exportált fájl feldolgozásakor automatikusan értelmezi és azoknak megfelelően módosítja a tokenizálást (sort töröl vagy sort szúr be az annotátor által megadott tartalommal). Emellett formátumkonverzió is történik, amikor a fájlt az emtsv saját formátumára alakítjuk. A kézi javítás után a szöveg tehát pontosan ugyanúgy néz ki, mint javítás előtt (az 1_emtsv lépés után), különbség az egyes mezők tartalmában van.

A posztprocesszálást végző szkript: [tag_postproc.py](../../szkriptek/tag_postproc.py)

A lépés bemenete: [3_google_kezi/globv_10.csv](../3_google_kezi/globv_10.csv)
