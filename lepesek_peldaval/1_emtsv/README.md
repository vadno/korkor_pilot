Az elemzett fájl előállításához az [emtsv](https://github.com/dlt-rilmta/emtsv) moduláris elemzőeszközt használtam a következő modulok működtetésével:

1. tokenizálás: emtoken (tok)
1. morfológiai elemzés és tövesítés: emmorph (morph)
1. egyértelműsítés: emtag (pos)

A modulok egyesével is megadhatók, de a `tok-pos` preset is ugyanezeket a modulokat működteti. Az emtsv használatával kapcsolatban a részleteket lásd [itt](https://github.com/dlt-rilmta/emtsv)!

A lépés bemenete: [0_pelda_raw/globv_10.txt](../0_pelda_raw/globv_10.txt)
