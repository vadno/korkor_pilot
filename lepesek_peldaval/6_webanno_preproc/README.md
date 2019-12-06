Ebben a lépésben előkészítjük a fájt olyan formátumúra, hogy az megfeleljen a [WebAnno](https://webanno.github.io/webanno/) annotációs segédeszköz bemenetének. Az átalakítást egy rövid parancs végzi el:

    cat [file] | awk -F $'\t' ' { t = $4; $4 = $5; $5 = t; print; } ' OFS=$'\t'

A lépés bemenete: [5_emtsv/globv_10.conll](../5_emtsv/globv_10.conll)