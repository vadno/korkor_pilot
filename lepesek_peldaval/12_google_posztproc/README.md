Ebben a lépésben a kézzel ellenőrzött és javított, tsv-ként exportált fájlt dolgozzuk fel. A szkript az annotátor által kijavított vagy beírt anaforikus és koreferenciakapcsolatokat veszi figyelembe. Ha az annotátor módosít a szóalakok, a tövön, a morfológiai címkén vagy a függőségi elemzésen, akkor az erre a javításra szolgáló cellák tartalmát is feldolgozza a szkript. Emellett formátumkonverzió is történik, amikor a fájlt ismét az emtsv saját formátumára alakítjuk.

A posztprocesszálást végző szkript: [koref_postproc.py](../../szkriptek/koref_postproc.py)

A lépés bemenete: [11_google_kezi/globv_10.tsv](../11_google_kezi/globv_10.tsv)
